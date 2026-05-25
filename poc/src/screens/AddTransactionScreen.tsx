import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, Plus, Trash2 } from "lucide-react";
import { useApp } from "../data/state";
import { cardsForHolder, CARDS } from "../data/cards";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { activePromotionsFor } from "../data/promotions";
import { fmtRate } from "../data/format";
import type { CardId } from "../data/types";
import clsx from "clsx";

interface DraftRow {
  id: string;
  cardId: CardId | null;
  name: string;
  amount: string;
}

/**
 * The bread-and-butter screen. Designed as a *mini-table* the user types into.
 * One-row entry by default; tap "+ row" to add bulk rows. Verbatim merchant
 * preservation is the entire point — no normalisation.
 */
export const AddTransactionScreen = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  const today = "2026-05-26";

  const myCards = useMemo(() => (holderKey ? cardsForHolder(holderKey) : []), [holderKey]);

  const [rows, setRows] = useState<DraftRow[]>([
    { id: crypto.randomUUID(), cardId: null, name: "", amount: "" },
  ]);

  const updateRow = (id: string, patch: Partial<DraftRow>) => {
    setRows((r) => r.map((row) => (row.id === id ? { ...row, ...patch } : row)));
  };

  const removeRow = (id: string) => {
    setRows((r) => (r.length === 1 ? r : r.filter((row) => row.id !== id)));
  };

  const addRow = () =>
    setRows((r) => [...r, { id: crypto.randomUUID(), cardId: r[r.length - 1]?.cardId ?? null, name: "", amount: "" }]);

  const valid = rows.every((r) => r.cardId && r.name.trim() && Number(r.amount) > 0);

  const total = rows.reduce((s, r) => s + (Number(r.amount) || 0), 0);

  const handleSave = () => {
    // POC: just bounce home. In a real build this'd persist.
    nav("/home");
  };

  return (
    <div className="top-safe relative px-5 pb-12">
      <div className="flex items-center justify-between">
        <button
          onClick={() => nav(-1)}
          className="tap -ml-2 flex items-center gap-1 rounded-full px-2 py-1 text-ink-dim"
          aria-label="close"
        >
          <X size={16} strokeWidth={1.5} />
          <span className="text-xs uppercase tracking-[0.18em]">cancel</span>
        </button>
        <span className="text-[10px] uppercase tracking-[0.22em] text-ink-faint">
          {today}
        </span>
      </div>

      <div className="mt-6">
        <div className="text-[10px] uppercase tracking-[0.28em] text-amber-glow/90">
          record · spend journal
        </div>
        <h1 className="mt-2 font-display text-3xl font-light leading-tight tracking-tight text-ink">
          What did you <em className="italic font-thin text-amber-glow">spend</em>?
        </h1>
        <p className="mt-2 text-xs text-ink-dim">
          Type merchant names <span className="text-ink">verbatim</span> — exactly as they appear on the bank statement. Tap <span className="text-amber-glow">+ row</span> to bulk-add.
        </p>
      </div>

      {/* Rows */}
      <div className="mt-6 space-y-3">
        <AnimatePresence initial={false}>
          {rows.map((r, i) => (
            <RowEditor
              key={r.id}
              row={r}
              index={i}
              cards={myCards.map((c) => c.id)}
              onChange={(patch) => updateRow(r.id, patch)}
              onRemove={() => removeRow(r.id)}
              canRemove={rows.length > 1}
            />
          ))}
        </AnimatePresence>

        <button
          onClick={addRow}
          className="tap flex w-full items-center justify-center gap-2 rounded-2xl border border-dashed border-paper-line py-3 text-[11px] uppercase tracking-[0.22em] text-ink-faint transition-colors hover:border-amber-200/50 hover:text-amber-glow"
        >
          <Plus size={14} /> add row
        </button>
      </div>

      {/* Totals + save */}
      <div className="mt-8 rounded-3xl border border-paper-line bg-paper-raised/60 p-5">
        <div className="flex items-baseline justify-between">
          <span className="text-[10px] uppercase tracking-[0.22em] text-ink-faint">
            batch total
          </span>
          <Amount value={total} signed={false} size="lg" className="text-ink" />
        </div>

        <button
          onClick={handleSave}
          disabled={!valid}
          className={clsx(
            "tap mt-4 flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-sm uppercase tracking-[0.22em]",
            "transition-all duration-300",
            valid
              ? "bg-gradient-to-r from-amber-200 to-amber-300 text-paper shadow-glow-amber hover:scale-[1.01]"
              : "border border-paper-line bg-paper-raised text-ink-faint",
          )}
        >
          <Check size={16} strokeWidth={2.4} /> save {rows.length > 1 ? `${rows.length} rows` : "transaction"}
        </button>
        <div className="mt-3 text-center text-[10px] uppercase tracking-[0.22em] text-ink-faint">
          POC · save is mocked, won't persist
        </div>
      </div>
    </div>
  );
};

