import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Check, FileText, Image as ImageIcon, Upload } from "lucide-react";
import { BILLS } from "../data/bills";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { TRANSACTIONS } from "../data/transactions";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import { TransactionRow } from "../components/TransactionRow";
import { CardFace } from "../components/CardFace";

export const BillDetailScreen = () => {
  const { id } = useParams();
  const bill = BILLS.find((b) => b.id === id);
  const [paid, setPaid] = useState(bill?.status === "paid");
  const [draftStripped, setDraftStripped] = useState(!bill?.isDraft);

  if (!bill) return null;
  const card = CARDS[bill.cardId];
  const holder = HOLDERS[bill.holder];

  const cycleTxs = useMemo(
    () =>
      TRANSACTIONS.filter(
        (t) => t.holder === bill.holder && t.cardId === bill.cardId && t.billCycleDate === bill.billCycleDate,
      ).sort((a, b) => a.transactionDate.localeCompare(b.transactionDate)),
    [bill],
  );

  const subtotal = cycleTxs.reduce((s, t) => s + (t.amount > 0 ? t.amount : 0), 0);
  const credits = cycleTxs.reduce((s, t) => s + (t.amount < 0 ? t.amount : 0), 0);

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title={`${card.name} · ${bill.billCycleDate.slice(0, 7)}`}
        eyebrow={`${holder.englishName} · cycle ${bill.billCycleDate}`}
        back
      />

      {/*
        lg+: left column (summary stack — card face + bill total + actions)
        sticky alongside a right column with the line items list. Below lg,
        falls back to the original vertical stack.
      */}
      <div className="lg:grid lg:grid-cols-12 lg:gap-10 lg:px-5">
        <div className="lg:col-span-5 lg:sticky lg:top-6 lg:self-start">
          <div className="px-5 lg:px-0">
            <CardFace card={card} holder={bill.holder} />
          </div>

          <section className="mx-5 mt-5 rounded-3xl border border-paper-line bg-paper-raised/60 p-5 lg:mx-0">
            <div className="flex items-baseline justify-between text-[12px] uppercase tracking-[0.22em] text-ink-faint">
              <span>{draftStripped ? "billed amount" : "draft total"}</span>
              <div className="flex gap-1.5">
                {!draftStripped && <Pill tone="amber" uppercase>draft</Pill>}
                {paid && <Pill tone="teal" uppercase>paid</Pill>}
              </div>
            </div>
            <Amount value={bill.amount} signed={false} size="xl" className="mt-2 text-ink" symbol />

            <div className="mt-4 grid grid-cols-2 gap-3 text-[13px]">
              <div>
                <div className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">gross</div>
                <Amount value={subtotal} signed={false} size="sm" className="mt-1" />
              </div>
              <div>
                <div className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">credits</div>
                <Amount value={credits} size="sm" className="mt-1" tone="credit" />
              </div>
            </div>
          </section>

          {/* Actions */}
          <section className="mx-5 mt-6 space-y-2 lg:mx-0">
            {!draftStripped && (
              <motion.button
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => setDraftStripped(true)}
                className="tap flex w-full items-center justify-between gap-3 rounded-2xl border border-amber-200/30 bg-amber-300/[0.05] px-4 py-4 text-left transition-colors hover:bg-amber-300/[0.08]"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-full border border-amber-200/40 bg-amber-200/10">
                    <Upload size={16} className="text-amber-glow" />
                  </span>
                  <div>
                    <div className="font-display text-sm tracking-tight text-ink">Upload statement PDF</div>
                    <div className="text-[12px] uppercase tracking-[0.16em] text-ink-faint">
                      strips the draft prefix
                    </div>
                  </div>
                </div>
                <span className="text-[12px] uppercase tracking-[0.22em] text-amber-glow">attach →</span>
              </motion.button>
            )}
            {!paid && (
              <motion.button
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => setPaid(true)}
                className="tap flex w-full items-center justify-between gap-3 rounded-2xl border border-teal-400/30 bg-teal-400/[0.05] px-4 py-4 text-left transition-colors hover:bg-teal-400/[0.08]"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-9 w-9 items-center justify-center rounded-full border border-teal-400/40 bg-teal-400/10">
                    <Check size={16} className="text-teal-400" />
                  </span>
                  <div>
                    <div className="font-display text-sm tracking-tight text-ink">Mark as paid</div>
                    <div className="text-[12px] uppercase tracking-[0.16em] text-ink-faint">
                      attach the transfer slip
                    </div>
                  </div>
                </div>
                <span className="text-[12px] uppercase tracking-[0.22em] text-teal-400">confirm →</span>
              </motion.button>
            )}
            {paid && (
              <div className="flex items-center justify-between rounded-2xl border border-teal-400/30 bg-teal-400/[0.06] px-4 py-3 text-[13px]">
                <div className="flex items-center gap-2 text-teal-400">
                  <Check size={14} /> Marked paid on {bill.paidAt ?? "today"}
                </div>
                <div className="flex gap-2 text-ink-faint">
                  {bill.hasSlip && <ImageIcon size={14} />}
                  {bill.hasStatementPdf && <FileText size={14} />}
                </div>
              </div>
            )}
          </section>
        </div>

        <div className="lg:col-span-7">
          <section className="mt-8 px-5 pb-10 lg:mt-0 lg:px-0">
            <SectionLabel number="01" trailing={`${cycleTxs.length} rows`}>
              Line items
            </SectionLabel>
            <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
              {cycleTxs.map((t, i) => (
                <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
              ))}
            </div>
          </section>
        </div>
      </div>
    </div>
  );
};
