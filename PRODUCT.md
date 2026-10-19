# Product

<!-- impeccable:product-schema 1 -->

## Platform

web

## Users

Biddify is a portfolio / demo project. Its real audience is the people evaluating it (reviewers, recruiters, instructors), who judge it by using it as its in-product users would.

In-product users are all registered **participants**, and any participant can be both:

- **Buyers / collectors**: they browse live lots of antiques and collectibles, bid against other collectors in real time, pay for lots they win, and track delivery.
- **Sellers**: they add objects to their inventory (photos, description, condition, year, creator, country, provenance document), schedule an auction window, ship once paid, and get paid after delivery.

**Admins** are a separate role. They manage the platform through Django admin, mark items as provenance-verified, and view dashboards.

## Product Purpose

A real-time, peer-to-peer auction platform for antiques and collectibles. Each lot gets a live countdown, bids reach everyone instantly, and outbid notifications arrive the moment they happen. Payment, shipping and tracking all happen inside Biddify, so neither side has to leave the platform or trust a stranger off-platform.

Success for the project: an evaluator can run the whole lifecycle (list, auction, bid, win, pay, ship, track) and it feels like a credible, trustworthy saleroom, not a CRUD demo.

## Positioning

The full lifecycle of a sale is live and lives in one place. Bidding is real-time over WebSockets, every lot carries its provenance (with admin verification), and Biddify holds the buyer's payment until the object has arrived. Many auction demos stop at "place a bid". Biddify continues through Stripe payment, escrow-style release, shipment and a tracking timeline.

## Operating Context

- Auction lifecycle: item in inventory → auction scheduled (start/end time) → live bidding with countdown → closed → winner pays via Stripe Checkout → shipment created → seller ships → tracking events → delivered → payment released to seller.
- Shipment statuses: Awaiting address → Label created → Shipped → In transit → Out for delivery → Delivered. Methods: Standard (3–5 business days) and Express (1–2 business days). The carrier is the fictional "Biddify Express".
- Notifications arrive over WebSockets (outbid, auction events, shipping) and can be marked read or dismissed.
- Item conditions use a fixed scale: Mint, Near Mint, Excellent, Very Good, Good, Fair, Poor.
- Server time zone is Asia/Tokyo. Prices are shown in euros (€).

## Capabilities and Constraints

- Stack: Django + Django Channels/Daphne, Django templates in `resources/views/`, Tailwind CSS 3 (with Flowbite and daisyUI plugins), Alpine.js, HTMX (including the WebSocket extension), built with Laravel Mix (`npm run dev`) and served with `python manage.py runserver`.
- Stripe runs in **test mode only**. Shipping is **mocked** (generated tracking numbers and events). These stay as they are; this is a demo.
- Bid amounts and starting prices are whole numbers (small-integer fields, max 32,767). Payments are stored as decimals.
- Escrow rule (confirmed as the intended commitment): Biddify holds the buyer's payment until 3 days after the object is received, or until the seller confirms pickup with no complaint raised. Then it is released to the seller. Copy and design may state and reinforce this rule. Enforcement in code may lag behind it.
- Uploaded media (item images, provenance documents) live in `localstorage/` and are not committed.

## Brand Commitments

- Name: **Biddify** (the Django project package is `keister_house`, which is not user-facing).
- The voice in the current copy (seen in the repo; the user has not yet confirmed it as binding): plain, warm, saleroom vocabulary ("lot", "the saleroom is quiet", "when the hammer falls", "under the hammer"), second person, British spelling ("favour").

## Evidence on Hand

- Real product copy: home page, How it works (`resources/views/utilities/about_us.html`), and the buyer and seller step flows.
- There are no real customers, testimonials, sales figures, press or partner logos. Future work must not invent any. Lot data is whatever exists in the local database.

## Product Principles

1. **Live means live.** The current bid, the countdown and the standing (leading or outbid) must always be accurate and update instantly. A stale price breaks the whole premise.
2. **Trust is the product.** Provenance, verification, held payment and tracking are what make a stranger-to-stranger sale safe. Surface them where decisions get made.
3. **One place, end to end.** Every step from listing to delivery should feel like part of the same saleroom, never a hand-off to a bolted-on flow.
4. **Both sides of the table.** Every participant can be a buyer and a seller. Neither role is an afterthought.
5. **Honest demo.** Show the real mechanics working. Never fake scale, social proof or claims beyond what the product does.
