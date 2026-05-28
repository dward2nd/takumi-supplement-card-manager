// Installment helpers — POC mirror of `scripts/python/lib/installments.py`.
//
// Two responsibilities:
//   1. Parse the trailing `NN/NN` suffix off a merchant string into a
//      structured `InstallmentTerm` so the UI gets typed data, not regex
//      scrubbing at render time.
//   2. Cluster a card's installment rows into distinct *plans* — same
//      logic as the Python lib: group by (base, total), then partition by
//      per-term amount within a 5% tolerance so two parallel Shopee plans
//      at different amounts read as separate sub-stanzas.
//
// Pure functions, no React imports — safe to import from data files.

import type { InstallmentTerm, Transaction } from "./types";

// Suffix matches `<base>` + space + `NN/NN`. Anchored at end so a stray
// `12/03` mid-string (e.g. a date) never trips this. Up to 3-digit terms.
const SUFFIX_RE = /^(?<base>.+?)\s+(?<term>\d{1,3})\/(?<total>\d{1,3})$/;

// Per-term amounts cluster if they're within 5% — same threshold as the
// Python lib. Absorbs bank-side rounding (e.g. 375.30 → 373.00 across
// consecutive terms) while keeping plans at materially different
// per-term amounts in separate buckets.
const AMOUNT_TOLERANCE = 0.05;

export const parseInstallmentName = (
  name: string,
  perTermAmount: number,
): InstallmentTerm | undefined => {
  if (!name) return undefined;
  const m = SUFFIX_RE.exec(name.trim());
  if (!m || !m.groups) return undefined;
  const term = Number(m.groups.term);
  const total = Number(m.groups.total);
  if (!Number.isFinite(term) || !Number.isFinite(total)) return undefined;
  if (term < 1 || total < 1 || term > total) return undefined;
  return {
    base: m.groups.base.trim(),
    term,
    total,
    perTermAmount,
  };
};

/** Format an installment name from base + term + total. Width matches `total`. */
export const formatInstallmentName = (
  base: string,
  term: number,
  total: number,
): string => {
  const width = Math.max(2, String(total).length);
  const pad = (n: number) => String(n).padStart(width, "0");
  return `${base.trim()} ${pad(term)}/${pad(total)}`;
};

const amountsMatch = (a: number, b: number): boolean => {
  if (a === 0 && b === 0) return true;
  const denom = Math.max(Math.abs(a), Math.abs(b));
  if (denom === 0) return false;
  return Math.abs(a - b) / denom < AMOUNT_TOLERANCE;
};

/**
 * A plan = one cluster of installment rows under the same (base, total)
 * with matching per-term amounts. Each row in the cluster is one term
 * already posted; the plan progresses as new rows are written.
 */
export interface InstallmentPlan {
  base: string;
  total: number;
  perTermAmount: number;
  /** Sorted ascending by term. */
  rows: Transaction[];
  /** Convenience — highest term posted. Equal to `rows.at(-1).installment.term`. */
  maxTerm: number;
  /** total - maxTerm. Zero when the plan is complete. */
  remainingTerms: number;
  /** Sum of the still-to-come terms at the canonical per-term amount. */
  remainingAmount: number;
}

/**
 * Partition a list of transactions into installment plans.
 *
 * Non-installment rows are skipped. Plans are returned in stable order:
 * by `base` then by `perTermAmount`, so multi-plan cards render
 * deterministically. Within each plan, rows are sorted ascending by term.
 */
export const clusterTransactionsByPlan = (txs: Transaction[]): InstallmentPlan[] => {
  // Step 1: group by (base, total).
  const groups = new Map<string, Transaction[]>();
  for (const tx of txs) {
    if (!tx.installment) continue;
    const key = `${tx.installment.base}\x00${tx.installment.total}`;
    const bucket = groups.get(key);
    if (bucket) bucket.push(tx);
    else groups.set(key, [tx]);
  }

  // Step 2: within each group, cluster by per-term amount (greedy, 5% tolerance).
  const plans: InstallmentPlan[] = [];
  for (const [key, rows] of groups) {
    const [base, totalStr] = key.split("\x00");
    const total = Number(totalStr);
    const buckets: Transaction[][] = [];
    for (const tx of rows) {
      const amt = tx.installment!.perTermAmount;
      let placed = false;
      for (const b of buckets) {
        const ref = b[0].installment!.perTermAmount;
        if (amountsMatch(amt, ref)) {
          b.push(tx);
          placed = true;
          break;
        }
      }
      if (!placed) buckets.push([tx]);
    }
    for (const bucket of buckets) {
      const sorted = [...bucket].sort(
        (a, b) => a.installment!.term - b.installment!.term,
      );
      const perTermAmount = sorted[0].installment!.perTermAmount;
      const maxTerm = sorted[sorted.length - 1].installment!.term;
      const remainingTerms = Math.max(0, total - maxTerm);
      plans.push({
        base,
        total,
        perTermAmount,
        rows: sorted,
        maxTerm,
        remainingTerms,
        remainingAmount: remainingTerms * perTermAmount,
      });
    }
  }

  // Step 3: deterministic order — base ASC, then perTermAmount ASC.
  plans.sort((a, b) => {
    const byBase = a.base.localeCompare(b.base);
    if (byBase !== 0) return byBase;
    return a.perTermAmount - b.perTermAmount;
  });

  return plans;
};

/**
 * Filter a card's plans down to ones still in progress (max_term < total).
 * Sorted with the longest-tail commitments first (most remaining), since
 * those are usually the ones the user wants to see prominently.
 */
export const inProgressPlans = (txs: Transaction[]): InstallmentPlan[] =>
  clusterTransactionsByPlan(txs)
    .filter((p) => p.remainingTerms > 0)
    .sort((a, b) => {
      // Primary: more remaining terms first.
      if (b.remainingTerms !== a.remainingTerms) {
        return b.remainingTerms - a.remainingTerms;
      }
      // Secondary: larger per-term amount first.
      return b.perTermAmount - a.perTermAmount;
    });

/** Aggregate every plan's remaining commitment across a list of transactions. */
export const totalRemainingObligation = (txs: Transaction[]): number =>
  inProgressPlans(txs).reduce((s, p) => s + p.remainingAmount, 0);
