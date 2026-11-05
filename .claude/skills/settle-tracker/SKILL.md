---
name: settle-tracker
description: Settle one cashback tracker row (`รายการติดตามเครดิตเงินคืนของ<name>`) — link the ledger row(s) that carry the credit into `Slip Transaction`, tick the unnamed checkbox once the Bureau period has ended and the credit accounts for it, and optionally write the Note. Use after booking a credit row ("UOB One Cashback 10% 5% posted — settle my tracker"), when the user says "tick the NW3 trackers", "link this credit to Baiboon's tracker", "I already received the QRT4 cashback", or when validating open trackers. Refuses to change a ticked (frozen) row.
---

# settle-tracker

Settles **one** tracker row of **one** holder. The rules are in [[../../../docs/databases/cashback-trackers|cashback-trackers]]. This skill only applies them, so read that note before deciding a basis.

It writes the tracker row only: `Slip Transaction` (links merged, never dropped), the unnamed checkbox, and `Note` when given. It never touches `Expected Cashback` (the Bureau sync owns that), the ledger rows, or `Slip` files.

## Execution — the deterministic script

```sh
echo '<JSON-spec>' | uv run --project scripts/python scripts/python/settle-tracker/cli.py
# --dry-run plans the writes without making them
```

```json
{
  "holder":  "takumi | baiboon | nuta",
  "tracker": "UOB One 10%/5% 1—31 Oct",
  "link":    ["<ledger row page ID or URL>"],
  "tick":    "auto",
  "basis":   "auto",
  "note":    "UOB's credit for the whole account, ฿381.54 posted 2 Nov (Bureau ฿381.54). Takumi's share ฿175.64."
}
```

- `tracker`: the exact title, or the page ID / URL when titles repeat.
- `link`: rows of the holder's **own** Transactions DS. `Slip Transaction` can't reach another ledger, so the CLI refuses those. A friend's credit that landed in Takumi's ledger is settled by his transfer slip instead (attach it in Notion).
- `tick`:
  - `"auto"` (default) ticks only when the Bureau row's `End Date` has passed **and** the basis holds. A tracker without a Bureau link has no period to wait for.
  - `true` is the user's word that the money arrived ("I already received it"). It skips both checks.
  - `false` links now and leaves the tick for later. Use it for a credit that lands before its period ends.
- `basis`: how the linked credit accounts for the tracker. `auto` tries `exact`, then `pooled`.

| `basis` | Holds when | Case |
|---|---|---|
| `exact` | Σ linked credit = `Expected Cashback` (±฿0.01) | a bank `CB…` line on the holder's card; a household `UOB ONE CASHBACK 1%` row |
| `pooled` | Takumi only: Σ linked credit = the Bureau row's `เงินคืนรวม` | the bank's whole-pool credit on his card (`UOB One Cashback 10% 5%`) |
| `cycles` | a linked credit's `Bill Cycle Date` ≥ the period's end | Baiboon's and Nuta's UOB One 10%/5% **month** trackers, paid by **cycle** credit rows. Link each cycle's rows as they're posted; it ticks once the cycle covering the month's end is in. The amounts differ by design. |
| `zero` | `Expected Cashback` ฿0, nothing linked | a ฿0 share past its period. First check it isn't a pending-relink artefact (NTW1 Oct 2026). |

- `note`: replaces the Note. Leave it out to keep the existing one. For `pooled`, give both figures (the pool and Takumi's share), as the September and October rows do.

## Output

The output is a JSON envelope:

- `tracker`: title, expected, Bureau row, `period_end`, and whether it was already ticked.
- `links.kept` / `links.added` (each with amount and cycle) and `credit_linked`.
- `basis`: `{key, ok, reason}`.
- `tick`: `{ticked, reason}`.
- `writes`, `unchanged`, `warnings` (e.g. a linked row that isn't a credit).

An `error` key means nothing was written.

Report the tracker, what was linked, and whether it ticked. When it didn't tick, give the `reason`: the period is still running, the amounts disagree, or it's waiting for a cycle.

## Rules the script enforces

- **A ticked tracker is frozen.** Re-running with the same spec reports `unchanged`. Adding a link, changing the Note or unticking is refused (`FrozenTracker`).
- **Idempotent.** Links are merged with the existing ones, and a second run writes nothing.
- **Own ledger only** (see `link` above).

## Not this skill

- Creating tracker rows or setting `Expected Cashback`: [[../sync-promotion/SKILL.md|/sync-promotion]] (Bureau campaigns). Non-Bureau campaigns (UOB PWP20) are hand-made.
- Booking the credit row itself: [[../add-transaction/SKILL.md|/add-transaction]], [[../post-cashback-credits/SKILL.md|/post-cashback-credits]] (UOB One household cycle credits), [[../record-statement/SKILL.md|/record-statement]].
- Paying a friend by transfer: attach the slip to the tracker's `Slip` in Notion (file upload isn't scripted here).
