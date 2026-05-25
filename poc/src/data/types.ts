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
  /** Synthetic 4-digit "card last 4" for the POC, since real PANs aren't tracked. */
  last4: string;
  pointsDefault?: "×0" | "×2" | "×3" | "×4" | "×5" | "÷4";
  petrolExclusion?: boolean;
  /** Per-holder presence: who has a supplement of this card. */
  holders: HolderKey[];
  /** Approximate credit limit, household-wide. ฿ */
  creditLimit?: number;
  /** Brand colour pair: [from, to] used for the card gradient. */
  brandColors: [string, string];
  /** One-liner the user has internalised about this card. */
  blurb?: string;
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
  isInstallment?: boolean;
  /** Optional canonical merchant + category from alias rules (phase-2 spec). */
  alias?: { canonical: string; category: string };
}

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
