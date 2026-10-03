export const QUESTION_REVIEW_STORAGE_KEY = 'swarm-lab-question-atlas-review-v1';
export const QUESTION_REVIEW_SCHEMA = 'swarm-lab-question-review-v1';
export const QUESTION_REVIEW_STATUSES = ['Unreviewed', 'Shortlist', 'Discuss', 'Park'] as const;

export type QuestionReviewStatus = typeof QUESTION_REVIEW_STATUSES[number];

export interface QuestionReview {
  status: QuestionReviewStatus;
  notes: string;
  updated: string;
  candidate_sha256?: string;
}

export interface QuestionReviewState {
  reviewer: string;
  review: Record<string, QuestionReview>;
  content_sha256?: string;
}

export interface QuestionReviewCandidate {
  id: string;
  title: string;
  candidate_sha256: string;
  change?: string;
}

export interface QuestionReviewExport {
  schema: typeof QUESTION_REVIEW_SCHEMA;
  date: string;
  reviewer: string;
  atlas_sha256: string;
  review: Record<string, QuestionReview & { title: string }>;
}

function isRecord(value: unknown): value is Record<string, unknown> {
  if (typeof value !== 'object' || value === null || Array.isArray(value)) return false;
  const prototype = Object.getPrototypeOf(value);
  return prototype === Object.prototype || prototype === null;
}

function isStatus(value: unknown): value is QuestionReviewStatus {
  return typeof value === 'string' && QUESTION_REVIEW_STATUSES.some(status => status === value);
}

function readReview(value: unknown): QuestionReview | null {
  if (!isRecord(value) || (value.status !== undefined && !isStatus(value.status))) return null;
  return {
    status: isStatus(value.status) ? value.status : 'Unreviewed',
    notes: typeof value.notes === 'string' ? value.notes : '',
    updated: typeof value.updated === 'string' ? value.updated : '',
    // Missing fingerprints identify legacy reviews. Never substitute the latest hash.
    ...(typeof value.candidate_sha256 === 'string' && value.candidate_sha256
      ? { candidate_sha256: value.candidate_sha256 }
      : {}),
  };
}

function emptyState(): QuestionReviewState {
  return { reviewer: '', review: {} };
}

/** Recover valid local entries without throwing or modifying the saved source. */
export function parseReviewState(
  raw: string | null,
  knownIds: ReadonlySet<string>,
): { state: QuestionReviewState; warning?: string } {
  if (raw === null) return { state: emptyState() };
  let saved: unknown;
  try {
    saved = JSON.parse(raw);
  } catch {
    return { state: emptyState(), warning: 'Saved review data could not be read.' };
  }
  if (!isRecord(saved) || (saved.review !== undefined && !isRecord(saved.review))) {
    return { state: emptyState(), warning: 'Saved review data has an unrecognized format.' };
  }
  let invalid = saved.reviewer !== undefined && typeof saved.reviewer !== 'string';
  const entries: [string, QuestionReview][] = [];
  for (const [id, value] of Object.entries(saved.review ?? {})) {
    if (!knownIds.has(id)) continue;
    const review = readReview(value);
    if (review) {
      entries.push([id, review]);
      if (isRecord(value) && ['notes', 'updated', 'candidate_sha256'].some(
        key => value[key] !== undefined && typeof value[key] !== 'string',
      )) invalid = true;
    }
    else invalid = true;
  }
  const state: QuestionReviewState = {
    reviewer: typeof saved.reviewer === 'string' ? saved.reviewer : '',
    review: Object.fromEntries(entries),
    ...(typeof saved.content_sha256 === 'string' ? { content_sha256: saved.content_sha256 } : {}),
  };
  return invalid
    ? { state, warning: 'Some saved review data was invalid; valid choices and notes were recovered.' }
    : { state };
}

export function needsRecheck(candidate: QuestionReviewCandidate, review?: QuestionReview): boolean {
  if (!review) return false;
  return review.candidate_sha256
    ? review.candidate_sha256 !== candidate.candidate_sha256
    : candidate.change === 'revised';
}

