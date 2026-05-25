import { ReactNode } from "react";
import { useNavigate } from "react-router-dom";
import { ArrowLeft } from "lucide-react";

interface Props {
  title: string;
  eyebrow?: string;
  /**
   * Subordinate possessive tag to render *before* the title, smaller and lower-
   * contrast — e.g. "Baiboon's". The card name (title) stays the visual lead;
   * this just gives possessive context when admin views someone else's instance.
   */
  ownershipTag?: { label: string; accent?: string };
  trailing?: ReactNode;
  back?: boolean | string;
}

/** Editorial top — a kicker line, a serif title, optional right slot. */
export const PageHeader = ({ title, eyebrow, ownershipTag, trailing, back }: Props) => {
  const nav = useNavigate();
  return (
    <header className="top-safe px-5 pb-4">
      <div className="flex items-center justify-between gap-3">
        {back ? (
          <button
            onClick={() => (typeof back === "string" ? nav(back) : nav(-1))}
            className="tap -ml-2 flex items-center gap-1 rounded-full px-2 py-1 text-ink-dim transition-colors hover:text-ink"
            aria-label="back"
          >
            <ArrowLeft size={16} strokeWidth={1.5} />
            <span className="text-xs uppercase tracking-[0.18em]">back</span>
          </button>
        ) : (
          <div />
        )}
        {trailing}
      </div>
      <div className="mt-3">
        {eyebrow && (
          <div className="text-[12px] uppercase tracking-[0.28em] text-amber-glow/90">
            {eyebrow}
          </div>
        )}
        {ownershipTag && (
          // Separate line above the title — subordinate weight, italic, holder
          // accent. Aligns cleanly with the title's left edge.
          <div
            className="font-display text-lg italic font-normal leading-tight text-ink-dim"
            style={ownershipTag.accent ? { color: ownershipTag.accent + "cc" } : undefined}
          >
            {ownershipTag.label}
          </div>
        )}
        <h1 className="font-display text-3xl font-normal leading-[1.02] tracking-tight text-ink">
          {title}
        </h1>
      </div>
    </header>
  );
};
