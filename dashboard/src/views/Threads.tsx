import { useEffect, useMemo, useRef, useState } from 'react';
import { forceSimulation, forceLink, forceManyBody, forceCollide, forceX, forceY, scaleSqrt } from 'd3';
import type { Dataset, Entry, ThreadMeta } from '../data/types';
import { topicName } from '../data/meta';
import { fmt, plural, word, Word } from '../lib/format';
import { href, useParamSetter } from '../lib/router';
import { EntryDrawer } from '../components/EntryDrawer';
import { renderer, type Vertex } from '../graph/renderer';
import './threads.css';

type SizeBy = 'likes' | 'views' | 'posts';
const SIZE_LABEL: Record<SizeBy, string> = { likes: 'Likes', views: 'Views', posts: 'Length' };

interface TopicNode { type: 'topic'; id: string; slug: string; n: number; likes: number; r: number; x: number; y: number; color: string }
interface ThreadNode { type: 'thread'; id: string; e: Entry; m: ThreadMeta | undefined; slug: string; r: number; x: number; y: number; color: string; hay: string }
type Node = TopicNode | ThreadNode;

/** Fourteen hues at one lightness and chroma so no topic shouts. Rank order, biggest topic first. */
const HUES = [30, 230, 140, 75, 290, 185, 335, 105, 255, 50, 160, 310, 205, 15];
function topicColor(rank: number, dark: boolean) {
  const h = HUES[rank % HUES.length];
  return dark ? `oklch(0.74 0.11 ${h})` : `oklch(0.58 0.12 ${h})`;
}
let probe: CanvasRenderingContext2D | null = null;
function toHex(css: string) {
  probe ??= document.createElement('canvas').getContext('2d', { willReadFrequently: true });
  if (!probe) return '#888888';
  probe.fillStyle = '#000';
  probe.fillStyle = css;
  probe.clearRect(0, 0, 1, 1);
  probe.fillRect(0, 0, 1, 1);
  const [r, g, b] = probe.getImageData(0, 0, 1, 1).data;
  return '#' + [r, g, b].map((v) => v.toString(16).padStart(2, '0')).join('');
}
function useDark() {
  const [dark, setDark] = useState(() => document.documentElement.dataset.theme === 'dark');
  useEffect(() => {
    const mo = new MutationObserver(() => setDark(document.documentElement.dataset.theme === 'dark'));
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ['data-theme'] });
    return () => mo.disconnect();
  }, []);
  return dark;
}

interface Label { slug: string; x: number; y: number; r: number; n: number; hidden?: boolean }
/** Greedy placement, biggest topic first: above the hub, then below, then hidden. Focused or hovered topics always win. */
function placeLabels(labels: Label[], width: number, height: number, focus: string, hovered: string): Label[] {
  const boxes: { x0: number; x1: number; y0: number; y1: number }[] = [];
  const pri = (l: Label) => (l.slug === focus || l.slug === hovered ? 1 : 0);
  const order = [...labels].sort((a, b) => pri(b) - pri(a) || b.n - a.n);
  const out: Label[] = [];
  for (const l of order) {
    const w = (topicName(l.slug).length + String(l.n).length + 1) * 6.4 + 14, h = 18;
    let spot: number | null = null;
    for (const y of [l.y - l.r - 4, l.y + l.r + 22]) {
      const box = { x0: l.x - w / 2, x1: l.x + w / 2, y0: y - h, y1: y };
      const inside = box.x0 > 2 && box.x1 < width - 2 && box.y0 > 2 && box.y1 < height - 2;
      if (inside && !boxes.some((b) => box.x0 < b.x1 && box.x1 > b.x0 && box.y0 < b.y1 && box.y1 > b.y0)) { boxes.push(box); spot = y; break; }
    }
    out.push({ ...l, y: spot ?? l.y - l.r - 4, hidden: spot == null });
  }
  return out;
}

