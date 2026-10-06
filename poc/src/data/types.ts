// Phase-1 mirror of the live data shapes (Notion + scripts/repositories/).
// Mock-only — no API calls. Reflects the structure documented in
// docs/databases/ + scripts/repositories/README.md so the POC stays
// faithful to the real model.

export type HolderKey = "takumi" | "baiboon" | "nuta";

export interface Holder {
  key: HolderKey;
  englishName: string;
  thaiName: string;
  /** Takumi is admin: sees own + Baiboon + Nuta. Supplements see only own. */
  isAdmin: boolean;
  /** Soft, recognisable avatar mark — initials in Thai. */
  initial: string;
  /** Accent color used for chips, badges, and the user's "presence". */
  accent: string;
}

export type IssuerKey =
  | "UOB"
  | "Krungsri"
  | "CardX"
  | "KTC"
  | "ttb"
  | "KBank"
  | "AEON"
  | "Lotus"
  | "Shopee"
  | "Grab";

export type CardId =
  | "uob-one"
  | "uob-world"
  | "uob-premier"
  | "uob-makro"
  | "first-choice"
  | "krungsri-jcb"
  | "krungsri-lady"
  | "krungsri-now"
  | "krungsri-visa"
  | "central-the-1-redz"
  | "cardx-jcb"
  | "ktc-digital-visa"
  | "ktc-jcb"
  | "ktc-mastercard"
  | "ktc-unionpay"
  | "ttb-so-smart"
  | "kbank-jcb"
  | "kbank-line-points"
  | "kbank-plustinum"
  | "kbank-shopee"
  | "aeon-next-gen"
  | "aeon-primo"
  | "aeon-rabbit"
  | "aeon-unionpay"
  | "aeon-world"
  | "lotuss-beyond"
  | "grab-paylater"
  | "spaylater";

/**
 * Network tier. Card names stay short (`KTC Mastercard`, never `KTC World
 * Reward Mastercard`); the tier lives here. Notion files every tier above
 * Platinum under `ความพรีเมียม` = `สูง (Signature)` — this union keeps the
 * product's own word so the UI can say it. KTC upgraded on 2026-10-02:
 * VISA → Signature, Mastercard → World Reward, JCB → Ultimate, UnionPay → Diamond.
 */
export type PremiumTier =
  | "Signature"
  | "Platinum"
  | "Infinite"
  | "Standard"
  | "World Reward"
  | "Ultimate"
  | "Diamond";

/** Multiplier checkboxes on the Transactions DSes. `×6` added 2026-10-05 (Lotus's coins at Lotus's). */
export type Multiplier = "×0" | "×2" | "×3" | "×4" | "×5" | "×6" | "÷4";

export interface Card {
  id: CardId;
  name: string;
  issuer: IssuerKey;
  network?: "VISA" | "Mastercard" | "JCB" | "UnionPay" | "American Express";
  premiumTier?: PremiumTier;
  /**
   * Per-holder physical card last-4. Each holder's supplement has a distinct
   * card number even though the product name is shared. Mirrors Notion: each
   * holder has their own Cards DB row for "UOB One" / "First Choice" / etc.
   */
  holderLast4: Partial<Record<HolderKey, string>>;
  pointsDefault?: Multiplier;
  /** Baht spent to earn 1 base point. Mirrors Notion's `บาทต่อ 1 คะแนน`. Undefined = no point-earning. */
  bahtPer1Point?: number;
  /**
   * Points one `บาทต่อ 1 คะแนน` block earns at ×1 — Notion's `คะแนนต่อ 1 หน่วย`
   * (empty = 1). Only Lotus's Beyond sets it (0.25 coins per whole ฿50), so a
   * row can earn fractions. Applied after the formula's floors.
   */
  pointsPerUnit?: number;
  /** What the issuer calls its points, when not "points" (Lotus's: coins). */
  pointsName?: string;
  petrolExclusion?: boolean;
  /** Per-holder presence: who has a supplement of this card. */
  holders: HolderKey[];
  /**
   * Cumulative lifetime points per holder. Mock-only — in the real app this
   * is a rollup over every processed transaction on that holder's card.
   */
  holderLifetimePoints?: Partial<Record<HolderKey, number>>;
  /**
   * Current outstanding balance per holder across all unpaid + processed-but-
   * unbilled cycles. Different from "this cycle's outstanding" — that's a
   * cycle-window slice. This is the live debt on the card right now.
   */
  holderCurrentBalance?: Partial<Record<HolderKey, number>>;
  /** Credit limit on the underlying credit line. Shared across all holders' supplements of the same card. ฿ */
  creditLimit?: number;
  /** Brand colour pair: [from, to] used for the card gradient. */
  brandColors: [string, string];
  /** One-liner the user has internalised about this card. */
  blurb?: string;
}

