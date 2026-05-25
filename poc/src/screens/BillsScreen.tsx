import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { BILLS } from "../data/bills";
import { CARDS } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import { daysUntil } from "../data/format";

export const BillsScreen = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  if (!holderKey) return null;

  const visible = useMemo(() => {
    const set: ("baiboon" | "nuta")[] = holderKey === "takumi"
      ? ["baiboon", "nuta"]
      : holderKey === "baiboon"
        ? ["baiboon"]
        : ["nuta"];
    return BILLS.filter((b) => set.includes(b.holder));
  }, [holderKey]);

  const drafts = visible.filter((b) => b.isDraft);
  const issued = visible.filter((b) => !b.isDraft && b.status !== "paid");
  const paid = visible
    .filter((b) => b.status === "paid")
    .sort((a, b) => b.billCycleDate.localeCompare(a.billCycleDate));

  const totalDue = drafts.reduce((s, b) => s + b.amount, 0);

  if (holderKey === "takumi") {
    // Takumi sees aggregated drafts; still useful surface.
  }

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title="Bills"
        eyebrow="statements & payment evidence"
      />

      {/* Headline panel */}
      <section className="mx-5 mb-8 overflow-hidden rounded-3xl border border-paper-line bg-paper-raised/60 p-5">
        <div className="text-[12px] uppercase tracking-[0.22em] text-ink-faint">
          due across all draft bills
        </div>
        <Amount value={totalDue} size="xl" signed={false} className="mt-2 text-ink" />
        <div className="mt-2 text-xs text-ink-dim">
          {drafts.length} {drafts.length === 1 ? "bill" : "bills"} drafting · upload statement PDFs to finalise
        </div>
      </section>

      {drafts.length > 0 && (
        <BillGroup title="Drafts · waiting for statement" number="01" items={drafts} nav={nav} />
      )}

      {issued.length > 0 && (
        <BillGroup title="Issued · awaiting payment" number="02" items={issued} nav={nav} />
      )}

      {paid.length > 0 && (
        <BillGroup
          title="Paid · history"
          number={drafts.length || issued.length ? "03" : "01"}
          items={paid}
          nav={nav}
          paid
        />
      )}
    </div>
  );
};

const BillGroup = ({
  title,
  number,
  items,
  nav,
  paid = false,
}: {
  title: string;
  number: string;
  items: import("../data/types").Bill[];
  nav: (path: string) => void;
  paid?: boolean;
}) => (
  <section className="px-5 pb-8">
    <SectionLabel number={number} trailing={`${items.length}`}>{title}</SectionLabel>
    <div className="mt-3 grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      {items.map((b, i) => {
        const card = CARDS[b.cardId];
        const today = new Date("2026-05-26");
        const dueDate = b.billCycleDate === "2026-05-25" ? "2026-06-15" : b.billCycleDate;
        const days = daysUntil(dueDate, today);
        return (
          <motion.button
            key={b.id}
            initial={{ opacity: 0, y: 6 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.03 * i, duration: 0.4 }}
            onClick={() => nav(`/bills/${b.id}`)}
            className="tap group flex w-full items-center justify-between gap-3 rounded-2xl border border-paper-line/70 bg-paper-raised/40 px-4 py-4 text-left transition-colors hover:bg-paper-raised"
          >
            <div className="flex items-center gap-3 min-w-0">
              <span
                aria-hidden
                className="h-12 w-12 shrink-0 rounded-xl"
                style={{
                  background: `linear-gradient(135deg, ${card.brandColors[0]}, ${card.brandColors[1]})`,
                }}
              />
              <div className="min-w-0">
                <div className="flex items-center gap-2">
                  <span className="font-display text-[15px] font-normal truncate text-ink">
                    {card.name}
                  </span>
                  {b.isDraft && <Pill tone="amber" uppercase>draft</Pill>}
                  {paid && <Pill tone="teal" uppercase>paid</Pill>}
                </div>
                <div className="text-[12px] uppercase tracking-[0.16em] text-ink-faint">
                  cycle {b.billCycleDate}{" "}
                  {b.isDraft ? (
                    <>· due in <span className="num text-ink-dim">{days}</span> days</>
                  ) : paid && b.paidAt ? (
                    <>· paid {b.paidAt}</>
                  ) : null}
                </div>
                <div className="text-[12px] uppercase tracking-[0.16em] text-ink-ghost">
                  {HOLDERS[b.holder].englishName} · {HOLDERS[b.holder].thaiName}
                </div>
              </div>
            </div>
            <Amount value={b.amount} signed={false} className="text-lg" />
          </motion.button>
        );
      })}
    </div>
  </section>
);
