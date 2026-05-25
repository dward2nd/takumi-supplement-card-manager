import { CARDS, CARD_LIST, last4For } from "./cards";
import type { CardInstance, HolderKey } from "./types";

/**
 * Materialise every card-instance visible to the given viewer.
 * - Takumi (admin): every (card, holder) where the holder actually holds it.
 * - Supplements: only their own instances.
 *
 * Ordering: Takumi's own instances first (when admin), then by issuer + name,
 * then by holder. The picker UI groups by issuer; this ordering keeps
 * the most-likely-default at the top.
 */
export const visibleInstances = (viewer: HolderKey): CardInstance[] => {
  const out: CardInstance[] = [];
  const include = (holder: HolderKey) => viewer === "takumi" || viewer === holder;

  for (const card of CARD_LIST) {
    for (const holder of card.holders) {
      if (!include(holder)) continue;
      out.push({ cardId: card.id, holder, last4: last4For(card, holder) });
    }
  }

  return out.sort((a, b) => {
    // Viewer's own instances first when admin sees others.
    if (viewer === "takumi") {
      if (a.holder === "takumi" && b.holder !== "takumi") return -1;
      if (b.holder === "takumi" && a.holder !== "takumi") return 1;
    }
    const ca = CARDS[a.cardId];
    const cb = CARDS[b.cardId];
    if (ca.issuer !== cb.issuer) return ca.issuer.localeCompare(cb.issuer);
    if (ca.name !== cb.name) return ca.name.localeCompare(cb.name);
    return a.holder.localeCompare(b.holder);
  });
};

export const instanceKey = (i: CardInstance) => `${i.cardId}#${i.holder}`;