/**
 * A specific holder's supplement of a card — what the user actually swipes.
 * Two holders may share the same `cardId` but have distinct `last4`s.
 */
export interface CardInstance {
  cardId: CardId;
  holder: HolderKey;
  last4: string;
}

export interface PromotionTier {
  rate: number;
  label?: "bonus" | "base";
  patterns: string[];
  excludePatterns?: string[];
}

export interface PromotionForeignOverride {
  merchantSubstring: string;
  rate: number;
  keepsPointsExclusion: boolean;
}

export interface Promotion {
  id: string;
  name: string;
  cardId: CardId;
  effectiveStart: string; // ISO date
  effectiveEnd: string | null; // ISO date or null = open-ended
  status: "active" | "superseded" | "expired";
  pointsDefault?: "×0";
  foreignInThbPolicy: {
    default: "exclude" | "apply";
    overrides: PromotionForeignOverride[];
  };
  tiers: PromotionTier[];
  installmentRule?: { rate: number; credited: "per_installment" | "at_purchase" };
  creditingSchedule?: Record<string, "bc_date" | "first_weekday_next_month">;
}

export type TransactionStatus = "pending" | "processed" | "paid" | "refunded";

/**
 * An installment plan term as it lives on a single transaction row.
 *
 * Parallel plans under the same bank-side merchant string are common (the
 * user routinely runs several Shopee installments at once). The disambiguator
 * is `perTermAmount` — two `2C2P *SHOPEE` 10-term plans at ฿449.10 and ฿1,079.20
 * are *distinct* plans and cluster separately. Mirrors `lib/installments.py`
 * in `scripts/python/` so the POC's logic stays faithful to the system of record.
 */
export interface InstallmentTerm {
  /** Merchant string with the trailing `NN/NN` stripped (e.g. `2C2P *SHOPEE`). */
  base: string;
  /** 1-indexed term number. */
  term: number;
  /** Total terms in the plan. */
  total: number;
  /** Canonical per-term baht — cluster identity within (base, total). */
  perTermAmount: number;
  /**
   * Plan-level installment campaign, when the plan is a post-purchase
   * conversion (`scripts/repositories/installment-campaigns/`). Invisible in
   * the merchant string — inherited from the campaign note on an earlier term.
   */
  campaign?: InstallmentCampaignId;
}

/** `u-plan` (Krungsri / First Choice, 0%×3 or with interest ×4–10) · `dee-jang` (CardX, 4 terms). Both: no points. */
export type InstallmentCampaignId = "u-plan" | "dee-jang";

/**
 * A posted charge re-split into installments (U PLAN). Recorded as the
 * statement prints it: the original charge (stays, now ×0, still counts once
 * toward pooled campaigns), a `REV-FC PLAN ON DEMAND: <merchant>` reversal at
 * minus the full amount (an adjustment, never a refund), then the terms.
 */
export interface Conversion {
  campaign: InstallmentCampaignId;
  role: "charge" | "reversal";
  /** Terms the charge was split into. */
  terms: number;
}

