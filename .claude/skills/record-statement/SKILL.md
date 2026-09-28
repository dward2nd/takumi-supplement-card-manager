---
name: record-statement
description: Record one of Takumi's bank statements (UOB, KBank, AEON, KTC, Krungsri-family or Lotus's PDF) across all three ledgers and file his bill. Splits every line by card number — supplement lines are checked against Baiboon's/Nuta's rows, friends' rows that sit on Takumi's primary card get the `[บัตรหลัก]` prefix, Takumi's own charges/bank credits/fees become rows in his Transactions DB — then creates his Bills row at the printed card total and attaches the PDF. Idempotent. Use when the user hands over a statement PDF and says "record my statement", "start from this statement", "file my UOB bill", or uploads a new month's statements.
---

# record-statement

Turns one issuer statement into everything the household ledger needs from it. The model it implements is in [[../../docs/databases/takumi-bills|takumi-bills]]: **every statement line lives in exactly one ledger**, and Takumi's bill is the statement's printed card total — his charges plus the supplements'.

This is a write skill across all three holders' Transactions DBs and Takumi's Bills DB. It overrides the project's "don't mutate Notion without explicit instruction" rule because the user invoked it explicitly — but always **dry-run first** and show the plan (see *Procedure*).

For the friends' own bills use [[../prepare-bill/SKILL.md|/prepare-bill]]; for a read-only diff of one friend's cycle use [[../audit-bill/SKILL.md|/audit-bill]].

## Primary execution path

```sh
echo '{"issuer": "UOB", "pdf": "/Users/.../MONTHLYSTATEMENT_….pdf"}' \
  | uv run --project scripts/python scripts/python/record-statement/cli.py --dry-run
# then the same without --dry-run
# --parse-only prints the parsed statement and touches nothing in Notion
```

Spec:

| Key | Meaning |
|---|---|
| `pdf` + `issuer` | The statement PDF and its issuer — `UOB`, `KBank`, `AEON`, `Krungsri` (First Choice, Krungsri NOW / Visa / JCB / Lady, Central The 1 Redz) `KTC` (KTC UnionPay / Digital VISA / JCB — one PDF per card number, since KTC bills the principal and each supplement separately; a friend with no section on a KTC statement only has their `[บัตรหลัก]` rows looked for) or `Lotus` (Lotus's Beyond — Krungsri's layout and password; the `Lotus` key only picks the parser, and its card numbers are looked up under `Krungsri`, the card's issuer since 2026-09-27). Encrypted PDFs open with the issuer's password from `statement-passwords.yaml`. |
| `statement` | Instead of `pdf` + `issuer`: the statement hand-transcribed into the `lib.statements.model.Statement` shape (`--parse-only` output shows it). Use for an issuer with no parser yet. |
| `attach_pdf` | Default `true` when `pdf` is given. |

The bill cycle date is the **statement date** and Takumi's rows carry the **printed due date**. The skill never infers either from today.

## What it does, per card account

1. **Parse and self-check.** The parser for the issuer reads every account (one per product), its card-number sections and their lines. It then refuses to continue unless previous balance + lines equals the printed total for every account, so a line misread by the parser can't reach Notion.
1a. **Dates.** Rows and the bill are filed under the card's own cycle. A printed statement date within 5 days of a cycle date is a paper shift: UOB printed 27 Sep / 19 Oct 2026 for the cycle that closed 25 Sep. In that case the cycle's BC and due dates are used, and the printed ones go into the bill `Note` and the report (`statement.printed` plus a warning). If the printed date is further off, or the cards' cycles disagree, the run is refused. See [[../../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]].
2. **Map card numbers.** Each section's last four digits resolve to `(card, holder)` via `statement_numbers` in `scripts/repositories/cards/<card>.yaml`. Takumi's number is the primary; anyone else's is their supplement. A number mapped to `unmonitored` is a real supplement no one tracks (Lotus's 6524, P. PETCHKULJINDA): its lines count toward the bill and show in the split, but nothing is matched or written for them. An account with **no activity and nothing due** (e.g. a paid-off UOB Simple) is skipped. An **unmapped number** blocks its account, and the reason names whose rows the lines match ("3818 matches nuta 92/92"). Add the number to the YAML, then re-run.
3. **Supplement sections** are checked against that holder's rows in the cycle (date + amount, exact then ±3 days). A line the holder hasn't recorded is reported under `missing`, **never written for them**.
4. **Primary section lines** (everything but payments):
   - already in Takumi's DB → counted as `recorded`;
   - recorded by a friend → theirs; the row is renamed `[บัตรหลัก] <name>` if it lacks the prefix;
   - a friend's `[บัตรหลัก]` row for *part* of the line (a half split recorded **without** the prefix isn't recognised as a share; it's reported under `not_on_statement` while Takumi gets the full line, so prefix it first and re-run the dry run) (same merchant stem, smaller amount) → their share; Takumi gets the remainder with a `Note` naming the shares. Credits split the same way without the prefix — First Choice's `เครดิตเงินคืน …` is shared out under the bank's own name;
   - a bank credit a friend already booked under the bank's own text (`CB15_ SUP1 CAMPAIGN …`, AEON's `CASH BACK - CREDIT CARD PROMOTION`) → theirs, matched as-is and not renamed: same leading two words, same amount, date within 3 days. Their row may sit in this cycle or the next one, where a credit that landed after their bill was paid gets booked. A friend's cashback rows are otherwise left out, since they're the household's own computed credits. ฿0 rows (points only) never stand for a line;
   - otherwise → a new Takumi row, name verbatim from the statement. A foreign charge's original amount goes into the `Note` (`Original amount 107.00 USD.`), not the name. The statement prints no country suffix for some foreign merchants (`AGODA.COM … Internet`), so check whether a friend's matching share is `×0` and mirror it. Charges take their points multiplier and `% cb` from `lib.promotions.classify` (a 0% rate stays unset); credits, fees and rebates get `×0` and no cashback.
