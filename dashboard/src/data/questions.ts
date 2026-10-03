import { useEffect, useState } from 'react';

export interface QuestionSource {
  id: string;
  relation: string;
  title: string;
  path: string;
  url: string;
  catalogued_depth: string;
}

export interface Question {
  id: string;
  area: string;
  title: string;
  question: string;
  hypothesis: string;
  test: string;
  baseline: string;
  metrics: string[];
  falsifier: string;
  confounds: string;
  prior: QuestionSource[];
  novelty: string;
  feasibility: string;
  needs: string;
  briefs: string[];
  lane: string;
  status: 'unreviewed-hunch';
  candidate_sha256: string;
  change: 'new' | 'revised' | 'unchanged';
}

export interface QuestionAtlas {
  version: number;
  date: string;
  status: string;
  source_snapshot: string;
  content_sha256: string;
  topics: Record<string, string>;
  changes: Record<'new' | 'revised' | 'unchanged', string[]>;
  candidates: Question[];
}

export const questionsDataUrl = `${import.meta.env.BASE_URL || '/'}data/questions.json`;
type QuestionState = { status: 'loading' } | { status: 'error' } | { status: 'ready'; atlas: QuestionAtlas };

/** Load this large, optional view independently so other dashboard routes remain available. */
export function useQuestionAtlas(retry: number): QuestionState {
  const [state, setState] = useState<QuestionState>({ status: 'loading' });
  useEffect(() => {
    const controller = new AbortController();
    setState({ status: 'loading' });
    fetch(questionsDataUrl, { cache: 'no-cache', signal: controller.signal })
      .then(async response => {
        if (!response.ok) throw new Error('Question bank unavailable');
        const atlas: QuestionAtlas = await response.json();
        if (!atlas.topics || !atlas.changes || !Array.isArray(atlas.candidates) || !atlas.candidates.length) {
          throw new Error('Invalid question bank');
        }
        if (!controller.signal.aborted) setState({ status: 'ready', atlas });
      })
      .catch(() => { if (!controller.signal.aborted) setState({ status: 'error' }); });
    return () => controller.abort();
  }, [retry]);
  return state;
}
