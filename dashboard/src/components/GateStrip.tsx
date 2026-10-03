import type { Dataset } from '../data/types';
import { fmt } from '../lib/format';

/** A topic counts as scanned once it has this many catalogued sources and at least one scan task done. */
export const SCAN_MIN = 20;

export function gateStats(data: Dataset) {
  const s = data.summary;
  const scanned = s.topics.filter((t) => t.total >= SCAN_MIN).length;
  const surveyPass = data.surveys.filter((x) => x.gate.passes).length;
  const surveyStarted = data.surveys.length;
  const reviewed = data.surveys.filter((x) => x.gate.passes && x.reviewed_by.filter(Boolean).length).length;
  return { scanned, surveyStarted, surveyPass, reviewed, hypotheses: s.hypotheses, experiments: s.experiments, topics: s.topics.length };
}

export function GateStrip({ data }: { data: Dataset }) {
  const g = gateStats(data);
  const steps = [
    { n: 'Scan', v: <><b>{g.scanned}</b> of {g.topics} topics with {SCAN_MIN}+ sources</>, p: g.scanned / g.topics, on: g.scanned > 0 },
    { n: 'Survey', v: <><b>{g.surveyPass}</b> passing the gate, <b>{g.reviewed}</b> reviewed</>, p: g.surveyPass / g.topics, on: g.surveyPass > 0 },
    { n: 'Hypothesis', v: g.hypotheses ? <><b>{fmt(g.hypotheses)}</b> filed against passing surveys</> : <>Opens once a survey is reviewed</>, p: g.hypotheses ? Math.min(1, g.hypotheses / g.topics) : 0, on: g.hypotheses > 0 },
    { n: 'Experiment', v: g.experiments ? <><b>{fmt(g.experiments)}</b> running or done</> : <>Needs a reviewed hypothesis</>, p: g.experiments ? Math.min(1, g.experiments / g.topics) : 0, on: g.experiments > 0 },
  ];
  return (
    <ol className="gate" style={{ listStyle: 'none', margin: 0, padding: 0 }}>
      {steps.map((st, i) => (
        <li key={st.n} className={`gate-step ${st.on ? 'on' : 'off'}`}>
          <div className="ix">0{i + 1}</div>
          <div className="nm">{st.n}</div>
          <div className="v">{st.v}</div>
          <div className="meter" aria-hidden="true"><i style={{ width: `${Math.round(st.p * 100)}%` }} /></div>
        </li>
      ))}
    </ol>
  );
}
