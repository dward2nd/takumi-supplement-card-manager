import { useMemo, useState } from "react";
import { useParams } from "react-router-dom";
import { motion } from "framer-motion";
import { Check, FileText, Image as ImageIcon, Landmark, Upload } from "lucide-react";
import { BILLS, statementLinesFor } from "../data/bills";
import { useApp } from "../data/state";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { TRANSACTIONS } from "../data/transactions";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import { TransactionRow } from "../components/TransactionRow";
import { CardFace } from "../components/CardFace";
import { BreakdownStrip, breakdownParts, categoriseBillTx, type BillTxBucket } from "../components/BillRow";
import type { Bill, Transaction } from "../data/types";

export const BillDetailScreen = () => {
  const { id } = useParams();
  const { holderKey: viewerKey } = useApp();
  const bill = BILLS.find((b) => b.id === id);
  const [paid, setPaid] = useState(bill?.status === "paid");
  const [draftStripped, setDraftStripped] = useState(!bill?.isDraft);

  if (!bill || !viewerKey) return null;
  // Scope: Takumi reads every Bills DB; a supplement holder only their own.
  if (viewerKey !== "takumi" && bill.holder !== viewerKey) return null;
  if (bill.source === "statement") return <StatementBillDetail bill={bill} />;
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

  // Bucket the cycle's rows by what they *represent* in the bill. Mirrors
  // the auto-Note structure on the Bills DB written by /prepare-bill and
  // /update-bill — the user reading the bill should see the same shape
  // they'd read in the Notion Note: regular purchases first (the bulk),
  // then installment terms, then cashback credits, then manual adjustments.
  const sections: Array<{
    key: BillTxBucket;
    title: string;
    rows: Transaction[];
  }> = [
    { key: "regular",            title: "Regular purchases",  rows: [] },
    { key: "installment",        title: "Installment terms",  rows: [] },
    { key: "cashback-credit",    title: "Cashback credits",   rows: [] },
    { key: "payment",            title: "Payments",           rows: [] },
    { key: "manual-adjustment",  title: "Manual adjustments", rows: [] },
  ];
  for (const tx of cycleTxs) {
    const bucket = categoriseBillTx(tx);
    const section = sections.find((s) => s.key === bucket)!;
    section.rows.push(tx);
  }
  const visibleSections = sections.filter((s) => s.rows.length > 0);

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
                      attach slip · records the payment row
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
          {visibleSections.map((section, idx) => {
            const total = section.rows.reduce((s, t) => s + t.amount, 0);
            const rowsWord = section.rows.length === 1 ? "row" : "rows";
            return (
              <section
                key={section.key}
                className={
                  idx === 0
                    ? "mt-8 px-5 pb-2 lg:mt-0 lg:px-0"
                    : "mt-6 px-5 pb-2 lg:px-0"
                }
              >
                <SectionLabel
                  number={String(idx + 1).padStart(2, "0")}
                  trailing={
                    <span className="flex items-baseline gap-3">
                      <span>{section.rows.length} {rowsWord}</span>
                      <Amount
                        value={total}
                        size="sm"
                        tone={total < 0 ? "credit" : "default"}
                      />
                    </span>
                  }
                >
                  {section.title}
                </SectionLabel>
                <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
                  {section.rows.map((t, i) => (
                    <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
                  ))}
                </div>
              </section>
            );
          })}
          <div className="px-5 pb-10 lg:px-0" />
        </div>
      </div>
    </div>
  );
};

/**
 * Takumi's statement-driven bill: the bank's printed per-card total —
 * his principal plus every supplement section. Every statement line lives in
 * exactly one ledger, so the parts below add up to the print. He pays the
 * bank himself; Baiboon's and Nuta's parts are what they owe him, and his
 * payment never touches their ledgers. Takumi's view only.
 */
