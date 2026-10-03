export type Kind = 'paper' | 'blog' | 'thread' | 'code' | 'dataset' | 'talk';
export type KindPlural = 'papers' | 'blogs' | 'threads' | 'code' | 'datasets' | 'talks';
export type Counts = Record<KindPlural, number> & { total: number };

export interface Summary {
  generated_at: string;
  head_sha: string;
  counts: Counts;
  topics: { slug: string; name: string; counts: Counts; total: number }[];
  surveys: { n: number; passing: number };
  hypotheses: number;
  experiments: number;
  tasks: { open: number; claimed: number; done: number; blocked?: number };
  agents: { active: number; total: number };
}

export interface Entry {
  id: string;
  kind: Kind;
  title: string;
  url: string;
  topics: string[];
  year: number | string | null;
  date?: string | null;
  authors: string;
  relevance: number | null;
  read_depth: 'skim' | 'abstract' | 'full' | 'ran' | string | null;
  added_by: string;
  added_at: string | null;
  summary: string;
  links: string[];
}

export interface TimelineRow { t: string; team: string; agent: string; kind: Kind; n_entries: number }

export interface Agent {
  id: string;
  team: string;
  model: string | null;
  state: string;
  task: string | null;
  doing: string;
  updated: string | null;
  entries_added: number;
  last_commit_at: string | null;
}

export interface Task {
  id: string;
  title: string;
  kind: 'scan' | 'survey' | 'review' | 'synthesis' | 'admin' | 'hypothesis' | 'experiment' | string;
  status: 'open' | 'claimed' | 'done' | 'blocked' | string;
  priority: string | null;
  owner: string | null;
  for: string | null;
  topics: string[] | null;
  depends_on: string[] | null;
  updated?: string | null;
  claimed_at?: string | null;
}

export interface Batch {
  id: string;
  source: string;
  topic: string | null;
  n_candidates: number;
  state: 'free' | 'claimed' | 'closed' | 'unknown' | string;
  assignees: string[];
  updated: string | null;
  number?: number;
  url?: string;
  title?: string;
}

export interface Survey {
  id: string;
  topic: string;
  status: string;
  gate: { passes: boolean; missing: string[] };
  sources: number;
  reviewed_by: (string | null)[];
}

export interface Doc { id: string; topics?: string[]; status?: string; owner?: string; [k: string]: unknown }

export interface Dataset {
  summary: Summary;
  library: Entry[];
  timeline: TimelineRow[];
  agents: Agent[];
  tasks: Task[];
  batches: Batch[];
  surveys: Survey[];
  hypotheses: Doc[];
  experiments: Doc[];
}
