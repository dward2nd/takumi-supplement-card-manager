import clsx from "clsx";
import { HOLDER_LIST } from "../data/holders";
import type { HolderKey } from "../data/types";

export type HolderFilter = HolderKey | "all";

/**
 * Editorial-style holder filter chip. Used wherever a screen needs to scope
 * the visible data to one cardholder — picker bottom-sheets, Cards index,
 * history archives, etc. The active state uses the holder's accent colour
 * via inline style; "All" falls back to amber.
 */
export const HolderChip = ({
  label,
  count,
  dot,
  accent,
  active,
  onClick,
}: {
  label: string;
  count: number;
  dot: string;
  /** Holder's accent — null for the "All" chip (uses amber). */
  accent: string | null;
  active: boolean;
  onClick: () => void;
}) => {
  const activeStyle =
    active && accent
      ? { borderColor: `${accent}66`, background: `${accent}1a` }
      : undefined;
  return (
    <button
      onClick={onClick}
      aria-pressed={active}
      className={clsx(
        "tap shrink-0 flex items-center gap-2 rounded-full border px-3.5 transition-colors",
        active
          ? accent
            ? "text-ink"
            : "border-amber-200/40 bg-amber-300/[0.08] text-ink"
          : "border-paper-line bg-paper-raised/40 text-ink-dim hover:bg-paper-raised hover:text-ink",
      )}
      style={activeStyle}
    >
      <span
        aria-hidden
        className="h-1.5 w-1.5 shrink-0 rounded-full"
        style={{ background: dot }}
      />
      <span className="text-[12.5px] uppercase tracking-[0.2em]">{label}</span>
      <span className="num text-[12px] text-ink-faint">{count}</span>
    </button>
  );
};

/**
 * Convenience row: an "All" chip followed by one chip per holder.
 * Counts are derived by the caller from whatever scope they care about
 * (typically the full unfiltered list). Hide the row entirely when only a
 * single holder is in play — there's nothing to filter.
 */
export const HolderChipRow = ({
  counts,
  total,
  active,
  onChange,
  /** Filter the holder list (e.g. omit Takumi for Bills, who has no Bills DB). */
  include = HOLDER_LIST,
  className,
}: {
  counts: Record<HolderKey, number>;
  total: number;
  active: HolderFilter;
  onChange: (f: HolderFilter) => void;
  include?: typeof HOLDER_LIST;
  className?: string;
}) => (
  <div
    className={clsx(
      "-mx-1 flex gap-2 overflow-x-auto px-1 [-ms-overflow-style:none] [scrollbar-width:none] [&::-webkit-scrollbar]:hidden",
      className,
    )}
  >
    <HolderChip
      label="All"
      count={total}
      dot="rgb(var(--amber-glow))"
      active={active === "all"}
      accent={null}
      onClick={() => onChange("all")}
    />
    {include.map((h) => (
      <HolderChip
        key={h.key}
        label={h.englishName}
        count={counts[h.key]}
        dot={h.accent}
        accent={h.accent}
        active={active === h.key}
        onClick={() => onChange(h.key)}
      />
    ))}
  </div>
);
