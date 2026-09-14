---
tags: [card, stub-index]
---

# Card stubs — observed products

Individual card notes are added **on demand**, when we discuss a specific card's quirks (its points rate, promo cycles, exclusions, etc.). This file is the working index of every card product seen anywhere in the eight databases.

Sources — the table is a **union of two harvests**, which do not agree:

- **Cards DB rows** — [[../databases/baiboon-cards]] (18 rows) and [[../databases/nuta-cards]] (5 rows). The live roster.
- **`Card` SELECT options on the Bills DBs** — [[../databases/baiboon-bills]] (16 options) and [[../databases/nuta-bills]] (13 options). Historical: a SELECT option survives after the card itself is gone, so this source over-reports.
- **Takumi** — still unenumerated. [[../databases/takumi-cards]] is **not shared with the `Claude Code's Automated Scripts` integration**, so `scripts/` gets `ObjectNotFound` on that data source and cannot read it; and Takumi has no Bills DB to harvest SELECT options from. Every `?` in the Takumi column below is this gap, not a negative finding. Sharing that database with the integration would close it.

The two sources diverge most sharply on Nuta: her Bills DB offers **13** card options while her Cards DB holds only **5** rows. The 8 extras (AEON Next Gen, AEON Primo, Krungsri JCB, Krungsri Visa, SPayLater, UOB Makro, UOB Premier, UOB World) are cards she billed against historically but no longer holds a row for. A ✓ below therefore means *observed in at least one source*, not *currently held*.

## Observed cards (union)

| Card name                            | Issuer (inferred) | Baiboon | Nuta | Takumi |
|--------------------------------------|-------------------|:-------:|:----:|:------:|
| AEON Next Gen                        | AEON              |    ✓    |  ✓   |   ?    |
| AEON Primo                           | AEON              |    ✓    |  ✓   |   ?    |
| AEON UnionPay                        | AEON              |         |  ✓   |   ?    |
| AEON World Mastercard                | AEON              |    ✓    |      |   ?    |
| CardX JCB                            | CardX             |         |  ✓   |   ?    |
| First Choice                         | Krungsri          |    ✓    |  ✓   |   ?    |
| KBank JCB                            | KBank             |    ✓    |      |   ?    |
| [[kbank-plustinum\|KBank PLUSTINUM]] | KBank             |    ✓    |      |   ✓    |
| Krungsri JCB                         | Krungsri          |    ✓    |  ✓   |   ?    |
| Krungsri Lady                        | Krungsri          |    ✓    |      |   ?    |
| Krungsri NOW                         | Krungsri          |    ✓    |      |   ?    |
| Krungsri Visa                        | Krungsri          |    ✓    |  ✓   |   ?    |
| [[ktc-unionpay\|KTC UnionPay]]       | KTC               |    ✓    |  ✓   |   ?    |
| [[lotuss-beyond\|Lotus's Beyond]]    | Lotus             |    ✓    |      |   ?    |
| SPayLater                            | Shopee            |    ✓    |  ✓   |   ?    |
| [[ttb-so-smart\|ttb so smart]]       | ttb               |    ✓    |      |   ?    |
| [[uob-makro\|UOB Makro]]             | UOB               |    ✓    |  ✓   |   ?    |
| [[uob-one\|UOB One]]                 | UOB               |    ✓    |  ✓   |   ?    |
| UOB Premier                          | UOB               |    ✓    |  ✓   |   ?    |
| [[uob-world\|UOB World]]             | UOB               |    ✓    |  ✓   |   ?    |

Last harvested: **2026-09-14**, from Baiboon's and Nuta's Cards DB rows plus both Bills DBs' `Card` SELECT options. That sweep added `AEON World Mastercard` and `KBank JCB` (both live in Baiboon's Cards DB, both missed by the 2026-05-19 Bills-only harvest) and confirmed `Krungsri Lady`, added earlier the same day on its first recorded transaction. Takumi's column is unchanged — his Cards DB is still unreadable (see Sources). Earlier: `KBank PLUSTINUM` added 2026-07-28 from a statement audit; `UOB World` promoted to its own note 2026-08-20. Re-harvest after any Cards/Bills DB edits.

## Promotion rule

When a specific card's behaviour needs documentation (e.g. "UOB Premier doubles points on travel from Mar–May"), create `docs/cards/<kebab-card-name>.md` with frontmatter `tags: [card]` and details. Update the table above to wikilink the name: `[[uob-premier|UOB Premier]]`.

## Useful Notion queries

To list every card Takumi actually holds:

```
mcp__notion__notion-search with
  query: ""
  data_source_url: "collection://1aacb755-f0f1-818a-a284-000b17d155de"
```

(Equivalent for Baiboon and Nuta: see their [[../databases/baiboon-cards]] / [[../databases/nuta-cards]] notes for collection IDs.)
