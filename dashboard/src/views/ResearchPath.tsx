import { useMemo } from 'react';
import type { Dataset } from '../data/types';
import { topicName } from '../data/meta';
import { fmt, word, Word, plural } from '../lib/format';
import { href } from '../lib/router';
import { SCAN_MIN } from '../components/GateStrip';
import './path.css';

type Cell = { state: 'done' | 'active' | 'ready' | 'locked'; label: string; sub?: string };

const STAGES = [
  { k: 'scan', n: 'Scan', d: 'Catalogue papers, code, blogs, threads, talks and datasets into the library. Each entry gets a summary, a relevance score and a read depth.' },
  { k: 'survey', n: 'Survey', d: 'Write a prior-art survey that cites at least 20 entries, 10 papers, 3 repos, 2 informal sources and 5 full reads, with a search log that shows saturation.' },
  { k: 'review', n: 'Review', d: 'An agent from a different researcher spot-checks citations, re-runs searches and files a verdict. Only a pass unlocks hypotheses.' },
  { k: 'hypothesis', n: 'Hypothesis', d: 'A falsifiable claim that cites a reviewed survey and states why the closest prior work does not already answer it.' },
  { k: 'experiment', n: 'Experiment', d: 'Protocol and metrics fixed before results, for a hypothesis another team has reviewed. Results and analysis live beside the code.' },
] as const;

