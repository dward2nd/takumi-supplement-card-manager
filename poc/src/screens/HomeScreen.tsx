import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { Plus } from "lucide-react";
import { useApp } from "../data/state";
import { HOLDERS } from "../data/holders";
import { CARDS } from "../data/cards";
import { TRANSACTIONS } from "../data/transactions";
import { BILLS } from "../data/bills";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import { TransactionRow } from "../components/TransactionRow";
import { fmtLong, daysUntil } from "../data/format";

export const HomeScreen = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  const today = new Date("2026-05-26"); // POC reference date — see CLAUDE context

  const holder = holderKey ? HOLDERS[holderKey] : null;
  if (!holder) return null;

  const visibleHolders = holder.isAdmin
    ? (["takumi", "baiboon", "nuta"] as const)
    : ([holder.key] as const);

  // Aggregate "this cycle" spend + cashback across all the user's visible cards.
  const stats = useMemo(() => {
    const txs = TRANSACTIONS.filter((t) => visibleHolders.includes(t.holder));
    // Active cycle = transactions whose billCycleDate is the most recent BC ≤ today
    // For the POC we just take the 2026-05-25 cycle for everyone (matches mock data).
    const cycle = txs.filter((t) => t.billCycleDate === "2026-05-25");
    const gross = cycle.reduce((s, t) => s + (t.amount > 0 ? t.amount : 0), 0);
    const cashback = cycle.reduce((s, t) => s + (t.amount < 0 ? -t.amount : 0), 0);
    const net = cycle.reduce((s, t) => s + t.amount, 0);
    return { gross, cashback, net, count: cycle.length };
  }, [visibleHolders]);

  const upcomingBills = useMemo(
    () =>
      BILLS.filter((b) => visibleHolders.includes(b.holder as any) && b.isDraft)
        .sort((a, b) => a.billCycleDate.localeCompare(b.billCycleDate)),
    [visibleHolders],
  );

  const recentTxs = useMemo(
    () =>
      TRANSACTIONS.filter((t) => visibleHolders.includes(t.holder))
        .filter((t) => t.amount > 0) // skip credit/cashback rows in "recent"
        .sort((a, b) => b.transactionDate.localeCompare(a.transactionDate))
        .slice(0, 6),
    [visibleHolders],
  );

  return (
    <div>
      {/* Top headline panel */}
      <section className="top-safe px-5 pb-6 pt-2">
        <div className="text-[10px] uppercase tracking-[0.28em] text-amber-glow/80">
          {fmtLong(today.toISOString())} &middot;{" "}
          {today.toLocaleDateString("en-GB", { weekday: "long" })}
        </div>
        <h1 className="mt-2 font-display text-3xl font-light leading-tight tracking-tight text-ink">
          Good morning, <em className="italic font-thin text-amber-glow">{holder.englishName}.</em>
        </h1>
        {holder.isAdmin && (
          <div className="mt-2 text-xs text-ink-dim">
            Showing aggregated view across all 3 holders.
          </div>
        )}
      </section>

      {/* Cycle hero — typography-led */}
      <section className="mx-5 mb-6 overflow-hidden rounded-3xl border border-paper-line bg-gradient-to-br from-paper-raised to-paper-high">
        <div className="relative p-6">
          <div className="flex items-baseline justify-between text-[10px] uppercase tracking-[0.22em] text-ink-faint">
            <span>cycle · 25 may → 24 jun</span>
            <span>net due</span>
          </div>
          <motion.div
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="mt-2 flex items-baseline justify-between gap-2"
          >
            <Amount value={stats.net} size="xl" symbol={true} className="text-ink" />
          </motion.div>

          <div className="mt-6 grid grid-cols-3 gap-3 text-[11px]">
            <Stat label="gross spend" value={stats.gross} tone="default" />
            <Stat label="cashback" value={stats.cashback} tone="credit" />
            <Stat label="rows" value={stats.count} format="int" />
          </div>

          {/* Soft halo behind the number */}
          <span
            aria-hidden
            className="pointer-events-none absolute -right-10 -top-10 h-40 w-40 rounded-full bg-amber-300/10 blur-3xl"
          />
        </div>
      </section>

      {/* Big add-transaction button — the daily-action anchor */}
      <section className="mx-5 mb-8">
        <button
          onClick={() => nav("/add")}
          className="tap group relative flex w-full items-center justify-between gap-4 overflow-hidden rounded-2xl border border-amber-200/30 bg-gradient-to-r from-amber-300/10 via-amber-200/5 to-transparent px-5 py-5 text-left transition-all duration-300 hover:border-amber-200/60"
        >
          <span className="absolute inset-0 -z-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" style={{ background: "radial-gradient(400px 100px at 0% 50%, rgba(247,196,99,0.12), transparent)" }} />
          <div className="relative">
            <div className="text-[10px] uppercase tracking-[0.22em] text-amber-glow/90">
              record a transaction
            </div>
            <div className="mt-1 font-display text-xl font-light tracking-tight text-ink">
              What did you spend today?
            </div>
          </div>
          <span className="relative flex h-11 w-11 items-center justify-center rounded-full bg-amber-200 text-paper transition-transform duration-300 group-hover:scale-110">
            <Plus size={20} strokeWidth={2.2} />
          </span>
        </button>
      </section>

      {/* Upcoming bills */}
      {upcomingBills.length > 0 && (
        <section className="px-5 pb-8">
          <SectionLabel number="01" trailing={`${upcomingBills.length} due`}>
            Bills · upcoming
          </SectionLabel>
          <div className="mt-3 space-y-2">
            {upcomingBills.map((b) => {
              const card = CARDS[b.cardId];
              const days = daysUntil(getDueDate(b.billCycleDate), today);
              return (
                <button
                  key={b.id}
                  onClick={() => nav(`/bills/${b.id}`)}
                  className="tap group flex w-full items-center justify-between gap-3 rounded-2xl border border-paper-line/60 bg-paper-raised/40 px-4 py-3.5 text-left transition-colors hover:bg-paper-raised"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <span
                      className="h-9 w-9 shrink-0 rounded-xl"
                      style={{
                        background: `linear-gradient(135deg, ${card.brandColors[0]}, ${card.brandColors[1]})`,
                      }}
                    />
                    <div className="min-w-0">
                      <div className="flex items-center gap-2">
                        <span className="font-display text-base font-light text-ink truncate">
                          {card.name}
                        </span>
                        {b.isDraft && <Pill tone="amber" uppercase>draft</Pill>}
                      </div>
                      <div className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
                        due in <span className="num text-ink-dim">{days}</span> days · {HOLDERS[b.holder].englishName}
                      </div>
                    </div>
                  </div>
                  <Amount value={b.amount} signed={false} className="text-lg" />
                </button>
              );
            })}
          </div>
        </section>
      )}

      {/* Recent transactions */}
      <section className="px-5 pb-12">
        <SectionLabel
          number="02"
          trailing={
            <button onClick={() => nav("/cards")} className="tap text-amber-glow/90">
              all cards →
            </button>
          }
        >
          Recent
        </SectionLabel>
        <div className="mt-2 -mx-1 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
          {recentTxs.map((t, i) => (
            <TransactionRow key={t.id} tx={t} index={i} onTap={() => nav(`/cards/${t.cardId}`)} />
          ))}
          {recentTxs.length === 0 && (
            <div className="px-5 py-10 text-center text-sm text-ink-faint">
              No recent transactions yet. Tap <span className="text-amber-glow">+</span> to add one.
            </div>
          )}
        </div>
      </section>
    </div>
  );
};

const getDueDate = (bc: string) => {
  // POC convention: UOB BC=2026-05-25 → DD=2026-06-15
  if (bc === "2026-05-25") return "2026-06-15";
  return bc;
};

const Stat = ({
  label,
  value,
  tone = "default",
  format = "money",
}: {
  label: string;
  value: number;
  tone?: "default" | "credit" | "muted";
  format?: "money" | "int";
}) => (
  <div className="flex flex-col gap-1.5">
    <span className="text-[9px] uppercase tracking-[0.22em] text-ink-faint">
      {label}
    </span>
    {format === "money" ? (
      <Amount value={value} signed={false} tone={tone} size="sm" />
    ) : (
      <span className="num text-base text-ink">{value}</span>
    )}
  </div>
);
