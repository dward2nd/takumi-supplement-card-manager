import type { Config } from "tailwindcss";

export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      fontFamily: {
        // Display: variable serif with strong italic. Used for big numbers + headings.
        display: ['"Fraunces"', "ui-serif", "Georgia", "serif"],
        // Body: humanist sans with first-class Thai support.
        sans: ['"IBM Plex Sans Thai Looped"', '"IBM Plex Sans"', "ui-sans-serif", "system-ui", "sans-serif"],
        // Mono: tabular figures for amounts. Plex Mono is condensed and unambiguous.
        mono: ['"IBM Plex Mono"', "ui-monospace", "Menlo", "monospace"],
      },
      colors: {
        // Palette is intentionally narrow. The neutral scales (ink / paper)
        // come from CSS variables so the same `text-ink-dim` / `bg-paper`
        // classes resolve to the correct value under either theme. The
        // accents (amber / teal / coral) are kept as fixed hues — brand
        // colour identity stays consistent across modes.
        //
        // Variable definitions live in src/index.css under :root (dark) and
        // .theme-light. Toggle by adding/removing `.theme-light` on <html>.
        /*
         * `rgb(var(--xxx) / <alpha-value>)` is the form Tailwind v3 understands
         * for opacity modifiers — `bg-paper/85` becomes `rgb(var(--paper) / 0.85)`.
         * Variables in index.css must be space-separated RGB triplets for this
         * to compose correctly.
         */
        ink: {
          DEFAULT: "rgb(var(--ink) / <alpha-value>)",
          dim: "rgb(var(--ink-dim) / <alpha-value>)",
          faint: "rgb(var(--ink-faint) / <alpha-value>)",
          ghost: "rgb(var(--ink-ghost) / <alpha-value>)",
        },
        paper: {
          DEFAULT: "rgb(var(--paper) / <alpha-value>)",
          raised: "rgb(var(--paper-raised) / <alpha-value>)",
          high: "rgb(var(--paper-high) / <alpha-value>)",
          line: "rgb(var(--paper-line) / <alpha-value>)",
        },
        /** Stable dark token for text on amber/teal/coral surfaces in any theme. */
        "on-accent": "#0d0b08",
        amber: {
          50: "#fcf3df",
          100: "#f7e3b1",
          200: "#f1cd75",
          300: "#e9b242",
          400: "#d99316",
          500: "#b87510",
          600: "#8e570a",
          glow: "rgb(var(--amber-glow) / <alpha-value>)",
        },
        teal: {
          400: "rgb(var(--teal-400) / <alpha-value>)",
          500: "#56a991",
          600: "#3c8775",
        },
        coral: {
          400: "rgb(var(--coral-400) / <alpha-value>)",
          500: "#d96650",
          600: "#b14a37",
        },
      },
      fontSize: {
        // Editorial-scale display sizes.
        "display-xl": ["clamp(3rem, 14vw, 5.5rem)", { lineHeight: "0.95", letterSpacing: "-0.04em" }],
        "display-lg": ["clamp(2.25rem, 9vw, 3.5rem)", { lineHeight: "0.95", letterSpacing: "-0.035em" }],
        "display-md": ["1.875rem", { lineHeight: "1.05", letterSpacing: "-0.025em" }],
      },
      boxShadow: {
        "glow-amber": "0 0 0 1px rgba(247,196,99,0.35), 0 8px 30px -10px rgba(247,196,99,0.4)",
        "inner-line": "inset 0 0 0 1px rgba(242,235,221,0.06)",
      },
      animation: {
        "fade-up": "fadeUp 0.5s cubic-bezier(0.2, 0.7, 0.1, 1) both",
        "spin-slow": "spin 24s linear infinite",
      },
      keyframes: {
        fadeUp: {
          "0%": { opacity: "0", transform: "translateY(8px)" },
          "100%": { opacity: "1", transform: "translateY(0)" },
        },
      },
      transitionTimingFunction: {
        editorial: "cubic-bezier(0.2, 0.7, 0.1, 1)",
      },
    },
  },
  plugins: [],
} satisfies Config;