export interface Transaction {
  id: string;
  holder: HolderKey;
  cardId: CardId;
  /** Verbatim merchant string — never normalised. */
  name: string;
  /** ยอดชำระ (baht). Negative for refunds / cashback credits. */
  amount: number;
  transactionDate: string; // ISO
  billCycleDate: string; // ISO
  dueDate: string; // ISO
  status: TransactionStatus;
  note?: string;
  cashbackPercent?: number; // raw fraction
  multiplier?: Multiplier;
  /** Set on the charge and the reversal of a U PLAN / ดีจังผ่อน conversion. */
  conversion?: Conversion;
  /**
   * When the merchant string carries a trailing `NN/NN`, this is populated
   * (parsed once at mock-data construction time via `parseInstallmentName`).
   * The `isInstallment(tx)` helper still works for legacy boolean checks.
   */
  installment?: InstallmentTerm;
  /** Optional canonical merchant + category from alias rules (phase-2 spec). */
  alias?: { canonical: string; category: string };
}

/** Back-compat boolean check; mirrors `lib.installments.is_installment` in Python. */
export const isInstallment = (tx: Transaction): boolean => tx.installment !== undefined;

export type BillStatus = "draft" | "issued" | "paid";

/**
 * Who owns which part of a statement-driven bill. Every statement line lives
 * in exactly one ledger, so Σ parts = the printed card total.
 */
export interface StatementBreakdown {
  /** Takumi's own lines on the principal card (plus bank fees / his own credits). */
  takumi: number;
  /** Baiboon's statement lines — her supplement section plus `[บัตรหลัก]` rows. */
  baiboon?: number;
  /** Nuta's statement lines. */
  nuta?: number;
  /** A real supplement nobody tracks (`unmonitored`) — billed, in no ledger. */
  untracked?: number;
}

export interface Bill {
  id: string;
  /**
   * Bills DB owner. Takumi has had one since 2026-09-27 — statement-driven:
   * one row per card per bank statement, at the printed card total.
   */
  holder: HolderKey;
  cardId: CardId;
  /** วันตัดรอบบิล */
  billCycleDate: string;
  /** Due date — the printed one on statement bills. */
  dueDate?: string;
  /** ยอดชำระ (baht) — net of cashback credits in the cycle */
  amount: number;
  status: BillStatus;
  /** title prefix when draft */
  isDraft: boolean;
  note?: string;
  paidAt?: string;
  hasStatementPdf?: boolean;
  hasSlip?: boolean;
  /**
   * `computed` — a friend's bill: Σ their own rows, drafted by /prepare-bill.
   * `statement` — Takumi's: the bank's per-card total (principal + every
   * supplement section). He pays the bank himself; friends owe him their parts.
   */
  source?: "computed" | "statement";
  /** Statement bills only — Takumi's view only. */
  breakdown?: StatementBreakdown;
  /** How Takumi paid the bank: Krungsri-family cards auto-debit, the rest by transfer slip. */
  paidVia?: "auto-debit" | "transfer";
}

// ─── Shared campaigns (the Promotion Bureau) ──────────────────────────────

/**
 * A primary account: Takumi's principal card(s) at one issuer plus every
 * supplement on them. Pooled campaigns and shared quotas live here, not on a
 * single Card — supplements see the account's aggregate, never others' rows.
 */
export interface PrimaryAccount {
  id: string;
  issuer: IssuerKey;
  /** e.g. "UOB account" */
  label: string;
  cardIds: CardId[];
  /** Shared credit line, ฿. */
  creditLimit?: number;
}

/**
 * Payout shapes — one class each in `scripts/python/lib/bureau/`:
 * - `ladder` — steps of pooled spend (LadderPromotion: NW4, LAN …)
 * - `credit-cap` — each row earns its rate until a pooled credit cap (UOB One)
 * - `per-slip` — a fixed credit per qualifying slip until a cap (QRT4)
 * - `points-quota` — a points bonus on the first ฿N of the period (UOB World ×5)
 */
