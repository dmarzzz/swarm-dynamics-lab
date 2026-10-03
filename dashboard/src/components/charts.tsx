import { useMemo, useRef, useState, useLayoutEffect, type ReactNode } from 'react';
import { scaleLinear, scaleTime, stack, area, line, curveMonotoneX, stackOrderNone, max, timeHour } from 'd3';
import { fmt, hourET, clockET } from '../lib/format';

export function useWidth<T extends HTMLElement>(initial = 600) {
  const ref = useRef<T>(null);
  const [w, setW] = useState(initial);
  useLayoutEffect(() => {
    const el = ref.current;
    if (!el) return;
    const ro = new ResizeObserver(([e]) => setW(Math.max(120, Math.floor(e.contentRect.width))));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  return [ref, w] as const;
}

export interface Series { key: string; label: string; color: string }

/** Stacked area over time with an hour axis in ET, a "hackathon start" marker and a hover readout. */
export function StackedArea({ rows, series, height = 220, marker, cumulative = false, unit = 'sources', caption }: {
  rows: { t: number; values: Record<string, number> }[];
  series: Series[];
  height?: number;
  marker?: { t: number; label: string };
  cumulative?: boolean;
  unit?: string;
  caption?: ReactNode;
}) {
  const [ref, w] = useWidth<HTMLDivElement>();
  const [hover, setHover] = useState<number | null>(null);
  const m = { t: 10, r: 8, b: 24, l: 40 };
  const data = useMemo(() => {
    if (!cumulative) return rows.map((r) => ({ t: r.t, ...r.values }));
    const acc: Record<string, number> = {};
    return rows.map((r) => {
      for (const s of series) acc[s.key] = (acc[s.key] ?? 0) + (r.values[s.key] ?? 0);
      return { t: r.t, ...acc };
    });
  }, [rows, series, cumulative]);
  const keys = series.map((s) => s.key);
  const stacked = useMemo(() => stack<Record<string, number>>().keys(keys).order(stackOrderNone)(data as unknown as Record<string, number>[]), [data, keys.join()]);
  if (!rows.length) return <div ref={ref} className="muted small">No data yet.</div>;
  const x = scaleTime().domain([rows[0].t, rows[rows.length - 1].t]).range([m.l, w - m.r]);
  const top = max(stacked.at(-1) ?? [], (d) => d[1]) ?? 1;
  const y = scaleLinear().domain([0, top || 1]).nice(4).range([height - m.b, m.t]);
  const ar = area<[number, number] & { data: Record<string, number> }>()
    .x((d) => x(d.data.t)).y0((d) => y(d[0])).y1((d) => y(d[1])).curve(curveMonotoneX);
  const ln = line<[number, number] & { data: Record<string, number> }>().x((d) => x(d.data.t)).y((d) => y(d[1])).curve(curveMonotoneX);
  const span = (rows[rows.length - 1].t - rows[0].t) / 3600e3;
  const ticks = x.ticks(timeHour.every(Math.max(1, Math.ceil(span / (w < 480 ? 4 : 9))))!);
  const hi = hover != null ? data[hover] as unknown as Record<string, number> : null;
  const onMove = (ev: React.PointerEvent<SVGRectElement>) => {
    const r = ev.currentTarget.getBoundingClientRect();
    const t = x.invert(ev.clientX - r.left + m.l).getTime();
    let best = 0, bd = Infinity;
    rows.forEach((row, i) => { const dd = Math.abs(row.t - t); if (dd < bd) { bd = dd; best = i; } });
    setHover(best);
  };
  return (
    <figure ref={ref} style={{ margin: 0, position: 'relative' }}>
      <svg className="chart" width={w} height={height} role="img" aria-label={typeof caption === 'string' ? caption : `Stacked ${unit} over time`}>
        <g className="grid">{y.ticks(4).map((v) => <line key={v} x1={m.l} x2={w - m.r} y1={y(v)} y2={y(v)} />)}</g>
        {y.ticks(4).map((v) => <text key={v} x={m.l - 8} y={y(v)} dy="0.32em" textAnchor="end">{fmt(v)}</text>)}
        {stacked.map((s, i) => (
          <g key={s.key}>
            <path d={ar(s as never) ?? ''} fill={series[i].color} fillOpacity={0.78} />
            <path d={ln(s as never) ?? ''} fill="none" stroke="var(--paper)" strokeWidth={0.75} strokeOpacity={0.7} />
          </g>
        ))}
        <line x1={m.l} x2={w - m.r} y1={height - m.b + 0.5} y2={height - m.b + 0.5} stroke="var(--rule-strong)" />
        {ticks.map((t) => (
          <text key={+t} x={x(t)} y={height - 6} textAnchor="middle">{hourET(+t)}</text>
        ))}
        {marker && marker.t >= rows[0].t && (
          <g className="now">
            <line x1={x(marker.t)} x2={x(marker.t)} y1={m.t - 4} y2={height - m.b} strokeDasharray="2 3" />
            <text x={x(marker.t) + 6} y={m.t + 6} style={{ fill: 'var(--accent-ink)' }}>{marker.label}</text>
          </g>
        )}
        {hover != null && (
          <line x1={x(rows[hover].t)} x2={x(rows[hover].t)} y1={m.t} y2={height - m.b} stroke="var(--ink)" strokeOpacity={0.5} />
        )}
        <rect x={m.l} y={0} width={Math.max(0, w - m.l - m.r)} height={height} fill="transparent"
          onPointerMove={onMove} onPointerLeave={() => setHover(null)} />
      </svg>
      {hi && hover != null && (
        <div className="tip" style={{ left: Math.min(w - 190, Math.max(0, x(rows[hover].t) + 10)), top: 8 }}>
          <div className="tip-h">{clockET(rows[hover].t)} ET{cumulative ? ', running total' : ''}</div>
          {series.slice().reverse().map((s) => (hi[s.key] ? (
            <div key={s.key} className="tip-r"><span className="sw" style={{ background: s.color }} />{s.label}<b className="num">{fmt(hi[s.key])}</b></div>
          ) : null))}
        </div>
      )}
      {caption && <figcaption className="small muted" style={{ marginTop: 6 }}>{caption}</figcaption>}
    </figure>
  );
}

/** Thin horizontal stacked bar for composition (e.g. kinds within a topic). */
export function CompositionBar({ parts, total, height = 8, label }: {
  parts: { key: string; value: number; color: string; label: string }[]; total?: number; height?: number; label?: string;
}) {
  const sum = total ?? parts.reduce((s, p) => s + p.value, 0);
  return (
    <div role="img" aria-label={label ?? parts.map((p) => `${p.label} ${p.value}`).join(', ')}
      style={{ display: 'flex', height, width: '100%', background: 'var(--paper-2)', borderRadius: 1, overflow: 'hidden', gap: 1 }}>
      {parts.filter((p) => p.value > 0).map((p) => (
        <div key={p.key} title={`${p.label}: ${fmt(p.value)}`} style={{ flex: `${p.value / Math.max(1, sum)} 0 0`, background: p.color, minWidth: 2 }} />
      ))}
    </div>
  );
}

/** Small multiple: one column chart per row, honest y from zero, shared scale optional. */
export function Spark({ values, color = 'var(--ink-2)', width = 120, height = 28, maxV }: {
  values: number[]; color?: string; width?: number; height?: number; maxV?: number;
}) {
  const mx = maxV ?? Math.max(1, ...values);
  const bw = width / Math.max(1, values.length);
  return (
    <svg width={width} height={height} aria-hidden="true" style={{ display: 'block' }}>
      <line x1={0} x2={width} y1={height - 0.5} y2={height - 0.5} stroke="var(--rule)" />
      {values.map((v, i) => v > 0 && (
        <rect key={i} x={i * bw + 0.5} width={Math.max(1, bw - 1)} y={height - 1 - (v / mx) * (height - 2)} height={(v / mx) * (height - 2)} fill={color} />
      ))}
    </svg>
  );
}
