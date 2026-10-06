// Shared campaigns — the POC mirror of the Promotion Bureau
// (docs/concepts/promotion-bureau.md, scripts/python/lib/bureau/).
//
// A bank campaign pays on the PRIMARY ACCOUNT's pooled spend — Takumi's
// principal plus every supplement — so no single holder's ledger can say what
// the bank will pay or who earned it. One record per quota period, named
// `<year>M<month> — <code> cb <headline>`.
//
// The payout comes in a few shapes (one class each in lib/bureau); this file
// mocks one campaign of each and splits the credit the way the Bureau does:
// first come, first served by transaction datetime, same-time rows straddling
// a step shared pro rata, every share rounded to the satang with the leftover
// satang going to the largest remainders — so shares sum to the credit exactly.
//
// Calendar note: the POC's reference date is 26 May 2026. UOB One and UOB
// World ×5 genuinely run then. NW4 (real: 1 Oct–31 Dec 2026), LAN (1 Oct–
// 31 Dec 2026) and QRT4 (1 Jul–31 Dec 2026) are shown six months early so
// one campaign of every shape sits in the demo's window — their payout rules
// are the real ones, their dates are illustrative.
//
// Pure data + pure functions; no React.

import { CARDS, cardsForHolder } from "./cards";
import { TRANSACTIONS } from "./transactions";
import type {
  Campaign,
  CampaignPeriod,
  CampaignShare,
  CardId,
  CashbackTracker,
  HolderKey,
  LadderStep,
  PrimaryAccount,
  Transaction,
} from "./types";

export const POC_TODAY = "2026-05-26";

/** Quota-threshold alert — the spec's configurable default. */
export const QUOTA_ALERT_THRESHOLD = 0.8;

const HOLDER_ORDER: HolderKey[] = ["takumi", "baiboon", "nuta"];

// ─── Primary accounts ─────────────────────────────────────────────────────

export const PRIMARY_ACCOUNTS: PrimaryAccount[] = [
  {
    id: "uob",
    issuer: "UOB",
    label: "UOB account",
    cardIds: ["uob-one", "uob-world", "uob-premier", "uob-makro"],
    creditLimit: 250_000,
  },
  {
    id: "first-choice",
    issuer: "Krungsri",
    label: "First Choice account",
    cardIds: ["first-choice"],
    creditLimit: 80_000,
  },
  {
    id: "lotuss",
    issuer: "Lotus",
    label: "Lotus's Beyond account",
    cardIds: ["lotuss-beyond"],
  },
];

export const accountById = (id: string) => PRIMARY_ACCOUNTS.find((a) => a.id === id)!;

/**
 * Aggregate balance across every card and every holder on the account — what
 * a supplement holder may see of the shared line ("UOB account: ฿X / ฿Y used
 * across all cards"), without any per-holder breakdown.
 */
export const accountUsage = (acc: PrimaryAccount): { used: number; limit?: number } => {
  let used = 0;
  for (const id of acc.cardIds) {
    const bal = CARDS[id].holderCurrentBalance ?? {};
    for (const v of Object.values(bal)) used += v ?? 0;
  }
  return { used: round2(used), limit: acc.creditLimit };
};

// ─── Campaigns ────────────────────────────────────────────────────────────

const ladderSteps = (
  first: { at: number; credit: number } | null,
  step: number,
  pay: number,
  count: number,
): LadderStep[] => {
  const out: LadderStep[] = first ? [first] : [];
  for (let i = 1; i <= count; i++) out.push({ at: step * i, credit: pay * i });
  return out;
};

