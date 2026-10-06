import { useMemo } from "react";
import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { CircleCheck, Gauge, Plus } from "lucide-react";
import { useApp } from "../data/state";
import { HOLDERS } from "../data/holders";
import { CARDS } from "../data/cards";
import { TRANSACTIONS } from "../data/transactions";
import { BILLS, billDueDate } from "../data/bills";
import { quotaAlertsFor, trackersVisibleTo } from "../data/campaigns";
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

  // Friends' drafts, plus — for Takumi — his own statement bills not yet paid
  // to the bank.
  const upcomingBills = useMemo(
    () =>
      BILLS.filter(
        (b) =>
          (visibleHolders as readonly string[]).includes(b.holder) &&
          (b.isDraft || (b.source === "statement" && b.status !== "paid")),
      ).sort((a, b) => billDueDate(a).localeCompare(billDueDate(b))),
    [visibleHolders],
  );

  const recentTxs = useMemo(
    () =>
      TRANSACTIONS.filter((t) => visibleHolders.includes(t.holder))
        .filter((t) => t.amount > 0) // skip credit/cashback rows in "recent"
        .filter((t) => t.transactionDate <= TODAY_ISO) // pre-dated terms aren't "recent"
        .sort((a, b) => b.transactionDate.localeCompare(a.transactionDate))
        .slice(0, 6),
    [visibleHolders],
  );

  // Shared campaigns: periods at/over the 80% alert threshold on the viewer's
  // cards (household-wide), and the viewer's open cashback trackers.
  const alerts = useMemo(() => quotaAlertsFor(holder.key), [holder.key]);
  const openTrackers = useMemo(
    () => trackersVisibleTo(holder.key).filter((t) => !t.settled),
    [holder.key],
  );

  let sectionN = 0;
  const num = () => String(++sectionN).padStart(2, "0");

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      {/*
        lg+: editorial 2-col spread. Left column (5/12) holds the masthead +
        cycle hero + record CTA — the "headline" stack. Right column (7/12)
        carries the lists. Below lg this collapses to a single column with
        cycle+record paired 2-up at md only.
      */}
      <div className="lg:grid lg:grid-cols-12 lg:gap-10 lg:px-5">
        <div className="lg:col-span-5">
          {/* Masthead — greeting */}
          <section className="top-safe px-5 pb-6 pt-2 lg:px-0">
            <div className="text-[12px] uppercase tracking-[0.28em] text-amber-glow/80">
              {fmtLong(today.toISOString())} &middot;{" "}
              {today.toLocaleDateString("en-GB", { weekday: "long" })}
            </div>
            <h1 className="mt-2 font-display text-3xl font-normal leading-tight tracking-tight text-ink lg:text-4xl">
              Good morning, <em className="italic font-normal text-amber-glow">{holder.englishName}.</em>
            </h1>
            {holder.isAdmin && (
              <div className="mt-2 text-xs text-ink-dim">
                Showing aggregated view across all 3 holders.
              </div>
            )}
          </section>

          {/* Cycle hero + Record CTA — paired 2-up at md only; stacked at lg */}
          <div className="md:grid md:grid-cols-2 md:gap-4 lg:grid-cols-1 lg:gap-6">
            {/* Cycle hero — typography-led */}
            <section className="mx-5 mb-6 overflow-hidden rounded-3xl border border-paper-line bg-gradient-to-br from-paper-raised to-paper-high md:mx-5 md:mb-0 lg:mx-0">
              <div className="relative p-6">
                <div className="flex items-baseline justify-between text-[12px] uppercase tracking-[0.22em] text-ink-faint">
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

                <div className="mt-6 grid grid-cols-3 gap-3 text-[13px]">
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
            <section className="mx-5 mb-8 md:mx-5 md:mb-0 lg:mx-0">
              <button
                onClick={() => nav("/add")}
                className="tap group relative flex w-full items-center justify-between gap-4 overflow-hidden rounded-2xl border border-amber-200/30 bg-gradient-to-r from-amber-300/10 via-amber-200/5 to-transparent px-5 py-5 text-left transition-all duration-300 hover:border-amber-200/60 md:h-full"
              >
                <span className="absolute inset-0 -z-0 opacity-0 transition-opacity duration-300 group-hover:opacity-100" style={{ background: "radial-gradient(400px 100px at 0% 50%, rgba(247,196,99,0.12), transparent)" }} />
                <div className="relative">
                  <div className="text-[12px] uppercase tracking-[0.22em] text-amber-glow/90">
                    record a transaction
                  </div>
                  <div className="mt-1 font-display text-xl font-normal tracking-tight text-ink">
                    What did you spend today?
                  </div>
                </div>
                <span className="relative flex h-11 w-11 items-center justify-center rounded-full bg-amber-200 text-on-accent transition-transform duration-300 group-hover:scale-110">
                  <Plus size={20} strokeWidth={2.2} />
                </span>
              </button>
            </section>
          </div>
        </div>

        <div className="lg:col-span-7 lg:pt-2">
          {/* Upcoming bills */}
          {upcomingBills.length > 0 && (
            <section className="px-5 pb-8 lg:px-0 lg:pt-0">
              <SectionLabel number={num()} trailing={`${upcomingBills.length} due`}>
                Bills · upcoming
              </SectionLabel>
              <div className="mt-3 space-y-2">
                {upcomingBills.map((b) => {
                  const card = CARDS[b.cardId];
                  const days = daysUntil(billDueDate(b), today);
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
                            <span className="font-display text-base font-normal text-ink truncate">
                              {card.name}
                            </span>
                            {b.isDraft && <Pill tone="amber" uppercase>draft</Pill>}
                          </div>
                          <div className="text-[12px] uppercase tracking-[0.18em] text-ink-faint">
                            {b.source === "statement" && <>statement · </>}
                            due in <span className="num text-ink-dim">{days}</span> days ·{" "}
                            {b.source === "statement" ? "you pay the bank" : HOLDERS[b.holder].englishName}
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

          {/* Shared campaigns — quota alerts + cashback owed */}
          {(alerts.length > 0 || openTrackers.length > 0) && (
            <section className="px-5 pb-8 lg:px-0">
              <SectionLabel
                number={num()}
                trailing={
                  <button onClick={() => nav("/campaigns")} className="tap -my-3 text-amber-glow/90">
                    all campaigns →
                  </button>
                }
              >
                Campaigns · May
              </SectionLabel>

              {alerts.length > 0 && (
                <div className="mt-3 space-y-2">
                  {alerts.map(({ period, campaign, progress }) => {
                    const full = progress.state === "full";
                    return (
                      <button
                        key={period.id}
                        onClick={() => nav("/campaigns")}
                        className={
                          "tap flex w-full items-center gap-3 rounded-2xl border px-4 py-3 text-left transition-colors " +
                          (full
                            ? "border-teal-400/30 bg-teal-400/[0.05] hover:bg-teal-400/[0.08]"
                            : "border-amber-300/35 bg-amber-300/[0.06] hover:bg-amber-300/[0.09]")
                        }
                      >
                        <span
                          className={
                            "flex h-9 w-9 shrink-0 items-center justify-center rounded-full border " +
                            (full ? "border-teal-400/40 text-teal-400" : "border-amber-300/50 text-amber-glow")
                          }
                        >
                          {full ? <CircleCheck size={16} strokeWidth={1.6} /> : <Gauge size={16} strokeWidth={1.6} />}
                        </span>
                        <div className="min-w-0 flex-1">
                          <div className="flex items-baseline gap-2">
                            <span className="font-display text-base text-ink">{campaign.code}</span>
                            <span className="num text-[13px] text-amber-glow">{campaign.headline}</span>
                          </div>
                          <div className="text-[12px] leading-snug text-ink-faint">
                            {progress.next} · household-wide
                          </div>
                        </div>
                        <span className={"num shrink-0 text-lg " + (full ? "text-teal-400" : "text-amber-glow")}>
                          {Math.round(progress.ratio * 100)}%
                        </span>
                      </button>
                    );
                  })}
                </div>
              )}

              {openTrackers.length > 0 && (
                <OwedBlock trackers={openTrackers} isAdmin={holder.isAdmin} onOpen={() => nav("/campaigns")} />
              )}
            </section>
          )}

          {/* Recent transactions */}
          <section className="px-5 pb-12 lg:px-0">
            <SectionLabel
              number={num()}
              trailing={
                <button onClick={() => nav("/cards")} className="tap text-amber-glow/90">
                  all cards →
                </button>
              }
            >
              Recent
            </SectionLabel>
            <div className="mt-2 -mx-1 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30 lg:mx-0">
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
      </div>
    </div>
  );
};

const TODAY_ISO = "2026-05-26"; // POC reference date

/**
 * Cashback owed — open tracker rows. A supplement sees only their own total;
 * Takumi sees every holder's, since he pays the friends' shares out when the
 * bank credits his card.
 */
const OwedBlock = ({
  trackers,
  isAdmin,
  onOpen,
}: {
  trackers: import("../data/types").CashbackTracker[];
  isAdmin: boolean;
  onOpen: () => void;
}) => {
  const total = trackers.reduce((s, t) => s + t.expected, 0);
  if (!isAdmin) {
    return (
      <button
        onClick={onOpen}
        className="tap mt-3 block w-full rounded-2xl border border-teal-400/25 bg-gradient-to-br from-teal-400/[0.06] to-transparent p-4 text-left"
      >
        <div className="flex items-baseline justify-between text-[11px] uppercase tracking-[0.22em] text-ink-faint">
          <span>cashback owed to you</span>
          <span>
            <span className="num text-ink-dim">{trackers.length}</span> open
          </span>
        </div>
        <Amount value={total} signed={false} size="lg" tone="credit" className="mt-1.5" />
        <div className="mt-2 space-y-1">
          {trackers.map((t) => (
            <div key={t.id} className="flex items-baseline justify-between gap-3 text-[12.5px]">
              <span className="num truncate text-ink-dim">{t.title}</span>
              <Amount value={t.expected} signed={false} size="sm" className="text-ink-dim" />
            </div>
          ))}
        </div>
      </button>
    );
  }
  const byHolder = (["takumi", "baiboon", "nuta"] as const)
    .map((h) => {
      const rows = trackers.filter((t) => t.holder === h);
      return { h, n: rows.length, sum: rows.reduce((s, t) => s + t.expected, 0) };
    })
    .filter((x) => x.n > 0);
  return (
    <button
      onClick={onOpen}
      className="tap mt-3 block w-full rounded-2xl border border-paper-line/70 bg-paper-raised/40 p-4 text-left"
    >
      <div className="flex items-baseline justify-between text-[11px] uppercase tracking-[0.22em] text-ink-faint">
        <span>cashback trackers · open</span>
        <Amount value={total} signed={false} size="sm" tone="credit" />
      </div>
      <div className="mt-2 divide-y divide-paper-line/40">
        {byHolder.map(({ h, n, sum }) => (
          <div key={h} className="flex items-center justify-between gap-3 py-2">
            <div className="flex items-center gap-2">
              <span aria-hidden className="h-2 w-2 rounded-full" style={{ background: HOLDERS[h].accent }} />
              <span className="text-[14px] text-ink">{HOLDERS[h].englishName}</span>
              <span className="text-[12px] text-ink-faint">
                <span className="num">{n}</span> {n === 1 ? "tracker" : "trackers"}
              </span>
            </div>
            <Amount value={sum} signed={false} size="sm" tone="credit" />
          </div>
        ))}
      </div>
      <p className="mt-1 text-[12px] leading-snug text-ink-faint">
        Friends&rsquo; shares that land on your card are yours to pay out.
      </p>
    </button>
  );
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
    <span className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">
      {label}
    </span>
    {format === "money" ? (
      <Amount value={value} signed={false} tone={tone} size="sm" />
    ) : (
      <span className="num text-base text-ink">{value}</span>
    )}
  </div>
);
