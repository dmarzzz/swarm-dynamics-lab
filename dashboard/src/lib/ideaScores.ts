export const REVIEWERS = ['vishesh', 'dmarz', 'shadow'] as const;
export type Reviewer = typeof REVIEWERS[number];
export const REVIEWER_LABELS = { vishesh: 'Vishesh', dmarz: 'Dimarz', shadow: 'Shadow' };
export const WEIGHTS = { visual: .30, practical: .30, theory: .25, novelty: .15 };
export type Dimension = keyof typeof WEIGHTS;
export const DIMENSION_LABELS: Record<Dimension, string> = {
  visual: 'Visual potential', practical: 'Practical usefulness', theory: 'Physical / biological connection', novelty: 'Novelty relative to our work',
};
export const DIMENSIONS = Object.keys(WEIGHTS) as Dimension[];
export const RUBRIC_VERSION = 'vishesh-visual-bio-v1';
export const SCORE_STORAGE_KEY = 'swarm-idea-score-drafts-v1';
export interface Rating {
  dimensions: Record<Dimension, number>; score: number; rationale: string;
  assessed_by: string; assessed_at: string; candidate_sha256: string; stale?: boolean;
}
export interface ScoresData {
  schema: 'swarm-idea-scores-v1';
  rubric: { version: string; title: string; provenance: string; limitations: string; anchors: string; dimensions: Record<Dimension, string> };
  ideas: Record<string, { title: string; candidate_sha256: string; ratings: Record<Reviewer, Rating | null> }>;
}
export type Drafts = Partial<Record<Reviewer, Record<string, Rating | null>>>;
export const total = (dimensions: Record<Dimension, number>) => Math.round(DIMENSIONS.reduce((n, k) => n + dimensions[k] * WEIGHTS[k], 0));
export function validRating(value: unknown): value is Rating | null {
  if (value === null) return true;
  if (!value || typeof value !== 'object') return false;
  const r = value as Rating;
  return !!r.dimensions && Object.keys(r.dimensions).length === DIMENSIONS.length
    && DIMENSIONS.every(k => typeof r.dimensions[k] === 'number' && Number.isFinite(r.dimensions[k]) && r.dimensions[k] >= 0 && r.dimensions[k] <= 100)
    && r.score === total(r.dimensions)
    && ['rationale', 'assessed_by', 'assessed_at', 'candidate_sha256'].every(k => typeof r[k as keyof Rating] === 'string' && String(r[k as keyof Rating]).trim().length > 0);
}
export function parseDrafts(raw: string | null): Drafts {
  if (raw === null) return {};
  const d = JSON.parse(raw);
  if (d?.schema !== SCORE_STORAGE_KEY || d.rubric_version !== RUBRIC_VERSION || !d.ratings || typeof d.ratings !== 'object' || Array.isArray(d.ratings)) throw new Error('Unrecognized saved score drafts.');
  for (const [reviewer, rows] of Object.entries(d.ratings)) {
    if (!REVIEWERS.includes(reviewer as Reviewer) || !rows || typeof rows !== 'object' || Array.isArray(rows)
      || Object.entries(rows).some(([id, r]) => !/^[A-Z]+-\d+$/.test(id) || !validRating(r))) throw new Error('Invalid saved score drafts.');
  }
  return d.ratings;
}
export function effectiveRating(data: ScoresData, drafts: Drafts, id: string, reviewer: Reviewer): Rating | null {
  const source = data.ideas[id];
  if (!source) return null;
  const record = Object.hasOwn(drafts[reviewer] || {}, id) ? drafts[reviewer]![id] : source.ratings[reviewer];
  return record == null ? null : { ...record, stale: record.candidate_sha256 !== source.candidate_sha256 };
}
export function scoreExport(data: ScoresData, drafts: Drafts, reviewer: Reviewer) {
  return { schema: 'swarm-idea-review-v1', rubric_version: RUBRIC_VERSION, reviewer,
    ratings: Object.fromEntries(Object.keys(data.ideas).map(id => {
      const r = effectiveRating(data, drafts, id, reviewer);
      if (r === null) return [id, null];
      const { stale: _stale, ...record } = r;
      return [id, record];
    })) };
}
export function sortIdeas<T extends { id: string }>(items: T[], reviewer: string, data: ScoresData | null, drafts: Drafts): T[] {
  if (!data || !REVIEWERS.includes(reviewer as Reviewer)) return items;
  return [...items].sort((a, b) => {
    const ar = effectiveRating(data, drafts, a.id, reviewer as Reviewer), br = effectiveRating(data, drafts, b.id, reviewer as Reviewer);
    // Stale assessments remain visible but are not treated as current rankings.
    const av = ar && !ar.stale ? ar.score : -1, bv = br && !br.stale ? br.score : -1;
    return bv - av || a.id.localeCompare(b.id, undefined, { numeric: true });
  });
}
