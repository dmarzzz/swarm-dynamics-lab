import { useEffect, useState } from 'react';
export interface Contribution {
  id: string; title: string; question: string; prediction: string; comparison: string;
  falsifier: string; confounds: string; feasibility: string; decision_value: string;
  scenario: string; delta: string; metrics: string[]; briefs: string[]; atlas: string[];
  related: string[]; sources: string[]; source_note: string; status: string;
  activity?: { added_at: string | null; tags_added_at: Record<string, string>; is_new: boolean; new_tags: string[] };
  bank: string; owner: string; source_path: string;
}
export interface ContributionsData {
  schema: string; atlas_count: number; contribution_count: number; question_record_count: number;
  registered_hypothesis_count: number;
  activity_as_of?: string; recent_days?: number;
  banks: { id: string; owner: string; path: string; count: number }[];
  questions: Contribution[];
}
export function useContributions(retry = 0) {
  const [state, setState] = useState<{ status: 'loading' | 'error' | 'ready'; data?: ContributionsData }>({ status: 'loading' });
  useEffect(() => {
    const controller = new AbortController();
    setState({ status: 'loading' });
    fetch(`${import.meta.env.BASE_URL || '/'}data/contributions.json`, { cache: 'no-cache', signal: controller.signal })
      .then(async response => {
        if (!response.ok) throw new Error('Unavailable');
        const data: ContributionsData = await response.json();
        if (data.schema !== 'swarm-contributions-v1' || !Array.isArray(data.questions) || !Array.isArray(data.banks)
          || data.questions.length !== data.contribution_count || data.atlas_count + data.contribution_count !== data.question_record_count) throw new Error('Invalid contract');
        if (!controller.signal.aborted) setState({ status: 'ready', data });
      }).catch(() => { if (!controller.signal.aborted) setState({ status: 'error' }); });
    return () => controller.abort();
  }, [retry]);
  return state;
}
