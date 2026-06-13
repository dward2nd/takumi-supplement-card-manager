import clsx from "clsx";
import type { Card, HolderKey } from "../data/types";
import { last4For } from "../data/cards";
import { formatBahtInt } from "../data/format";

interface Props {
  card: Card;
  /** The holder whose physical card-instance we're rendering. */
  holder: HolderKey;
  /** Show lifetime points + utilisation strip. Defaults to true on detail screens. */
  showOverall?: boolean;
  className?: string;
  size?: "sm" | "md" | "lg";
  withBlurb?: boolean;
}

/**
 * The miniaturised credit-card face. Renders one **holder's** supplement
 * of a card — distinct last-4 per holder. Optional `showOverall` paints a
 * utilisation strip + lifetime-points readout on the bottom band, used on
 * the card-detail screen where the face represents the card's overall
 * (not this-cycle) state.
 *
 * The "lustre" line is a CSS-only diagonal gradient that gives the face
 * a material feel — not just a flat rectangle.
 */
export const CardFace = ({
  card,
  holder,
  showOverall = false,
  className,
  size = "md",
  withBlurb = false,
}: Props) => {
  const [from, to] = card.brandColors;
  const last4 = last4For(card, holder);
  const lifetimePoints = card.holderLifetimePoints?.[holder];
  const balance = card.holderCurrentBalance?.[holder] ?? 0;
  const limit = card.creditLimit ?? 0;
  const usage = limit > 0 ? Math.min(1, Math.max(0, balance / limit)) : 0;

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
      {/* Lustre — diagonal sheen */}
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
      {/* Embossed corner glyph */}
      <span
        aria-hidden
        className="absolute -right-6 -bottom-6 font-display text-[7rem] font-normal leading-none text-white/5 select-none"
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
                  : card.issuer === "KBank"
                    ? "K"
                    : card.issuer === "AEON"
                      ? "A"
                      : card.issuer === "Lotus"
                        ? "L"
                        : "S"}
      </span>

      <div className="relative flex h-full flex-col justify-between text-white">
        {/* Top block — issuer eyebrow + card name + network badge */}
        <div className="flex items-start justify-between gap-2">
          <div className="min-w-0">
            <div className="text-[12px] uppercase tracking-[0.22em] text-white/65">
              {card.issuer}
            </div>
            <div
              className={clsx(
                "mt-1 font-display font-normal tracking-tight",
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
            <span className="shrink-0 rounded-full border border-white/20 px-2 py-0.5 text-[11px] uppercase tracking-[0.18em] text-white/70">
              {card.network}
            </span>
          )}
        </div>

        {/*
          Middle block — always rendered at md+ so every card on a page has
          the same vertical content rhythm. Shows the holder's current
          outstanding balance on this card (the daily-use "how much do I
          owe" answer). Falls back to ฿ 0 for cards with no balance.
        */}
        {size !== "sm" && (
          <div className="leading-tight">
            <div className="text-[10.5px] uppercase tracking-[0.22em] text-white/55">
              {/* A negative balance is a credit (advance payment / cashback-heavy
                  cards like AEON UnionPay sit in credit) — label it as such so
                  formatBahtInt's unsigned figure doesn't read as debt. */}
              {balance < 0 ? "in credit" : "outstanding"}
            </div>
            <div className="num mt-0.5 text-base text-white/95">
              ฿ {formatBahtInt(balance)}
            </div>
          </div>
        )}

        {/* Bottom block — utilisation + last4 + lifetime points / points default */}
        <div>
          {showOverall && limit > 0 && (
            <div className="mb-2">
              <div className="mb-1 flex items-baseline justify-between text-[11px] uppercase tracking-[0.2em] text-white/60">
                <span>credit used</span>
                <span className="num text-white/80">
                  <span className="num">{Math.round(usage * 100)}%</span>
                  <span className="text-white/40"> · ฿ {formatBahtInt(limit)}</span>
                </span>
              </div>
              <div className="h-1 w-full overflow-hidden rounded-full bg-white/10">
                <div
                  className={clsx(
                    "h-full rounded-full transition-all duration-700",
                    usage > 0.85
                      ? "bg-coral-400"
                      : usage > 0.6
                        ? "bg-amber-200"
                        : "bg-white/80",
                  )}
                  style={{ width: `${Math.max(usage * 100, 2)}%` }}
                />
              </div>
            </div>
          )}

          <div className="flex items-end justify-between gap-3">
            <div className="num text-sm tracking-[0.3em] text-white/70">
              •••• {last4}
            </div>

            {showOverall && lifetimePoints !== undefined && lifetimePoints > 0 ? (
              <div className="text-right">
                <div className="text-[10.5px] uppercase tracking-[0.2em] text-white/55">
                  lifetime pts
                </div>
                <div className="num text-base font-medium text-white/95">
                  {lifetimePoints.toLocaleString("en-US")}
                </div>
              </div>
            ) : card.pointsDefault ? (
              <div className="text-right">
                <div className="text-[10.5px] uppercase tracking-[0.2em] text-white/55">
                  points
                </div>
                <div className="font-display text-base font-normal text-white/85">
                  {card.pointsDefault}
                </div>
              </div>
            ) : (
              <div className="text-right">
                <div className="text-[10.5px] uppercase tracking-[0.2em] text-white/55">
                  points
                </div>
                <div className="font-display text-base font-normal text-white/55">—</div>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
