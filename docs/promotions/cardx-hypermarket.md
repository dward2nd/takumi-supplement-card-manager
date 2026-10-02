---
tags: [promotion, cardx]
---

# CardX HY1 / HYP — "คุ้มยกแพ็ก รับคืนแรง ที่ไฮเปอร์มาร์เก็ต" (Oct–Dec 2026)

CardX cashback at hypermarkets, 1 Oct – 31 Dec 2026, on every CardX credit card. The household's only CardX card is Nuta's CardX JCB. CardX bills each card number on its own, so its quota is that card's. Tracked in the [[../concepts/promotion-bureau|Promotion Bureau]].

> **Structured source of truth**: `scripts/python/lib/bureau/cardx_hypermarket.py`.

| Part | Class | Pays | Cap |
|---|---|---|---|
| **HY1** (คุ้มที่ 1) | `CardXHypermarketPromotion` (per slip) | ฿40 for ฿3,000–9,999, ฿200 for ฿10,000–29,999, ฿720 from ฿30,000 | ฿1,440/month per person, all CardX cards together (฿4,320 campaign) |
| **HYP** (รับเพิ่ม) | `CardXHypermarketBonus` (whole campaign) | ฿3,000 once, for ฿300,000 over the campaign; first 150 people | one right per person |
| **HY2** (คุ้มที่ 2) | — | POINTX points equal to the slip for 12% back (Mon–Thu) or 14% (Fri–Sun), SMS each time | a redemption, not tracked |

- **Stores**, in store: Big C (food place, market, mini Big C), GO WHOLESALE (`CFW-…`), Lotus's (PRIVE, go fresh), Makro. Online: Big C Online, Freshket, the GO WHOLESALE app, Lotus's online, Makro PRO.
- **Not**: every kind of installment (ดีจังแบ่งชำระ 0%, plans set up through CardX or SCB EASY), ShopeePay and Rabbit LINE Pay payments, business use, cancelled charges.
- **TrueMoney is only a maybe.** The page names ShopeePay and Rabbit LINE Pay but not TrueMoney, so `TMN MAKRO`-style rows are flagged `uncertain`, not linked.
- **Registered** on Nuta's CardX JCB (user, 2026-10-01); October's row is `2026M10 — HY1 cb ฿40/200/720`.
- **Registration**: once per card, via the CardX app or website, or SMS `HY1` / `HYP` / `HY2` + last 12 digits to 4545777.
- **Crediting**: within 60 days after 31 Dec 2026, to the card used, on the next statement.
- **HYP has no Bureau rows.** ฿300,000 at hypermarkets on one CardX card is far past the household's spend. Rows keep `% cb` unset, since the credit is fixed per slip.

Source: <https://www.cardx.co.th/credit-card/promotion/top-hypermarket-oct26-usc02>. The terms were read on 2026-10-01 from the user's copy of the rendered page. CardX serves the terms from `cdx-prod-ssc-frontend.cardx.co.th/content/<locale>/promotion/slug-name/<slug>`, which returned 403 to this machine (traffic leaves through Hong Kong). Its Meilisearch index (`kong-prod-frontend.cardx.co.th/indexes/search-content/search`, the site's public key) gives only the title, dates, category and eligible card codes.
