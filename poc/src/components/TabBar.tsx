import clsx from "clsx";
import { NavLink } from "react-router-dom";
import { Home, CreditCard, Receipt, Plus } from "lucide-react";
import { motion } from "framer-motion";
import { useApp } from "../data/state";
import { HOLDERS } from "../data/holders";

const STATIC_TABS = [
  { to: "/home", label: "home", icon: Home },
  { to: "/cards", label: "cards", icon: CreditCard },
  { to: "/bills", label: "bills", icon: Receipt },
] as const;

export const TabBar = ({ canBills }: { canBills: boolean }) => {
  const { holderKey } = useApp();
  const me = holderKey ? HOLDERS[holderKey] : null;

  return (
    <nav
      className="bottom-safe pointer-events-auto fixed inset-x-0 bottom-0 z-30 mx-auto max-w-md px-4"
      aria-label="Main"
    >
      <div className="relative">
        <div className="relative grid grid-cols-4 items-end gap-1 rounded-2xl border border-paper-line/80 bg-paper/85 px-2 py-2 backdrop-blur-md">
          {STATIC_TABS.map((tab) => {
            const Icon = tab.icon;
            const disabled = tab.label === "bills" && !canBills;
            return (
              <NavLink
                key={tab.to}
                to={disabled ? "/home" : tab.to}
                className={({ isActive }) =>
                  clsx(
                    "tap relative flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 text-[12px] uppercase tracking-[0.18em]",
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

          {/*
            The "you" tab — replaces the generic Settings icon with the
            active holder's avatar + name. It's both the entry point to the
            Settings screen and a "logged in as" indicator, consolidating the
            old top-right presence badge into the bottom nav.
          */}
          <NavLink
            to="/settings"
            className={({ isActive }) =>
              clsx(
                "tap relative flex flex-col items-center justify-center gap-1 rounded-xl px-2 py-2 text-[12px] uppercase tracking-[0.18em]",
                "transition-colors duration-300",
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
                {me ? (
                  <span
                    className="relative flex h-[18px] w-[18px] items-center justify-center rounded-full text-[10px] font-medium text-on-accent"
                    style={{ background: me.accent }}
                  >
                    {me.initial}
                  </span>
                ) : (
                  <span aria-hidden className="relative h-[18px] w-[18px] rounded-full bg-ink-ghost/30" />
                )}
                <span className="relative">{me?.englishName.toLowerCase() ?? "you"}</span>
              </>
            )}
          </NavLink>
        </div>
      </div>
    </nav>
  );
};

/**
 * FAB pinned to the right edge — viewport-right on md+ (so it sits near the
 * border instead of floating mid-canvas alongside the multi-column desktop
 * layouts), and right edge of the phone container on mobile.
 * `bottom` clears the tab bar + safe-area inset.
 */
export const FAB = ({ onClick, label = "add" }: { onClick: () => void; label?: string }) => (
  <div
    aria-hidden
    className="pointer-events-none fixed inset-x-0 z-40 mx-auto flex max-w-md justify-end px-5 md:max-w-none md:px-6 lg:px-8"
    style={{
      bottom: "calc(env(safe-area-inset-bottom, 0px) + 5.25rem)",
    }}
  >
    <button
      onClick={onClick}
      className={clsx(
        "tap pointer-events-auto",
        "flex h-14 w-14 items-center justify-center rounded-full",
        "bg-gradient-to-br from-amber-200 to-amber-400 text-on-accent",
        "shadow-glow-amber transition-transform duration-300 active:scale-95",
      )}
      aria-label={label}
    >
      <Plus size={22} strokeWidth={2.2} />
    </button>
  </div>
);
