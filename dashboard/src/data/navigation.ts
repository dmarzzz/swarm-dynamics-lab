export interface ResearchProject {
  id: string; name: string; path: string; questions: string[];
  direct_questions: string[]; reviewer_questions: string[];
}
export interface ResearchFocus { id: string; name: string; description: string; questions: string[] }
export interface ConnectedWork {
  id: string; title: string; path: string; status: string; focus_areas: string[]; projects: string[]; topics: string[];
}
export type TaggedHypothesis = ConnectedWork;
export interface ResearchNavigation {
  schema: string; owner: string; source_path: string; reviewed_at: string; mapping_stale: boolean;
  focus_areas: ResearchFocus[]; projects: ResearchProject[];
  designs: ConnectedWork[]; hypotheses: TaggedHypothesis[];
}

/** Primary areas and editorial connections are independent facets; all active facets intersect. */
export function matchesResearch(
  question: { id: string; area: string }, nav: ResearchNavigation,
  topic = '', focus = '', project = '',
): boolean {
  return (!topic || question.area === topic)
    && (!focus || !!nav.focus_areas.find(f => f.id === focus)?.questions.includes(question.id))
    && (!project || !!nav.projects.find(p => p.id === project)?.questions.includes(question.id));
}

export function matchesHypothesis(h: TaggedHypothesis, topic = '', focus = '', project = ''): boolean {
  return (!topic || h.topics.includes(topic)) && (!focus || h.focus_areas.includes(focus))
    && (!project || h.projects.includes(project));
}
