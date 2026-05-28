import type { CardId, HolderKey, Transaction } from "./types";
import { parseInstallmentName } from "./installments";

// A representative slice of cycle 2026-05-25 data, plus a few earlier rows
// so cycle-history views aren't empty. Real merchant strings (verbatim).

const tx = (
  id: string,
  holder: HolderKey,
  cardId: CardId,
  name: string,
  amount: number,
  transactionDate: string,
  billCycleDate: string,
  dueDate: string,
  extras: Partial<Transaction> = {},
): Transaction => {
  // Auto-derive the structured installment field from the merchant string.
  // Any new row whose name ends `NN/NN` lights up the installment surfaces
  // (TransactionRow pill, CardDetail's in-progress section, BillDetail's
  // bucketed sections) without per-row plumbing in the mock data.
  // An explicit `extras.installment` still wins.
  const auto = parseInstallmentName(name, Math.abs(amount));
  return {
    id,
    holder,
    cardId,
    name,
    amount,
    transactionDate,
    billCycleDate,
    dueDate,
    status: "processed",
    ...(auto ? { installment: auto } : {}),
    ...extras,
  };
};

const NUTA_UOB_CYCLE = (() => {
  // Compressed sample. Reflects the real cycle's tier mix.
  const bc = "2026-05-25";
  const dd = "2026-06-15";
  // Prior cycle — same UOB cadence, one month earlier. Used for the 02/10
  // rows of two ongoing installment plans so the in-progress section has
  // visible term progression (02 → 03).
  const prevBc = "2026-04-25";
  const prevDd = "2026-05-15";
  const rows: Transaction[] = [
    tx("n-uob-1", "nuta", "uob-one", "WWW.GRAB.COM BANGKOK TH", 111, "2026-04-23", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),
    tx("n-uob-2", "nuta", "uob-one", "TMN 7-11 BANGKOK TH", 133, "2026-04-24", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-3", "nuta", "uob-one", "(FOR SHOPEE) BANGKOK TH", 54, "2026-04-25", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-4", "nuta", "uob-one", "WWW.GRAB.COM BANGKOK TH", 27, "2026-04-25", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),
    tx("n-uob-5", "nuta", "uob-one", "WWW.GRAB.COM BANGKOK TH", 80, "2026-04-24", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),
    tx("n-uob-6", "nuta", "uob-one", "AIATH AUTO PAYMENT BANGKOK TH", 836, "2026-04-28", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-7", "nuta", "uob-one", "MINISO SIAM SQUARE BANGKOK TH", 259, "2026-05-02", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-8", "nuta", "uob-one", "LPTH*PF_LM_Sam Yan 32E Bangkok TH", 71.4, "2026-05-03", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-9", "nuta", "uob-one", "X CORP. PAID FEATURES BASTROP US", 95, "2026-05-12", bc, dd, {
      multiplier: "×0",
      note: "Foreign merchant (US) charged in THB — no cashback / points by default rule.",
    }),
    tx("n-uob-10", "nuta", "uob-one", "MO-MO PARADISE-MBK CEN BANGKOK TH", 658, "2026-05-17", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-11", "nuta", "uob-one", "SHOPEETH BANGKOK TH", 184, "2026-05-22", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-12", "nuta", "uob-one", "TMN 7-11 BANGKOK TH", 106, "2026-05-24", bc, dd, { cashbackPercent: 0.01, multiplier: "×0" }),
    tx("n-uob-13", "nuta", "uob-one", "WWW.GRAB.COM BANGKOK TH", 165, "2026-05-24", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),

    // Installments — current cycle 2026-05-25.
    // One brand-new plan (01/10) and two ongoing 10-term plans on the same
    // bank-side merchant string but different per-term amounts (plan
    // identity = per-term ฿). Plus one electronics plan mid-progression.
    // All earn 1% per the UOB One 2026 promo's installment_rule; ×0 because
    // UOB One never earns points.
    tx("n-uob-inst-shopee-a-01", "nuta", "uob-one", "2C2P *SHOPEE 01/10", 449.10, "2026-05-25", bc, dd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),
    tx("n-uob-inst-shopee-b-03", "nuta", "uob-one", "2C2P *SHOPEE 03/10", 1079.20, "2026-05-25", bc, dd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),
    tx("n-uob-inst-shopee-c-03", "nuta", "uob-one", "2C2P *SHOPEE 03/10", 373.00, "2026-05-25", bc, dd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),
    tx("n-uob-inst-com7-05", "nuta", "uob-one", "COM7-ID175-BN-CT-CHO 05/10", 959.00, "2026-05-25", bc, dd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),

    // Prior-cycle 02/10 rows for the three ongoing plans, so the
    // in-progress section shows real term progression (02 → 03).
    tx("n-uob-inst-shopee-b-02", "nuta", "uob-one", "2C2P *SHOPEE 02/10", 1079.20, "2026-04-24", prevBc, prevDd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),
    tx("n-uob-inst-shopee-c-02", "nuta", "uob-one", "2C2P *SHOPEE 02/10", 373.00, "2026-04-24", prevBc, prevDd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),
    tx("n-uob-inst-com7-04", "nuta", "uob-one", "COM7-ID175-BN-CT-CHO 04/10", 959.00, "2026-04-24", prevBc, prevDd, {
      cashbackPercent: 0.01,
      multiplier: "×0",
      note: "Installment transaction — per UOB One 2026 cashback promotion, 1% per installment row.",
    }),

    // Cashback credit rows (the ones we wrote earlier via /post-cashback-credits)
    tx("n-uob-cb-1", "nuta", "uob-one", "UOB ONE CASHBACK 1%", -60.61, bc, bc, dd, {
      multiplier: "×0",
      note: "Cycle 2026-05-25 cashback credit: 1% × 6061.40 = 60.61.",
    }),
    tx("n-uob-cb-5", "nuta", "uob-one", "UOB ONE CASHBACK 5%", -102.4, "2026-06-01", bc, dd, {
      multiplier: "×0",
      note: "Cycle 2026-05-25 cashback credit: 5% × 2048.00 = 102.40.",
    }),
  ];
  return rows;
})();

