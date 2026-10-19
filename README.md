# 🏷️ Biddify – Real-Time Auction Website

**Biddify** is a full-stack real-time online auction platform that allows users to register, list items, and bid on antiques or collectibles with live countdowns and dynamic bidding updates. Built with Django, Django Channels, and WebSockets, Biddify delivers seamless user experiences and interactive bidding functionalities.


## 🔧 Tech Stack

- **Backend**: Django, Django Channels, Daphne
- **Frontend**: HTML, Tailwind CSS, Alpine.js, HTMX
- **Database**: PostgreSQL / MySQL (configurable)
- **Real-time**: WebSockets (via Django Channels)
- **Auth**: Custom User Model with permissions
- **Media Handling**: Django Media Files
- **Payments**: Stripe (test mode)

## ✨ Features

- 🔐 User Registration & Login (Admin & Participant roles)
- 📦 Item Listing with provenance and condition fields
- 🖼️ Multi-image upload and preview for items
- ⏱️ Real-time auction countdowns
- 💰 Live bidding system with instant updates
- 🔔 WebSocket-based bid and auction notifications
- 📊 Visual dashboards with `django-admin-charts`
- 💳 Stripe integration for payments (test mode)
- 📦 Mock shipping with tracking numbers and a live tracking timeline

## 🚀 Getting Started

### 1. Create and activate virtual environment
```bash
python -m venv venv
source venv/bin/activate
```
### 2. Install dependencies
```bash
pip install -r requirements.txt
npm install
```
### 3. Setup database
Inside the **keister_house** folder there will be a file named **settings.py**, and it needs to be configured as below.
```bash
DATABASES  = {
	'default': {
	'ENGINE': 'django.db.backends.mysql', #currently using MySQL
	'NAME': '[your_database_name]',
	'USER': '[your_database_user_name]',
	'PASSWORD':'[your_database_password]',
	'HOST' : '[your_database_hostname]',
	'PORT':'[your_database_port_number]',
	}
}
```
### 4. Create a Stripe account and setup keys

As a prerequisite, you will have to create a Stripe account and in developer dashboard you will be provided with a Publishable Key and a Secret Key. Inside the **settings.py** configure as below.
```python
STRIPE_PUBLISHABLE_KEY  =  "[your_stripe_publishable_key]"
STRIPE_SECRET_KEY  =  "[your_stripe_secret_key]"
```
As the next step, install stripe-cli, this will differ according to the operating system, so it is recommended to check out the [🔗documentation](https://docs.stripe.com/stripe-cli). Next run the following commands to login to Stripe account and get Webhook Secret Key.
```bash
stripe login
stripe listen --events checkout.session.completed --forward-to localhost:8000/payment/stripe/webhook/
```
A Webhook Secret Key will be generated for you, so place it in **settings.py** as well.
```python
STRIPE_WEBHOOK_SECRET="[your_webhook_secret_key]"
```
### 5. Database migrations
```bash
python manage.py makemigrations
python manage.py migrate
```

### 6. Running the server
```bash
python manage.py runserver
npm run dev
```

## 📦 Shipping (mock carrier)

Shipping is simulated: no real carrier is contacted and no parcels are sent.

1. When Stripe confirms a payment, a shipment is created for the winning bidder.
2. The buyer enters a delivery address (**Shipments** in the user menu, or **Enter shipping details** on the item page). A fake `BDF…EU` tracking number is then generated.
3. The seller clicks **Mark as shipped**.
4. The mock carrier moves the parcel through *In transit → Out for delivery → Delivered*, one step every `MOCK_SHIPPING_STEP_SECONDS` (default 120, half that for express). Buyer and seller get notifications along the way.

While `DEBUG = True`, the tracking page has a **Simulate next carrier scan** button so you can skip the wait. Staff can also advance shipments from the Django admin.
