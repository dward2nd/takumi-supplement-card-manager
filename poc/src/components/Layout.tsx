import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { useApp } from "../data/state";
import { TabBar, FAB } from "./TabBar";
import { HOLDERS } from "../data/holders";

export const Layout = () => {
  const { holderKey } = useApp();
  const loc = useLocation();
  const nav = useNavigate();

  const isLogin = !holderKey;
  const isAdd = loc.pathname === "/add";
  const showChrome = !isLogin && !isAdd;
  const canBills = holderKey !== null && holderKey !== "takumi" ? true : holderKey === "takumi";

  return (
    <div className="relative mx-auto flex min-h-dvh max-w-md flex-col overflow-x-hidden">
      <span className="grain-overlay" aria-hidden />
      <AnimatePresence mode="wait">
        <motion.main
          key={loc.pathname}
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          exit={{ opacity: 0, y: -6 }}
          transition={{ duration: 0.35, ease: [0.2, 0.7, 0.1, 1] }}
          className="relative z-10 flex-1 pb-32"
        >
          <Outlet />
        </motion.main>
      </AnimatePresence>

      {showChrome && (
        <>
          <FAB onClick={() => nav("/add")} />
          <TabBar canBills={canBills} />
          {holderKey && <PresenceBadge />}
        </>
      )}
    </div>
  );
};

const PresenceBadge = () => {
  const { holderKey } = useApp();
  const nav = useNavigate();
  if (!holderKey) return null;
  const h = HOLDERS[holderKey];
  return (
    <button
      onClick={() => nav("/settings")}
      className="tap top-safe fixed right-4 z-30 flex h-9 items-center gap-2 rounded-full border border-paper-line/80 bg-paper/70 pl-1 pr-3 backdrop-blur-md"
      aria-label={`logged in as ${h.englishName}`}
    >
      <span
        className="flex h-7 w-7 items-center justify-center rounded-full text-sm font-medium text-paper"
        style={{ background: h.accent }}
      >
        {h.initial}
      </span>
      <span className="text-[10px] uppercase tracking-[0.18em] text-ink-dim">
        {h.englishName}
      </span>
    </button>
  );
};
