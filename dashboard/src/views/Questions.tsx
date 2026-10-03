import { ContributionCount } from './Contributions';
import { useDeferredValue, useMemo, useRef, useState } from 'react';
import { questionsDataUrl, useQuestionAtlas, type Question, type QuestionAtlas } from '../data/questions';
import {
  QUESTION_REVIEW_STORAGE_KEY, QUESTION_REVIEW_STATUSES, parseReviewState,
  mergeReviewImport, createReviewExport, updateReview, acknowledgeReview, needsRecheck,
  type QuestionReviewState,
} from '../lib/questionReviews';
import { href, useParamSetter } from '../lib/router';
import './questions.css';
import { matchesResearch, type ResearchNavigation } from '../data/navigation';
import { ResearchConnections } from '../components/ResearchConnections';

const REPO = 'https://github.com/dmarzzz/swarm-lab/blob/main/';
const GUIDE = REPO + 'synthesis/research-question-atlas.md';
const TEST_CLASSES: Record<string, string> = {
  offline: 'Offline simulation / traces', 'api-small': 'Small model-call study',
  training: 'Train policies / models', hardware: 'Hardware / physical access',
  'access-dependent': 'Dataset / participant access',
};
const repoLink = (path: string) => REPO + path.split('/').map(encodeURIComponent).join('/');
const normalize = (value: string) => value.toLowerCase().normalize('NFKD').replace(/[\u0300-\u036f]/g, '');

export function Questions({ params, navigation }: { params: URLSearchParams; navigation: ResearchNavigation }) {
  const [retry, setRetry] = useState(0);
  const state = useQuestionAtlas(retry);
  if (state.status === 'loading') return <div className="wrap page-head" role="status">Loading research questions…</div>;
  if (state.status === 'error') return <div className="wrap page-head">
    <h1 className="display">The question bank is unavailable.</h1>
    <p className="lede">Try loading it again, or read the source-linked bank in the repository.</p>
    <div className="q-actions"><button className="q-button" onClick={() => setRetry(n => n + 1)}>Try again</button><a href={GUIDE}>Read the research guide</a></div>
  </div>;
  return <QuestionBrowser atlas={state.atlas} params={params} navigation={navigation} />;
}

