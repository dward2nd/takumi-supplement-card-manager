import { motion } from "framer-motion";
import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { daysUntil } from "../data/format";
import { TRANSACTIONS } from "../data/transactions";
import { Amount } from "./Amount";
import { Pill } from "./Pill";
import type { Bill, Transaction } from "../data/types";

/**
 * Categorise a cycle row into one of four buckets. Same rules as
 * `lib.bills._categorize_row` in the Python backend so the POC's visual
 * groups mirror the auto-generated Note. The `[` prefix rule is for
 * adjustment / debt-takeover rows (e.g. `[เว็บรับหนี้ไปบริหารต่อ] …`);
 * names that just start with `(` (like `(FOR SHOPEE)*…`) stay regular.
 */
export type BillTxBucket =
  | "installment"
  | "cashback-credit"
  | "payment"
  | "manual-adjustment"
  | "regular";

// Payment rows are negative-amount transactions whose name is one of the
// `lib.payments` labels (ชำระบิลเต็มจำนวน / ชำระบางส่วน / ชำระบิลล่วงหน้า).
// They offset the cycle to ~zero — distinct from cashback credits and from
// bracket-prefixed manual adjustments. Written by /record-payment (and by
// /update-bill on slip upload).
const PAYMENT_NAME = /ชำระบิล|ชำระบางส่วน|payment/i;

export const categoriseBillTx = (tx: Transaction): BillTxBucket => {
  const name = (tx.name || "").trim();
  if (/CASHBACK/i.test(name)) return "cashback-credit";
  if (tx.installment) return "installment";
  if (tx.amount < 0 && PAYMENT_NAME.test(name)) return "payment";
  if (name.startsWith("[")) return "manual-adjustment";
  if (tx.status === "refunded") return "manual-adjustment";
  if (tx.amount < 0) return "manual-adjustment";
  return "regular";
};

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

  // Per-bucket counts for the faint subline beneath the amount. Visible
  // only when at least one non-regular bucket has rows — the regular case
  // is implied and would just be noise. Mirrors the auto-Note structure
  // in `lib.bills.explain_cycle`.
  const buckets = useMemo(() => {
    const counts = { installment: 0, "cashback-credit": 0, payment: 0, "manual-adjustment": 0 };
    for (const tx of TRANSACTIONS) {
      if (tx.holder !== bill.holder) continue;
      if (tx.cardId !== bill.cardId) continue;
      if (tx.billCycleDate !== bill.billCycleDate) continue;
      const b = categoriseBillTx(tx);
      if (b !== "regular") counts[b] += 1;
    }
    return counts;
  }, [bill.holder, bill.cardId, bill.billCycleDate]);
  const subParts = [
    buckets.installment > 0 ? `${buckets.installment} installment${buckets.installment === 1 ? "" : "s"}` : null,
    buckets["cashback-credit"] > 0
      ? `${buckets["cashback-credit"]} credit${buckets["cashback-credit"] === 1 ? "" : "s"}`
      : null,
    buckets.payment > 0 ? `${buckets.payment} payment${buckets.payment === 1 ? "" : "s"}` : null,
    buckets["manual-adjustment"] > 0
      ? `${buckets["manual-adjustment"]} adjustment${buckets["manual-adjustment"] === 1 ? "" : "s"}`
      : null,
  ].filter((s): s is string => s !== null);

  return (
    <motion.button
      initial={{ opacity: 0, y: 6 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.03 * index, duration: 0.4 }}
      onClick={() => nav(`/bills/${bill.id}`)}
      className="tap group flex w-full flex-col gap-2 rounded-2xl border border-paper-line/70 bg-paper-raised/40 px-4 py-4 text-left transition-colors hover:bg-paper-raised"
    >
      <div className="flex w-full items-center justify-between gap-3">
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
        <Amount value={bill.amount} signed={false} className="shrink-0 text-lg" />
      </div>
      {subParts.length > 0 && (
        <div className="border-t border-paper-line/40 pt-2 text-[10.5px] uppercase tracking-[0.22em] text-ink-faint">
          {subParts.join(" · ")}
        </div>
      )}
    </motion.button>
  );
};
