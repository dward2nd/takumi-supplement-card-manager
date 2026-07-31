---
tags: [card, kbank, points, makro]
issuer: KBank
holders: [takumi, baiboon]
points: integer
---

# KBank PLUSTINUM

Card number `4417 70XX XXXX 3831`. The account is in **Takumi's** name; Baiboon uses it for a single, narrow purpose (see below). Notion tracks it on [[../databases/baiboon-cards]].

## Baiboon's usage is Makro-only

Confirmed by the user (2026-07-28) while auditing the 2026-07-25 cycle:

> For Baiboon's KBank Plustinum, it should be correct to only have 1 transaction from Makro.

The card carries **two independent streams of spending** that must not be conflated:

| Stream | Merchant shape | Recorded in Notion? |
|---|---|---|
| Baiboon's Makro runs | `WWW.MAKRO.PRO …` / `HTTPS://WWW.MAKRO.PRO/ …` | **Yes** — on Baiboon's Transactions DB |
| Takumi's own spending | small local/food merchants, typically suffixed `CITY` (`A BEAR CHA CITY`, `DUMPLINGS CITY`, `SOMTAM LAMYONG CITY`, `BOOSHIFOOD CITY`, `100 BAHT SHOP-CMN CITY`, `PEENUTCHA PEIAPPLE CITY`) | **No** — deliberately absent |

So an [[../../.claude/skills/audit-bill/SKILL|/audit-bill]] run against the full statement section will always report Takumi's rows as `missing_in_notion`. **That is expected, not drift.** Only the `MAKRO.PRO` rows are in scope for Baiboon's ledger.

Each cycle normally contains exactly one Makro purchase, offset by a `ชำระบิลล่วงหน้า` (advance payment) row of the same magnitude, so the bill's `ยอดชำระ` (amount due) nets to **0**. Observed pattern:

| Cycle (BC) | Makro purchase | Advance payment |
|---|---|---|
| 2026-05-25 → 2026-06-25 | ฿10,630 (31 May) | −฿10,630 (1 Jun) |
| 2026-06-25 | ฿10,562 (9 Jun)  | −฿10,562 (22 Jun) |
| 2026-07-25 | ฿17,280 (29 Jun) | −฿17,280 (5 Jul)  |

## `CASH BACK HYPERMARKET` credits

KBank posts a hypermarket cashback credit directly onto the statement — e.g. `CASH BACK HYPERMARKET 202 6` for **−฿540.00** on 22/07/26. It is **not currently mirrored into Notion**, and its attribution is unresolved: the credit plausibly derives from Baiboon's Makro spend, but it lands on Takumi's account. Rate is not yet pinned down (−฿540 against the same cycle's ฿17,280 Makro row would be 3.125%; a flat cap is equally consistent with one data point). Revisit once a second credit is observed.

## Bill cycle

Statement date is day **25**; due date is day **10** of the following month (2026-07-25 → 2026-08-10). This matches the `kbank` pattern in `scripts/python/lib/bill_cycle.py`, and Notion's stored `Due Date` agreed exactly on the 2026-07 cycle — unlike [[uob-one|UOB]], which drifted that month. See [[../concepts/bill-cycle-patterns]].

## Statement shape

One PDF bundles **three KBank card products**, all under the primary holder — there are **no supplement-holder sub-sections**:

| Card type | Number |
|---|---|
| KBANK-SHOPEE | `4221 82XX XXXX 0052` |
| KBANK PLUSTINUM | `4417 70XX XXXX 3831` |
| KBANK-LINE POINTS | `4417 70XX XXXX 7805` |

Locate the `KBANK PLUSTINUM` section by its `ประเภทบัตร CARD TYPE` header. Note this differs from the Krungsri family, whose PDFs *do* carry a per-supplement sub-section.

The PDF is AES-encrypted. The password is the **primary holder's date of birth in `DDMMYYYY`** — registered under `KBank:` in `scripts/repositories/statement-passwords.yaml` (gitignored), so `audit-bill/extract.py --card "KBank PLUSTINUM"` resolves it automatically. Note the format differs from the `Krungsri` key, which stores the same date as `DDMonYYYY`.

## See also

- [[_stubs|Card stub index]]
- [[uob-makro]] — the other Makro-linked card, with a very different (points-side) rule set.
- [[../concepts/bill-cycle-patterns]]
