# scripts/repositories/

**A lightweight database of script-side facts.** YAML files, one entry per resource, with a fixed schema per kind. The script layer (`scripts/python/lib/`) reads from here as the source of truth for everything that is **not** transactional data (transactions and bills still live in Notion).

The vault (`docs/`) contains the human-readable narrative. The narrative *references* what's here, but the structured fields live here only — don't duplicate.

## Kinds

| Kind          | Directory / file                      | Keyed by                       |
|---------------|---------------------------------------|--------------------------------|
| Cards         | `cards/`                              | exact Cards DS title (verbatim) |
| Promotions    | `promotions/`                         | promo `id` (kebab-case)        |
| Installment campaigns | `installment-campaigns/`      | campaign `id` (kebab-case)     |
| Statement passwords | `statement-passwords.yaml` *(gitignored)* | card `issuer`            |

One file per resource for cards/promotions. Filename = `<id>.yaml` for promotions; `<card-slug>.yaml` for cards (lowercase, hyphens for spaces and apostrophes). The slug is just the filename; the canonical key inside each file is the explicit `name` / `id` field.

Statement passwords are the exception — a **single gitignored file** holding real secrets (see its schema below), with `statement-passwords.example.yaml` committed as the template. This mirrors the `.env` / `.env.example` convention.

## Cards schema (`cards/<slug>.yaml`)

```yaml
name: UOB One                  # required — exact Cards DS title (matches the Notion page)
issuer: UOB                    # required — bank or company (matches the ธนาคาร/บริษัท select where present)
bill_cycle_pattern: uob        # required — pattern key in lib.bill_cycle.PATTERNS
points_default: "×0"           # optional — multiplier checkbox default. Omit if the card earns at the standard ×1 rate.
petrol_exclusion: true         # optional, default false — when true, petrol-station merchants earn nothing on this card (the UOB-wide rule).
truemoney_711_points_exclusion: true  # optional, default false — when true, 7-11 and TrueMoney merchants earn no *points* on this card (the Krungsri-family rule). Cashback is NOT affected.
installment_rewards_upfront: true     # optional, default false — when true, `NN/NN` installment terms earn neither points nor cashback on this card. BOTH axes, unlike the flag above.
installment_note: >-                  # optional — replaces the generic explanation this rule writes into `Note`. Use when the card's *reason* differs (First Choice: personal-loan credit line, not upfront crediting).
  Installment term — ...
notes: |                       # optional — anything the schema doesn't capture
  Free-form text.
```

### Required fields

- `name` — exact title; used for joining with Notion's Cards DS. Matched by
  `lib.card_repo.by_name`, which falls back to apostrophe-folded then
  case-insensitive comparison, so Notion's `Krungsri VISA` resolves against
  this repo's `Krungsri Visa`. Prefer the verbatim Cards DS title anyway —
  the folds are a safety net, not a licence. See
  [[../../docs/concepts/known-divergences]] §11.
- `issuer` — referenced by skill prose ("is this a UOB card?").
- `bill_cycle_pattern` — key into `lib.bill_cycle.PATTERNS`. Drives `/add-transaction`'s auto BC/DD inference.

### Sigil values

- `points_default: "×0"` — string, matches the multiplier names. Any multiplier is meaningful, not just `×0`: it is the card's **base earning tier**, used when no promotion is active and as the fallback a promo-boosted card drops back to. `UOB World` sets `×2` because an unboosted row on that card still earns double, so omitting the field (⇒ Notion reads `×1`) would under-report.
- `petrol_exclusion: true` — applies the petrol exclusion to this card.
- `truemoney_711_points_exclusion: true` — applies the Krungsri-family 7-11 / TrueMoney **points** exclusion. Points-only: `lib.promotions.classify` forces `×0` and leaves the promo's `% cb` untouched. Set on First Choice, Krungsri JCB, Krungsri NOW and Krungsri Visa; deliberately absent on the other `issuer: Krungsri` cards, notably on `Lotus's Beyond` (CP ALL exemption) and on `CardX JCB` (SCB X group — shares only the `krungsri` bill-cycle pattern key, not the family). See [[../../docs/concepts/krungsri-truemoney-711-exclusion]].
- `installment_rewards_upfront: true` — installment terms earn nothing on **both** axes. Set on First Choice, Krungsri JCB, Krungsri NOW and Krungsri Visa: Krungsri grants an installment's rewards in full at purchase, so crediting the terms would double-count. A promo with an explicit `installment_rule` outranks it. See [[../../docs/concepts/installment-reward-campaigns]].

### Merchant points exclusions

```yaml
points_excluded_merchants:    # optional — merchant strings that earn no points from a date on
  - prefix: "WWW.MAKRO.PRO "  #   prefix match, after dropping a leading `[บัตรหลัก] `; "*" = every merchant
    mcc: "5199"               #   informational: the excluded MCC the string bills under
    effective_from: 2025-11-11
    note: "..."               #   written into the row's Note
