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
        // The palette is intentionally narrow.
        // Background = warm near-black; surface = a touch lifted; ink = warm cream;
        // amber = primary accent; teal = paid/done; coral = due/danger.
        ink: {
          // The text-on-dark layer. Warm cream → not pure white.
          DEFAULT: "#F2EBDD",
          dim: "#C7BFAD",
          faint: "#8A8472",
          ghost: "#5A5547",
        },
        paper: {
          // Background layers, warm dark.
          DEFAULT: "#0d0b08",
          raised: "#161310",
          high: "#1f1a14",
          line: "#2a241c",
        },
        amber: {
          50: "#fcf3df",
          100: "#f7e3b1",
          200: "#f1cd75",
          300: "#e9b242",
          400: "#d99316",
          500: "#b87510",
          600: "#8e570a",
          glow: "#f7c463",
        },
        teal: {
          400: "#7ec8b5",
          500: "#56a991",
          600: "#3c8775",
        },
        coral: {
          400: "#f08977",
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
