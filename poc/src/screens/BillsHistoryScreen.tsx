import { useMemo, useState } from "react";
import clsx from "clsx";
import { useApp } from "../data/state";
import { BILLS } from "../data/bills";
import { CARDS } from "../data/cards";
import { HOLDER_LIST } from "../data/holders";
import { PageHeader } from "../components/PageHeader";
import { BillRow } from "../components/BillRow";
import { HolderChipRow, type HolderFilter } from "../components/HolderChips";
import type { CardId, HolderKey } from "../data/types";

export const BillsHistoryScreen = () => {
  const { holderKey: viewerKey } = useApp();
  if (!viewerKey) return null;

  // Scope: paid bills only — this is the archive.
  const visiblePaid = useMemo(() => {
    const inScope: ("baiboon" | "nuta")[] =
      viewerKey === "takumi"
        ? ["baiboon", "nuta"]
        : viewerKey === "baiboon"
          ? ["baiboon"]
          : ["nuta"];
    return BILLS.filter(
      (b) => b.status === "paid" && inScope.includes(b.holder),
    ).sort((a, b) => b.billCycleDate.localeCompare(a.billCycleDate));
  }, [viewerKey]);

  const [cycle, setCycle] = useState<"all" | string>("all");
  const [holderFilter, setHolderFilter] = useState<HolderFilter>("all");
  const [cardId, setCardId] = useState<"all" | CardId>("all");
  const [showAllCycles, setShowAllCycles] = useState(false);

  const cycleCounts = useMemo(() => {
    const counts = new Map<string, number>();
    for (const b of visiblePaid) {
      const k = b.billCycleDate.slice(0, 7);
      counts.set(k, (counts.get(k) ?? 0) + 1);
    }
    return [...counts.entries()].sort((a, b) => b[0].localeCompare(a[0]));
  }, [visiblePaid]);

  const visibleCycles = showAllCycles ? cycleCounts : cycleCounts.slice(0, 6);

  // Per-holder counts for the chip row badges (admin only).
  const holderCounts = useMemo(() => {
    const counts: Record<HolderKey, number> = { takumi: 0, baiboon: 0, nuta: 0 };
    for (const b of visiblePaid) counts[b.holder]++;
    return counts;
  }, [visiblePaid]);

  // Per-card counts for the card filter pills.
  const cardCounts = useMemo(() => {
    const counts = new Map<CardId, number>();
    for (const b of visiblePaid) {
      counts.set(b.cardId, (counts.get(b.cardId) ?? 0) + 1);
    }
    return [...counts.entries()].sort((a, b) =>
      CARDS[a[0]].name.localeCompare(CARDS[b[0]].name),
    );
  }, [visiblePaid]);

  const filtered = useMemo(() => {
    return visiblePaid.filter((b) => {
      if (cycle !== "all" && b.billCycleDate.slice(0, 7) !== cycle) return false;
      if (holderFilter !== "all" && b.holder !== holderFilter) return false;
      if (cardId !== "all" && b.cardId !== cardId) return false;
      return true;
    });
  }, [visiblePaid, cycle, holderFilter, cardId]);

  // Bills DB only exists for supplement holders, so the admin chip row
  // excludes Takumi.
  const include = HOLDER_LIST.filter((h) => h.key !== "takumi");

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title="Paid bills"
        eyebrow={`${visiblePaid.length} across all cycles`}
        back
      />

      <div className="lg:grid lg:grid-cols-12 lg:gap-8 lg:px-5">
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
                  all <span className="num text-[11px] text-ink-faint">{visiblePaid.length}</span>
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

            {viewerKey === "takumi" && (
              <div className="mt-5">
                <div className="mb-2 text-[10.5px] uppercase tracking-[0.24em] text-ink-faint">
                  holder
                </div>
                <HolderChipRow
                  counts={holderCounts}
                  total={visiblePaid.length}
                  active={holderFilter}
                  onChange={setHolderFilter}
                  include={include}
                />
              </div>
            )}

            <div className="mt-5">
              <div className="mb-2 text-[10.5px] uppercase tracking-[0.24em] text-ink-faint">
                card
              </div>
              <div className="-mx-1 flex flex-wrap gap-1.5 px-1">
                <FilterPill active={cardId === "all"} onClick={() => setCardId("all")}>
                  all
                </FilterPill>
                {cardCounts.map(([id, n]) => (
                  <FilterPill key={id} active={cardId === id} onClick={() => setCardId(id)}>
                    {CARDS[id].name}{" "}
                    <span className="num text-[11px] text-ink-faint">{n}</span>
                  </FilterPill>
                ))}
              </div>
            </div>

            <div className="mt-5 rule" />
            <div className="mt-3 flex items-baseline justify-between text-[11px] uppercase tracking-[0.18em] text-ink-faint">
              <span>matching</span>
              <span className="num text-ink">{filtered.length}</span>
            </div>
          </div>
        </aside>

        <div className="px-5 pt-4 pb-12 lg:col-span-8 lg:px-0 lg:pt-0">
          {filtered.length === 0 ? (
            <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
              <div className="px-5 py-10 text-center text-sm text-ink-faint">
                No paid bills match these filters.
              </div>
            </div>
          ) : (
            <div className="grid gap-2 md:grid-cols-2 lg:grid-cols-2">
              {filtered.map((b, i) => (
                <BillRow key={b.id} bill={b} index={i} />
              ))}
            </div>
          )}
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
