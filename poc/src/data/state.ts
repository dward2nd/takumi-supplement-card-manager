import { createContext, useContext, useEffect, useState } from "react";
import { HOLDERS } from "./holders";
import type { HolderKey } from "./types";

const HOLDER_KEY = "takumi.poc.holder";
const THEME_KEY = "takumi.poc.theme";

export type ThemePref = "light" | "dark" | "system";
export type ResolvedTheme = "light" | "dark";

interface AppState {
  holderKey: HolderKey | null;
  setHolder: (key: HolderKey | null) => void;
  themePref: ThemePref;
  setThemePref: (t: ThemePref) => void;
  resolvedTheme: ResolvedTheme;
}

export const AppContext = createContext<AppState>({
  holderKey: null,
  setHolder: () => {},
  themePref: "system",
  setThemePref: () => {},
  resolvedTheme: "dark",
});

export const useApp = () => useContext(AppContext);

const readSystemTheme = (): ResolvedTheme => {
  if (typeof window === "undefined") return "dark";
  return window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark";
};

const applyTheme = (resolved: ResolvedTheme) => {
  const root = document.documentElement;
  if (resolved === "light") root.classList.add("theme-light");
  else root.classList.remove("theme-light");
};

export const useAppStore = (): AppState => {
  const [holderKey, setHolderKey] = useState<HolderKey | null>(() => {
    if (typeof window === "undefined") return null;
    const v = window.localStorage.getItem(HOLDER_KEY);
    return v && v in HOLDERS ? (v as HolderKey) : null;
  });

  const [themePref, setThemePrefState] = useState<ThemePref>(() => {
    if (typeof window === "undefined") return "system";
    const v = window.localStorage.getItem(THEME_KEY);
    return v === "light" || v === "dark" || v === "system" ? v : "system";
  });

  const [systemTheme, setSystemTheme] = useState<ResolvedTheme>(() => readSystemTheme());

  // Holder persistence
  useEffect(() => {
    if (holderKey) {
      window.localStorage.setItem(HOLDER_KEY, holderKey);
    } else {
      window.localStorage.removeItem(HOLDER_KEY);
    }
  }, [holderKey]);

  // Theme preference persistence
  useEffect(() => {
    window.localStorage.setItem(THEME_KEY, themePref);
  }, [themePref]);

  // Follow OS preference when themePref === "system"
  useEffect(() => {
    const media = window.matchMedia("(prefers-color-scheme: light)");
    const onChange = (e: MediaQueryListEvent) => setSystemTheme(e.matches ? "light" : "dark");
    media.addEventListener("change", onChange);
    return () => media.removeEventListener("change", onChange);
  }, []);

  const resolvedTheme: ResolvedTheme = themePref === "system" ? systemTheme : themePref;

  // Apply on every change
  useEffect(() => {
    applyTheme(resolvedTheme);
  }, [resolvedTheme]);

  return {
    holderKey,
    setHolder: setHolderKey,
    themePref,
    setThemePref: setThemePrefState,
    resolvedTheme,
  };
};

export const currentHolder = (key: HolderKey | null) =>
  key ? HOLDERS[key] : null;
