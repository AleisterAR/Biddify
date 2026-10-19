---
target: current theme
total_score: 24
max_score: 40
na_heuristics: 
p0_count: 0
p1_count: 4
target_identity: "file:C:\\Users\\thuta.DOINET\\Work\\biddify\\resources\\views"
timestamp: 2026-10-19T00-32-37Z
slug: resources-views
---
Method: dual-agent (A: design review · B: detector + CDP screenshots)

## Design Health Score — 24/40 (Acceptable)
| # | Heuristic | Score | Key Issue |
|---|---|---|---|
| 1 | Visibility of System Status | 3 | No WebSocket connection state; home first paints false "No bids placed yet" (home.html:72) |
| 2 | Match System / Real World | 3 | Blue "brass", red "Live" undercut saleroom metaphor |
| 3 | User Control and Freedom | 2 | Login drops `next`; reload on close (app.js:460) wipes typed bid |
| 4 | Consistency and Standards | 2 | Red = Live + Outbid + final seconds; Flowbite blue/gray leftovers in item_list.html |
| 5 | Error Prevention | 2 | No persistent minimum-next-bid; no sanity check on typed bid |
| 6 | Recognition Rather Than Recall | 3 | Quick-bid chips, breadcrumb, labels |
| 7 | Flexibility and Efficiency | 2 | No sort/watchlist; filters not in URL |
| 8 | Aesthetic and Minimalist Design | 3 | Restrained; palette generic |
| 9 | Error Recovery | 2 | Shouting/garbled errors; register failures silent |
| 10 | Help and Documentation | 2 | Escrow/bid rules only on About |

## Design Specificity Verdict
Half-authored. Type + lot-tag motif + saleroom copy are product-specific; palette is stock Tailwind slate/blue-600/emerald ("brass" = #3B82F6; gallery≈canvas 1.04:1); page skeletons template-generic.
Detector: file scan 0 findings but color rules blind ({% static %} unresolved). URL scans: low-contrast Live chip #DC2626/#FEE2E2 4.0:1 (real); skipped-heading /auction/ h1→h3 (real); skipped-heading /login/ (false positive, debug toolbar); bounce-easing global.css:118 (deliberate). Screenshots: Bodoni heading line collisions (auth_base.html:17, display-xl); live price renders "€ I 40". No overflow/console errors/font fallbacks. No overlay (no injection-capable browser).

## Priority Issues
1. [P1] Palette contradicts the product; red overloaded; 3 chips <4.5:1 — re-author tokens (paper/ink/brass/one deep accent; Live own hue; red only outbid/final minute). /impeccable colorize
2. [P1] Live bid figures in hairline Bodoni illegible ("€ I 40"); tight display leading collides — tabular sturdier figures, loosen leading. /impeccable typeset
3. [P1] Trust claims overstated (footer provenance, "curated", "shipping included") and absent at decision points (no Verified mark, no escrow line at Pay). /impeccable clarify
4. [P1] focus:outline-none on lot cards/hero tag; invalid a>button notification rows; hover-only menus. /impeccable harden
5. [P2] First run (false empty state, login wall, `next` dropped) and hammer moment = page reload. /impeccable onboard, /impeccable animate

## Persona Red Flags
Jordan: false empty state; login wall then home; validation on focus; no binding/min-bid info.
Casey: 36px chips; nested 320px scroll; hover menus; reload wipes input; truncated placeholder.
Sam: no focus on lot cards/hero; notifications unreachable; Provenance label lacks for; h1→h3; chips never say "live".

## Minor Observations
.button-ink 1.22:1 (unused); dead bidding_list.html; seconds on 43-day countdown; duplicate hero/contested lot; Lot NNN = auction id; won-lot inventory copy stale after payment; Sign out styled destructive; "agreee" typo; auth aside half-screen/vanishes on mobile; success page leaves navbar; debug toolbar expanded.

## Questions to Consider
- Why is the most-clicked colour Tailwind link blue in a saleroom?
- Why is the hammer falling a page refresh?
- Can a buyer tell a verified lot from an unverified one in the grid?
