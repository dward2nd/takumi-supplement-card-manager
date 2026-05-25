import clsx from "clsx";
import { motion } from "framer-motion";
import { CARDS } from "../data/cards";
import { Amount } from "./Amount";
import { Pill } from "./Pill";
import { fmtRate, fmtShort, splitMerchant } from "../data/format";
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
            <span className="num text-[10px] tracking-[0.14em] text-ink-faint">
              {fmtShort(tx.transactionDate)}
            </span>
            {!hideCardChip && (
              <span
                className="rounded-full px-2 py-0.5 text-[9px] uppercase tracking-[0.16em]"
                style={{
                  borderTop: `1px solid ${card.brandColors[0]}55`,
                  background: `linear-gradient(90deg, ${card.brandColors[0]}1f, ${card.brandColors[1]}0f)`,
                  color: "#f2ebdd",
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
            <div className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
              {tail}
            </div>
          )}
          {tx.note && (
            <div className="mt-1 line-clamp-2 max-w-[26ch] text-[11px] leading-snug text-ink-faint">
              {tx.note}
            </div>
          )}
        </div>

        <div className="flex shrink-0 flex-col items-end gap-1">
          <Amount
            value={tx.amount}
            tone={isCredit ? "credit" : "default"}
            className={clsx(isCashbackRow && "font-medium", "text-base")}
          />
          <div className="flex items-center gap-1">
            {tx.cashbackPercent !== undefined && (
              <Pill tone="amber" uppercase={false}>
                {fmtRate(tx.cashbackPercent)} cb
              </Pill>
            )}
            {tx.multiplier === "×0" && !isCashbackRow && (
              <Pill tone="ghost" uppercase={false}>
                ×0
              </Pill>
            )}
          </div>
        </div>
      </div>
    </motion.button>
  );
};