export type CampaignShape = "ladder" | "credit-cap" | "per-slip" | "points-quota";

/** The window the bank counts a limit over. */
export type PeriodBasis = "month" | "cycle" | "campaign";

export interface LadderStep {
  /** Pooled spend that reaches this step (฿). */
  at: number;
  /** Total credit paid at this step (฿) — the highest reached tier pays. */
  credit: number;
}

export interface Campaign {
  /** Stable id — one per Bureau class (UOB One has two: 10%/5% and 1%). */
  id: string;
  /** Bank's registration code — `LAN`, `QRT4`, `NW4`, `UOB One` … */
  code: string;
  /** The campaign page's own title (Thai where the bank's page is Thai). */
  title: string;
  issuer: IssuerKey;
  accountId: string;
  cardIds: CardId[];
  shape: CampaignShape;
  reward: "cashback" | "points";
  /** The figure in the Bureau row's name: `2%`, `10%/5%`, `×5`. */
  headline: string;
  periodBasis: PeriodBasis;
  effectiveStart: string;
  effectiveEnd: string | null;
  /** One sentence: how it pays. */
  rule: string;
  /** Ladder: the paying steps, ascending. */
  steps?: LadderStep[];
  /** credit-cap / per-slip: ฿ of credit per period. points-quota: ฿ of spend per period. */
  cap?: number;
  /** per-slip: credit per qualifying slip, and the minimum slip. */
  perSlip?: { credit: number; minSlip: number };
  /** points-quota: the bonus and fallback multipliers. */
  quota?: { bonus: Multiplier; after: Multiplier };
}

/** One holder's place in a period's first-come-first-served split. */
export interface CampaignShare {
  holder: HolderKey;
  /** Their linked spend in the period (฿). */
  spend: number;
  /** The part of it inside a paying step / the quota (฿). */
  counted: number;
  /** Their credit (฿). Shares sum to the period's credit exactly. 0 on points campaigns. */
  credit: number;
  /** per-slip: their qualifying slips that were paid. */
  slips?: number;
}

/** One Bureau row: `2026M5 — LAN cb 2%`. */
export interface CampaignPeriod {
  id: string;
  campaignId: string;
  /** `<year>M<month> — <code> <cb?> <headline>` */
  name: string;
  start: string;
  end: string;
  /** Household-wide pooled spend (฿). */
  pooledSpend: number;
  /** Spend inside a paying step / quota (฿). */
  counted: number;
  /** Cashback the account earns this period (฿). 0 on points campaigns. */
  credit: number;
  /** per-slip: qualifying slips paid. */
  slips?: number;
  /** Ladder: next step above the pooled spend, if any. */
  nextStep?: LadderStep;
  /** The top of the meter: max credit (cashback) or the quota (points). */
  cap: number;
  shares: CampaignShare[];
}

/**
 * A row in `รายการติดตามเครดิตเงินคืนของ<name>` — one credit a holder expects
 * to get back. Open until the credit reaches them.
 */
export interface CashbackTracker {
  id: string;
  holder: HolderKey;
  periodId: string;
  /** `<code> <headline> <span>` — e.g. `QRT4 10% 1—31 May`. */
  title: string;
  cardId: CardId;
  /** `Expected Cashback` — the holder's share. */
  expected: number;
  settled: boolean;
  /**
   * `bank-credit` — the bank's credit line landed in the holder's own ledger
   * (linked as `Slip Transaction`). `transfer` — Takumi paid it out, slip attached.
   */
  settledBy?: "bank-credit" | "transfer";
  /** The ledger row that *is* the credit (bank-credit settlements). */
  slipTransaction?: { name: string; amount: number; date: string };
  /** The day Takumi transferred it (transfer settlements). */
  transferredAt?: string;
}
