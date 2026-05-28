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
  | "AEON"
  | "Lotus"
  | "Shopee";

export type CardId =
  | "uob-one"
  | "uob-world"
  | "uob-premier"
  | "uob-makro"
  | "first-choice"
  | "krungsri-jcb"
  | "krungsri-now"
  | "krungsri-visa"
  | "cardx-jcb"
  | "ktc-unionpay"
  | "ttb-so-smart"
  | "aeon-primo"
  | "aeon-next-gen"
  | "lotuss-beyond"
  | "spaylater";

export interface Card {
  id: CardId;
  name: string;
  issuer: IssuerKey;
  network?: "VISA" | "Mastercard" | "JCB" | "UnionPay" | "American Express";
  premiumTier?: "Signature" | "Platinum" | "Infinite" | "Standard";
  /**
   * Per-holder physical card last-4. Each holder's supplement has a distinct
   * card number even though the product name is shared. Mirrors Notion: each
   * holder has their own Cards DB row for "UOB One" / "First Choice" / etc.
   */
  holderLast4: Partial<Record<HolderKey, string>>;
  pointsDefault?: "×0" | "×2" | "×3" | "×4" | "×5" | "÷4";
  /** Baht spent to earn 1 base point. Mirrors Notion's `บาทต่อ 1 คะแนน`. Undefined = no point-earning. */
  bahtPer1Point?: number;
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
  multiplier?: "×0" | "×2" | "×3" | "×4" | "×5" | "÷4";
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

export interface Bill {
  id: string;
  holder: Exclude<HolderKey, "takumi">; // Takumi has no Bills DB
  cardId: CardId;
  /** วันตัดรอบบิล */
  billCycleDate: string;
  /** ยอดชำระ (baht) — net of cashback credits in the cycle */
  amount: number;
  status: BillStatus;
  /** title prefix when draft */
  isDraft: boolean;
  note?: string;
  paidAt?: string;
  hasStatementPdf?: boolean;
  hasSlip?: boolean;
}
