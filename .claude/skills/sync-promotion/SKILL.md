---
name: sync-promotion
description: Bring one Promotion Bureau row (one quota period of a bank campaign) up to date — create it if new, link each holder's qualifying transactions, split the bank's reward first come first served, write `เงินคืนรวม` / `เงินคืนส่วน<name>` and each holder's `รายการติดตามเครดิตเงินคืนของ<name>` tracker row (cashback campaigns), check every linked row's `% cb` / multiplier / points-used against the split, and render the campaign summary into the Bureau page. Covers NW3/NW4, ON3/ON4, DLV3, IS3/IS4 (First Choice); the BTS draw (Krungsri VISA + First Choice, lucky-draw rights); ONQ3, SUP1, PTT2, J Dining, DN, Bangchak/BC3P and from Oct 2026 Bangchak700/BXP, LOTA/LOTB (Krungsri Card, per card account); LBS3, SMP1, SMT2, LAN and QRT4 (Lotus's); ttb so smart 1% and ttb's fuel, hypermarket (BMG/BGO) and MUJI (MUJC) campaigns; AEON Rabbit, AEON World 5% and Everyday with AEON (NTW1); UOB One 10%/5% and 1%, UOB World ×5, EPW538/SPW796 and SPW592 supermarkets; the UNIQLO campaigns UNO (UOB), UNQ (Krungsri, per card account), UQN (KBank, per card), UQCB (ttb) and UQC (CardX); KBank MKR at Makro (per card); UOB Makro's Gold Mission UMK26 (Makro stores, Makro PRO app per slip, other spend); CardX HY1 at hypermarkets; UnionPay QR 6% on KTC UnionPay (per card number, with UnionPay's monthly pool). Use when the user says "sync NW3", "update the Promotion Bureau for <promo>", "who gets how much of the UOB One cashback?", "create the September rows for EPW538", "check the UOB World quota", or after new statement rows are recorded. Also lays out drift against the bank app's eligible-spend figure.
---

# sync-promotion

One Bureau row ([[../../../docs/databases/promotion-bureau|Promotion Bureau]]) = one **quota period**: the window the bank counts a limit over. It's named `<year>M<month> — <campaign>`, where the month is the calendar month, the month of the statement cycle's closing date, or the campaign's first month ([[../../../docs/concepts/promotion-bureau|concept note]]). This skill keeps everything derived from that row consistent with the transactions linked to it.

## Usually automatic

[[../add-transaction/SKILL.md|/add-transaction]], [[../update-transaction/SKILL.md|/update-transaction]] and [[../record-statement/SKILL.md|/record-statement]] re-sync the Bureau rows their rows touch after every write (`lib.bureau.follow`; user, 2026-09-28). That follow-up runs this skill's core (`lib.bureau.runner.run`) with `link_candidates`, **applies** the `field_mismatches` instead of just listing them, and repeats until nothing changes. It never creates a Bureau row. So run this skill by hand to:

- **create a new period's row.** The writers report it under `promotions.missing`, with the `create_with` spec ready to pass here.
- **reconcile against the bank's figure** (`bank_spend`), or rewrite a page summary.
- **re-sync after a change the writers don't cover**: archiving a row, editing in Notion directly, or `/add-installment` / `/populate-installment` / `/record-payment` rows.

## Primary execution path

```sh
echo '{"promotion":"2026M9 — NW3 cb 2%","bank_spend":36803.92}' \
  | uv run --project scripts/python scripts/python/sync-promotion/cli.py --dry-run
```

Always dry-run first and show the user the shares, `flagged`, `unlinked_candidates`, `field_mismatches` and `drift`; then run without `--dry-run`.

