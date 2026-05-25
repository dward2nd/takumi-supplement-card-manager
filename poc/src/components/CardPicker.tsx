import { useEffect, useMemo, useRef, useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { ChevronDown, Search, X } from "lucide-react";
import clsx from "clsx";
import { CARDS } from "../data/cards";
import { HOLDERS, HOLDER_LIST } from "../data/holders";
import { instanceKey } from "../data/card-instances";
import type { CardInstance, HolderKey } from "../data/types";

type HolderFilter = HolderKey | "all";

interface Props {
  selected: CardInstance | null;
  /** All card-instances the viewer is allowed to choose from. */
  instances: CardInstance[];
  /** Instance keys touched most recently, top-first. */
  recents?: string[];
  onChange: (i: CardInstance) => void;
}

/**
 * A tap-to-open card-instance picker. Each row is one (card, holder) pair,
 * because multiple holders can have the same product (different last-4).
 * Bottom-sheet pattern scales past the horizontal-pill ceiling.
 */
export const CardPicker = ({ selected, instances, recents, onChange }: Props) => {
  const [open, setOpen] = useState(false);
  const card = selected ? CARDS[selected.cardId] : null;
  const holder = selected ? HOLDERS[selected.holder] : null;

  return (
    <>
      <button
        onClick={() => setOpen(true)}
        className={clsx(
          "tap flex w-full items-center justify-between gap-3 rounded-2xl border px-4 py-3.5 text-left",
          "transition-colors duration-200",
          selected
            ? "border-amber-200/40 bg-amber-300/[0.05]"
            : "border-paper-line bg-paper-raised/40 hover:bg-paper-raised",
        )}
        aria-label="Select card"
      >
        <div className="flex items-center gap-3 min-w-0">
          <span
            aria-hidden
            className="h-9 w-9 shrink-0 rounded-lg"
            style={
              card
                ? {
                    background: `linear-gradient(135deg, ${card.brandColors[0]}, ${card.brandColors[1]})`,
                  }
                : { background: "rgba(255,255,255,0.04)" }
            }
          />
          <div className="min-w-0 flex-1">
            <div className="flex items-baseline gap-1.5 text-[12px] uppercase tracking-[0.18em] text-ink-faint">
              <span>{card?.issuer ?? "card"}</span>
              {selected && (
                <span className="num text-ink-faint/80">·</span>
              )}
              {selected && (
                <span className="num text-ink-faint/80">•••• {selected.last4}</span>
              )}
            </div>
            <div className="mt-0.5 flex items-baseline gap-2">
              <span
                className={clsx(
                  "truncate font-display text-base font-normal tracking-tight",
                  card ? "text-ink" : "text-ink-faint",
                )}
              >
                {card ? card.name : "Choose a card"}
              </span>
              {holder && (
                <span className="shrink-0 text-[12px] uppercase tracking-[0.18em]" style={{ color: holder.accent }}>
                  {holder.englishName}
                </span>
              )}
            </div>
          </div>
        </div>
        <ChevronDown
          size={18}
          strokeWidth={1.6}
          className="shrink-0 text-ink-faint"
        />
      </button>

      <AnimatePresence>
        {open && (
          <CardSheet
            instances={instances}
            recents={recents}
            selected={selected}
            onPick={(i) => {
              onChange(i);
              setOpen(false);
            }}
            onClose={() => setOpen(false)}
          />
        )}
      </AnimatePresence>
    </>
  );
};

const CardSheet = ({
  instances,
  recents,
  selected,
  onPick,
  onClose,
}: {
  instances: CardInstance[];
  recents?: string[];
  selected: CardInstance | null;
  onPick: (i: CardInstance) => void;
  onClose: () => void;
}) => {
  const [query, setQuery] = useState("");
  const [holderFilter, setHolderFilter] = useState<HolderFilter>("all");
  const searchRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    if (window.matchMedia("(min-width: 768px)").matches) {
      searchRef.current?.focus();
    }
  }, []);

  useEffect(() => {
    const onKey = (e: KeyboardEvent) => {
      if (e.key === "Escape") onClose();
    };
    window.addEventListener("keydown", onKey);
    return () => window.removeEventListener("keydown", onKey);
  }, [onClose]);

  // Per-holder totals are derived from the full instances list (not from the
  // search-filtered subset) so chip badges stay stable as the user types.
  const holderCounts = useMemo(() => {
    const counts: Record<HolderKey, number> = { takumi: 0, baiboon: 0, nuta: 0 };
    for (const i of instances) counts[i.holder]++;
    return counts;
  }, [instances]);

  const filtered = useMemo(() => {
    const q = query.trim().toLowerCase();
    return instances.filter((i) => {
      if (holderFilter !== "all" && i.holder !== holderFilter) return false;
      if (!q) return true;
      const c = CARDS[i.cardId];
      return (
        c.name.toLowerCase().includes(q) ||
        c.issuer.toLowerCase().includes(q) ||
        HOLDERS[i.holder].englishName.toLowerCase().includes(q) ||
        i.last4.includes(q)
      );
    });
  }, [instances, query, holderFilter]);

  // Header count reflects the chip-filtered subset (ignoring query) so the
  // headline number describes the scope the user has narrowed to, while the
  // query just thins the visible rows further.
  const scopeCount = useMemo(() => {
    if (holderFilter === "all") return instances.length;
    return holderCounts[holderFilter];
  }, [instances, holderFilter, holderCounts]);

  const recentList = useMemo(() => {
    if (!recents?.length) return [];
    const filteredKeys = new Set(filtered.map((i) => instanceKey(i)));
    const byKey = new Map(instances.map((i) => [instanceKey(i), i]));
    return recents
      .map((k) => byKey.get(k))
      .filter((i): i is CardInstance => Boolean(i && filteredKeys.has(instanceKey(i))))
      .slice(0, 4);
  }, [recents, filtered, instances]);

  const restGrouped = useMemo(() => {
    const recentKeys = new Set(recentList.map((i) => instanceKey(i)));
    const groups = new Map<string, CardInstance[]>();
    for (const i of filtered) {
      if (recentKeys.has(instanceKey(i))) continue;
      const k = CARDS[i.cardId].issuer;
      if (!groups.has(k)) groups.set(k, []);
      groups.get(k)!.push(i);
    }
    return [...groups.entries()].sort((a, b) => a[0].localeCompare(b[0]));
  }, [filtered, recentList]);

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      transition={{ duration: 0.2 }}
      className="fixed inset-0 z-50 flex items-end justify-center"
      onClick={onClose}
    >
      <span aria-hidden className="absolute inset-0 bg-paper/70 backdrop-blur-sm" />

      <motion.div
        role="dialog"
        aria-modal="true"
        initial={{ y: "100%" }}
        animate={{ y: 0 }}
        exit={{ y: "100%" }}
        transition={{ duration: 0.35, ease: [0.2, 0.7, 0.1, 1] }}
        className="relative z-10 mx-auto flex h-[80dvh] w-full max-w-md md:max-w-lg flex-col rounded-t-3xl border border-paper-line bg-paper-raised shadow-glow-amber"
        onClick={(e) => e.stopPropagation()}
      >
        <div className="flex justify-center py-3">
          <span className="h-1 w-10 rounded-full bg-ink-ghost/60" />
        </div>

        <header className="flex items-center justify-between px-5 pb-3">
          <div>
            <div className="text-[12px] uppercase tracking-[0.28em] text-amber-glow/90">
              choose a card
            </div>
            <h2 className="mt-1 font-display text-xl font-normal tracking-tight text-ink">
              <span className="num">{scopeCount}</span> cards
            </h2>
          </div>
          <button
            onClick={onClose}
            className="tap -mr-2 flex items-center gap-1 rounded-full px-2 py-1 text-ink-faint hover:text-ink"
            aria-label="close"
          >
            <X size={16} strokeWidth={1.5} />
          </button>
        </header>

        <div className="-mx-1 flex gap-2 overflow-x-auto px-5 pb-3 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden">
          <HolderChip
            label="All"
            count={instances.length}
            dot="rgb(var(--amber-glow))"
            active={holderFilter === "all"}
            accent={null}
            onClick={() => setHolderFilter("all")}
          />
          {HOLDER_LIST.map((h) => (
            <HolderChip
              key={h.key}
              label={h.englishName}
              count={holderCounts[h.key]}
              dot={h.accent}
              accent={h.accent}
              active={holderFilter === h.key}
              onClick={() => setHolderFilter(h.key)}
            />
          ))}
        </div>

        <div className="px-5 pb-3">
          <label className="flex items-center gap-2 rounded-xl border border-paper-line bg-paper px-3 py-2.5 focus-within:border-amber-200/60">
            <Search size={14} strokeWidth={1.6} className="text-ink-faint" />
            <input
              ref={searchRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              placeholder="Search name, issuer, holder, or last-4…"
              className="w-full bg-transparent text-sm text-ink placeholder:text-ink-ghost focus:outline-none"
            />
          </label>
        </div>

        <div className="flex-1 overflow-y-auto px-5 pb-8">
          {recentList.length > 0 && (
            <Group title="Recent" instances={recentList} selected={selected} onPick={onPick} />
          )}
          {restGrouped.map(([issuer, group]) => (
            <Group
              key={issuer}
              title={issuer}
              instances={group}
              selected={selected}
              onPick={onPick}
            />
          ))}
          {filtered.length === 0 && (
            <div className="py-12 text-center text-sm text-ink-faint">
              {query ? (
                <>
                  No cards match <span className="text-ink">“{query}”</span>
                  {holderFilter !== "all" && (
                    <> in <span className="text-ink">{HOLDERS[holderFilter].englishName}</span>'s scope</>
                  )}
                  .
                </>
              ) : (
                <>No cards for <span className="text-ink">{holderFilter !== "all" ? HOLDERS[holderFilter].englishName : "this scope"}</span>.</>
              )}
            </div>
          )}
        </div>
      </motion.div>
    </motion.div>
  );
};

