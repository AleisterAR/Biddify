from django.urls import path
from django.shortcuts import redirect
from .views import stripe_config, create_checkout_session, successful_view, cancelled_view, stripe_webhook

urlpatterns = [
    path("get_stripe_config/", stripe_config, name="get_stripe_config"),
    path("create_checkout_session/<int:auction_id>/", create_checkout_session, name="create_checkout_session"),
    path("success/", successful_view, name="success"), 
    path("cancel/", cancelled_view, name="cancel"),
    path('stripe/webhook/', stripe_webhook, name='stripe-webhook'),
]