# scripts/repositories/

**A lightweight database of script-side facts.** YAML files, one entry per resource, with a fixed schema per kind. The script layer (`scripts/python/lib/`) reads from here as the source of truth for everything that is **not** transactional data (transactions and bills still live in Notion).

The vault (`docs/`) contains the human-readable narrative. The narrative *references* what's here, but the structured fields live here only — don't duplicate.

## Kinds

| Kind          | Directory / file                      | Keyed by                       |
|---------------|---------------------------------------|--------------------------------|
| Cards         | `cards/`                              | exact Cards DS title (verbatim) |
| Promotions    | `promotions/`                         | promo `id` (kebab-case)        |
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
notes: |                       # optional — anything the schema doesn't capture
  Free-form text.
```

### Required fields

- `name` — exact title; used for joining with Notion's Cards DS.
- `issuer` — referenced by skill prose ("is this a UOB card?").
- `bill_cycle_pattern` — key into `lib.bill_cycle.PATTERNS`. Drives `/add-transaction`'s auto BC/DD inference.

### Sigil values

- `points_default: "×0"` — string, matches the multiplier names. Currently only `×0` is meaningful.
- `petrol_exclusion: true` — applies the petrol exclusion to this card.

## Promotions schema (`promotions/<id>.yaml`)

```yaml
id: uob-one-2026
name: UOB One 2026 cashback promotion
card: UOB One                   # exact card name; must match a card in cards/
effective_start: 2026-01-01     # required, ISO date
effective_end: 2026-12-31       # optional; null/omitted = open-ended
status: active                  # active | superseded | expired
points_default: "×0"            # optional — same shape as the card field; redundant convenience for classification

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
3. **UOB petrol exclusion** (general, card-level) fires on UOB-flagged cards.
4. **Tiers** are tried in order; first match wins.
5. **No match** → no cashback (`% cb` left unset).

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
- `scripts/python/lib/statement_secrets.py` — resolve a card/issuer to its statement-PDF password (consumed by `/audit-bill`'s `extract.py`).
- Existing libs (`lib/bill_cycle.py`, `lib/cards.py` for Notion joins) consume the card repo as the source of truth for pattern keys and policy flags. **Never hard-code a card-by-name list inside a script.** Add the fact to the repository instead.

## How skills write this

- `/add-promotion` — wraps `scripts/python/add-promotion/cli.py`. Validates the schema and writes the file.
- `/update-promotion` — wraps `scripts/python/update-promotion/cli.py`. Patches an existing promotion file (top-level fields or sub-blocks).
- Cards have no dedicated write skill yet; edit YAML directly when adding a new card. Add an `/add-card` skill the day card data starts changing often.
