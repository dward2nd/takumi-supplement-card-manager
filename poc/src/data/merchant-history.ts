import { TRANSACTIONS } from "./transactions";
import type { CardId, HolderKey, Transaction } from "./types";

/**
 * Returns merchants the holder has used most often on a given card,
 * sorted by frequency (most-used first), then by recency. Cashback /
 * credit / payment rows (negative or "*CASHBACK*" / debt-takeover) are
 * skipped — they're not "merchants" in the everyday sense.
 *
 * In the real app this would come from the live Transactions DS. In the
 * POC it just reads from the seeded array.
 */
export const frequentMerchants = (
  holder: HolderKey,
  cardId: CardId,
  limit: number = 5,
): { name: string; lastUsed: string; count: number; lastAmount: number }[] => {
  const counts = new Map<
    string,
    { name: string; lastUsed: string; count: number; lastAmount: number }
  >();
  for (const t of TRANSACTIONS) {
    if (t.holder !== holder || t.cardId !== cardId) continue;
    if (isHistoryNoise(t)) continue;
    const k = t.name;
    const existing = counts.get(k);
    if (!existing) {
      counts.set(k, { name: t.name, lastUsed: t.transactionDate, count: 1, lastAmount: t.amount });
    } else {
      existing.count += 1;
      if (t.transactionDate > existing.lastUsed) {
        existing.lastUsed = t.transactionDate;
        existing.lastAmount = t.amount;
      }
    }
  }
  return [...counts.values()]
    .sort(
      (a, b) =>
        b.count - a.count ||
        b.lastUsed.localeCompare(a.lastUsed),
    )
    .slice(0, limit);
};

const isHistoryNoise = (t: Transaction) => {
  if (t.amount <= 0) return true;
  if (/cashback/i.test(t.name)) return true;
  if (/^\[.+?\]/.test(t.name)) return true; // debt-takeover-tagged rows
  if (/installment|\d{2}\/\d{2}/.test(t.name)) return true;
  return false;
};
