---
name: post-cashback-credits
description: Write a card's cashback credit rows for one bill cycle into Baiboon's or Nuta's ledger — for UOB One, one negative `UOB ONE CASHBACK <n>%` row per `% cb` tier (1% dated the BC date, 5%/10% dated the first weekday of the next month), all billed on the cycle. Use when the user says "post the cashback for Baiboon's UOB One", "credit the cycle's cashback before drafting the bill", or before running [[../prepare-bill/SKILL.md|/prepare-bill]] on a UOB One cycle.
---

# post-cashback-credits

Materializes one cycle's cashback as negative-amount credit rows in a holder's Transactions DB, so [[../prepare-bill/SKILL.md|/prepare-bill]] sums the cycle to the right net balance. How a card is credited is a class per card in `scripts/python/lib/crediting/` (today: `UOBOneCrediting`); a card without one is refused, and so is Takumi (his credits come off his statement via [[../record-statement/SKILL.md|/record-statement]]).

## Primary execution path

```sh
echo '{"holder":"nuta","card":"UOB One","bill_cycle":"2026-09-25"}' \
  | uv run --project scripts/python scripts/python/post-cashback-credits/cli.py --dry-run
```

| Field | Default | Meaning |
|---|---|---|
| `holder` | — | `baiboon` or `nuta` |
| `card` | — | a card with a Crediting class (`UOB One`) |
| `bill_cycle` | active cycle | the cycle to credit (ISO BC date) |
| `skip_populate_installments` | `false` | skip adding the cycle's installment terms first (historical re-credits) |
| `force` | `false` | write even though the cycle already has `*CASHBACK*` rows (archive those first with `scripts/python/add-transaction/archive.py`) |

## The UOB One rule — the household's agreement

Per bill cycle (user, 2026-05-25; kept 2026-09-28 even though UOB counts 10%/5% per calendar month — the [[../sync-promotion/SKILL.md|Promotion Bureau]] shows the bank's view):

1. **Populate installment terms** into the cycle first (each earns 1%); a dry run simulates them.
2. **Sum each row's cashback per `% cb` tier** over the rows that **count in the cycle by UOB's rules** (user, 2026-09-28: the household follows the same rules as UOB). A row counts if it *posted* from the previous statement date to the day before this one; spend posted on the statement date counts in the next cycle's credit. Installment terms count on the cycle they're billed on. The posting date is `Process Date` from the statement, or the next working day until the statement comes. Each row's cashback is rounded to the satang, as UOB does. Existing `*CASHBACK*` rows are skipped, and carry-forward legs carrying `% cb` net out by construction. `counted_next_cycle` lists this cycle's rows whose cashback moves on.
3. **One row per tier with a positive sum**: `UOB ONE CASHBACK 1%` dated the BC date; `UOB ONE CASHBACK 5%` / `10%` dated the first weekday of the following month. Amount `−Σ round(rate × row, 2)`, `×0`, `Bill Cycle Date`/`Due Date` = the cycle's (the explicit date-rule exception), Note `Cycle <BC> cashback credit: 5% × 2048.00 = 102.40.`
4. **Never twice**: refuses a cycle that already has `*CASHBACK*` rows unless `force`.

Rows past the month's ฿500 10%/5% cap carry `% cb` 1% (set via `/sync-promotion`'s `field_mismatches`), so they're credited at 1% here.

## Workflow position

`/post-cashback-credits` → verify the credits → `/prepare-bill` → upload the statement via `/update-bill`. `/prepare-bill` refuses a UOB One cycle with no `*CASHBACK*` row unless `skip_cashback_check: true`.

## Adding a card

Subclass `Crediting` in `scripts/python/lib/crediting/<card>.py` (`plan()` returns the rows; the base `post()` writes them) and register it in `CREDITINGS` (`lib/crediting/__init__.py`). No YAML key does this (`crediting_schedule` was retired 2026-09-28).
