export interface LibraryEntry {
  id: string;
  kind: string;
  title: string;
  url?: string;
  topics: string[];
  authors?: string;
  added_by?: string;
  added_at?: string;
  summary?: string;
  links?: string[];
  read_depth?: string;
  relevance?: number;
}
export interface GraphData {
  nodes: { id: string; kind: string; topic: string }[];
  edges: { s: string; t: string }[];
}
export interface TimelineEntry {
  t: string;
  team: string;
  agent: string;
  kind: string;
  n_entries: number;
}
export interface SwarmData {
  graph: GraphData;
  library: LibraryEntry[];
  timeline?: TimelineEntry[];
}
export const START = Date.parse("2026-10-03T12:00:00-04:00");
export const label = (s: string) => s.replaceAll("-", " ");
export const timeLabel = (t: number) =>
  new Intl.DateTimeFormat("en-US", {
    timeZone: "America/New_York",
    hour: "numeric",
    minute: "2-digit",
  }).format(t);
export function hash(s: string) {
  let h = 2166136261;
  for (let i = 0; i < s.length; i++)
    h = Math.imul(h ^ s.charCodeAt(i), 16777619);
  return (h >>> 0) / 4294967296;
}
export const kinds = ["paper", "blog", "thread", "code", "dataset", "talk"];
export const teams = ["dmarz", "vishesh", "shadow", "unknown"];
export const colors: Record<string, string> = {
  paper: "#526b87",
  blog: "#b68a37",
  thread: "#c76048",
  code: "#448d80",
  dataset: "#749547",
  talk: "#a27096",
  dmarz: "#b58a3b",
  vishesh: "#6185aa",
  shadow: "#61906b",
  unknown: "#929087",
};
export interface Particle {
  id: string;
  kind: string;
  topic: number;
  team: string;
  birth: number;
  x: number;
  y: number;
  vx: number;
  vy: number;
  ox: number;
  oy: number;
  phase: number;
}
export interface Cluster {
  name: string;
  x: number;
  y: number;
  count: number;
  radius: number;
}
export function createWorld(data: SwarmData) {
  const entries = new Map(data.library.map((e) => [e.id, e]));
  const counts = new Map<string, number>();
  data.graph.nodes.forEach((n) =>
    counts.set(n.topic, (counts.get(n.topic) || 0) + 1),
  );
  const sorted = [...counts].sort((a, b) => b[1] - a[1]);
  const clusters: Cluster[] = sorted.map(([name, count], i) => {
    const angle = i * 2.399963;
    const r =
      i === 0 ? 0 : 0.12 + Math.sqrt(i / Math.max(1, sorted.length - 1)) * 0.26;
    return {
      name,
      count,
      x: 0.5 + Math.cos(angle) * r,
      y: 0.48 + Math.sin(angle) * r,
      radius: 0.027 + Math.sqrt(count / data.graph.nodes.length) * 0.12,
    };
  });
  const particles: Particle[] = data.graph.nodes.map((n) => {
    const e = entries.get(n.id);
    const topic = clusters.findIndex((c) => c.name === n.topic);
    const c = clusters[topic];
    const phase = hash(n.id) * Math.PI * 2;
    const r = Math.sqrt(hash(n.id + "r")) * c.radius;
    const ox = Math.cos(phase) * r,
      oy = Math.sin(phase) * r;
    return {
      id: n.id,
      kind: n.kind,
      topic,
      team: e?.added_by?.split("/")[0] || "unknown",
      birth: Date.parse(e?.added_at || "") || START,
      x: c.x + ox,
      y: c.y + oy,
      vx: 0,
      vy: 0,
      ox,
      oy,
      phase,
    };
  });
  const index = new Map(particles.map((p, i) => [p.id, i]));
  const edges = data.graph.edges.flatMap((e) =>
    index.has(e.s) && index.has(e.t)
      ? [[index.get(e.s)!, index.get(e.t)!]]
      : [],
  );
  // Only explicit wikilinks exert force. Shared-topic edges describe coverage, not citations.
  const links = data.library.flatMap((e) =>
    (e.links || []).flatMap((t) =>
      index.has(e.id) && index.has(t)
        ? [[index.get(e.id)!, index.get(t)!]]
        : [],
    ),
  );
  return { particles, clusters, edges, links, entries };
}
export type World = ReturnType<typeof createWorld>;
/** O(nodes + links). Topic mean velocity supplies alignment without an all-pairs pass. */
export function stepWorld(w: World, dt: number, time: number) {
  const means = w.clusters.map(() => ({ vx: 0, vy: 0, n: 0 }));
  for (const p of w.particles) {
    const m = means[p.topic];
    m.vx += p.vx;
    m.vy += p.vy;
    m.n++;
  }
  for (const p of w.particles) {
    const c = w.clusters[p.topic],
      m = means[p.topic];
    const a = time * 0.075;
    const tx = c.x + p.ox * Math.cos(a) - p.oy * Math.sin(a),
      ty = c.y + p.ox * Math.sin(a) + p.oy * Math.cos(a);
    p.vx += (tx - p.x) * 0.3 * dt + (m.vx / m.n - p.vx) * 0.35 * dt;
    p.vy += (ty - p.y) * 0.3 * dt + (m.vy / m.n - p.vy) * 0.35 * dt;
  }
  for (const [a, b] of w.links) {
    const p = w.particles[a],
      q = w.particles[b];
    const dx = (q.x - p.x) * 0.0004 * dt,
      dy = (q.y - p.y) * 0.0004 * dt;
    p.vx += dx;
    p.vy += dy;
    q.vx -= dx;
    q.vy -= dy;
  }
  for (const p of w.particles) {
    p.vx *= Math.pow(0.65, dt);
    p.vy *= Math.pow(0.65, dt);
    p.x += p.vx * dt;
    p.y += p.vy * dt;
  }
}
