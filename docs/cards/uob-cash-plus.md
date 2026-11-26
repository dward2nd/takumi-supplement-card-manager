---
tags: [card, uob, cash-card, loan]
issuer: UOB
holders: [takumi, nuta]
points: none
cashback: none
---

# UOB Cash Plus

UOB's cash card (บัตรกดเงินสด, a cash-withdrawal card): a personal-loan line, **not a credit card**. Takumi holds it. Since 2026-10-27 it has a row in his Cards DB and in [[../people/nuta|Nuta]]'s, both titled `UOB Cash Plus`, created when Nuta's UNITRIP charge moved onto it as a cash loan.

## No points, no cashback, ever

Thai cash cards earn no reward points and no cashback on anything (user, 2026-10-27). The card's YAML sets `points_default: "×0"`, and the `CashCard` earning class (`scripts/python/lib/earning/families.py`) forces `×0` and an unset `% cb` on every row, whatever a promotion says, with the Note `Cash card — UOB Cash Plus earns no points or cashback.` [[../../.claude/skills/populate-installment/SKILL|/populate-installment]] reclassifies each new term, so later terms inherit this. In the Cards rows, `บาทต่อ 1 คะแนน` (baht per point) is `0`, `Card Network` is `Unspecified` and `ความพรีเมียม` (premium tier) is `ไม่มี` (none).

## No supplements: friends' rows are `[บัตรหลัก]`

A cash card can't have supplement cards, so it is in Takumi's name only. A row a friend owes on it goes in that friend's ledger with the `[บัตรหลัก]` (primary card) prefix, on the friend's own `UOB Cash Plus` Cards row, like any other charge on Takumi's primary card (see [[../concepts/supplement-card-model#`[บัตรหลัก]` rows — primary-card charges on a supplement ledger|supplement-card-model]]). Takumi's statement bill for the card is the printed total, which includes those rows ([[../databases/takumi-bills|takumi-bills]]).

## Moving a charge onto a cash loan (first case, 2026-10-27)

Nuta's `UNITHAI TRIP CO.,LTD. BANGKOK TH` ฿20,000 (5 Oct 2026) was charged to her UOB One supplement and billed in cycle 2026-10-22. She turned it into a 12-month installment at 8.99% a year. UOB didn't convert the charge on UOB One: Takumi drew a ฿20,000 cash loan on Cash Plus and paid that into UOB One. So the charge stays on UOB One, with its 1% cashback, and the ledgers record the move as a payment:

| Ledger | Card | Row | Amount | Cycle |
|---|---|---|---:|---|
| Nuta | UOB One | `ชำระบางส่วน` (partial payment), dated on the slip (27 Oct) | −20,000.00 | 2026-10-22 |
| Takumi | UOB One | `ชำระบางส่วน`, Note `Slip memo: นุตาผ่อนจ่าย UNITRIP` | −20,000.00 | 2026-10-22 |
| Takumi | UOB One | `โอนยอดจากนุตา` (transfer from Nuta), `×0` | +20,000.00 | 2026-10-22 |
| Nuta | UOB Cash Plus | `[บัตรหลัก] CASH LOAN INSTALLMENT 01/12`, `×0`, no `% cb` | 1,748.94 | 2026-11-25 |

