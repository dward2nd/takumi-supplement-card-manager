import { TRANSACTIONS } from "./transactions";
import type { Bill, CardId, HolderKey, StatementBreakdown, Transaction } from "./types";

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

// ─── Takumi's statement-driven bills (Bills DB since 2026-09-27) ────────────
//
// One row per card per bank statement, at the printed card total — his
// principal plus every supplement section. Every statement line lives in
// exactly one ledger, so Σ Takumi's rows + Σ the friends' statement lines
// (+ any untracked supplement) = the printed total. No [DRAFT] estimate:
// /prepare-bill refuses him. He pays the bank himself (Krungsri-family cards
// by auto-debit, the rest by transfer); the friends' parts are what they owe him.

// Payment rows (ชำระบิลเต็มจำนวน / ชำระบางส่วน / AUTO DEBIT) and Takumi's
// โอนยอดจาก<friend> transfers. Not "PAYMENT" in general — `AIATH AUTO PAYMENT`
// is a purchase.
const PAYMENT_ROW = /^ชำระ|^AUTO DEBIT\b|^โอนยอดจาก/;

/**
 * Is this ledger row a line the bank printed? Household-only rows — the
 * computed `UOB ONE CASHBACK n%` credits, payments, `[ยอดยกมา…]` carry-forwards,
 * `[เว็บรับหนี้…]` offsets — are not; `[บัตรหลัก]` rows (a friend's spend on
 * the primary card) are. Mirrors `lib.statements.attribution.is_statement_line_row`.
 */
export const isStatementLine = (t: Transaction): boolean => {
  const name = t.name.trim();
  if (/^UOB ONE CASHBACK/i.test(name)) return false;
  if (PAYMENT_ROW.test(name)) return false;
  if (name.startsWith("[") && !name.startsWith("[บัตรหลัก]")) return false;
  return true;
};

/** The statement lines of one holder's ledger on a card for one cycle. */
export const statementLinesFor = (holder: HolderKey, cardId: CardId, billCycleDate: string) =>
  TRANSACTIONS.filter(
    (t) => t.holder === holder && t.cardId === cardId && t.billCycleDate === billCycleDate && isStatementLine(t),
  );

const sum2 = (txs: Transaction[]) => Math.round(txs.reduce((s, t) => s + t.amount, 0) * 100) / 100;

/** Build the breakdown from the ledgers — the identity the statement proves. */
const breakdownFromLedgers = (cardId: CardId, bc: string): StatementBreakdown => {
  const b: StatementBreakdown = { takumi: sum2(statementLinesFor("takumi", cardId, bc)) };
  const baiboon = sum2(statementLinesFor("baiboon", cardId, bc));
  const nuta = sum2(statementLinesFor("nuta", cardId, bc));
  if (baiboon) b.baiboon = baiboon;
  if (nuta) b.nuta = nuta;
  return b;
};

export const breakdownTotal = (b: StatementBreakdown) =>
  Math.round(((b.takumi ?? 0) + (b.baiboon ?? 0) + (b.nuta ?? 0) + (b.untracked ?? 0)) * 100) / 100;

const statementBill = (
  b: Omit<Bill, "amount" | "source" | "holder" | "breakdown" | "isDraft"> & { breakdown?: StatementBreakdown },
): Bill => {
  const breakdown = b.breakdown ?? breakdownFromLedgers(b.cardId, b.billCycleDate);
  return {
    ...b,
    holder: "takumi",
    source: "statement",
    isDraft: false,
    breakdown,
    amount: breakdownTotal(breakdown),
  };
};

const TAKUMI_BILLS: Bill[] = [
  // Statements in for cycle 2026-05-25, not yet paid.
  statementBill({
    id: "bill-takumi-uo-2026-05",
    cardId: "uob-one",
    billCycleDate: "2026-05-25",
    dueDate: "2026-06-15",
    status: "issued",
    hasStatementPdf: true,
    paidVia: "transfer",
  }),
  statementBill({
    id: "bill-takumi-uw-2026-05",
    cardId: "uob-world",
    billCycleDate: "2026-05-25",
    dueDate: "2026-06-15",
    status: "issued",
    hasStatementPdf: true,
    paidVia: "transfer",
  }),

  // Paid history. Lines for these cycles aren't in the POC's mock slice, so
  // the breakdown is given as the statement split it.
  statementBill({
    id: "bill-takumi-lb-2026-05",
    cardId: "lotuss-beyond",
    billCycleDate: "2026-05-05",
    dueDate: "2026-05-25",
    status: "paid",
    paidAt: "2026-05-25",
    paidVia: "auto-debit",
    hasStatementPdf: true,
    breakdown: { takumi: 3_104.25, baiboon: 486, untracked: 1_840 },
    note: "AUTO DEBIT on the due date. The untracked supplement's part is a โอนยอดจากบัตรเสริม row in Takumi's ledger.",
  }),
  statementBill({
    id: "bill-takumi-fc-2026-04",
    cardId: "first-choice",
    billCycleDate: "2026-04-05",
    dueDate: "2026-04-25",
    status: "paid",
    paidAt: "2026-04-25",
    paidVia: "auto-debit",
    hasStatementPdf: true,
    breakdown: { takumi: 2_210.4, baiboon: 18_744.15, nuta: 1_312.5 },
  }),
  statementBill({
    id: "bill-takumi-ktcm-2026-04",
    cardId: "ktc-mastercard",
    billCycleDate: "2026-04-27",
    dueDate: "2026-05-12",
    status: "paid",
    paidAt: "2026-05-10",
    paidVia: "transfer",
    hasStatementPdf: true,
    hasSlip: true,
    breakdown: { takumi: 1_545.3 },
    note: "KTC prints one PDF per card number — principal only.",
  }),
];

BILLS.push(...TAKUMI_BILLS);

export const billsFor = (holder: HolderKey) =>
  BILLS.filter((b) => b.holder === holder);

/** Due date for a bill — the printed one when known, else the POC's UOB convention. */
export const billDueDate = (b: Bill): string =>
  b.dueDate ?? (b.billCycleDate === "2026-05-25" ? "2026-06-15" : b.billCycleDate);
