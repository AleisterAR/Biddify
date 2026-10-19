from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http.response import JsonResponse
import stripe
from bid.models import Auction
from .models import Payment
from shipping.models import Shipment
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY


def completed_payment(auction):
    """The winner is the only person who can pay for a lot, so a completed payment for the auction settles it."""
    return Payment.objects.filter(auction=auction, payment_status='completed').first()


def record_checkout(session):
    """Record a paid Checkout Session exactly once.

    Called from both the webhook and the success page, so a payment is never lost
    when the webhook is late or not forwarded (e.g. `stripe listen` isn't running in development).
    Returns the Payment, or None if the session isn't a paid session for a known auction.
    """
    # stripe-python >= 7 objects are no longer dicts, so .get() needs a plain dict
    if hasattr(session, 'to_dict'):
        session = session.to_dict()
    if session.get('payment_status') != 'paid':
        return None
    auction_id = (session.get('metadata') or {}).get('auction_id')
    auction = Auction.objects.filter(id=auction_id).select_related('item').first() if auction_id else None
    if not auction:
        return None
    winning_bid = auction.bids.select_related('bidder').order_by('-bid_amount').first()
    customer_details = session.get('customer_details') or {}
    email = session.get('customer_email') or customer_details.get('email') or (winning_bid.bidder.email if winning_bid else '')
    # Stripe may deliver the webhook and the success redirect in either order, so key on the payment intent
    payment, created = Payment.objects.get_or_create(
        payment_intent=session.get('payment_intent') or session.get('id'),
        defaults={
            'user_email': email,
            'auction': auction,
            'amount': session.get('amount_total', 0) / 100,
            'payment_status': 'completed',
            'created_at': timezone.now(),
        }
    )
    if created and winning_bid:
        item = auction.item
        # Record the seller before ownership moves to the buyer
        Shipment.objects.get_or_create(payment=payment, defaults={'auction': auction, 'buyer': winning_bid.bidder, 'seller': item.owner})
        item.owner = winning_bid.bidder
        item.save()
    return payment


# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey' : settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)

@login_required
def create_checkout_session(request, auction_id):
    auction = Auction.objects.select_related("item").filter(id=auction_id).first()
    if auction is None or not auction.auction_ended():
        return JsonResponse({'error': "This lot can't be paid for yet."}, status=400)
    highest_bid = auction.bids.order_by("-bid_amount").first()
    if highest_bid is None or highest_bid.bidder_id != request.user.id:
        return JsonResponse({'error': "Only the winning bidder can pay for this lot."}, status=403)
    if completed_payment(auction):
        return JsonResponse({'error': "This lot has already been paid for."}, status=409)
    try:
        session_args = dict(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': 'eur',
                    'product_data': {
                        'name': f'Payment for Item: {auction.item.name}',
                    },
                    'unit_amount': int(float(highest_bid.bid_amount) * 100),
                },
                'quantity': 1,
            }],
            metadata={'auction_id': auction.id, 'user_id': request.user.id},
            mode='payment',
            # Stripe fills in the session id, so the success page can confirm the payment itself
            success_url=f"{request.build_absolute_uri('/')}payment/success/?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=f"{request.build_absolute_uri('/')}payment/cancel/",
        )
        if request.user.email:
            session_args['customer_email'] = request.user.email
        session = stripe.checkout.Session.create(**session_args)
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@login_required
def successful_view(request):
    payment = shipment = None
    session_id = request.GET.get('session_id')
    if session_id:
        try:
            session = stripe.checkout.Session.retrieve(session_id).to_dict()
            if str((session.get('metadata') or {}).get('user_id')) == str(request.user.id):
                payment = record_checkout(session)
        except stripe.error.StripeError:
            payment = None
    if payment is not None:
        shipment = Shipment.objects.filter(payment=payment).first()
    return render(request, "payment/success.html", {"payment": payment, "shipment": shipment})

def cancelled_view(request):
    return render(request, "payment/cancel.html")

@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get('HTTP_STRIPE_SIGNATURE', '')
    endpoint_secret = settings.STRIPE_WEBHOOK_SECRET
    try:
        event = stripe.Webhook.construct_event(payload, sig_header, endpoint_secret)
    except ValueError:
        return JsonResponse({'error': 'Invalid payload'}, status=400)
    except stripe.error.SignatureVerificationError:
        return JsonResponse({'error': 'Invalid signature'}, status=400)

    if event['type'] == 'checkout.session.completed':
        record_checkout(event['data']['object'])
    return JsonResponse({'status': 'success'})
