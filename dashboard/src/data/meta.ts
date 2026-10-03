import type { Kind } from './types';

/** Hackathon start: 12:00 ET, 3 Oct 2026. */
export const HACK_START = Date.parse('2026-10-03T16:00:00Z');

export const KINDS: Kind[] = ['paper', 'thread', 'blog', 'code', 'talk', 'dataset'];
export const KIND_LABEL: Record<Kind, string> = {
  paper: 'Papers', thread: 'Threads', blog: 'Blogs', code: 'Code', talk: 'Talks', dataset: 'Datasets',
};
export const KIND_ONE: Record<Kind, string> = {
  paper: 'paper', thread: 'thread', blog: 'blog post', code: 'repository', talk: 'talk', dataset: 'dataset',
};
export const kindColor = (k: string) => `var(--k-${k in KIND_LABEL ? k : 'paper'})`;
export const PLURAL: Record<Kind, 'papers' | 'blogs' | 'threads' | 'code' | 'datasets' | 'talks'> = {
  paper: 'papers', blog: 'blogs', thread: 'threads', code: 'code', dataset: 'datasets', talk: 'talks',
};

export const TEAMS = ['dmarz', 'vishesh', 'shadow'] as const;
export const teamColor = (t: string) => ((TEAMS as readonly string[]).includes(t) ? `var(--team-${t})` : 'var(--team-unknown)');
export const teamOf = (agent: string | null | undefined) => (agent || 'unknown').split('/')[0];

export const DEPTH_ORDER = ['skim', 'abstract', 'full', 'ran'];
export const DEPTH_LABEL: Record<string, string> = {
  skim: 'Skimmed', abstract: 'Abstract', full: 'Read in full', ran: 'Code run',
};

export const TOPIC_SHORT: Record<string, string> = {
  'collective-motion': 'Collective motion',
  'collective-decision': 'Collective decisions',
  'swarm-robotics': 'Swarm robotics',
  'swarm-intelligence': 'Swarm intelligence',
  'active-matter': 'Active matter',
  'sync-consensus': 'Sync and consensus',
  'criticality-measurement': 'Criticality and measurement',
  'marl-emergence': 'Multi-agent RL',
  'llm-agent-swarms': 'LLM agent swarms',
  'crowds-and-traffic': 'Crowds and traffic',
  meta: 'Meta and tooling',
  'sybil-resistance': 'Sybil resistance',
  'fork-merge-security': 'Fork and merge security',
  'swarm-detection': 'Swarm detection',
};
export const topicName = (slug: string) => TOPIC_SHORT[slug] ?? slug.replace(/-/g, ' ');

export const ACTIVE_STATES = new Set(['working', 'active', 'running', 'busy']);
