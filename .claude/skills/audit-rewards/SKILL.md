---
name: audit-rewards
description: Reconcile a bank statement's printed reward-points summary against every holder's ledger — per card or account, per cycle — and point at the rows behind any gap. Read-only. Covers UOB (UOB Rewards), KBank (K Point), KTC (KTC FOREVER), Krungsri (Visa/JCB/Lady/NOW) and Lotus's (coins); First Choice, Central The 1 and AEON print no points. Use when the user says "audit the points", "do our points match the statement?", "check reward points for <card>", or after recording a statement (/record-statement).
---

# audit-rewards

Every points summary a statement prints is compared with what the ledgers give the same card for the same period. The data comes from all holders' rows, because banks pool points on the account.

## Primary execution path

```sh
echo '{"pdf":"/abs/MONTHLYSTATEMENT_….pdf","issuer":"UOB"}' \
  | uv run --project scripts/python scripts/python/audit-rewards/cli.py
```

`issuer`: `UOB`, `KBank`, `KTC`, `Krungsri` or `Lotus`. For a PDF, use the statement on the Bills row's `ใบแจ้งยอด (PDF)` ([[../../../docs/concepts/billing-cycle|statements live on the bills]]). A paper-shifted statement date is mapped onto the card's cycle first, as `/record-statement` does. Read-only.

## How the ledger side is counted

Each issuer's parser class states two facts. The engine is `lib/rewards_audit.py`.

| Issuer | `points_timing` | `points_rounding` | Evidence |
|---|---|---|---|
| UOB | `posting`: rows *posted* from the previous statement date to the day before this one (`Process Date`, else inferred). Points are credited as each charge posts. | `line`, like the ledger formula | Aug/Sep 2026 exact |
| KBank, AEON | `cycle`: rows billed on the cycle. Points are credited per cycle, in the app the day after BC (user). | `cycle`: floor(Σ spend / ฿ per point) per multiplier | KBank Aug exact after rounding |
| KTC, Krungsri, Lotus's | `cycle` (default) | `cycle` | KTC Aug, Krungsri Visa Sep exact |

- **Which rows:** every holder's rows on the card when points pool on the account (UOB, KBank, Krungsri, Lotus's). On KTC, where each card number gets its own PDF, only that card's own rows count, plus friends' `[บัตรหลัก]` shares on your principal card.
- **Points:** the `คะแนนที่ได้จริง` formula per row ([[../../../docs/formulas/points-realized]], `lib/points.py`).
- **`[ปรับคะแนน]` rows** are the split-line adjustments `/record-statement` writes, and count as earned.
- **Other `ใช้คะแนน` rows** are redemptions, or hand adjustments when named `ปรับคะแนน…`.
- **`Reset …` rows** are ledger bookkeeping and are left out (`left_out`).

## Reading the report

Per summary:
- `status`:
  - `ok`: the ledger matches the bank.
  - `rounding`: the only gap is `rounding`, the points the ledger's per-row flooring loses on a bank that rounds per cycle.
  - `gap`: something else differs.
  - `unmapped`: the card number isn't in any card YAML's `statement_numbers`.
- `bank`: earned, bonus, adjusted, redeemed and outstanding, as printed.
- `ledger`: earned, split adjustments, hand adjustments, redeemed, and rows counted per holder.
- `delta_earned`, `delta_after_rounding`, `delta_redeemed`: each is ledger minus bank.
- `suspects` (on a gap): rows whose multiplier differs from `lib.promotions.classify`. They're candidates, not verdicts; rules the classifier doesn't know yet (KTC UnionPay supermarkets `×0`, UOB World dining) show up here.

A `gap` usually means one of these:
- a wrong multiplier;
- a bank bonus or redemption the ledger doesn't record (KBank prints bonus points separately);
- a holder whose rows for the period aren't in the ledger (your rows before your ledger started).

Report it; fix nothing without the user's decision ([[../../../docs/concepts/reconcile-dont-correct|reconcile, don't correct]]).

## Adding an issuer

Give its `StatementParser` a `rewards(text, statement)` reader that returns `RewardSummary` rows (`lib/statements/model.py`). Set `points_timing` and `points_rounding` once a month's figures confirm them.
