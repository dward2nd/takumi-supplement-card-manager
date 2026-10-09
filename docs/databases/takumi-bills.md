---
tags: [database, takumi, bills]
owner: takumi
role: bills
---

# Takumi — Bills (`บิลเรียกเก็บค่าบัตรเครดิตของเว็บ`)

One row per card per **bank statement** — the amount [[../people/takumi|Takumi]] actually pays the issuer. Created by Takumi on 2026-09-27 when he started keeping his own ledger again, and shared with the scripts' integration the same day.

- **Collection ID**: `63dcb755-f0f1-83df-aaa8-871bb9069dae` (data source; its database is `3e3cb755-f0f1-80a0-80be-f0151b47a900`)
- **Schema**: identical to [[baiboon-bills]] — untitled title property, `Card` (one-way relation → [[takumi-cards]]), `Card (old select)` (legacy SELECT), `วันตัดรอบบิล` (bill cycle date), `ยอดชำระ` (amount due), `จ่ายแล้ว` (paid), `ใบแจ้งยอด (PDF)` (statement), `หลักฐานการชำระ` (payment evidence), `Note`.
- **`Card`**: a relation to Takumi's own Cards DB since 2026-09-30. Before that it was a SELECT whose options began as Baiboon's list, because the DB started as a copy of hers. That SELECT was renamed `Card (old select)` and kept so existing views still work; it will be deleted once the views move to the relation, and scripts ignore it. All 28 existing bills were linked, each to the Cards page its old select named. `/record-statement` links the bills it creates to his Cards page. See [[../concepts/known-divergences]] #1.
- **Last schema-verified**: 2026-09-30

## Different in kind from the supplement holders' Bills

A supplement holder's bill is **computed**: the sum of *their own* Transactions rows for the cycle, drafted by `/prepare-bill` and reconciled against the statement afterwards. Takumi's bill is **the statement**:

- `ยอดชำระ` is the issuer's printed total for that card — principal **plus every supplement section**. Takumi pays the whole card to the bank, usually after Baiboon and Nuta have paid their shares to him.
- The title has no `[DRAFT] ` prefix once the statement is recorded. Before that, a `[DRAFT] ` row is either an estimate from the ledgers (see *Drafting before the statement* below) or a placeholder drafted from a payment slip (see *Slip before statement* below).
- `จ่ายแล้ว` means *Takumi paid the bank*, not *a friend paid Takumi*.

In code Takumi is a `PrimaryHolder` (`scripts/python/lib/holders.py`), whose `statement_bills` is `True`; Baiboon and Nuta are `SupplementHolder`s. That makes the automatic full-bill payment row refuse him: the one that `/update-bill` and `/record-payment` write on a slip (see *Payments* below). `/prepare-bill` drafts his bills from all three ledgers instead of his own rows, and `/update-bill`'s `refresh_from_transactions` re-estimates such a draft the same way. A final bill can't be refreshed (see *Drafting before the statement* below). Slips, statement PDFs, `Note` and an explicit `paid: true` all work through `/update-bill` as usual.

## Drafting before the statement (2026-10-06)

The friends' bills are drafted when a cycle closes. Takumi asked for his own to be drafted alongside them ("draft my own bills too"), with each friend's subtotal shown. Because every statement line lives in exactly one ledger (next section), the printed card total can be estimated before the PDF arrives:

- **Takumi's statement-line rows**, his bank credits (`CB…`) included.
- **Each friend's statement-line rows on that card**, plus their cashback rows. On these cards a friend's cashback row is the bank's credit booked in their ledger: Krungsri `CB…`, their share of First Choice's NW3, AEON's `CASH BACK …`. The exception is a card whose cashback comes back as household credit rows, which the bank never prints (`lib.crediting`: UOB One). On KTC and CardX, which print one statement per card number, only a friend's `[บัตรหลัก]` rows are on his statement.
- **An unmonitored supplement's total**, which no ledger holds. The user reads it off the bank's app and passes it as `unmonitored`. Lotus's 6524 was ฿2,603.25 for 2026-10.

