---
tags: [card, uob, points, merchant-bonus]
issuer: UOB
holders: [takumi, baiboon]
points: integer
---

# UOB Makro

UOB's Makro co-brand card. Earns integer points across the board, with a built-in differentiation between **in-store Makro purchases** and **everything else** that the Notion multiplier enum encodes via the `÷4` checkbox.

## Earning rules

| Where | Rate | Notion encoding |
|---|---|---|
| In-store Makro (merchant string starts with `MAKRO`)  | **100 ฿ → 1 pt** | `÷4` (the standard 25 ฿ → 1 pt rate divided by 4) |
| Anything via TrueMoney (merchant string starts with `TMN`) — *including* `TMN*MAKRO …` | **25 ฿ → 1 pt** | no multiplier (default `×1`) |
| General (everywhere else)                             | **25 ฿ → 1 pt**  | no multiplier (default `×1`) |

Notes:

- Integer points only — no fractional accumulation like [[lotuss-beyond]].
- The `÷4` checkbox is what the user uses to mark "this row earned at the in-store-Makro rate". The reason the user chose `÷4` (rather than introducing a custom integer multiplier) is that the Notion checkbox UI has a fixed enum and `÷4` of the 25 ฿ rate gives the right 100 ฿ → 1 pt result.
- **The bonus is the *worse* rate, not the better one.** In-store Makro earns *fewer* points per baht than other merchants — this is the only example in the household where the per-merchant rule reduces rather than amplifies earning. The card is positioned as a Makro-loyalty card, so this is presumably traded against a separate Makro-cashback or discount layer outside this system.

## Routing rule (the "is this really an in-store Makro swipe?" check)

The `÷4` rate applies **only** when the transaction was physically read by Makro's in-store card reader. The merchant-string signal:

- `MAKRO …` (no prefix) → in-store card reader, **`÷4` applies**.
- `HTTPS://WWW.MAKRO.PRO/ BANGKOK TH` → Makro online; goes through the regular payment processor, not Makro's in-store reader. **Treated as a regular merchant** on the general 25 ฿ → 1 pt rate. Working assumption until contradicted by a statement.
- `TMN*MAKRO …` (TrueMoney top-up at a Makro counter) → routed through TrueMoney's processor, *not* Makro's in-store reader. **`÷4` does not apply**; falls back to 25 ฿ → 1 pt.
- Any other `TMN*…` → not Makro, regular 25 ฿ → 1 pt rate.

The common thread: the `÷4` rate is conditional on the **physical reader**, not the merchant brand. TrueMoney intermediation breaks the connection.

## Cashback, and standalone `MAKRO` on *other* UOB cards

Two clarifications from the user (2026-07-13) that the points table above doesn't capture:

- **Cashback**: standalone in-store `MAKRO_…` earns **no cashback** on any UOB card — including UOB Makro (leave `% cb` unset). `HTTPS://WWW.MAKRO.PRO/…` and `TMN*MAKRO …` are ordinary merchants and *are* eligible for cashback under whatever promo the card runs.
- **The `÷4` rate is UOB-Makro-only.** Standalone `MAKRO_…` on a **non-Makro UOB card** (UOB One / UOB World / UOB Premier) earns **`×0` points and no cashback** — *not* `÷4`. Only the UOB Makro co-brand card applies the reduced Makro rate; every other UOB card zeroes standalone in-store Makro entirely.

So the merchant string alone isn't enough — the `÷4`-vs-`×0` split depends on *which UOB card* the row sits on. The historical `MAKRO_…` rows on Baiboon's UOB World / Premier / One are correctly `×0` and should stay that way. Cross-ref: memory `project_card_uob_makro`, and the `/add-transaction` skill's Makro card-policy section.

## Notion encoding

The `÷4` checkbox is the cleanest fit on the fixed-enum UI but it's still a *projection* of the true rule — the underlying rule is "this transaction earns at the Makro rate". The phase-2 app should model this as an `EarningRule` on the card that matches merchant-substring `MAKRO` (anchored start) → 1 pt per 100 ฿, and a base rule of 1 pt per 25 ฿ for everything else. See [[../future-app/data-model-target]] and [[../concepts/points-and-multipliers#approximation-caveat]].

## See also

- [[_stubs|Card stub index]]
- [[../concepts/points-and-multipliers]] — explains the Notion enum + its limitations.
- Memory: `project_points_earning_complexity` — the cross-card framing.
