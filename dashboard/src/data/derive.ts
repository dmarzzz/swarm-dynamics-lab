import type { Dataset, Entry, Kind, Task } from './types';
import { ACTIVE_STATES, HACK_START, KINDS, teamOf } from './meta';
import { parseT } from '../lib/format';

export interface Derived {
  now: number;
  entryTimes: Map<string, number>;
  first: number;
  /** Per-bucket counts of new entries, one row per 15 min bucket, keyed by kind and team. */
  buckets: { t: number; byKind: Record<Kind, number>; byTeam: Record<string, number>; total: number }[];
  bucketMs: number;
  lastHour: number;
  prevHour: number;
  sinceStart: number;
  perHourAvg: number;
  agentsLastHour: { agent: string; team: string; n: number; kinds: Partial<Record<Kind, number>> }[];
  activeAgents: number;
  teams: { team: string; entries: number; agents: number; active: number }[];
  fullReads: number;
  humanAsks: { kind: 'task' | 'review' | 'blocked' | 'stale'; title: string; who: string | null; href?: string; detail?: string }[];
  topicsWithSurvey: number;
}

const BUCKET = 15 * 60 * 1000;

export function derive(d: Dataset): Derived {
  const gen = parseT(d.summary.generated_at) ?? Date.now();
  const entryTimes = new Map<string, number>();
  let first = Infinity;
  let maxT = 0;
  for (const e of d.library) {
    const t = parseT(e.added_at);
    if (t == null) continue;
    entryTimes.set(e.id, t);
    if (t < first) first = t;
    if (t > maxT) maxT = t;
  }
  const now = Math.max(gen, maxT);
  const start = Math.floor(Math.min(first, HACK_START) / BUCKET) * BUCKET;
  const end = Math.ceil(now / BUCKET) * BUCKET;
  const n = Math.max(1, Math.round((end - start) / BUCKET));
  const buckets = Array.from({ length: n }, (_, i) => ({
    t: start + i * BUCKET,
    byKind: Object.fromEntries(KINDS.map((k) => [k, 0])) as Record<Kind, number>,
    byTeam: {} as Record<string, number>,
    total: 0,
  }));
  let lastHour = 0, prevHour = 0, sinceStart = 0;
  const agentMap = new Map<string, { agent: string; team: string; n: number; kinds: Partial<Record<Kind, number>> }>();
  for (const e of d.library) {
    const t = entryTimes.get(e.id);
    if (t == null) continue;
    const i = Math.min(n - 1, Math.max(0, Math.floor((t - start) / BUCKET)));
    const b = buckets[i];
    b.byKind[e.kind] = (b.byKind[e.kind] ?? 0) + 1;
    const team = teamOf(e.added_by);
    b.byTeam[team] = (b.byTeam[team] ?? 0) + 1;
    b.total++;
    if (t >= HACK_START) sinceStart++;
    if (t > now - 3600e3) {
      lastHour++;
      const a = agentMap.get(e.added_by) ?? { agent: e.added_by, team, n: 0, kinds: {} };
      a.n++;
      a.kinds[e.kind] = (a.kinds[e.kind] ?? 0) + 1;
      agentMap.set(e.added_by, a);
    } else if (t > now - 7200e3) prevHour++;
  }
  const hours = Math.max(0.25, (now - Math.max(HACK_START, first)) / 3600e3);
  const agentsLastHour = [...agentMap.values()].sort((a, b) => b.n - a.n);

  const teams = new Map<string, { team: string; entries: number; agents: number; active: number }>();
  for (const a of d.agents) {
    const t = teams.get(a.team) ?? { team: a.team, entries: 0, agents: 0, active: 0 };
    t.agents++;
    if (ACTIVE_STATES.has(a.state)) t.active++;
    teams.set(a.team, t);
  }
  for (const e of d.library) {
    const team = teamOf(e.added_by);
    const t = teams.get(team) ?? { team, entries: 0, agents: 0, active: 0 };
    t.entries++;
    teams.set(team, t);
  }

  return {
    now, entryTimes, first, buckets, bucketMs: BUCKET,
    lastHour, prevHour, sinceStart, perHourAvg: sinceStart / hours,
    agentsLastHour,
    activeAgents: d.agents.filter((a) => ACTIVE_STATES.has(a.state)).length,
    teams: [...teams.values()].filter((t) => t.team !== 'unknown').sort((a, b) => b.entries - a.entries),
    fullReads: d.library.filter((e) => e.read_depth === 'full' || e.read_depth === 'ran').length,
    humanAsks: humanAsks(d, now),
    topicsWithSurvey: new Set(d.surveys.map((s) => s.topic)).size,
  };
}

function humanAsks(d: Dataset, now: number): Derived['humanAsks'] {
  const out: Derived['humanAsks'] = [];
  const repo = 'https://github.com/dmarzzz/swarm-lab/blob/main/';
  for (const t of d.tasks as Task[]) {
    if (t.status === 'done') continue;
    const owner = t.owner ? teamOf(t.owner) : null;
    if (t.kind === 'admin' || (t.for && (t.owner == null || t.owner.endsWith('/human')))) {
      out.push({ kind: 'task', title: t.title, who: t.for ?? owner, href: `${repo}tasks/${t.id}.md`, detail: t.priority ?? undefined });
    } else if (t.kind === 'review' && t.status === 'open') {
      out.push({ kind: 'review', title: t.title, who: t.for, href: `${repo}tasks/${t.id}.md`, detail: 'needs a reviewer from another team' });
    }
  }
  for (const a of d.agents) {
    if (a.state === 'blocked') out.push({ kind: 'blocked', title: a.doing || 'Agent is blocked', who: a.id, detail: 'agent blocked' });
  }
  for (const s of d.surveys) {
    if (s.gate.passes && !s.reviewed_by.filter(Boolean).length) {
      out.push({ kind: 'review', title: `Review the ${s.topic} survey`, who: null, detail: 'passes the gate, waiting on a cross-team review' });
    }
  }
  void now;
  return out;
}

export function countBy<T>(arr: T[], key: (x: T) => string | null | undefined) {
  const m = new Map<string, number>();
  for (const x of arr) { const k = key(x); if (k == null) continue; m.set(k, (m.get(k) ?? 0) + 1); }
  return m;
}

export const yearOf = (e: Entry) => (typeof e.year === 'number' ? e.year : Number.parseInt(String(e.year ?? ''), 10) || null);
