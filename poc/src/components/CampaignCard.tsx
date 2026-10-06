import { useState } from "react";
import clsx from "clsx";
import { AnimatePresence, motion } from "framer-motion";
import { ChevronDown } from "lucide-react";
import { HOLDERS } from "../data/holders";
import {
  BASIS_LABEL,
  SHAPE_LABEL,
  QUOTA_ALERT_THRESHOLD,
  campaignById,
  progressOf,
  sharesVisibleTo,
  trackerFor,
  viewerShare,
  type PeriodProgress,
  type ProgressState,
} from "../data/campaigns";
import { Amount } from "./Amount";
import { Pill } from "./Pill";
import type { Campaign, CampaignPeriod, CampaignShare, CashbackTracker, HolderKey } from "../data/types";

/**
 * One Bureau period — a shared campaign's quota for one month / cycle.
 *
 * Reads like a ruler laid across the household's pooled spend: the band is
 * household-wide progress (neutral while open, amber past the 80% alert
 * threshold, teal once the cap is reached), notches mark the ladder's steps,
 * a caret marks the alert threshold. Below it, the viewer's own share — and,
 * for Takumi only, everyone's.
 */
export const CampaignCard = ({
  period,
  viewer,
  focus,
  index = 0,
  dense = false,
}: {
  period: CampaignPeriod;
  viewer: HolderKey;
  /** The holder whose share to lead with (card detail: the instance's holder). */
  focus?: HolderKey;
  index?: number;
  /** Collapse the "how it pays" note by default. */
  dense?: boolean;
}) => {
  const campaign = campaignById(period.campaignId);
  const progress = progressOf(period);
  const [open, setOpen] = useState(!dense);
  const lead = focus ?? viewer;

  return (
    <motion.article
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: Math.min(index * 0.05, 0.3), duration: 0.45, ease: [0.2, 0.7, 0.1, 1] }}
      className={clsx(
        "relative overflow-hidden rounded-2xl border p-4",
        progress.state === "near" && "border-amber-300/35 bg-gradient-to-br from-amber-300/[0.06] to-transparent",
        progress.state === "full" && "border-teal-400/30 bg-gradient-to-br from-teal-400/[0.05] to-transparent",
        progress.state === "open" && "border-paper-line/70 bg-paper-raised/30",
      )}
    >
      {/* Bureau row name — the archival stamp — and the state */}
      <div className="flex items-start justify-between gap-3">
        <span className="num pt-1 text-[11px] tracking-[0.02em] text-ink-faint">{period.name}</span>
        <StatePill state={progress.state} campaign={campaign} />
      </div>

      <div className="mt-2 flex items-end justify-between gap-3">
        <div className="min-w-0">
          <div className="flex items-baseline gap-2">
            <h3 className="font-display text-[1.6rem] font-normal leading-none tracking-tight text-ink">
              {campaign.code}
            </h3>
            <span className="num text-sm text-amber-glow">{campaign.headline}</span>
          </div>
          {/* The bank's own campaign title — Thai stays in the body face. */}
          <div className="mt-1 truncate font-sans text-[13px] text-ink-dim">{campaign.title}</div>
        </div>
        <div className="shrink-0 text-right">
          <div className="text-[10.5px] uppercase tracking-[0.22em] text-ink-faint">
            {campaign.periodBasis === "cycle" ? "cycle" : "period"}
          </div>
          <div className="num text-[12px] text-ink-dim">{fmtWindow(period.start, period.end)}</div>
        </div>
      </div>

      <Hero period={period} campaign={campaign} />

      <Meter period={period} campaign={campaign} progress={progress} />

      <p
        className={clsx(
          "mt-2 text-[13px] leading-snug",
          progress.state === "near" && "text-amber-glow",
          progress.state === "full" && "text-teal-400",
          progress.state === "open" && "text-ink-dim",
        )}
      >
        {progress.next}
      </p>

      <Shares period={period} campaign={campaign} viewer={viewer} lead={lead} />

      {/* How it pays — the campaign's rule, collapsible in dense contexts */}
      <div className="mt-1 border-t border-paper-line/40">
        <button
          onClick={() => setOpen((v) => !v)}
          aria-expanded={open}
          className="tap -mb-2 flex w-full items-center justify-between gap-2 text-left text-[11px] uppercase tracking-[0.2em] text-ink-faint transition-colors hover:text-ink-dim"
        >
          <span>
            how it pays · {SHAPE_LABEL[campaign.shape]} · {BASIS_LABEL[campaign.periodBasis]}
          </span>
          <ChevronDown
            size={14}
            strokeWidth={1.5}
            className={clsx("shrink-0 transition-transform duration-300", open && "rotate-180")}
          />
        </button>
        <AnimatePresence initial={false}>
          {open && (
            <motion.div
              initial={{ height: 0, opacity: 0 }}
              animate={{ height: "auto", opacity: 1 }}
              exit={{ height: 0, opacity: 0 }}
              transition={{ duration: 0.3, ease: [0.2, 0.7, 0.1, 1] }}
              className="overflow-hidden"
            >
              <p className="pb-1 pt-2 text-[13px] leading-relaxed text-ink-dim">{campaign.rule}</p>
              <p className="pb-1 text-[12px] leading-relaxed text-ink-faint">
                {campaign.reward === "points"
                  ? "The quota fills first come, first served by transaction time; the row it runs out in keeps the bonus and gives the over-quota part back."
                  : campaign.shape === "ladder"
                    ? "Split first come, first served by transaction time; rows on the same date share a step pro rata. Shares add up to the credit to the satang."
                    : "The cap is claimed first come, first served by transaction time; rows on the same date share what's left pro rata. Shares add up to the credit to the satang."}
              </p>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </motion.article>
  );
};

