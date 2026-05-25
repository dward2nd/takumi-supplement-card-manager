import type { Promotion } from "./types";

// Promotions seeded from scripts/repositories/promotions/.
// The First Choice May 2026 promo is added here for the POC (user mentioned
// it during the session even though it's not yet in the YAML repository).
export const PROMOTIONS: Promotion[] = [
  {
    id: "uob-one-2026",
    name: "UOB One 2026 cashback",
    cardId: "uob-one",
    effectiveStart: "2026-01-01",
    effectiveEnd: "2026-12-31",
    status: "active",
    pointsDefault: "×0",
    foreignInThbPolicy: { default: "exclude", overrides: [] },
    tiers: [
      { rate: 0.1, label: "bonus", patterns: ["BTS", "MRT", "AMZ"] },
      {
        rate: 0.05,
        label: "bonus",
        patterns: ["7-11", "WATSON", "WWW.GRAB.COM", "GRABTAXI"],
        excludePatterns: ["TMN 7-11"],
      },
      { rate: 0.01, label: "base", patterns: ["*"] },
    ],
    installmentRule: { rate: 0.01, credited: "per_installment" },
    creditingSchedule: {
      "0.01": "bc_date",
      "0.05": "first_weekday_next_month",
      "0.10": "first_weekday_next_month",
    },
  },
  {
    id: "first-choice-may-2026",
    name: "First Choice 2% May 2026",
    cardId: "first-choice",
    effectiveStart: "2026-05-01",
    effectiveEnd: "2026-05-31",
    status: "active",
    foreignInThbPolicy: {
      default: "exclude",
      overrides: [
        { merchantSubstring: "AGODA", rate: 0.015, keepsPointsExclusion: true },
      ],
    },
    tiers: [{ rate: 0.02, label: "base", patterns: ["*"] }],
    installmentRule: { rate: 0, credited: "at_purchase" },
  },
];

export const activePromotionsFor = (cardId: string, dateISO: string) => {
  const d = dateISO;
  return PROMOTIONS.filter(
    (p) =>
      p.cardId === cardId &&
      p.status === "active" &&
      p.effectiveStart <= d &&
      (p.effectiveEnd === null || p.effectiveEnd >= d),
  );
};
