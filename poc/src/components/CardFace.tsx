import clsx from "clsx";
import type { Card } from "../data/types";
import { formatBahtInt } from "../data/format";

interface Props {
  card: Card;
  outstanding?: number;
  className?: string;
  size?: "sm" | "md" | "lg";
  withBlurb?: boolean;
}

/**
 * The miniaturised credit-card face. The "lustre" line is a CSS-only
 * gradient sheen that makes the card feel material rather than flat.
 */
export const CardFace = ({
  card,
  outstanding,
  className,
  size = "md",
  withBlurb = false,
}: Props) => {
  const [from, to] = card.brandColors;
  return (
    <div
      className={clsx(
        "relative isolate w-full overflow-hidden rounded-2xl",
        "shadow-inner-line",
        "transition-transform duration-700 ease-editorial will-change-transform",
        size === "sm" && "aspect-[16/9] min-h-[110px] p-3",
        size === "md" && "aspect-[16/10] min-h-[160px] p-5",
        size === "lg" && "aspect-[5/3] min-h-[200px] p-6",
        className,
      )}
      style={{
        background: `linear-gradient(135deg, ${from} 0%, ${to} 100%)`,
      }}
    >
      {/* Lustre line — the diagonal sheen */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 opacity-60 mix-blend-overlay"
        style={{
          background:
            "linear-gradient(115deg, transparent 35%, rgba(255,255,255,0.18) 50%, transparent 65%)",
        }}
      />
      {/* Hairline border */}
      <span
        aria-hidden
        className="pointer-events-none absolute inset-0 rounded-2xl ring-1 ring-inset ring-white/10"
      />
      {/* Embossed corner glyph — issuer-specific */}
      <span
        aria-hidden
        className="absolute -right-6 -bottom-6 font-display text-[7rem] font-light leading-none text-white/5 select-none"
      >
        {card.issuer === "UOB"
          ? "u"
          : card.issuer === "Krungsri"
            ? "K"
            : card.issuer === "CardX"
              ? "X"
              : card.issuer === "KTC"
                ? "k"
                : card.issuer === "ttb"
                  ? "t"
                  : card.issuer === "AEON"
                    ? "A"
                    : card.issuer === "Lotus"
                      ? "L"
                      : "S"}
      </span>

      <div className="relative flex h-full flex-col justify-between text-white">
        <div className="flex items-start justify-between">
          <div>
            <div className="text-[10px] uppercase tracking-[0.22em] text-white/65">
              {card.issuer}
            </div>
            <div
              className={clsx(
                "mt-1 font-display font-light tracking-tight",
                size === "lg" ? "text-2xl" : "text-lg",
              )}
            >
              {card.name}
            </div>
            {withBlurb && card.blurb && (
              <div className="mt-1 max-w-[90%] text-xs text-white/60">{card.blurb}</div>
            )}
          </div>
          {card.network && (
            <span className="rounded-full border border-white/20 px-2 py-0.5 text-[9px] uppercase tracking-[0.18em] text-white/70">
              {card.network}
            </span>
          )}
        </div>

        <div className="flex items-end justify-between gap-3">
          <div>
            <div className="num text-sm tracking-[0.3em] text-white/70">
              •••• {card.last4}
            </div>
            {outstanding !== undefined && (
              <div className="mt-2 text-[10px] uppercase tracking-[0.18em] text-white/55">
                cycle outstanding
              </div>
            )}
            {outstanding !== undefined && (
              <div className="num text-xl font-medium text-white">
                ฿ {formatBahtInt(outstanding)}
              </div>
            )}
          </div>

          {card.pointsDefault && (
            <div className="text-right">
              <div className="text-[9px] uppercase tracking-[0.18em] text-white/55">
                points
              </div>
              <div className="font-display text-base font-light text-white/85">
                {card.pointsDefault}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
