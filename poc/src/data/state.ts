import { createContext, useContext, useEffect, useState } from "react";
import { HOLDERS } from "./holders";
import type { HolderKey } from "./types";

const STORAGE_KEY = "takumi.poc.holder";

interface AppState {
  holderKey: HolderKey | null;
  setHolder: (key: HolderKey | null) => void;
}

export const AppContext = createContext<AppState>({
  holderKey: null,
  setHolder: () => {},
});

export const useApp = () => useContext(AppContext);

export const useAppStore = () => {
  const [holderKey, setHolderKey] = useState<HolderKey | null>(() => {
    if (typeof window === "undefined") return null;
    const v = window.localStorage.getItem(STORAGE_KEY);
    return v && v in HOLDERS ? (v as HolderKey) : null;
  });

  useEffect(() => {
    if (holderKey) {
      window.localStorage.setItem(STORAGE_KEY, holderKey);
    } else {
      window.localStorage.removeItem(STORAGE_KEY);
    }
  }, [holderKey]);

  return {
    holderKey,
    setHolder: setHolderKey,
  };
};

export const currentHolder = (key: HolderKey | null) =>
  key ? HOLDERS[key] : null;