// ─── pieces ───────────────────────────────────────────────────────────────

const StatePill = ({ state, campaign }: { state: ProgressState; campaign: Campaign }) => {
  if (state === "near")
    return (
      <Pill tone="amber" className="shrink-0">
        near cap
      </Pill>
    );
  if (state === "full")
    return (
      <Pill tone="teal" className="shrink-0">
        {campaign.shape === "ladder" ? "top step" : campaign.shape === "points-quota" ? "quota used" : "cap reached"}
      </Pill>
    );
  return null;
};

/** The figure that matters: credit earned (cashback), or quota used (points) — plus the pool it came from. */
const Hero = ({ period, campaign }: { period: CampaignPeriod; campaign: Campaign }) => {
  const pooled = (
    <div className="mt-0.5 text-[12px] text-ink-faint">
      on <span className="num text-ink-dim">฿{fmtB(period.pooledSpend)}</span>{" "}
      {campaign.shape === "per-slip"
        ? `of linked slips · ${period.slips ?? 0} paid`
        : "pooled household spend"}
    </div>
  );
  if (campaign.reward === "points") {
    return (
      <div className="mt-4">
        <div className="flex items-baseline gap-2">
          <Amount value={period.counted} signed={false} size="lg" className="text-ink" />
          <span className="text-[12px] text-ink-faint">
            of <span className="num">฿{period.cap.toLocaleString("en-US")}</span> at {campaign.quota?.bonus}
          </span>
        </div>
        {pooled}
      </div>
    );
  }
  return (
    <div className="mt-4">
      <div className="flex items-baseline gap-2">
        <Amount value={period.credit} signed={false} size="lg" tone={period.credit > 0 ? "credit" : "muted"} />
        <span className="text-[12px] text-ink-faint">
          of <span className="num">฿{period.cap.toLocaleString("en-US")}</span>{" "}
          {campaign.shape === "ladder" ? "at the top step" : campaign.periodBasis === "cycle" ? "a cycle" : "a month"}
        </span>
      </div>
      {pooled}
    </div>
  );
};

const FILL: Record<ProgressState, string> = {
  open: "bg-ink-dim",
  near: "bg-amber-glow shadow-[0_0_14px_-2px_rgba(247,196,99,0.55)]",
  full: "bg-teal-400",
};

/**
 * The ruler. Continuous for spend/credit meters (ladder notches cut into the
 * band where steps are reached); discrete pips for per-slip campaigns.
 */
