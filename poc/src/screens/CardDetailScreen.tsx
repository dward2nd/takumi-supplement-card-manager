import { useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { CARDS } from "../data/cards";
import { TRANSACTIONS } from "../data/transactions";
import { activePromotionsFor } from "../data/promotions";
import { CardFace } from "../components/CardFace";
import { PageHeader } from "../components/PageHeader";
import { Amount } from "../components/Amount";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import { TransactionRow } from "../components/TransactionRow";
import { fmtLong, fmtRate } from "../data/format";
import type { CardId } from "../data/types";

export const CardDetailScreen = () => {
  const { holderKey } = useApp();
  const { id } = useParams();
  const nav = useNavigate();
  const card = id ? CARDS[id as CardId] : undefined;
  if (!card || !holderKey) return null;

  const txs = useMemo(
    () =>
      TRANSACTIONS.filter((t) => t.cardId === card.id && (holderKey === "takumi" || t.holder === holderKey))
        .sort((a, b) => b.transactionDate.localeCompare(a.transactionDate)),
    [card.id, holderKey],
  );

  const promos = activePromotionsFor(card.id, "2026-05-26");

  const cycleTxs = txs.filter((t) => t.billCycleDate === currentBC(card));
  const cycleSpend = cycleTxs.reduce((s, t) => s + (t.amount > 0 ? t.amount : 0), 0);
  const cycleCredit = cycleTxs.reduce((s, t) => s + (t.amount < 0 ? -t.amount : 0), 0);
  const cycleNet = cycleTxs.reduce((s, t) => s + t.amount, 0);

  // Tier breakdown (excluding cashback credit rows)
  const tierMap = new Map<number, number>();
  for (const t of cycleTxs) {
    if (/cashback/i.test(t.name)) continue;
    if (t.cashbackPercent === undefined) continue;
    tierMap.set(t.cashbackPercent, (tierMap.get(t.cashbackPercent) ?? 0) + t.amount);
  }
  const tiers = [...tierMap.entries()].sort((a, b) => b[0] - a[0]);

  return (
    <div>
      <PageHeader title={card.name} eyebrow={card.issuer} back />

      <div className="px-5">
        <CardFace card={card} size="lg" withBlurb />
      </div>

      <div className="mx-5 mt-6 rounded-3xl border border-paper-line bg-paper-raised/60 p-5">
        <div className="flex items-baseline justify-between text-[10px] uppercase tracking-[0.22em] text-ink-faint">
          <span>cycle outstanding</span>
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
        <div className="mt-4 grid grid-cols-3 gap-3 text-[11px]">
          <Tile label="spend" value={cycleSpend} />
          <Tile label="cashback" value={cycleCredit} tone="credit" />
          <Tile label="rows" value={cycleTxs.length} format="int" />
        </div>
      </div>

      {promos.length > 0 && (
        <section className="mt-8 px-5">
          <SectionLabel number="01">Active promotions</SectionLabel>
          <div className="mt-3 space-y-3">
            {promos.map((p) => (
              <div
                key={p.id}
                className="overflow-hidden rounded-2xl border border-amber-300/25 bg-gradient-to-br from-amber-300/[0.04] to-amber-200/[0.02] p-4"
              >
                <div className="flex items-baseline justify-between gap-3">
                  <div className="font-display text-base font-light tracking-tight text-ink">
                    {p.name}
                  </div>
                  <Pill tone="amber" uppercase={false}>
                    {p.effectiveStart.slice(0, 7)} → {p.effectiveEnd?.slice(0, 7) ?? "open"}
                  </Pill>
                </div>
                <div className="mt-3 flex flex-wrap gap-1.5">
                  {p.tiers.map((t, i) => (
                    <span
                      key={i}
                      className="rounded-md border border-paper-line bg-paper-raised px-2 py-1 text-[10px] uppercase tracking-[0.14em] text-ink-dim"
                    >
                      <span className="num text-amber-glow">{fmtRate(t.rate)}</span>{" "}
                      &middot;{" "}
                      {t.patterns.join(", ").slice(0, 28)}
                      {t.patterns.join(", ").length > 28 ? "…" : ""}
                    </span>
                  ))}
                </div>
                {p.installmentRule && (
                  <div className="mt-2 text-[11px] text-ink-faint">
                    Installments: <span className="num text-ink-dim">{fmtRate(p.installmentRule.rate)}</span> · {p.installmentRule.credited.replace("_", " ")}
                  </div>
                )}
              </div>
            ))}
          </div>
        </section>
      )}

      {tiers.length > 0 && (
        <section className="mt-8 px-5">
          <SectionLabel number="02">Earned this cycle</SectionLabel>
          <div className="mt-3 overflow-hidden rounded-2xl border border-paper-line bg-paper-raised/30">
            {tiers.map(([rate, total]) => {
              const cb = Math.round(rate * total * 100) / 100;
              return (
                <div
                  key={rate}
                  className="flex items-center justify-between border-b border-paper-line/60 px-4 py-3 last:border-b-0"
                >
                  <div className="flex items-center gap-3">
                    <span className="num text-amber-glow text-lg">{fmtRate(rate)}</span>
                    <div>
                      <div className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
                        tier total
                      </div>
                      <Amount value={total} signed={false} size="sm" tone="muted" />
                    </div>
                  </div>
                  <div className="text-right">
                    <div className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
                      cashback
                    </div>
                    <Amount value={cb} signed={false} tone="credit" size="sm" />
                  </div>
                </div>
              );
            })}
          </div>
        </section>
      )}

      <section className="mt-8 px-5 pb-10">
        <SectionLabel number={tiers.length > 0 ? "03" : "02"} trailing={`${txs.length} total`}>
          Transactions
        </SectionLabel>
        <div className="mt-2 overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
          {txs.length === 0 && (
            <div className="px-5 py-10 text-center text-sm text-ink-faint">
              No transactions on this card yet.
            </div>
          )}
          {txs.map((t, i) => (
            <TransactionRow
              key={t.id}
              tx={t}
              hideCardChip
              index={i}
              onTap={() => nav(`/cards/${card.id}`)}
            />
          ))}
        </div>
      </section>
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
    <div className="text-[9px] uppercase tracking-[0.22em] text-ink-faint">
      {label}
    </div>
    {format === "int" ? (
      <div className="num mt-1 text-base text-ink">{value}</div>
    ) : (
      <Amount value={value} signed={false} tone={tone} size="sm" className="mt-1" />
    )}
  </div>
);
