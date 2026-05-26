import { type ReactNode, useMemo } from "react";
import { groupBy } from "../data/format";
import { TransactionRow } from "./TransactionRow";
import type { Transaction } from "../data/types";

const dateHeader = new Intl.DateTimeFormat("en-GB", {
  weekday: "short",
  day: "numeric",
  month: "short",
});

/**
 * Reverse-chronologically date-grouped transaction list. Each day is a
 * section with a small eyebrow-style heading row above the per-day
 * TransactionRow block.
 *
 * `cap` (optional) limits the rendered transactions, but never slices
 * mid-day — once a day is opened it's rendered in full. This preserves the
 * grouping integrity at the cost of a slight over-cap.
 */
export const DateGroupedTransactions = ({
  transactions,
  cap,
  footer,
  emptyLabel,
}: {
  transactions: Transaction[];
  /** Approximate cap on rendered rows; never breaks a day open. */
  cap?: number;
  /** Slot rendered after the last day group — typically a "See all →" link. */
  footer?: ReactNode;
  /** Empty-state label. */
  emptyLabel?: string;
}) => {
  const groups = useMemo(() => {
    const byDay = groupBy(transactions, (t) => t.transactionDate);
    return [...byDay.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  }, [transactions]);

  // Walk day-by-day, accumulating rows until the cap is reached. Always
  // include the full day in which the cap was hit — never half a day.
  const visibleGroups = useMemo(() => {
    if (cap === undefined) return groups;
    const out: typeof groups = [];
    let used = 0;
    for (const [day, txs] of groups) {
      out.push([day, txs]);
      used += txs.length;
      if (used >= cap) break;
    }
    return out;
  }, [groups, cap]);

  if (transactions.length === 0) {
    return (
      <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
        <div className="px-5 py-10 text-center text-sm text-ink-faint">
          {emptyLabel ?? "No transactions in this scope."}
        </div>
      </div>
    );
  }

  return (
    <div className="mt-2 flex flex-col gap-4">
      {visibleGroups.map(([day, txs]) => (
        <section key={day}>
          <DateHeading iso={day} count={txs.length} />
          <div className="mt-1 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
            {txs.map((t, i) => (
              <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
            ))}
          </div>
        </section>
      ))}
      {footer && <div className="flex justify-end">{footer}</div>}
    </div>
  );
};

const DateHeading = ({ iso, count }: { iso: string; count: number }) => {
  const d = new Date(iso);
  const formatted = dateHeader.format(d);
  const [weekday, ...rest] = formatted.split(" ");
  return (
    <div className="flex items-baseline justify-between gap-3 px-1">
      <div className="flex items-baseline gap-2.5">
        <span className="text-[10.5px] uppercase tracking-[0.28em] text-amber-glow/80">
          {weekday}
        </span>
        <span className="font-display text-base font-normal text-ink">
          {rest.join(" ")}
        </span>
      </div>
      <span className="num text-[11px] text-ink-faint">
        {count} {count === 1 ? "row" : "rows"}
      </span>
    </div>
  );
};
