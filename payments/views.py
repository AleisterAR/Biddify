from django.shortcuts import render
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
import stripe
from bid.models import Auction
from django.db.models import Max

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