---
tags: [card, stub-index]
---

# Card stubs — observed products

Individual card notes are added **on demand**, when we discuss a specific card's quirks (its points rate, promo cycles, exclusions, etc.). This file is the working index of every card product seen anywhere in the eight databases.

Sources — the table is a **union of two harvests**, which do not agree:

- **Cards DB rows** — [[../databases/baiboon-cards]] (19 rows) and [[../databases/nuta-cards]] (5 rows). The live roster.
- **`Card` SELECT options on the Bills DBs** — [[../databases/baiboon-bills]] (17 options) and [[../databases/nuta-bills]] (13 options). Historical: a SELECT option survives after the card itself is gone, so this source over-reports. **Legacy since 2026-09-30**: a bill's `Card` is now a relation to a page in the holder's own Cards DB, and the old options live on in `Card (old select)` only until the household's views move over. New bills add no options, so this source is frozen. From now on the Cards DBs are the only roster.
- **Takumi** — [[../databases/takumi-cards]] (16 rows), readable since 2026-09-22 when the DS was shared with the `Claude Code's Automated Scripts` integration. His Bills DB only arrived on 2026-09-27 (a copy of Baiboon's, so its `Card` options started as hers), so it offers no independent cross-check; his column is a Cards-DB harvest only.

The two sources diverge most sharply on Nuta: her Bills DB offers **13** card options while her Cards DB holds only **5** rows. The 8 extras (AEON Next Gen, AEON Primo, Krungsri JCB, Krungsri Visa, SPayLater, UOB Makro, UOB Premier, UOB World) were read as cards she billed against historically but no longer holds a row for. The 2026-09-30 relation migration rules that reading out: every one of her 35 bills was linked to the Cards page in *her* Cards DB that its select named. So an extra either has no bill behind it (possibly an option inherited when her DB was cloned from Baiboon's), or it has a Cards row after all. Re-harvest to tell which. A ✓ below therefore means *observed in at least one source*, not *currently held*.

## Observed cards (union)

| Card name                            | Issuer (inferred) | Baiboon | Nuta | Takumi |
|--------------------------------------|-------------------|:-------:|:----:|:------:|
| AEON Next Gen                        | AEON              |    ✓    |  ✓   |   ✓    |
| AEON Primo                           | AEON              |    ✓    |  ✓   |   ✓    |
| [[aeon-rabbit\|AEON Rabbit]]                          | AEON              |         |      |   ✓    |
| AEON UnionPay                        | AEON              |         |  ✓   |        |
| [[aeon-world-mastercard\|AEON World Mastercard]] | AEON        |    ✓    |      |        |
| CardX JCB                            | CardX             |         |  ✓   |        |
| Central The 1 Redz                   | Krungsri          |    ✓    |      |   ✓    |
| First Choice                         | Krungsri          |    ✓    |  ✓   |        |
| Grab PayLater                        | Grab              |         |      |   ✓    |
| KBank JCB                            | KBank             |    ✓    |      |        |
| [[kbank-plustinum\|KBank PLUSTINUM]] | KBank             |    ✓    |      |   ✓*   |
| Krungsri JCB                         | Krungsri          |    ✓    |  ✓   |   ✓    |
| Krungsri Lady                        | Krungsri          |    ✓    |      |        |
| Krungsri NOW                         | Krungsri          |    ✓    |      |   ✓    |
| Krungsri Visa                        | Krungsri          |    ✓    |  ✓   |   ✓    |
| KTC Digital VISA (Visa Signature)    | KTC               |         |      |   ✓    |
| KTC JCB (JCB Ultimate)               | KTC               |         |      |   ✓    |
| KTC Mastercard (World Reward)        | KTC               |         |      |   ✓    |
| [[ktc-unionpay\|KTC UnionPay]] (Diamond) | KTC          |    ✓    |  ✓   |   ✓    |
| [[lotuss-beyond\|Lotus's Beyond]]    | Lotus             |    ✓    |      |        |
| SPayLater                            | Shopee            |    ✓    |  ✓   |   ✓    |
| [[ttb-so-smart\|ttb so smart]]       | ttb               |    ✓    |      |        |
| [[uob-makro\|UOB Makro]]             | UOB               |    ✓    |  ✓   |        |
| [[uob-one\|UOB One]]                 | UOB               |    ✓    |  ✓   |   ✓    |
| UOB Premier                          | UOB               |    ✓    |  ✓   |   ✓    |
| [[uob-world\|UOB World]]             | UOB               |    ✓    |  ✓   |   ✓    |

`*` **KBank PLUSTINUM** is the one Takumi ✓ that does *not* come from his Cards DB — it has no row there. It's observed via statement audit (he is the primary holder; Baiboon uses it Makro-only). Either the Cards DB is missing a row, or Takumi tracks that card outside Notion. Worth asking.

A blank Takumi cell is now a genuine negative — no row in his Cards DB — where before it was a `?` meaning unreadable. Blanks in the Baiboon / Nuta columns remain *observed-in-neither-source*, and a ✓ there still means *observed in at least one source*, not *currently held*.

The KTC products in brackets are the tiers after the upgrade (user, 2026-10-02); the Cards DB names stay short. See [[../concepts/premium-tier|premium tier]].

Last harvested: **2026-09-23**, from all three Cards DBs plus both Bills DBs' `Card` SELECT options. That sweep enumerated Takumi's column for the first time (his Cards DS became readable on 2026-09-22), adding six Takumi-only products — `AEON Rabbit`, `Grab PayLater`, `KTC Digital VISA`, `KTC JCB`, `KTC Mastercard` — and `Central The 1 Redz`, which turns out to be held by **both** Takumi and Baiboon and had been missing from this table entirely. Earlier: 2026-09-14 added `AEON World Mastercard` and `KBank JCB` and confirmed `Krungsri Lady`; `KBank PLUSTINUM` added 2026-07-28 from a statement audit; `UOB World` promoted to its own note 2026-08-20. Re-harvest after any Cards DB edits. The Bills options no longer change: they sit on the legacy `Card (old select)` since 2026-09-30.

## Promotion rule

When a specific card's behaviour needs documentation (e.g. "UOB Premier doubles points on travel from Mar–May"), create `docs/cards/<kebab-card-name>.md` with frontmatter `tags: [card]` and details. Update the table above to wikilink the name: `[[uob-premier|UOB Premier]]`.

## Useful Notion queries

To list every card Takumi actually holds:

```sh
echo '{"holder":"takumi","include_zero_balance":true}' \
  | uv run --project scripts/python scripts/python/summarize-overview/cli.py
```

Swap `takumi` for `baiboon` or `nuta`. Pass `include_zero_balance: true` to see cards sitting at zero, which the default view hides.
