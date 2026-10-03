import { useMemo, useState } from 'react';
import type { Dataset, Kind } from '../data/types';
import { derive } from '../data/derive';
import { HACK_START, KINDS, KIND_LABEL, kindColor, teamColor, TEAMS } from '../data/meta';
import { clockET, fmt, hourET, parseT, plural, Word } from '../lib/format';
import { StackedArea, useWidth } from '../components/charts';
import { scaleLinear, scaleSqrt, quantile } from 'd3';
import './timeline.css';

export function Timeline({ data }: { data: Dataset }) {
  const d = useMemo(() => derive(data), [data]);
  const [by, setBy] = useState<'team' | 'kind'>('kind');
  const [mode, setMode] = useState<'rate' | 'total'>('rate');

  const rows = useMemo(() => d.buckets.map((b) => ({ t: b.t, values: by === 'kind' ? (b.byKind as Record<string, number>) : b.byTeam })), [d.buckets, by]);
  const series = by === 'kind'
    ? KINDS.map((k) => ({ key: k, label: KIND_LABEL[k], color: kindColor(k) }))
    : TEAMS.map((t) => ({ key: t, label: t, color: teamColor(t) }));
  const peak = useMemo(() => d.buckets.reduce((m, b) => (b.total > m.total ? b : m), d.buckets[0]), [d.buckets]);

  // Commit river: one lane per agent with >0 entries, one mark per 15-min bucket sized by count.
  const river = useMemo(() => {
    const m = new Map<string, { agent: string; team: string; total: number; first: number; cells: Map<number, { n: number; kinds: Partial<Record<Kind, number>> }> }>();
    for (const r of data.timeline) {
      const t = parseT(r.t);
      if (t == null) continue;
      const b = Math.floor(t / d.bucketMs) * d.bucketMs;
      const a = m.get(r.agent) ?? { agent: r.agent, team: r.team, total: 0, first: t, cells: new Map() };
      a.total += r.n_entries;
      a.first = Math.min(a.first, t);
      const c = a.cells.get(b) ?? { n: 0, kinds: {} };
      c.n += r.n_entries;
      c.kinds[r.kind] = (c.kinds[r.kind] ?? 0) + r.n_entries;
      a.cells.set(b, c);
      m.set(r.agent, a);
    }
    return [...m.values()].sort((a, b) => TEAMS.indexOf(a.team as never) - TEAMS.indexOf(b.team as never) || a.first - b.first);
  }, [data.timeline, d.bucketMs]);

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow"><span className="tick" />Timeline</p>
        <h1 className="display">The busiest quarter hour was <em>{clockET(peak?.t ?? 0)}</em>, when agents added {fmt(peak?.total ?? 0)} sources.</h1>
        <p className="lede">
          Every library entry carries the time its file first appeared in git. These charts are built from that, in 15 minute buckets, Eastern time.
          Bursts mark batch pushes: agents commit locally and the sync timer pushes every ten minutes.
        </p>
      </section>

      <section className="wrap">
        <div className="section-head">
          <div>
            <h2 className="h2">{mode === 'rate' ? 'Sources added per 15 minutes' : 'Running total'}</h2>
            <p className="reading">{fmt(d.sinceStart)} since noon, an average of {fmt(d.perHourAvg)} an hour.</p>
          </div>
          <div className="tl-ctrl">
            <div className="seg" role="group" aria-label="Measure">
              <button aria-pressed={mode === 'rate'} onClick={() => setMode('rate')}>Rate</button>
              <button aria-pressed={mode === 'total'} onClick={() => setMode('total')}>Total</button>
            </div>
            <div className="seg" role="group" aria-label="Colour by">
              <button aria-pressed={by === 'kind'} onClick={() => setBy('kind')}>By kind</button>
              <button aria-pressed={by === 'team'} onClick={() => setBy('team')}>By team</button>
            </div>
          </div>
        </div>
        <StackedArea rows={rows} series={series} height={300} cumulative={mode === 'total'} marker={{ t: HACK_START, label: 'Noon, start' }} />
        <div className="legend" style={{ marginTop: 10 }}>
          {series.map((s) => <span key={s.key}><i className="sw" style={{ background: s.color }} />{s.label}</span>)}
        </div>
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div>
            <h2 className="h2">Commit river</h2>
            <p className="reading">
              {Word(river.length)} {plural(river.length, 'agent has', 'agents have')} added sources. One lane per agent, grouped by team and ordered by when it started.
              Each mark is a 15 minute window; size is the number of sources (capped so one big push does not hide the rest), colour is the dominant kind.
            </p>
          </div>
        </div>
        <River lanes={river} start={d.buckets[0]?.t ?? 0} end={d.now} bucketMs={d.bucketMs} />
      </section>
    </>
  );
}

