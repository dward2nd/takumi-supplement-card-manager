# `poc/` — Phase-2 product-shape POC

Mobile-first, installable PWA for the [Takumi supplement-card manager](../CLAUDE.md). All code self-contained inside this directory. **Mock data only** — no backend, no Notion calls. The point is to prove the daily-use experience laid out in [`docs/future-app/product-shape.md`](../docs/future-app/product-shape.md).

## Run

```bash
cd poc
bun install
bun run dev          # http://localhost:5173 — opens on your LAN too (host: true)
```

Build + preview:

```bash
bun run build
bun run preview --host
```

Open the preview URL on a phone (same Wi-Fi) and use the browser's "Add to Home Screen" — the manifest + service worker are wired through `vite-plugin-pwa`. Installing gives you the standalone, status-bar-respecting experience.

## Stack

| Concern    | Choice                  | Why                                          |
|------------|-------------------------|----------------------------------------------|
| Runtime + pkg mgr | Bun 1.3+        | Matches the repo's TypeScript-scripts convention. |
| Build      | Vite 5                  | Fast HMR, first-class TS, mature PWA plugin. |
| Framework  | React 18                | Conventional, ergonomic for 3-user scale.    |
| Routing    | React Router 6          | Tiny.                                        |
| Styling    | Tailwind v3             | Design-token-driven, no CSS-in-JS overhead.  |
| Motion     | Framer Motion           | Page transitions + tab-bar pill morph.       |
| Icons      | lucide-react            | Hand-tuned outline icons, no glyph licensing. |
| PWA        | vite-plugin-pwa + Workbox | Service worker, manifest, offline cache.   |
| State      | React `useState` + `localStorage` | Three users, no need for a store.    |

## What's mocked, what's not

**Mocked** (lives under `src/data/`):
- The three holders (Takumi / Baiboon / Nuta), with role + accent colour.
- All 15 cards from `scripts/repositories/cards/`, with brand colours + synthetic `last4` for the card-face renderer.
- The UOB One 2026 promo (from the real YAML) + the First Choice May 2026 promo (the one the user described during the session — not yet in the YAML repo).
- A representative slice of cycle 2026-05-25 transactions for each holder, including: tier-matched purchases, foreign-in-THB exclusions, the `[เว็บรับหนี้ไปบริหารต่อ]` debt-takeover pair, installment rows, and the cashback credit rows that `/post-cashback-credits` writes.
- The three `[DRAFT]` bills from `/prepare-bill` + a few historical paid bills.

**Faithful to the real model**:
- The classification preview on the Add Transaction screen runs a TypeScript port of `lib/promotions.classify` (installment override → foreign-in-THB → tier match). Same precedence rules, same outputs.
- Date / cycle / due-date conventions match `lib/bill_cycle.py`.
- Verbatim merchant strings (per project Rule 1).

**Not in the POC**:
- No persistence. Add-transaction saves are mocked (the screen bounces home).
- No real auth — the "login" is a holder-picker, since this is exactly the 3-user scenario.
- No backend. The phase-2 spec calls for a Rust API + Postgres on a VPS; this POC is the client surface that would talk to it.

## If I were building the real backend (proposal)

A short proposal for the real thing, since you asked: **Rust API server** (the repo's pinned phase-2 stack), Postgres for storage, on a small Hetzner / Linode VPS. Auth via email + password with passkeys as a stretch goal. The client speaks JSON over HTTPS, caches recent reads with the service worker for the flaky-connection case mentioned in the spec, and uses SSE (or just polling) for the "new transaction on phone shows on laptop" sync. No frameworks for the API server beyond `axum` + `sqlx` — three users, deliberately minimal.

Per-holder data scoping is enforced server-side via the auth middleware: Takumi can read everything, supplements read their own slice plus the aggregate `PrimaryAccount` view. Promotions and cards stay as YAML committed alongside the code (the `scripts/repositories/` convention), bundled into the binary at build time — no admin UI needed for resources that change once a year.

## Layout

```
poc/
├── index.html
├── package.json
├── tailwind.config.ts
├── vite.config.ts
├── public/
│   └── icon-*.svg
├── src/
│   ├── main.tsx
│   ├── App.tsx
│   ├── index.css                # design tokens + global styles
│   ├── components/
│   │   ├── Layout.tsx
│   │   ├── TabBar.tsx           # bottom tab + FAB
│   │   ├── PageHeader.tsx
│   │   ├── CardFace.tsx         # the credit-card face renderer
│   │   ├── TransactionRow.tsx
│   │   ├── Amount.tsx           # mono, tabular figures, ฿ symbol
│   │   ├── Pill.tsx
│   │   └── SectionLabel.tsx
│   ├── screens/
│   │   ├── LoginScreen.tsx
│   │   ├── HomeScreen.tsx
│   │   ├── CardsScreen.tsx
│   │   ├── CardDetailScreen.tsx
│   │   ├── BillsScreen.tsx
│   │   ├── BillDetailScreen.tsx
│   │   ├── AddTransactionScreen.tsx
│   │   └── SettingsScreen.tsx
│   └── data/
│       ├── types.ts
│       ├── holders.ts
│       ├── cards.ts
│       ├── promotions.ts
│       ├── transactions.ts
│       ├── bills.ts
│       ├── state.ts             # tiny app store
│       └── format.ts            # baht / date / merchant-split helpers
```

## Design notes

Aesthetic direction: an **editorial journal**, not a banking app dashboard. Two pillars:

1. **Typography-first**. Fraunces (variable serif, with italic) for the display layer, IBM Plex Sans Thai Looped for body, IBM Plex Mono for numerals. The hero cycle-balance and big merchant titles are intentionally large — this is a journal you flip through, not a chart.
2. **Restrained colour**. Warm dark default (`#0d0b08` near-black with subtle radial-gradient atmosphere). One amber accent for primary actions, teal for done/paid, coral for due/danger. Everything else is neutral ink-on-paper.

Mobile UX:
- Container clamps to `max-w-md` (~448px) and centers on desktop — the design is portrait-phone first; desktop is a courtesy.
- Bottom tab bar with a floating amber **+** FAB. Hidden during the add-transaction flow.
- Safe-area-inset everywhere. iOS notch + home indicator handled.
- 44px minimum touch targets enforced via `.tap`.
- Page transitions are short (0.35s) and motion-curved (`cubic-bezier(0.2, 0.7, 0.1, 1)`).

## Phase-2 hand-off

When the real client gets built, this POC is a reference for: typographic hierarchy, the data-model shape (the TS types in `src/data/types.ts` translate ~1:1 to Rust structs / Postgres schemas), the classification UX (live preview on entry), and the FAB+tab navigation rhythm.
