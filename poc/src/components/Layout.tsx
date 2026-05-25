import { Outlet, useLocation, useNavigate } from "react-router-dom";
import { AnimatePresence, motion } from "framer-motion";
import { useApp } from "../data/state";
import { TabBar, FAB } from "./TabBar";

export const Layout = () => {
  const { holderKey } = useApp();
  const loc = useLocation();
  const nav = useNavigate();

  const isLogin = !holderKey;
  const isAdd = loc.pathname === "/add";
  const showChrome = !isLogin && !isAdd;
  const canBills = holderKey !== null && holderKey !== "takumi" ? true : holderKey === "takumi";

  return (
    // Mobile-first: the container has no max-width at the outer level. Each
    // screen clamps its own content (max-w-md by default, expanding to
    // md:max-w-3xl / lg:max-w-6xl where the screen benefits from extra width).
    // The editorial line-length feel is preserved on phones; desktops spread
    // into purposeful multi-column layouts at lg+. The "logged in as <holder>"
    // affordance lives in the bottom TabBar's right-most tab, not a separate
    // top-right badge.
    <div className="relative flex min-h-dvh flex-col overflow-x-hidden">
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
        </>
      )}
    </div>
  );
};