function River({ lanes, start, end, bucketMs }: {
  lanes: { agent: string; team: string; total: number; cells: Map<number, { n: number; kinds: Partial<Record<Kind, number>> }> }[];
  start: number; end: number; bucketMs: number;
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<{ x: number; y: number; agent: string; t: number; n: number; kinds: Partial<Record<Kind, number>> } | null>(null);
  const narrow = w < 640;
  const labelW = narrow ? 0 : 190;
  const laneH = narrow ? 16 : 18;
  const m = { t: 24, r: 50 };
  const x = scaleLinear().domain([start, end]).range([labelW + 8, w - m.r]);
  const ns = lanes.flatMap((l) => [...l.cells.values()].map((c) => c.n)).sort((a, b) => a - b);
  const maxN = Math.max(4, quantile(ns, 0.9) ?? 1);
  const r = scaleSqrt().domain([0, maxN]).range([0, laneH * 0.82]).clamp(true);
  const H = m.t + lanes.length * laneH + 8;
  const hours: number[] = [];
  for (let t = Math.ceil(start / 3600e3) * 3600e3; t <= end; t += 3600e3) hours.push(t);
  let prevTeam = '';
  return (
    <div ref={ref} className="river" style={{ position: 'relative' }}>
      <svg width={w} height={H} className="chart" role="img" aria-label={`Commit river, ${lanes.length} agents`}>
        {hours.map((t) => (
          <g key={t}>
            <line x1={x(t)} x2={x(t)} y1={m.t - 6} y2={H} stroke="var(--rule)" strokeDasharray="1 3" />
            <text x={x(t)} y={12} textAnchor="middle">{hourET(t)}</text>
          </g>
        ))}
        {HACK_START > start && <line x1={x(HACK_START)} x2={x(HACK_START)} y1={m.t - 6} y2={H} stroke="var(--accent)" strokeDasharray="2 3" />}
        {lanes.map((l, i) => {
          const y = m.t + i * laneH + laneH / 2;
          const sep = l.team !== prevTeam && i > 0;
          prevTeam = l.team;
          const [team, name] = l.agent.split('/');
          return (
            <g key={l.agent}>
              {sep && <line x1={0} x2={w} y1={y - laneH / 2} y2={y - laneH / 2} stroke="var(--rule-strong)" />}
              {!narrow && (
                <text x={0} y={y} dy="0.32em" style={{ fontFamily: 'var(--f-mono)', fontSize: 11, fill: 'var(--ink-2)' }}>
                  <tspan style={{ fill: teamColor(team) }}>● </tspan><tspan style={{ fill: 'var(--muted)' }}>{team}/</tspan>{(name ?? '').slice(0, 20)}
                </text>
              )}
              <line x1={x(start)} x2={w - m.r} y1={y} y2={y} stroke="var(--rule)" />
              {[...l.cells.entries()].map(([t, c]) => {
                const dom = (Object.entries(c.kinds).sort((a, b) => (b[1] ?? 0) - (a[1] ?? 0))[0]?.[0] ?? 'paper') as Kind;
                const cx = x(t + bucketMs / 2);
                return (
                  <circle key={t} cx={cx} cy={y} r={Math.max(1.6, r(c.n) / 2)} fill={kindColor(dom)} fillOpacity={0.85}
                    onPointerEnter={() => setHover({ x: cx, y, agent: l.agent, t, n: c.n, kinds: c.kinds })} onPointerLeave={() => setHover(null)} />
                );
              })}
              <text x={w - m.r + 8} y={y} dy="0.32em" style={{ fontVariantNumeric: 'tabular-nums' }}>{fmt(l.total)}</text>
            </g>
          );
        })}
      </svg>
      {hover && (
        <div className="tip" style={{ left: Math.min(w - 200, hover.x + 12), top: hover.y + 8 }}>
          <div className="tip-h mono">{hover.agent}</div>
          <div className="tip-h">{clockET(hover.t)} to {clockET(hover.t + bucketMs)} ET</div>
          {KINDS.filter((k) => hover.kinds[k]).map((k) => (
            <div key={k} className="tip-r"><span className="sw" style={{ background: kindColor(k) }} />{KIND_LABEL[k]}<b className="num">{hover.kinds[k]}</b></div>
          ))}
        </div>
      )}
    </div>
  );
}
