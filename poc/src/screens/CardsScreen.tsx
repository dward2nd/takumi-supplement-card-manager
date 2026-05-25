import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { visibleInstances } from "../data/card-instances";
import { CardFace } from "../components/CardFace";
import { PageHeader } from "../components/PageHeader";
import { Pill } from "../components/Pill";
import { activePromotionsFor } from "../data/promotions";
import type { HolderKey } from "../data/types";

export const CardsScreen = () => {
  const { holderKey: viewerKey } = useApp();
  const nav = useNavigate();
  if (!viewerKey) return null;

  // Per-instance list — one entry per (card, holder) pair. Admin sees them all.
  const instances = useMemo(() => visibleInstances(viewerKey), [viewerKey]);

  // Group by holder so Takumi's admin view stays scannable.
  const byHolder = useMemo(() => {
    const groups: { holder: HolderKey; instances: typeof instances }[] = [];
    for (const i of instances) {
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
  }, [instances, viewerKey]);

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title="The wallet"
        eyebrow={`${instances.length} card supplements · current cycle`}
      />

      <div className="px-5 pb-12 space-y-8">
        {byHolder.map(({ holder, instances }) => {
          const h = HOLDERS[holder];
          const showHolderHeader = viewerKey === "takumi";
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
      </div>
    </div>
  );
};
