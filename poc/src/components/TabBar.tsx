import clsx from "clsx";
import { NavLink } from "react-router-dom";
import { Home, CreditCard, Receipt, Settings, Plus } from "lucide-react";
import { motion } from "framer-motion";

const TABS = [
  { to: "/home", label: "home", icon: Home },
  { to: "/cards", label: "cards", icon: CreditCard },
  { to: "/bills", label: "bills", icon: Receipt },
  { to: "/settings", label: "you", icon: Settings },
] as const;

export const TabBar = ({ canBills }: { canBills: boolean }) => {
  return (
    <nav
      className="bottom-safe pointer-events-auto fixed inset-x-0 bottom-0 z-30 mx-auto max-w-md px-4"
      aria-label="Main"
    >
      <div className="relative">
        {/* Soft fade from background up into the bar so floating content
            doesn't look like it's cut off mid-air */}
        <span
          aria-hidden
          className="pointer-events-none absolute -top-10 left-0 right-0 h-10 bg-gradient-to-t from-paper to-transparent"
        />
        <div className="relative grid grid-cols-4 items-end gap-1 rounded-2xl border border-paper-line/80 bg-paper/85 px-2 py-2 backdrop-blur-md">
          {TABS.map((tab) => {
            const Icon = tab.icon;
            const disabled = tab.label === "bills" && !canBills;
            return (
              <NavLink
                key={tab.to}
                to={disabled ? "/home" : tab.to}
                className={({ isActive }) =>
                  clsx(
                    "tap relative flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 text-[10px] uppercase tracking-[0.18em]",
                    "transition-colors duration-300",
                    disabled && "pointer-events-none opacity-30",
                    isActive ? "text-ink" : "text-ink-faint",
                  )
                }
              >
                {({ isActive }) => (
                  <>
                    {isActive && (
                      <motion.span
                        layoutId="tab-pill"
                        className="absolute inset-0 -z-0 rounded-xl bg-paper-raised"
                        transition={{ type: "spring", stiffness: 380, damping: 30 }}
                      />
                    )}
                    <Icon
                      size={18}
                      strokeWidth={isActive ? 1.8 : 1.4}
                      className="relative"
                    />
                    <span className="relative">{tab.label}</span>
                  </>
                )}
              </NavLink>
            );
          })}
        </div>
      </div>
    </nav>
  );
};

export const FAB = ({ onClick, label = "add" }: { onClick: () => void; label?: string }) => (
  <button
    onClick={onClick}
    className={clsx(
      "tap fixed bottom-[calc(env(safe-area-inset-bottom,0px)+5.25rem)] right-5 z-40",
      "flex h-14 w-14 items-center justify-center rounded-full",
      "bg-gradient-to-br from-amber-200 to-amber-400 text-paper",
      "shadow-glow-amber transition-transform duration-300 active:scale-95",
    )}
    aria-label={label}
  >
    <Plus size={22} strokeWidth={2.2} />
  </button>
);
