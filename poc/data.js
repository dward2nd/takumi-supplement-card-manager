// Mock data shaped after docs/future-app/data-model-target.md.
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
  // The Notion-as-built model lacks this entity — it's introduced in the phase-2 target.
  primaryAccounts: [
    { id: "pa-uob",      issuerId: "iss-uob",      holderPersonId: "p-takumi", creditLimit: 300000 },
    { id: "pa-ktc",      issuerId: "iss-ktc",      holderPersonId: "p-takumi", creditLimit: 200000 },
    { id: "pa-krungsri", issuerId: "iss-krungsri", holderPersonId: "p-takumi", creditLimit: 250000 },
  ],

  // Cards: primary + supplement plastic. `holderPersonId` is who carries this card.
  cards: [
    { id: "c-uob-takumi",       primaryAccountId: "pa-uob",      holderPersonId: "p-takumi",  productId: "cp-uob-premier",   premiumTier: "Signature", bahtPerPoint: 25, pointsPerCycle: false, allocatedLimit: 200000 },
    { id: "c-uob-baiboon",      primaryAccountId: "pa-uob",      holderPersonId: "p-baiboon", productId: "cp-uob-premier",   premiumTier: "Signature", bahtPerPoint: 25, pointsPerCycle: false, allocatedLimit: 100000 },

    { id: "c-ktc-takumi",       primaryAccountId: "pa-ktc",      holderPersonId: "p-takumi",  productId: "cp-ktc-forest",    premiumTier: "Platinum",  bahtPerPoint: 25, pointsPerCycle: true,  allocatedLimit: 120000 },
    { id: "c-ktc-nuta",         primaryAccountId: "pa-ktc",      holderPersonId: "p-nuta",    productId: "cp-ktc-forest",    premiumTier: "Platinum",  bahtPerPoint: 25, pointsPerCycle: true,  allocatedLimit: 80000  },

    { id: "c-krungsri-takumi",  primaryAccountId: "pa-krungsri", holderPersonId: "p-takumi",  productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 100000 },
    { id: "c-krungsri-baiboon", primaryAccountId: "pa-krungsri", holderPersonId: "p-baiboon", productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 75000  },
    { id: "c-krungsri-nuta",    primaryAccountId: "pa-krungsri", holderPersonId: "p-nuta",    productId: "cp-krungsri-plat", premiumTier: "Platinum",  bahtPerPoint: 20, pointsPerCycle: false, allocatedLimit: 75000  },
  ],

  // Categories — only Takumi has `หมวดหมู่` in the Notion-as-built model.
  categories: [
    { id: "cat-food",     name: "อาหาร"  },
    { id: "cat-transit",  name: "เดินทาง" },
    { id: "cat-online",   name: "ออนไลน์" },
    { id: "cat-utility",  name: "ค่าใช้จ่ายประจำ" },
  ],

  // Transactions. `rewardRules` replaces the per-column multiplier checkboxes
  // and Nuta's `% cb`. `status` is the unified enum from data-model-target.md.
  transactions: [
    // Takumi
    { id: "t-001", cardId: "c-uob-takumi",       categoryId: "cat-utility", amountBaht: 12500, swipedAt: "2026-04-12", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "paid",      rewardRules: [{ type: "multiplier", value: 2 }], note: "ค่าไฟ" },
    { id: "t-002", cardId: "c-ktc-takumi",       categoryId: "cat-food",    amountBaht:  2380, swipedAt: "2026-05-02", billCycleDate: "2026-05-15", dueDate: "2026-05-31", status: "processed", rewardRules: [{ type: "multiplier", value: 3 }], note: "ร้านอาหาร" },
    { id: "t-003", cardId: "c-krungsri-takumi",  categoryId: "cat-online",  amountBaht:  4990, swipedAt: "2026-05-08", billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "pending",   rewardRules: [{ type: "multiplier", value: 5 }], note: "ช้อปออนไลน์" },

    // Baiboon
    { id: "t-101", cardId: "c-uob-baiboon",      amountBaht:  890, swipedAt: "2026-04-18", billCycleDate: "2026-04-25", dueDate: "2026-05-10", status: "paid",      rewardRules: [{ type: "multiplier", value: 1 }], note: "Starbucks" },
    { id: "t-102", cardId: "c-uob-baiboon",      amountBaht: 3450, swipedAt: "2026-05-05", billCycleDate: "2026-05-25", dueDate: "2026-06-10", status: "processed", rewardRules: [{ type: "multiplier", value: 2 }], note: "ปั๊มน้ำมัน" },
    { id: "t-103", cardId: "c-krungsri-baiboon", amountBaht: 1290, swipedAt: "2026-05-12", billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "pending",   rewardRules: [{ type: "multiplier", value: 1 }], note: "ซูเปอร์มาร์เก็ต" },

    // Nuta — note the `cashback` reward rule, which is Nuta-only in the Notion-as-built model.
    { id: "t-201", cardId: "c-ktc-nuta",         amountBaht:  650, swipedAt: "2026-04-22", billCycleDate: "2026-04-30", dueDate: "2026-05-15", status: "paid",      rewardRules: [{ type: "multiplier", value: 1 }, { type: "cashback", percent: 1.0 }], note: "ร้านสะดวกซื้อ" },
    { id: "t-202", cardId: "c-krungsri-nuta",    amountBaht: 2980, swipedAt: "2026-05-10", billCycleDate: "2026-05-20", dueDate: "2026-06-05", status: "processed", rewardRules: [{ type: "multiplier", value: 2 }, { type: "cashback", percent: 0.5 }], note: "ห้างสรรพสินค้า" },
    { id: "t-203", cardId: "c-ktc-nuta",         amountBaht:  450, swipedAt: "2026-05-14", billCycleDate: "2026-05-30", dueDate: "2026-06-15", status: "pending",   rewardRules: [{ type: "multiplier", value: 1 }, { type: "cashback", percent: 1.0 }], note: "ร้านกาแฟ" },
  ],

  // Bills exist only for supplement holders (Takumi has no Bills DB in Notion).
  // In the phase-2 model `cardId` is a real FK rather than a SELECT (resolves divergence #1).
  bills: [
    { id: "b-101", cardId: "c-uob-baiboon",      cycleDate: "2026-04-25", amountBaht:  890, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-08.jpg" },
    { id: "b-102", cardId: "c-krungsri-baiboon", cycleDate: "2026-04-20", amountBaht: 2150, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-03.jpg" },
    { id: "b-103", cardId: "c-uob-baiboon",      cycleDate: "2026-05-25", amountBaht: 3450, paid: false, statementFile: null, paymentEvidence: null },

    { id: "b-201", cardId: "c-ktc-nuta",         cycleDate: "2026-04-30", amountBaht:  650, paid: true,  statementFile: null, paymentEvidence: "slip-2026-05-12.jpg" },
    { id: "b-202", cardId: "c-krungsri-nuta",    cycleDate: "2026-05-20", amountBaht: 2980, paid: false, statementFile: null, paymentEvidence: null },
  ],
};
