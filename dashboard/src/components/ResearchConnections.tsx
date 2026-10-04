import { matchesHypothesis, type ResearchNavigation } from '../data/navigation';
import { href } from '../lib/router';
import { repoFile as repo } from '../lib/repo';
import './researchConnections.css';

export function ResearchConnections({ navigation: nav, topic = '', focus = '', project = '' }: {
  navigation: ResearchNavigation; topic?: string; focus?: string; project?: string;
}) {
  const designs = nav.designs.filter(d => matchesHypothesis(d, topic, focus, project));
  const hypotheses = nav.hypotheses.filter(h => matchesHypothesis(h, topic, focus, project));
  const selectedProject = nav.projects.find(p => p.id === project);
  return <details className="research-connections" open={!!(focus || project)}>
    <summary>Connected work · {designs.length} exploratory {designs.length === 1 ? 'design' : 'designs'} · {hypotheses.length} formal {hypotheses.length === 1 ? 'hypothesis' : 'hypotheses'}</summary>
    <p>Matches the research area and project filters. Question search and personal review choices do not filter these documents.</p>
    {selectedProject && <p>Project brief: <a href={repo(selectedProject.path)}>{selectedProject.name}</a></p>}
    {designs.length > 0 && <ul>{designs.map(d => <li key={d.id}><a href={repo(d.path)}>{d.title}</a> <span>— {d.status}</span></li>)}</ul>}
    <h3>Formal hypotheses</h3>
    {hypotheses.length ? <ul>{hypotheses.map(h => <li key={h.id}><a href={repo(h.path)}>{h.title}</a> — {h.status}
      <div className="research-tags">{h.topics.map(t => <a key={t} href={href('/questions', { topic: t })}>{t}</a>)}
        {h.focus_areas.map(f => <a key={f} href={href('/questions', { focus: f })}>{nav.focus_areas.find(x => x.id === f)?.name}</a>)}
        {h.projects.map(p => <a key={p} href={href('/questions', { project: p })}>{nav.projects.find(x => x.id === p)?.name}</a>)}
        {!h.topics.length && !h.focus_areas.length && !h.projects.length && <span>No research tags recorded</span>}
      </div></li>)}</ul> : <p>{nav.hypotheses.length ? 'No formal hypotheses carry these tags yet. Clear the area and project filters to see all registered hypotheses.' : 'No formal hypotheses are registered on main yet. Tentative question claims and exploratory designs do not count as accepted hypotheses.'}</p>}
    <p><a href={repo('dashboard/RESEARCH-AREAS.md')}>How to contribute research areas and tags</a></p>
  </details>;
}

export function ResearchFocusIndex({ navigation: nav }: { navigation: ResearchNavigation }) {
  return <section className="research-focus-index">
    <h2 className="h2">Explore across topics</h2>
    <p>Cross-cutting focus areas connect questions from several literature topics. Project filters also include reviewed connections to the original sixteen briefs.</p>
    {nav.mapping_stale && <p role="status">The question bank changed since these connections were reviewed. Check the linked questions before relying on the mapping.</p>}
    <div className="research-focus-grid">{nav.focus_areas.map(f => <article key={f.id}>
      <h3><a href={href('/questions', { focus: f.id })}>{f.name}</a></h3><p>{f.description}</p>
      <a href={href('/questions', { focus: f.id })}>{f.questions.length} connected questions</a>
    </article>)}</div>
    <details><summary>Original project briefs ({nav.projects.length})</summary><ul>{nav.projects.map(p => <li key={p.id}><a href={href('/questions', { project: p.id })}>{p.name}</a> · {p.questions.length} connected questions · <a href={repo(p.path)}>Read brief</a></li>)}</ul></details>
    <ResearchConnections navigation={nav} />
  </section>;
}
