import { createContext, useContext, useEffect, useState, type ReactNode } from 'react';
import { DIMENSIONS, DIMENSION_LABELS, REVIEWERS, REVIEWER_LABELS, RUBRIC_VERSION, SCORE_STORAGE_KEY, WEIGHTS,
  effectiveRating, parseDrafts, scoreExport, total, validRating, type Dimension, type Drafts, type Rating, type Reviewer, type ScoresData } from '../lib/ideaScores';
import './ideaScores.css';

interface State { data: ScoresData | null; drafts: Drafts; status: string; notice: string; save: (id: string, reviewer: Reviewer, rating: Rating | null) => void; discard: (id: string, reviewer: Reviewer) => void; exportReviewer: (reviewer: Reviewer) => void }
const Context = createContext<State | null>(null);
export function useIdeaScores() { const state = useContext(Context); if (!state) throw new Error('Missing scores provider'); return state; }
const dataUrl = `${import.meta.env.BASE_URL || '/'}data/idea-scores.json`;

export function IdeaScoresProvider({ children }: { children: ReactNode }) {
  const [loaded] = useState(() => { try { return { drafts: parseDrafts(localStorage.getItem(SCORE_STORAGE_KEY)), notice: '' }; } catch { return { drafts: {} as Drafts, notice: 'Saved score drafts could not be read. Published ratings are unchanged.' }; } });
  const [drafts, setDrafts] = useState<Drafts>(loaded.drafts);
  const [notice, setNotice] = useState(loaded.notice);
  const [data, setData] = useState<ScoresData | null>(null);
  const [status, setStatus] = useState('loading');
  useEffect(() => {
    const controller = new AbortController();
    fetch(dataUrl, { cache: 'no-cache', signal: controller.signal }).then(async response => {
      if (!response.ok) throw new Error('Unavailable');
      const d: ScoresData = await response.json();
      if (d.schema !== 'swarm-idea-scores-v1' || d.rubric?.version !== RUBRIC_VERSION || !d.ideas || !Object.keys(d.ideas).length
        || Object.values(d.ideas).some(q => !q.ratings || !q.candidate_sha256 || REVIEWERS.some(r => !Object.hasOwn(q.ratings, r) || !validRating(q.ratings[r])))) throw new Error('Invalid scores');
      setData(d); setStatus('ready');
    }).catch(() => { if (!controller.signal.aborted) setStatus('error'); });
    return () => controller.abort();
  }, []);
  const persist = (next: Drafts) => {
    setDrafts(next);
    try { localStorage.setItem(SCORE_STORAGE_KEY, JSON.stringify({ schema: SCORE_STORAGE_KEY, rubric_version: RUBRIC_VERSION, ratings: next })); setNotice('Score draft saved on this device only. Export and commit it to publish.'); }
    catch { setNotice('Could not save to this device. Your draft is in memory; export before leaving.'); }
  };
  const save = (id: string, reviewer: Reviewer, rating: Rating | null) => {
    if (!data?.ideas[id] || !validRating(rating)) throw new Error('Invalid score');
    persist({ ...drafts, [reviewer]: { ...drafts[reviewer], [id]: rating } });
  };
  const discard = (id: string, reviewer: Reviewer) => {
    const next = { ...drafts[reviewer] }; delete next[id]; persist({ ...drafts, [reviewer]: next });
  };
  const exportReviewer = (reviewer: Reviewer) => {
    if (!data) return;
    const blob = new Blob([JSON.stringify(scoreExport(data, drafts, reviewer), null, 2) + '\n'], { type: 'application/json' });
    const url = URL.createObjectURL(blob), a = document.createElement('a'); a.href = url; a.download = `${reviewer}.json`; a.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000); setNotice(`Exported ${REVIEWER_LABELS[reviewer]} ratings. Nothing was published automatically.`);
  };
  return <Context.Provider value={{ data, drafts, status, notice, save, discard, exportReviewer }}>{children}</Context.Provider>;
}

export function ScoreGuide() {
  const { data, status, notice } = useIdeaScores();
  return <aside className="score-guide" aria-label="Research scoring rubric">
    <strong>Researcher scores / 100</strong>
    <p>Visual potential 30% · Practical usefulness 30% · Physical / biological connection 25% · Novelty relative to our work 15%.</p>
    <p>Vishesh’s initial scores were assessed by Codex on his behalf. Dimarz and Shadow are optional: NA means not rated, never zero.</p>
    {status === 'error' ? <p role="alert">Published scores could not be loaded. Reload to retry; this is not an NA rating.</p> : status === 'loading' ? <p role="status">Loading scores…</p> : <details><summary>Rubric, provenance and downloads</summary><p>{data?.rubric.anchors}</p><p>{data?.rubric.limitations}</p><p><a href={dataUrl}>Download all scores</a> · <a href="https://github.com/dmarzzz/swarm-lab/blob/main/dashboard/IDEA-SCORES.md">How to publish your scores</a></p></details>}
    {notice && <p role="status">{notice}</p>}
  </aside>;
}

export function ScoreSort({ value, onChange }: { value: string; onChange: (value: string) => void }) {
  return <label>Sort by score<select value={value} onChange={e => onChange(e.target.value)}><option value="">Catalogue order</option>{REVIEWERS.map(r => <option key={r} value={r}>{REVIEWER_LABELS[r]}: highest first</option>)}</select></label>;
}

