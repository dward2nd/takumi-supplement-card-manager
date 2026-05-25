import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import clsx from "clsx";
import { HOLDER_LIST } from "../data/holders";
import { useApp } from "../data/state";

/**
 * Editorial cover page. The three holders are introduced like dramatis personae
 * in a play programme: typography-driven, generous spacing, a strong serif italic.
 */
export const LoginScreen = () => {
  const nav = useNavigate();
  const { setHolder } = useApp();

  return (
    <div className="top-safe relative flex min-h-dvh flex-col px-6 pb-12">
      {/* Issue line — masthead-style */}
      <div className="flex items-center justify-between text-[10px] uppercase tracking-[0.32em] text-ink-faint">
        <span>Vol. I &nbsp;&middot;&nbsp; phase ii</span>
        <span className="num">2026 / V</span>
      </div>

      {/* Display title — overlapped, asymmetric */}
      <div className="relative mt-12">
        <div className="text-[11px] uppercase tracking-[0.32em] text-amber-glow/90">
          บัตรเสริม &nbsp;&middot;&nbsp; supplement&nbsp;card&nbsp;journal
        </div>
        <motion.h1
          initial={{ opacity: 0, y: 18 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6, ease: [0.2, 0.7, 0.1, 1] }}
          className="mt-4 font-display text-display-xl font-light leading-[0.92] tracking-[-0.04em] text-ink"
        >
          who, <em className="italic font-thin text-amber-glow">today,</em>
          <br />
          is keeping
          <br />
          the books?
        </motion.h1>
        <p className="mt-5 max-w-[26ch] text-sm leading-relaxed text-ink-dim">
          A daily journal for three people who share one wallet but not one set of
          numbers. Pick yourself to begin.
        </p>
      </div>

      <div className="mt-12 flex-1 space-y-3">
        {HOLDER_LIST.map((h, idx) => (
          <motion.button
            key={h.key}
            initial={{ opacity: 0, x: -10 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.25 + idx * 0.08, duration: 0.5, ease: [0.2, 0.7, 0.1, 1] }}
            onClick={() => {
              setHolder(h.key);
              nav("/home");
            }}
            className={clsx(
              "tap group relative flex w-full items-center justify-between gap-4",
              "overflow-hidden rounded-2xl border border-paper-line bg-paper-raised/70 px-5 py-5",
              "text-left transition-all duration-300",
              "hover:border-paper-line/0 hover:bg-paper-high",
              "active:scale-[0.99]",
            )}
          >
            {/* Accent bar at the leading edge */}
            <span
              aria-hidden
              className="absolute inset-y-3 left-0 w-[3px] rounded-r-full"
              style={{ background: h.accent }}
            />
            <span
              aria-hidden
              className="absolute -right-12 -bottom-12 font-display text-[10rem] font-light leading-none text-ink/[0.04] transition-transform duration-700 group-hover:translate-x-2"
            >
              {h.initial}
            </span>

            <div className="relative flex items-center gap-4">
              <span
                className="flex h-12 w-12 items-center justify-center rounded-full text-lg font-medium text-paper"
                style={{ background: h.accent }}
              >
                {h.initial}
              </span>
              <div>
                <div className="font-display text-xl font-light tracking-tight text-ink">
                  {h.englishName}
                </div>
                <div className="text-xs uppercase tracking-[0.18em] text-ink-faint">
                  {h.thaiName}
                  {h.isAdmin && <span className="ml-2 text-amber-glow">· admin</span>}
                </div>
              </div>
            </div>

            <span className="relative text-[10px] uppercase tracking-[0.22em] text-ink-faint transition-transform duration-300 group-hover:translate-x-1">
              enter →
            </span>
          </motion.button>
        ))}
      </div>

      <div className="rule mt-10" />
      <div className="mt-6 flex items-baseline justify-between text-[10px] uppercase tracking-[0.22em] text-ink-faint">
        <span>POC · mock data only</span>
        <span className="num">N.{HOLDER_LIST.length}</span>
      </div>
    </div>
  );
};