const Meter = ({
  period,
  campaign,
  progress,
}: {
  period: CampaignPeriod;
  campaign: Campaign;
  progress: PeriodProgress;
}) => {
  if (campaign.shape === "per-slip" && campaign.perSlip) {
    const pips = Math.round((campaign.cap ?? 0) / campaign.perSlip.credit);
    const filled = period.slips ?? 0;
    return (
      <div className="mt-3">
        <div className="flex gap-1.5" role="img" aria-label={`${filled} of ${pips} slips paid`}>
          {Array.from({ length: pips }).map((_, i) => (
            <motion.span
              key={i}
              initial={{ scaleY: 0.4, opacity: 0 }}
              animate={{ scaleY: 1, opacity: 1 }}
              transition={{ delay: 0.15 + i * 0.06, duration: 0.35 }}
              className={clsx(
                "h-2.5 flex-1 origin-bottom rounded-[3px]",
                i < filled ? FILL[progress.state] : "border border-dashed border-paper-line bg-transparent",
              )}
            />
          ))}
        </div>
        <div className="mt-1.5 flex justify-between text-[10.5px] uppercase tracking-[0.18em] text-ink-faint">
          <span>
            <span className="num text-ink-dim">{filled}</span> of <span className="num">{pips}</span> slips
          </span>
          <span className="num normal-case tracking-normal">
            ฿{campaign.perSlip.credit} a slip ≥ ฿{campaign.perSlip.minSlip}
          </span>
        </div>
      </div>
    );
  }

  const pct = (v: number) => `${Math.max(0, Math.min(100, (v / progress.target) * 100))}%`;
  const steps = campaign.shape === "ladder" ? campaign.steps ?? [] : [];
  const next = period.nextStep;
  // Label the next step only when it won't collide with the end labels.
  const nextRatio = next ? next.at / progress.target : 0;
  const showNextLabel = next && nextRatio > 0.1 && nextRatio < 0.8;

  return (
    <div className="mt-3">
      <div
        className="relative h-[9px]"
        role="meter"
        aria-valuemin={0}
        aria-valuemax={progress.target}
        aria-valuenow={progress.value}
        aria-label={`${campaign.code} ${campaign.headline} — ${Math.round(progress.ratio * 100)}% used, household-wide`}
      >
        {/* track */}
        <span className="absolute inset-x-0 top-[3px] h-[3px] rounded-full bg-paper-line/70" />
        {/* household fill */}
        <motion.span
          initial={{ width: 0 }}
          animate={{ width: `${Math.max(progress.ratio * 100, progress.value > 0 ? 1.5 : 0)}%` }}
          transition={{ duration: 0.9, delay: 0.15, ease: [0.2, 0.7, 0.1, 1] }}
          className={clsx("absolute left-0 top-0 h-[9px] rounded-full", FILL[progress.state])}
        />
        {/* ladder notches — cut into the band once reached */}
        {steps.slice(0, -1).map((s) => (
          <span
            key={s.at}
            className={clsx(
              "absolute top-0 h-[9px] w-[2px] -translate-x-1/2",
              s.at <= period.pooledSpend ? "bg-paper/80" : s === next ? "bg-amber-glow/80" : "bg-ink-ghost/50",
            )}
            style={{ left: pct(s.at) }}
          />
        ))}
        {/* 80% alert threshold caret */}
        <span
          aria-hidden
          className="absolute -top-[5px] h-0 w-0 -translate-x-1/2 border-x-[3.5px] border-t-[4px] border-x-transparent border-t-amber-glow/60"
          style={{ left: `${QUOTA_ALERT_THRESHOLD * 100}%` }}
        />
      </div>

      <div className="num relative mt-1.5 h-4 text-[10.5px] text-ink-faint">
        <span className="absolute left-0">0</span>
        {showNextLabel && next ? (
          <span
            className="absolute -translate-x-1/2 whitespace-nowrap text-amber-glow/90"
            style={{ left: pct(next.at) }}
          >
            ฿{fmtK(next.at)} → ฿{fmtK(next.credit)}
          </span>
        ) : (
          <span
            className="absolute -translate-x-1/2 text-amber-glow/70"
            style={{ left: `${QUOTA_ALERT_THRESHOLD * 100}%` }}
          >
            {Math.round(QUOTA_ALERT_THRESHOLD * 100)}%
          </span>
        )}
        <span className="absolute right-0">฿{fmtK(progress.target)}</span>
      </div>
    </div>
  );
};

/**
 * Who earned what. A supplement holder sees their own line only — the pool
 * is household-wide, the share is theirs. Takumi sees every holder's.
 */
const Shares = ({
  period,
  campaign,
  viewer,
  lead,
}: {
  period: CampaignPeriod;
  campaign: Campaign;
  viewer: HolderKey;
  lead: HolderKey;
}) => {
  const visible = sharesVisibleTo(period, viewer);
  const isAdmin = viewer === "takumi";
  const rows: CampaignShare[] = isAdmin
    ? [...visible].sort((a, b) => (a.holder === lead ? -1 : b.holder === lead ? 1 : 0))
    : [viewerShare(period, viewer)];

  return (
    <div className="mt-3 border-t border-paper-line/40 pt-2.5">
      <div className="mb-1 flex items-baseline justify-between text-[10.5px] uppercase tracking-[0.22em] text-ink-faint">
        <span>{isAdmin ? "household split" : "your share"}</span>
        <span>{campaign.reward === "points" ? "inside quota" : "credit"}</span>
      </div>
      {rows.length === 0 && (
        <div className="py-1 text-[13px] text-ink-faint">No linked spend yet.</div>
      )}
      {rows.map((s) => (
        <ShareRow
          key={s.holder}
          share={s}
          campaign={campaign}
          tracker={trackerFor(period.id, s.holder)}
          you={s.holder === viewer}
          emphasised={s.holder === lead}
          showName={isAdmin}
        />
      ))}
    </div>
  );
};

