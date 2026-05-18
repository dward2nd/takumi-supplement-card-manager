---
tags: [card, stub-index]
---

# Card stubs — observed products

Individual card notes are added **on demand**, when we discuss a specific card's quirks (its points rate, promo cycles, exclusions, etc.). This file is the working index of every card product seen anywhere in the eight databases.

Sources:
- `Card` SELECT options on [[../databases/baiboon-bills]] and [[../databases/nuta-bills]]
- TODO: enumerate Takumi's cards by querying [[../databases/takumi-cards]] for actual rows — the SELECT option harvest only works for Bills, and Takumi has no Bills DB.

## Observed cards (union)

| Card name        | Issuer (inferred) | Baiboon | Nuta | Takumi |
|------------------|-------------------|:-------:|:----:|:------:|
| AEON Next Gen    | AEON              | ✓        | ✓     |  ?      |
| AEON Primo       | AEON              | ✓        | ✓     |  ?      |
| AEON UnionPay    | AEON              |          | ✓     |  ?      |
| CardX JCB        | CardX             |          | ✓     |  ?      |
| First Choice     | Krungsri          | ✓        | ✓     |  ?      |
| Krungsri JCB     | Krungsri          | ✓        | ✓     |  ?      |
| Krungsri NOW     | Krungsri          | ✓        |       |  ?      |
| Krungsri Visa    | Krungsri          | ✓        | ✓     |  ?      |
| KTC UnionPay     | KTC               | ✓        | ✓     |  ?      |
| Lotus's Beyond   | Lotus             | ✓        |       |  ?      |
| SPayLater        | Shopee            | ✓        | ✓     |  ?      |
| ttb so smart     | ttb               | ✓        |       |  ?      |
| UOB Makro        | UOB               | ✓        | ✓     |  ?      |
| UOB One          | UOB               | ✓        | ✓     |  ?      |
| UOB Premier      | UOB               | ✓        | ✓     |  ?      |
| UOB World        | UOB               | ✓        | ✓     |  ?      |

Last harvested: 2026-05-19. Re-harvest after any Cards/Bills DB edits.

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