| Field | Default | Meaning |
|---|---|---|
| `promotion` | — | Bureau row Name (exact), page ID or URL |
| `start`, `end` | — | Create the row when no row has that Name. ISO dates; for a cycle quota, `start` is the previous BC date and `end` the day before this cycle's BC date (spend on the BC date lands on the next statement). Refused unless a campaign class matches the Name and period. A dry run previews the new period against a stand-in row (nothing is written) |
| `bank_spend` | — | The total of the bank app's eligible-transactions list (Krungsri-family apps show one; other issuers unknown). Adds a `drift` block: per-date totals to read against the app, dates whose total equals the gap, repeated rows. (A single row equal to the gap is no lead: every even half of a split charge is one.) |
| `link_candidates` | `false` | Link the campaign cards' **eligible** unlinked rows in the period (by transaction date, or by `Bill Cycle Date` for a cycle quota). Uncertain/excluded rows are never linked. Refunds (negative merchant rows, `[ยกเลิก] …`) are screened as the charge they give back and linked too; the split nets them off their holder's charge ([[../../../docs/concepts/promotion-bureau#Refunds come off the charge they give back|refunds]]). Existing `Promotion` links on a row are kept |
| `replace_summary` | `false` | Rewrite the page body even if it already has content (it's written automatically only when empty) |
| `quota_gone` | — | For a campaign with a nationwide pool (UnionPay QR): the day it ran out, as the bank announced it (UnionPay's Facebook page). Written to `Quotas Exceeded Date`, replacing a later sighting |

## What it does

1. **Resolves the campaign class** from the row's Name + dates (`lib.bureau.promotion_for`). No class → error: a new campaign needs a class first (*New campaign* below).
2. **Reads linked rows** per holder from the Transactions side (a page's own relation list is cut off at 25) and checks them against the `ยอดจาก<name>` rollups.
3. **Screens** each row: not a purchase, not counted by this quota (`qualifies`), or hit by one of the bank's `rules` → `flagged`. Informational only; links are the household's call.
4. **Splits** the reward **first come, first served** by `Transaction Datetime` with the campaign's own `allocate`: ladder steps or one-off bands (NW3/NW4, EPW538/SPW796, ON3/ON4, DLV3, ONQ3, LBS3, SMP1/SMT2, LAN, NTW1, SPW592; NW4 first caps supermarket and fuel spend at ฿30,000 a month each), a per-row rate until a pooled credit cap (UOB One, ttb so smart, AEON), a fixed credit per slip until a cap (IS3/IS4, SUP1, PTT2, J Dining, BXP, LOTA/LOTB, MUJC, BGO, the UNIQLO campaigns, QRT4), a points quota (UOB World), or draw rights per slip up to a monthly count (BTS). Same-time rows share a straddled boundary pro rata. `boundary` shows that group.
5. **Cashback campaigns** write `เงินคืนรวม` and each `เงินคืนส่วน<name>`, then upsert trackers: one row per holder with a positive share, titled `tracker_title` (`UOB One 1% 25 Aug—24 Sep`), dated the period start — or, for a statement-cycle quota, the statement date that bills it (`tracker_date`) — `Card` = the holder's campaign card (for a multi-card campaign, the one carrying most of their spend), `Promotion` = the Bureau row, `Expected Cashback` = the share. `เงินคืนรวม` follows the split while it equals Σ shares; a figure typed by hand is never overwritten, and a split that disagrees with it is held back with a warning. A ticked tracker row is never changed; a same-titled row without a `Promotion` link is reported, not duplicated. **Points campaigns** (UOB World) have no money and no trackers. **Rights campaigns** (BTS) write the month's count to `สิทธิ์ลุ้นรางวัล` and nothing else. A hand-made tracker with another title is picked up once it's linked to the Bureau row: link it before the first sync so it isn't duplicated.
6. **Checks every linked row's fields** against the split (`expected`): `% cb` for the card's own cashback (full rate inside the quota; unset on the partly paid boundary and after), or the multiplier and `ใช้คะแนน` for UOB World. An overlay campaign (EPW538, `marks_rows = False`) claims no row fields: a row can earn from several campaigns of the same bank, but it has one `% cb`. Disagreements come back under `field_mismatches`, each with a ready `/update-transaction` entry under `update` (a multiplier change unticks the old box via `properties`). Here they're only reported: pass the `update` entries to [[../update-transaction/SKILL.md|/update-transaction]]. Its automatic follow-up re-syncs, so those fixes then settle any quota they feed. The writers' follow-up applies them directly.
7. **Writes the page summary** when the page body is empty.

**A discount inside the charge** (UnionPay QR, `InstantDiscountPromotion`): the ledger's amount is already net, so the split reads each slip's discount back from it (฿67.68 = ฿72 less ฿4.32) and writes only the Bureau's `เงินคืน…` fields: no `% cb`, no trackers. Before splitting, the sync reads UnionPay's offer page for the month (`quota` in the envelope: `live` with `left`, `used up`, `not started`, `not listed`). The first sync inside the month that finds it `used up` writes that day to `Quotas Exceeded Date`, and from then on nothing is discounted. Warnings name slips whose amount disagrees with the terms (discounted after the pool ran out, or not discounted although the terms give one), and days where which slip took the day's one discount is a guess.

## Hard rules

- **Never edit transactions to close drift.** Report the gap and the candidate rows; the user fixes data from the statement or the app's list (reconcile, don't correct).
- **Never alter pre-existing tracker rows** that aren't linked to this Bureau row.
- **Open period → provisional numbers.** Re-run after new rows are recorded (e.g. after `/record-statement` brings Takumi's rows in); shares and `Expected Cashback` follow.
- **Boundary day times**: apps show dates only, so ask the user for times on the one day the quota ends on, never more.

## New campaign

Pick the payout shape and subclass it in `scripts/python/lib/bureau/<code>.py`: `LadderPromotion` (`tranches()` + the bank's `examples`), `CreditCapPromotion` (`rate()` + `cap`), or `BasePromotion` for a new shape (`allocate()` + `expected()`). Declare `code` (or `name_pattern`), `cards`, `campaign`, `period_basis`, `qualifies`/`rules`, and the page text, then add it to `PROMOTIONS` in `lib/bureau/__init__.py`. Document it in `docs/promotions/<id>.md`.