export function ScoreBadges({ id }: { id: string }) {
  const { data, drafts, status } = useIdeaScores();
  if (!data) return <span className="score-badges">{status === 'error' ? 'Scores unavailable' : 'Scores loading…'}</span>;
  return <span className="score-badges">{REVIEWERS.map(reviewer => {
    const r = effectiveRating(data, drafts, id, reviewer), draft = Object.hasOwn(drafts[reviewer] || {}, id);
    return <span key={reviewer} title={r?.rationale}>{REVIEWER_LABELS[reviewer]} <b>{r?.score ?? 'NA'}</b>{draft ? ' (draft)' : ''}{r?.stale ? ' · review again' : ''}</span>;
  })}</span>;
}

export function ScorePanel({ id }: { id: string }) {
  const { data, drafts } = useIdeaScores();
  const [reviewer, setReviewer] = useState<Reviewer>('dmarz');
  if (!data?.ideas[id]) return null;
  return <section className="idea-score-panel" aria-label={`Researcher scores for ${id}`}>
    <ScoreBadges id={id} />
    <details><summary>Score breakdown and optional rating</summary>
      {REVIEWERS.map(r => {
        const rating = effectiveRating(data, drafts, id, r);
        return <div className="score-explanation" key={r}><strong>{REVIEWER_LABELS[r]}: {rating?.score ?? 'NA'}</strong>{rating ? <><p>{DIMENSIONS.map(k => `${DIMENSION_LABELS[k]} ${rating.dimensions[k]}`).join(' · ')}</p><p>{rating.rationale}</p><small>Assessed by {rating.assessed_by} · {rating.assessed_at}{rating.stale ? ' · Content changed; review this score again.' : ''}</small></> : <p>No rating supplied.</p>}</div>;
      })}
      <label>Whose score are you entering?<select value={reviewer} onChange={e => setReviewer(e.target.value as Reviewer)}>{REVIEWERS.map(r => <option key={r} value={r}>{REVIEWER_LABELS[r]}</option>)}</select></label>
      <RatingEditor key={`${id}-${reviewer}`} id={id} reviewer={reviewer} />
    </details>
  </section>;
}

function RatingEditor({ id, reviewer }: { id: string; reviewer: Reviewer }) {
  const { data, drafts, save, discard, exportReviewer } = useIdeaScores();
  const existing = effectiveRating(data!, drafts, id, reviewer);
  const [values, setValues] = useState<Record<Dimension, string>>(() => Object.fromEntries(DIMENSIONS.map(k => [k, existing == null ? '' : String(existing.dimensions[k])])) as Record<Dimension, string>);
  const [rationale, setRationale] = useState(existing?.rationale ?? '');
  const [error, setError] = useState('');
  const complete = DIMENSIONS.every(k => values[k].trim() !== '' && Number.isFinite(Number(values[k])) && Number(values[k]) >= 0 && Number(values[k]) <= 100);
  const dimensions = Object.fromEntries(DIMENSIONS.map(k => [k, Number(values[k])])) as Record<Dimension, number>;
  return <form className="score-editor" onSubmit={e => {
    e.preventDefault();
    if (!complete || !rationale.trim()) { setError('Enter all four dimensions from 0 to 100 and a short rationale, or choose Set to NA.'); return; }
    save(id, reviewer, { dimensions, score: total(dimensions), rationale: rationale.trim(), assessed_by: `${reviewer}/local-review`, assessed_at: new Date().toISOString(), candidate_sha256: data!.ideas[id].candidate_sha256 }); setError('');
  }}>
    <p>Only enter ratings for yourself or someone who authorized you. These are local drafts. Export and commit the reviewer file to publish; this page does not authenticate a reviewer.</p>
    <div className="score-inputs">{DIMENSIONS.map(k => <label key={k}>{DIMENSION_LABELS[k]} ({WEIGHTS[k] * 100}%)<input type="number" min="0" max="100" step="any" placeholder="NA" value={values[k]} onChange={e => setValues({ ...values, [k]: e.target.value })} /></label>)}</div>
    <label>Score rationale<textarea value={rationale} onChange={e => setRationale(e.target.value)} rows={3} /></label>
    <p>Weighted score: <strong>{complete ? total(dimensions) : 'NA'}</strong></p>
    <div className="score-actions"><button type="submit">Save local draft</button><button type="button" onClick={() => { save(id, reviewer, null); setValues({ visual: '', practical: '', theory: '', novelty: '' }); setRationale(''); setError(''); }}>Set to NA</button>
      <button type="button" onClick={() => { discard(id, reviewer); const published = data!.ideas[id].ratings[reviewer]; setValues(Object.fromEntries(DIMENSIONS.map(k => [k, published == null ? '' : String(published.dimensions[k])])) as Record<Dimension, string>); setRationale(published?.rationale ?? ''); setError(''); }}>Discard local draft</button>
      <button type="button" onClick={() => exportReviewer(reviewer)}>Export {REVIEWER_LABELS[reviewer]} scores</button></div>
    <p>Exports include saved drafts only. Publish at <a href={`https://github.com/dmarzzz/swarm-lab/blob/main/dashboard/idea-scores/${reviewer}.json`}>dashboard/idea-scores/{reviewer}.json</a>. Reconcile the latest file before committing.</p>
    {error && <p role="alert">{error}</p>}
  </form>;
}