export const CAMPAIGNS: Campaign[] = [
  {
    id: "uob-one-bonus",
    code: "UOB One",
    title: "UOB One cashback",
    issuer: "UOB",
    accountId: "uob",
    cardIds: ["uob-one"],
    shape: "credit-cap",
    reward: "cashback",
    headline: "10%/5%",
    periodBasis: "month",
    effectiveStart: "2026-01-01",
    effectiveEnd: "2026-12-31",
    rule:
      "BTS, MRT and Café Amazon earn 10%; 7-Eleven, Grab and Watsons 5% — ฿500 of credit a calendar month, shared by everyone on the account. Past it, those rows earn 1%.",
    cap: 500,
  },
  {
    id: "uob-one-base",
    code: "UOB One",
    title: "UOB One cashback",
    issuer: "UOB",
    accountId: "uob",
    cardIds: ["uob-one"],
    shape: "credit-cap",
    reward: "cashback",
    headline: "1%",
    periodBasis: "cycle",
    effectiveStart: "2026-01-01",
    effectiveEnd: "2026-12-31",
    rule:
      "Everything else earns 1%, up to ฿2,000 of credit a statement cycle, shared by the account. Installment terms post on the statement date, so they count next cycle.",
    cap: 2_000,
  },
  {
    id: "uob-world-x5",
    code: "UOB World",
    title: "UOB World ×5 UOB Rewards points",
    issuer: "UOB",
    accountId: "uob",
    cardIds: ["uob-world"],
    shape: "points-quota",
    reward: "points",
    headline: "×5",
    periodBasis: "cycle",
    effectiveStart: "2025-01-01",
    effectiveEnd: null,
    rule:
      "×5 on online, e-wallet, dining, travel and foreign spend inside the first ฿20,000 of the cycle. Every row on the account fills the quota; past it, ×2.",
    cap: 20_000,
    quota: { bonus: "×5", after: "×2" },
  },
  {
    id: "nw4",
    code: "NW4",
    title: "รูดก็ได้เงินคืน กดก็ได้แคชเบ็ค",
    issuer: "Krungsri",
    accountId: "first-choice",
    cardIds: ["first-choice"],
    shape: "ladder",
    reward: "cashback",
    headline: "2%",
    periodBasis: "month",
    effectiveStart: "2026-04-01", // illustrative — real: 2026-10-01
    effectiveEnd: "2026-06-30", //   illustrative — real: 2026-12-31
    rule:
      "฿50 at ฿5,000, then ฿200 per whole ฿10,000 of pooled full-amount spend in the month, up to ฿2,000. Merchant installments never count; a U PLAN charge counts once.",
    steps: ladderSteps({ at: 5_000, credit: 50 }, 10_000, 200, 10),
  },
  {
    id: "lan",
    code: "LAN",
    title: "ช้อปโลตัส รับคืนซูเปอร์คุ้ม",
    issuer: "Lotus",
    accountId: "lotuss",
    cardIds: ["lotuss-beyond"],
    shape: "ladder",
    reward: "cashback",
    headline: "2%",
    periodBasis: "month",
    effectiveStart: "2026-04-01", // illustrative — real: 2026-10-01
    effectiveEnd: "2026-06-30", //   illustrative — real: 2026-12-31
    rule:
      "Only the highest tier pays: ฿40 per whole ฿2,000 up to ฿200, or ฿300 per whole ฿20,000 up to ฿600. Lotus's stores and Shop Online, by card or QR — no e-wallet.",
    steps: [
      ...ladderSteps(null, 2_000, 40, 5),
      { at: 20_000, credit: 300 },
      { at: 40_000, credit: 600 },
    ],
  },
  {
    id: "qrt4",
    code: "QRT4",
    title: "จ่ายแบบไหน ก็ได้คืน",
    issuer: "Lotus",
    accountId: "lotuss",
    cardIds: ["lotuss-beyond"],
    shape: "per-slip",
    reward: "cashback",
    headline: "10%",
    periodBasis: "month",
    effectiveStart: "2026-01-01", // illustrative — real: 2026-07-01
    effectiveEnd: "2026-06-30", //   illustrative — real: 2026-12-31
    rule:
      "฿10 on each slip of ฿100 or more at restaurants, fashion, department stores, health and home stores, paid by QR or TrueMoney — up to ฿40 a month.",
    cap: 40,
    perSlip: { credit: 10, minSlip: 100 },
  },
];

