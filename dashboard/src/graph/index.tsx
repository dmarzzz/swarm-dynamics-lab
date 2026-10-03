import { useEffect, useMemo, useRef, useState } from "react";
import {
  colors,
  createWorld,
  kinds,
  label,
  START,
  stepWorld,
  syncPalette,
  teams,
  timeLabel,
} from "./model";
import type { LibraryEntry, SwarmData } from "./model";
import { renderer } from "./renderer";
import type { Vertex } from "./renderer";
import "./swarm.css";
export type {
  SwarmData,
  GraphData,
  LibraryEntry,
  TimelineEntry,
} from "./model";
export interface SwarmProps {
  data?: SwarmData;
  dataUrl?: string;
  className?: string;
  onSelect?: (entry: LibraryEntry) => void;
}
const KIND_NAMES: Record<string, string> = { paper: "Papers", blog: "Blogs", thread: "Threads", code: "Code", dataset: "Datasets", talk: "Talks" };
let cached: Promise<SwarmData> | undefined;
function load(url: string) {
  return Promise.all(
    ["graph", "library", "timeline"].map(async (name) => {
      const r = await fetch(`${url}/${name}.json`);
      if (!r.ok) throw Error(`Cannot load ${name}`);
      return r.json();
    }),
  ).then(([graph, library, timeline]) => ({ graph, library, timeline }));
}
function useData(props: SwarmProps) {
  const [state, set] = useState<{ data?: SwarmData; error?: string }>({
    data: props.data,
  });
  useEffect(() => {
    if (props.data) {
      set({ data: props.data });
      return;
    }
    let alive = true;
    const promise = props.dataUrl
      ? load(props.dataUrl)
      : (cached ??= load(`${import.meta.env.BASE_URL}data`).catch((e) => {
          cached = undefined;
          throw e;
        }));
    promise
      .then((data) => alive && set({ data }))
      .catch((e) => alive && set({ error: e.message }));
    return () => {
      alive = false;
    };
  }, [props.data, props.dataUrl]);
  return state;
}
function Field({
  data,
  query = "",
  topic = "",
  colorBy = "kind",
  until = Infinity,
  paused = false,
  hero = false,
  onSelect,
  onStats,
}: {
  data: SwarmData;
  query?: string;
  topic?: string;
  colorBy?: string;
  until?: number;
  paused?: boolean;
  hero?: boolean;
  onSelect?: (e: LibraryEntry) => void;
  onStats?: (s: string) => void;
}) {
  const world = useMemo(() => createWorld(data), [data]);
  const host = useRef<HTMLDivElement>(null),
    canvas = useRef<HTMLCanvasElement>(null);
  const [hover, setHover] = useState<LibraryEntry>();
  const [hoverCluster, setHoverCluster] = useState<string>();
  const [view, setView] = useState({ zoom: 1, x: 0, y: 0 });
  const [reduced, setReduced] = useState(false);
  const [dimensions, setDimensions] = useState({ width: 800, height: 500 });
  const live = useRef({
    query,
    topic,
    colorBy,
    until,
    paused,
    view,
    reduced,
    onSelect,
    onStats,
  });
  live.current = {
    query,
    topic,
    colorBy,
    until,
    paused,
    view,
    reduced,
    onSelect,
    onStats,
  };
  const [, setPaletteRev] = useState(0);
  useEffect(() => {
    syncPalette();
    setPaletteRev((n) => n + 1);
    const mo = new MutationObserver(() => { syncPalette(); setPaletteRev((n) => n + 1); });
    mo.observe(document.documentElement, { attributes: true, attributeFilter: ["data-theme"] });
    return () => mo.disconnect();
  }, []);
  const hit = useRef<{ p: Vertex; id: string }[]>([]);
  const pointer = useRef({ x: 0, y: 0, drag: false, moved: false });
  useEffect(() => {
    const m = matchMedia("(prefers-reduced-motion: reduce)");
    setReduced(m.matches);
    const f = () => setReduced(m.matches);
    m.addEventListener("change", f);
    return () => m.removeEventListener("change", f);
  }, []);
  useEffect(() => {
    if (!canvas.current || !host.current) return;
    const engine = renderer(canvas.current);
    let frame = 0,
      last = 0,
      elapsed = 0,
      frames = 0,
      total = 0,
      lastStats = 0;
    let width = 800,
      height = 500,
      visible = true;
    const resize = new ResizeObserver(([entry]) => {
      width = entry.contentRect.width;
      height = entry.contentRect.height;
      setDimensions({ width, height });
    });
    resize.observe(host.current);
    const io = new IntersectionObserver(([e]) => {
      visible = e.isIntersecting;
    });
    io.observe(host.current);
    const draw = (now: number) => {
      frame = requestAnimationFrame(draw);
      if (!visible || document.hidden) return;
      const s = live.current;
      const dt = Math.min((now - last) / 1000 || 0.016, 0.04);
      last = now;
      const start = performance.now();
      if (!s.paused && !s.reduced) {
        elapsed += dt;
        stepWorld(world, dt, elapsed);
      }
      const scaleX = Math.min(width * 0.9, height * 1.65) * s.view.zoom,
        scaleY = Math.min(width * 0.94, height * 1.08) * s.view.zoom;
      const project = (x: number, y: number) => ({
        x: (x - 0.5) * scaleX + width / 2 + s.view.x,
        y: (y - 0.5) * scaleY + height / 2 + s.view.y,
      });
      const q = s.query.toLowerCase().trim();
      const selected = world.particles.map(
        (p) =>
          !q ||
          `${world.entries.get(p.id)?.title} ${p.id} ${label(world.clusters[p.topic].name)}`
            .toLowerCase()
            .includes(q),
      );
      const points: Vertex[] = [],
        byIndex: (Vertex | undefined)[] = [];
      hit.current = [];
      for (let i = 0; i < world.particles.length; i++) {
        const p = world.particles[i];
        if (p.birth > s.until) {
          byIndex.push(undefined);
          continue;
        }
        const matches =
          selected[i] && (!s.topic || world.clusters[p.topic].name === s.topic);
        const v = {
          ...project(p.x, p.y),
          color:
            colors[s.colorBy === "team" ? p.team : p.kind] || colors.unknown,
          alpha: matches ? 0.88 : 0.09,
          size: matches ? (q ? 5 : 3.5) : 2,
        };
        points.push(v);
        byIndex.push(v);
        if (matches) hit.current.push({ p: v, id: p.id });
      }
      const lines: Vertex[] = [];
      const edges = hero ? world.links : world.edges;
      const stride = hero ? 3 : Math.max(1, Math.ceil(edges.length / 1600));
      for (let i = 0; i < edges.length; i += stride) {
        const [a, b] = edges[i],
          p = byIndex[a],
          q = byIndex[b];
        if (!p || !q || p.alpha < 0.2 || q.alpha < 0.2) continue;
        lines.push({ ...p, alpha: 0.055 }, { ...q, alpha: 0.055 });
      }
      engine.draw(points, lines, width, height, Math.min(devicePixelRatio, 2));
      frames++;
      total += performance.now() - start;
      if (now - lastStats > 1500) {
        const fps = (frames * 1000) / (now - lastStats);
        s.onStats?.(`${engine.mode}, ${Math.round(fps)} fps`);
        canvas.current!.dataset.perf = JSON.stringify({
          renderer: engine.mode,
          fps: +fps.toFixed(1),
          cpuMs: +(total / frames).toFixed(2),
          nodes: points.length,
        });
        frames = 0;
        total = 0;
        lastStats = now;
      }
    };
    frame = requestAnimationFrame(draw);
    return () => {
      cancelAnimationFrame(frame);
      resize.disconnect();
      io.disconnect();
      engine.dispose();
    };
  }, [world, hero]);
  const inspect = (x: number, y: number) => {
    let nearest: string | undefined,
      best = 144;
    for (const h of hit.current) {
      const d = (h.p.x - x) ** 2 + (h.p.y - y) ** 2;
      if (d < best) {
        best = d;
        nearest = h.id;
      }
    }
    return nearest ? world.entries.get(nearest) : undefined;
  };
  return (
    <div
      className={`swarm-field ${hero ? "swarm-field--hero" : ""}`}
      ref={host}
    >
      <canvas
        ref={canvas}
        aria-label={`${world.particles.length} library sources grouped by research topic. Use the search and source list to explore with a keyboard.`}
        onPointerDown={(e) => {
          pointer.current = {
            x: e.clientX,
            y: e.clientY,
            drag: true,
            moved: false,
          };
          e.currentTarget.setPointerCapture(e.pointerId);
        }}
        onPointerMove={(e) => {
          const r = e.currentTarget.getBoundingClientRect();
          if (pointer.current.drag && !hero) {
            const dx = e.clientX - pointer.current.x,
              dy = e.clientY - pointer.current.y;
            if (Math.abs(dx) + Math.abs(dy) > 2) pointer.current.moved = true;
            setView((v) => ({ ...v, x: v.x + dx, y: v.y + dy }));
            pointer.current.x = e.clientX;
            pointer.current.y = e.clientY;
          } else {
            const px = e.clientX - r.left, py = e.clientY - r.top;
            setHover(inspect(px, py));
            const sx = Math.min(dimensions.width * 0.9, dimensions.height * 1.65), sy = Math.min(dimensions.width * 0.94, dimensions.height * 1.08);
            const near = world.clusters.find((c) => {
              const cx = dimensions.width / 2 + (c.x - 0.5) * sx, cy = dimensions.height / 2 + (c.y - 0.5) * sy;
              return Math.hypot(px - cx, py - cy) < c.radius * sy + 14;
            });
            setHoverCluster(near?.name);
          }
        }}
        onPointerUp={(e) => {
          if (!pointer.current.moved) {
            const r = e.currentTarget.getBoundingClientRect();
            const entry = inspect(e.clientX - r.left, e.clientY - r.top);
            if (entry) onSelect?.(entry);
          }
          pointer.current.drag = false;
        }}
        onPointerCancel={() => {
          pointer.current.drag = false;
        }}
        onPointerLeave={() => { setHover(undefined); setHoverCluster(undefined); }}
      />
      <div className="swarm-labels" aria-hidden="true">
        {view.zoom === 1 && !view.x && !view.y &&
          layoutLabels(world.clusters, dimensions, hoverCluster, topic).map((l) => (
            <span
              key={l.name}
              className={l.hidden ? "is-hidden" : undefined}
              style={{ left: l.x, top: l.y, opacity: topic && topic !== l.name ? 0.25 : undefined }}
            >
              {label(l.name)} <small>{l.count.toLocaleString()}</small>
            </span>
          ))}
      </div>
      {!hero && (
        <div className="swarm-camera">
          <button
            aria-label="Zoom in"
            onClick={() =>
              setView((v) => ({ ...v, zoom: Math.min(3, v.zoom * 1.25) }))
            }
          >
            +
          </button>
          <button
            aria-label="Zoom out"
            onClick={() =>
              setView((v) => ({ ...v, zoom: Math.max(0.6, v.zoom / 1.25) }))
            }
          >
            −
          </button>
          <button onClick={() => setView({ zoom: 1, x: 0, y: 0 })}>Fit</button>
        </div>
      )}
      {hover && (
        <div className="swarm-tooltip" role="status">
          <small>
            {KIND_NAMES[hover.kind] ?? label(hover.kind)}, <span className="swarm-mono">{hover.added_by}</span>
          </small>
          <strong>{hover.title}</strong>
          <span>Click to inspect source</span>
        </div>
      )}
      {reduced && <span className="swarm-motion-note">Motion reduced</span>}
    </div>
  );
}
/** Greedy label placement: biggest clusters first, above then below, hidden on collision and revealed on hover or topic focus. */
function layoutLabels(
  clusters: { name: string; x: number; y: number; radius: number; count: number }[],
  dim: { width: number; height: number },
  hovered?: string,
  focus?: string,
) {
  const sx = Math.min(dim.width * 0.9, dim.height * 1.65), sy = Math.min(dim.width * 0.94, dim.height * 1.08);
  const placed: { x0: number; x1: number; y0: number; y1: number }[] = [];
  const out: { name: string; count: number; x: number; y: number; hidden: boolean }[] = [];
  const pri = (n: string) => (n === hovered || n === focus ? 1 : 0);
  const order = [...clusters].sort((a, b) => pri(b.name) - pri(a.name) || b.count - a.count);
  for (const c of order) {
    const w = (label(c.name).length + String(c.count).length + 1) * 6.3 + 10, h = 16;
    const cx = dim.width / 2 + (c.x - 0.5) * sx, cy = dim.height / 2 + (c.y - 0.5) * sy, r = c.radius * sy;
    let spot: { x: number; y: number } | null = null;
    for (const y of [cy - r - 11, cy + r + 11]) {
      const box = { x0: cx - w / 2, x1: cx + w / 2, y0: y - h / 2, y1: y + h / 2 };
      const inside = box.x0 > 2 && box.x1 < dim.width - 2 && box.y0 > 2 && box.y1 < dim.height - 2;
      if (inside && !placed.some((p) => box.x0 < p.x1 && box.x1 > p.x0 && box.y0 < p.y1 && box.y1 > p.y0)) {
        placed.push(box);
        spot = { x: cx, y };
        break;
      }
    }
    out.push({ name: c.name, count: c.count, x: spot?.x ?? cx, y: spot?.y ?? cy - r - 11, hidden: !spot });
  }
  return out;
}
export function HeroSwarm(props: SwarmProps) {
  const { data, error } = useData(props);
  return (
    <div className={`swarm-root swarm-hero ${props.className || ""}`}>
      {data ? (
        <>
          <Field data={data} hero onSelect={props.onSelect} />
          <p className="swarm-caption">
            One dot, one source.{" "}
            <strong>{data.graph.nodes.length.toLocaleString()}</strong> entries
            finding their place across research topics.
          </p>
        </>
      ) : (
        <p role="status">
          {error
            ? "The source map is unavailable."
            : "Gathering the research swarm…"}
        </p>
      )}
    </div>
  );
}
export function GraphView(props: SwarmProps) {
  const { data, error } = useData(props);
  const [query, setQuery] = useState(""),
    [topic, setTopic] = useState(""),
    [colorBy, setColor] = useState("kind"),
    [progress, setProgress] = useState(100),
    [paused, setPaused] = useState(false),
    [playing, setPlaying] = useState(false),
    [selected, setSelected] = useState<LibraryEntry>(),
    [stats, setStats] = useState("");
  const end = useMemo(
    () =>
      Math.max(
        START + 1,
        ...(data?.library || []).map(
          (e) => Date.parse(e.added_at || "") || START,
        ),
      ),
    [data],
  );
  const until =
    progress === 100 ? Infinity : START + ((end - START) * progress) / 100;
  useEffect(() => {
    if (!playing) return;
    const timer = setInterval(
      () =>
        setProgress((p) => {
          if (p >= 100) {
            setPlaying(false);
            return 100;
          }
          return Math.min(100, p + 0.4);
        }),
      100,
    );
    return () => clearInterval(timer);
  }, [playing]);
  const entries = useMemo(
    () =>
      (data?.library || []).filter(
        (e) =>
          (!topic || e.topics.includes(topic)) &&
          `${e.title} ${e.id} ${e.topics.join(" ")}`
            .toLowerCase()
            .includes(query.toLowerCase()) &&
          (Date.parse(e.added_at || "") || START) <= until,
      ),
    [data, topic, query, until],
  );
  if (!data)
    return (
      <section className="swarm-root swarm-loading" role="status">
        <h2>
          {error ? "The map could not load" : "Gathering the research swarm"}
        </h2>
        <p>
          {error || "Reading sources, connections and first-add timestamps."}
        </p>
        {error && <button onClick={() => location.reload()}>Try again</button>}
      </section>
    );
  const choose = (e: LibraryEntry) => {
    setSelected(e);
    props.onSelect?.(e);
  };
  return (
    <section className={`swarm-root swarm-graph ${props.className || ""}`}>
      <header className="swarm-heading">
        <div>
          <p className="swarm-eyebrow">The living library</p>
          <h2>Ideas do not travel alone.</h2>
          <p>
            Every dot is a source. Topics hold them together; links pull ideas
            across the field.
          </p>
        </div>
        <div className="swarm-reading">
          <strong>{entries.length.toLocaleString()}</strong>
          <span>sources in view</span>
        </div>
      </header>
      <div className="swarm-toolbar">
        <label className="swarm-search">
          <span>Find a source</span>
          <input
            type="search"
            placeholder="Search titles, topics or IDs"
            value={query}
            onChange={(e) => setQuery(e.target.value)}
          />
        </label>
        <label>
          <span>Topic</span>
          <select value={topic} onChange={(e) => setTopic(e.target.value)}>
            <option value="">All topics</option>
            {[...new Set(data.graph.nodes.map((n) => n.topic))]
              .sort()
              .map((t) => (
                <option key={t} value={t}>
                  {label(t)}
                </option>
              ))}
          </select>
        </label>
        <label>
          <span>Colour by</span>
          <select value={colorBy} onChange={(e) => setColor(e.target.value)}>
            <option value="kind">Source kind</option>
            <option value="team">Research team</option>
          </select>
        </label>
        <button aria-pressed={paused} onClick={() => setPaused(!paused)}>
          {paused ? "Resume motion" : "Pause motion"}
        </button>
      </div>
      <div className="swarm-legend">
        {(colorBy === "kind" ? kinds : teams).map((k) => (
          <span key={k}>
            <i style={{ background: colorBy === "kind" ? `var(--k-${k})` : `var(--team-${k})` }} />
            {colorBy === "kind" ? KIND_NAMES[k] ?? label(k) : label(k)}
          </span>
        ))}
        <span className="swarm-renderer">{stats}</span>
      </div>
      <div
        className={`swarm-stage ${selected ? "swarm-stage--inspecting" : ""}`}
      >
        <Field
          data={data}
          query={query}
          topic={topic}
          colorBy={colorBy}
          until={until}
          paused={paused}
          onSelect={choose}
          onStats={setStats}
        />
        {selected && (
          <aside className="swarm-inspector" aria-label="Selected source">
            <button
              className="swarm-close"
              onClick={() => setSelected(undefined)}
              aria-label="Close source details"
            >
              ×
            </button>
            <p className="swarm-eyebrow">
              {KIND_NAMES[selected.kind] ?? label(selected.kind)}, {selected.read_depth === "full" ? "read in full" : selected.read_depth || "depth not recorded"}
            </p>
            <h3>{selected.title}</h3>
            <p>{selected.authors}</p>
            <div className="swarm-tags">
              {selected.topics.map((t) => (
                <button key={t} onClick={() => setTopic(t)}>
                  {label(t)}
                </button>
              ))}
            </div>
            <p>{selected.summary || "No summary recorded for this source."}</p>
            <dl>
              <dt>Added by</dt>
              <dd className="swarm-mono">{selected.added_by || "Unknown"}</dd>
              <dt>First recorded</dt>
              <dd>
                {selected.added_at
                  ? timeLabel(Date.parse(selected.added_at)) + " ET"
                  : "Unknown"}
              </dd>
              <dt>Explicit links</dt>
              <dd>{selected.links?.length || 0}</dd>
            </dl>
            {selected.url && /^https?:\/\//.test(selected.url) && (
              <a href={selected.url} target="_blank" rel="noreferrer">
                Read original source ↗
              </a>
            )}
          </aside>
        )}
      </div>
      <div className="swarm-replay">
        <button
          onClick={() => {
            if (progress === 100) setProgress(0);
            setPlaying(!playing);
          }}
        >
          {playing ? "Pause replay" : "Replay growth"}
        </button>
        <label>
          <span>Noon ET</span>
          <input
            aria-label="Library growth replay"
            className="swarm-range"
            style={{ ["--p" as string]: `${progress}%` }}
            type="range"
            min="0"
            max="100"
            step="0.1"
            value={progress}
            onChange={(e) => {
              setPlaying(false);
              setProgress(Number(e.target.value));
            }}
          />
          <span>
            {progress === 100 ? "Latest snapshot" : `${timeLabel(until)} ET`}
          </span>
        </label>
      </div>
      <p className="swarm-caption">
        Drag to pan. Select a dot to inspect. Lines show a sparse sample of
        wikilinks and shared topics. Movement illustrates topic cohesion, not a
        measured similarity score. Replay includes only sources still in the
        library.
      </p>
      <details className="swarm-sources" open={Boolean(query)}>
        <summary>
          {entries.length
            ? `Browse ${entries.length.toLocaleString()} matching sources`
            : "No matching sources. Try another title or reset your filters."}
        </summary>
        <div>
          {entries.slice(0, 60).map((e) => (
            <button key={e.id} onClick={() => choose(e)}>
              <span className="swarm-src-title">
                <i style={{ background: `var(--k-${e.kind})` }} />
                {e.title}
              </span>
              <small>
                {KIND_NAMES[e.kind] ?? label(e.kind)}, added by <span className="swarm-mono">{e.added_by}</span>
              </small>
            </button>
          ))}
        </div>
        {entries.length > 60 && (
          <p>
            Showing the first 60. Search or choose a topic to narrow the list.
          </p>
        )}
      </details>
    </section>
  );
}