const StatementBillDetail = ({ bill }: { bill: Bill }) => {
  const [paid, setPaid] = useState(bill.status === "paid");
  const card = CARDS[bill.cardId];
  const breakdown = bill.breakdown ?? { takumi: bill.amount };
  const parts = breakdownParts(breakdown);
  const autoDebit = bill.paidVia === "auto-debit";

  // Each ledger's statement lines for the cycle (household-only rows left out).
  const ledgers = (["takumi", "baiboon", "nuta"] as const)
    .map((h) => ({ holder: h, rows: statementLinesFor(h, bill.cardId, bill.billCycleDate) }))
    .filter((l) => l.rows.length > 0);

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title={`${card.name} · ${bill.billCycleDate.slice(0, 7)}`}
        eyebrow={`Takumi · statement · ${bill.billCycleDate}`}
        back
      />

      <div className="lg:grid lg:grid-cols-12 lg:gap-10 lg:px-5">
        <div className="lg:col-span-5 lg:sticky lg:top-6 lg:self-start">
          <div className="px-5 lg:px-0">
            <CardFace card={card} holder="takumi" />
          </div>

          <section className="mx-5 mt-5 rounded-3xl border border-paper-line bg-paper-raised/60 p-5 lg:mx-0">
            <div className="flex items-baseline justify-between text-[12px] uppercase tracking-[0.22em] text-ink-faint">
              <span>printed card total</span>
              <div className="flex gap-1.5">
                <Pill tone="neutral">statement</Pill>
                {paid && <Pill tone="teal" uppercase>paid</Pill>}
              </div>
            </div>
            <Amount value={bill.amount} signed={false} size="xl" className="mt-2 text-ink" symbol />
            {bill.dueDate && (
              <div className="mt-1 text-[12px] uppercase tracking-[0.18em] text-ink-faint">
                due <span className="num text-ink-dim">{bill.dueDate}</span> ·{" "}
                {autoDebit ? "auto-debit" : "paid by transfer"}
              </div>
            )}

            <div className="mt-5">
              <BreakdownStrip breakdown={breakdown} total={bill.amount} legend={false} />
            </div>
            <div className="mt-3 divide-y divide-paper-line/40">
              {parts.map((p) => (
                <div key={p.key} className="flex items-baseline justify-between gap-3 py-2">
                  <div className="flex min-w-0 items-center gap-2">
                    <span
                      aria-hidden
                      className="h-2 w-2 shrink-0 rounded-full"
                      style={{
                        background: p.color ?? "transparent",
                        outline: p.color ? undefined : "1px dashed rgb(var(--ink-ghost))",
                      }}
                    />
                    <span className="truncate text-[14px] text-ink">
                      {p.key === "untracked" ? "Untracked supplement" : p.label}
                    </span>
                    <span className="truncate text-[12px] text-ink-faint">
                      {p.key === "takumi"
                        ? "your lines"
                        : p.key === "untracked"
                          ? "in no ledger"
                          : "owes you"}
                    </span>
                  </div>
                  <Amount value={p.amount} signed={false} size="sm" />
                </div>
              ))}
            </div>
            <p className="mt-3 text-[12px] leading-snug text-ink-faint">
              Your payment to the bank never touches the friends&rsquo; ledgers — their parts clear
              when they pay you.
            </p>
          </section>

          <section className="mx-5 mt-6 space-y-2 lg:mx-0">
            {!paid ? (
              <motion.button
                initial={{ opacity: 0, y: 6 }}
                animate={{ opacity: 1, y: 0 }}
                onClick={() => setPaid(true)}
                className="tap flex w-full items-center justify-between gap-3 rounded-2xl border border-teal-400/30 bg-teal-400/[0.05] px-4 py-4 text-left transition-colors hover:bg-teal-400/[0.08]"
              >
                <div className="flex items-center gap-3">
                  <span className="flex h-9 w-9 shrink-0 items-center justify-center rounded-full border border-teal-400/40 bg-teal-400/10">
                    <Landmark size={16} className="text-teal-400" />
                  </span>
                  <div>
                    <div className="font-display text-sm tracking-tight text-ink">
                      {autoDebit ? "Confirm the auto-debit" : "Mark paid to the bank"}
                    </div>
                    <div className="text-[12px] uppercase tracking-[0.16em] text-ink-faint">
                      {autoDebit ? "AUTO DEBIT row on the due date" : "attach slip · ชำระบิลเต็มจำนวน row"}
                    </div>
                  </div>
                </div>
                <span className="text-[12px] uppercase tracking-[0.22em] text-teal-400">confirm →</span>
              </motion.button>
            ) : (
              <div className="flex items-center justify-between rounded-2xl border border-teal-400/30 bg-teal-400/[0.06] px-4 py-3 text-[13px]">
                <div className="flex items-center gap-2 text-teal-400">
                  <Check size={14} /> {autoDebit ? "Auto-debited" : "Paid to the bank"} on {bill.paidAt ?? "today"}
                </div>
                <div className="flex gap-2 text-ink-faint">
                  {bill.hasSlip && <ImageIcon size={14} />}
                  {bill.hasStatementPdf && <FileText size={14} />}
                </div>
              </div>
            )}
            {bill.note && <p className="px-1 text-[12px] leading-snug text-ink-faint">{bill.note}</p>}
          </section>
        </div>

        <div className="lg:col-span-7">
          {ledgers.length === 0 ? (
            <section className="mt-8 px-5 pb-10 lg:mt-0 lg:px-0">
              <div className="rounded-2xl border border-paper-line/60 bg-paper-raised/30 px-5 py-8 text-center text-sm text-ink-faint">
                This cycle&rsquo;s lines aren&rsquo;t in the demo&rsquo;s mock slice — the statement PDF is attached.
              </div>
            </section>
          ) : (
            ledgers.map((l, idx) => {
              const total = l.rows.reduce((s, t) => s + t.amount, 0);
              const h = HOLDERS[l.holder];
              return (
                <section
                  key={l.holder}
                  className={idx === 0 ? "mt-8 px-5 pb-2 lg:mt-0 lg:px-0" : "mt-6 px-5 pb-2 lg:px-0"}
                >
                  <SectionLabel
                    number={String(idx + 1).padStart(2, "0")}
                    trailing={
                      <span className="flex items-baseline gap-3">
                        <span>
                          {l.rows.length} {l.rows.length === 1 ? "line" : "lines"}
                        </span>
                        <Amount value={total} size="sm" tone={total < 0 ? "credit" : "default"} />
                      </span>
                    }
                  >
                    <span className="inline-flex items-center gap-2">
                      <span aria-hidden className="h-2 w-2 rounded-full" style={{ background: h.accent }} />
                      {l.holder === "takumi" ? "Your lines" : `${h.englishName}'s lines`}
                    </span>
                  </SectionLabel>
                  <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
                    {l.rows
                      .slice()
                      .sort((a, b) => a.transactionDate.localeCompare(b.transactionDate))
                      .map((t, i) => (
                        <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
                      ))}
                  </div>
                </section>
              );
            })
          )}
          <div className="px-5 pb-10 lg:px-0" />
        </div>
      </div>
    </div>
  );
};
