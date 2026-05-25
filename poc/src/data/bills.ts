import type { Bill } from "./types";

// Reflects what /prepare-bill wrote in the live data: three drafts at
// cycle 2026-05-25, plus a few historical paid bills for context.
export const BILLS: Bill[] = [
  // Current cycle drafts (BC 2026-05-25, DD 2026-06-15)
  {
    id: "bill-baiboon-uw-2026-05",
    holder: "baiboon",
    cardId: "uob-world",
    billCycleDate: "2026-05-25",
    amount: 1802,
    status: "draft",
    isDraft: true,
  },
  {
    id: "bill-baiboon-uo-2026-05",
    holder: "baiboon",
    cardId: "uob-one",
    billCycleDate: "2026-05-25",
    amount: 558.57,
    status: "draft",
    isDraft: true,
  },
  {
    id: "bill-nuta-uo-2026-05",
    holder: "nuta",
    cardId: "uob-one",
    billCycleDate: "2026-05-25",
    amount: 8041.39,
    status: "draft",
    isDraft: true,
  },

  // Historical (paid)
  {
    id: "bill-baiboon-uo-2026-04",
    holder: "baiboon",
    cardId: "uob-one",
    billCycleDate: "2026-04-24",
    amount: 809,
    status: "paid",
    isDraft: false,
    paidAt: "2026-05-10",
    hasStatementPdf: true,
    hasSlip: true,
  },
  {
    id: "bill-nuta-uo-2026-04",
    holder: "nuta",
    cardId: "uob-one",
    billCycleDate: "2026-04-24",
    amount: 17611.21,
    status: "paid",
    isDraft: false,
    paidAt: "2026-05-08",
    hasStatementPdf: true,
    hasSlip: true,
  },
  {
    id: "bill-baiboon-uw-2026-04",
    holder: "baiboon",
    cardId: "uob-world",
    billCycleDate: "2026-04-24",
    amount: 2317.5,
    status: "paid",
    isDraft: false,
    paidAt: "2026-05-09",
    hasStatementPdf: true,
    hasSlip: true,
  },
  {
    id: "bill-baiboon-fc-2026-05",
    holder: "baiboon",
    cardId: "first-choice",
    billCycleDate: "2026-05-05",
    amount: 1402.6,
    status: "paid",
    isDraft: false,
    paidAt: "2026-05-22",
    hasStatementPdf: true,
    hasSlip: true,
  },
  {
    id: "bill-nuta-cardx-2026-05",
    holder: "nuta",
    cardId: "cardx-jcb",
    billCycleDate: "2026-05-05",
    amount: 0,
    status: "paid",
    isDraft: false,
    paidAt: "2026-05-23",
    note: "Zero balance this cycle.",
  },
];

export const billsFor = (holder: import("./types").HolderKey) =>
  BILLS.filter((b) => b.holder === holder);
