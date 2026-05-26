import { useMemo, useState } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { Search } from "lucide-react";
import clsx from "clsx";
import { useApp } from "../data/state";
import { CARDS, last4For } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { TRANSACTIONS } from "../data/transactions";
import { PageHeader } from "../components/PageHeader";
import { DateGroupedTransactions } from "../components/DateGroupedTransactions";
import type { CardId, HolderKey } from "../data/types";

const TODAY = "2026-05-26"; // POC reference date — must stay in sync with CardDetailScreen.

type TypeFilter = "all" | "debit" | "credit";

/**
 * Full archive of one card-instance's transactions, with a quiet filter row.
 * Reached from CardDetail's "See all N transactions →" link when the recent
 * list is capped.
 */
export const TransactionsHistoryScreen = () => {
  const { holderKey: viewerKey } = useApp();
  const { id } = useParams();
  const [params] = useSearchParams();
  const card = id ? CARDS[id as CardId] : undefined;
  if (!card || !viewerKey) return null;

  const requestedHolder = params.get("holder") as HolderKey | null;
  const instanceHolder: HolderKey =
    requestedHolder && card.holders.includes(requestedHolder)
      ? requestedHolder
      : card.holders.includes(viewerKey)
        ? viewerKey
        : card.holders[0];

  // Scope rule: Takumi (admin) can view any instance; supplements only their own.
  if (viewerKey !== "takumi" && instanceHolder !== viewerKey) return null;

  // History view = today-or-past only. Future-dated installments are surfaced
  // on the CardDetail screen's "Upcoming" section, not here.
  const allTxs = useMemo(
    () =>
      TRANSACTIONS.filter(
        (t) =>
          t.cardId === card.id &&
          t.holder === instanceHolder &&
          t.transactionDate <= TODAY,
      ).sort((a, b) => b.transactionDate.localeCompare(a.transactionDate)),
    [card.id, instanceHolder],
  );

  const [cycle, setCycle] = useState<"all" | string>("all");
  const [typeFilter, setTypeFilter] = useState<TypeFilter>("all");
  const [query, setQuery] = useState("");
  const [showAllCycles, setShowAllCycles] = useState(false);

  const cycleCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const t of allTxs) {
      const key = t.billCycleDate.slice(0, 7); // YYYY-MM
      counts.set(key, (counts.get(key) ?? 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  }, [allTxs]);

  const visibleCycles = showAllCycles ? cycleCounts : cycleCounts.slice(0, 6);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return allTxs.filter((t) => {
      if (cycle !== "all" && t.billCycleDate.slice(0, 7) !== cycle) return false;
      if (typeFilter === "debit" && t.amount <= 0) return false;
      if (typeFilter === "credit" && t.amount >= 0) return false;
      if (q && !t.name.toLowerCase().includes(q)) return false;
      return true;
    });
  }, [allTxs, cycle, typeFilter, query]);

  const instance = HOLDERS[instanceHolder];

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title={`${card.name} · transactions`}
        eyebrow={`${instance.englishName}'s · •••• ${last4For(card, instanceHolder)} · ${allTxs.length} rows total`}
        back
      />

      <div className="lg:grid lg:grid-cols-12 lg:gap-8 lg:px-5">
        {/* Filters — at lg+ sticky left sidebar; stack above at mobile/md. */}
        <aside className="px-5 lg:col-span-4 lg:px-0 lg:sticky lg:top-6 lg:self-start">
          <div className="rounded-3xl border border-paper-line/70 bg-paper-raised/40 p-5">
            <div className="text-[12px] uppercase tracking-[0.28em] text-amber-glow/90">
              filters
            </div>

            <div className="mt-4">
              <div className="mb-2 text-[10.5px] uppercase tracking-[0.24em] text-ink-faint">
                cycle
              </div>
              <div className="-mx-1 flex flex-wrap gap-1.5 px-1">
                <FilterPill active={cycle === "all"} onClick={() => setCycle("all")}>
                  all <span className="num text-[11px] text-ink-faint">{allTxs.length}</span>
                </FilterPill>
                {visibleCycles.map(([k, n]) => (
                  <FilterPill key={k} active={cycle === k} onClick={() => setCycle(k)}>
                    <span className="num">{k}</span>{" "}
                    <span className="num text-[11px] text-ink-faint">{n}</span>
                  </FilterPill>
                ))}
                {cycleCounts.length > 6 && !showAllCycles && (
                  <FilterPill active={false} onClick={() => setShowAllCycles(true)}>
                    older →
                  </FilterPill>
                )}
              </div>
            </div>

            <div className="mt-5">
              <div className="mb-2 text-[10.5px] uppercase tracking-[0.24em] text-ink-faint">
                type
              </div>
              <div className="flex gap-1.5">
                <FilterPill active={typeFilter === "all"} onClick={() => setTypeFilter("all")}>
                  all
                </FilterPill>
                <FilterPill active={typeFilter === "debit"} onClick={() => setTypeFilter("debit")}>
                  debit
                </FilterPill>
                <FilterPill active={typeFilter === "credit"} onClick={() => setTypeFilter("credit")}>
                  credit
                </FilterPill>
              </div>
            </div>

            <div className="mt-5">
              <div className="mb-2 text-[10.5px] uppercase tracking-[0.24em] text-ink-faint">
                merchant
              </div>
              <label className="flex items-center gap-2 rounded-xl border border-paper-line bg-paper px-3 py-2.5 focus-within:border-amber-200/60">
                <Search size={14} strokeWidth={1.6} className="text-ink-faint" />
                <input
                  type="text"
                  value={query}
                  onChange={(e) => setQuery(e.target.value)}
                  placeholder="Search merchant…"
                  className="w-full bg-transparent text-sm text-ink placeholder:text-ink-ghost focus:outline-none"
                />
              </label>
            </div>

            <div className="mt-5 rule" />
            <div className="mt-3 flex items-baseline justify-between text-[11px] uppercase tracking-[0.18em] text-ink-faint">
              <span>matching</span>
              <span className="num text-ink">{filtered.length}</span>
            </div>
          </div>
        </aside>

        <div className="px-5 pt-4 pb-12 lg:col-span-8 lg:px-0 lg:pt-0">
          <DateGroupedTransactions
            transactions={filtered}
            emptyLabel={
              query || cycle !== "all" || typeFilter !== "all"
                ? "No transactions match these filters."
                : "No transactions on this card yet."
            }
          />
        </div>
      </div>
    </div>
  );
};

const FilterPill = ({
  active,
  onClick,
  children,
}: {
  active: boolean;
  onClick: () => void;
  children: React.ReactNode;
}) => (
  <button
    onClick={onClick}
    aria-pressed={active}
    className={clsx(
      "tap shrink-0 rounded-full border px-3 text-[12px] uppercase tracking-[0.18em] transition-colors",
      active
        ? "border-amber-200/40 bg-amber-300/[0.08] text-ink"
        : "border-paper-line/80 bg-paper-raised/40 text-ink-dim hover:bg-paper-raised hover:text-ink",
    )}
  >
    {children}
  </button>
);
