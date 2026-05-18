---
tags: [formula, nuta-only]
---

# `cashback` — baht cashback earned per transaction (Nuta only)

A formula property exclusive to [[../databases/nuta-transactions]]. Computes the baht-value cashback for this transaction based on `% cb` and `ยอดชำระ`.

## Where to find the body

`formulaCode://2a1cb755-f0f1-8110-9795-000bf7d48b4f/TVZkPw`

## Decoded body

_TBD — fetch from Notion when reconciling cashback claims with the bank._

## Likely shape (hypothesis)

```
if Credit Return then 0
else if Processed = false then 0
else ยอดชำระ × (% cb / 100)
```

Verify before quoting — the gating on `Processed` / `Credit Return` is conventional but not certain.

## See also

- [[../concepts/cashback]] — the conceptual model.
- Migration: should generalise to "rewards" per transaction in [[../future-app/data-model-target]].
