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
| Rewards paid upfront | Krungsri family, card-level | ×0 | none | `KrungsriFamilyCard` (lib/earning) |
| Personal-loan credit line | First Choice, card-level | ×0 | none | `FirstChoice` (same rule, its own note) |
| **ดีจังผ่อน 0%** (Dee-Jang) | CardX, **plan-level** | ×0 | unaffected | `installment-campaigns/dee-jang.yaml` |
| **U Plan** (0% or with interest) | Krungsri / First Choice, **plan-level** | ×0 | varies by promo | `installment-campaigns/u-plan.yaml` |

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

On the Krungsri family's cards (First Choice, JCB, Lady, NOW, Visa, Central The 1 Redz), the points and cashback for an installment
purchase are granted **in full at the moment of purchase**, not spread across the
terms (user, 2026-08-10). Each `NN/NN` term therefore earns nothing on its own —
the reward already landed on the original charge, and crediting the terms too
would double-count it.

Code: `KrungsriFamilyCard` in `scripts/python/lib/earning/families.py` (a YAML
flag, `installment_rewards_upfront`, until 2026-09-28). It zeroes **both** axes,
unlike [[krungsri-truemoney-711-exclusion|the 7-11 / TrueMoney rule]] which is
points-only.

### First Choice runs two credit lines

First Choice is the same rule for a different reason, so its class
(`FirstChoice`) writes its own note. The card operates **two simultaneous credit lines**:

1. **credit card** — a pay-in-full purchase lands here and earns normally;
2. **personal loan** — a merchant-offered installment (0% interest, up to 10
   months) lands here instead. Only an installment set up at checkout lands
   here; a charge paid in full stays on the card line even when U Plan
   re-splits it later.

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

### U Plan — Krungsri / First Choice

Pay in full at the merchant, then ask Krungsri to re-split it. The charge
**stays on the card line**: a full-amount charge can never move to the
personal-loan line (user, 2026-10-03). The statement shows it there, as the
original charge, a `REV-FC PLAN ON DEMAND: <merchant>` reversal under
`รายละเอียดการเปลี่ยนรายการปกติเป็นผ่อนชำระ` (conversions to installments), and
each term as `FIRST CHOICE PLAN ON DEMAND <principal> 001/003 <term>` inside
"Total Payment Due For Credit Card"; the personal-loan total stays ฿0. Two kinds: **0% over 3 months** (only where a
promotion offers it, e.g. 11 listed public hospitals) and **with interest**,
0.39% a month on the principal for 4–10 months. Those rows earn **no
points**, but **may earn cashback** depending on the active promotion.

The 0.39% is a **promotional** rate and may not be offered next month or next year (user, 2026-10-05). For how it compares with UOB and ttb, see [[installment-conversion-rates]].

A term with interest is the principal ÷ terms plus 0.39% of the principal:
Nuta's `OMISE*ROOJAI Chon Buri TH 01/10` is ฿5,548.55 ÷ 10 + ฿21.64 = ฿576.49
(user, 2026-10-03).

**The original charge still counts toward Krungsri's cashback campaigns**
(user, 2026-10-03). U PLAN gives up the points; its page says nothing of
cashback campaigns, so a full-amount charge converted later counts toward
NW4 (and the like) once, as the original charge, on its own date. Sure for
0% plans, not yet confirmed for plans with interest. The terms themselves are
never new spend, which is why the Bureau's installment rules still hit every
`NN/NN` row. This is what separates U Plan from a **merchant installment**:
that one books to First Choice's personal-loan line and never counts at all.

#### Recording a conversion: as the statement prints it (user, 2026-10-03)

Every conversion is recorded as three kinds of rows, so the Bureau counts the
original charge and the bill still adds up:

| Row | Amount | Cycle | Points | Note |
|---|---|---|---|---|
| the original charge, as entered at purchase | + full | its own | `×0` | the U PLAN campaign note |
| `REV-FC PLAN ON DEMAND: <merchant>`, dated like the charge | − full | the charge's | `×0` | — |
| each term, `<merchant> 01/NN` (`/add-installment` with `campaign: "u-plan"`) | + term | the statement that bills it | `×0` | the U PLAN campaign note |

- **The charge earns no points.** A row's points can't be cancelled by a
  negative row (`คะแนนที่ได้จริง` earns only on positive amounts), so the
  original row itself goes to `×0` when it's converted.
- **The reversal isn't a refund.** `lib.ledger.is_refund_row` leaves
  `REV-… PLAN ON DEMAND` out, so the Bureau doesn't net it off the charge, and
  NW4 and the like count the charge once. The charge and its reversal cancel in
  the bill; the terms are what's owed.
- **`/record-statement` reads it all.** The Krungsri parser puts each
  `FIRST CHOICE PLAN ON DEMAND` term in its card's section, dated the day it's
  billed and named `<merchant> 01/03`, and tags the charge, the reversal and the
  term. A friend's missing piece is reported. A charge or term recorded with
  points, or without the campaign note, is flagged with the fix. Takumi's own
  pieces are written with `×0` and the campaign note.

The first plan recorded this way: Nuta's First Choice `7-11 NAPHRU SOI 3 CHONBURI TH` ฿7,175.88 (3 Oct 2026), 0% over 3 terms of ฿2,391.96 (user, 2026-10-05). Its `01/03` first went on the 5 Oct cycle, and was moved to the 5 Nov cycle the next day (rule below). The charge and its reversal stay on the 5 Oct cycle, where they cancel.

**A charge that posts on the cut-off day bills its first term a cycle later** (user, 2026-10-06, confirmed with Krungsri's call centre). The `7-11 NAPHRU` charge posted on 5 Oct, the bill-cycle date itself, which left the bank no time to put the conversion's first term on that statement. So `01/03` belongs to the **next** cycle: dated that cycle's BC date (`Transaction Datetime` 2026-11-05, `Bill Cycle Date` 2026-11-05, `Due Date` 2026-11-25), so `/record-statement` matches it to the November line. The app's bill and the printed statement differ meanwhile. This applies only when the charge posts on the BC date, which is rare. A charge that posts earlier in the cycle has its first term on that cycle as usual.

Older plans are left as they were. Baiboon's ICARE and FUTURE ELECTRONICS plans
kept only the terms. Nuta's `CTRIP (THAILAND) CO., BANGKOK TH` ฿11,766.58
(Apr 2026) kept the original charge, offset by a `[เว็บรับหนี้ไปบริหารต่อเอง]`
row when Takumi took the debt over. All three predate the Bureau. The BTS draw (`bts.py`) already flags a term as "the bank
counts the purchase slip, which the ledger may not show"; see
[[promotion-bureau]].

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
