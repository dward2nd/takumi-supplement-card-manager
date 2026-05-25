import clsx from "clsx";
import { ReactNode } from "react";

interface Props {
  children: ReactNode;
  trailing?: ReactNode;
  className?: string;
  number?: string;
}

/** The eyebrow row above each section — numbered, tracked-out caps. */
export const SectionLabel = ({ children, trailing, className, number }: Props) => (
  <div className={clsx("flex items-baseline justify-between gap-3", className)}>
    <div className="flex items-baseline gap-3 text-ink-faint">
      {number && (
        <span className="num text-[12px] tabular-nums text-amber-glow/80">{number}</span>
      )}
      <span className="text-[13px] uppercase tracking-[0.22em]">{children}</span>
    </div>
    {trailing && <span className="text-[13px] text-ink-faint">{trailing}</span>}
  </div>
);
