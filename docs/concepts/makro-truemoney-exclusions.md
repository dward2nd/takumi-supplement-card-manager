---
tags: [concept, points, cashback, makro, truemoney, exclusions]
---

# Makro, MCC 5199 and TrueMoney: which cards still earn

Thai issuers took Makro and TrueMoney out of their rewards one by one through 2026. Most of these notices withhold **points only**. Cashback campaigns read their own terms ([[../promotions/first-choice-2026h2|NW4]] leaves out "MCC 5199 อาทิ Makro และ Makro PRO"; AEON World's 5% and NTW1 still pay at Makro PRO). Researched 2026-11-08, after the user asked (2026-11-08: "Krungsri Card … has stopped giving reward points to Makro … other banks [may] exclude Makro, Makro PRO, and TrueMoney transactions too, so please dig deeper"). The November catalogue reports came first and hold the earlier reading ([[../catalogues/2026-11/all-spend]] §1, [[../catalogues/campaigns]] "November 2026").

**Nobody knows Makro PRO's MCC.** Krungsri, First Choice, Central The 1 and KBank call Makro and Makro PRO "MCC 5199". The household treats `WWW.MAKRO.PRO` as 5199 on AEON and Lotus's ([[../cards/aeon-world-mastercard]]). `HTTPS://WWW.MAKRO.PRO/` is open: on 11 Nov 2026, AEON's app will show what Baiboon's ฿16,068.50 order earned (see *Open* below). UOB World paid ×5 on `WWW.MAKRO.PRO` ฿16,850 on the 25 Oct 2026 statement ([[../cards/uob-world]]).

## By issuer

V = read on the issuer's own page or PDF, T = search snippet only, R = the household's reading. "Earns" means the terms don't name it.

| Issuer (household cards) | Makro (store, Makro PRO) | MCC 5199 | TrueMoney | 7-Eleven | From | Encoded |
|---|---|---|---|---|---|---|
| **Krungsri Card** (Visa, JCB, Lady, NOW) | no points, every channel | no points | no points | no points | Makro 1 Nov 2026; TMN/7-11 1 Aug 2026 | YAML `points_excluded_merchants` + `KrungsriFamilyCard` |
| **First Choice** | no points, every branch and online | no points | no points | no points | same | same |
| **Central The 1** (Redz) | no points, every channel | no points | no points (card bound to TrueMoney Wallet; 2c2p e-wallet top-ups) | no points | Makro 1 Nov 2026; TMN/7-11 1 Aug 2026 | same |
| **Lotus's Beyond** | earns | no coins | earns (e-wallet top-ups: no coins) | earns | 5199 20 Feb 2026; fuel out 1 Dec 2026 | `LotussBeyond`; `WWW.MAKRO.PRO` as 5199 |
| **UOB** (One, World, Premier, Makro) | Makro **stores**: no points, no One 1% (UOB Makro ÷4); Makro PRO earns | earns | top-ups: no points; payments earn | earns | top-ups 1 Jan 2025 | `UOBCard`; `MAKRO_…` by hand |
| **KTC UnionPay** | not named; out if Makro codes 5411/5399/5499 (rule 16) | earns | earns, except 7-Eleven through TrueMoney | no points | rule 16 undated | `KTCUnionPay` |
| **KTC VISA** (Digital VISA) | no points or cashback | no points | no points (card bound to TrueMoney) | no points | Makro 1 Sep 2026; 5199 and binding 1 May 2026 | YAML + `KTCTrueMoneyBound` |
| **KTC Mastercard** | not named | no points | no points (bound) | no points | binding 1 May 2026 | `KTCTrueMoneyBound`; 5199 not encoded |
| **KTC JCB** | not named | earns | earns, except 7-Eleven | no points | — | `KTCCard` |
| **CardX** (UP2ME, JCB) | earns (supermarket/fuel MCCs share a ฿100,000 a month cap) | earns | top-ups (MCC 6540): no points or cashback; payments earn | earns | 6540 1 Aug 2026 | not encoded |
| **AEON** (World, UnionPay, Rabbit) | not named | no points | top-ups (6540): no points | 5499 listed | 11 Nov 2025 | `AEONCard`; `WWW.MAKRO.PRO` as 5199 |
| **ttb** (so smart) | no points, no so smart 1% | — | so smart: TMN excluded | excluded | Makro 3 Nov 2026 | so smart is ×0; the 1% Makro rule isn't encoded |
| **KBank** | no points | no points | no points (bound) | no points | "current terms" (catalogue) or **1 Dec 2026** (T, 19 Oct notice) | not encoded |
| **Bangkok Bank** (not held yet) | earns; 5310/5411 earn nothing above ฿20,000 a cycle | earns | earns | earns | terms PDF of 9 Oct 2026 | — |

- **KTC's TrueMoney rule is 7-Eleven only on JCB and UnionPay.** Clause (3) withholds points at 7-Eleven "ทุกช่องทาง… ซึ่งรวมถึงการชำระ… ผ่านแอปพลิเคชันทรูมันนี่ วอลเล็ท" (7-Eleven in every channel, including paying through TrueMoney). The 27 Aug 2026 KTC JCB statement printed 10 points, and that needs `TMN LOTUS HYPER` ฿91 to have earned its 3. Until 2026-11-08 `KTCCard` zeroed every `TMN …` row. No ledger row was affected.
- **AEON caps supermarket and fuel points**: from 11 Aug 2025 (2568), MCC 5541, 5542, 5411 and 5310 earn points on at most ฿10,000 each per card per cycle. AEON's MCC list from 11 Nov 2025 is longer than the vault had: 1520, 4111, 4112, 4121, 4131, 4215, 4784, 4814, 4816, 4899, 4900, 5199, 5322, 5399, 5462, 5499, 5814, 5912, 5994, 6540, 7216, 7523, 7832, 7841, 7933, 7994, 7999, 8062, 8211, 8220, 8241, 8244, 8249, 8299, 8398, 8661, 9211, 9223, 9399, 9402, 9405, 9406, 9950. Only what a merchant string shows can be encoded.
- **Bangkok Bank** (the user plans to apply). The Thank You Rewards terms exclude no e-wallet, wholesale, government or insurance spend. They exclude unit trusts, unit-linked insurance, cash advances, taxes, fees, MEA/PEA/MWA auto-debits, named schools' tuition, the EEA, and fuel above ฿15,000 and hypermarkets/supermarkets above ฿20,000 a cycle. The **UnionPay 2%** counts all spend worldwide except China, Alipay/WeChat Pay, investments, insurance, cash, fees (MCC 6012, 4829) and installments. It needs ≥ ฿2,000 a month, pays up to ฿1,000 a month and ฿12,000 over 1 Jul 2026 – 30 Jun 2027, within 60 days. The user's reading holds: Makro, Makro PRO and TrueMoney all count.

## Sources

- Krungsri Point terms, item 2.3 (7): <https://www.krungsricard.com/th/krungsri-point> (V)
- First Choice: `exemption-of-accumulated-points-mcc-5199.pdf`, from <https://www.firstchoice.co.th/firstchoice-rewards> (V)
- Central The 1: notice of 1 Oct 2026 (`point-makro`) and letter of 1 Jul 2026 (7-11 / TrueMoney Wallet), <https://www.centralthe1card.com/news-and-anoucement-page/01>; Redz page <https://www.centralthe1card.com/product-listing/product-detail-redz> (V)
- Lotus's: <https://www.lotussmoney.com/announcement-corporate/coin-exclusion-2026> (5199), <https://www.lotussmoney.com/announcement-corporate/lotus-money-coin-fuel-station-exclusion> (fuel, letter 25 Oct 2026), card page <https://www.lotussmoney.com/credit-card/platinum-beyond> (V). None of these names Makro or TrueMoney (user, 2026-11-08: "Lotus's does exclude points for MCC 5199, but not specific to Makro or TrueMoney").
- UOB: <https://www.uob.co.th/personal/credit-cards/rewards/uob-world-credit-card.page> ("ยอดใช้จ่ายในห้างแม็คโคร", e-wallet top-ups from 1 Jan 2025) (V)
- KTC: <https://www.ktc.co.th/rewards> clauses (3), (5), (6), (16); notice `KTC2569-Notice-Changes-KTC-Point-Cashback-Earning-th.pdf`; `Makro-CPAXT-KTCVisa-Notice-changes-Points-and-Cashback-Earning-t.pdf` (V)
- CardX: <https://www.cardx.co.th/th-TH/news/details/pointx-cashback-changes> (MCC 6540 from 1 Aug 2026); the UP2ME and JCB Platinum card pages (V)
- AEON: <https://www.aeon.co.th/aeon/news-events/notification-aeon-credit-cards-2025> (V)
- KBank: the 19 Oct 2026 announcement answered 403; only a search snippet was read (T)
- Bangkok Bank: `thankyourewards-conditions.pdf` (modified 9 Oct 2026) and the UnionPay card page <https://www.bangkokbank.com/th-TH/Personal/Cards/Credit-Cards/Bangkok-Bank-UnionPay-Credit-Card> (V)

## Open

- **Baiboon's AEON World** shows 559 points in Notion. 535 of them are her 10 Oct `HTTPS://WWW.MAKRO.PRO/` ฿16,068.50 order, billed on the 2026-11-10 cycle, and AEON credits a cycle's points the day after it closes. On 11 Nov the app should add 535 points if the order codes as ordinary spend, 333 if it codes 5411 (the ฿10,000 cap), or 0 if it codes 5199. Each answer also settles that Makro PRO string's MCC for every bank.
- **KBank**: check whether the Makro/TrueMoney/7-Eleven exclusions started already or start on 1 Dec 2026, then encode them for the KBank cards.
- **Not encoded**: ttb so smart's 1% at Makro (from 3 Nov), CardX's MCC 6540 top-ups, KTC Mastercard's 5199, and AEON's 5411/5310 cap.

See also [[points-and-multipliers]], [[krungsri-truemoney-711-exclusion]], [[promotions]].