```

Points-only: `lib.promotions.classify` forces `×0` from `effective_from` onwards and leaves `% cb` untouched (reason suffix `+merchant-points-exclusion`). Issuers exclude by MCC, which a merchant string doesn't carry, so list the strings known to bill under an excluded code. Used on `AEON World Mastercard` (AEON's MCC exclusions from 2025-11-11) and on `AEON Rabbit` with `prefix: "*"` (no points on anything from 2025-11-11).

### Statement card numbers

```yaml
statement_numbers:            # optional — last 4 digits on the issuer's statement → holder
  "4672": takumi              #   Takumi's number is the primary card
  "2497": baiboon             #   anyone else's is their supplement
```

Read by `/record-statement` to decide whose section each statement line sits in. Keys **must be quoted** — an unquoted `0052` loads as a number (and YAML 1.1 reads a leading zero as octal), so the loader rejects anything that isn't a 4-digit string. Values are holder slugs, or `unmonitored` for a real supplement nobody in the household tracks (its charges count toward Takumi's bill but go in no ledger). A number is unique within an issuer, not across issuers.

## Installment-campaigns schema (`installment-campaigns/<id>.yaml`)

Bank campaigns that change how an installment **plan** earns — as opposed to how a card or a merchant earns. Needed because both known campaigns are *post-purchase conversions*: the merchant string is identical whether or not a plan was converted, so `lib.promotions.classify(card, date, merchant)` provably cannot decide it. Membership is instead read off the plan's earlier terms.

```yaml
id: dee-jang                    # required — kebab-case, matches the filename
name: ดีจังผ่อน 0% (…)           # required — Thai label preserved verbatim
issuer: CardX                   # required — gates the advisory term-count hint
status: active                  # active | superseded | expired
points_default: "×0"            # optional — multiplier forced onto every term
cashback: unaffected            # optional, documentation-only: unaffected | varies-by-promotion
note: ไม่ได้รับคะแนนสะสม …        # required in practice — written verbatim onto each term
detect:
  note_contains: ดีจังผ่อน       # DEFINITIVE — substring searched in earlier terms' `Note`
  typical_total_terms: [4]      # ADVISORY ONLY — raises a `campaign_hint`, never applied
notes: |                        # optional
  Free-form text.
```

**The `note` is load-bearing, not decoration.** It's the only durable record that a plan was converted, and `detect.note_contains` matches against it. Rewording a note breaks inheritance for every future term of every existing plan — so keep it byte-identical to what's already in Notion.

**`typical_total_terms` never auto-applies.** A term count is circumstantial (Dee-Jang issues 4 terms, but so could a merchant), so a match only surfaces `campaign_hint: ["<id>"]` for a human to confirm.

Read by `lib.installment_campaigns`; applied by `lib.installments.populate_for_cycle` (inheritance) and `/add-installment`'s `campaign` spec key (declaration on term 1).

## Promotions schema (`promotions/<id>.yaml`)

```yaml
id: uob-one-2026
name: UOB One 2026 cashback promotion
card: UOB One                   # exact card name; must match a card in cards/
effective_start: 2026-01-01     # required, ISO date
effective_end: 2026-12-31       # optional; null/omitted = open-ended
status: active                  # active | superseded | expired
points_default: "×0"            # optional — same shape as the card field. Overrides the card's base tier while the promo is active, so it carries the POINTS axis of a promotion (see promotions/uob-world-points.yaml, which is points-only and grants no cashback at all).

# Foreign-merchant-billed-in-THB handling. Default = "exclude" (general rule).
# Per-merchant overrides grant cashback at the override rate, optionally
# preserving the points-exclusion. Set default: apply to make tier rules
# apply to foreign-in-THB rows like any other row (rare).
foreign_in_thb_policy:
  default: exclude
  overrides:
    - merchant_substring: AGODA
      rate: 0.015
      keeps_points_exclusion: true

