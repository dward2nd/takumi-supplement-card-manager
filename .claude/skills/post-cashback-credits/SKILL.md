---
name: post-cashback-credits
description: Write a card's cashback credit rows into Baiboon's or Nuta's ledger the way the bank credits them — for UOB One, a `UOB ONE CASHBACK 1%` row per statement cycle and `UOB ONE CASHBACK 10%` / `5%` rows per calendar month, each holder's amount being their first-come-first-served share of the account's capped cashback from the Promotion Bureau. Use when the user says "post the cashback for Baiboon's UOB One", "credit September's UOB One cashback", "post the 1% for the cycle closing 25 Sep", or before running [[../prepare-bill/SKILL.md|/prepare-bill]] on a UOB One cycle.
---

# post-cashback-credits

Materializes a card's cashback as negative-amount credit rows in a holder's Transactions DB, so [[../prepare-bill/SKILL.md|/prepare-bill]] sums the cycle to the right net balance. How a card is credited is a class per card in `scripts/python/lib/crediting/` (today: `UOBOneCrediting`); a card without one is refused. Takumi is refused too: his credits come off his statement via [[../record-statement/SKILL.md|/record-statement]].

## Primary execution path

```sh
echo '{"holder":"nuta","card":"UOB One","month":"2026-09"}' \
  | uv run --project scripts/python scripts/python/post-cashback-credits/cli.py --dry-run
```

Always dry-run first and show the user `detail` and `plan`; then run without `--dry-run`.

| Field | Default | Meaning |
|---|---|---|
| `holder` | — | `baiboon` or `nuta` |
| `card` | — | a card with a Crediting class (`UOB One`) |
| `bill_cycle` | — | post the 1% for the cycle closing on this date |
| `month` | — | `YYYY-MM`: post the 10%/5% for this calendar month |
| `skip_populate_installments` | `false` | skip adding the cycle's installment terms before the 1% (historical re-credits) |
| `force` | `false` | re-post a period whose credit row already exists (archive the old row first with `scripts/python/add-transaction/archive.py`) |

With neither `bill_cycle` nor `month`: the most recently closed cycle and the last completed calendar month.

## How UOB One is credited (user, 2026-09-28: follow the bank's periods)

| Row | Period | Dated | Billed on |
|---|---|---|---|
| `UOB ONE CASHBACK 1%` | statement cycle | the BC date | that cycle |
| `UOB ONE CASHBACK 10%`, `… 5%` | calendar month | the month's last day, or the next working day | the cycle that date falls in |

1. **Amounts come from the Promotion Bureau** (`2026M9 — UOB One cb 1%`, `2026M9 — UOB One cb 10%/5%`): the rows are created if missing and the period's qualifying rows linked, then the account's cashback is split first come, first served under the pooled caps (฿2,000 a cycle; ฿500 a month for 10% and 5% together). The holder's row is their share. See [[../sync-promotion/SKILL.md|/sync-promotion]].
2. **Carry-forward legs net out**: a bracketed row carrying `% cb` (e.g. Nuta's `[ยอดยกมาจากรอบ 2026-08]` −฿231 at 1%) subtracts its cashback, which already reached the holder in an earlier period. The Note says so.
3. **Installment terms first** (1% path): the cycle's in-progress terms are populated before the split, since each earns 1%. A dry run simulates them.
4. **Never twice**: a period whose row exists is reported under `already_posted`. For 10%/5%, rows already covered by the old per-bill-cycle credits (`Cycle <BC> cashback credit`, before 2026-09-28) are left out, so the first monthly run pays only what those didn't cover.

Each row is `×0`, `Processed`, with a Note carrying the working (`Month 2026-09 cashback credit (10%): baiboon's first-come-first-served share …`).

## Workflow position

`/record-statement` (Takumi's rows) → `/sync-promotion` on the UOB One rows (optional: this skill links rows itself) → `/post-cashback-credits` → `/prepare-bill`. `/prepare-bill` refuses a UOB One cycle with no `*CASHBACK*` row unless `skip_cashback_check: true`.

## Adding a card

Subclass `Crediting` in `scripts/python/lib/crediting/<card>.py` (`plan()` returns the rows; the base `post()` writes them) and register it in `CREDITINGS` in `lib/crediting/__init__.py`. No YAML key does this any more (`crediting_schedule` was retired 2026-09-28).
