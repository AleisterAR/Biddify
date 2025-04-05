from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from participants.models import Participant
import stripe
from bid.models import Auction
from django.db.models import Max
from .models import Payment
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

# Create your views here.
@csrf_exempt
def stripe_config(request):
    if request.method == "GET":
        stripe_config = {'publicKey' : settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)
    
@csrf_exempt
def create_checkout_session(request, auction_id):
    auction = Auction.objects.prefetch_related("bids").get(id=auction_id)
    highest_bid = auction.bids.order_by("-bid_amount").first()
    try:
        session = stripe.checkout.Session.create(
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
            metadata={'auction_id': auction.id},
            customer_email=request.user.email,
            mode='payment',
            success_url=f"{request.build_absolute_uri('/')}payment/success/",
            cancel_url=f"{request.build_absolute_uri('/')}payment/cancel/",
        )
        return JsonResponse({'id': session.id})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)
    
def successful_view(request):
    return render(request, "payment/success.html")

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
        session = event['data']['object']
        customer_email = session.get('customer_email')
        auction_id = session.get('metadata', {}).get('auction_id')
        payment_intent = session.get('payment_intent')
        amount_paid = session.get('amount_total') / 100
        
        if auction_id:
            auction = Auction.objects.filter(id=auction_id).first()
            if auction:
                Payment.objects.create(
                    user_email=customer_email,
                    auction=auction,
                    amount=amount_paid,
                    payment_intent=payment_intent,
                    payment_status='completed',
                    created_at=timezone.now()
                )
                winning_bid = auction.bids.order_by('-bid_amount').first()
                if winning_bid:
                    item = auction.item
                    item.owner = winning_bid.bidder
                    item.save()
    return JsonResponse({'status': 'success'})
    