const dateFmt = new Intl.DateTimeFormat('en-US', { month: 'short', day: 'numeric', year: 'numeric', timeZone: 'UTC' });
const niceDate = (d: string | null | undefined) => (d ? dateFmt.format(Date.parse(`${d}T00:00:00Z`)) : null);

export function Threads({ data, params }: { data: Dataset; params: URLSearchParams }) {
  const set = useParamSetter('/threads');
  const focus = params.get('t') ?? '';
  const query = params.get('q') ?? '';
  const open = params.get('e');
  const sizeBy = ((params.get('size') as SizeBy) || 'likes') as SizeBy;
  const dark = useDark();

  const threads = useMemo(() => data.library.filter((e) => e.kind === 'thread'), [data.library]);
  const meta = useMemo(() => new Map((data.threads ?? []).map((t) => [t.id, t])), [data.threads]);
  const byId = useMemo(() => new Map(data.library.map((e) => [e.id, e])), [data.library]);

  const topics = useMemo(() => {
    const m = new Map<string, { n: number; likes: number }>();
    for (const e of threads) for (const s of e.topics) {
      const t = m.get(s) ?? { n: 0, likes: 0 };
      t.n++; t.likes += meta.get(e.id)?.likes ?? 0;
      m.set(s, t);
    }
    return [...m].map(([slug, v]) => ({ slug, ...v })).sort((a, b) => b.n - a.n || a.slug.localeCompare(b.slug));
  }, [threads, meta]);
  const rank = useMemo(() => new Map(topics.map((t, i) => [t.slug, i])), [topics]);
  const colorOf = (slug: string) => topicColor(rank.get(slug) ?? 13, dark);
  const hexOf = useMemo(() => {
    const m = new Map<string, string>();
    for (const t of topics) m.set(t.slug, toHex(colorOf(t.slug)));
    return m;
  }, [topics, dark]);

  const hasMetric = (k: SizeBy) => threads.some((e) => (meta.get(e.id)?.[k] ?? null) != null);
  const sizeOptions = (['likes', 'views', 'posts'] as SizeBy[]).filter(hasMetric);
  const value = (e: Entry) => { const m = meta.get(e.id); const v = m?.[sizeBy]; return typeof v === 'number' ? v : 0; };

  // Layout: a bipartite force graph, topics as hubs, threads as leaves. Computed once per dataset and size mode.
  const world = useMemo(() => {
    const maxV = Math.max(1, ...threads.map(value));
    const rScale = scaleSqrt().domain([0, maxV]).range([2.4, 13]);
    const maxN = Math.max(1, ...topics.map((t) => t.n));
    const tScale = scaleSqrt().domain([0, maxN]).range([9, 26]);
    const golden = 2.399963;
    const tnodes: TopicNode[] = topics.map((t, i) => ({
      type: 'topic', id: `topic:${t.slug}`, slug: t.slug, n: t.n, likes: t.likes, r: tScale(t.n),
      x: Math.cos(i * golden) * (40 + i * 22), y: Math.sin(i * golden) * (40 + i * 22), color: t.slug,
    }));
    const tIndex = new Map(tnodes.map((t) => [t.slug, t]));
    const nodes: ThreadNode[] = threads.map((e, i) => {
      const m = meta.get(e.id);
      const slug = e.topics[0] ?? topics[topics.length - 1]?.slug ?? '';
      const hub = tIndex.get(slug);
      const a = i * golden;
      return {
        type: 'thread', id: e.id, e, m, slug, r: rScale(value(e)), color: slug,
        x: (hub?.x ?? 0) + Math.cos(a) * 30, y: (hub?.y ?? 0) + Math.sin(a) * 30,
        hay: `${m?.handle ?? ''} ${m?.name ?? ''} ${e.title} ${m?.first_line ?? ''}`.toLowerCase(),
      };
    });
    const links = threads.flatMap((e, i) => e.topics.filter((s) => tIndex.has(s)).map((s) => ({ source: nodes[i], target: tIndex.get(s)!, primary: s === e.topics[0] })));
    const all: Node[] = [...tnodes, ...nodes];
    const sim = forceSimulation<Node>(all)
      .force('link', forceLink<Node, { source: Node; target: Node; primary: boolean }>(links).distance((l) => 38 + (l.target as TopicNode).r + (l.source as ThreadNode).r).strength((l) => (l.primary ? 0.9 : 0.25)))
      .force('charge', forceManyBody<Node>().strength((d) => (d.type === 'topic' ? -900 : -9)).distanceMax(420))
      .force('collide', forceCollide<Node>((d) => d.r + (d.type === 'topic' ? 10 : 1.6)).iterations(2))
      // Fields are wider than tall, so gravity pulls harder on y and the cloud settles into a landscape shape.
      .force('x', forceX(0).strength(0.022))
      .force('y', forceY(0).strength(0.075))
      .alphaDecay(0.035)
      .stop();
    return { sim, nodes: all, topics: tnodes, threads: nodes, links };
  }, [threads, topics, meta, sizeBy]);

  const host = useRef<HTMLDivElement>(null);
  const canvas = useRef<HTMLCanvasElement>(null);
  const [hover, setHover] = useState<ThreadNode | TopicNode | null>(null);
  const [labels, setLabels] = useState<Label[]>([]);
  const [mode, setMode] = useState('');
  const live = useRef({ focus, query, hover, hexOf, dark });
  live.current = { focus, query, hover, hexOf, dark };
  const hit = useRef<{ x: number; y: number; r: number; n: Node }[]>([]);
  const redraw = useRef<() => void>(() => {});

  useEffect(() => {
    if (!canvas.current || !host.current) return;
    const engine = renderer(canvas.current);
    setMode(engine.mode);
    let width = host.current.clientWidth, height = host.current.clientHeight;
    const draw = () => {
      const s = live.current;
      const q = s.query.trim().toLowerCase();
      // Fit the settled layout into the field, keeping aspect.
      let x0 = Infinity, x1 = -Infinity, y0 = Infinity, y1 = -Infinity;
      for (const n of world.nodes) { x0 = Math.min(x0, n.x - n.r); x1 = Math.max(x1, n.x + n.r); y0 = Math.min(y0, n.y - n.r); y1 = Math.max(y1, n.y + n.r); }
      const pad = 30;
      const kx0 = (width - pad * 2) / Math.max(1, x1 - x0), ky0 = (height - pad * 2 - 18) / Math.max(1, y1 - y0);
      // Fit to the field. Positions may stretch up to 20% on one axis; distances here are not measurements.
      const k = Math.min(kx0, ky0);
      const kx = Math.min(kx0, k * 1.2), ky = Math.min(ky0, k * 1.2);
      const cx = (x0 + x1) / 2, cy = (y0 + y1) / 2;
      const px = (x: number) => (x - cx) * kx + width / 2, py = (y: number) => (y - cy) * ky + height / 2 + 9;
      const ink = s.dark ? '#d9d4c8' : '#3b3732';
      const on = (n: Node) => {
        if (n.type === 'topic') return (!s.focus || n.slug === s.focus) && !q;
        return (!s.focus || n.e.topics.includes(s.focus)) && (!q || n.hay.includes(q));
      };
      const points: Vertex[] = [], lines: Vertex[] = [];
      hit.current = [];
      const pos = new Map<Node, Vertex>();
      for (const n of world.nodes) {
        const active = on(n);
        const hovered = s.hover?.id === n.id;
        const v: Vertex = { x: px(n.x), y: py(n.y), color: s.hexOf.get(n.slug) ?? '#888888', alpha: n.type === 'topic' ? (active ? 0.28 : 0.08) : active ? (hovered ? 1 : 0.86) : 0.07, size: n.r * 2 + (hovered ? 3 : 0) };
        pos.set(n, v);
        if (active || n.type === 'topic') hit.current.push({ x: v.x, y: v.y, r: Math.max(5, n.r + 1), n });
      }
      for (const l of world.links) {
        const a = pos.get(l.source as Node)!, b = pos.get(l.target as Node)!;
        const src = l.source as ThreadNode, tgt = l.target as TopicNode;
        const active = on(src) && (!s.focus || tgt.slug === s.focus || on(tgt));
        const hovered = s.hover?.id === src.id || (s.hover?.type === 'topic' && s.hover.slug === tgt.slug && on(src));
        const alpha = hovered ? 0.6 : active ? (l.primary ? 0.16 : 0.07) : 0.015;
        lines.push({ ...a, color: hovered ? (s.dark ? '#f1ece2' : '#2a2724') : b.color, alpha }, { ...b, color: hovered ? ink : b.color, alpha });
      }
      // Topics draw on top as a ring: a filled disc plus a thin dark core so the hub reads as a hub.
      for (const t of world.topics) {
        const v = pos.get(t)!;
        points.push(v, { ...v, color: v.color, alpha: on(t) ? 0.9 : 0.25, size: 7 });
      }
      for (const n of world.threads) points.push(pos.get(n)!);
      engine.draw(points, lines, width, height, Math.min(devicePixelRatio, 2));
      setLabels(placeLabels(world.topics.map((t) => ({ slug: t.slug, x: px(t.x), y: py(t.y), r: t.r, n: t.n })), width, height, s.focus, s.hover?.type === 'topic' ? s.hover.slug : ''));
    };
    redraw.current = draw;
    const ro = new ResizeObserver(([e]) => { width = e.contentRect.width; height = e.contentRect.height; draw(); });
    ro.observe(host.current);
    const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
    const sim = world.sim;
    let frame = 0;
    if (reduced) { sim.tick(220); draw(); }
    else {
      sim.alpha(1);
      const step = () => {
        sim.tick(3);
        draw();
        if (sim.alpha() > sim.alphaMin()) frame = requestAnimationFrame(step);
      };
      frame = requestAnimationFrame(step);
    }
    return () => { cancelAnimationFrame(frame); ro.disconnect(); engine.dispose(); };
  }, [world]);
  useEffect(() => { redraw.current(); }, [focus, query, hover, hexOf]);

  const pick = (ev: React.PointerEvent<HTMLCanvasElement>) => {
    const r = ev.currentTarget.getBoundingClientRect();
    const x = ev.clientX - r.left, y = ev.clientY - r.top;
    let best: Node | null = null, bd = Infinity;
    for (const h of hit.current) {
      const d = Math.hypot(h.x - x, h.y - y) - h.r;
      if (d < 6 && d < bd) { bd = d; best = h.n; }
    }
    return best;
  };
  const hoverPos = hover ? hit.current.find((h) => h.n.id === hover.id) : null;
  const fieldW = host.current?.clientWidth ?? 800;

  const visible = useMemo(() => {
    const q = query.trim().toLowerCase();
    return world.threads.filter((n) => (!focus || n.e.topics.includes(focus)) && (!q || n.hay.includes(q)));
  }, [world, focus, query]);
  const top = useMemo(() => [...visible].sort((a, b) => (b.m?.likes ?? -1) - (a.m?.likes ?? -1)).slice(0, 8), [visible]);
  const handles = useMemo(() => {
    const m = new Map<string, number>();
    for (const n of visible) { const h = n.m?.handle; if (h) m.set(h, (m.get(h) ?? 0) + 1); }
    return [...m].sort((a, b) => b[1] - a[1]).slice(0, 10);
  }, [visible]);
  const withMetric = threads.filter((e) => meta.get(e.id)?.likes != null).length;
  const maxN = Math.max(1, ...topics.map((t) => t.n));
  const multi = threads.filter((e) => e.topics.length > 1).length;
  const openEntry = byId.get(open ?? '') ?? null;

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow"><span className="tick" />X threads</p>
        <h1 className="display">
          {fmt(threads.length)} X threads across {word(topics.length)} topics, <em>most of them on {topicName(topics[0]?.slug ?? '')}</em> and {topicName(topics[1]?.slug ?? '')}.
        </h1>
        <p className="lede">
          Each small dot is a thread the agents catalogued from X, pulled toward the topics it is tagged with. {Word(multi)} {plural(multi, 'thread sits', 'threads sit')} between two or more topics.
          Dot size is {SIZE_LABEL[sizeBy].toLowerCase()} on the root post{sizeBy === 'posts' ? ', counted in posts' : ''}, as recorded at catalogue time; {fmt(withMetric)} of {fmt(threads.length)} carry engagement numbers.
          Hover for the author and opening line, click to read the entry.
        </p>
      </section>

      <section className="wrap">
        <div className="xt-tools">
          <label className="xt-search">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none" stroke="currentColor" strokeWidth="1.3" aria-hidden="true"><circle cx="6" cy="6" r="4.2" /><path d="M9.2 9.2L13 13" /></svg>
            <input className="input" type="search" placeholder="Handle, author or words from the thread" value={query} onChange={(ev) => set({ q: ev.target.value || null })} aria-label="Filter threads" />
          </label>
          {sizeOptions.length > 1 && (
            <div className="seg" role="group" aria-label="Size dots by">
              {sizeOptions.map((k) => <button key={k} aria-pressed={sizeBy === k} onClick={() => set({ size: k === 'likes' ? null : k })}>{SIZE_LABEL[k]}</button>)}
            </div>
          )}
          {(focus || query) && <button className="btn-text" onClick={() => set({ t: null, q: null })}>Clear</button>}
          <span className="xt-status num">{fmt(visible.length)} of {fmt(threads.length)} in view{mode ? `, ${mode}` : ''}</span>
        </div>

        <div className="grid-12 xt-grid">
          <div className="span-8">
            <div className="xt-field" ref={host}>
              <canvas ref={canvas} aria-label={`${threads.length} X threads connected to the research topics they are tagged with. Use the topic list and the ranked threads below to explore with a keyboard.`}
                onPointerMove={(ev) => setHover(pick(ev))}
                onPointerLeave={() => setHover(null)}
                onClick={(ev) => {
                  const n = pick(ev as unknown as React.PointerEvent<HTMLCanvasElement>);
                  if (!n) return;
                  if (n.type === 'topic') set({ t: focus === n.slug ? null : n.slug });
                  else set({ e: n.id });
                }}
                style={{ cursor: hover ? 'pointer' : 'default' }} />
              <div className="xt-labels" aria-hidden="true">
                {labels.map((l) => (
                  <span key={l.slug} className={`${focus && focus !== l.slug ? 'dim' : ''} ${l.hidden ? 'hidden' : ''}`} style={{ left: l.x, top: l.y }}>
                    {topicName(l.slug)} <small className="num">{l.n}</small>
                  </span>
                ))}
              </div>
              {hover && hoverPos && (
                <div className="tip xt-tip" role="status" style={{ left: Math.min(fieldW - 300, Math.max(0, hoverPos.x + 14)), top: Math.max(0, hoverPos.y - 10) }}>
                  {hover.type === 'topic' ? (
                    <>
                      <div className="tip-h">Topic{focus === hover.slug ? ', click to release' : ', click to focus'}</div>
                      <strong>{topicName(hover.slug)}</strong>
                      <div className="xt-tip-meta">{fmt(hover.n)} {plural(hover.n, 'thread')}{hover.likes ? `, ${fmt(hover.likes)} likes combined` : ''}</div>
                    </>
                  ) : (
                    <>
                      <div className="tip-h"><span className="mono">{hover.m?.handle || 'unknown handle'}</span>{hover.m?.name && hover.m.name !== hover.m.handle.slice(1) ? `, ${hover.m.name}` : ''}{niceDate(hover.m?.date) ? `, ${niceDate(hover.m?.date)}` : ''}</div>
                      <strong className="serif">{hover.m?.first_line || hover.e.title}</strong>
                      <div className="xt-tip-meta">
                        {hover.m?.likes != null ? `${fmt(hover.m.likes)} likes` : 'no engagement recorded'}
                        {hover.m?.views != null ? `, ${fmt(hover.m.views)} views` : ''}
                        {hover.m && hover.m.posts > 1 ? `, ${hover.m.posts} posts` : ''}
                        {' in '}{hover.e.topics.map(topicName).join(', ')}
                      </div>
                    </>
                  )}
                </div>
              )}
            </div>
            <div className="legend xt-legend">
              {topics.map((t) => (
                <button key={t.slug} className={`xt-key ${focus && focus !== t.slug ? 'dim' : ''}`} aria-pressed={focus === t.slug} onClick={() => set({ t: focus === t.slug ? null : t.slug })}>
                  <i className="sw round" style={{ background: colorOf(t.slug) }} />{topicName(t.slug)}
                </button>
              ))}
            </div>
          </div>

          <aside className="span-4 xt-side">
            <div className="section-head xt-side-head">
              <div><h2 className="h2">Threads per topic</h2><p className="reading">Click a topic to light up its threads. Tags overlap, so the bars sum past the total.</p></div>
            </div>
            <div className="xt-bars" role="table" aria-label="Threads per topic">
              {topics.map((t) => {
                const inView = visible.filter((n) => n.e.topics.includes(t.slug)).length;
                return (
                  <button key={t.slug} role="row" className={`xt-bar ${focus === t.slug ? 'on' : ''} ${focus && focus !== t.slug ? 'dim' : ''}`} onClick={() => set({ t: focus === t.slug ? null : t.slug })} aria-pressed={focus === t.slug}>
                    <span role="cell" className="xb-l">{topicName(t.slug)}</span>
                    <span role="cell" className="xb-t">
                      <i style={{ width: `${(t.n / maxN) * 100}%`, background: colorOf(t.slug), opacity: 0.35 }} />
                      <i style={{ width: `${(inView / maxN) * 100}%`, background: colorOf(t.slug) }} />
                    </span>
                    <span role="cell" className="xb-v num">{inView !== t.n ? <><span className="muted">{fmt(inView)} of </span>{fmt(t.n)}</> : fmt(t.n)}</span>
                  </button>
                );
              })}
            </div>

            {handles.length > 0 && (
              <div className="xt-handles">
                <span className="stage-k">Most catalogued handles{focus ? ` in ${topicName(focus)}` : ''}</span>
                <ul className="rows">
                  {handles.map(([h, n]) => (
                    <li key={h}>
                      <button className="xt-handle" onClick={() => set({ q: query === h ? null : h })} aria-pressed={query === h}>
                        <span className="mono">{h}</span><span className="num muted">{fmt(n)}</span>
                      </button>
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </aside>
        </div>
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div><h2 className="h2">Most liked{focus ? ` in ${topicName(focus)}` : ''}{query ? ` matching "${query}"` : ''}</h2><p className="reading">Root-post likes at the time the agent catalogued the thread. Not live.</p></div>
          <a className="more" href={href('/library', { kind: 'thread', topic: focus || null })}>All threads in the library</a>
        </div>
        <ol className="xt-top">
          {top.map((n) => (
            <li key={n.id}>
              <button onClick={() => set({ e: n.id })}>
                <span className="xt-top-h"><i className="sw round" style={{ background: colorOf(n.slug) }} /><span className="mono">{n.m?.handle || n.e.id}</span>{niceDate(n.m?.date) && <span className="muted">{niceDate(n.m?.date)}</span>}</span>
                <span className="xt-top-t serif">{n.m?.first_line || n.e.title}</span>
                <span className="xt-top-m num">{n.m?.likes != null ? `${fmt(n.m.likes)} likes` : 'no count'}{n.m?.views != null ? `, ${fmt(n.m.views)} views` : ''}</span>
              </button>
            </li>
          ))}
          {!top.length && <li className="empty-note">No threads match. Clear the filter or try another handle.</li>}
        </ol>
      </section>

      <EntryDrawer entry={openEntry} byId={byId} onClose={() => set({ e: null })} onOpen={(id) => set({ e: id })} />
    </>
  );
}