# Tier classification — first match wins. Order matters.
tiers:
  - rate: 0.10
    label: bonus
    patterns: [BTS, MRT, AMZ]
  - rate: 0.05
    label: bonus
    patterns: ["7-11", WATSON, "WWW.GRAB.COM", GRABTAXI]
    exclude_patterns: ["TMN 7-11"]   # carve-outs within this tier
  - rate: 0.01
    label: base
    patterns: ["*"]                  # "*" matches everything

# Installment handling. Rows whose merchant name contains NN/NN.
# Omit the block entirely if installments follow the same tier rules.
installment_rule:
  rate: 0.01
  credited: per_installment          # per_installment | at_purchase

# How the issuer credits cashback per cycle, keyed by tier-rate string.
# Used by /post-cashback-credits to schedule the credit transaction dates.
# Values: bc_date | first_weekday_next_month
crediting_schedule:
  "0.01": bc_date
  "0.05": first_weekday_next_month
  "0.10": first_weekday_next_month
```

### Classification precedence

When `lib.promotions.classify(card, date, merchant, [is_installment])` runs against an active promotion:

1. **Installment rule** wins if the row looks like an installment and the promo declares one.
2. **Foreign-in-THB** is checked next. Default-exclude promos return no cashback unless a per-merchant `override` matches.
3. **UOB petrol exclusion** (general, card-level) fires on UOB-flagged cards. Forces `×0` on **both** axes — it does *not* inherit `points_default` from either the promo or the card, since a petrol row earns nothing by definition. (Fixed 2026-08-20; previously it inherited, which was latent until `UOB World` became the first petrol-excluding card with a non-`×0` default.)
4. **Tiers** are tried in order; first match wins.
5. **No match** → no cashback (`% cb` left unset).

Then two card-level rules are layered **on top of** that result, in this order:

6. **`installment_rewards_upfront`** — installment rows get `×0` and no cashback. Skipped when step 1 fired (an explicit promo `installment_rule` is the more specific fact). Reason tag `<base>+installment-rewards-upfront`.
7. **`truemoney_711_points_exclusion`** — forces `×0`, leaves `% cb` alone. Skipped when points are already `×0`, so it never double-notes on top of step 6. Reason tag `<base>+truemoney-711-points-exclusion`.

Plan-level installment campaigns sit **outside** `classify` entirely — they're applied by `lib.installments.populate_for_cycle` after classification, and override the points side and the `Note` while leaving `% cb` as classified.

## Statement passwords schema (`statement-passwords.yaml` — gitignored)

Most Thai issuers ship AES-encrypted statement PDFs. The decryption passwords
live in this one file, keyed by the card's `issuer` (the same string as the
`issuer:` field in `cards/*.yaml`). **Never commit the real file** — only
`statement-passwords.example.yaml`.

```yaml
issuers:
  # Scalar = one password for every card from this issuer. Krungsri-family
  # bundles the primary + all supplements in one PDF locked with the PRIMARY
  # holder's date of birth, so a single value covers all four Krungsri cards.
  Krungsri: "DDMonYYYY"

  # Mapping form — when an issuer locks each supplement's PDF with that
  # holder's own DOB instead of the primary's:
  CardX:
    default: "DDMonYYYY"        # primary
    holders:
      nuta: "DDMonYYYY"         # keyed by lowercase holder slug
```

Resolution is `card name → card_repo issuer → password`. `/audit-bill`'s
`extract.py` auto-resolves it from `--card "<title>"` (or `--issuer`), so a
known issuer's password is never re-typed.

## How skills read this

- `scripts/python/lib/card_repo.py` — load + lookup cards by name.
- `scripts/python/lib/promotions.py` — load + classify + crediting schedule.
- `scripts/python/lib/installment_campaigns.py` — load campaigns, detect one from a row's `Note`, and compute advisory term-count hints. Consumed by `lib/installments.py` and `/add-installment`.
- `scripts/python/lib/statement_secrets.py` — resolve a card/issuer to its statement-PDF password (consumed by `/audit-bill`'s `extract.py`).
- Existing libs (`lib/bill_cycle.py`, `lib/cards.py` for Notion joins) consume the card repo as the source of truth for pattern keys and policy flags. **Never hard-code a card-by-name list inside a script.** Add the fact to the repository instead.

## How skills write this

- `/add-promotion` — wraps `scripts/python/add-promotion/cli.py`. Validates the schema and writes the file.
- `/update-promotion` — wraps `scripts/python/update-promotion/cli.py`. Patches an existing promotion file (top-level fields or sub-blocks).
- Cards have no dedicated write skill yet; edit YAML directly when adding a new card. Add an `/add-card` skill the day card data starts changing often.
