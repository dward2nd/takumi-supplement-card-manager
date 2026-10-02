---
tags: [promotion, kbank, makro]
---

# KBank MKR — "ช้อปเยอะคุ้มกว่า ที่ MAKRO" (Oct–Dec 2026)

KBank cashback on monthly spend at MAKRO, in store and on MAKRO PRO, 1 Oct – 31 Dec 2026. It's tracked in the [[../concepts/promotion-bureau|Promotion Bureau]] with **one row per KBank card** per calendar month. The page caps it per person, but KBank counts each card separately unless its terms say otherwise (user, 2026-10-01; see [[uniqlo-2026]] for the same rule on UQN). Baiboon's Makro PRO slips (฿10k–17k in May–Jun 2026) go on KBank PLUSTINUM, Takumi's card, so they pool with his spend there.

> **Structured source of truth**: `scripts/python/lib/bureau/kbank_makro.py`.

| Part | Class | Pays | Cap |
|---|---|---|---|
| ต่อ 1 | `KBankMakroPromotion` (bands) | ฿100 from ฿10,000 a month, ฿240 from ฿20,000 | ฿240/month, ฿720 campaign |
| ต่อ 2 | `KBankMakroBonusPromotion` (steps) | ฿1,500 per whole ฿300,000 a month, counting only spend after registering | ฿3,000/month, ฿9,000 campaign |
| ต่อ 3 | — | 10% back for K Points equal to the spend, `BCB` by SMS each time | a redemption, not tracked |

- **Registered** on every KBank card (user, 2026-10-01): KBank registers all of a person's cards at once, and each card still counts on its own. October's rows are `2026M10 — MKR <card> cb ฿100/240`.
- **Registration**: once, before or after spending (part 2 counts only spend after it), between 1 Oct and 31 Dec 2026: K PLUS, or SMS `MKR <last 12 digits>` to 4545888.
- **What counts**: full-amount spend at MAKRO (`MAKRO_…`) and MAKRO PRO (`HTTPS://WWW.MAKRO.PRO/`, `WWW.MAKRO.PRO`) on every KBank card except business, juristic, Fleet and ThaiBev cards.
- **Not**: Smart Pay 0% installments, the liquor department, gift cards, redemption goods, shops renting space inside, Makro through Shopee/Lazada/TikTok, and e-wallet payments (`TMN MAKRO`).
- **Crediting**: within 60 days after 31 Dec 2026, to the card.
- **Rows keep `% cb` unset.** KBank cards earn points; the credit lives in the Bureau shares and the trackers.
- **KBank LINE Points**: spend counted here earns no LINE POINTS.
- **Part 2 has no Bureau rows.** No household card comes near ฿300,000 a month at Makro, so its classes exist without rows. Create the month's row if one ever does.
- **Smart Pay 0% 3 months**: available on Makro slips of ฿50,000 or more, but installments don't count toward the cashback.

Source, read 2026-10-01: <https://www.kasikornbank.com/th/promotion/creditcard/pages/shopping-makro.aspx>. KBank's site answers plain requests with an Akamai bot challenge. A headless Chrome (`--headless=new --dump-dom`, fresh `--user-data-dir`) gets the page.
