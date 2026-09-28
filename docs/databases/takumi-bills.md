---
tags: [database, takumi, bills]
owner: takumi
role: bills
---

# Takumi — Bills (`บิลเรียกเก็บค่าบัตรเครดิตของเว็บ`)

One row per card per **bank statement** — the amount [[../people/takumi|Takumi]] actually pays the issuer. Created by Takumi on 2026-09-27 when he started keeping his own ledger again, and shared with the scripts' integration the same day.

- **Collection ID**: `63dcb755-f0f1-83df-aaa8-871bb9069dae` (data source; its database is `3e3cb755-f0f1-80a0-80be-f0151b47a900`)
- **Schema**: identical to [[baiboon-bills]] — untitled title property, `Card` (SELECT), `วันตัดรอบบิล` (bill cycle date), `ยอดชำระ` (amount due), `จ่ายแล้ว` (paid), `ใบแจ้งยอด (PDF)` (statement), `หลักฐานการชำระ` (payment evidence), `Note`. It started as a copy of Baiboon's, so its `Card` options began as her list; new cards add their option on first use.
- **Last schema-verified**: 2026-09-27

## Different in kind from the supplement holders' Bills

A supplement holder's bill is **computed**: the sum of *their own* Transactions rows for the cycle, drafted by `/prepare-bill` and reconciled against the statement afterwards. Takumi's bill is **the statement**:

- `ยอดชำระ` is the issuer's printed total for that card — principal **plus every supplement section**. Takumi pays the whole card to the bank, usually after Baiboon and Nuta have paid their shares to him.
- The title has no `[DRAFT] ` prefix; there is no pre-statement estimate.
- `จ่ายแล้ว` means *Takumi paid the bank*, not *a friend paid Takumi*.

In code Takumi is a `PrimaryHolder` (`scripts/python/lib/holders.py`), whose `statement_bills` is `True`; Baiboon and Nuta are `SupplementHolder`s. That makes three automations refuse him: `/prepare-bill` (a sum of his own rows would understate the bill), `/update-bill`'s `refresh_from_transactions` (same reason), and the automatic full-bill payment row that `/update-bill` and `/record-payment` write on a slip (see *Payments* below). Slips, statement PDFs, `Note` and an explicit `paid: true` all work through `/update-bill` as usual.

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

Then attach the slip(s) with `/update-bill` and set `จ่ายแล้ว` once the slips sum to `ยอดชำระ`. `/update-bill` won't write the payment row for him (`statement_bills`), so it goes in through `/add-transaction`.

**Krungsri-family cards pay by auto-debit** (user, 2026-09-27), so there is no slip. The group is the `issuer: Krungsri` cards: First Choice, Central The 1 Redz, Krungsri NOW, Krungsri JCB, Krungsri Visa, Krungsri Lady, and Lotus's Beyond (issued through Lotus Money Service, a Krungsri Consumer partner; `issuer: Krungsri` since 2026-09-27). Each paid bill gets one row named `AUTO DEBIT`:

- **Amount**: the negative full `ยอดชำระ`.
- **Cycle and date**: dated on the due date and tagged to the paid bill's cycle.
- **Multiplier**: none.

The bill's `จ่ายแล้ว` is then set by hand, with nothing attached to `หลักฐานการชำระ`. His 2025 ledger named these rows `AUTO DEBIT - <card>`. From 2026 the name is just `AUTO DEBIT`, because the `Card` relation already says which card.

**KTC: transfer rows at statement time** (user, 2026-09-27). KTC bills the principal and each supplement card separately, one PDF per card number, and Takumi may pay a KTC bill in one transfer or split it. So when his principal statement carries a friend's `[บัตรหลัก]` line, add the `โอนยอดจาก<friend>` row **when the statement is recorded**. Date it on the statement date, tag it to that cycle, and set `×0`. His card balance then equals the bill before payment, and the payment row(s) can mirror the slip(s) exactly. First case: KTC UnionPay 2026-08, `โอนยอดจากใบบุญ` +376.00 for `[บัตรหลัก] CMU FITNESS`, making ฿1,447.60 = the bill.

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

His own credits stayed with him: Krungsri Lady `CB12_BC3P` (his card), First Choice `เครดิตเงินคืน` −21.32 (his remainder after the split), and Lotus's Beyond's `CB…` rows. Takumi is building something to manage this attribution. Until it lands, check each new statement run for cashback a friend already carries before trusting the split. Re-running `/record-statement` on the 2026-09-05 Krungsri or 2026-09-10 AEON statement would recreate the archived rows.

### KTC — first statements (2026-09-27)

Closing 2026-08-27, due 2026-09-11. Each PDF holds only Takumi's principal card; Baiboon's and Nuta's KTC UnionPay supplements get statements of their own.

| Bill | `ยอดชำระ` | Split |
|---|---:|---|
| KTC UnionPay 2026-08 (1346) | 1,447.60 | Takumi 1,071.60 + Baiboon `[บัตรหลัก]` 376.00 |
| KTC Digital VISA 2026-08 (0581) | 1,841.90 | Takumi |
| KTC JCB 2026-08 (0059) | 269.00 | Takumi |

KTC's rule that the supermarket earns no points was applied by hand to Takumi's two `RIMPING` rows on UnionPay. Petrol on KTC (`BANGCHAK …` ฿940) is still undecided and was left at `×1`.