`/prepare-bill` with `holder: takumi` writes `[DRAFT] <Card> <YYYY-MM>` at that sum. Its `Note` gives the split, e.g. `฿12,046.73 = เว็บ ฿-5.27 + ใบบุญ ฿12,052.00`, plus a warning when the previous bill isn't marked paid, since the statement would carry that balance. Window mode finds the cycles in all three ledgers, so a card Takumi didn't use still gets a draft when a friend did. It skips cycles with nothing on the principal's statement, such as Nuta's own CardX JCB or a ledger reset. The code is `lib/bill_estimate.py` and `lib.bill_draft.draft_primary_bill`.

`/record-statement` completes the draft in place: title, printed `ยอดชำระ` and `Note`. It reports `estimate_off_by` (printed − estimate). A gap is a lead, not an error: a line nobody recorded, a credit that posted for a different amount, or Takumi's share of a pooled credit that isn't in his ledger yet. When rows are added after the draft, `/update-bill` with `refresh_from_transactions` re-estimates it from the three ledgers (`lib.bill_draft.reestimate_primary_bill`). Pass `unmonitored` again for Lotus's. First uses, 2026-10-06: Krungsri NOW ฿3,839.00 → ฿5,739.00 after his `AMP*AIS SERVICESPaymen` ฿2,000 and its `CB` −฿100, and Krungsri Lady ฿4,305.00 → ฿5,073.00 after his Bangchak ฿800, its −฿8 discount and `CB12_BC3P` −฿24.

First batch, 2026-10-06, BC 2026-10-05:

| Draft | `ยอดชำระ` | Split |
|---|---:|---|
| First Choice 2026-10 | 32,657.03 | เว็บ 11,204.44 + ใบบุญ 17,877.51 + นุตา 3,575.08 |
| Krungsri JCB 2026-10 | 12,227.14 | เว็บ 980.00 + ใบบุญ 11,247.14 |
| Krungsri Visa 2026-10 | 12,046.73 | เว็บ −5.27 + ใบบุญ 12,052.00 |
| Lotus's Beyond 2026-10 | 5,372.25 | เว็บ 2,769.00 + unmonitored …6524 2,603.25 |
| Krungsri Lady 2026-10 | 4,305.00 | ใบบุญ 4,305.00 |
| Krungsri NOW 2026-10 | 3,839.00 | ใบบุญ 3,839.00 |
| Central The 1 Redz 2026-10 | 2,763.00 | ใบบุญ 2,763.00 |

First Choice includes the August NW3 credit, ฿800 split three ways and all under `NW3 Cashback 2% (1–31 Aug 2026)`: ใบบุญ −674.54, นุตา −17.84 and Takumi's remainder −107.62. Takumi's share was added the same day, and the draft was re-estimated from ฿32,657.03 to ฿32,549.41.

**Watch the dry run when the 2026-10 statement is recorded.** July's three shares carried the bank's text (`เครดิตเงินคืน NW3_1JUL26-31JUL26`), so `/record-statement` claimed the friends' rows as shares of the bank's line and matched Takumi's remainder. The August rows don't carry that text. A friend's row that says `Cashback` is left out of the share pool, and the first two words (`NW3 Cashback`) won't match the bank's line either. The dry run will then plan a new −฿800 row for Takumi on top of the three shares. Rename the three rows to the printed text before the real run.

## Every statement line lives in exactly one ledger

The ledger model that makes the numbers add up:

| Statement line | Recorded in |
|---|---|
| On a supplement card number | that supplement holder's Transactions DB, plain name |
| On Takumi's primary card, spent by (or charged to) a friend | the friend's Transactions DB, `[บัตรหลัก]`-prefixed — see [[../concepts/supplement-card-model]] |
| On Takumi's primary card, his own | Takumi's Transactions DB |
| Bank fees and Takumi's own credits on the primary card (annual fees, point rebates, cashback his own spending earned) | Takumi's Transactions DB |
| Bank cashback earned by a friend's spending (Krungsri `CB…` campaign credits, AEON `CASH BACK - CREDIT CARD PROMOTION`, First Choice `เครดิตเงินคืน …` shares) | that friend's Transactions DB (`[บัตรหลัก]`-prefixed when printed on the primary card). If the friend's bill for that cycle is already paid, it goes into their **next** cycle so it reduces the next bill (user, 2026-09-27) |
| On a supplement nobody tracks (`unmonitored` — Lotus's 6524, P. PETCHKULJINDA) | no ledger; counted in the bill only |

So for each card, **Σ Takumi's rows + Σ the friends' statement-line rows = the statement's card total**. The friends' household-only rows — computed `UOB ONE CASHBACK n%` credits, `[ยอดยกมา…]` carry-forwards, payment rows — are not statement lines and sit outside that identity.

Bank credits going to Takumi follows his own 2025 ledger, which recorded the bank's `UOB One Cashback 10% 5%` and fee lines on his cards. The friends' cashback is a separate, household-internal credit.

## Recording a statement

[[../../.claude/skills/record-statement/SKILL|/record-statement]] does all of the below from the PDF: it parses the statement (UOB, KBank and AEON so far), splits the lines by card number, adds the `[บัตรหลัก]` prefixes, writes Takumi's rows and creates his bill. Card numbers map to holders through `statement_numbers` in the card YAMLs.

## First statements — 2026-09-27

Takumi began with UOB and KBank (bill cycle 2026-08-25) and AEON (2026-09-10). Each card reconciled to the satang except UOB One, where Notion ran ฿22.00 over the statement: Nuta's `WWW.GRAB.COM BANGKOK TH` ฿22 (7 Aug) had no statement line. Takumi had it archived the same day.

| Bill | `ยอดชำระ` | Split |
|---|---:|---|
| UOB One 2026-08 | 16,005.65 | Takumi 390.97 + Baiboon (2497) 169.00 + Nuta (3818) 15,445.68 |
| UOB World 2026-08 | 4,628.73 | Takumi 4,288.73 + Baiboon (1009) 340.00 |
| UOB Makro 2026-08 | 89.00 | Baiboon `[บัตรหลัก]` 89.00 |
| KBank Shopee 2026-08 | 5,077.00 | Takumi |
| KBank PLUSTINUM 2026-08 | 33,496.44 | Takumi |
| KBank LINE Points 2026-08 | 1,290.00 | Takumi |
| AEON World Mastercard 2026-09 | 35,745.00 | Baiboon `[บัตรหลัก]` 34,260.00 + Takumi 1,485.00 (annual fee − cashback) |
| AEON Rabbit 2026-09 | 1,939.04 | Takumi |
| AEON UnionPay 2026-09 | 5,946.13 | Nuta `[บัตรหลัก]` 5,956.18 + Takumi −10.05 (cashback) |

The same pass renamed 13 friend rows that sat on primary card numbers to `[บัตรหลัก] …` (Baiboon's UOB Makro and AEON World Mastercard rows, Nuta's AEON UnionPay rows), and created six cards in [[takumi-cards]]: KBank PLUSTINUM, KBank Shopee, KBank LINE Points, AEON World Mastercard, AEON UnionPay, UOB Makro.

The UOB statement printed a due date of **18 Sep 2026**; the UOB pattern in [[../concepts/bill-cycle-patterns]] gives 14 Sep (25 Aug + 20). Takumi's new rows carry the printed 18 Sep, and the friends' rows in the same cycle carry 14 Sep.

## Payments

Takumi pays the banks **himself, from his own accounts**, and the transfer slips show that (user, 2026-09-27). A slip is therefore his payment for the whole card, and there is no per-friend split to ask about. Record it as a negative row in **his** Transactions DB with these properties:

- **Cycle and date**: tagged to the paid bill's cycle and dated on the slip.
- **Multiplier**: none.
- **Name**: `ชำระบิลเต็มจำนวน` (paid in full) for a single slip. When several slips add up to the bill, use `ชำระบางส่วน` (partial payment) for the earlier ones and `ชำระเพิ่มบางส่วนจนครบ` (final partial payment completing the bill) for the last. Example: UOB One 2026-08 was paid as ฿15,420.18 on 29 Aug plus ฿585.47 on 31 Aug.

Then attach the slip(s) with `/update-bill` and set `จ่ายแล้ว` once the slips sum to `ยอดชำระ`. Since 2026-09-28, `/update-bill` also writes these rows when given the slip's `payment_amount`, plus `payment_covers` when the slip pays friends' shares. It picks the name from what the bill already has paid.

**Slip before statement** (user, 2026-09-28: "put the payment slips to new drafted bills; I'll bring the statements later"). When he pays before the PDF arrives, `/update-bill` creates a placeholder for the slip: `[DRAFT] <Card> <YYYY-MM>`, with no `ยอดชำระ` and a Note naming the slips (`lib.bill_draft.draft_statement_bill`). `/record-statement` later fills in that same row (title, `ยอดชำระ`, Note) instead of creating a second one. The payment rows wait for it, because full vs partial depends on the bill total. First case: KTC Digital VISA (฿20.00), KTC Mastercard …5549 (฿1,545.30) and KTC UnionPay …1346 (฿967.26 + ฿940.00), all cycle 2026-09-27 and paid 28 Sep.

**Krungsri-family cards pay by auto-debit** (user, 2026-09-27), so there is no slip. The group is the `issuer: Krungsri` cards: First Choice, Central The 1 Redz, Krungsri NOW, Krungsri JCB, Krungsri Visa, Krungsri Lady, and Lotus's Beyond (issued through Lotus Money Service, a Krungsri Consumer partner; `issuer: Krungsri` since 2026-09-27). Each paid bill gets one row named `AUTO DEBIT`:

- **Amount**: the negative full `ยอดชำระ`.
- **Cycle and date**: dated on the due date and tagged to the paid bill's cycle.
- **Multiplier**: none.

The bill's `จ่ายแล้ว` is then set by hand, with nothing attached to `หลักฐานการชำระ`. His 2025 ledger named these rows `AUTO DEBIT - <card>`. From 2026 the name is just `AUTO DEBIT`, because the `Card` relation already says which card.

**KTC: transfer rows at statement time** (user, 2026-09-27). KTC bills the principal and each supplement card separately, one PDF per card number, and Takumi may pay a KTC bill in one transfer or split it. So when his principal statement carries a friend's `[บัตรหลัก]` line, add the `โอนยอดจาก<friend>` row **when the statement is recorded**. Date it on the statement date, tag it to that cycle, and set `×0`. His card balance then equals the bill before payment, and the payment row(s) can mirror the slip(s) exactly. First case: KTC UnionPay 2026-08, `โอนยอดจากใบบุญ` +376.00 for `[บัตรหลัก] CMU FITNESS`, making ฿1,447.60 = the bill.

**Bank credits that post after the cut-off pay the closed bill** (user, 2026-10-06). A credit that lands between the statement and its due date, such as a pay-with-points credit or a waived fee, lowers what the bank wants for the closed statement. So it goes on that bill as a payment:

- **Old cycle**: one `ชำระบางส่วน` / `ชำระเพิ่มบางส่วนจนครบ` row per credit, for the credit's amount and dated on its posting date. The Note names the bank line. Write it with `lib.payments.record_primary_payment`, since `/update-bill` only writes payment rows when a slip is attached. A friend's PWP credit also brings in the friend's `โอนยอดจาก<name>` row for her statement-line total.
- **Next cycle**, only for a credit on Takumi's own charges: the bank's line, plus `[ยกยอดมาจาก <YYYY-MM>]` for the opposite amount, both `×0`. The pair stops the credit counting twice when `/record-statement` reads the next PDF. A friend's PWP credit already has that pair in her ledger: `[หักลบหนี้เก่า] PWP: <merchant>` (debt offset) in the purchase's cycle, then `PWP: <merchant>` and `[ยกยอดมาจาก <YYYY-MM>]` in the cycle that prints it.

First case: UOB Makro 2026-09 (฿3,161.71). The ฿440.35 slip was followed by Baiboon's `PWP: MAKRO_CHIANGMAI 2` ฿171.43 (26 Sep, with `โอนยอดจากใบบุญ` +688.35) and the waived `CARD MEMBERSHIP FEE - WITH VAT 7%`, `CR CARD MEMBERSHIP FEE - INC OF VAT` ฿2,033.00 (30 Sep, with the cancelling pair on 2026-10-22). That leaves Baiboon's ฿516.92 and ฿0.01.

### Overpayments

When the payments after a statement add up to more than it asked for, the bank credits the excess on the next statement and prints it as part of the previous balance. `/record-statement` reports this as `overpaid` and says so in the bill's Note (2026-10-06). Before that change it was labelled "balance carried from the previous statement". The ledger needs three rows on that card, all `×0` and dated on the extra payment:

| Row | Amount | Cycle |
|---|---:|---|
| `ชำระบางส่วน`, Note naming the bank line and slip | −excess | the overpaid cycle |
| `[ยอดยกมาจากรอบ <YYYY-MM>]` | +excess | the overpaid cycle |
| `[ยอดยกมาจากรอบ <YYYY-MM>]` | −excess | the next cycle |

Attach the extra slip to the overpaid bill with `record_payment: false`, since the script would call it a payment completing the bill. First case: UOB One 2026-08. Takumi's ฿585.47 slip on 31 Aug already covered Baiboon's ฿169.00. Her ฿160.55 then went to UOB a second time (`PAYMENT THANK YOU - BAY 0025/7603`, 31 Aug), and the 25 Sep statement credited it.

### Friends' balances are debts to Takumi, not to the bank

Baiboon's and Nuta's open balances are what they owe **Takumi**. His payment to the bank never touches their ledgers. Their balances clear only through their own `ชำระ…` rows when they transfer to him.

On his side, a full-bill payment would leave his own card balance at **minus the friends' statement lines** on that card. It also leaves out any `unmonitored` supplement. So each payment is paired with one **`โอนยอดจาก<friend>`** row per friend in **his DB only** (user, 2026-09-27, carrying on his 2025 practice). That row brings the friend's share back onto his card without touching the friend's ledger:

- **Name**: `โอนยอดจากใบบุญ` / `โอนยอดจากนุตา`, with no card suffix. The `Card` relation already names the card; his 2025 rows read `โอนยอดจากใบบุญ - UOB One`.
- **Amount**: positive. It is the friend's statement-line sum on that card for the paid cycle: `lib.statements.attribution.is_statement_line_row` over their rows, so household-only rows (their payments, our computed cashback, carry-forwards) don't count.
- **Multiplier**: `×0`. The points formula earns on any positive amount, and those points were already counted on the friend's rows.
- **Date and cycle**: dated on the day his payment covered that share and tagged to the paid bill's cycle.

With the transfers in place, every paid card nets to zero. First batch, same day. Amounts are net of the friend's cashback: the AEON and Krungsri JCB/Visa/NOW figures were reduced once the cashback moved to the friends.

| Card | `โอนยอดจากใบบุญ` | `โอนยอดจากนุตา` |
|---|---:|---:|
| UOB One 2026-08 | 169.00 | 15,445.68 |
| AEON World Mastercard 2026-09 | 34,140.00 | |
| AEON UnionPay 2026-09 | | 5,946.13 |
| First Choice 2026-09 | 39,908.81 | 1,854.84 |
| Krungsri JCB 2026-09 | 768.00 | |
| Krungsri Visa 2026-09 | 4,170.00 | |
| Krungsri NOW 2026-09 | 630.42 | |

**Unmonitored supplements** get the same treatment under the name `โอนยอดจากบัตรเสริม`, again `×0` and positive (user, 2026-09-27; the name comes from his 2025 ledger, 3,052.16 on 2025-04-05). The 6524 card on Lotus's Beyond (P. PETCHKULJINDA) is billed but not tracked in any ledger, so its share isn't a friend's debt. First row: Lotus's Beyond 2026-09, 2,363.00.

### Cashback moved to the friends (2026-09-27)

`/record-statement` currently books every bank credit to Takumi, because `is_statement_line_row` skips a friend's cashback-like rows. On the first statements that duplicated three Krungsri credits Baiboon already had: `CB88_SAV1` on NOW (−100), `CB15_ SUP1` on Visa (−120), and `CB12_BC3P` on JCB (−24, spelled `…1AUG26-31AUG` in her ledger). It also put two AEON credits in his ledger that were earned by friends: `CASH BACK - CREDIT CARD PROMOTION` on AEON UnionPay (−10.05, Nuta's) and on AEON World Mastercard (−120.00, Baiboon's). His Krungsri copies were archived. The AEON pair moved to `[บัตรหลัก] CASH BACK - CREDIT CARD PROMOTION` in the friends' BC 2026-10-10 cycle, because their 2026-09 bills were already paid.

Baiboon's half of the pair was undone on 2026-10-09 (user). Her −฿120.00 is Everyday with AEON (NTW1) for the cycle billed 10 Aug. Takumi paid it to her by transfer instead, so her row was archived and the slip settles her tracker row `Everyday with AEON 10 Aug`. The credit goes back to his ledger in the 2026-09-10 cycle, like ttb `CB BANGCHAK` below. A dry run of the 10 Sep AEON statement now plans that one row (−฿120.00, `×0`) and moves Baiboon's split on AEON World back to ฿34,260.00. See [[../promotions/aeon-2026#NTW1 for the cycle billed 10 Aug, paid by transfer|aeon-2026]].

His own credits stayed with him: Krungsri Lady `CB12_BC3P` (his card), First Choice `เครดิตเงินคืน` −21.32 (his remainder after the split), and Lotus's Beyond's `CB…` rows.

Since 2026-09-28 the attribution handles this itself. A friend's row that carries the bank's credit text *is* that primary-section line, booked in their ledger. A match needs the same leading words (`CB12_BC3P CAMPAIGN`, so a truncated date range still matches), the same amount and a date within 3 days. The row can sit in the statement's cycle or, if the credit landed after their bill was paid, in the next one (the AEON pair). It's matched as-is, without the `[บัตรหลัก]` rename, and Takumi gets no copy. A credit only Takumi carries (ttb `CB BANGCHAK`, which he pays Baiboon himself) stays his. Re-running every statement recorded so far plans no new rows.

### KTC — first statements (2026-09-27)

Closing 2026-08-27, due 2026-09-11. Each PDF holds only Takumi's principal card; Baiboon's and Nuta's KTC UnionPay supplements get statements of their own.

| Bill | `ยอดชำระ` | Split |
|---|---:|---|
| KTC UnionPay 2026-08 (1346) | 1,447.60 | Takumi 1,071.60 + Baiboon `[บัตรหลัก]` 376.00 |
| KTC Digital VISA 2026-08 (0581) | 1,841.90 | Takumi |
| KTC JCB 2026-08 (0059) | 269.00 | Takumi |

KTC's rule that the supermarket earns no points was applied by hand to Takumi's two `RIMPING` rows on UnionPay. Petrol on KTC (`BANGCHAK …` ฿940) was left at `×1`; the September statement showed it earns (below).

### KTC — 2026-09 statements (recorded 2026-09-29)

Closing 2026-09-27, due 2026-10-12. Takumi paid all three from slips on 28 Sep, before the PDFs arrived, so `/record-statement` completed the slip-first placeholders.

| Bill | `ยอดชำระ` | Split | Paid |
|---|---:|---|---|
| KTC UnionPay 2026-09 (1346) | 3,797.96 | Takumi 1,907.26 + Baiboon `[บัตรหลัก]` 1,890.70 | ✓ ฿1,907.26 (two `ชำระบางส่วน`, 28 Sep) + Baiboon's ฿1,890.70 (`ชำระเพิ่มบางส่วนจนครบ`, 6 Oct) |
| KTC Mastercard 2026-09 (5549) | 1,545.30 | Takumi | ✓ |
| KTC Digital VISA 2026-09 (0581) | 20.00 | Takumi | ✓ |

- `โอนยอดจากใบบุญ` +1,890.70 was added at statement time, as the KTC rule above says. In August Baiboon paid her 1346 share to KTC herself (`Payment-BAY Internet` −376.00 on 6 Sep). In September she transferred it to Takumi with her own …2310 bill (฿9,797.38, 6 Oct) and he paid KTC the same day (Krungsri bill payment, memo `1346 - KTC UnionPay (ส่วนของใบบุญ)`). Because the transfer row already existed, that slip took only `payment_amount`, no `payment_covers`.
- Baiboon's own statement (…2310, ฿7,906.68) went on **her** KTC UnionPay bill with the 1346 PDF, as in August: ฿9,797.38 = 7,906.68 + her 1,890.70 of `[บัตรหลัก]` shares. Three of its lines (฿514.00) were missing from her ledger and were added.
- Points: `CNX BC DOM L2 LS(6110)` (Bonchon at Chiang Mai airport, ฿478.46, split Takumi 281.06 / Baiboon 197.40) earned nothing: fast food, MCC 5814, KTC UnionPay rule (16). Both halves are `×0`. The petrol lines (`BANGCHAK …` ฿940, `BSRC-…` ฿686.20) earned, so KTC UnionPay has no petrol exclusion (see [[../promotions/ktc-forever|ktc-forever]]).