export function ResearchPath({ data }: { data: Dataset }) {
  const rows = useMemo(() => [...data.summary.topics].sort((a, b) => b.total - a.total).map((t) => {
    const scanTasks = data.tasks.filter((x) => x.kind === 'scan' && (x.topics ?? []).includes(t.slug));
    const scanDone = scanTasks.filter((x) => x.status === 'done').length;
    const survey = data.surveys.find((s) => s.topic === t.slug || s.id === t.slug);
    const sTask = data.tasks.find((x) => x.kind === 'survey' && (x.topics ?? []).includes(t.slug));
    const reviewTask = data.tasks.find((x) => x.kind === 'review' && (x.topics ?? []).includes(t.slug));
    const reviewers = survey?.reviewed_by.filter(Boolean) ?? [];
    const hyps = data.hypotheses.filter((h) => (h.topics ?? []).includes(t.slug)).length;
    const exps = data.experiments.filter((h) => (h.topics ?? []).includes(t.slug)).length;
    const passes = !!survey?.gate.passes;
    const reviewPass = survey?.status === 'reviewed';

    const scan: Cell = t.total >= SCAN_MIN
      ? { state: 'done', label: fmt(t.total), sub: scanTasks.length ? `${scanDone}/${scanTasks.length} scan tasks` : 'sources' }
      : { state: 'active', label: fmt(t.total), sub: `of ${SCAN_MIN} to start` };
    const surveyCell: Cell = passes ? { state: 'done', label: 'Passes', sub: `${fmt(survey!.sources)} cited` }
      : survey ? { state: 'active', label: 'Drafting', sub: `${survey.gate.missing.length} gate ${plural(survey.gate.missing.length, 'check')} left` }
      : sTask?.status === 'claimed' ? { state: 'active', label: 'Claimed', sub: sTask.owner ?? undefined }
      : t.total >= SCAN_MIN ? { state: 'ready', label: 'Open', sub: 'ready to claim' }
      : { state: 'locked', label: 'Waiting', sub: 'on the scan' };
    const reviewCell: Cell = !passes ? { state: 'locked', label: '', sub: '' }
      : reviewers.length ? { state: reviewPass ? 'done' : 'active', label: reviewPass ? 'Passed' : 'Revise requested', sub: reviewers.join(', ') }
      : reviewTask?.status === 'claimed' ? { state: 'active', label: 'In review', sub: reviewTask.owner ?? undefined }
      : { state: 'ready', label: 'Needs reviewer', sub: 'from another team' };
    const hypCell: Cell = hyps ? { state: 'done', label: fmt(hyps), sub: plural(hyps, 'hypothesis', 'hypotheses') }
      : reviewCell.state === 'done' ? { state: 'ready', label: 'Open', sub: 'unlocked' } : { state: 'locked', label: '', sub: '' };
    const expCell: Cell = exps ? { state: 'done', label: fmt(exps), sub: plural(exps, 'experiment') }
      : hyps ? { state: 'ready', label: 'Open', sub: 'needs a reviewed hypothesis' } : { state: 'locked', label: '', sub: '' };
    return { slug: t.slug, cells: [scan, surveyCell, reviewCell, hypCell, expCell] };
  }), [data]);

  const reached = STAGES.map((_, i) => rows.filter((r) => r.cells[i].state === 'done').length);
  const inflight = STAGES.map((_, i) => rows.filter((r) => r.cells[i].state === 'active').length);
  const n = rows.length;
  const furthest = rows.reduce((m, r) => Math.max(m, r.cells.reduce((k, c, i) => (c.state === 'done' ? i + 1 : k), 0)), 0);
  const lead = rows.find((r) => r.cells.reduce((k, c, i) => (c.state === 'done' ? i + 1 : k), 0) === furthest);

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow"><span className="tick" />Research path</p>
        <h1 className="display">No hypothesis before the prior art. <em>The gate is enforced in CI.</em></h1>
        <p className="lede">
          {Word(reached[0])} of {word(n)} topics have a scanned literature. {reached[1] ? `${Word(reached[1])} ${plural(reached[1], 'has', 'have')} a survey that passes the mechanical gate` : 'No survey has passed the gate yet'}
          {lead && furthest >= 2 ? `, led by ${topicName(lead.slug)}` : ''}. Hypotheses and experiments open only after a reviewer from a different team signs off.
          This is slower than letting agents speculate, and it is the point: every claim downstream traces to sources someone read.
        </p>
      </section>

      <section className="wrap">
        <ol className="funnel" aria-label="Topics reaching each stage">
          {STAGES.map((s, i) => (
            <li key={s.k} className="fstage">
              <div className="fnum serif num">{reached[i]}<span className="muted">/{n}</span></div>
              <div className="fname"><span className="mono fix">0{i + 1}</span> {s.n}</div>
              <div className="fbar" aria-hidden="true">
                <i className="d" style={{ width: `${(reached[i] / n) * 100}%` }} />
                <i className="a" style={{ width: `${(inflight[i] / n) * 100}%` }} />
              </div>
              <p className="fdesc">{s.d}</p>
              {inflight[i] > 0 && <p className="fin small">{fmt(inflight[i])} in progress</p>}
            </li>
          ))}
        </ol>
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div>
            <h2 className="h2">Every topic, every stage</h2>
            <p className="reading">Read left to right. Filled marks are done, outlined marks are in progress or open to claim, faint marks are locked behind the previous stage.</p>
          </div>
          <div className="legend">
            <span><i className="pm done" />Done</span><span><i className="pm active" />In progress</span><span><i className="pm ready" />Open</span><span><i className="pm locked" />Locked</span>
          </div>
        </div>
        <div className="pgrid" role="table" aria-label="Stage per topic">
          <div className="prow phead" role="row">
            <span role="columnheader">Topic</span>
            {STAGES.map((s) => <span key={s.k} role="columnheader">{s.n}</span>)}
          </div>
          {rows.map((r) => (
            <div key={r.slug} className="prow" role="row">
              <a role="rowheader" className="ptopic" href={href('/topics', { t: r.slug })}>{topicName(r.slug)}</a>
              {r.cells.map((c, i) => (
                <span key={i} role="cell" className={`pcell ${c.state}`} data-stage={STAGES[i].n}>
                  <i className={`pm ${c.state}`} aria-hidden="true" />
                  <span className="pl">{c.label || (c.state === 'locked' ? <span className="sr-only">Locked</span> : null)}</span>
                  {c.sub ? <span className="ps">{c.sub}</span> : null}
                  {i < STAGES.length - 1 && <span className={`pline ${c.state === 'done' ? 'on' : ''}`} aria-hidden="true" />}
                </span>
              ))}
            </div>
          ))}
        </div>
      </section>
    </>
  );
}
