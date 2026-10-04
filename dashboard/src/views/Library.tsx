import { useDeferredValue, useMemo, useRef, useState, useEffect } from 'react';
import {
  useReactTable, getCoreRowModel, getSortedRowModel, flexRender, createColumnHelper, type SortingState,
} from '@tanstack/react-table';
import { useWindowVirtualizer } from '@tanstack/react-virtual';
import type { Dataset, Entry, Kind } from '../data/types';
import { DEPTH_LABEL, DEPTH_ORDER, KINDS, KIND_LABEL, KIND_ONE, kindColor, teamColor, teamOf, topicName, TEAMS } from '../data/meta';
import { fmt, Word, plural, parseT, clockET } from '../lib/format';
import { useParamSetter } from '../lib/router';
import { EntryDrawer, Dots } from '../components/EntryDrawer';
import { yearOf } from '../data/derive';
import './library.css';

const col = createColumnHelper<Entry>();

function norm(s: string) { return s.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, ''); }

export function Library({ data, params }: { data: Dataset; params?: URLSearchParams }) {
  const p = params ?? new URLSearchParams();
  const set = useParamSetter('/library');
  const [q, setQ] = useState(p.get('q') ?? '');
  const dq = useDeferredValue(q);
  const kind = p.get('kind');
  const topic = p.get('topic');
  const team = p.get('team');
  const depth = p.get('depth');
  const minRel = Number(p.get('rel') ?? 0);
  const view = (p.get('view') ?? 'table') as 'table' | 'cards';
  const open = p.get('e');
  const [sorting, setSorting] = useState<SortingState>([{ id: p.get('sort') ?? 'added_at', desc: p.get('dir') !== 'asc' }]);

  useEffect(() => { const id = setTimeout(() => set({ q: q || null }), 250); return () => clearTimeout(id); }, [q, set]);
  useEffect(() => { const s = sorting[0]; set({ sort: s && s.id !== 'added_at' ? s.id : null, dir: s && !s.desc ? 'asc' : null }); }, [sorting, set]);

  const index = useMemo(() => data.library.map((e) => ({ e, hay: norm(`${e.title} ${e.authors} ${e.id} ${e.summary} ${e.added_by}`) })), [data.library]);
  const byId = useMemo(() => new Map(data.library.map((e) => [e.id, e])), [data.library]);

  const base = useMemo(() => {
    const terms = norm(dq).split(/\s+/).filter(Boolean);
    return index.filter(({ e, hay }) => terms.every((t) => hay.includes(t))).map((x) => x.e);
  }, [index, dq]);

  const apply = (skip?: string) => base.filter((e) =>
    (skip === 'kind' || !kind || e.kind === kind) &&
    (skip === 'topic' || !topic || e.topics.includes(topic)) &&
    (skip === 'team' || !team || teamOf(e.added_by) === team) &&
    (skip === 'depth' || !depth || e.read_depth === depth) &&
    (skip === 'rel' || !minRel || (e.relevance ?? 0) >= minRel));
  const rows = useMemo(() => apply(), [base, kind, topic, team, depth, minRel]);
  const facet = (skip: string, key: (e: Entry) => string | string[] | null | undefined) => {
    const m = new Map<string, number>();
    for (const e of apply(skip)) { const k = key(e); for (const v of Array.isArray(k) ? k : [k]) if (v != null) m.set(String(v), (m.get(String(v)) ?? 0) + 1); }
    return m;
  };
  const fKind = useMemo(() => facet('kind', (e) => e.kind), [base, topic, team, depth, minRel]);
  const fTopic = useMemo(() => facet('topic', (e) => e.topics), [base, kind, team, depth, minRel]);
  const fTeam = useMemo(() => facet('team', (e) => teamOf(e.added_by)), [base, kind, topic, depth, minRel]);
  const fDepth = useMemo(() => facet('depth', (e) => e.read_depth), [base, kind, topic, team, minRel]);

  const columns = useMemo(() => [
    col.accessor('kind', {
      header: 'Kind', size: 92,
      cell: (c) => <span className="cell-kind"><i className="sw round" style={{ background: kindColor(c.getValue()) }} />{KIND_ONE[c.getValue() as Kind]}</span>,
    }),
    col.accessor('title', {
      header: 'Title', size: 520,
      cell: (c) => (
        <div className="cell-title">
          <span className="t">{c.getValue()}</span>
          <span className="a">{c.row.original.authors}{c.row.original.topics.length ? <> <span className="faint">·</span> {c.row.original.topics.map(topicName).join(', ')}</> : null}</span>
        </div>
      ),
    }),
    col.accessor((e) => yearOf(e) ?? 0, { id: 'year', header: 'Year', size: 64, cell: (c) => <span className="num">{c.getValue() || ''}</span> }),
    col.accessor((e) => e.relevance ?? 0, { id: 'relevance', header: 'Relevance', size: 96, cell: (c) => <Dots n={c.getValue()} /> }),
    col.accessor((e) => DEPTH_ORDER.indexOf(e.read_depth ?? ''), {
      id: 'depth', header: 'Read', size: 96,
      cell: (c) => <span className={`depth d-${c.row.original.read_depth}`}>{DEPTH_LABEL[c.row.original.read_depth ?? ''] ?? c.row.original.read_depth}</span>,
    }),
    col.accessor('added_by', {
      header: 'Added by', size: 170,
      cell: (c) => <span className="cell-agent"><i className="sw round" style={{ background: teamColor(teamOf(c.getValue())) }} /><span className="mono">{c.getValue()}</span></span>,
    }),
    col.accessor((e) => parseT(e.added_at) ?? 0, {
      id: 'added_at', header: 'Added', size: 78,
      cell: (c) => <span className="num muted">{c.getValue() ? clockET(c.getValue()) : ''}</span>,
    }),
  ], []);

  const table = useReactTable({
    data: rows, columns, state: { sorting }, onSortingChange: setSorting,
    getCoreRowModel: getCoreRowModel(), getSortedRowModel: getSortedRowModel(),
  });
  const sorted = table.getRowModel().rows;

  const active = [kind, topic, team, depth, minRel ? 'rel' : null, dq].filter(Boolean).length;
  const reset = () => { setQ(''); set({ kind: null, topic: null, team: null, depth: null, rel: null, q: null }); };
  const openEntry = byId.get(open ?? '') ?? null;
  const searchRef = useRef<HTMLInputElement>(null);
  const toolsRef = useRef<HTMLElement>(null);
  useEffect(() => {
    const el = toolsRef.current;
    if (!el) return;
    const ro = new ResizeObserver(() => {
      const sticky = getComputedStyle(el).position === 'sticky';
      document.documentElement.style.setProperty('--tools-h', sticky ? `${el.offsetHeight}px` : '0px');
    });
    ro.observe(el);
    return () => { ro.disconnect(); document.documentElement.style.removeProperty('--tools-h'); };
  }, []);
  useEffect(() => {
    const on = (ev: KeyboardEvent) => {
      if (ev.key === '/' && document.activeElement?.tagName !== 'INPUT') { ev.preventDefault(); searchRef.current?.focus(); }
    };
    window.addEventListener('keydown', on);
    return () => window.removeEventListener('keydown', on);
  }, []);

  const full = rows.filter((e) => e.read_depth === 'full' || e.read_depth === 'ran').length;

  return (
    <>
      <section className="wrap page-head lib-head">
        <p className="eyebrow"><span className="tick" />Library</p>
        <h1 className="display">Every source the agents have read, <em>searchable</em>.</h1>
        <p className="lede">
          {fmt(data.library.length)} catalogue entries across {Word(KINDS.length).toLowerCase()} kinds. Each has a summary, a relevance score from 1 to 5,
          how deeply it was read, and the agent that added it. Press <kbd>/</kbd> to search.
        </p>
      </section>

      <section ref={toolsRef} className="wrap lib-tools" aria-label="Search and filters">
        <div className="lib-search">
          <svg width="15" height="15" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="1.3" aria-hidden="true"><circle cx="7" cy="7" r="4.6" /><path d="M10.5 10.5 14 14" /></svg>
          <input ref={searchRef} className="input" type="search" value={q} onChange={(ev) => setQ(ev.target.value)}
            placeholder="Search titles, authors, summaries, agents" aria-label="Search the library" />
        </div>
        <div className="lib-filters">
          <div className="chips" role="group" aria-label="Kind">
            {KINDS.map((k) => (
              <button key={k} className="chip" aria-pressed={kind === k} onClick={() => set({ kind: kind === k ? null : k })}>
                <i className="sw round" style={{ background: kindColor(k) }} />{KIND_LABEL[k]} <span className="c">{fmt(fKind.get(k) ?? 0)}</span>
              </button>
            ))}
          </div>
          <div className="lib-selects">
            <Select label="Topic" value={topic} onChange={(v) => set({ topic: v })}
              options={[...fTopic.entries()].sort((a, b) => b[1] - a[1]).map(([k, n]) => ({ v: k, l: `${topicName(k)} (${fmt(n)})` }))} />
            <Select label="Team" value={team} onChange={(v) => set({ team: v })}
              options={[...TEAMS].map((t) => ({ v: t, l: `${t} (${fmt(fTeam.get(t) ?? 0)})` }))} />
            <Select label="Read depth" value={depth} onChange={(v) => set({ depth: v })}
              options={DEPTH_ORDER.map((d) => ({ v: d, l: `${DEPTH_LABEL[d]} (${fmt(fDepth.get(d) ?? 0)})` }))} />
            <Select label="Relevance" value={minRel ? String(minRel) : null} onChange={(v) => set({ rel: v })}
              options={[5, 4, 3, 2].map((r) => ({ v: String(r), l: r === 5 ? 'Only 5' : `${r} or more` }))} />
          </div>
        </div>
        <div className="lib-status">
          <p aria-live="polite">
            <b className="num">{fmt(rows.length)}</b> {plural(rows.length, 'source')}{active ? ' match' : ''}, {fmt(full)} read in full.
            {active > 0 && <> <button className="btn-text" onClick={reset}>Clear filters</button></>}
          </p>
          <div className="seg" role="group" aria-label="Layout">
            <button aria-pressed={view === 'table'} onClick={() => set({ view: null })}>Table</button>
            <button aria-pressed={view === 'cards'} onClick={() => set({ view: 'cards' })}>Cards</button>
          </div>
        </div>
      </section>

      <section className="wrap">
        {rows.length === 0 ? (
          <div className="lib-empty">
            <p className="h2">Nothing matches.</p>
            <p className="reading">Try a broader term or <button className="btn-text" onClick={reset}>clear the filters</button>. If a source is missing, drop its link in <span className="mono">lab/researchers/&lt;you&gt;/inbox.md</span> and an agent will catalogue it.</p>
          </div>
        ) : view === 'table' ? (
          <VirtualTable table={table} rows={sorted} onOpen={(id) => set({ e: id })} />
        ) : (
          <VirtualCards rows={sorted.map((r) => r.original)} onOpen={(id) => set({ e: id })} />
        )}
      </section>

      <EntryDrawer entry={openEntry} byId={byId} onClose={() => set({ e: null })} onOpen={(id) => set({ e: id })} />
    </>
  );
}