const BAIBOON_UOB_ONE = (() => {
  const bc = "2026-05-25";
  const dd = "2026-06-15";
  return [
    tx("b-uob-1", "baiboon", "uob-one", "AMZ_SD1524 GREEN FOR B BANGKOK TH", 70, "2026-04-28", bc, dd, { cashbackPercent: 0.10, multiplier: "×0" }),
    tx("b-uob-2", "baiboon", "uob-one", "[บัตรหลัก] 379 WATSONS CENTRAL PA BANGKOK TH", 431.34, "2026-04-28", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),
    tx("b-uob-3", "baiboon", "uob-one", "RMAMZ_RM4676 RY SUKHUM RAYONG TH", 70, "2026-04-29", bc, dd, { cashbackPercent: 0.10, multiplier: "×0" }),
    tx("b-uob-4", "baiboon", "uob-one", "WWW.GRAB.COM BANGKOK TH", 24, "2026-05-04", bc, dd, { cashbackPercent: 0.05, multiplier: "×0" }),
    tx("b-uob-cb-5", "baiboon", "uob-one", "UOB ONE CASHBACK 5%", -22.77, "2026-06-01", bc, dd, {
      multiplier: "×0",
      note: "Cycle 2026-05-25 cashback credit: 5% × 455.34 = 22.77.",
    }),
    tx("b-uob-cb-10", "baiboon", "uob-one", "UOB ONE CASHBACK 10%", -14.0, "2026-06-01", bc, dd, {
      multiplier: "×0",
      note: "Cycle 2026-05-25 cashback credit: 10% × 140.00 = 14.00.",
    }),
  ];
})();

const BAIBOON_UOB_WORLD = (() => {
  const bc = "2026-05-25";
  const dd = "2026-06-15";
  return [
    tx("b-uw-1", "baiboon", "uob-world", "TMN ISERVICECCP BANGKOK TH", 100, "2026-04-26", bc, dd),
    tx("b-uw-2", "baiboon", "uob-world", "TMN ISERVICECCP BANGKOK TH", 50, "2026-04-27", bc, dd),
    tx("b-uw-3", "baiboon", "uob-world", "TMN 7-11 BANGKOK TH", 501, "2026-04-29", bc, dd),
    tx("b-uw-4", "baiboon", "uob-world", "TMN 7-11 BANGKOK TH", 111, "2026-04-29", bc, dd),
    tx("b-uw-5", "baiboon", "uob-world", "Google YouTubePremium Mountain View USA", 359, "2026-04-30", bc, dd, {
      multiplier: "×0",
      note: "Foreign merchant (USA) charged in THB — no cashback/points.",
    }),
    tx("b-uw-6", "baiboon", "uob-world", "KFC3293-SPTT OR NA YAI CHANTHABURI TH", 19, "2026-05-01", bc, dd),
    tx("b-uw-7", "baiboon", "uob-world", "KFC3293-SPTT OR NA YAI CHANTHABURI TH", 69, "2026-05-01", bc, dd),
    tx("b-uw-8", "baiboon", "uob-world", "DONKI THANIYA PLAZA BANGKOK TH", 348, "2026-05-02", bc, dd),
    tx("b-uw-9", "baiboon", "uob-world", "RIMPING -MAYA CHIANGMAI TH", 66, "2026-05-03", bc, dd),
    tx("b-uw-10", "baiboon", "uob-world", "TMN 7-11 BANGKOK TH", 118, "2026-05-03", bc, dd),
    tx("b-uw-11", "baiboon", "uob-world", "TMN FAST FOOD BANGKOK TH", 39, "2026-05-02", bc, dd),
    tx("b-uw-12", "baiboon", "uob-world", "TMN 7-11 BANGKOK TH", 22, "2026-05-02", bc, dd),
  ];
})();

