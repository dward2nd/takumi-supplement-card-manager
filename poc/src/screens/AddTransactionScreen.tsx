import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";
import { motion, AnimatePresence } from "framer-motion";
import { Check, X, Plus, Trash2, History } from "lucide-react";
import { useApp } from "../data/state";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { visibleInstances, instanceKey } from "../data/card-instances";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { CardPicker } from "../components/CardPicker";
import { activePromotionsFor } from "../data/promotions";
import { fmtRate, splitMerchant } from "../data/format";
import { frequentMerchants } from "../data/merchant-history";
import type { CardInstance } from "../data/types";
import clsx from "clsx";

/**
 * Card-grouped entry surface.
 *
 *   ┌─ Card picker (one instance) ──────────┐
 *   │  Row 1: merchant + amount             │
 *   │  Row 2: merchant + amount             │
 *   │  [+ another for this card]            │
 *   └───────────────────────────────────────┘
 *   ┌─ Card picker (another instance) ──────┐
 *   │  …                                    │
 *   └───────────────────────────────────────┘
 *   [+ another card]
 *
 * Picking the card is the *expensive* tap; the row list under it is cheap.
 * Multiple groups support batching across cards in one session.
 */

interface DraftRow {
  id: string;
  name: string;
  amount: string;
}

interface CardGroup {
  id: string;
  instance: CardInstance | null;
  rows: DraftRow[];
}

const emptyRow = (): DraftRow => ({
  id: crypto.randomUUID(),
  name: "",
  amount: "",
});

const emptyGroup = (instance: CardInstance | null = null): CardGroup => ({
  id: crypto.randomUUID(),
  instance,
  rows: [emptyRow()],
});

