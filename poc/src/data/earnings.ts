import type { Card, Transaction } from "./types";

/** Numeric multiplier value from the `×N` / `÷4` checkbox names. */
const MULTIPLIER_VALUES: Record<string, number> = {
  "×0": 0,
  "×2": 2,
  "×3": 3,
  "×4": 4,
  "×5": 5,
  "÷4": 0.25,
};

export const multiplierValue = (m?: string | null): number => {
  if (!m) return 1; // default = ×1
  return MULTIPLIER_VALUES[m] ?? 1;
};

const isCreditRow = (tx: Transaction) =>
  tx.amount < 0 || /cashback/i.test(tx.name);

/**
 * Points the cardholder actually earned on this transaction.
 * - null when the card doesn't earn points (e.g. UOB One, SPayLater).
 * - 0 when the row is a credit/refund or the multiplier is ×0.
 * Truncates toward zero (Thai issuers typically round down at posting time).
 */
export const earnedPoints = (tx: Transaction, card: Card): number | null => {
  if (!card.bahtPer1Point || card.bahtPer1Point <= 0) return null;
  if (isCreditRow(tx)) return 0;
  const mult = multiplierValue(tx.multiplier);
  if (mult === 0) return 0;
  const raw = (tx.amount / card.bahtPer1Point) * mult;
  return Math.floor(Math.max(0, raw));
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
  return total;
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
