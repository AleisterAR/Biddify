from datetime import timedelta
from unittest import mock
from django.test import TestCase, override_settings
from django.urls import reverse
from django.utils import timezone
from participants.models import Participant
from item.models import Item
from bid.models import Auction, Bid, Notification
from payments.models import Payment
from shipping.models import Shipment
from shipping import carrier

ADDRESS = {
    "recipient_name": "Ada Buyer",
    "phone": "+31 600000000",
    "address_line": "Damrak 1",
    "city": "Amsterdam",
    "postal_code": "1012 LG",
    "country": "Netherlands",
    "method": "standard",
}


@override_settings(MOCK_SHIPPING_STEP_SECONDS=60, DEBUG=True)
class ShippingFlowTests(TestCase):
    def setUp(self):
        self.seller = Participant.objects.create_user(username="seller", email="seller@example.com", password="pw")
        self.buyer = Participant.objects.create_user(username="buyer", email="buyer@example.com", password="pw")
        self.item = Item.objects.create(name="Old Clock", owner=self.seller, starting_price=10)
        now = timezone.now()
        self.auction = Auction.objects.create(item=self.item, starting_time=now - timedelta(days=2), ending_time=now - timedelta(days=1))
        Bid.objects.create(auction=self.auction, bidder=self.buyer, bid_amount=50)

    def _send_webhook(self, payment_intent="pi_123"):
        event = {"type": "checkout.session.completed", "data": {"object": {
            "customer_email": self.buyer.email,
            "metadata": {"auction_id": str(self.auction.id)},
            "payment_intent": payment_intent,
            "amount_total": 5000,
        }}}
        with mock.patch("payments.views.stripe.Webhook.construct_event", return_value=event):
            return self.client.post(reverse("stripe-webhook"), data=b"{}", content_type="application/json")

    def _paid_shipment(self):
        self._send_webhook()
        return Shipment.objects.get(auction=self.auction)

    def _labelled_shipment(self):
        shipment = self._paid_shipment()
        Shipment.objects.filter(id=shipment.id).update(**ADDRESS)
        return carrier.create_label(Shipment.objects.get(id=shipment.id))

    def test_webhook_creates_shipment_with_original_seller(self):
        shipment = self._paid_shipment()
        self.item.refresh_from_db()
        self.assertEqual(shipment.seller, self.seller)
        self.assertEqual(shipment.buyer, self.buyer)
        self.assertEqual(shipment.status, "awaiting_address")
        self.assertEqual(self.item.owner, self.buyer)

    def test_webhook_retry_is_idempotent(self):
        self._send_webhook()
        response = self._send_webhook()
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Payment.objects.count(), 1)
        self.assertEqual(Shipment.objects.get().seller, self.seller)

    def test_buyer_submits_address_and_gets_label(self):
        shipment = self._paid_shipment()
        self.client.force_login(self.buyer)
        response = self.client.post(reverse("shipping_details", args=[shipment.id]), ADDRESS)
        self.assertRedirects(response, reverse("track_shipment", args=[shipment.id]))
        shipment.refresh_from_db()
        self.assertEqual(shipment.status, "label_created")
        self.assertRegex(shipment.tracking_number, r"^BDF\d{10}EU$")
        self.assertIsNotNone(shipment.estimated_delivery)
        self.assertTrue(Notification.objects.filter(user=self.seller).exists())

    def test_only_buyer_can_enter_address(self):
        shipment = self._paid_shipment()
        self.client.force_login(self.seller)
        response = self.client.post(reverse("shipping_details", args=[shipment.id]), ADDRESS)
        self.assertEqual(response.status_code, 404)

    def test_only_seller_can_mark_shipped(self):
        shipment = self._labelled_shipment()
        self.client.force_login(self.buyer)
        self.assertEqual(self.client.post(reverse("mark_shipped", args=[shipment.id])).status_code, 404)
        self.client.force_login(self.seller)
        self.client.post(reverse("mark_shipped", args=[shipment.id]))
        shipment.refresh_from_db()
        self.assertEqual(shipment.status, "shipped")

    def test_outsider_cannot_track(self):
        shipment = self._paid_shipment()
        outsider = Participant.objects.create_user(username="other", email="other@example.com", password="pw")
        self.client.force_login(outsider)
        self.assertEqual(self.client.get(reverse("track_shipment", args=[shipment.id])).status_code, 403)

    def test_mock_carrier_progresses_over_time(self):
        shipment = self._labelled_shipment()
        carrier.mark_shipped(shipment)

        shipment.shipped_at = timezone.now() - timedelta(seconds=130)
        shipment.save()
        carrier.sync(shipment)
        self.assertEqual(shipment.status, "out_for_delivery")

        shipment.shipped_at = timezone.now() - timedelta(hours=1)
        shipment.save()
        carrier.sync(shipment)
        self.assertEqual(shipment.status, "delivered")
        self.assertIsNotNone(shipment.delivered_at)
        statuses = list(shipment.events.values_list("status", flat=True))
        self.assertEqual(sorted(statuses), sorted(["label_created", "shipped", "in_transit", "out_for_delivery", "delivered"]))

    def test_pages_render(self):
        shipment = self._paid_shipment()
        self.client.force_login(self.buyer)
        self.assertContains(self.client.get(reverse("shipments")), "Old Clock")
        self.assertContains(self.client.get(reverse("shipping_details", args=[shipment.id])), "Confirm address")
        self.assertContains(self.client.get(reverse("item_detail", args=[self.item.id])), "Enter shipping details")
        self.client.post(reverse("shipping_details", args=[shipment.id]), ADDRESS)
        self.assertContains(self.client.get(reverse("track_shipment", args=[shipment.id])), Shipment.objects.get().tracking_number)
        self.assertContains(self.client.get(reverse("item_detail", args=[self.item.id])), "Track shipment")