const RowEditor = ({
  row,
  index,
  cards,
  onChange,
  onRemove,
  canRemove,
}: {
  row: DraftRow;
  index: number;
  cards: CardId[];
  onChange: (patch: Partial<DraftRow>) => void;
  onRemove: () => void;
  canRemove: boolean;
}) => {
  // Live preview of the classification for the typed merchant.
  const card = row.cardId ? CARDS[row.cardId] : null;
  const classification = useMemo(() => {
    if (!card || !row.name.trim()) return null;
    const promos = activePromotionsFor(card.id, "2026-05-26");
    if (promos.length === 0) return null;
    const promo = promos[0];
    const upper = row.name.toUpperCase();
    // 1) Foreign-in-THB?
    const tokens = row.name.trim().split(/\s+/);
    const foreign = tokens.length > 0 && /^[A-Z]{2,3}$/.test(tokens[tokens.length - 1] ?? "") &&
      tokens[tokens.length - 1] !== "TH";
    if (foreign && promo.foreignInThbPolicy.default === "exclude") {
      for (const o of promo.foreignInThbPolicy.overrides) {
        if (upper.includes(o.merchantSubstring.toUpperCase())) {
          return { rate: o.rate, reason: "foreign override", tone: "amber" as const };
        }
      }
      return { rate: null, reason: "foreign-in-THB · no cashback", tone: "coral" as const };
    }
    // 2) Tiers
    for (const t of promo.tiers) {
      const matches = t.patterns.some((p) => p === "*" || upper.includes(p.toUpperCase()));
      if (!matches) continue;
      const excluded = (t.excludePatterns ?? []).some((p) => upper.includes(p.toUpperCase()));
      if (excluded) continue;
      return { rate: t.rate, reason: t.label ?? "tier", tone: t.rate >= 0.05 ? ("amber" as const) : ("neutral" as const) };
    }
    return null;
  }, [card, row.name]);

  return (
    <motion.div
      layout
      initial={{ opacity: 0, height: 0 }}
      animate={{ opacity: 1, height: "auto" }}
      exit={{ opacity: 0, height: 0 }}
      transition={{ duration: 0.35, ease: [0.2, 0.7, 0.1, 1] }}
      className="overflow-hidden rounded-2xl border border-paper-line bg-paper-raised/40"
    >
      <div className="flex items-center justify-between border-b border-paper-line/60 px-4 py-2.5">
        <span className="num text-[10px] tracking-[0.16em] text-ink-faint">
          row · {String(index + 1).padStart(2, "0")}
        </span>
        {canRemove && (
          <button
            onClick={onRemove}
            className="tap rounded-full p-1 text-ink-faint hover:text-coral-400"
            aria-label="remove row"
          >
            <Trash2 size={14} />
          </button>
        )}
      </div>

      <div className="p-4 space-y-3">
        {/* Card pills — horizontal scroll for many cards */}
        <div className="-mx-1 flex gap-2 overflow-x-auto pb-1 px-1" style={{ scrollbarWidth: "none" }}>
          {cards.map((cid) => {
            const c = CARDS[cid];
            const active = row.cardId === cid;
            return (
              <button
                key={cid}
                onClick={() => onChange({ cardId: cid })}
                className={clsx(
                  "shrink-0 whitespace-nowrap rounded-full border px-4 py-2 text-[11px] uppercase tracking-[0.14em]",
                  "min-h-[36px] touch-manipulation select-none",
                  "transition-colors duration-200",
                  active
                    ? "border-amber-200/60 bg-amber-300/15 text-amber-100"
                    : "border-paper-line bg-paper-raised text-ink-dim hover:border-paper-line/40",
                )}
              >
                {c.name}
              </button>
            );
          })}
        </div>

        {/* Merchant + amount */}
        <div className="grid grid-cols-[1fr_auto] gap-3">
          <input
            type="text"
            value={row.name}
            onChange={(e) => onChange({ name: e.target.value })}
            placeholder="VERBATIM MERCHANT BANGKOK TH"
            className="w-full rounded-xl border border-paper-line bg-paper px-3 py-3 text-sm font-mono uppercase tracking-wider text-ink placeholder:text-ink-ghost focus:border-amber-200/60 focus:outline-none"
          />
          <input
            type="number"
            inputMode="decimal"
            value={row.amount}
            onChange={(e) => onChange({ amount: e.target.value })}
            placeholder="0.00"
            className="num w-28 rounded-xl border border-paper-line bg-paper px-3 py-3 text-right text-sm text-ink placeholder:text-ink-ghost focus:border-amber-200/60 focus:outline-none"
          />
        </div>

        {/* Live classification preview */}
        <div className="flex items-center justify-between text-[10px] uppercase tracking-[0.18em] text-ink-faint">
          <span>auto-classify preview</span>
          {classification ? (
            classification.rate !== null ? (
              <Pill tone={classification.tone} uppercase={false}>
                {fmtRate(classification.rate)} · {classification.reason}
              </Pill>
            ) : (
              <Pill tone="coral" uppercase={false}>{classification.reason}</Pill>
            )
          ) : card && row.name.trim() ? (
            <Pill tone="ghost">no match</Pill>
          ) : (
            <span className="text-ink-ghost">awaiting input</span>
          )}
        </div>
      </div>
    </motion.div>
  );
};
