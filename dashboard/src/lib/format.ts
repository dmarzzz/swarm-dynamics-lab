const nf = new Intl.NumberFormat('en-US');
export const fmt = (n: number) => nf.format(Math.round(n));
export const fmt1 = (n: number) => (n >= 10 ? fmt(n) : n.toFixed(1).replace(/\.0$/, ''));

const WORDS = ['zero', 'one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine', 'ten', 'eleven', 'twelve'];
export const word = (n: number) => (n >= 0 && n < WORDS.length ? WORDS[n] : fmt(n));
export const Word = (n: number) => { const w = word(n); return w.charAt(0).toUpperCase() + w.slice(1); };

export const plural = (n: number, one: string, many = one + 's') => (n === 1 ? one : many);

export function parseT(s: string | null | undefined): number | null {
  if (!s) return null;
  const t = Date.parse(s.length === 17 && s.endsWith('Z') ? s.replace('Z', ':00Z') : s);
  return Number.isFinite(t) ? t : null;
}

export function ago(t: number | null, now = Date.now()): string {
  if (t == null) return 'unknown';
  const s = Math.max(0, (now - t) / 1000);
  if (s < 60) return 'just now';
  const m = s / 60;
  if (m < 60) return `${Math.round(m)} min ago`;
  const h = m / 60;
  if (h < 24) return `${h < 10 ? h.toFixed(1).replace(/\.0$/, '') : Math.round(h)} h ago`;
  return `${Math.round(h / 24)} d ago`;
}

const timeFmt = new Intl.DateTimeFormat('en-US', { hour: 'numeric', minute: '2-digit', timeZone: 'America/New_York' });
export const clockET = (t: number) => timeFmt.format(t).replace(' ', '\u202f').toLowerCase();
const hourFmt = new Intl.DateTimeFormat('en-US', { hour: 'numeric', timeZone: 'America/New_York' });
export const hourET = (t: number) => hourFmt.format(t).replace(' ', '').toLowerCase();

export function shortAgent(id: string) {
  const [team, name] = id.split('/');
  return { team, name: name ?? id };
}
