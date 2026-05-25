import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { CARDS, cardsForHolder } from "../data/cards";
import { TRANSACTIONS } from "../data/transactions";
import { CardFace } from "../components/CardFace";
import { PageHeader } from "../components/PageHeader";
import { Pill } from "../components/Pill";
import { activePromotionsFor } from "../data/promotions";

export const CardsScreen = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  if (!holderKey) return null;

  const cards = useMemo(() => {
    if (holderKey === "takumi") {
      // Admin: union of all distinct cards across holders
      return Object.values(CARDS);
    }
    return cardsForHolder(holderKey);
  }, [holderKey]);

  return (
    <div>
      <PageHeader
        title="The wallet"
        eyebrow={`${cards.length} cards · current cycle`}
      />

      <div className="px-5 pb-12 space-y-3">
        {cards.map((c, i) => {
          const outstanding = TRANSACTIONS.filter(
            (t) =>
              t.cardId === c.id &&
              t.billCycleDate === currentBcFor(c.id) &&
              (holderKey === "takumi" || t.holder === holderKey),
          ).reduce((s, t) => s + t.amount, 0);
          const promos = activePromotionsFor(c.id, "2026-05-26");
          return (
            <motion.div
              key={c.id}
              initial={{ opacity: 0, y: 14 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.04 * i, duration: 0.5, ease: [0.2, 0.7, 0.1, 1] }}
            >
              <button
                onClick={() => nav(`/cards/${c.id}`)}
                className="tap block w-full text-left"
              >
                <CardFace card={c} outstanding={outstanding > 0 ? outstanding : 0} />
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
    </div>
  );
};

const currentBcFor = (cardId: string): string => {
  // Simplification: UOB cards = 2026-05-25; Krungsri (First Choice et al) = 2026-06-05
  const c = CARDS[cardId as keyof typeof CARDS];
  if (c.issuer === "UOB") return "2026-05-25";
  if (c.issuer === "Krungsri" || c.issuer === "CardX") return "2026-06-05";
  return "2026-05-25";
};
