import { useMemo } from "react";
import { useParams, useSearchParams } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { CARDS, last4For } from "../data/cards";
import { HOLDERS } from "../data/holders";
import { TRANSACTIONS } from "../data/transactions";
import { activePromotionsFor } from "../data/promotions";
import { CardFace } from "../components/CardFace";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { SectionLabel } from "../components/SectionLabel";
import { TransactionRow } from "../components/TransactionRow";
import { fmtLong, fmtRate } from "../data/format";
import { sumCashback, sumPoints } from "../data/earnings";
import type { CardId, HolderKey, Transaction } from "../data/types";

const TODAY = "2026-05-26"; // POC reference date

export const CardDetailScreen = () => {
  const { holderKey: viewerKey } = useApp();
  const { id } = useParams();
  const [params] = useSearchParams();
  const card = id ? CARDS[id as CardId] : undefined;
  if (!card || !viewerKey) return null;

  // Which holder's instance of this card are we looking at?
  //  - URL param wins (admin navigation from per-instance card list).
  //  - Otherwise: the viewer if they hold it, else the first holder that does.
  const requestedHolder = params.get("holder") as HolderKey | null;
  const instanceHolder: HolderKey =
    requestedHolder && card.holders.includes(requestedHolder)
      ? requestedHolder
      : card.holders.includes(viewerKey)
        ? viewerKey
        : card.holders[0];

  // Scope rule: Takumi (admin) can view any instance; supplements only their own.
  if (viewerKey !== "takumi" && instanceHolder !== viewerKey) return null;

  const txs = useMemo(
    () =>
      TRANSACTIONS.filter((t) => t.cardId === card.id && t.holder === instanceHolder)
        .sort((a, b) => b.transactionDate.localeCompare(a.transactionDate)),
    [card.id, instanceHolder],
  );

  const promos = activePromotionsFor(card.id, TODAY);

  const cycleTxs = txs.filter((t) => t.billCycleDate === currentBC(card));
  const cycleSpend = cycleTxs.reduce((s, t) => s + (t.amount > 0 ? t.amount : 0), 0);
  const cycleCredit = cycleTxs.reduce((s, t) => s + (t.amount < 0 ? -t.amount : 0), 0);
  const cycleNet = cycleTxs.reduce((s, t) => s + t.amount, 0);

  const cyclePoints = sumPoints(cycleTxs, card);
  const cycleCashback = sumCashback(cycleTxs);
  const earnsPoints = card.bahtPer1Point !== undefined && card.bahtPer1Point > 0;

  // Tier × this-cycle totals, for the merged promo+earnings panel.
  const tierMap = new Map<number, number>();
  for (const t of cycleTxs) {
    if (/cashback/i.test(t.name)) continue;
    if (t.cashbackPercent === undefined || t.cashbackPercent === 0) continue;
    tierMap.set(t.cashbackPercent, (tierMap.get(t.cashbackPercent) ?? 0) + t.amount);
  }
  const earnedByRate = (rate: number): number => {
    const sum = tierMap.get(rate) ?? 0;
    return Math.round(rate * sum * 100) / 100;
  };

  // Today-first / future-separated transaction sections.
  const todayOrPast: Transaction[] = [];
  const upcoming: Transaction[] = [];
  for (const t of txs) {
    if (t.transactionDate > TODAY) upcoming.push(t);
    else todayOrPast.push(t);
  }
  upcoming.sort((a, b) => a.transactionDate.localeCompare(b.transactionDate));

  // Section numbering — promos absorb cashback breakdown so there's no separate block.
  let n = 0;
  const nextNum = () => String(++n).padStart(2, "0");
  const promoNum = promos.length > 0 ? nextNum() : null;
  const txNum = nextNum();
  const upcomingNum = upcoming.length > 0 ? nextNum() : null;

  const instance = HOLDERS[instanceHolder];

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader
        title={card.name}
        eyebrow={`${card.issuer} · •••• ${last4For(card, instanceHolder)}`}
        // Always show whose physical card-instance this is — even when the
        // viewer is the holder. With shared product names like "First Choice"
        // across holders, the possessive tag is what disambiguates.
        ownershipTag={{ label: `${instance.englishName}'s`, accent: instance.accent }}
        back
      />

      {/* On desktop: card face on the left, cycle panel on the right. Mobile stays stacked. */}
      <div className="px-5 md:grid md:grid-cols-2 md:gap-6">
        <div>
          <CardFace card={card} holder={instanceHolder} size="lg" showOverall withBlurb />
        </div>

        {/* Cycle panel — explicit "this cycle" label, dense single grid. */}
        <div className="mt-6 md:mt-0 rounded-3xl border border-paper-line bg-paper-raised/60 p-5">
          <div className="flex items-baseline justify-between text-[12px] uppercase tracking-[0.22em] text-ink-faint">
            <span>this cycle &middot; outstanding</span>
            <span>{fmtLong(currentBC(card))}</span>
          </div>
          <motion.div
            initial={{ opacity: 0, y: 8 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.5 }}
            className="mt-2"
          >
            <Amount value={cycleNet} size="xl" className="text-ink" symbol />
          </motion.div>

          {/* Dense grid — only axes that apply to this card render. */}
          <div className="mt-5 grid grid-cols-3 gap-x-3 gap-y-4 text-[13px]">
            <Tile label="spend" value={cycleSpend} />
            {earnsPoints && (
              <Tile label="points earned" value={cyclePoints} format="int" />
            )}
            {cycleCashback > 0 || !earnsPoints ? (
              <Tile
                label={earnsPoints ? "cashback" : "credit"}
                value={earnsPoints ? cycleCashback : cycleCredit}
                tone="credit"
              />
            ) : (
              <Tile label="cashback" value={0} tone="muted" />
            )}
          </div>
        </div>
      </div>

      {/*
        Below the card+cycle top: at lg+ split into a 2-col reading layout.
        Promotions (content-dense, benefits from a narrower column) on the
        left; transactions + upcoming (long lists) on the right. When no
        promotions are active, the transactions section uses full width.
      */}
      <div className={promos.length > 0 ? "lg:grid lg:grid-cols-12 lg:gap-8 lg:px-5" : ""}>
      {promos.length > 0 && promoNum && (
        <section className="mt-8 px-5 lg:col-span-5 lg:mt-8 lg:px-0">
          <SectionLabel number={promoNum}>Active promotions</SectionLabel>
          <div className="mt-3 space-y-3">
            {promos.map((p) => {
              const totalCashback = p.tiers.reduce(
                (s, t) => s + earnedByRate(t.rate),
                0,
              );
              return (
                <div
                  key={p.id}
                  className="overflow-hidden rounded-2xl border border-amber-300/25 bg-gradient-to-br from-amber-300/[0.04] to-amber-200/[0.02] p-4"
                >
                  <div className="flex items-baseline justify-between gap-3">
                    <div>
                      <div className="font-display text-base font-normal tracking-tight text-ink">
                        {p.name}
                      </div>
                      <div className="mt-0.5 text-[12px] uppercase tracking-[0.18em] text-ink-faint">
                        {p.effectiveStart.slice(0, 7)} → {p.effectiveEnd?.slice(0, 7) ?? "open"}
                      </div>
                    </div>
                    <div className="text-right">
                      <div className="text-[12px] uppercase tracking-[0.18em] text-ink-faint">
                        earned this cycle
                      </div>
                      <Amount
                        value={totalCashback}
                        signed={false}
                        tone={totalCashback > 0 ? "credit" : "muted"}
                        size="md"
                      />
                    </div>
                  </div>

                  {/* Tier table inside the promo — patterns + earned-this-cycle per tier */}
                  <div className="mt-3 overflow-hidden rounded-xl border border-paper-line/50 bg-paper/40">
                    {p.tiers.map((t, i) => {
                      const tierSum = tierMap.get(t.rate) ?? 0;
                      const tierCb = earnedByRate(t.rate);
                      return (
                        <div
                          key={i}
                          className="flex items-center justify-between gap-3 border-b border-paper-line/40 px-3 py-2 last:border-b-0"
                        >
                          <div className="flex min-w-0 items-baseline gap-2">
                            <span className="num shrink-0 text-amber-glow text-sm">
                              {fmtRate(t.rate)}
                            </span>
                            <span className="truncate text-[12px] uppercase tracking-[0.14em] text-ink-dim">
                              {t.patterns.join(", ")}
                            </span>
                          </div>
                          <div className="flex items-baseline gap-3 shrink-0">
                            <div className="text-right">
                              <div className="text-[10.5px] uppercase tracking-[0.18em] text-ink-faint">spent</div>
                              <Amount value={tierSum} signed={false} size="sm" tone={tierSum > 0 ? "default" : "muted"} />
                            </div>
                            <div className="text-right">
                              <div className="text-[10.5px] uppercase tracking-[0.18em] text-ink-faint">earned</div>
                              <Amount value={tierCb} signed={false} size="sm" tone={tierCb > 0 ? "credit" : "muted"} />
                            </div>
                          </div>
                        </div>
                      );
                    })}
                  </div>

                  {p.installmentRule && (
                    <div className="mt-2 text-[13px] text-ink-faint">
                      Installments: <span className="num text-ink-dim">{fmtRate(p.installmentRule.rate)}</span> · {p.installmentRule.credited.replace("_", " ")}
                    </div>
                  )}
                  {p.foreignInThbPolicy.overrides.length > 0 && (
                    <div className="mt-2 text-[13px] text-ink-faint">
                      Foreign-in-THB exceptions:{" "}
                      {p.foreignInThbPolicy.overrides.map((o) => (
                        <span key={o.merchantSubstring} className="num text-ink-dim">
                          {o.merchantSubstring} @ {fmtRate(o.rate)}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              );
            })}
          </div>
        </section>
      )}

      <div className={promos.length > 0 ? "lg:col-span-7" : ""}>
        <section className="mt-8 px-5 pb-10 lg:px-0">
          <SectionLabel number={txNum} trailing={`${todayOrPast.length} rows`}>
            Transactions
          </SectionLabel>
          <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
            {todayOrPast.length === 0 && (
              <div className="px-5 py-10 text-center text-sm text-ink-faint">
                No transactions on this card yet.
              </div>
            )}
            {todayOrPast.map((t, i) => (
              <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
            ))}
          </div>
        </section>

        {upcoming.length > 0 && upcomingNum && (
          <section className="mt-2 px-5 pb-12 lg:px-0">
            <SectionLabel number={upcomingNum} trailing={`${upcoming.length} scheduled`}>
              Upcoming · installments &amp; pre-dated rows
            </SectionLabel>
            <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/40 bg-paper-raised/15">
              {upcoming.map((t, i) => (
                <TransactionRow key={t.id} tx={t} hideCardChip index={i} />
              ))}
            </div>
            <p className="mt-2 text-[12px] uppercase tracking-[0.18em] text-ink-faint">
              Future-dated rows — typically instalments scheduled by the bank.
            </p>
          </section>
        )}
      </div>
      </div>
    </div>
  );
};

const currentBC = (c: { issuer: string }): string => {
  if (c.issuer === "UOB") return "2026-05-25";
  if (c.issuer === "Krungsri" || c.issuer === "CardX") return "2026-06-05";
  return "2026-05-25";
};

const Tile = ({
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
  <div>
    <div className="text-[11px] uppercase tracking-[0.22em] text-ink-faint">
      {label}
    </div>
    {format === "int" ? (
      <div
        className={
          "num mt-1 text-base " +
          (tone === "credit"
            ? "text-teal-400"
            : tone === "muted"
              ? "text-ink-faint"
              : "text-ink")
        }
      >
        {value.toLocaleString("en-US")}
      </div>
    ) : (
      <Amount value={value} signed={false} tone={tone} size="sm" className="mt-1" />
    )}
  </div>
);
