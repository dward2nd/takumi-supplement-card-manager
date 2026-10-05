---
tags: [concept, notion, presentation]
---

# Page icons — telling rows apart at a glance

Every row the scripts create carries a page icon, so a ledger, a bill list or the [[../databases/promotion-bureau|Promotion Bureau]] reads at a glance (user, 2026-09-30). The icon is presentation only: no formula, rollup or script reads it.

**Emoji, always.** Notion's built-in icon set is monochrome; emoji are colourful, which is the point (user, 2026-09-30).

**The Cards DBs are never touched.** Takumi gives every Cards row its bank's logo by hand (`uob-logo`, `krungsri-logo`, `kbank-logo`, …). The scripts don't write to Cards, and no icon code runs there.

## Where the icon comes from

`notion_client.create_page` asks `lib.icons.for_new_page` for an icon whenever its caller passes none. Every write path therefore gets one without knowing about icons: `/add-transaction`, `/add-installment`, `/populate-installment`, `/record-payment`, `/post-cashback-credits`, `/prepare-bill`, `/record-statement`, `/sync-points-balance`, `/sync-promotion`. The code is in `scripts/python/lib/icons/`, one class per kind of database.

| Database | Icon |
|---|---|
| Transactions (all three) | the row's **kind** first, then the merchant's **category** (below) |
| Bills (all three) | 📝 while the title opens `[DRAFT] ` (drafted from transactions, or a placeholder awaiting the statement), 🧾 once final. No paid icon: `จ่ายแล้ว` already shows that. The `Card` relation shows whose card it is, so the bank logo isn't repeated (user, 2026-09-30) |
| Promotion Bureau | the campaign's `icon` (`BasePromotion.icon`, default 🤑) |
| Cashback trackers (all three) | the same campaign `icon` as the Bureau row the tracker belongs to |

Existing hand-set icons don't set the scheme (user, 2026-09-30). Icons are chosen for what fits the row, not copied from what the household used before.

## Transactions: kind before merchant

A row is bookkeeping before it is a merchant. The kind tests are the ones bills and statements already use (`lib.ledger`, `lib.promotions`), so an icon never contradicts how a script treats the row.

| Icon | Kind | Recognised by |
|---|---|---|
| ↪️ | carry-forward | `[ยอดยกมา…]` / `[ยกยอดมา…]` |
| ⚖️ | offset or debt takeover | `[หักลบหนี้…]` / `[เว็บรับหนี้…]` |
| ↩️ | cancellation or refund | `[ยกเลิก…]`, `REFUND`, or any other credit that names a merchant |
| ⭐ | points only | `[ปรับคะแนน]`, `[คะแนนพิเศษ]`, `…คะแนน…` rows, ฿0 rows |
| 🤑 | cashback or bank credit | `ledger.is_cashback_row`, `เครดิตเงินคืน`, `CASH BACK`, `SPECIAL DISCOUNT` |
| 🎁 | paid with points | `PWP:`, `แลกคะแนน…`, `CASH REBATE` |
| 🔄 | [[ledger-reset]] | `Reset …` |
| 🔁 | balance moved between ledgers | `โอน…`, `รวมยอด…` |
| 🛠️ | cycle or card admin | `…วันตัดรอบบิล…`, `เปิดบัตรใหม่` |
| 🧾 | fee, interest or bill counter | `FEE`, `ค่าธรรมเนียม`, `INTEREST`, `ISERVICE` |
| 📆 | installment term | `NN/NN`, `(INST 005 OF 010)`, `ผ่อน` |
| 💸 | bill payment | `ชำระ…` / `จ่าย…`, `AUTO DEBIT`, `PAYMENT THANK YOU` |

Every other row is a purchase, and gets its merchant's category, matched on the name with any `[…]` prefix removed (`lib/icons/merchants.py`). The order matters where categories overlap. Food delivery comes before rides (Grab Food is food), transit before wallets (`LINEPAY*BTS` is a fare), and flights before hotels (Agoda sells both). The petrol, e-wallet top-up and supermarket tests are the earning rules' own.

| | | | |
|---|---|---|---|
| 🏪 7-Eleven, convenience | 🚗 Grab, taxis | 🛵 food delivery | 🚆 BTS / MRT / SRT |
| ⛽ petrol | 👛 e-wallet top-up | 📲 PromptPay, PayAnything | 🛣️ tolls |
| ☕ cafés, Café Amazon | 🧋 tea, juice | 🍦 ice cream, desserts | 🥐 bakeries |
| 🍔 fast food | 🍣 Japanese | 🍲 hotpot, shabu | 🍜 other dining |
| 🛒 supermarkets, Makro, Lotus's | 🛍️ Shopee, Lazada, online | 👕 fashion, department stores | 🛋️ home, IKEA |
| ✈️ flights, travel agents | 🏨 hotels, Agoda | 🎬 cinemas | 🎓 education |
| 🤖 AI (Claude, OpenAI) | 📺 video streaming | 🎵 music streaming | 💻 software, app stores |
| 📶 phone, internet | 🛡️ insurance | 🏥 clinics, hospitals | 💊 pharmacies, beauty |
| 💆 massage, spa | 🏋️ fitness | 📱 phones, electronics | 📚 books, stationery |
| 🏛️ government, museums | ⛴️ boats | 🧺 laundry | 🇨🇳 Alipay / UnionPay in China |
| 🌐 other foreign merchants | 💳 anything else | | |

## Bills: draft or final

A bill's icon follows its title. `/prepare-bill` and slip-first placeholders create it as 📝. `/update-bill`'s finalize (explicit, or on attaching the statement) and `/record-statement` completing a placeholder re-set it to 🧾 along with the title. A title edited by hand in Notion keeps its old icon until `backfill-icons --db bills --replace`. Bills briefly carried their card's bank logo (2026-09-30, before the `Card` relation made that redundant).

## Campaign icons

| Icon | Campaigns |
|---|---|
| 🤑 | cashback in general: NW3, UOB One 10%/5% and 1%, ttb so smart 1%, NTW1 |
| 🛍️ | online shopping: EPW538, ON3, ONQ3, Krungsri NOW 5%; Lotus's SMP1 (shopping categories) |
| 🛒 | supermarkets and hypermarkets: SUP1, LBS3, AEON World 5%, ttb BMG |
| ⛽ | fuel: Bangchak 1%, BC3P, PTT2, ttb Caltex / Bangchak |
| 🍽️ | dining: EAT, J Dining |
| 🛵 | delivery: DLV3 |
| 🛡️ | insurance premiums: IS3 |
| 🚆 | AEON Rabbit |
| 🌏 | AEON UnionPay 3% abroad |
| 📈 | points: UOB World ×5 |
| 🎟️ | lucky-draw rights: BTS |
| 🐦 | early-bird bonuses for the first N accounts: Lotus's SMT2 |

A new campaign class inherits 🤑 unless it sets `icon`.

## Adding a category

Put an `IconRule` in `MERCHANT_RULES` (`scripts/python/lib/icons/merchants.py`) ahead of any rule that would otherwise catch the merchant. For a new row kind, add one to `_NAMED_KINDS` in `lib/icons/transactions.py`.

## Backfill

Rows from before 2026-09-30 were given icons by `scripts/python/backfill-icons/cli.py` (the same pickers, applied to existing pages). It skips any page that already has an icon, so hand-set ones stay. After changing a rule, re-run it with `--replace --db transactions` to bring old rows in line; `--dry-run` shows the plan first.

```sh
uv run --project scripts/python scripts/python/backfill-icons/cli.py --dry-run [--replace] [--db transactions,bills,bureau,trackers] [--holder nuta]
```
