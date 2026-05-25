import { useNavigate } from "react-router-dom";
import { motion } from "framer-motion";
import { LogOut, RefreshCw, Info, Sparkles } from "lucide-react";
import { useApp } from "../data/state";
import { HOLDERS, HOLDER_LIST } from "../data/holders";
import { PageHeader } from "../components/PageHeader";
import { Pill } from "../components/Pill";
import { SectionLabel } from "../components/SectionLabel";
import clsx from "clsx";

export const SettingsScreen = () => {
  const { holderKey, setHolder } = useApp();
  const nav = useNavigate();
  if (!holderKey) return null;
  const me = HOLDERS[holderKey];

  return (
    <div>
      <PageHeader title="You · ตัวคุณ" eyebrow="profile + session" />

      <section className="mx-5 mb-8 overflow-hidden rounded-3xl border border-paper-line bg-paper-raised/60 p-6">
        <div className="flex items-center gap-4">
          <span
            className="flex h-14 w-14 items-center justify-center rounded-full font-display text-xl text-paper"
            style={{ background: me.accent }}
          >
            {me.initial}
          </span>
          <div>
            <div className="font-display text-2xl font-light tracking-tight text-ink">
              {me.englishName}
            </div>
            <div className="text-[11px] uppercase tracking-[0.18em] text-ink-faint">
              {me.thaiName}
              {me.isAdmin && <span className="ml-2 text-amber-glow">· admin</span>}
            </div>
          </div>
        </div>

        <div className="mt-5 rule" />

        <div className="mt-5 grid grid-cols-2 gap-3 text-[11px]">
          <div>
            <div className="text-[9px] uppercase tracking-[0.22em] text-ink-faint">role</div>
            <div className="mt-1 text-ink">{me.isAdmin ? "Primary · admin" : "Supplement holder"}</div>
          </div>
          <div>
            <div className="text-[9px] uppercase tracking-[0.22em] text-ink-faint">visibility</div>
            <div className="mt-1 text-ink">
              {me.isAdmin ? "All 3 holders" : "Own data only"}
            </div>
          </div>
        </div>
      </section>

      <section className="px-5 pb-8">
        <SectionLabel number="01">Switch holder · POC convenience</SectionLabel>
        <div className="mt-3 grid grid-cols-3 gap-2">
          {HOLDER_LIST.map((h) => (
            <button
              key={h.key}
              onClick={() => setHolder(h.key)}
              className={clsx(
                "tap flex flex-col items-center gap-2 rounded-2xl border px-3 py-4 transition-colors",
                holderKey === h.key
                  ? "border-amber-200/40 bg-amber-300/[0.06]"
                  : "border-paper-line bg-paper-raised/40 hover:bg-paper-raised",
              )}
            >
              <span
                className="flex h-9 w-9 items-center justify-center rounded-full text-sm font-medium text-paper"
                style={{ background: h.accent }}
              >
                {h.initial}
              </span>
              <span className="text-[11px] uppercase tracking-[0.16em] text-ink-dim">
                {h.englishName}
              </span>
              {holderKey === h.key && <Pill tone="amber" uppercase>active</Pill>}
            </button>
          ))}
        </div>
      </section>

      <section className="px-5 pb-8">
        <SectionLabel number="02">About</SectionLabel>
        <div className="mt-3 space-y-2">
          <Row icon={<Sparkles size={16} />} title="POC · phase II">
            Mock data only — refreshing the app resets nothing.
          </Row>
          <Row icon={<Info size={16} />} title="Source of truth (live)">
            Notion + scripts/repositories/. This UI mirrors the data model.
          </Row>
          <Row icon={<RefreshCw size={16} />} title="Sync">
            Single-page client, no network. The real app will sync via a Rust backend on a VPS.
          </Row>
        </div>
      </section>

      <section className="px-5 pb-16">
        <motion.button
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.2 }}
          onClick={() => {
            setHolder(null);
            nav("/");
          }}
          className="tap flex w-full items-center justify-between gap-3 rounded-2xl border border-paper-line bg-paper-raised/40 px-4 py-4 text-left transition-colors hover:bg-paper-raised"
        >
          <div className="flex items-center gap-3">
            <span className="flex h-9 w-9 items-center justify-center rounded-full border border-paper-line text-ink-dim">
              <LogOut size={16} strokeWidth={1.6} />
            </span>
            <div>
              <div className="font-display text-sm tracking-tight text-ink">Sign out</div>
              <div className="text-[10px] uppercase tracking-[0.18em] text-ink-faint">
                back to the cover page
              </div>
            </div>
          </div>
          <span className="text-[10px] uppercase tracking-[0.22em] text-ink-faint">leave →</span>
        </motion.button>
      </section>
    </div>
  );
};

const Row = ({
  icon,
  title,
  children,
}: {
  icon: React.ReactNode;
  title: string;
  children: React.ReactNode;
}) => (
  <div className="flex items-start gap-3 rounded-2xl border border-paper-line/60 bg-paper-raised/30 px-4 py-3">
    <span className="mt-1 text-amber-glow/80">{icon}</span>
    <div>
      <div className="font-display text-sm tracking-tight text-ink">{title}</div>
      <div className="mt-0.5 text-[11px] leading-relaxed text-ink-dim">{children}</div>
    </div>
  </div>
);
