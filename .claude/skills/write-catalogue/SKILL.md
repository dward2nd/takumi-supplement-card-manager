---
name: write-catalogue
description: Research and write a Promotion Catalogues page — a Thai reading page for one merchant (or programme) for one month, e.g. `Makro — Oct 2026`, with a spending plan for the household's cards and a catalogue of every payment promotion there (all issuers, not only the household's cards), plus the page's logo cover and icon. Use when the user says "write a summary of the promotions at <merchant>", "รวมโปร <merchant>", "make a catalogue page for Shopee in October", "how should Baiboon spend at GO Wholesale this month?", or adds a blank page to the Promotion Catalogues DB. Also refreshes an existing page (`replace_body`) and reports the month's Promotion Bureau usage for the plan.
---

# write-catalogue

One page in the [[../../../docs/databases/promotion-catalogues|Promotion Catalogues]] DB = one merchant (or programme, like The 1) for one month. It's reading material for the household, in Thai. Nothing in it is linked to transactions; the money side lives in the [[../../../docs/databases/promotion-bureau|Promotion Bureau]].

## Workflow

1. **Research every promotion that pays there that month, whoever issues it** (user, 2026-09-30: "the promotions are not limited to only cards I have"). Bank credit and debit cards, network offers (Visa, Mastercard, UnionPay, JCB), wallets and BNPL, points-for-cashback, installment deals, and the merchant's own campaigns. For each one record: issuer and cards, channel (in store, app, web), mechanic with every tier, caps (per slip, month, campaign; per card or per person), period, registration code, crediting, stacking, the official URL, and a confidence label (verified on the official page / third-party only / unverified).
   - For a broad page, send researchers out in parallel (one for bank cards, one for wallets and the merchant's own deals), each with the known facts from the repo to verify.
   - **Include promotions that name no merchant** (user, 2026-10-01): all-spend cashback cards, monthly spend-threshold campaigns, network-wide offers and welcome offers, from every issuer. Check each one's exclusions against the merchant (supermarket MCC 5411, Makro PRO's 5199, marketplaces, e-wallets, "except China"). They can beat the merchant's own deals: the Bangkok Bank UnionPay card pays 2% on ≥ ฿2,000 a month, anywhere except China, which outranks most Makro campaigns without mentioning Makro. Give them their own researcher.
   - Many bank pages render only in a browser. What worked in Sep 2026: `curl -A Mozilla/5.0` for raw HTML and embedded JSON; `https://www.centralthe1card.com/gcspromotion` (POST) returns all Central The 1 promotions with their T&Cs; CardX's search index; UnionPay's offer API (`lib.bureau.unionpay_offer`); the posters' images for tier tables.
   - Added in Oct 2026:
     - **CardX**: its pages return 403, but the search index they query (`kong-prod-frontend.cardx.co.th/indexes/promotion/search`, with the page's public key) has the full text.
     - **UOB**: `…/credit-cards/promotions/data-promotion.json` lists every campaign with dates, and each `.page` has a `.json` twin.
     - **KBank and GO Wholesale** block curl, so use headless Chrome. GO is WordPress: `wp-json/wp/v2/promotions`.
     - **Shopee**: its own `m/` pages are captcha-walled. Take bank codes from the banks' pages, campaign dates (10.10) from Shopee's App Store / Google Play listing, and standing rules from the Help Center API.
   - **The 1 covers both halves** (user, 2026-10-01): the membership (points, member-only deals, network coupons in the The 1 app) and the Central The 1 card. Say which deals need the card and which just the membership.
   - Repo facts first: `docs/promotions/*.md` and the `lib/bureau/` campaign classes already hold verified terms for the campaigns the household tracks.
   - **Start from the archive** ([[../../../docs/catalogues/index|docs/catalogues/]]). In [[../../../docs/catalogues/campaigns|campaigns.md]], each ended campaign needs its successor found and each continuing one its end date checked. [[../../../docs/catalogues/research-methods|research-methods.md]] says how to read each site. Give the researchers last month's reports to verify against.
   - **Document the research, don't just use it** (user, 2026-10-01: "Make documents somewhere in case we can just easily find it next time").
     - Save each researcher's report to `docs/catalogues/<YYYY-MM>/<topic>.md`, with the snapshot header the October reports carry.
     - Add new campaigns and predecessor → successor chains to `campaigns.md`.
     - Record new site tricks in `research-methods.md`, and list the month in `docs/catalogues/index.md`.
     - No one's points balance goes into these files.
2. **Get the household's position** for the plan: which cards each holder has (`scripts/repositories/cards/`, the Cards DBs), what's registered (memory `project_campaign_registrations`), and this month's Bureau usage:

   ```sh
   echo '{"status":"2026-10"}' | uv run --project scripts/python scripts/python/write-catalogue/cli.py
   ```

   Each Bureau row overlapping the month comes back with `pooled_spend`, `credit`, `cap` and `left`.
3. **Write the body as Markdown** in the page format below, to a file in the scratchpad.
4. **Pick the cover and icon.** The logo is a Wikimedia Commons file (`commons:Makro logo.svg`), an image URL, or a local file; the brand's own site often has one when Commons doesn't (the T1 mark: `https://www.centralthe1card.com/getmedia/92566f51-45ec-4d34-9ef1-38430794d1b2/T1_Sq_1080.jpg`). An icon-only logo takes `logo_text` for a wordmark (TikTok Shop). Presets: `makro`, `go-wholesale`, `shopee`, `lazada`, `tiktok-shop`, `central-the-1` (black, like the T1 mark); a new merchant gets a theme dict (brand colour, darker stripe, floor band, the issuers' card colours). **Keep the gallery's tones varied** (user, 2026-10-01): most retail brands are red or orange, so a brand whose mark is black gets a black cover, and the top card of the fan must stand out from the background.
5. **Dry-run, look at the cover, then write.** Read the rendered `cover_file`: the logo must be fully visible on its white plate.

```sh
uv run --project scripts/python scripts/python/write-catalogue/cli.py --input spec.json --dry-run
uv run --project scripts/python scripts/python/write-catalogue/cli.py --input spec.json
```

| Field | Meaning |
|---|---|
| `page` | exact Name, `<Merchant> — <Mon YYYY>` (`Makro — Oct 2026`) |
| `start`, `end` | the month; needed to create, corrected when they differ |
| `icon` | an emoji (Makro 🛒, GO Wholesale 🧺, Shopee 🛍️, Lazada 💗, TikTok Shop 🎵, The 1 💳) |
| `cover` | `{logo, logo_text?, period?, subtitle, theme}`; `period` defaults to the Thai month of `start` (`ตุลาคม 2569`) |
| `replace_cover` | upload a new cover over an existing one (default: only when the page has none) |
| `cover_out` | where to save the rendered JPEG (default: a temp dir) |
| `body_file` | the Markdown body |
| `replace_body` | rewrite a page that already has content (default: write only an empty page) |

## Page format

Set by the user's Makro example (2026-09-30). Thai narrative; card, campaign and code names verbatim.

1. **Callouts**: `!> 🛒 รวมโปร … ให้น้องใบบุญเอาไปใช้ · <period> · อัปเดต <date>`, what ends today, and channel caveats (`!> ⚠️ …`).
2. **`# แนะนำ แผนการทำยอด …`** (the spending plan): a numbered list of the household's cards, **strictly most value first** (user, 2026-10-01), each with the slip size to aim for, the combined rate (`cb 5% + 2%`), and the month's usage as an italic note (`_ก.ย.: เหลือ 100_`).
   - Rank by the effective rate at the recommended spend: cashback, discounts and vouchers usable there.
   - Lead each line with the card and its rate: `**Krungsri NOW** ทาง Makro PRO — **7%**: …`.
   - Add an italic note under the heading saying how the list is ordered.
   - Coupons for other merchants (Starbucks) are shown on a line but don't move it up.
   - Points redemptions go in a separate "ถ้ามีคะแนนเหลือ" list after the ranking, ordered by baht per point.
   - Shopee ranks codes by discount ÷ minimum order, with the stacking accumulations listed after the codes.
   - Add a worked example for a typical monthly amount, and the registration codes needed.
3. **`# รวมโปร … — <month>`** (the catalogue): `## N. <Issuer>` per issuer, with a tier table (`| ยอดต่อสลิป | เงินคืน |`, the rate as `(<= 1.5%)`), caps, period, registration, and a `ref:` link. `*====== ซ้อนโปร ======*` introduces a promotion that stacks on the one above.
4. Then: cards the household doesn't hold, the merchant's own deals, what's coming next month, and what couldn't be found.

Markdown the converter knows (`lib.catalogue.markdown`): `#`/`##`/`###`, `- ` and `1. ` lists (two-space indent nests one level), `> ` quote, `!> <emoji> ` callout, `---`, `|` tables, `**bold**`, `*italic*`/`_italic_`, `__underline__`, `` `code` ``, `[text](url)` and bare URLs.

## Hard rules

- **No figure without a source.** Say "third-party only" or "unverified" in the page when it is. Never fill a gap with a guess.
- **No reward-points balances, for anyone** (user, 2026-10-01: private). Give the redemption rate and say "ถ้ามีคะแนนเหลือ". Reading balances to decide what to mention is fine; printing them isn't.
- **Channels matter.** A promotion that counts only in-app QR, only Makro PRO or only in store says so in the plan, not just in the catalogue (Sep 2026: most banks count a Makro store purchase only through their app's QR).
- **Every page has an icon and a cover carrying the merchant's logo**, legible on its plate (user, 2026-09-30).
- **Say where a quota is shared with another page.** Krungsri SUP1, CardX HY1, NW4's supermarket allowance and AEON's cycle caps pay once across Makro, GO Wholesale and Tops, so a plan that spends them on one page warns on the others.
- **Don't write to the Bureau, the ledgers or the trackers** from this skill. Usage is read-only (`status`).
- Rewrite an existing page (`replace_body`, `replace_cover`) only when the user asks or to correct it.
