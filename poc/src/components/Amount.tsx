import clsx from "clsx";
import { formatBaht } from "../data/format";

interface Props {
  value: number;
  /** When true (default for credits), shows a leading "−" instead of "-". */
  signed?: boolean;
  /** Hairline currency mark before the number. */
  symbol?: boolean;
  className?: string;
  tone?: "default" | "credit" | "debit" | "muted";
  size?: "sm" | "md" | "lg" | "xl";
}

/**
 * Mono, tabular figures, hairline currency mark.
 * The defining "voice" of every amount across the app.
 */
export const Amount = ({
  value,
  signed = true,
  symbol = true,
  className,
  tone,
  size = "md",
}: Props) => {
  const negative = value < 0;
  const auto = tone ?? (negative ? "credit" : "default");

  return (
    <span
      className={clsx(
        "num inline-flex items-baseline",
        size === "sm" && "text-sm",
        size === "md" && "text-base",
        size === "lg" && "text-2xl",
        size === "xl" && "font-display text-display-lg font-normal tracking-tight",
        auto === "credit" && "text-teal-400",
        auto === "debit" && "text-coral-400",
        auto === "muted" && "text-ink-faint",
        className,
      )}
    >
      {signed && negative && <span aria-hidden>−</span>}
      {symbol && (
        <span
          className={clsx(
            "mr-1 align-baseline",
            size === "xl" ? "text-[0.42em] tracking-widest" : "text-[0.7em]",
            "font-sans uppercase text-ink-faint",
          )}
        >
          ฿
        </span>
      )}
      {formatBaht(value)}
    </span>
  );
};
