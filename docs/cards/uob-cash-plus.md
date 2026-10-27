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

The term amount ฿1,748.94 is the amortised payment for ฿20,000 at 8.99% ÷ 12 a month over 12 months. The bank may round the first and last terms differently. Everything here waits on the first statement:

- the bank's name for the line (`CASH LOAN INSTALLMENT` is a placeholder);
- the first and last terms' amounts;
- the statement cycle. The card YAML assumes the UOB credit cards' `uob` pattern (cycle on the 25th, shifted earlier off weekends and holidays; due 20 days later), so term 1 is filed on 2026-11-25, due 2026-12-15. The loan was drawn after the 22 Oct close;
- whether it prints on the bundled UOB statement, and its card number (`statement_numbers` is empty).

Later terms come from `/populate-installment` as each cycle closes.