const BAIBOON_FIRST_CHOICE = (() => {
  const bc = "2026-06-05";
  const dd = "2026-06-25";
  return [
    tx("b-fc-1", "baiboon", "first-choice", "AGODA.COM THE QUARTE Internet SG", 2479.76, "2026-05-01", bc, dd, {
      cashbackPercent: 0.015,
      multiplier: "×0",
      note: "Per First Choice May 2026 promo: 1.5% cashback on Agoda (promo override of foreign-in-THB rule). Points still excluded (×0).",
    }),
    tx("b-fc-2", "baiboon", "first-choice", "[เว็บรับหนี้ไปบริหารต่อ] AGODA.COM THE QUARTE Internet SG", -2479.76, "2026-05-01", bc, dd, {
      note: "Debt-takeover offset — Takumi covers this charge.",
    }),
    tx("b-fc-3", "baiboon", "first-choice", "MINISO SIAM SQUARE BANGKOK TH", 200, "2026-05-02", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-4", "baiboon", "first-choice", "BSRC-CHAROENSAP 369 LTD CHIANGMAI TH", 100, "2026-05-03", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-5", "baiboon", "first-choice", "ON DEMAND (CMI) BANGKOK TH", 37897, "2026-05-06", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-6", "baiboon", "first-choice", "HTTPS://WWW.MAKRO.PRO/ BANGKOK TH", 8800, "2026-05-07", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-7", "baiboon", "first-choice", "HTTPS://WWW.MAKRO.PRO/ BANGKOK TH", 6839, "2026-05-18", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-8", "baiboon", "first-choice", "HTTPS://WWW.MAKRO.PRO/ BANGKOK TH", 9846, "2026-05-24", bc, dd, {
      note: "Excluded from May 2026 First Choice 2% promo per the card promo terms.",
    }),
    tx("b-fc-9", "baiboon", "first-choice", "HTTPS://WWW.MAKRO.PRO/ BANGKOK TH", 5532, "2026-05-24", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-10", "baiboon", "first-choice", "FUTURE ELECTRONICS SERV 01/03", 2073.67, "2026-05-05", bc, dd, {
      note: "Installment 1/3 — First Choice installment cashback rule TBD; left unset.",
    }),
    tx("b-fc-11", "baiboon", "first-choice", "FUTURE ELECTRONICS SERV 02/03", 2073.67, "2026-06-05", bc, dd),
    tx("b-fc-12", "baiboon", "first-choice", "FUTURE ELECTRONICS SERV 03/03", 2073.67, "2026-07-05", bc, dd),
    tx("b-fc-13", "baiboon", "first-choice", "2C2P*MAJOR CINEPLEX BANGKOK TH", 450, "2026-05-24", bc, dd, { cashbackPercent: 0.02 }),
    tx("b-fc-14", "baiboon", "first-choice", "NW2 Cashback 2% (1 พ.ค. - 31 พ.ค.)", -1136.91, "2026-06-05", bc, dd, {
      note: "Cashback credit posted by the bank.",
    }),
  ];
})();

const TAKUMI_SAMPLE = (() => {
  const bc = "2026-05-25";
  const dd = "2026-06-15";
  return [
    tx("t-uw-1", "takumi", "uob-world", "MEDIUM SUBSCRIPTION SAN FRANCISCO US", 195, "2026-05-10", bc, dd, {
      multiplier: "×0",
      note: "Foreign merchant in THB.",
    }),
    tx("t-up-1", "takumi", "uob-premier", "JIB COMPUTER BANGKOK TH", 24500, "2026-05-12", bc, dd),
    tx("t-up-2", "takumi", "uob-premier", "EATIGO BANGKOK TH", 1850, "2026-05-15", bc, dd),
    tx("t-um-1", "takumi", "uob-makro", "MAKRO-RAMA9 BANGKOK TH", 7240, "2026-05-18", bc, dd),
  ];
})();

export const TRANSACTIONS: Transaction[] = [
  ...NUTA_UOB_CYCLE,
  ...BAIBOON_UOB_ONE,
  ...BAIBOON_UOB_WORLD,
  ...BAIBOON_FIRST_CHOICE,
  ...TAKUMI_SAMPLE,
];

export const transactionsFor = (holder: HolderKey, cardId?: CardId) =>
  TRANSACTIONS.filter((t) => t.holder === holder && (!cardId || t.cardId === cardId));
