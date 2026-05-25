import clsx from "clsx";
import { motion } from "framer-motion";
import { CARDS } from "../data/cards";
import { Amount } from "./Amount";
import { Pill } from "./Pill";
import { fmtShort, splitMerchant } from "../data/format";
import { earnedCashback, earnedPoints } from "../data/earnings";
import type { Transaction } from "../data/types";

interface Props {
  tx: Transaction;
  /** When true, hides the per-row card pill (e.g. inside a card-scoped feed). */
  hideCardChip?: boolean;
  onTap?: () => void;
  index?: number;
}

export const TransactionRow = ({ tx, hideCardChip, onTap, index = 0 }: Props) => {
  const card = CARDS[tx.cardId];
  const { headline, tail } = splitMerchant(tx.name);
  const isCredit = tx.amount < 0;
  const isCashbackRow = /cashback/i.test(tx.name);

  // Per-row earnings — same axes whether the row earned points, cashback, or both.
  // null means "this axis doesn't apply" (e.g. UOB One has no points line).
  const pts = isCashbackRow ? null : earnedPoints(tx, card);
  const cb = isCashbackRow ? null : earnedCashback(tx);

  return (
    <motion.button
      onClick={onTap}
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.03, 0.4), duration: 0.4, ease: [0.2, 0.7, 0.1, 1] }}
      className={clsx(
        "tap group block w-full text-left",
        "border-b border-paper-line/60 px-5 py-4 last:border-b-0",
        "transition-colors duration-300",
        onTap && "hover:bg-paper-raised/50 active:bg-paper-raised",
      )}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <div className="flex items-center gap-2">
            <span className="num text-[12px] tracking-[0.14em] text-ink-faint">
              {fmtShort(tx.transactionDate)}
            </span>
            {!hideCardChip && (
              // The chip background is a very translucent brand-colour
              // gradient. Text uses the theme-aware `text-ink-dim` so it
              // reads against either cream (light mode) or warm-dark
              // (dark mode) page background — without that, the
              // hardcoded cream we used to set would vanish on light.
              <span
                className="rounded-full px-2 py-0.5 text-[11px] uppercase tracking-[0.16em] text-ink-dim"
                style={{
                  borderTop: `1px solid ${card.brandColors[0]}55`,
                  background: `linear-gradient(90deg, ${card.brandColors[0]}33, ${card.brandColors[1]}1a)`,
                }}
              >
                {card.name}
              </span>
            )}
            {tx.isInstallment && <Pill tone="ghost">installment</Pill>}
          </div>
          <div className="mt-1.5 truncate font-display text-[15px] leading-tight tracking-tight text-ink">
            {headline}
          </div>
          {tail && (
            <div className="text-[12px] uppercase tracking-[0.18em] text-ink-faint">
              {tail}
            </div>
          )}
          {tx.note && (
            <div className="mt-1 line-clamp-2 max-w-[26ch] text-[13px] leading-snug text-ink-faint">
              {tx.note}
            </div>
          )}
        </div>

        <div className="flex shrink-0 flex-col items-end gap-1.5">
          <Amount
            value={tx.amount}
            tone={isCredit ? "credit" : "default"}
            className={clsx(isCashbackRow && "font-medium", "text-base")}
          />

          {/* Per-row earnings — only render axes that apply to this card/row. */}
          {(pts !== null || cb !== null) && (
            <div className="flex items-center gap-3">
              {pts !== null && (
                <Earned
                  label="pts"
                  value={pts > 0 ? pts.toLocaleString("en-US") : "—"}
                  tone={pts > 0 ? "default" : "muted"}
                />
              )}
              {cb !== null && cb > 0 && (
                <Earned
                  label="cb"
                  value={`฿${cb.toFixed(2)}`}
                  tone="credit"
                />
              )}
            </div>
          )}
        </div>
      </div>
    </motion.button>
  );
};

const Earned = ({
  label,
  value,
  tone,
}: {
  label: string;
  value: string;
  tone: "default" | "credit" | "muted";
}) => (
  <div className="flex flex-col items-end leading-none">
    <span
      className={clsx(
        "num text-[12px]",
        tone === "default" && "text-ink",
        tone === "credit" && "text-teal-400",
        tone === "muted" && "text-ink-ghost",
      )}
    >
      {value}
    </span>
    <span className="mt-0.5 text-[10.5px] uppercase tracking-[0.22em] text-ink-faint">
      {label}
    </span>
  </div>
);
