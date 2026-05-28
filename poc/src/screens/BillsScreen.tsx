import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { useApp } from "../data/state";
import { BILLS } from "../data/bills";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { SectionLabel } from "../components/SectionLabel";
import { BillRow } from "../components/BillRow";

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
          items={paid.slice(0, 6)}
          nav={nav}
          paid
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
  footer,
}: {
  title: string;
  number: string;
  items: import("../data/types").Bill[];
  /** Unused — kept for callers' historical signature; pill rendering now reads bill.status. */
  paid?: boolean;
  nav?: (path: string) => void;
  footer?: React.ReactNode;
}) => (
  <section className="px-5 pb-8">
    <SectionLabel number={number} trailing={`${items.length}`}>{title}</SectionLabel>
    <div className="mt-3 grid gap-2 md:grid-cols-2 lg:grid-cols-3">
      {items.map((b, i) => (
        <BillRow key={b.id} bill={b} index={i} />
      ))}
    </div>
    {footer && <div className="flex justify-end">{footer}</div>}
  </section>
);
