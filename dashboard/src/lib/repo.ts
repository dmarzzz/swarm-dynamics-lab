/** GitHub links into the repository. Study files written before the research-phase layout move (the question
 *  atlas, the navigation crosswalk) are hash-bound and keep their old paths; `currentPath` resolves those. */
export const REPO_URL = 'https://github.com/dmarzzz/swarm-dynamics-lab';
export const REPO_NAME = 'dmarzzz/swarm-dynamics-lab';

const PREFIXES: [string, string][] = [
  ['library/', '1-library/'], ['surveys/', '2-surveys/'], ['reviews/', '2-surveys/reviews/'],
  ['synthesis/', '3-synthesis/'], ['hypotheses/', '4-hypotheses/'], ['experiments/', '5-experiments/'],
  ['tooling/', '5-experiments/toolkit/'], ['tasks/', 'lab/tasks/'], ['candidates/', 'lab/candidates/'],
  ['templates/', 'lab/templates/'],
];
const EXACT: Record<string, string> = { 'STATUS.md': 'lab/STATUS.md', 'PIPELINE.md': 'lab/PIPELINE.md' };

/** Old-layout repo path -> current path; a path already in the current layout is returned unchanged.
 *  Keep in step with dashboard/scripts/layout.py. */
export function currentPath(path: string): string {
  if (EXACT[path]) return EXACT[path];
  const study = /^researchers\/([^/]+)\/(?:notes\/|(?=(?:factory|qa)\/))/.exec(path);
  if (study) return `5-experiments/studies/${study[1]}/` + path.slice(study[0].length);
  if (path.startsWith('researchers/')) return 'lab/' + path;
  for (const [from, to] of PREFIXES) if (path.startsWith(from)) return to + path.slice(from.length);
  return path;
}

/** Link to a file on main, by repo path (old or current layout). */
export const repoFile = (path: string) => `${REPO_URL}/blob/main/` + currentPath(path).split('/').map(encodeURIComponent).join('/');
