import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useApp } from "../data/state";
import { BILLS } from "../data/bills";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { SectionLabel } from "../components/SectionLabel";
import { BillRow } from "../components/BillRow";
import type { Bill } from "../data/types";

export const BillsScreen = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  if (!holderKey) return null;
  const isAdmin = holderKey === "takumi";

  // Takumi sees every Bills DB (his statement bills + both friends'); a
  // supplement holder sees only their own.
  const visible = useMemo(
    () => BILLS.filter((b) => isAdmin || b.holder === holderKey),
    [holderKey, isAdmin],
  );

  // Takumi's own bills are statement-driven: the bank's printed per-card
  // total, which he pays himself. Friends' bills are what they owe him.
  const statements = visible.filter((b) => b.source === "statement" && b.status !== "paid");
  const drafts = visible.filter((b) => b.source !== "statement" && b.isDraft);
  const issued = visible.filter((b) => b.source !== "statement" && !b.isDraft && b.status !== "paid");
  const paid = visible
    .filter((b) => b.status === "paid")
    .sort((a, b) => b.billCycleDate.localeCompare(a.billCycleDate));

  const totalDue = drafts.reduce((s, b) => s + b.amount, 0);
  const toBank = statements.reduce((s, b) => s + b.amount, 0);

  let n = 0;
  const num = () => String(++n).padStart(2, "0");

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title="Bills"
        eyebrow="statements & payment evidence"
      />

      {/* Headline panel */}
      <section className="mx-5 mb-8 overflow-hidden rounded-3xl border border-paper-line bg-paper-raised/60 p-5">
        {isAdmin ? (
          // Two different debts, side by side: what the bank wants from Takumi,
          // and what the friends' drafts say they owe him.
          <div className="grid grid-cols-2 gap-4">
            <div>
              <div className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">to pay the bank</div>
              <Amount value={toBank} size="lg" signed={false} className="mt-2 text-ink" />
              <div className="mt-1 text-xs text-ink-dim">
                {statements.length} {statements.length === 1 ? "statement" : "statements"} · printed card totals
              </div>
            </div>
            <div className="border-l border-paper-line/60 pl-4">
              <div className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">owed to you</div>
              <Amount value={totalDue} size="lg" signed={false} className="mt-2 text-ink" />
              <div className="mt-1 text-xs text-ink-dim">
                {drafts.length} friends&rsquo; {drafts.length === 1 ? "draft" : "drafts"}
              </div>
            </div>
          </div>
        ) : (
          <>
            <div className="text-[12px] uppercase tracking-[0.22em] text-ink-faint">
              due across all draft bills
            </div>
            <Amount value={totalDue} size="xl" signed={false} className="mt-2 text-ink" />
            <div className="mt-2 text-xs text-ink-dim">
              {drafts.length} {drafts.length === 1 ? "bill" : "bills"} drafting · upload statement PDFs to finalise
            </div>
          </>
        )}
      </section>

      {statements.length > 0 && (
        <BillGroup
          title="Your statements · you pay the bank"
          number={num()}
          items={statements}
          caption="Each is the bank's printed total for the card — your lines plus every supplement section. Baiboon's and Nuta's parts are what they owe you."
        />
      )}

      {drafts.length > 0 && (
        <BillGroup
          title={isAdmin ? "Friends' drafts · waiting for statement" : "Drafts · waiting for statement"}
          number={num()}
          items={drafts}
        />
      )}

      {issued.length > 0 && (
        <BillGroup title="Issued · awaiting payment" number={num()} items={issued} />
      )}

      {paid.length > 0 && (
        <BillGroup
          title="Paid · history"
          number={num()}
          items={paid.slice(0, 6)}
          footer={
            paid.length > 6 ? (
              <button
                onClick={() => nav("/bills/history")}
                className="tap mt-3 ml-auto flex items-center gap-2 rounded-full px-3 py-1.5 text-[12px] uppercase tracking-[0.22em] text-amber-glow/90 transition-colors hover:text-amber-glow"
              >
                see all <span className="num">{paid.length}</span> paid bills →
              </button>
            ) : null
          }
        />
      )}
    </div>
  );
};

const BillGroup = ({
  title,
  number,
  items,
  caption,
  footer,
}: {
  title: string;
  number: string;
  items: Bill[];
  caption?: string;
  footer?: React.ReactNode;
}) => (
  <section className="px-5 pb-8">
    <SectionLabel number={number} trailing={`${items.length}`}>{title}</SectionLabel>
    {caption && <p className="mt-1 max-w-prose text-[12px] leading-snug text-ink-faint">{caption}</p>}
    <div className="mt-3 grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      {items.map((b, i) => (
        <BillRow key={b.id} bill={b} index={i} />
      ))}
    </div>
    {footer && <div className="flex justify-end">{footer}</div>}
  </section>
);
