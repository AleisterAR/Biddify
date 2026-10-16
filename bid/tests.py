from datetime import timedelta
from asgiref.sync import async_to_sync
from channels.testing import WebsocketCommunicator
from django.test import TransactionTestCase
from django.utils import timezone
from participants.models import Participant
from item.models import Item
from bid.models import Auction, Bid
from bid.consumers import AuctionConsumer


class AuctionConsumerTests(TransactionTestCase):
    def setUp(self):
        self.seller = Participant.objects.create_user(username="seller", email="seller@example.com", password="pw")
        self.alice = Participant.objects.create_user(username="alice", email="alice@example.com", password="pw")
        self.bob = Participant.objects.create_user(username="bob", email="bob@example.com", password="pw")
        item = Item.objects.create(name="Old Clock", owner=self.seller, starting_price=10)
        now = timezone.now()
        self.auction = Auction.objects.create(item=item, starting_time=now - timedelta(hours=1), ending_time=now + timedelta(hours=1))
        Bid.objects.create(auction=self.auction, bidder=self.bob, bid_amount=20)

    async def _connect(self, user):
        communicator = WebsocketCommunicator(AuctionConsumer.as_asgi(), f"/ws/auction/{self.auction.id}/")
        communicator.scope["user"] = user
        communicator.scope["url_route"] = {"kwargs": {"auction_id": str(self.auction.id)}}
        connected, _ = await communicator.connect()
        self.assertTrue(connected)
        return communicator

    def test_rejected_bid_is_only_shown_to_the_bidder(self):
        async def scenario():
            alice, bob = await self._connect(self.alice), await self._connect(self.bob)
            await alice.send_json_to({"bid_amount": "5", "user_id": self.alice.id})
            self.assertIn("must be more than the previous bid", await alice.receive_from())
            self.assertTrue(await bob.receive_nothing())
            await alice.disconnect()
            await bob.disconnect()
        async_to_sync(scenario)()

    def test_accepted_bid_tells_each_viewer_where_they_stand(self):
        async def scenario():
            alice, bob = await self._connect(self.alice), await self._connect(self.bob)
            await alice.send_json_to({"bid_amount": "30", "user_id": self.alice.id})
            to_alice, to_bob = await alice.receive_from(), await bob.receive_from()
            self.assertIn("You're the highest bidder", to_alice)
            self.assertIn("You've been outbid", to_bob)
            for html in (to_alice, to_bob):
                self.assertIn('id="current-bid"', html)
                self.assertIn("30", html)
            await alice.disconnect()
            await bob.disconnect()
        async_to_sync(scenario)()