const ShareRow = ({
  share,
  campaign,
  tracker,
  you,
  emphasised,
  showName,
}: {
  share: CampaignShare;
  campaign: Campaign;
  tracker?: CashbackTracker;
  you: boolean;
  emphasised: boolean;
  showName: boolean;
}) => {
  const h = HOLDERS[share.holder];
  const isPoints = campaign.reward === "points";
  const pastQuota = Math.max(0, share.spend - share.counted);
  return (
    <div className="py-1.5">
      <div className="flex items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-2">
          <span aria-hidden className="h-2 w-2 shrink-0 rounded-full" style={{ background: h.accent }} />
          <span className={clsx("truncate text-[14px]", emphasised ? "text-ink" : "text-ink-dim")}>
            {showName ? h.englishName : "You"}
            {showName && you && <span className="ml-1 text-ink-faint">(you)</span>}
          </span>
          <span className="num shrink-0 text-[11.5px] text-ink-faint">
            {share.spend > 0 ? `฿${fmtB(share.spend)} linked` : "no spend yet"}
          </span>
        </div>
        {isPoints ? (
          <Amount value={share.counted} signed={false} size="sm" tone={share.counted > 0 ? "default" : "muted"} />
        ) : (
          <Amount value={share.credit} signed={false} size="sm" tone={share.credit > 0 ? "credit" : "muted"} />
        )}
      </div>
      {isPoints && pastQuota > 0 && (
        <div className="ml-4 mt-0.5 text-[11.5px] text-ink-faint">
          <span className="num">฿{fmtB(pastQuota)}</span> past the quota
          at {campaign.quota?.after}
        </div>
      )}
      {share.slips !== undefined && share.slips > 0 && (
        <div className="ml-4 mt-0.5 text-[11.5px] text-ink-faint">
          <span className="num">{share.slips}</span> slip{share.slips === 1 ? "" : "s"} paid
        </div>
      )}
      {tracker && <TrackerLine tracker={tracker} showTitle={false} />}
    </div>
  );
};

export const TrackerLine = ({
  tracker,
  inset = true,
  showTitle = true,
}: {
  tracker: CashbackTracker;
  /** Indent under a share row's dot. */
  inset?: boolean;
  /** Repeat the tracker's title (off where the title is already the row's heading). */
  showTitle?: boolean;
}) => {
  const base = clsx("mt-0.5 text-[11.5px]", inset && "ml-4");
  if (!tracker.settled)
    return (
      <div className={clsx(base, "text-ink-faint")}>
        tracker open ·{" "}
        {showTitle ? <span className="num">{tracker.title}</span> : "waiting for the credit"}
      </div>
    );
  return (
    <div className={clsx(base, "text-teal-400")}>
      settled ·{" "}
      {tracker.settledBy === "bank-credit" && tracker.slipTransaction ? (
        <span className="num">
          {tracker.slipTransaction.name} −฿{Math.abs(tracker.slipTransaction.amount).toFixed(2)}
        </span>
      ) : (
        <>transferred by Takumi{tracker.transferredAt ? ` · ${fmtDay(tracker.transferredAt)}` : ""}</>
      )}
    </div>
  );
};

// ─── format ───────────────────────────────────────────────────────────────

const MON = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];

const fmtDay = (iso: string) => {
  const [, m, d] = iso.split("-").map(Number);
  return `${d} ${MON[m - 1]}`;
};

/** `1–31 May` · `25 Apr – 24 May` */
export const fmtWindow = (start: string, end: string) => {
  const [, sm, sd] = start.split("-").map(Number);
  const [, em, ed] = end.split("-").map(Number);
  return sm === em ? `${sd}–${ed} ${MON[em - 1]}` : `${sd} ${MON[sm - 1]} – ${ed} ${MON[em - 1]}`;
};

/** Whole baht stay whole; anything with satang shows both digits (8,001.50). */
const fmtB = (n: number) =>
  n.toLocaleString("en-US", { minimumFractionDigits: Number.isInteger(n) ? 0 : 2, maximumFractionDigits: 2 });

/** Compact baht for ruler labels: 8001.5 → "8,001.50"; 40000 → "40k". */
const fmtK = (n: number) => {
  if (n >= 10_000 && n % 1_000 === 0) return `${n / 1_000}k`;
  return n.toLocaleString("en-US", { minimumFractionDigits: Number.isInteger(n) ? 0 : 2, maximumFractionDigits: 2 });
};