function Select({ label, value, onChange, options }: { label: string; value: string | null; onChange: (v: string | null) => void; options: { v: string; l: string }[] }) {
  return (
    <label className="sel">
      <span className="sr-only">{label}</span>
      <select className="select" value={value ?? ''} onChange={(e) => onChange(e.target.value || null)} data-set={value ? 'y' : undefined}>
        <option value="">{label}: all</option>
        {options.map((o) => <option key={o.v} value={o.v}>{o.l}</option>)}
      </select>
    </label>
  );
}

type T = ReturnType<typeof useReactTable<Entry>>;
function VirtualTable({ table, rows, onOpen }: { table: T; rows: ReturnType<T['getRowModel']>['rows']; onOpen: (id: string) => void }) {
  const listRef = useRef<HTMLDivElement>(null);
  const [offset, setOffset] = useState(0);
  useEffect(() => { setOffset(listRef.current?.offsetTop ?? 0); }, []);
  const v = useWindowVirtualizer({ count: rows.length, estimateSize: () => 54, overscan: 12, scrollMargin: offset });
  const grid = table.getVisibleLeafColumns().map((c) => (c.id === 'title' ? 'minmax(0, 1fr)' : `${c.getSize()}px`)).join(' ');
  return (
    <div className="ltable" role="table" aria-rowcount={rows.length} style={{ ['--grid' as string]: grid }}>
      <div className="lrow lhead" role="row">
        {table.getHeaderGroups()[0].headers.map((h) => {
          const s = h.column.getIsSorted();
          return (
            <div key={h.id} role="columnheader" className={`lcell c-${h.id}`} aria-sort={s === 'asc' ? 'ascending' : s === 'desc' ? 'descending' : 'none'}>
              <button onClick={h.column.getToggleSortingHandler()}>
                {flexRender(h.column.columnDef.header, h.getContext())}
                <span className="sort" aria-hidden="true">{s === 'asc' ? '↑' : s === 'desc' ? '↓' : ''}</span>
              </button>
            </div>
          );
        })}
      </div>
      <div ref={listRef} role="rowgroup" style={{ height: v.getTotalSize(), position: 'relative' }}>
        {v.getVirtualItems().map((vi) => {
          const r = rows[vi.index];
          return (
            <div key={r.id} role="row" tabIndex={0} className="lrow lbody" data-index={vi.index} ref={v.measureElement}
              style={{ position: 'absolute', top: 0, left: 0, right: 0, transform: `translateY(${vi.start - v.options.scrollMargin}px)` }}
              onClick={() => onOpen(r.original.id)} onKeyDown={(e) => { if (e.key === 'Enter' || e.key === ' ') { e.preventDefault(); onOpen(r.original.id); } }}>
              {r.getVisibleCells().map((c) => (
                <div key={c.id} role="cell" className={`lcell c-${c.column.id}`}>{flexRender(c.column.columnDef.cell, c.getContext())}</div>
              ))}
            </div>
          );
        })}
      </div>
    </div>
  );
}

