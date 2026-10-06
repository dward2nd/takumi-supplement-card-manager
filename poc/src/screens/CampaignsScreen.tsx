import { useMemo } from "react";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { HOLDERS } from "../data/holders";
import { CARDS } from "../data/cards";
import {
  PRIMARY_ACCOUNTS,
  accountUsage,
  campaignById,
  periodsVisibleTo,
  trackersVisibleTo,
} from "../data/campaigns";
import { PageHeader } from "../components/PageHeader";
import { SectionLabel } from "../components/SectionLabel";
import { Amount } from "../components/Amount";
import { CampaignCard, TrackerLine } from "../components/CampaignCard";
import type { CashbackTracker, HolderKey, PrimaryAccount } from "../data/types";

/**
 * Every active campaign period on cards the viewer holds, grouped by the
 * primary account that pools it. A supplement holder sees the household-wide
 * progress and their own share + trackers; Takumi sees every share.
 */
export const CampaignsScreen = () => {
  const { holderKey: viewer } = useApp();
  if (!viewer) return null;
  const isAdmin = viewer === "takumi";

  const groups = useMemo(() => {
    const periods = periodsVisibleTo(viewer);
    return PRIMARY_ACCOUNTS.map((acc) => ({
      account: acc,
      periods: periods.filter((p) => campaignById(p.campaignId).accountId === acc.id),
    })).filter((g) => g.periods.length > 0);
  }, [viewer]);

  const trackers = useMemo(() => trackersVisibleTo(viewer), [viewer]);

  let n = 0;
  const num = () => String(++n).padStart(2, "0");

  return (
    <div className="mx-auto max-w-md md:max-w-3xl lg:max-w-6xl">
      <PageHeader title="Campaigns" eyebrow="household-wide · May 2026" back />

      <p className="-mt-1 max-w-prose px-5 pb-6 text-[13px] leading-relaxed text-ink-dim">
        Banks pay these on the primary account&rsquo;s <em className="font-display italic text-ink">pooled</em>{" "}
        spend — Takumi&rsquo;s card and every supplement together — and the credit is split first come,
        first served.{" "}
        {isAdmin
          ? "You see every holder's share."
          : "You see the household's progress and your own share, never anyone else's."}
      </p>

      {groups.map(({ account, periods }) => (
        <section key={account.id} className="px-5 pb-10">
          <SectionLabel number={num()} trailing={`${periods.length} ${periods.length === 1 ? "period" : "periods"}`}>
            {account.label}
          </SectionLabel>
          <AccountLine account={account} />
          <div className="mt-4 grid gap-3 md:grid-cols-2 lg:grid-cols-3">
            {periods.map((p, i) => (
              <CampaignCard key={p.id} period={p} viewer={viewer} index={i} />
            ))}
          </div>
        </section>
      ))}

      <section className="px-5 pb-12">
        <SectionLabel
          number={num()}
          trailing={`${trackers.filter((t) => !t.settled).length} open`}
        >
          Cashback trackers
        </SectionLabel>
        <p className="mt-1 max-w-prose text-[12px] leading-snug text-ink-faint">
          One per credit someone expects back. It settles when the bank&rsquo;s credit lands in their own
          ledger, or when Takumi transfers it with a slip.
        </p>
        <Trackers trackers={trackers} isAdmin={isAdmin} />
      </section>
    </div>
  );
};

/**
 * The shared credit line, aggregated across every card and holder on the
 * account — the one balance a supplement may see beyond their own.
 */
const AccountLine = ({ account }: { account: PrimaryAccount }) => {
  const { used, limit } = accountUsage(account);
  const ratio = limit ? Math.min(1, used / limit) : 0;
  return (
    <div className="mt-2.5">
      <div className="flex items-baseline justify-between gap-3 text-[12px] text-ink-faint">
        <span>
          {account.cardIds.map((id) => CARDS[id].name).join(" · ")}
        </span>
        <span className="shrink-0">
          <span className="num text-ink-dim">
            ฿{used.toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 })}
          </span>
          {limit ? (
            <>
              {" "}
              / <span className="num">฿{limit.toLocaleString("en-US")}</span> used
            </>
          ) : (
            " outstanding"
          )}
        </span>
      </div>
      {limit && (
        <div className="mt-1.5 h-px w-full bg-paper-line/70">
          <motion.div
            initial={{ width: 0 }}
            animate={{ width: `${Math.max(ratio * 100, 0.5)}%` }}
            transition={{ duration: 0.8, ease: [0.2, 0.7, 0.1, 1] }}
            className="h-px bg-ink-faint"
          />
        </div>
      )}
    </div>
  );
};

const Trackers = ({ trackers, isAdmin }: { trackers: CashbackTracker[]; isAdmin: boolean }) => {
  if (trackers.length === 0)
    return <div className="mt-3 text-sm text-ink-faint">No trackers yet.</div>;
  const byHolder = (["takumi", "baiboon", "nuta"] as HolderKey[])
    .map((h) => ({ holder: h, rows: trackers.filter((t) => t.holder === h) }))
    .filter((g) => g.rows.length > 0);

  return (
    <div className="mt-3 space-y-5">
      {byHolder.map(({ holder, rows }) => {
        const h = HOLDERS[holder];
        const open = rows.filter((t) => !t.settled).reduce((s, t) => s + t.expected, 0);
        return (
          <div key={holder}>
            <div className="mb-2">
              {isAdmin && (
                <div className="flex items-baseline justify-between gap-3">
                  <div className="flex items-center gap-2">
                    <span aria-hidden className="h-2.5 w-2.5 rounded-full" style={{ background: h.accent }} />
                    <span className="text-[12px] uppercase tracking-[0.24em] text-ink-dim">{h.englishName}</span>
                  </div>
                  <span className="text-[12px] text-ink-faint">
                    open <Amount value={open} signed={false} size="sm" tone="credit" />
                  </span>
                </div>
              )}
              {/* The Notion DB's own title, verbatim */}
              <div className={isAdmin ? "ml-[18px] text-[12px] text-ink-ghost" : "text-[12px] text-ink-ghost"}>
                {`รายการติดตามเครดิตเงินคืนของ${h.thaiName}`}
              </div>
            </div>
            <div className="overflow-hidden rounded-2xl border border-paper-line/60 bg-paper-raised/30">
              {rows.map((t) => (
                <div
                  key={t.id}
                  className="flex items-start justify-between gap-3 border-b border-paper-line/50 px-4 py-3 last:border-b-0"
                >
                  <div className="min-w-0">
                    <div className="truncate font-display text-[15px] leading-tight tracking-tight text-ink">
                      {t.title}
                    </div>
                    <div className="text-[11px] uppercase tracking-[0.18em] text-ink-faint">
                      {CARDS[t.cardId].name}
                    </div>
                    <TrackerLine tracker={t} inset={false} showTitle={false} />
                  </div>
                  <div className="shrink-0 text-right">
                    <div className="text-[10.5px] uppercase tracking-[0.2em] text-ink-faint">expected</div>
                    <Amount
                      value={t.expected}
                      signed={false}
                      size="sm"
                      tone={t.settled ? "muted" : "credit"}
                    />
                  </div>
                </div>
              ))}
            </div>
          </div>
        );
      })}
    </div>
  );
};
