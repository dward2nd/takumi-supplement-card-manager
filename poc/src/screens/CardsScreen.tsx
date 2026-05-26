import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { visibleInstances } from "../data/card-instances";
import { CardFace } from "../components/CardFace";
import { PageHeader } from "../components/PageHeader";
import { Pill } from "../components/Pill";
import { HolderChipRow, type HolderFilter } from "../components/HolderChips";
import { activePromotionsFor } from "../data/promotions";
import type { HolderKey } from "../data/types";

export const CardsScreen = () => {
  const { holderKey: viewerKey } = useApp();
  const nav = useNavigate();
  const [holderFilter, setHolderFilter] = useState<HolderFilter>("all");
  if (!viewerKey) return null;

  // Per-instance list — one entry per (card, holder) pair. Admin sees them all.
  const instances = useMemo(() => visibleInstances(viewerKey), [viewerKey]);

  // Stable per-holder counts (independent of the chip filter) for the chip
  // row badges. Supplements only see their own row, so for them the counts
  // collapse to a single entry — used to decide whether to show chips at all.
  const holderCounts = useMemo(() => {
    const counts: Record<HolderKey, number> = { takumi: 0, baiboon: 0, nuta: 0 };
    for (const i of instances) counts[i.holder]++;
    return counts;
  }, [instances]);

  const filteredInstances = useMemo(() => {
    if (holderFilter === "all") return instances;
    return instances.filter((i) => i.holder === holderFilter);
  }, [instances, holderFilter]);

  // Group by holder so Takumi's admin view stays scannable.
  const byHolder = useMemo(() => {
    const groups: { holder: HolderKey; instances: typeof filteredInstances }[] = [];
    for (const i of filteredInstances) {
      let g = groups.find((x) => x.holder === i.holder);
      if (!g) {
        g = { holder: i.holder, instances: [] };
        groups.push(g);
      }
      g.instances.push(i);
    }
    // For admin Takumi: own cards first.
    return groups.sort((a, b) => {
      if (viewerKey === "takumi") {
        if (a.holder === "takumi" && b.holder !== "takumi") return -1;
        if (b.holder === "takumi" && a.holder !== "takumi") return 1;
      }
      return a.holder.localeCompare(b.holder);
    });
  }, [filteredInstances, viewerKey]);

  const isAdmin = viewerKey === "takumi";

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title="The wallet"
        eyebrow={`${instances.length} card supplements · current cycle`}
      />

      {isAdmin && (
        <div className="px-5 pb-4">
          <HolderChipRow
            counts={holderCounts}
            total={instances.length}
            active={holderFilter}
            onChange={setHolderFilter}
          />
        </div>
      )}

      <div className="px-5 pb-12 space-y-8">
        {byHolder.map(({ holder, instances }) => {
          const h = HOLDERS[holder];
          // Hide the per-holder section header when a single holder is
          // narrowed via the chip — the chip itself is the scope label.
          const showHolderHeader = isAdmin && holderFilter === "all";
          return (
            <section key={holder}>
              {showHolderHeader && (
                <div className="mb-3 flex items-baseline justify-between">
                  <div className="flex items-center gap-2">
                    <span
                      className="h-3 w-3 rounded-full"
                      style={{ background: h.accent }}
                    />
                    <span className="text-[12px] uppercase tracking-[0.28em] text-ink-faint">
                      {h.englishName} · {h.thaiName}
                    </span>
                  </div>
                  <span className="num text-[12px] text-ink-faint">
                    {instances.length}
                  </span>
                </div>
              )}

              <div className="grid grid-cols-1 gap-3 md:grid-cols-2 lg:grid-cols-3">
                {instances.map((i, idx) => {
                  const card = CARDS[i.cardId];
                  const promos = activePromotionsFor(card.id, "2026-05-26");
                  return (
                    <motion.div
                      key={`${i.cardId}#${i.holder}`}
                      initial={{ opacity: 0, y: 14 }}
                      animate={{ opacity: 1, y: 0 }}
                      transition={{ delay: 0.04 * idx, duration: 0.5, ease: [0.2, 0.7, 0.1, 1] }}
                    >
                      <button
                        onClick={() => nav(`/cards/${i.cardId}?holder=${i.holder}`)}
                        className="tap block w-full text-left"
                      >
                        <CardFace
                          card={card}
                          holder={i.holder}
                          showOverall
                        />
                        {promos.length > 0 && (
                          <div className="mt-2 flex flex-wrap items-center gap-1.5">
                            {promos.map((p) => (
                              <Pill key={p.id} tone="amber" uppercase={false}>
                                active promo · {p.name}
                              </Pill>
                            ))}
                          </div>
                        )}
                      </button>
                    </motion.div>
                  );
                })}
              </div>
            </section>
          );
        })}
        {byHolder.length === 0 && (
          <div className="py-12 text-center text-sm text-ink-faint">
            No cards in this scope.
          </div>
        )}
      </div>
    </div>
  );
};
