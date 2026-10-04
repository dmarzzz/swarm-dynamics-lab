import { ScoreGuide, ScoreSort, ScorePanel, useIdeaScores } from '../components/IdeaScores';
import { sortIdeas } from '../lib/ideaScores';
import { useState } from 'react';
import { useContributions } from '../data/contributions';
import { href, useParamSetter } from '../lib/router';
import { repoFile } from '../lib/repo';
import './questions.css';
import './contributions.css';

export function ContributionCount() {
  const { status, data } = useContributions();
  return <p className="q-boundary">{data ? <>{data.atlas_count} atlas + {data.contribution_count} contributed = {data.question_record_count} question records. Overlapping ideas are not independent hypotheses. </> : status === 'error' ? 'Contribution counts are currently unavailable. ' : 'Loading contribution counts. '}<a href="#/contributions">View contributions</a>.</p>;
}

export function Contributions({ params }: { params: URLSearchParams }) {
  const [retry, setRetry] = useState(0);
  const { status, data } = useContributions(retry);
  const set = useParamSetter('/contributions');
  const scores = useIdeaScores();
  const scoreSort = params.get('score') || '';
  const q = params.get('q') || '', bank = params.get('bank') || '', brief = params.get('brief') || '', activity = params.get('activity') || '';
  const query = q.trim().toLowerCase();
  const filteredQuestions = data?.questions.filter(item => (!bank || item.bank === bank) && (!brief || item.briefs.includes(brief))
    && (!activity || (activity === 'new' ? item.activity?.is_new : activity === 'tags' ? !!item.activity?.new_tags.length : false))
    && (!query || `${item.id} ${item.title} ${item.question} ${item.delta} ${item.atlas.join(' ')} ${item.related.join(' ')}`.toLowerCase().includes(query))) || [];
  const questions = sortIdeas(filteredQuestions, scoreSort, scores.data, scores.drafts);
  const briefs = [...new Set(data?.questions.flatMap(item => item.briefs) || [])].sort();
  return <div className="wrap contribution-page">
    <header className="page-head"><p className="eyebrow">Exploratory research</p><h1 className="display">Contributed questions.</h1>
      <p className="lede">Concrete comparisons and extensions from researcher notes.</p>
      {data && <p>{data.atlas_count} atlas + {data.contribution_count} contributed = <strong>{data.question_record_count} question records</strong>. {data.registered_hypothesis_count} registered hypotheses.</p>}
      <p className="q-boundary">These ideas overlap. They are unreviewed hunches, not approved experiments or claims of novelty. Source links are catalogue leads; check the methods before adopting a prediction. Canonical atlas reviews remain separate.</p>
      <p><a href="#/questions">Canonical question atlas</a> · <a href={`${import.meta.env.BASE_URL || '/'}data/contributions.json`}>Download contribution bank</a></p>
    </header>
    <ScoreGuide />
    {status === 'loading' && <p role="status">Loading contributions…</p>}
    {status === 'error' && <p role="alert">Contribution data unavailable. <button onClick={() => setRetry(retry + 1)}>Retry</button></p>}
    {data && <>
      <div className="contribution-filters">
        <ScoreSort value={scoreSort} onChange={value => set({ score: value })} />
        <label>Search<input aria-label="Search" type="search" value={q} onChange={e => set({ q: e.target.value })} placeholder="Question, ID or linked atlas ID" /></label>
        <label>Bank<select aria-label="Bank" value={bank} onChange={e => set({ bank: e.target.value })}><option value="">All banks ({data.contribution_count})</option>{data.banks.map(b => <option key={b.id} value={b.id}>{b.id} ({b.count})</option>)}</select></label>
        <label>Original project area<select aria-label="Original project area" value={brief} onChange={e => set({ brief: e.target.value })}><option value="">All project areas</option>{briefs.map(b => <option key={b} value={b}>{b}</option>)}</select></label>
        <label>Recent activity<select aria-label="Recent activity" value={activity} onChange={e => set({ activity: e.target.value })}><option value="">All contributions</option><option value="new">New items</option><option value="tags">New project tags</option></select></label>
        <a href="#/contributions">Clear filters</a>
      </div>
      <p className="q-boundary">Badges cover the last {data.recent_days || 7} days as of {data.activity_as_of ? new Date(data.activity_as_of).toLocaleString() : 'the latest export'}. Undated items have no activity badge. “New” describes publication, not scientific novelty.</p>
      <p role="status">Showing {questions.length} of {data.contribution_count} contributions.</p>
      <div className="contribution-grid">{questions.map(item => <article className="contribution-card" key={item.id}>
        <p className="eyebrow">{item.id} · {item.owner}</p><h2>{item.title} {item.activity?.is_new && <span className="contribution-badge" title={`Published ${item.activity.added_at}`}>New</span>} {!!item.activity?.new_tags.length && <span className="contribution-badge" title="Project-area tags added in the last seven days">Tags added</span>}</h2><p>{item.question}</p>
        <p className="q-boundary">{item.status}</p><ScorePanel id={item.id} />
        <dl>{[['Prediction', item.prediction], ['Comparison', item.comparison], ['Metrics', item.metrics.join('; ')], ['Falsifier', item.falsifier], ['Confounds', item.confounds], ['Added variable / overlap', item.delta], ['Decision value', item.decision_value], ['Feasibility', item.feasibility]].filter(([,value]) => value).map(([label,value]) => <div key={label}><dt>{label}</dt><dd>{value}</dd></div>)}</dl>
        <p>Closest atlas: {item.atlas.map(id => <a className="contribution-link" key={id} href={href('/questions', { q: id })}>{id}</a>)}</p>
        {!!item.related.length && <p>Related extensions: {item.related.map(id => <a className="contribution-link" key={id} href={href('/contributions', { q: id })}>{id}</a>)}</p>}
        <p>Project areas: {item.briefs.map(id => <a className="contribution-link" key={id} href={href('/contributions', { brief: id })}>{id} {item.activity?.new_tags.includes(id) && <span className="contribution-badge" title={`Tag added ${item.activity.tags_added_at[id]}`}>New tag</span>}</a>)}</p>
        <p>Source leads: {item.sources.map(id => <a className="contribution-link" key={id} href={href('/library', { q: id })}>{id}</a>)}</p>
        <p className="q-boundary">{item.source_note}</p>
        <a href={repoFile(item.source_path)}>Original contribution record</a>
      </article>)}</div>
      {!questions.length && <p>No matching contributions. Clear filters to see all banks.</p>}
    </>}
  </div>;
}
