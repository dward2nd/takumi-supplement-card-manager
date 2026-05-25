import clsx from "clsx";
import { ReactNode } from "react";

type Tone = "amber" | "teal" | "coral" | "neutral" | "ghost";

interface Props {
  children: ReactNode;
  tone?: Tone;
  className?: string;
  uppercase?: boolean;
}

export const Pill = ({ children, tone = "neutral", className, uppercase = true }: Props) => (
  <span
    className={clsx(
      "inline-flex items-center gap-1.5 rounded-full border px-2.5 py-1 text-[12px] leading-none",
      uppercase && "uppercase tracking-[0.14em]",
      // Accent text uses the theme-aware `--amber-glow / --teal-400 / --coral-400`
      // variables so the text darkens enough on the cream paper of light mode.
      tone === "amber" && "border-amber-300/40 bg-amber-300/15 text-amber-glow",
      tone === "teal" && "border-teal-400/40 bg-teal-400/15 text-teal-400",
      tone === "coral" && "border-coral-400/40 bg-coral-400/15 text-coral-400",
      tone === "neutral" && "border-paper-line bg-paper-raised text-ink-dim",
      tone === "ghost" && "border-transparent text-ink-faint",
      className,
    )}
  >
    {children}
  </span>
);
