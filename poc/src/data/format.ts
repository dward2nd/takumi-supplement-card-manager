// Number / date / merchant formatting helpers.

const baht = new Intl.NumberFormat("th-TH", {
  minimumFractionDigits: 2,
  maximumFractionDigits: 2,
});

export const formatBaht = (n: number) => baht.format(Math.abs(n));

export const formatBahtSigned = (n: number) =>
  (n < 0 ? "−" : "") + baht.format(Math.abs(n));

export const formatBahtInt = (n: number) =>
  Math.abs(n).toLocaleString("th-TH", { maximumFractionDigits: 0 });

const dateShort = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "short",
});
const dateLong = new Intl.DateTimeFormat("en-GB", {
  day: "numeric",
  month: "long",
  year: "numeric",
});
const dateMonth = new Intl.DateTimeFormat("en-GB", {
  month: "short",
  year: "numeric",
});

export const fmtShort = (iso: string) => dateShort.format(new Date(iso));
export const fmtLong = (iso: string) => dateLong.format(new Date(iso));
export const fmtMonth = (iso: string) => dateMonth.format(new Date(iso));

/** Take the country suffix off a merchant string for the secondary line. */
export const splitMerchant = (
  name: string,
): { headline: string; tail: string | null } => {
  const trimmed = name.trim();
  // Country-suffix tokens we'd want to peel off into the tail line.
  const m = trimmed.match(/^(.+?)\s+([A-Z]{2,3})$/);
  if (m && m[1].length > 6) {
    return { headline: m[1], tail: m[2] };
  }
  return { headline: trimmed, tail: null };
};

/** Pretty rate: 0.05 → "5%". Used for tier badges. */
export const fmtRate = (rate: number) => {
  const pct = rate * 100;
  return Number.isInteger(pct) ? `${pct}%` : `${pct.toFixed(1)}%`;
};

export const daysUntil = (iso: string, today = new Date()): number => {
  const d = new Date(iso);
  const ms = d.getTime() - today.getTime();
  return Math.ceil(ms / (1000 * 60 * 60 * 24));
};

/** Group-by helper. */
export const groupBy = <T, K extends string | number>(
  list: T[],
  key: (t: T) => K,
): Map<K, T[]> => {
  const map = new Map<K, T[]>();
  for (const item of list) {
    const k = key(item);
    if (!map.has(k)) map.set(k, []);
    map.get(k)!.push(item);
  }
  return map;
};
