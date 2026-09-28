---
tags: [concept, rewards, exclusion]
---

# Krungsri-family 7-11 / TrueMoney points exclusion

Effective **2026-08-08** (announced by the user that day, applied to rows dated
from **2026-08-01** onward): on cards in the **Krungsri family**, transactions at
**7-Eleven** and at **TrueMoney** no longer earn reward points.

This is a **points-only** withdrawal. Cashback is untouched — see
[[#cashback-is-unaffected]] below.

## What the rule covers

| Merchant shape | Example | Points |
|---|---|:--:|
| 7-Eleven, direct swipe | `7-11 Bangkok TH` | ×0 |
| 7-Eleven via TrueMoney | `TMN 7-11 BANGKOK TH`, `TMN*TMN 7-11 BANGKOK TH` | ×0 |
| Any other TrueMoney charge | `TMN*PROMPTPAY30 BANGKOK TH`, `TMN*LOTUS BANGKOK TH`, `TMN*FAST FOOD BANGKOK TH`, `TMN MAKRO …` | ×0 |

"TrueMoney" is matched on the merchant-string **prefix** (`TMN ` / `TMN*`) so an
unrelated merchant that happens to contain the letters `TMN` mid-string doesn't
trip the rule. 7-Eleven is matched anywhere in the string.

Note that the rule catches **all** TrueMoney activity, not just the 7-Eleven
top-ups: `TMN*PROMPTPAY30` is a PromptPay transfer routed through TrueMoney
(see [[../../CLAUDE|CLAUDE.md]] and the TMN merchant-string note), and it is
excluded like every other `TMN*` row.

## Which cards carry it

| Card | Issuer | Excluded? |
|---|---|:--:|
| [[../cards/_stubs\|First Choice]] | Krungsri | ✅ |
| Krungsri JCB | Krungsri | ✅ |
| Krungsri NOW | Krungsri | ✅ |
| Krungsri Visa | Krungsri | ✅ |
| [[../cards/lotuss-beyond\|Lotus's Beyond]] | Lotus | ❌ **exempt** |
| CardX JCB | CardX | ❌ **out of scope** |

### Why Lotus's Beyond is exempt

Lotus's, 7-Eleven and TrueMoney are all **CP ALL** businesses. The issuer has no
reason to withhold points when the cardholder spends inside the same
conglomerate that runs the card's own retail programme, so 7-11 and TrueMoney
rows keep earning on Lotus's Beyond. The exemption is recorded as a comment in
`scripts/repositories/cards/lotuss-beyond.yaml` — deliberately *not* as a flag,
so nobody "completes" the set by adding one.

### CardX JCB is not in the family at all

CardX belongs to the **SCB X** group — a completely different financial group
from Krungsri (user, 2026-08-08). The only thing it shares with the Krungsri
cards is the `bill_cycle_pattern: krungsri` key, which describes a BC/DD *shape*
(day 5, +20 days) and nothing about corporate affiliation.

Don't read the shared pattern key as family membership — a `cardx-jcb.yaml`
comment previously called CardX "a Krungsri spinoff", which was wrong and has
been corrected in place. Krungsri-family rules do not reach this card.

## Cashback is unaffected

First Choice's cashback promotions still pay out at 7-11 / TrueMoney. The user
adjusts First Choice cashback by hand anyway (see
[[promotions]] and the First Choice section of
`.claude/skills/add-transaction/SKILL.md`), so the rule deliberately does not
touch `% cb`.

Mechanically: `lib.promotions.classify` layers this exclusion **on top of** the
promo result as step 6, overriding `points_override` to `×0` while passing
`cashback_percent` through unchanged. A row can therefore legitimately carry
`% cb = 2%` *and* `×0` — that is not a data-entry error.

## How it's encoded

A rule of the Krungsri card family: `KrungsriFamilyCard` in
`scripts/python/lib/earning/families.py` (until 2026-09-28 a YAML flag,
`truemoney_711_points_exclusion`). `lib.promotions.classify` runs it and tags the reason
`<base-reason>+truemoney-711-points-exclusion` and writes this `Note`:

> 7-11 / TrueMoney — Krungsri-family cards earn no reward points at these merchants.

Because it runs inside `classify`, `/add-transaction` with `auto_classify: true`
applies it automatically — no manual `multiplier` needed on these rows. Rows
already excluded by a stronger rule (foreign-in-THB, petrol, a card whose
`points_default` is already `×0`) are left alone rather than double-noted.

## Related

- [[points-and-multipliers]] — the multiplier model this writes into.
- [[cashback]] — the `% cb` axis the rule leaves alone.
- [[promotions]] — why rewards are promotion-driven, and where card-level rules sit instead.
- [[../cards/lotuss-beyond]] — the exempt card.
- [[../cards/uob-makro]] — a different TrueMoney interaction: `TMN MAKRO` *restores* normal earning where a standalone `MAKRO_…` swipe would not. On UOB, not Krungsri.
