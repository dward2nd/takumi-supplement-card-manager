---
tags: [concept, taxonomy]
---

# Card network (`Card Network`)

A select on every Cards DB with five options:

| Option         | Colour |
|----------------|--------|
| `JCB`          | pink   |
| `Mastercard`   | orange |
| `VISA`         | blue   |
| `UnionPay`     | red    |
| `Unspecified`  | gray   |

## What it means

The card-association network (rails) the card rides on. Determines:

- Where the card is accepted internationally.
- Some currency-conversion behaviour.
- The first 1–4 digits of the card number (BIN).

## `Unspecified`

Used for products that aren't network cards — store cards (`Lotus's Beyond`), BNPL/credit lines without a physical card (`SPayLater`), and bank-internal credit lines (`First Choice`-style products in some configurations).

## Where it's used

- View groupings and gallery cards.
- No formula consumes this directly.

## Subtlety: network ≠ issuer

`ธนาคาร/บริษัท` (issuer) and `Card Network` are independent dimensions. `KTC UnionPay` (issuer: KTC; network: UnionPay) and `UOB World` (issuer: UOB; network: Mastercard or VISA depending on card-product) both exist.
