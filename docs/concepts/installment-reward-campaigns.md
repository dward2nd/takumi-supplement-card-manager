---
tags: [concept, rewards, exclusion, installments]
---

# Installment reward campaigns

An installment plan's rewards don't always follow the card's normal policy. Three
distinct mechanisms are in play across the portfolio, and they differ in *where
the deciding fact lives* — which is what makes this worth a concept note rather
than a line in each card's file.

| Mechanism | Scope | Points | Cashback | Where it's encoded |
|---|---|:--:|:--:|---|
| Rewards paid upfront | Krungsri family, card-level | ×0 | none | `installment_rewards_upfront` flag |
| Personal-loan credit line | First Choice, card-level | ×0 | none | same flag + `installment_note` |
| **ดีจังผ่อน 0%** (Dee-Jang) | CardX, **plan-level** | ×0 | unaffected | `installment-campaigns/dee-jang.yaml` |
| **U Plan 0%** | Krungsri / First Choice, **plan-level** | ×0 | varies by promo | `installment-campaigns/u-plan.yaml` |

## Why some of this is plan-level

`lib.promotions.classify` sees exactly three things: the card, the date, and the
merchant string. That is enough for a card-level rule — "is this an installment
row on a Krungsri card?" is answerable from the `NN/NN` suffix plus the card
name.

It is **not** enough for a campaign. Both ดีจังผ่อน and U Plan are
*post-purchase conversions*: the cardholder asks the bank to re-split a charge
that has already posted. Nothing about the merchant changes, so two plans with
byte-identical merchant strings on the same card can earn differently depending
on how each was created. No function of (card, date, merchant) can tell them
apart — the information simply isn't in the inputs.

So campaigns are recognised from the plan's own history: the `Note` written on an
earlier term. See [[#how-inheritance-works]].

## The card-level rules

### Krungsri pays installment rewards upfront

On the four `issuer: Krungsri` cards, the points and cashback for an installment
purchase are granted **in full at the moment of purchase**, not spread across the
terms (user, 2026-08-10). Each `NN/NN` term therefore earns nothing on its own —
the reward already landed on the original charge, and crediting the terms too
would double-count it.

Flag: `installment_rewards_upfront: true` in the
[[../../scripts/repositories/README|cards repository]]. It zeroes **both** axes,
unlike [[krungsri-truemoney-711-exclusion|the 7-11 / TrueMoney rule]] which is
points-only.

### First Choice runs two credit lines

First Choice is the same flag for a different reason, so it carries its own
`installment_note`. The card operates **two simultaneous credit lines**:

1. **credit card** — a pay-in-full purchase lands here and earns normally;
2. **personal loan** — a merchant-offered installment (0% interest, up to 10
   months) lands here instead.

A merchant installment therefore earns no points and no cashback because it
never touches the card line at all. That's a different product doing the
lending, not a reward exclusion — worth saying precisely, since "no cashback on
installments" invites someone to look for a promo override that cannot exist.

## The campaigns

### ดีจังผ่อน 0% — CardX

The cardholder asks CardX to convert a posted charge into 0% installments.
Converted terms earn **no points**; cashback is untouched (CardX JCB pays
cashback only on in-store foreign-currency spend anyway, so in practice this is
academic — but the campaign is written points-only because that is what was
observed).

The tell is the term count: **4 terms**, where Thai plans conventionally run 3,
6 or 10. Note that this is a *hint*, not proof — see below.

Confirmed scope (user, 2026-08-10): **only** plans in this campaign lose points.
Other CardX JCB installments earn normally, which is why this can't be a card
flag.

### U Plan 0% — Krungsri / First Choice

Pay in full at the merchant — so the charge starts on the **card** line — then
ask Krungsri to re-split it into 0% over **3 months**. Those rows earn **no
points**, but **may earn cashback** depending on the active promotion.

That cashback caveat is why U Plan is a campaign and not covered by the card
flag: the flag zeroes cashback, while a promo with an explicit `installment_rule`
overrides it and pays per term. The campaign forces `×0` on top of whatever
cashback survives.

Observed on Baiboon's First Choice (`ICARE-RT-CHIANGMAI AIRP 01/03`–`03/03`,
`FUTURE ELECTRONICS SERV 01/03`–`03/03`), all carrying:

> เป็นรายการผ่อนชำระเอง ไม่ได้รับคะแนนสะสม

`ผ่อนชำระเอง` — "installment requested by oneself" — is the detection substring.

## How inheritance works

`lib.installments.populate_for_cycle` reads every recorded term of the plan it's
about to extend. If any of them carries a campaign's `detect.note_contains`
substring in its `Note`, the campaign applies to the new term: its
`points_default` overrides the multiplier and its `note` is written verbatim.

Two consequences worth knowing:

- **The note is load-bearing.** It is not decoration — it is the only durable
  record that a plan was converted. Rewording a campaign note by hand breaks
  detection for every future term of that plan. The exact strings live in the
  campaign YAML for this reason.
- **One tagged term is enough.** A partially-tagged plan means earlier
  automation missed some terms, not that the plan is mixed. This is exactly the
  gap that existed before 2026-08-10: `/populate-installment` wrote 10 CardX JCB
  terms with no `×0` and no note while all 38 hand-entered rows had both.

### Term-count hints are advisory only

A campaign may declare `detect.typical_total_terms`. When a plan matches on
issuer + term count but carries **no** campaign note, the tooling reports a
`campaign_hint` and applies **nothing**. A term count is circumstantial:
Dee-Jang issues 4 terms, but so could a merchant. Zeroing someone's points on a
coincidence is worse than asking.

The hint is genuinely weaker for U Plan (3 terms is a conventional length) than
for Dee-Jang (4 is unusual), and both are treated the same way — surfaced, never
applied.

## Declaring a campaign on a new plan

`/add-installment` (see `.claude/skills/add-installment/SKILL.md`) takes
`campaign: "<id>"`, which writes the campaign's note and multiplier onto term 1.
From there `/populate-installment` inherits it for every later term with no
further instruction.

Because the campaign is invisible in the merchant string, **the user has to say
so when the plan starts.** If they don't, the term-count hint is the only
prompt — treat it as a question to ask, not a fact to act on.

## Related

- [[points-and-multipliers]] — the multiplier model these rules write into.
- [[cashback]] — the `% cb` axis; the card flag zeroes it, the campaigns mostly don't.
- [[promotions]] — why rewards are promotion-driven, and how an explicit `installment_rule` outranks the card flag.
- [[krungsri-truemoney-711-exclusion]] — the other Krungsri-family rule; points-only, merchant-detectable, and therefore card-level.
- [[bill-cycle-patterns]] — which cycle a term posts into.
