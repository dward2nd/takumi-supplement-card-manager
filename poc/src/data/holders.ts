import type { Holder, HolderKey } from "./types";

export const HOLDERS: Record<HolderKey, Holder> = {
  takumi: {
    key: "takumi",
    englishName: "Takumi",
    thaiName: "เว็บ",
    isAdmin: true,
    initial: "ว",
    accent: "#f7c463", // amber
  },
  baiboon: {
    key: "baiboon",
    englishName: "Baiboon",
    thaiName: "ใบบุญ",
    isAdmin: false,
    initial: "บ",
    accent: "#7ec8b5", // teal
  },
  nuta: {
    key: "nuta",
    englishName: "Nuta",
    thaiName: "นุตา",
    isAdmin: false,
    initial: "น",
    accent: "#f08977", // coral
  },
};

export const HOLDER_LIST = Object.values(HOLDERS);