export const campaignById = (id: string) => CAMPAIGNS.find((c) => c.id === id)!;

// ─── What each campaign counts ───────────────────────────────────────────

const inWindow = (iso: string, start: string, end: string) => iso >= start && iso <= end;
const isCreditLike = (t: Transaction) =>
  t.amount <= 0 || /cashback|^CB /i.test(t.name) || t.name.trim().startsWith("[");
const looksForeign = (t: Transaction) => /\s(SG|US|USA|HK|JP|CN|GB|IE|NL)$/.test(t.name.trim());

// QRT4 links every ฿100 slip on the card unless the merchant name shows it's
// outside the five categories (lib/bureau/lotus_qr.py `_outside`, abridged).
const QRT4_OUTSIDE =
  /LOTUS|MAKRO|7-11|BIG ?C|TOPS|SHOPEE|LAZADA|AIS|TRUE|DTAC|BANGCHAK|PTT|TMN|PROMPTPAY|GRAB/i;

interface PeriodDef {
  id: string;
  campaignId: string;
  start: string;
  end: string;
  /** Bill cycle date, for statement-cycle periods. */
  billCycleDate?: string;
  /** Which ledger rows the campaign links, and each row's rate (credit-cap only). */
  rows: (t: Transaction) => boolean;
  rate?: (t: Transaction) => number;
}

const onCards = (t: Transaction, ids: CardId[]) => ids.includes(t.cardId);