4a. **Posting dates.** When the issuer prints a POST date (UOB), every row a line accounts for gets it as `Process Date` (`process_dates` in the report): matched rows and shares by an update, new rows at creation. Re-running an already-recorded statement is how older rows get stamped; the Aug and Sep 2026 UOB statements were re-run on 2026-09-28. The Bureau follow-up then moves rows whose posting date puts them in another UOB One period.
4b. **Split-line points.** A primary line split between a friend's `[บัตรหลัก]` share and your remainder loses points when each row rounds down on its own. TMN 7-11 ฿51 at `×5` earns 10 at the bank; the ฿27.50 and ฿23.50 rows give 5. The difference goes on a `[ปรับคะแนน] <line>` row in your ledger (user, 2026-09-28: the principal holder carries it): ฿0, `×0`, with `ใช้คะแนน` set to minus the lost points. It's reported as `points_adjustments` and not written twice.
5. **Payments** (`PAYMENT THANK YOU…`, `PAYMENT RECEIVED…`) are never recorded — they settle the previous bill. They're listed under `payments_skipped`.
6. **Bill.** Creates `<Card> YYYY-MM` in Takumi's Bills DB at the printed total. There's no `[DRAFT]`, since the statement is in hand. `Note` gives the split per holder, any balance carried from the previous statement, and any Notion drift. The PDF is attached unless a file of that name is already on the bill. An existing bill is left unchanged; if its amount differs from the statement, that's reported.

7. **Promotion Bureau** (`sync_promotions`, default `true`; user, 2026-09-28). Once every account is written, the Bureau rows that the new Takumi rows and renamed `[บัตรหลัก]` rows count toward are re-synced (`lib.bureau.follow`). Eligible rows are linked, the split and trackers are redone, and linked rows' `% cb` / multiplier / `ใช้คะแนน` are set to the split. This is when the UOB rows stop being provisional: Takumi's own spend joins the pooled caps and can push a friend's rows past them. The dry run only names the Bureau rows it would sync.

Re-running over a recorded statement plans nothing (verified on the first three statements, 2026-09-27). With nothing written, nothing is followed.

## Reading the report

Per account: `split` (holder → amount the statement attributes to them), `recorded`, `renames`, `creates` (with `multiplier` / `note`), `bill`, `drift` (Notion minus statement over the lines it accounts for), and when present `near_matches`, `shares`, `missing`, `not_on_statement`, `carried`. Top-level `warnings` compare the printed dates with each card's pattern in [[../../docs/concepts/bill-cycle-patterns|bill-cycle-patterns]].

Top-level `promotions` (after a real run) is `{synced, fixed, missing, warnings}`, the same as [[../add-transaction/SKILL.md|/add-transaction]]'s. Report the fields it `fixed` (a friend's row whose rate changed because Takumi's spend came first matters to them), the new shares, `missing` Bureau periods (offer to create them), and warnings. An `error` there means the statement is recorded but the sync failed: re-run [[../sync-promotion/SKILL.md|/sync-promotion]], never the record.

Per [[../../docs/concepts/reconcile-dont-correct|reconcile, don't correct]], `missing` and `not_on_statement` are **reported, never fixed** by this skill. Surface them to the user — a friend's row with no statement line is often a cancelled charge, or one that landed in the next cycle.

## Procedure

1. Run with `--dry-run`. Summarise the plan per card: new Takumi rows (count + total), renames (list them — each changes a friend's merchant name), the bill amount and split, and every `missing` / `not_on_statement` / `near_matches` / `shares` / warning. Near-date matches and shares are judgement calls; point them out.
2. If an account is **blocked**: for an unmapped number, add it to the card's `statement_numbers` (quoted 4-digit key) after confirming the holder with the user; for a card missing from Takumi's Cards DB, create it (Name + Card Network), then re-run the dry run.
3. Run for real once the user is happy, then report counts, the bills written, and the Bureau follow-up (`promotions`).

## Hard rules

- **Names stay verbatim.** New rows take the statement's description exactly. Renames only prepend `[บัตรหลัก] ` — the rest of the friend's name is untouched.
- **Never write a friend's missing line.** Their ledgers are theirs; a gap is a finding.
- **Never record payments or edit amounts.** Takumi's payments stay manual on purpose: whose money a slip is depends on the occasion, and he states it each time. His 2025 ledger paired a full `ชำระบิลเต็มจำนวน - <card>` row with `โอนยอดจาก<friend> - <card>` rows, but that's one possible shape, not a rule.
- **Don't touch older cycles.** The skill only reads and writes the statement's own bill cycle.

## Adding an issuer

Write `scripts/python/lib/statements/<issuer>.py` exposing `parse(text) -> Statement` and register it in `PARSERS` and `_SIGNATURES` in `lib/statements/__init__.py`. Use the existing parsers as templates; Krungsri's statements name each supplement holder on the section line, which is the evidence for a new `statement_numbers` entry. `Statement.check()` will tell you when the parse is complete. Until a parser exists, transcribe the statement into the `statement` spec key.

## What this skill does NOT do

- Does not create cards or register card numbers — step 2 of *Procedure* covers both, with the user's confirmation.
- Does not draft or refresh Baiboon's/Nuta's bills — [[../prepare-bill/SKILL.md|/prepare-bill]] and [[../update-bill/SKILL.md|/update-bill]].
- Does not attach payment slips or mark bills paid — [[../update-bill/SKILL.md|/update-bill]] (`paid: true` on Takumi's bills).
- Does not translate Thai labels.