const HolderChip = ({
  label,
  count,
  dot,
  accent,
  active,
  onClick,
}: {
  label: string;
  count: number;
  dot: string;
  /** Holder's accent — null for the "All" chip (uses amber). */
  accent: string | null;
  active: boolean;
  onClick: () => void;
}) => {
  const activeStyle =
    active && accent
      ? { borderColor: `${accent}66`, background: `${accent}1a` }
      : undefined;
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={clsx(
        "tap shrink-0 flex items-center gap-2 rounded-full border px-3.5 transition-colors",
        active
          ? accent
            ? "text-ink"
            : "border-amber-200/40 bg-amber-300/[0.08] text-ink"
          : "border-paper-line bg-paper-raised/40 text-ink-dim hover:bg-paper-raised hover:text-ink",
      )}
      style={activeStyle}
    >
      <span
        aria-hidden
        className="h-1.5 w-1.5 shrink-0 rounded-full"
        style={{ background: dot }}
      />
      <span className="text-[12.5px] uppercase tracking-[0.2em]">{label}</span>
      <span className="num text-[12px] text-ink-faint">{count}</span>
    </button>
  );
};

const Group = ({
  title,
  instances,
  selected,
  onPick,
}: {
  title: string;
  instances: CardInstance[];
  selected: CardInstance | null;
  onPick: (i: CardInstance) => void;
}) => (
  <section className="mb-5">
    <div className="mb-2 text-[12px] uppercase tracking-[0.22em] text-ink-faint">
      {title}
    </div>
    <div className="space-y-1.5">
      {instances.map((i) => {
        const c = CARDS[i.cardId];
        const holder = HOLDERS[i.holder];
        const active = selected ? instanceKey(selected) === instanceKey(i) : false;
        return (
          <button
            key={instanceKey(i)}
            onClick={() => onPick(i)}
            className={clsx(
              "tap flex w-full items-center gap-3 rounded-2xl border px-3 py-3 text-left",
              "transition-colors duration-200",
              active
                ? "border-amber-200/60 bg-amber-300/10"
                : "border-paper-line/60 hover:bg-paper-high",
            )}
          >
            <span
              aria-hidden
              className="h-9 w-9 shrink-0 rounded-lg"
              style={{
                background: `linear-gradient(135deg, ${c.brandColors[0]}, ${c.brandColors[1]})`,
              }}
            />
            <div className="min-w-0 flex-1">
              <div className="flex items-baseline gap-2">
                <span className="truncate font-display text-base font-normal tracking-tight text-ink">
                  {c.name}
                </span>
                <span
                  className="shrink-0 text-[12px] uppercase tracking-[0.18em]"
                  style={{ color: holder.accent }}
                >
                  {holder.englishName}
                </span>
              </div>
              <div className="text-[12px] uppercase tracking-[0.18em] text-ink-faint">
                {c.network ?? "—"} · •••• {i.last4}
              </div>
            </div>
            {active && (
              <span className="text-[12px] uppercase tracking-[0.22em] text-amber-glow">
                selected
              </span>
            )}
          </button>
        );
      })}
    </div>
  </section>
);
