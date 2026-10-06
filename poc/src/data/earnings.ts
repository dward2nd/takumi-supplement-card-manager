import type { Card, Transaction } from "./types";

/** Numeric multiplier value from the `×N` / `÷4` checkbox names. */
const MULTIPLIER_VALUES: Record<string, number> = {
  "×0": 0,
  "×2": 2,
  "×3": 3,
  "×4": 4,
  "×5": 5,
  "×6": 6,
  "÷4": 0.25,
};

export const multiplierValue = (m?: string | null): number => {
  if (!m) return 1; // default = ×1
  return MULTIPLIER_VALUES[m] ?? 1;
};

const isCreditRow = (tx: Transaction) =>
  tx.amount < 0 || /cashback/i.test(tx.name);

/** `คะแนนต่อ 1 หน่วย` — empty (or not above 0) counts as 1. */
export const pointsPerUnit = (card: Card): number =>
  card.pointsPerUnit !== undefined && card.pointsPerUnit > 0 ? card.pointsPerUnit : 1;

/** True when the card can earn fractions of a point (Lotus's coins). */
export const earnsFractionalPoints = (card: Card): boolean => pointsPerUnit(card) < 1;

/**
 * Points the cardholder actually earned on this transaction — a port of the
 * `คะแนนที่ได้จริง` formula (docs/formulas/points-realized.md):
 *
 *   floor(floor(ยอดชำระ / บาทต่อ 1 คะแนน) × multiplier) × คะแนนต่อ 1 หน่วย
 *
 * **Floor first, then multiply.** Whole baht blocks are counted per line, the
 * multiplier applies to the already-floored blocks (the outer floor only bites
 * on `÷4`), and the per-unit figure comes last so a quarter-coin survives:
 * ฿151 at Lotus's = floor(151/50) × 6 × 0.25 = 4.5 coins; ฿52 elsewhere = 0.25.
 *
 * - null when the card doesn't earn points (e.g. UOB One, SPayLater).
 * - 0 when the row is a credit/refund or the multiplier is ×0.
 */
export const earnedPoints = (tx: Transaction, card: Card): number | null => {
  if (!card.bahtPer1Point || card.bahtPer1Point <= 0) return null;
  if (isCreditRow(tx)) return 0;
  const mult = multiplierValue(tx.multiplier);
  if (mult === 0) return 0;
  const blocks = Math.floor(tx.amount / card.bahtPer1Point);
  const pts = Math.floor(blocks * mult) * pointsPerUnit(card);
  // Quarter-coins are binary-exact, but round to the satang-equivalent anyway
  // so a future 0.1-style unit can't leak float noise into the UI.
  return Math.max(0, Math.round(pts * 100) / 100);
};

/** Baht of cashback earned on this row. null when no cashback applies. */
export const earnedCashback = (tx: Transaction): number | null => {
  if (isCreditRow(tx)) return null;
  if (tx.cashbackPercent === undefined || tx.cashbackPercent === 0) return null;
  return Math.round(tx.amount * tx.cashbackPercent * 100) / 100;
};

/** Sum of earned points across a list of transactions on a given card. */
export const sumPoints = (txs: Transaction[], card: Card): number => {
  let total = 0;
  for (const t of txs) {
    const p = earnedPoints(t, card);
    if (p !== null) total += p;
  }
  return Math.round(total * 100) / 100;
};

/** Sum of earned cashback across a list of transactions. */
export const sumCashback = (txs: Transaction[]): number => {
  let total = 0;
  for (const t of txs) {
    const c = earnedCashback(t);
    if (c !== null) total += c;
  }
  return total;
};

/**
 * Format a points figure for this card: up to 2 decimals where the card earns
 * fractions (Lotus's coins — `4.5`, `0.25`, `87.25`), whole numbers elsewhere.
 */
export const fmtPoints = (n: number, card: Card): string =>
  earnsFractionalPoints(card)
    ? n.toLocaleString("en-US", { minimumFractionDigits: 0, maximumFractionDigits: 2 })
    : Math.round(n).toLocaleString("en-US");

/** "pts" or the issuer's own word ("coins"). */
export const pointsLabel = (card: Card, short = true): string =>
  card.pointsName ?? (short ? "pts" : "points");