The slip (27 Oct 16:02, Takumi's One Account → UOB One card …4672) is attached to both UOB One 2026-10 bills, Nuta's and Takumi's. On Nuta's side it stands for her payment, settled by taking on the loan. On Takumi's side it is a bank payment like any other ([[../databases/takumi-bills#Payments|payments]]). Her bill still owes ฿12,360.14, and Takumi's next UOB One slip covers `nuta: 12,824.18`: her statement-line share of ฿32,824.18 less this ฿20,000.

The term amount ฿1,748.94 is the amortised payment for ฿20,000 at 8.99% ÷ 12 a month over 12 months. The single-line placeholder was replaced on 2026-11-26 by what the UOB app shows: see [[#Statement lines: principal and interest (UOB app, 2026-11-26)|statement lines]]. The first statement settled where it prints and its card number ([[#First statement (25 Nov 2026)|below]]). Still open: the last term's amounts.

## Statement lines: principal and interest (UOB app, 2026-11-26)

The UOB app shows each loan's term as **two lines**, a principal (`PRIN`) and an interest (`INT`) line, named by loan: `MPFCDM00001` for the ฿20,000 loan, `MPFCDM00002` for the ฿16,000 one (numbered in drawing order). Term 01/12 of each, in the cycle closing **2026-11-25**, which confirms the assumed `uob` cycle:

| Loan | Row in Nuta's ledger | ยอดชำระ | How the bank gets it |
|---|---|---:|---|
| ฿20,000 (drawn 27 Oct) | `[บัตรหลัก] MPFCDM00001 MONTHLY PRIN 01/12` | 1,599.11 | ฿1,748.94 instalment − 20,000 × 8.99% ÷ 12 (฿149.83) |
| | `[บัตรหลัก] MPFCDM00001 MONTHLY INT 01/12` | 147.78 | 20,000 × 8.99% × 30/365 (27 Oct–25 Nov, both ends counted) |
| ฿16,000 (drawn 16 Nov) | `[บัตรหลัก] MPFCDM00002 MONTHLY PRIN 01/12` | 1,279.28 | ฿1,399.15 instalment − 16,000 × 8.99% ÷ 12 (฿119.87) |
| | `[บัตรหลัก] MPFCDM00002 MONTHLY INT 01/12` | 39.41 | 16,000 × 8.99% × 10/365 (16–25 Nov) |

So principal follows the 30/360 amortisation table: the fixed instalment less a flat month's interest on the opening balance, rising each month. Interest is charged on the **actual days** since the last statement (from the draw date for term 1). A term is therefore never the nominal instalment: term 1 came to ฿1,746.89 and ฿1,318.69, ฿3,065.58 in all against the ฿3,148.09 first estimated. Both formulas reproduce the app to the satang, but they are inferred from one month. Check them against the next term.

The two placeholder rows (`[บัตรหลัก] CASH LOAN INSTALLMENT 01/12` ฿1,748.94 and ฿1,399.15) were archived and the four rows above written in their place. `[DRAFT] UOB Cash Plus 2026-11` on Nuta's Bills DB was refreshed to ฿3,065.58.

**`/populate-installment` can't produce later terms.** It copies the seed term's amount into the next term, and it tells plans apart by amount within 2%. Both PRIN lines grow every month, and the INT lines change with the balance and the day count: the ฿16,000 loan's interest jumps from ฿39.41 (10 days) to about ฿108.77 (30 days to 25 Dec), out of its own cluster. By the formulas above, term 02/12 should be PRIN ฿1,611.09 + INT ≈ ฿135.96 on the ฿20,000 loan and PRIN ฿1,288.87 + INT ≈ ฿108.77 on the ฿16,000 one. Until a cash-loan class computes the schedule, enter each term from the app or the statement, and pass `skip_populate_installments: true` to `/prepare-bill` for a Cash Plus bill.

## Second loan (2026-11-16)

Nuta's `UNITHAI TRIP CO.,LTD. BANGKOK TH` ฿15,976 (UOB One, 16 Nov 2026, cycle 2026-11-25, 1% cashback) went the same way: a ฿16,000 Cash Plus loan over 12 months at 8.99% a year, drawn the same day (user). The same amortisation formula gives **฿1,399.15 a term** (฿16,789.80 in all, ฿789.80 interest). The user expects term 1 in the same cycle as the first loan's, so `[บัตรหลัก] CASH LOAN INSTALLMENT 01/12` ฿1,399.15 is filed on BC 2026-11-25, due 2026-12-15, next to the first plan's ฿1,748.94.

The app names this loan `MPFCDM00002` (the first is `MPFCDM00001`), so the two plans no longer share a line name, and the 16 Nov loan does bill its first term in the 25 Nov cycle, for 10 days' interest ([[#Statement lines: principal and interest (UOB app, 2026-11-26)|above]]).

Takumi paid **฿15,976** into UOB One on 26 Nov 2026, 12:17, from his One Account to card …4672 with memo `ทัวร์จีนนุตา`. He paid the charge, not the ฿16,000 loan. The rows follow the first loan's:

| Ledger | Card | Row | Amount | Cycle |
|---|---|---|---:|---|
| Nuta | UOB One | `ชำระบางส่วน`, dated 26 Nov | −15,976.00 | 2026-11-25 |
| Takumi | UOB One | `ชำระบางส่วน`, Note `Slip memo: ทัวร์จีนนุตา` | −15,976.00 | 2026-11-25 |
| Takumi | UOB One | `โอนยอดจากนุตา`, `×0` | +15,976.00 | 2026-11-25 |

The slip is attached to both UOB One 2026-11 bills, and both stay unpaid. Nuta's bill (฿30,536.06) still owes ฿14,560.06. Hers was finalized when the 25 Nov statement was attached (2026-11-27). Takumi's stays `[DRAFT]` until /record-statement completes it.

## First statement (25 Nov 2026)

Cash Plus has a **statement of its own**, not a section of the bundled UOB credit-card PDF. It is a separate account (`816-…`; the credit cards' bundle is `810-…`), printed on the same day with the same due date: dated 25 Nov 2026, due 18 Dec 2026. The `uob` cycle pattern gives 15 Dec, and the credit cards printed 18 Dec too. The summary table heads its column `CASHPLUS NUMBER` instead of `CARD NUMBER (S)`. The card is `4043 65XX XXXX 5024`, now `"5024": takumi` in the card's `statement_numbers`.

The lines are the four the app showed, to the satang: `MPFCDM00002 MONTHLY INT 01/12` ฿39.41, `MPFCDM00001 MONTHLY INT 01/12` ฿147.78, `MPFCDM00002 MONTHLY PRIN 01/12` ฿1,279.28, `MPFCDM00001 MONTHLY PRIN 01/12` ฿1,599.11. `SUB TOTAL` / `TOTAL BALANCE` ฿3,065.58, minimum payment the same, no fee. Page 2 splits the balance as principal ฿2,878.39 + interest ฿187.19. Nuta's four `[บัตรหลัก]` rows matched it with no drift ([[../../.claude/skills/audit-bill/SKILL|/audit-bill]], 2026-11-27).

**The layout differs from the credit cards'.** `UOB CASH PLUS 4043 65XX XXXX 5024` puts the heading and the card number on one line, and the total is a bare `TOTAL BALANCE 3,065.58` with no `- <PRODUCT>`. At first `lib/statements/uob.py` found no account in it, so Takumi's `UOB Cash Plus 2026-11` bill was filed by hand with [[../../.claude/skills/update-bill/SKILL|/update-bill]]: ฿3,065.58 (= นุตา ฿3,065.58), finalized, PDF attached. His estimate had been ฿3,148.09, drafted before her placeholder rows became the PRIN/INT lines. Nuta's bill took the same PDF and was finalized at ฿3,065.58.

The parser has read both forms since 2026-11-27 (user: "teach the Cash Plus layout"), and the main statement's parse came out unchanged. [[../../.claude/skills/record-statement/SKILL|/record-statement]] then recorded this statement: Nuta's four rows matched with no drift and got their `Process Date`, and the existing bill was left as filed. From term 02/12 on, record the Cash Plus PDF like any UOB statement. Takumi's `[DRAFT]` is completed the usual way, but Nuta's term rows still have to be entered first (see above), since the recording never writes a friend's lines.
