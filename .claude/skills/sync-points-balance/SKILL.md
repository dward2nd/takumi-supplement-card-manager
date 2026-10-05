---
name: sync-points-balance
description: Set each card's running points balance (`คะแนนสะสม`) to the outstanding points its latest bank statement prints — statement total = Takumi's points + his friends' points — by writing one `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด <BC>` row per card per statement on the account holder's ledger. Idempotent: a re-run updates the row in place. Covers UOB, KBank, KTC, Krungsri, CardX and Lotus's coins (fractions kept, since 2026-10-05). Use when the user says "adjust my points to the statements", "bring the points balances up to date", "set every card's points to the bank's figure", or after /record-statement when /audit-rewards shows a balance the ledger doesn't hold.
---

# sync-points-balance

A card's `คะแนนสะสม` is the sum of its ledger rows, but no ledger holds an account's whole history. Takumi's reset rows zeroed his cards on 2026-09-22 ([[../../../docs/concepts/ledger-reset|ledger reset]]), and the friends' ledgers start when they did. This skill makes each card's points match the bank's printed balance.

**The rule** (user, 2026-09-29): *the points total on a statement = Takumi's points + his friends' points.*

## Primary execution path

Every card's latest statement, read from the `ใบแจ้งยอด (PDF)` files on the three Bills DBs:

```sh
echo '{"latest": true}' \
  | uv run --project scripts/python scripts/python/sync-points-balance/cli.py --dry-run
```

One statement:

```sh
echo '{"pdf":"/abs/MONTHLYSTATEMENT_….pdf","issuer":"UOB"}' \
  | uv run --project scripts/python scripts/python/sync-points-balance/cli.py
```

- **Issuers:** `issuer` is `UOB`, `KBank`, `KTC`, `Krungsri`, `Lotus` or `CardX`.
- **Hand-transcribed statements:** `"statement": {…}` (a Statement dict with `rewards`) replaces `pdf` for an issuer that has no PDF parser.
- **Writing:** run with `--dry-run` first, show the user the `accounts` table, then run again without it. The user's request to adjust the points is the go-ahead to write. A dry run alone never writes.

## What it writes

For each printed points summary, one row on the **account holder's** ledger:

| Property | Value |
|---|---|
| `Name` | `[ปรับคะแนน] ยอดคะแนนคงเหลือตามใบแจ้งยอด <statement BC>` |
| `ยอดชำระ` / multiplier | `0`, `×0` |
| `ใช้คะแนน` | −(printed outstanding − ledgers' points as of the statement); negative adds points |
| dates | the statement's cycle (BC, due), with the printed date mapped onto the card's cycle as `/record-statement` does |
| `Note` | the printed figure, each holder's share, the adjustment |

- **Account holder:**
  - Pooled account (UOB, KBank, Krungsri): Takumi.
  - One PDF per card number (KTC, CardX): the card's holder. Baiboon's KTC …2310 and Nuta's CardX …1265 get their rows on their own ledgers.
- **Rows each summary covers:** its `PointsAccount` (`lib/points_account.py`, the same classes `/audit-rewards` uses).
  - Pooled account: every holder's rows on the card.
  - The principal's KTC or CardX card: Takumi's rows plus friends' `[บัตรหลัก]` shares.
  - A supplement's own card: that holder's rows, minus their `[บัตรหลัก]` shares.
- **"As of the statement":** decided by its `PointsPeriod`.
  - UOB charges count if they posted before the cycle date.
  - Everything else counts if it's billed on or before the cycle.
  - `Reset …` rows always count.
  - Later rows (the open cycle, a redemption made since) stay on top, so `balance_now` = printed + `since`.
- **Points per row:** the `คะแนนที่ได้จริง` formula value itself (`points_realized`), so the card's rollup lands exactly.

## Reading the report

`accounts[].status`:
- `ok`: the balance already matches, or the row exists with the right figure.
- `create` / `update`: the row that was, or will be, written. `was` is an existing row's previous figure.
- `superseded`: a later statement's balance row is on the card. An older statement is never rewritten, because that would shift the later one.
- `unmapped`: the card number isn't in any card YAML's `statement_numbers`. Add it first.
- `no-outstanding`: the summary prints no balance.

Statements that print no points (AEON, First Choice, Central The 1) produce no accounts. Neither do issuers with no parser (ttb, Grab, Shopee).

## Relations

- `/audit-rewards` and `/record-statement`'s rounding step leave these rows out (`BALANCE_ADJUSTMENT`), because they set an opening balance rather than record points earned in a cycle. `/record-statement` never takes a `[ปรับคะแนน…` row for a statement line.
- Run it after `/record-statement` + `/audit-rewards`. When the audit is `ok`, the new statement's row comes out `ok` (no row written).
- Background and the first run's table (2026-09-29): [[../../../docs/concepts/points-and-multipliers#Statement balance rows|statement balance rows]].