/** Imports are atomic: an invalid known entry rejects the entire import. */
export function mergeReviewImport(
  state: QuestionReviewState,
  raw: unknown,
  candidates: readonly QuestionReviewCandidate[],
  currentAtlasSha: string,
): { state: QuestionReviewState; imported: number; atlasMismatch: boolean } {
  let payload: unknown = raw;
  if (typeof raw === 'string') {
    try {
      payload = JSON.parse(raw);
    } catch {
      throw new Error('The selected file is not valid JSON.');
    }
  }
  if (!isRecord(payload) || payload.schema !== QUESTION_REVIEW_SCHEMA || !isRecord(payload.review)) {
    throw new Error('Unrecognized review format.');
  }
  const knownIds = new Set(candidates.map(candidate => candidate.id));
  const additions: [string, QuestionReview][] = [];
  for (const [id, value] of Object.entries(payload.review)) {
    if (!knownIds.has(id)) continue;
    if (isRecord(value) && ['notes', 'updated', 'candidate_sha256'].some(
      key => Object.prototype.hasOwnProperty.call(value, key) && typeof value[key] !== 'string',
    )) throw new Error(`Invalid review fields for ${id}.`);
    const review = readReview(value);
    if (!review) throw new Error(`Invalid decision for ${id}.`);
    additions.push([id, review]);
  }
  return {
    state: {
      ...state,
      // Like the standalone reviewer, importing decisions keeps the local reviewer name.
      review: { ...state.review, ...Object.fromEntries(additions) },
      content_sha256: currentAtlasSha,
    },
    imported: additions.length,
    atlasMismatch: payload.atlas_sha256 !== currentAtlasSha,
  };
}

/** Prepare the existing v1 interchange format; exporting never acknowledges a revision. */
export function createReviewExport(
  state: QuestionReviewState,
  candidates: readonly QuestionReviewCandidate[],
  atlasSha: string,
  date: string,
): QuestionReviewExport {
  const entries: [string, QuestionReview & { title: string }][] = [];
  for (const candidate of candidates) {
    if (!Object.prototype.hasOwnProperty.call(state.review, candidate.id)) continue;
    const review = state.review[candidate.id];
    entries.push([candidate.id, { title: candidate.title, ...review }]);
  }
  return {
    schema: QUESTION_REVIEW_SCHEMA,
    date,
    reviewer: state.reviewer,
    atlas_sha256: atlasSha,
    review: Object.fromEntries(entries),
  };
}

export function updateReview(
  state: QuestionReviewState,
  candidate: QuestionReviewCandidate,
  change: { status?: QuestionReviewStatus; notes?: string },
  updated: string,
): QuestionReviewState {
  if (change.status === undefined && change.notes === undefined) return state;
  if (change.status !== undefined && !isStatus(change.status)) throw new Error('Invalid decision.');
  if (change.notes !== undefined && typeof change.notes !== 'string') throw new Error('Invalid notes.');
  const existing = Object.prototype.hasOwnProperty.call(state.review, candidate.id)
    ? state.review[candidate.id]
    : undefined;
  const review: QuestionReview = {
    ...(existing ?? { status: 'Unreviewed', notes: '', updated: '', candidate_sha256: candidate.candidate_sha256 }),
    ...(change.status !== undefined ? { status: change.status } : {}),
    ...(change.notes !== undefined ? { notes: change.notes } : {}),
    updated,
    // Editing old notes does not silently confirm that the revised card was reviewed.
    ...(change.status !== undefined ? { candidate_sha256: candidate.candidate_sha256 } : {}),
  };
  return { ...state, review: { ...state.review, [candidate.id]: review } };
}

export function acknowledgeReview(
  state: QuestionReviewState,
  candidate: QuestionReviewCandidate,
  updated: string,
): QuestionReviewState {
  if (!Object.prototype.hasOwnProperty.call(state.review, candidate.id)) return state;
  return {
    ...state,
    review: {
      ...state.review,
      [candidate.id]: { ...state.review[candidate.id], candidate_sha256: candidate.candidate_sha256, updated },
    },
  };
}