const PERIOD_DEFS: PeriodDef[] = [
  {
    // 10%/5% counts per calendar month (by posting date at UOB; by
    // transaction date here — the POC doesn't model posting).
    id: "2026M5-uob-one-bonus",
    campaignId: "uob-one-bonus",
    start: "2026-05-01",
    end: "2026-05-31",
    rows: (t) =>
      onCards(t, ["uob-one"]) &&
      !isCreditLike(t) &&
      (t.cashbackPercent === 0.1 || t.cashbackPercent === 0.05) &&
      inWindow(t.transactionDate, "2026-05-01", "2026-05-31"),
    rate: (t) => t.cashbackPercent ?? 0,
  },
  {
    // 1% counts per statement cycle: 25 Apr – 24 May, billed 25 May.
    id: "2026M5-uob-one-base",
    campaignId: "uob-one-base",
    start: "2026-04-25",
    end: "2026-05-24",
    billCycleDate: "2026-05-25",
    rows: (t) =>
      onCards(t, ["uob-one"]) &&
      !isCreditLike(t) &&
      t.cashbackPercent === 0.01 &&
      !t.installment && // terms post on the statement date → next cycle
      t.billCycleDate === "2026-05-25",
    rate: () => 0.01,
  },
  {
    // Every row on the account fills the ×5 quota, bonus category or not.
    id: "2026M5-uob-world-x5",
    campaignId: "uob-world-x5",
    start: "2026-04-25",
    end: "2026-05-24",
    billCycleDate: "2026-05-25",
    rows: (t) => onCards(t, ["uob-world"]) && t.amount > 0 && t.billCycleDate === "2026-05-25",
  },
  {
    id: "2026M5-nw4",
    campaignId: "nw4",
    start: "2026-05-01",
    end: "2026-05-31",
    rows: (t) =>
      onCards(t, ["first-choice"]) &&
      !isCreditLike(t) &&
      !t.installment && // terms are never new spend
      !looksForeign(t) &&
      !/^Excluded/i.test(t.note ?? "") &&
      inWindow(t.transactionDate, "2026-05-01", "2026-05-31"),
  },
  {
    id: "2026M5-lan",
    campaignId: "lan",
    start: "2026-05-01",
    end: "2026-05-31",
    rows: (t) =>
      onCards(t, ["lotuss-beyond"]) &&
      t.amount > 0 &&
      /^LOTUS['’]?S\b/.test(t.name) &&
      inWindow(t.transactionDate, "2026-05-01", "2026-05-31"),
  },
  {
    id: "2026M5-qrt4",
    campaignId: "qrt4",
    start: "2026-05-01",
    end: "2026-05-31",
    rows: (t) =>
      onCards(t, ["lotuss-beyond"]) &&
      !isCreditLike(t) &&
      t.amount >= 100 && // a slip under ฿100 earns nothing, so it isn't linked
      !t.installment &&
      !QRT4_OUTSIDE.test(t.name) &&
      inWindow(t.transactionDate, "2026-05-01", "2026-05-31"),
  },
];

// ─── The split: first come, first served ──────────────────────────────────

interface Credited {
  tx: Transaction;
  counted: number;
  credit: number;
}

const round2 = (n: number) => Math.round(n * 100) / 100;

/**
 * Walk rows in transaction-datetime order. Rows with the same datetime are
 * simultaneous (a shared bill, or date-only rows whose order the ledger can't
 * tell), so `take` gets one same-time group at a time with the pooled spend
 * before and after it — mirrors `BasePromotion._walk`.
 */
const walk = (
  txs: Transaction[],
  take: (lo: number, hi: number, grp: Transaction[]) => Credited[],
): Credited[] => {
  const spend = txs.filter((t) => t.amount > 0).sort((a, b) => a.transactionDate.localeCompare(b.transactionDate));
  const out: Credited[] = [];
  let cum = 0;
  let i = 0;
  while (i < spend.length) {
    const when = spend[i].transactionDate;
    const grp: Transaction[] = [];
    while (i < spend.length && spend[i].transactionDate === when) grp.push(spend[i++]);
    const size = grp.reduce((s, t) => s + t.amount, 0);
    out.push(...take(cum, cum + size, grp));
    cum += size;
  }
  return out;
};

/** The highest step the pooled spend reaches — a ladder pays that tier only. */
const reachedStep = (steps: LadderStep[], pooled: number): LadderStep | null => {
  let best: LadderStep | null = null;
  for (const s of steps) if (pooled >= s.at) best = s;
  return best;
};

const splitRows = (c: Campaign, def: PeriodDef, rows: Transaction[]): { credited: Credited[]; credit: number } => {
  if (c.shape === "ladder") {
    const pooled = rows.reduce((s, t) => s + Math.max(0, t.amount), 0);
    const step = reachedStep(c.steps ?? [], pooled);
    // One tranche, [0, step.at), paying step.credit spread over its baht.
    const credited = walk(rows, (lo, hi, grp) => {
      const size = hi - lo;
      const end = step?.at ?? 0;
      const overlap = Math.max(0, Math.min(hi, end) - Math.max(lo, 0));
      const earned = step ? (overlap * step.credit) / step.at : 0;
      return grp.map((t) => ({ tx: t, counted: (overlap * t.amount) / size, credit: (earned * t.amount) / size }));
    });
    return { credited, credit: step?.credit ?? 0 };
  }

  if (c.shape === "points-quota") {
    let left = c.cap ?? 0;
    const credited = walk(rows, (_lo, hi, grp) => {
      const size = grp.reduce((s, t) => s + t.amount, 0);
      const granted = Math.min(left, size);
      left -= granted;
      void hi;
      return grp.map((t) => ({ tx: t, counted: (granted * t.amount) / size, credit: 0 }));
    });
    return { credited, credit: 0 };
  }

  // credit-cap and per-slip: every row wants its own credit (UOB rounds per
  // line; a slip wants its fixed ฿), granted first come, first served until
  // the period's pooled cap; a same-time group crossing it shares pro rata.
  let left = c.cap ?? 0;
  const want = (t: Transaction): number =>
    c.shape === "per-slip"
      ? t.amount >= (c.perSlip?.minSlip ?? Infinity)
        ? c.perSlip!.credit
        : 0
      : round2((def.rate?.(t) ?? 0) * t.amount);
  const credited = walk(rows, (_lo, _hi, grp) => {
    const wants = grp.map(want);
    const total = wants.reduce((s, w) => s + w, 0);
    const granted = Math.min(left, total);
    left -= granted;
    const share = total > 0 ? granted / total : 0;
    return grp.map((t, k) => ({
      tx: t,
      counted: wants[k] > 0 ? t.amount * share : 0,
      credit: wants[k] * share,
    }));
  });
  return { credited, credit: round2(credited.reduce((s, r) => s + r.credit, 0)) };
};

/** Round each holder's raw credit to the satang; leftover satang go to the largest remainders. */
const roundToTotal = (raw: Map<HolderKey, number>, total: number): Map<HolderKey, number> => {
  const target = Math.round(total * 100);
  const entries = [...raw.entries()].map(([h, v]) => {
    const satang = v * 100;
    return { h, floor: Math.floor(satang + 1e-9), rem: satang - Math.floor(satang + 1e-9) };
  });
  let left = target - entries.reduce((s, e) => s + e.floor, 0);
  entries.sort((a, b) => b.rem - a.rem);
  for (const e of entries) {
    if (left <= 0) break;
    e.floor += 1;
    left -= 1;
  }
  return new Map(entries.map((e) => [e.h, e.floor / 100]));
};

const periodName = (c: Campaign, start: string, billCycleDate?: string): string => {
  // Calendar month → that month; statement cycle → the month of its BC date.
  const ref = billCycleDate ?? start;
  const [y, m] = ref.split("-").map(Number);
  return `${y}M${m} — ${c.code}${c.reward === "cashback" ? " cb" : ""} ${c.headline}`;
};

const buildPeriod = (def: PeriodDef): CampaignPeriod => {
  const c = campaignById(def.campaignId);
  const rows = TRANSACTIONS.filter(def.rows);
  const { credited, credit } = splitRows(c, def, rows);

  const spend = new Map<HolderKey, number>();
  const counted = new Map<HolderKey, number>();
  const raw = new Map<HolderKey, number>();
  const slips = new Map<HolderKey, number>();
  for (const r of credited) {
    const h = r.tx.holder;
    spend.set(h, (spend.get(h) ?? 0) + r.tx.amount);
    counted.set(h, (counted.get(h) ?? 0) + r.counted);
    raw.set(h, (raw.get(h) ?? 0) + r.credit);
    if (c.shape === "per-slip" && r.credit > 0) slips.set(h, (slips.get(h) ?? 0) + 1);
  }
  const rounded = c.reward === "cashback" ? roundToTotal(raw, credit) : new Map<HolderKey, number>();

  const shares: CampaignShare[] = HOLDER_ORDER.filter((h) => spend.has(h)).map((h) => ({
    holder: h,
    spend: round2(spend.get(h) ?? 0),
    counted: round2(counted.get(h) ?? 0),
    credit: rounded.get(h) ?? 0,
    ...(c.shape === "per-slip" ? { slips: slips.get(h) ?? 0 } : {}),
  }));

  const pooledSpend = round2(rows.reduce((s, t) => s + Math.max(0, t.amount), 0));
  const steps = c.steps ?? [];
  const top = steps[steps.length - 1];
  const nextStep = c.shape === "ladder" ? steps.find((s) => s.at > pooledSpend) : undefined;

  return {
    id: def.id,
    campaignId: c.id,
    name: periodName(c, def.start, def.billCycleDate),
    start: def.start,
    end: def.end,
    pooledSpend,
    counted: round2(credited.reduce((s, r) => s + r.counted, 0)),
    credit,
    ...(c.shape === "per-slip" ? { slips: [...slips.values()].reduce((s, n) => s + n, 0) } : {}),
    ...(nextStep ? { nextStep } : {}),
    cap: c.shape === "ladder" ? top?.credit ?? 0 : c.cap ?? 0,
    shares,
  };
};

export const CAMPAIGN_PERIODS: CampaignPeriod[] = PERIOD_DEFS.map(buildPeriod);

// ─── Cashback trackers ────────────────────────────────────────────────────

const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
const dayMon = (iso: string) => {
  const [, m, d] = iso.split("-").map(Number);
  return { d, mon: MON[m - 1], m };
};

/** `NW4 2% 1—31 May` — the household's tracker naming (`BasePromotion.tracker_title`). */
export const trackerTitle = (c: Campaign, p: CampaignPeriod): string => {
  const s = dayMon(p.start);
  const e = dayMon(p.end);
  const span = s.m === e.m ? `${s.d}—${e.d} ${e.mon}` : `${s.d} ${s.mon}—${e.d} ${e.mon}`;
  return `${c.code} ${c.headline} ${span}`;
};

/**
 * How each tracker settled, where it has. A credit the bank paid onto the
 * holder's own card is linked as the `Slip Transaction`; a friend's credit
 * that landed on Takumi's principal is paid out by his transfer.
 */
const SETTLEMENTS: Record<string, Partial<CashbackTracker>> = {
  "2026M5-qrt4#takumi": {
    settled: true,
    settledBy: "bank-credit",
    slipTransaction: { name: "CB TMN QR QRT4MAY26", amount: -20, date: "2026-05-06" },
  },
  "2026M5-qrt4#baiboon": {
    settled: true,
    settledBy: "transfer",
    transferredAt: "2026-05-14",
  },
};

export const CASHBACK_TRACKERS: CashbackTracker[] = CAMPAIGN_PERIODS.flatMap((p) => {
  const c = campaignById(p.campaignId);
  if (c.reward !== "cashback") return [];
  return p.shares
    .filter((s) => s.credit > 0)
    .map((s) => {
      const id = `${p.id}#${s.holder}`;
      // The tracker's Card is the holder's own card on the campaign.
      const cardId = c.cardIds.find((cid) => CARDS[cid].holders.includes(s.holder)) ?? c.cardIds[0];
      return {
        id,
        holder: s.holder,
        periodId: p.id,
        title: trackerTitle(c, p),
        cardId,
        expected: s.credit,
        settled: false,
        ...SETTLEMENTS[id],
      };
    });
});

// ─── Visibility + presentation helpers ────────────────────────────────────

/** Periods on any card the viewer holds — supplements see household-wide progress of these. */
export const periodsVisibleTo = (viewer: HolderKey): CampaignPeriod[] => {
  if (viewer === "takumi") return CAMPAIGN_PERIODS;
  const mine = new Set(cardsForHolder(viewer).map((c) => c.id));
  return CAMPAIGN_PERIODS.filter((p) => campaignById(p.campaignId).cardIds.some((id) => mine.has(id)));
};

export const periodsForCard = (cardId: CardId, viewer: HolderKey): CampaignPeriod[] =>
  periodsVisibleTo(viewer).filter((p) => campaignById(p.campaignId).cardIds.includes(cardId));

/**
 * Shares a viewer may see: Takumi (admin) every holder's; a supplement only
 * their own — never another holder's rows or share.
 */
export const sharesVisibleTo = (p: CampaignPeriod, viewer: HolderKey): CampaignShare[] =>
  viewer === "takumi" ? p.shares : p.shares.filter((s) => s.holder === viewer);

/** The viewer's own share, or an empty one when they have no linked spend yet. */
export const viewerShare = (p: CampaignPeriod, viewer: HolderKey): CampaignShare =>
  p.shares.find((s) => s.holder === viewer) ?? { holder: viewer, spend: 0, counted: 0, credit: 0 };

export const trackersVisibleTo = (viewer: HolderKey): CashbackTracker[] =>
  viewer === "takumi" ? CASHBACK_TRACKERS : CASHBACK_TRACKERS.filter((t) => t.holder === viewer);

export const trackerFor = (periodId: string, holder: HolderKey) =>
  CASHBACK_TRACKERS.find((t) => t.periodId === periodId && t.holder === holder);

export type ProgressState = "open" | "near" | "full";

export interface PeriodProgress {
  /** What the meter measures: pooled spend (ladder, points quota) or credit (caps). */
  measure: "spend" | "credit";
  value: number;
  target: number;
  ratio: number;
  state: ProgressState;
  /** One line: what's left / what the next step pays. */
  next: string;
}

const baht = (n: number, digits = 0) =>
  "฿" + n.toLocaleString("en-US", { minimumFractionDigits: digits, maximumFractionDigits: 2 });

const basisWord = (c: Campaign) =>
  c.periodBasis === "month" ? "this month" : c.periodBasis === "cycle" ? "this cycle" : "this campaign";

export const progressOf = (p: CampaignPeriod): PeriodProgress => {
  const c = campaignById(p.campaignId);
  const stateOf = (ratio: number): ProgressState =>
    ratio >= 1 ? "full" : ratio >= QUOTA_ALERT_THRESHOLD ? "near" : "open";

  if (c.shape === "ladder") {
    const top = (c.steps ?? [])[(c.steps ?? []).length - 1];
    const target = top?.at ?? 1;
    const ratio = Math.min(1, p.pooledSpend / target);
    const next = p.nextStep
      ? `${baht(p.nextStep.at - p.pooledSpend, 2)} more pooled spend pays ${baht(p.nextStep.credit)}`
      : `Top step reached — ${baht(p.credit)} ${basisWord(c)}`;
    return { measure: "spend", value: p.pooledSpend, target, ratio, state: stateOf(ratio), next };
  }

  if (c.shape === "points-quota") {
    const target = c.cap ?? 1;
    const ratio = Math.min(1, p.counted / target);
    const past = Math.max(0, p.pooledSpend - target);
    const next =
      ratio >= 1
        ? `Quota used up — rows now earn ${c.quota?.after ?? "the base rate"}${past > 0 ? ` (${baht(past, 2)} past it)` : ""}`
        : `${baht(target - p.counted, 2)} of ${c.quota?.bonus ?? "bonus"} spend left ${basisWord(c)}`;
    return { measure: "spend", value: p.counted, target, ratio, state: stateOf(ratio), next };
  }

  const target = c.cap ?? 1;
  const ratio = Math.min(1, p.credit / target);
  let next: string;
  if (ratio >= 1) next = `Cap reached ${basisWord(c)}`;
  else if (c.shape === "per-slip") {
    const left = Math.round((target - p.credit) / (c.perSlip?.credit ?? 1));
    next = `${left} more slip${left === 1 ? "" : "s"} of ${baht(c.perSlip?.minSlip ?? 0)}+ fill${left === 1 ? "s" : ""} the month`;
  } else next = `${baht(target - p.credit, 2)} of credit left ${basisWord(c)}`;
  return { measure: "credit", value: p.credit, target, ratio, state: stateOf(ratio), next };
};

/** Periods at or past the alert threshold, on cards the viewer holds. */
export const quotaAlertsFor = (viewer: HolderKey) =>
  periodsVisibleTo(viewer)
    .map((p) => ({ period: p, campaign: campaignById(p.campaignId), progress: progressOf(p) }))
    .filter((x) => x.progress.ratio >= QUOTA_ALERT_THRESHOLD);

export const SHAPE_LABEL: Record<Campaign["shape"], string> = {
  ladder: "ladder",
  "credit-cap": "credit cap",
  "per-slip": "per slip",
  "points-quota": "points quota",
};

export const BASIS_LABEL: Record<Campaign["periodBasis"], string> = {
  month: "per month",
  cycle: "per cycle",
  campaign: "whole campaign",
};
