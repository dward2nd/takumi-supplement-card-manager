import { motion } from "framer-motion";
import { useNavigate } from "react-router-dom";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { daysUntil } from "../data/format";
import { Amount } from "./Amount";
import { Pill } from "./Pill";
import type { Bill } from "../data/types";

/**
 * Bill-row tile — used in BillsScreen's groups and BillsHistoryScreen's
 * archive grid. Renders the card chip, name, status pill, cycle / paid
 * date, holder, and the amount.
 */
export const BillRow = ({ bill, index = 0 }: { bill: Bill; index?: number }) => {
  const nav = useNavigate();
  const card = CARDS[bill.cardId];
  const today = new Date("2026-05-26");
  const dueDate =
    bill.billCycleDate === "2026-05-25" ? "2026-06-15" : bill.billCycleDate;
  const days = daysUntil(dueDate, today);
  const paid = bill.status === "paid";

  return (
    <motion.button
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.03 * index, duration: 0.4 }}
      onClick={() => nav(`/bills/${bill.id}`)}
      className="tap group flex w-full items-center justify-between gap-3 rounded-2xl border border-paper-line/70 bg-paper-raised/40 px-4 py-4 text-left transition-colors hover:bg-paper-raised"
    >
      <div className="flex min-w-0 items-center gap-3">
        <span
          aria-hidden
          className="h-12 w-12 shrink-0 rounded-xl"
          style={{
            background: `linear-gradient(135deg, ${card.brandColors[0]}, ${card.brandColors[1]})`,
          }}
        />
        <div className="min-w-0">
          <div className="flex items-center gap-2">
            <span className="truncate font-display text-[15px] font-normal text-ink">
              {card.name}
            </span>
            {bill.isDraft && (
              <Pill tone="amber" uppercase>
                draft
              </Pill>
            )}
            {paid && (
              <Pill tone="teal" uppercase>
                paid
              </Pill>
            )}
          </div>
          <div className="text-[12px] uppercase tracking-[0.16em] text-ink-faint">
            cycle {bill.billCycleDate}{" "}
            {bill.isDraft ? (
              <>
                · due in <span className="num text-ink-dim">{days}</span> days
              </>
            ) : paid && bill.paidAt ? (
              <>· paid {bill.paidAt}</>
            ) : null}
          </div>
          <div className="text-[12px] uppercase tracking-[0.16em] text-ink-ghost">
            {HOLDERS[bill.holder].englishName} · {HOLDERS[bill.holder].thaiName}
          </div>
        </div>
      </div>
      <Amount value={bill.amount} signed={false} className="text-lg" />
    </motion.button>
  );
};