function QuestionBrowser({ atlas, params, navigation }: { atlas: QuestionAtlas; params: URLSearchParams; navigation: ResearchNavigation }) {
  const setParams = useParamSetter('/questions');
  const ids = useMemo(() => new Set(atlas.candidates.map(d => d.id)), [atlas]);
  const [loaded] = useState(() => {
    try { return parseReviewState(localStorage.getItem(QUESTION_REVIEW_STORAGE_KEY), ids); }
    catch { return { state: { reviewer: '', review: {} } as QuestionReviewState, warning: 'Local storage is unavailable. Export your review before leaving.' }; }
  });
  const [reviewState, setReviewState] = useState(loaded.state);
  const latestReview = useRef(loaded.state);
  const [notice, setNotice] = useState(loaded.warning || '');
  const [importing, setImporting] = useState(false);
  const importRef = useRef<HTMLInputElement>(null);
  const detailRef = useRef<HTMLElement>(null);
  const search = params.get('q') || '';
  const query = useDeferredValue(normalize(search));
  const topic = params.get('topic') || '';
  const focus = params.get('focus') || '';
  const project = params.get('project') || '';
  const selectedFocus = navigation.focus_areas.find(f => f.id === focus);
  const kind = params.get('kind') || '';
  const testClass = params.get('test') || '';
  const change = params.get('change') || '';
  const decision = params.get('review') || '';
  const review = reviewState.review;
  const index = useMemo(() => atlas.candidates.map(d => ({ d, text: normalize(JSON.stringify(d)) })), [atlas]);
  const rows = index.filter(({ d, text }) => (!query || query.split(/\s+/).every(t => text.includes(t)))
    && matchesResearch(d, navigation, topic, focus, project) && (!kind || d.novelty === kind) && (!testClass || d.feasibility === testClass)
    && (!decision || (review[d.id]?.status || 'Unreviewed') === decision)
    && (!change || (change === 'recheck' ? needsRecheck(d, review[d.id]) : d.change === change))).map(({ d }) => d);
  const selected = rows.find(d => d.id === params.get('id')) || rows[0];
  const shortlisted = atlas.candidates.filter(d => review[d.id]?.status === 'Shortlist').length;
  const pending = atlas.candidates.filter(d => needsRecheck(d, review[d.id])).length;
  const topicCounts = useMemo(() => atlas.candidates.reduce<Record<string, number>>((out, d) => {
    out[d.area] = (out[d.area] || 0) + 1; return out;
  }, {}), [atlas]);
  const save = (next: QuestionReviewState) => {
    const stamped = { ...next, content_sha256: atlas.content_sha256 };
    latestReview.current = stamped;
    setReviewState(stamped);
    try {
      localStorage.setItem(QUESTION_REVIEW_STORAGE_KEY, JSON.stringify(stamped));
      setNotice('Saved on this device for this site. Export to share or move your review.');
      return true;
    } catch {
      setNotice('Could not save on this device. Your review is still here; export it before leaving.');
      return false;
    }
  };
  const clear = () => setParams({ q: null, topic: null, focus: null, project: null, kind: null, test: null, change: null, review: null, id: null });
  const select = (id: string) => {
    setParams({ id });
    requestAnimationFrame(() => {
      detailRef.current?.focus({ preventScroll: true });
      if (matchMedia('(max-width: 760px)').matches) detailRef.current?.scrollIntoView({ block: 'start' });
    });
  };
  const exportReview = () => {
    const payload = createReviewExport(reviewState, atlas.candidates, atlas.content_sha256, new Date().toISOString());
    const url = URL.createObjectURL(new Blob([JSON.stringify(payload, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url; link.download = `swarm-lab-review-${new Date().toISOString().slice(0, 10)}.json`; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    setNotice('Review exported. Nothing was sent automatically.');
  };
  const importReview = async (file: File) => {
    setImporting(true);
    try {
      const raw = await file.text();
      const result = mergeReviewImport(latestReview.current, raw, atlas.candidates, atlas.content_sha256);
      const persisted = save(result.state);
      setNotice(`Imported ${result.imported} candidate reviews. Overlapping choices were replaced.${result.atlasMismatch ? ' The source bank differs; check Needs review again.' : ''}${persisted ? '' : ' Could not save on this device; export your review before leaving.'}`);
    } catch (error) { setNotice(`Import failed: ${error instanceof Error ? error.message : 'Unrecognized review file.'} Your current review was kept.`); }
    finally { setImporting(false); if (importRef.current) importRef.current.value = ''; }
  };

  return <div className="wrap questions-page">
    <header className="page-head q-heading">
      <h1 className="display">Questions worth testing.</h1>
      <ContributionCount />
      <p className="lede">{atlas.candidates.length} questions across {Object.keys(atlas.topics).length} literature topics and {navigation.focus_areas.length} cross-cutting focus areas, connected to {navigation.projects.length} project ideas. Each question has a tentative hypothesis, a test and evidence that could count against it.</p>
      <p className="q-boundary">For human selection. These are unreviewed ideas; shortlisting does not approve an experiment.</p>
      <div className="q-update"><span>Update {atlas.version}</span><button onClick={() => setParams({ change: 'new', id: null })}>{atlas.changes.new.length} new</button><button onClick={() => setParams({ change: 'revised', id: null })}>{atlas.changes.revised.length} revised</button><span>{atlas.date}</span><a href={GUIDE}>Research guide</a><a href={questionsDataUrl} download="swarm-lab-questions.json">Download question bank</a></div>
    </header>

    <section className="q-tools" aria-label="Find and review questions">
      <div className="q-filters">
        <label className="q-search">Search questions, tests and sources<input type="search" value={search} placeholder="Try memory, dissent or commons" onChange={e => setParams({ q: e.target.value || null, id: null })} /></label>
        <label>Research area<select value={focus ? `focus:${focus}` : topic} onChange={e => { const value = e.target.value; setParams({ topic: value.startsWith('focus:') ? null : value || null, focus: value.startsWith('focus:') ? value.slice(6) : null, id: null }); }}><option value="">All areas</option><optgroup label="Literature topics">{Object.entries(atlas.topics).sort((a, b) => a[1].localeCompare(b[1])).map(([id, name]) => <option key={id} value={id}>{name} ({topicCounts[id] ?? 0})</option>)}</optgroup><optgroup label="Cross-cutting focus areas">{navigation.focus_areas.map(f => <option key={f.id} value={`focus:${f.id}`}>{f.name} ({f.questions.length})</option>)}</optgroup></select></label>
        <label>Project idea<select value={project} onChange={e => setParams({ project: e.target.value || null, id: null })}><option value="">All project ideas</option>{navigation.projects.map(p => <option key={p.id} value={p.id}>{p.name} ({p.questions.length})</option>)}</select></label>
        <label>Kind of question<select value={kind} onChange={e => setParams({ kind: e.target.value || null, id: null })}><option value="">All kinds</option>{[...new Set(atlas.candidates.map(d => d.novelty))].sort().map(value => <option key={value}>{value}</option>)}</select></label>
        <label>First test<select value={testClass} onChange={e => setParams({ test: e.target.value || null, id: null })}><option value="">All test classes</option>{Object.entries(TEST_CLASSES).map(([value, label]) => <option key={value} value={value}>{label}</option>)}</select></label>
        <label>Research update<select value={change} onChange={e => setParams({ change: e.target.value || null, id: null })}><option value="">All versions</option><option value="new">New in this update</option><option value="revised">Revised in this update</option><option value="recheck">Needs review again ({pending})</option></select></label>
        <label>Your review<select value={decision} onChange={e => setParams({ review: e.target.value || null, id: null })}><option value="">All choices</option>{QUESTION_REVIEW_STATUSES.map(value => <option key={value}>{value}</option>)}</select></label>
      </div>
      <div className="q-review-tools">
        <p role="status">{rows.length} / {atlas.candidates.length} shown · {shortlisted} shortlisted</p>
        <button className="q-button" onClick={clear}>Clear filters</button>
        <label className="q-reviewer">Reviewer<input value={reviewState.reviewer} placeholder="Your name" onChange={e => save({ ...reviewState, reviewer: e.target.value })} /></label>
        <button className="q-button" onClick={exportReview}>Export review</button>
        <button className="q-button" disabled={importing} onClick={() => importRef.current?.click()}>{importing ? 'Importing…' : 'Import review'}</button>
        <input ref={importRef} className="sr-only" type="file" accept="application/json,.json" aria-label="Review file" tabIndex={-1} onChange={e => { const file = e.target.files?.[0]; if (file) void importReview(file); }} />
      </div>
      <p className="q-storage">Reviews stay on this device for this site. Import an earlier atlas review to bring its notes here. Export before combining reviewers; imports replace overlapping choices.</p>
      <p className="q-storage">Focus areas and project connections are editorial mappings by {navigation.owner}, reviewed {navigation.reviewed_at}. Counts show total membership; active filters intersect. <a href={repoLink('dashboard/RESEARCH-AREAS.md')}>Contribute a connection</a></p>
      {selectedFocus && <p>{selectedFocus.description}</p>}
      {topic && focus && <p role="status">Both the literature topic “{atlas.topics[topic] || topic}” and focus area “{selectedFocus?.name || focus}” are active in this link.</p>}
      {navigation.mapping_stale && <p role="status">The atlas changed since these connections were reviewed. Treat the mapping as needing another look.</p>}
      {notice && <p className="q-notice" role="status">{notice}</p>}
    </section>

    <ResearchConnections navigation={navigation} topic={topic} focus={focus} project={project} />

    {selected ? <div className="q-browser">
      <nav className="q-list" aria-label="Candidate questions">{rows.map(d => <button key={d.id} className={`q-row${d.id === selected.id ? ' selected' : ''}`} aria-current={d.id === selected.id ? 'true' : undefined} onClick={() => select(d.id)}>
        <span className="q-row-meta"><span>{d.id}</span><span>{review[d.id]?.status || 'Unreviewed'}</span>{d.change !== 'unchanged' && <span className="q-change">{d.change}</span>}</span>
        <strong>{d.title}</strong><span className="q-row-topic">{atlas.topics[d.area]}</span>{needsRecheck(d, review[d.id]) && <span className="q-recheck">Review again</span>}
      </button>)}</nav>
      <article className="q-detail" tabIndex={-1} ref={detailRef} aria-label={`${selected.id}: ${selected.title}`} key={selected.id}>
        <div className="q-detail-meta"><span>{selected.id}</span><span>{atlas.topics[selected.area]}</span><a href={href('/questions', { id: selected.id })}>Link to this question</a></div>
        <h2>{selected.title}</h2>
        <div className="q-tags"><span>{selected.novelty}</span><span>{TEST_CLASSES[selected.feasibility]}</span><span>{selected.change} in update {atlas.version}</span></div>
        <div className="research-tags" aria-label="Research connections">{navigation.focus_areas.filter(f => f.questions.includes(selected.id)).map(f => <a key={f.id} href={href('/questions', { focus: f.id })}>{f.name}</a>)}</div>
        {navigation.projects.some(p => p.questions.includes(selected.id)) && <section className="q-section"><h3>Project connections</h3><ul>{navigation.projects.filter(p => p.questions.includes(selected.id)).map(p => <li key={p.id}><a href={repoLink(p.path)}>{p.name}</a> — {p.direct_questions.includes(selected.id) ? 'linked by the question author' : 'reviewer cross-connection'} · <a href={href('/questions', { project: p.id })}>Explore project questions</a></li>)}</ul></section>}
        {needsRecheck(selected, review[selected.id]) && <div className="q-stale"><p>This question changed. Your earlier choice and notes are preserved; review the updated test before keeping your choice.</p><button className="q-button" onClick={() => save(acknowledgeReview(reviewState, selected, new Date().toISOString()))}>Keep my choice after reviewing this update</button></div>}
        <QuestionSection title="Question" text={selected.question} />
        <div className="q-hypothesis"><QuestionSection title="Tentative hypothesis" text={selected.hypothesis} /></div>
        <QuestionSection title="How we could test it" text={selected.test} />
        <QuestionSection title="Compare against" text={selected.baseline} />
        <section className="q-section"><h3>What to measure</h3><ul>{selected.metrics.map(metric => <li key={metric}>{metric}</li>)}</ul></section>
        <QuestionSection title="What would count against it" text={selected.falsifier} />
        <QuestionSection title="Confounds to control" text={selected.confounds} />
        <QuestionSection title="Before promotion" text={selected.needs} />
        <section className="q-section"><h3>Closest prior work</h3><p className="q-help">Reading depths come from the catalogue. These links are starting points for a focused review, not a novelty certification.</p><ol className="q-sources">{selected.prior.map(source => <li key={source.id}>
          <a href={href('/library', { e: source.id })}>{source.title}</a><p>{source.relation}</p><div className="q-source-links"><span>Catalogue depth: {source.catalogued_depth}</span><a href={repoLink(source.path)}>Source record</a>{/^https?:\/\//.test(source.url) && <a href={source.url} target="_blank" rel="noopener noreferrer">Original source</a>}</div>
        </li>)}</ol></section>
        {selected.briefs.length > 0 && <section className="q-section"><h3>Related team work</h3><ul>{selected.briefs.map(path => <li key={path}><a href={repoLink(path)}>{path.split('/').pop()?.replace(/\.md$/, '').replace(/-/g, ' ')}</a></li>)}</ul></section>}
        <section className="q-selection"><h3>Your review</h3><div className="q-decisions" role="group" aria-label="Selection decision">{QUESTION_REVIEW_STATUSES.map(status => <button key={status} className="q-button" aria-pressed={(review[selected.id]?.status || 'Unreviewed') === status} onClick={() => save(updateReview(reviewState, selected, { status }, new Date().toISOString()))}>{status}</button>)}</div>
          <label htmlFor="question-notes">Why pursue, discuss or park this?</label><textarea id="question-notes" rows={4} value={review[selected.id]?.notes || ''} placeholder="What matters? What would need to change?" onChange={e => save(updateReview(reviewState, selected, { notes: e.target.value }, new Date().toISOString()))} />
          <p className="q-help">A selection note keeps the research status unchanged. Formal hypotheses and protocols still need their reviews.</p>
        </section>
      </article>
    </div> : <section className="q-empty"><h2>No questions match these filters.</h2><p>Try a broader search or clear the filters to explore the full bank.</p><button className="q-button" onClick={clear}>Show all questions</button></section>}
  </div>;
}

function QuestionSection({ title, text }: { title: string; text: Question['question'] }) {
  return <section className="q-section"><h3>{title}</h3><p>{text}</p></section>;
}
