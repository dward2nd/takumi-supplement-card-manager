---
tags: [formula]
---

# `cashback` — baht cashback earned per transaction

A formula property on [[../databases/baiboon-transactions]] and [[../databases/nuta-transactions]]. Computes the baht-value cashback for this transaction as `% cb × ยอดชำระ`. [[../databases/takumi-transactions|Takumi]]'s DS does not have it.

> **Phase 2**: this Notion formula is replaced by application code in the new app — see [[../future-app/product-shape#Rewards & computation]]. The body below is retained for reference.

## Body

`prop("% cb") * prop("ยอดชำระ")` — straight multiplication, with no gating on `Processed` or `Credit Return`. Cashback continues to "accumulate" on those rows; consumers must filter when computing what the bank actually credits.

The original Nuta formula was authored via Notion's UI as property references (block-id tokens); Baiboon's was added 2026-05-25 with the equivalent plain-expression form. Both evaluate identically.

## See also

- [[../concepts/cashback]] — the conceptual model.
- Migration: should generalise to "rewards" per transaction in [[../future-app/data-model-target]].
