// Mock data shaped after docs/future-app/product-shape.md (canonical) and
// docs/future-app/data-model-target.md (entity shape).
//
// All values are illustrative only — none of this corresponds to real cards.
// Thai labels are preserved verbatim (e.g. `เว็บ`, `ใบบุญ`, `นุตา`) as the vault requires.

window.POC_DATA = {
  issuers: [
    { id: "iss-uob",      name: "UOB" },
    { id: "iss-ktc",      name: "KTC" },
    { id: "iss-krungsri", name: "Krungsri" },
  ],

  networks: [
    { id: "net-jcb",  name: "JCB" },
    { id: "net-mc",   name: "Mastercard" },
    { id: "net-visa", name: "VISA" },
  ],

  cardProducts: [
    { id: "cp-uob-premier",   name: "UOB Premier",            issuerId: "iss-uob",      networkId: "net-jcb" },
    { id: "cp-ktc-forest",    name: "KTC Forest",             issuerId: "iss-ktc",      networkId: "net-mc" },
    { id: "cp-krungsri-plat", name: "Krungsri Visa Platinum", issuerId: "iss-krungsri", networkId: "net-visa" },
  ],

  // The three cardholders. `displayName` = vault English; `notionName` = the Thai handle Notion uses.
  people: [
    { id: "p-takumi",  displayName: "Takumi",  notionName: "เว็บ",   role: "primary" },
    { id: "p-baiboon", displayName: "Baiboon", notionName: "ใบบุญ",  role: "supplement" },
    { id: "p-nuta",    displayName: "Nuta",    notionName: "นุตา",   role: "supplement" },
  ],

  // PrimaryAccount: the credit line. Always held by Takumi in this household.
  // Phase 2: exposed as its own UI surface (see product-shape.md).
  primaryAccounts: [
    { id: "pa-uob",      issuerId: "iss-uob",      holderPersonId: "p-takumi", accountNumberHash: "uob-hash-mock-0001",      creditLimit: 300000 },
    { id: "pa-ktc",      issuerId: "iss-ktc",      holderPersonId: "p-takumi", accountNumberHash: "ktc-hash-mock-0002",      creditLimit: 200000 },
    { id: "pa-krungsri", issuerId: "iss-krungsri", holderPersonId: "p-takumi", accountNumberHash: "krungsri-hash-mock-0003", creditLimit: 250000 },
  ],

  // Cards: primary + supplement plastic. `holderPersonId` is who carries this card.
  // `last4` and `nickname` are the only card identifiers stored in phase 2 (never the PAN).
  cards: [
    { id: "c-uob-takumi",       primaryAccountId: "pa-uob",      holderPersonId: "p-takumi",  productId: "cp-uob-premier",   premiumTier: "Signature", bahtPerPoint: 25, pointsPerCycle: false, allocatedLimit: 200000, last4: "1234", nickname: "Takumi UOB primary" },
    { id: "c-uob-baiboon",      primaryAccountId: "pa-uob",      holderPersonId: "p-baiboon", productId: "cp-uob-premier",   premiumTier: "Signature", bahtPerPoint: 25, pointsPerCycle: false, allocatedLimit: 100000, last4: "5678", nickname: "Baiboon UOB supp" },

    { id: "c-ktc-takumi",       primaryAccountId: "pa-ktc",      holderPersonId: "p-takumi",  productId: "cp-ktc-forest",    premiumTier: "Platinum",  bahtPerPoint: 25, pointsPerCycle: true,  allocatedLimit: 120000, last4: "2468", nickname: "Takumi KTC" },
    { id: "c-ktc-nuta",         primaryAccountId: "pa-ktc",      holderPersonId: "p-nuta",    productId: "cp-ktc-forest",    premiumTier: "Platinum",  bahtPerPoint: 25, pointsPerCycle: true,  allocatedLimit: 80000,  last4: "1357", nickname: "Nuta KTC" },

    { id: "c-krungsri-takumi",  primaryAccountId: "pa-krungsri", holderPersonId: "p-takumi",  productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 100000, last4: "9090", nickname: "Takumi Krungsri" },
    { id: "c-krungsri-baiboon", primaryAccountId: "pa-krungsri", holderPersonId: "p-baiboon", productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 75000,  last4: "9191", nickname: "Baiboon Krungsri" },
    { id: "c-krungsri-nuta",    primaryAccountId: "pa-krungsri", holderPersonId: "p-nuta",    productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 75000,  last4: "9292", nickname: "Nuta Krungsri" },
  ],

  // Categories — phase 2: universal across all three holders (Notion had this Takumi-only).
  categories: [
    { id: "cat-food",     name: "อาหาร"  },
    { id: "cat-transit",  name: "เดินทาง" },
    { id: "cat-online",   name: "ออนไลน์" },
    { id: "cat-utility",  name: "ค่าใช้จ่ายประจำ" },
    { id: "cat-travel",   name: "ท่องเที่ยว" },
    { id: "cat-other",    name: "Other / Uncategorized" },
  ],

  // Alias rules — pattern → canonical merchant + auto-category.
  // Phase 2 entry flow: when a typed merchant string matches a rule, the alias
  // auto-fills the canonical name and category. The raw verbatim string is still
  // stored on the Transaction.
  aliases: [
    { id: "al-001", pattern: { type: "contains", text: "Agoda" }, canonicalMerchant: "Agoda", categoryId: "cat-travel" },
    { id: "al-002", pattern: { type: "contains", text: "Starbucks" }, canonicalMerchant: "Starbucks", categoryId: "cat-food" },
  ],

  // Per-cycle quotas. Some promotions cap per-card; others cap household-wide at PrimaryAccount level.
  // `usedThisCycle` is illustrative; the new app computes it from accumulated transactions.
  cardQuotas: [
    { id: "cq-001", cardId: "c-uob-takumi", rewardType: "multiplier", value: 5, capBaht: 10000, usedThisCycleBaht: 7200, label: "×5 promo (per card)" },
  ],

  accountQuotas: [
    { id: "aq-001", primaryAccountId: "pa-uob", rewardType: "cashback", percent: 5, capBaht: 8000, usedThisCycleBaht: 3200, label: "5% cashback (shared across UOB account)" },
  ],

  // Transactions. `rewardRules` is a JSON array per phase-2 design.
  // Negative `amountBaht` rows are refund adjustment rows.
  // `refundOfTxId` (if set) points to the original transaction that was refunded.
  // Cross-cycle refunds carry the *next* billCycleDate to act as advance payment on the next bill.
  transactions: [
    // Takumi
    { id: "t-001", cardId: "c-uob-takumi",       categoryId: "cat-utility", amountBaht: 12500, swipedAt: "2026-04-12", processedDate: "2026-04-13", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "paid",      rewardRules: [{ type: "multiplier", value: 2 }], note: "ค่าไฟ" },
    { id: "t-002", cardId: "c-ktc-takumi",       categoryId: "cat-food",    amountBaht:  2380, swipedAt: "2026-05-02", processedDate: "2026-05-03", billCycleDate: "2026-05-15", dueDate: "2026-05-31", status: "processed", rewardRules: [{ type: "multiplier", value: 3 }], note: "ร้านอาหาร" },
    { id: "t-003", cardId: "c-krungsri-takumi",  categoryId: "cat-online",  amountBaht:  4990, swipedAt: "2026-05-08", processedDate: null,         billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "pending",   rewardRules: [{ type: "multiplier", value: 5 }], note: "ช้อปออนไลน์" },
    // Takumi ×5 promo example — counts against the per-card quota cq-001
    { id: "t-004", cardId: "c-uob-takumi",       categoryId: "cat-online",  amountBaht:  7200, swipedAt: "2026-05-09", processedDate: "2026-05-10", billCycleDate: "2026-05-25", dueDate: "2026-06-10", status: "processed", rewardRules: [{ type: "multiplier", value: 5 }], note: "Promo eligible" },

    // Baiboon
    { id: "t-101", cardId: "c-uob-baiboon",      categoryId: "cat-food",    amountBaht:  890, swipedAt: "2026-04-18", processedDate: "2026-04-19", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "paid",      rewardRules: [{ type: "multiplier", value: 1 }], note: "Starbucks", aliasMatchedId: "al-002" },
    { id: "t-102", cardId: "c-uob-baiboon",      categoryId: "cat-transit", amountBaht: 3450, swipedAt: "2026-05-05", processedDate: "2026-05-06", billCycleDate: "2026-05-25", dueDate: "2026-06-10", status: "processed", rewardRules: [{ type: "multiplier", value: 2 }], note: "ปั๊มน้ำมัน" },
    { id: "t-103", cardId: "c-krungsri-baiboon", categoryId: "cat-food",    amountBaht: 1290, swipedAt: "2026-05-12", processedDate: null,         billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "pending",   rewardRules: [{ type: "multiplier", value: 1 }], note: "ซูเปอร์มาร์เก็ต" },
    // Same-cycle refund — both rows in cycle 2026-04-25. Status flip + negative adjustment.
    { id: "t-104", cardId: "c-uob-baiboon",      categoryId: "cat-food",    amountBaht:  450, swipedAt: "2026-04-22", processedDate: "2026-04-23", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "refunded",  rewardRules: [{ type: "multiplier", value: 1 }], note: "Returned item" },
    { id: "t-104a", cardId: "c-uob-baiboon",     categoryId: "cat-food",    amountBaht: -450, swipedAt: "2026-04-24", processedDate: "2026-04-25", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "processed", rewardRules: [],                                  note: "Refund of t-104 (same cycle)", refundOfTxId: "t-104" },
    // Cross-cycle refund — original in 04-25 cycle, adjustment row in 05-25 cycle as advance payment on next bill.
    { id: "t-105", cardId: "c-uob-baiboon",      categoryId: "cat-other",   amountBaht:  800, swipedAt: "2026-04-20", processedDate: "2026-04-21", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "refunded",  rewardRules: [{ type: "multiplier", value: 1 }], note: "Hotel cancellation" },
    { id: "t-105a", cardId: "c-uob-baiboon",     categoryId: "cat-other",   amountBaht: -800, swipedAt: "2026-05-02", processedDate: "2026-05-03", billCycleDate: "2026-05-25", dueDate: "2026-06-10", status: "processed", rewardRules: [],                                  note: "Cross-cycle refund of t-105 — credited to next bill", refundOfTxId: "t-105" },

    // Nuta
    { id: "t-201", cardId: "c-ktc-nuta",         categoryId: "cat-other",   amountBaht:  650, swipedAt: "2026-04-22", processedDate: "2026-04-23", billCycleDate: "2026-04-30", dueDate: "2026-05-15", status: "paid",      rewardRules: [{ type: "multiplier", value: 1 }, { type: "cashback", percent: 1.0 }], note: "ร้านสะดวกซื้อ" },
    { id: "t-202", cardId: "c-krungsri-nuta",    categoryId: "cat-other",   amountBaht: 2980, swipedAt: "2026-05-10", processedDate: "2026-05-11", billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "processed", rewardRules: [{ type: "multiplier", value: 2 }, { type: "cashback", percent: 0.5 }], note: "ห้างสรรพสินค้า" },
    { id: "t-203", cardId: "c-ktc-nuta",         categoryId: "cat-food",    amountBaht:  450, swipedAt: "2026-05-14", processedDate: null,         billCycleDate: "2026-05-30", dueDate: "2026-06-15", status: "pending",   rewardRules: [{ type: "multiplier", value: 1 }, { type: "cashback", percent: 1.0 }], note: "ร้านกาแฟ" },
    // Alias-matched: typed "Agoda - Bangkok Hotel" → matched alias al-001 → canonical "Agoda" + category Travel.
    // The verbatim string is preserved in `note` for statement reconciliation.
    { id: "t-204", cardId: "c-krungsri-nuta",    categoryId: "cat-travel",  amountBaht: 4500, swipedAt: "2026-05-13", processedDate: "2026-05-14", billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "processed", rewardRules: [{ type: "multiplier", value: 1 }, { type: "cashback", percent: 1.0 }], note: "Agoda - Bangkok Hotel", aliasMatchedId: "al-001" },
  ],

  // Bills — phase 2 makes them symmetric (every holder gets bills; Takumi too).
  // `cardId` is a real FK to `cards.id` (resolves the SELECT-vs-relation divergence).
  bills: [
    // Takumi (NEW in phase 2 — was absent in Notion).
    { id: "b-001", cardId: "c-uob-takumi",       cycleDate: "2026-04-25", amountBaht: 12500, paid: true,  statementFile: "uob-takumi-2026-04.pdf", paymentEvidence: null },
    { id: "b-002", cardId: "c-ktc-takumi",       cycleDate: "2026-05-15", amountBaht:  2380, paid: false, statementFile: null, paymentEvidence: null },

    // Baiboon
    { id: "b-101", cardId: "c-uob-baiboon",      cycleDate: "2026-04-25", amountBaht:  890, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-08.jpg" },
    { id: "b-102", cardId: "c-krungsri-baiboon", cycleDate: "2026-04-20", amountBaht: 2150, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-03.jpg" },
    { id: "b-103", cardId: "c-uob-baiboon",      cycleDate: "2026-05-25", amountBaht: 3450, paid: false, statementFile: null, paymentEvidence: null },

    // Nuta
    { id: "b-201", cardId: "c-ktc-nuta",         cycleDate: "2026-04-30", amountBaht:  650, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-12.jpg" },
    { id: "b-202", cardId: "c-krungsri-nuta",    cycleDate: "2026-05-20", amountBaht: 7480, paid: false, statementFile: null, paymentEvidence: null },
  ],
};