function VirtualCards({ rows, onOpen }: { rows: Entry[]; onOpen: (id: string) => void }) {
  const wrapRef = useRef<HTMLDivElement>(null);
  const [cols, setCols] = useState(3);
  const [offset, setOffset] = useState(0);
  useEffect(() => {
    const el = wrapRef.current;
    if (!el) return;
    setOffset(el.offsetTop);
    const ro = new ResizeObserver(([e]) => setCols(e.contentRect.width < 620 ? 1 : e.contentRect.width < 980 ? 2 : 3));
    ro.observe(el);
    return () => ro.disconnect();
  }, []);
  const lines = Math.ceil(rows.length / cols);
  const v = useWindowVirtualizer({ count: lines, estimateSize: () => 210, overscan: 4, scrollMargin: offset });
  return (
    <div ref={wrapRef} style={{ height: v.getTotalSize(), position: 'relative' }}>
      {v.getVirtualItems().map((vi) => (
        <div key={vi.key} data-index={vi.index} ref={v.measureElement} className="lcards"
          style={{ position: 'absolute', top: 0, left: 0, right: 0, transform: `translateY(${vi.start - v.options.scrollMargin}px)`, gridTemplateColumns: `repeat(${cols}, minmax(0, 1fr))` }}>
          {rows.slice(vi.index * cols, vi.index * cols + cols).map((e) => (
            <button key={e.id} className="lcard" onClick={() => onOpen(e.id)}>
              <span className="lcard-top">
                <span className="cell-kind"><i className="sw round" style={{ background: kindColor(e.kind) }} />{KIND_ONE[e.kind]}{yearOf(e) ? `, ${yearOf(e)}` : ''}</span>
                <Dots n={e.relevance ?? 0} />
              </span>
              <span className="lcard-title">{e.title}</span>
              <span className="lcard-sum">{e.summary}</span>
              <span className="lcard-foot">
                <span className="cell-agent"><i className="sw round" style={{ background: teamColor(teamOf(e.added_by)) }} /><span className="mono">{e.added_by}</span></span>
                <span className={`depth d-${e.read_depth}`}>{DEPTH_LABEL[e.read_depth ?? ''] ?? e.read_depth}</span>
              </span>
            </button>
          ))}
        </div>
      ))}
    </div>
  );
}