export const AddTransactionScreen = () => {
  const { holderKey: viewerKey } = useApp();
  const nav = useNavigate();
  const today = "2026-05-26";

  const allInstances = useMemo(
    () => (viewerKey ? visibleInstances(viewerKey) : []),
    [viewerKey],
  );

  const [groups, setGroups] = useState<CardGroup[]>([emptyGroup()]);
  // Most-recent-first list of instance keys, for the picker's "Recent" group.
  const [recents, setRecents] = useState<string[]>([]);

  const touchInstance = (i: CardInstance) => {
    const k = instanceKey(i);
    setRecents((r) => [k, ...r.filter((x) => x !== k)].slice(0, 6));
  };

  const setInstance = (groupId: string, inst: CardInstance) => {
    touchInstance(inst);
    setGroups((gs) => gs.map((g) => (g.id === groupId ? { ...g, instance: inst } : g)));
  };

  const updateRow = (groupId: string, rowId: string, patch: Partial<DraftRow>) => {
    setGroups((gs) =>
      gs.map((g) =>
        g.id !== groupId ? g : { ...g, rows: g.rows.map((r) => (r.id === rowId ? { ...r, ...patch } : r)) },
      ),
    );
  };

  const removeRow = (groupId: string, rowId: string) => {
    setGroups((gs) =>
      gs.map((g) => {
        if (g.id !== groupId) return g;
        if (g.rows.length === 1) return g;
        return { ...g, rows: g.rows.filter((r) => r.id !== rowId) };
      }),
    );
  };

  const addRow = (groupId: string) => {
    setGroups((gs) =>
      gs.map((g) => (g.id !== groupId ? g : { ...g, rows: [...g.rows, emptyRow()] })),
    );
  };

  const applyMerchantChip = (groupId: string, name: string) => {
    setGroups((gs) =>
      gs.map((g) => {
        if (g.id !== groupId) return g;
        const blank = g.rows.find((r) => !r.name.trim());
        if (blank) {
          return { ...g, rows: g.rows.map((r) => (r.id === blank.id ? { ...r, name } : r)) };
        }
        return { ...g, rows: [...g.rows, { ...emptyRow(), name }] };
      }),
    );
  };

  const addGroup = () => setGroups((gs) => [...gs, emptyGroup()]);
  const removeGroup = (gid: string) =>
    setGroups((gs) => (gs.length === 1 ? gs : gs.filter((g) => g.id !== gid)));

  const totalCount = groups.reduce((s, g) => s + g.rows.length, 0);
  const total = groups.reduce(
    (s, g) => s + g.rows.reduce((rs, r) => rs + (Number(r.amount) || 0), 0),
    0,
  );
  const valid = groups.every(
    (g) => g.instance && g.rows.every((r) => r.name.trim() && Number(r.amount) > 0),
  );

  const handleSave = () => {
    nav("/home");
  };

  return (
    <div className="top-safe relative mx-auto max-w-md px-5 pb-12 md:max-w-3xl lg:max-w-5xl">
      <div className="flex items-center justify-between">
        <button
          onClick={() => nav(-1)}
          className="tap -ml-2 flex items-center gap-1 rounded-full px-2 py-1 text-ink-dim"
          aria-label="close"
        >
          <X size={16} strokeWidth={1.5} />
          <span className="text-xs uppercase tracking-[0.18em]">cancel</span>
        </button>
        <span className="text-[12px] uppercase tracking-[0.22em] text-ink-faint">
          {today}
        </span>
      </div>

      <div className="mt-6">
        <div className="text-[12px] uppercase tracking-[0.28em] text-amber-glow/90">
          record · spend journal
        </div>
        <h1 className="mt-2 font-display text-3xl font-normal leading-tight tracking-tight text-ink">
          What did you <em className="italic font-normal text-amber-glow">spend</em>?
        </h1>
        <p className="mt-2 text-xs text-ink-dim">
          Type merchant names <span className="text-ink">verbatim</span> — exactly as on the bank statement. Tap a recent-merchant chip to autofill from history. Group multiple transactions per card.
        </p>
      </div>

      {/*
        lg+: editors take the left two-thirds; batch-total + save sits as a
        sticky side panel on the right. Below lg, falls back to the original
        vertical stack with the panel sticky at the bottom on md.
      */}
      <div className="mt-6 lg:grid lg:grid-cols-12 lg:gap-8">
        <div className="space-y-4 lg:col-span-7">
          <AnimatePresence initial={false}>
            {groups.map((g, gi) => (
              <CardGroupEditor
                key={g.id}
                group={g}
                index={gi}
                instances={allInstances}
                recents={recents}
                onSetInstance={(i) => setInstance(g.id, i)}
                onUpdateRow={(rid, patch) => updateRow(g.id, rid, patch)}
                onRemoveRow={(rid) => removeRow(g.id, rid)}
                onAddRow={() => addRow(g.id)}
                onApplyMerchant={(name) => applyMerchantChip(g.id, name)}
                onRemoveGroup={() => removeGroup(g.id)}
                canRemoveGroup={groups.length > 1}
              />
            ))}
          </AnimatePresence>

          <button
            onClick={addGroup}
            className="tap flex w-full items-center justify-center gap-2 rounded-2xl border border-dashed border-paper-line py-3 text-[13px] uppercase tracking-[0.22em] text-ink-faint transition-colors hover:border-amber-200/50 hover:text-amber-glow"
          >
            <Plus size={14} /> add another card
          </button>
        </div>

        <div className="lg:col-span-5">
          <div className="mt-8 rounded-3xl border border-paper-line bg-paper-raised/60 p-5 md:sticky md:bottom-4 lg:mt-0 lg:sticky lg:top-6 lg:self-start lg:bottom-auto">
            <div className="flex items-baseline justify-between">
              <div>
                <div className="text-[12px] uppercase tracking-[0.22em] text-ink-faint">
                  batch total · {totalCount} {totalCount === 1 ? "row" : "rows"} across {groups.length} {groups.length === 1 ? "card" : "cards"}
                </div>
              </div>
              <Amount value={total} signed={false} size="lg" className="text-ink" />
            </div>

            <button
              onClick={handleSave}
              disabled={!valid}
              className={clsx(
                "tap mt-4 flex w-full items-center justify-center gap-2 rounded-2xl py-4 text-sm uppercase tracking-[0.22em]",
                "transition-all duration-300",
                valid
                  ? "bg-gradient-to-r from-amber-200 to-amber-300 text-on-accent shadow-glow-amber hover:scale-[1.005]"
                  : "border border-paper-line bg-paper-raised text-ink-faint",
              )}
            >
              <Check size={16} strokeWidth={2.4} /> save {totalCount > 1 ? `${totalCount} rows` : "transaction"}
            </button>
            <div className="mt-3 text-center text-[12px] uppercase tracking-[0.22em] text-ink-faint">
              POC · save is mocked, won't persist
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

const CardGroupEditor = ({
  group,
  index,
  instances,
  recents,
  onSetInstance,
  onUpdateRow,
  onRemoveRow,
  onAddRow,
  onApplyMerchant,
  onRemoveGroup,
  canRemoveGroup,
}: {
  group: CardGroup;
  index: number;
  instances: CardInstance[];
  recents: string[];
  onSetInstance: (i: CardInstance) => void;
  onUpdateRow: (rid: string, patch: Partial<DraftRow>) => void;
  onRemoveRow: (rid: string) => void;
  onAddRow: () => void;
  onApplyMerchant: (name: string) => void;
  onRemoveGroup: () => void;
  canRemoveGroup: boolean;
}) => {
  const card = group.instance ? CARDS[group.instance.cardId] : null;
  const holder = group.instance ? HOLDERS[group.instance.holder] : null;

  // Recent merchants scoped to the *selected card-instance's holder* —
  // distinguish by who actually swiped the supplement.
  const merchantChips = useMemo(() => {
    if (!group.instance) return [];
    return frequentMerchants(group.instance.holder, group.instance.cardId, 8);
  }, [group.instance]);

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
        <span className="num text-[12px] tracking-[0.16em] text-ink-faint">
          card · {String(index + 1).padStart(2, "0")}
        </span>
        {canRemoveGroup && (
          <button
            onClick={onRemoveGroup}
            className="tap rounded-full p-1 text-ink-faint hover:text-coral-400"
            aria-label="remove card group"
          >
            <Trash2 size={14} />
          </button>
        )}
      </div>

      <div className="p-4 space-y-3">
        <CardPicker
          selected={group.instance}
          instances={instances}
          recents={recents}
          onChange={onSetInstance}
        />

        {card && merchantChips.length > 0 && (
          <div>
            <div className="mb-1.5 flex items-center gap-1.5 text-[12px] uppercase tracking-[0.22em] text-ink-faint">
              <History size={11} strokeWidth={1.6} />
              recent on {card.name}
              {holder && (
                <span style={{ color: holder.accent }}>· {holder.englishName}</span>
              )}
            </div>
            <div className="-mx-1 flex gap-2 overflow-x-auto px-1 pb-1" style={{ scrollbarWidth: "none" }}>
              {merchantChips.map((m) => {
                const { headline } = splitMerchant(m.name);
                const display = headline.length > 22 ? headline.slice(0, 22) + "…" : headline;
                return (
                  <button
                    key={m.name}
                    onClick={() => onApplyMerchant(m.name)}
                    className={clsx(
                      "shrink-0 whitespace-nowrap rounded-full border px-3 py-1.5 text-[13px]",
                      "min-h-[34px] touch-manipulation select-none",
                      "border-paper-line bg-paper-raised text-ink-dim transition-colors hover:border-amber-200/40",
                    )}
                    title={`Used ${m.count}× · last seen ${m.lastUsed}`}
                  >
                    {display}
                    <span className="ml-1.5 text-ink-faint">·</span>
                    <span className="ml-1.5 num text-[12px] text-ink-faint">{m.count}×</span>
                  </button>
                );
              })}
            </div>
          </div>
        )}

        {/* Row table */}
        <div className="rounded-xl border border-paper-line/60 bg-paper/30">
          {group.rows.map((r, ri) => (
            <RowFields
              key={r.id}
              row={r}
              rowIndex={ri}
              instance={group.instance}
              onChange={(patch) => onUpdateRow(r.id, patch)}
              onRemove={() => onRemoveRow(r.id)}
              canRemove={group.rows.length > 1}
            />
          ))}
          <button
            onClick={onAddRow}
            className="tap flex w-full items-center justify-center gap-1.5 border-t border-paper-line/40 py-2.5 text-[12px] uppercase tracking-[0.22em] text-ink-faint transition-colors hover:bg-paper-raised/30 hover:text-amber-glow"
          >
            <Plus size={12} /> another row on {card?.name ?? "this card"}
          </button>
        </div>
      </div>
    </motion.div>
  );
};

const RowFields = ({
  row,
  rowIndex,
  instance,
  onChange,
  onRemove,
  canRemove,
}: {
  row: DraftRow;
  rowIndex: number;
  instance: CardInstance | null;
  onChange: (patch: Partial<DraftRow>) => void;
  onRemove: () => void;
  canRemove: boolean;
}) => {
  const classification = useMemo(() => {
    if (!instance || !row.name.trim()) return null;
    const promos = activePromotionsFor(instance.cardId, "2026-05-26");
    if (promos.length === 0) return null;
    const promo = promos[0];
    const upper = row.name.toUpperCase();
    const tokens = row.name.trim().split(/\s+/);
    const foreign =
      tokens.length > 0 &&
      /^[A-Z]{2,3}$/.test(tokens[tokens.length - 1] ?? "") &&
      tokens[tokens.length - 1] !== "TH";
    if (foreign && promo.foreignInThbPolicy.default === "exclude") {
      for (const o of promo.foreignInThbPolicy.overrides) {
        if (upper.includes(o.merchantSubstring.toUpperCase())) {
          return { rate: o.rate, reason: "foreign override", tone: "amber" as const };
        }
      }
      return { rate: null, reason: "foreign-in-THB · no cashback", tone: "coral" as const };
    }
    for (const t of promo.tiers) {
      const matches = t.patterns.some((p) => p === "*" || upper.includes(p.toUpperCase()));
      if (!matches) continue;
      const excluded = (t.excludePatterns ?? []).some((p) =>
        upper.includes(p.toUpperCase()),
      );
      if (excluded) continue;
      return {
        rate: t.rate,
        reason: t.label ?? "tier",
        tone: t.rate >= 0.05 ? ("amber" as const) : ("neutral" as const),
      };
    }
    return null;
  }, [instance, row.name]);

  return (
    <div className="border-b border-paper-line/40 last:border-b-0 px-3 py-2.5">
      <div className="grid grid-cols-[auto_1fr_auto_auto] items-center gap-2">
        <span className="num text-[12px] text-ink-faint">
          {String(rowIndex + 1).padStart(2, "0")}
        </span>
        <input
          type="text"
          value={row.name}
          onChange={(e) => onChange({ name: e.target.value })}
          placeholder="VERBATIM MERCHANT BANGKOK TH"
          className="w-full min-w-0 rounded-lg border border-paper-line bg-paper px-2.5 py-2 text-[13px] font-mono uppercase tracking-wider text-ink placeholder:text-ink-ghost focus:border-amber-200/60 focus:outline-none"
        />
        <input
          type="number"
          inputMode="decimal"
          value={row.amount}
          onChange={(e) => onChange({ amount: e.target.value })}
          placeholder="0.00"
          className="num w-24 rounded-lg border border-paper-line bg-paper px-2.5 py-2 text-right text-[13px] text-ink placeholder:text-ink-ghost focus:border-amber-200/60 focus:outline-none"
        />
        {canRemove ? (
          <button
            onClick={onRemove}
            className="tap rounded-full p-1 text-ink-faint hover:text-coral-400"
            aria-label="remove row"
          >
            <Trash2 size={14} />
          </button>
        ) : (
          <span className="w-[28px]" />
        )}
      </div>

      <div className="mt-1.5 ml-7 flex items-center justify-between text-[12px] uppercase tracking-[0.16em] text-ink-faint">
        <span className="text-ink-ghost">auto-classify</span>
        {classification ? (
          classification.rate !== null ? (
            <Pill tone={classification.tone} uppercase={false}>
              {fmtRate(classification.rate)} · {classification.reason}
            </Pill>
          ) : (
            <Pill tone="coral" uppercase={false}>
              {classification.reason}
            </Pill>
          )
        ) : instance && row.name.trim() ? (
          <span className="text-ink-ghost">no match</span>
        ) : (
          <span className="text-ink-ghost">—</span>
        )}
      </div>
    </div>
  );
};
