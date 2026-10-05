---
tags: [promotion, lotuss]
---

# Lotus's QRT4 "จ่ายแบบไหน ก็ได้คืน" (Jul–Dec 2026)

Lotus's Mastercard pays **10%, at most ฿10, on a slip of ฿100 or more** in five categories when paid by Tap & Go, the card's QR in UCHOOSE, or the card linked in TrueMoney Wallet. Takumi's [[../cards/lotuss-beyond|Lotus's Beyond]] is registered and has been paid since September 2026. The bank's credit lines are `CB TMN QR QRT4<MON><YY>`. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] from September 2026.

> **Structured source of truth**: `scripts/python/lib/bureau/lotus_qr.py` (`QRT4Promotion`).

## Rate and caps

A ฿100 slip already reaches the ฿10 maximum, so in practice **every qualifying slip of ฿100 or more earns ฿10**. Slips never add up. Per primary card number and calendar month:

| Channel | Cap |
|---|---|
| Tap & Go | ฿10 a slip, ฿10 a month |
| UCHOOSE credit-card QR, or the card linked in TrueMoney Wallet | ฿10 a slip, ฿40 a month |
| Both together | ฿50 a month, ฿300 for the campaign |

The ledger can't tell a tap from a QR payment. The household pays by QR / TrueMoney (that's what the credit line's `TMN QR` says), so the Bureau caps at **฿40 a month**. A tap at one of the categories would add up to ฿10 on top; tell the Bureau's page if it happens.

## The five categories (by MCC)

| Category | The page's examples |
|---|---|
| Fashion | UNIQLO, ZARA, H&M |
| Department stores | Central, Emporium, The Mall, Paragon |
| Hospitals, clinics, pharmacies | private hospitals, vet hospitals, health and beauty clinics, dental clinics, pharmacies; **not** government hospitals (MCC 9399) |
| Restaurants | any, **except** restaurants inside hotels |
| Home décor and building materials | Thai Watsadu, Boonthavorn, DoHome, Global House, HomePro, IKEA, Index Living Mall, MR.D.I.Y., Mega Home, SB Design Square, SCG Home |

Excluded: installments, cancelled charges, misuse of the card, digital assets, crypto and forex.

### How the Bureau decides

The household's QRT4 slips are **restaurants whose names nothing can match**: `MOOYIM JIMJUM CITY THA`, `CHAILAISALADROLLHEALHT CITY TH`, `PHUNGNOI MAYA-CM CITY TH`. So the class counts **every ฿100 slip on the card unless the merchant name shows it's outside the five categories**: Lotus's and every supermarket or convenience store, Makro, marketplaces, phone and utility bills, fuel, transport, top-ups, PromptPay. Hospitals, hotels and food-delivery apps come out *uncertain* and aren't linked automatically. The bank's own credit a few days after each slip confirms or refutes each one.

Checked against every credit so far:

| Slip | Credit |
|---|---|
| 2 Sep: `MOOYIM JIMJUM` ฿100 × 3 (and ฿52) | 3 Sep `CB TMN QR QRT4SEP26` −฿30 (the ฿52 earned nothing) |
| 8 Sep: `CHAILAISALADROLLHEALHT` ฿100 | 10 Sep `CB TMN QR QRT4SEP26` −฿10 (September's ฿40 now full) |
| 1 Oct: `CHAILAISALADROLLHEALTHT` ฿100 | 4 Oct `CB TMN QR QRT4OCT26` −฿10 |
| 3 Oct: `PHUNGNOI MAYA-CM` ฿108 | pending |

## Crediting

The terms say within 60 days after each month-end. In practice each slip's ฿10 posts within **three days**, as `CB TMN QR QRT4<MON><YY>` named for the slip's month. Book it in Takumi's ledger like any bank credit: negative, `×0`, `% cb` unset. Then link it to the month's tracker row (`Slip Transaction`) and tick the tracker once the credits add up to `Expected Cashback` ([[../databases/cashback-trackers|cashback trackers]]).

## Registration

Once, **before** the transaction: UCHOOSE → `QRT4`, or SMS `QRT4 <16-digit card no.>` to 081-250-7777. Lotus's Mastercard only. Supplements count, and their credit goes to the primary account.

## Bureau rows

| Row | Created | State |
|---|---|---|
| `2026M9 — QRT4 cb 10%` | 2026-10-05 | ฿40 to Takumi, settled by the two `QRT4SEP26` credits (tracker ticked) |
| `2026M10 — QRT4 cb 10%` | 2026-10-05 | ฿20 to Takumi; ฿10 credited 4 Oct, PHUNGNOI's ฿10 pending |

July and August have no rows: the ledger has no qualifying slip on the card in either month.

Source, read 2026-10-05: <https://www.lotussmoney.com/promotion/credit-card/shopping/shopping-lotus-paywave>.
