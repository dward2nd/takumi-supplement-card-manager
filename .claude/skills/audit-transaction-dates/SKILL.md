---
name: audit-transaction-dates
description: Scan a cardholder's Transactions DB and flag every row whose `Bill Cycle Date` / `Due Date` pair doesn't match the card's issuer pattern — missing dates, wrong day, wrong delta, or cross-card copy-paste mistakes. Read-only diagnostic. Use when the user asks "are any transactions on this card misaligned?", "check for bad cycle dates", "audit dates on <holder>'s data".
---

# audit-transaction-dates

Reads transactions and reports the ones whose `(Bill Cycle Date, Due Date)` doesn't fit the card's issuer pattern.

This skill is **read-only**. To patch the offenders it surfaces, hand the IDs to [[../update-transaction/SKILL.md|/update-transaction]].

## Primary execution path — the deterministic script

Backed by `scripts/python/audit-transaction-dates/cli.py`. Uses `lib/bill_cycle.py` (the same patterns the write skill uses to infer BC/Due) and `lib/transaction_audit.py` (the per-row check).

```sh
echo '<JSON-spec>' | uv run scripts/python/audit-transaction-dates/cli.py
```

JSON spec:

```json
{
  "holder": "takumi | baiboon | nuta",
  "card":   "First Choice"
}
```

`card` is optional. With it, only that card's transactions are scanned. Without it, every transaction on the holder is checked against whatever card it's related to.

Output envelope:

```json
{
  "holder": "baiboon",
  "card": "First Choice",
  "scanned": 79,
  "issue_count": 5,
  "skipped_unknown_pattern": 0,
  "issues": [
    {
      "id": "...", "url": "...", "name": "...", "card_name": "...",
      "amount": ..., "transaction_date": "...",
      "bill_cycle_date": "...", "due_date": "...",
      "expected_bill_cycle_date": "...", "expected_due_date": "...",
      "issue": "both_missing | bc_missing | due_missing | bc_mismatch | due_mismatch"
    },
    ...
  ]
}
```

`skipped_unknown_pattern` counts rows whose card name doesn't match any prefix in [[../../docs/concepts/bill-cycle-patterns]]. Document that issuer (and add the prefix to `lib/bill_cycle.py:_CARD_PATTERN_PREFIXES`) before those rows can be audited.

## Issue kinds

| `issue`           | Meaning                                                                            | Fix direction                                       |
|-------------------|------------------------------------------------------------------------------------|-----------------------------------------------------|
| `both_missing`    | Neither BC nor Due is set on the row.                                              | Most likely an orphan — fill in the active cycle.   |
| `bc_missing`      | Due is set but BC is not.                                                          | Set BC; verify Due also fits the pattern.           |
| `due_missing`     | BC is set but Due is not.                                                          | Set Due = BC + pattern delta (shifted for UOB).     |
| `bc_mismatch`     | BC's day-of-month doesn't match the issuer's cut-off day (or UOB shift).            | Often a cross-card copy-paste — confirm the cycle, then patch. |
| `due_mismatch`    | BC is plausible but Due isn't `pattern.due_from_nominal_bc(BC)` (or UOB shift).     | Patch Due.                                          |

The `expected_*` fields show what the pattern *says* the row should have, computed from the BC's calendar month. For `bc_missing` / `both_missing` rows where the transaction date is known, the expected pair is the **active cycle on the transaction date** (per `lib.bill_cycle.active_cycle`) — useful for orphans but check it; back-fills that posted late to a closed older cycle won't be on the active cycle.

## What this skill does NOT do

- Does **not** patch anything. Pass the IDs to [[../update-transaction/SKILL.md|/update-transaction]].
- Does **not** audit Bills (`บิลเรียกเก็บค่าบัตรเครดิต`) — only Transactions. The Bills schema is small enough that drift is unlikely; if that changes, write a separate `audit-bill-dates` skill.
- Does **not** check non-date properties (e.g. `Card` relation vs `ธนาคาร` mismatches). Future skill candidate if it comes up.
- Does **not** translate Thai labels.
