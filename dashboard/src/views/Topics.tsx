import { useMemo, useEffect } from 'react';
import type { Dataset, Entry, KindPlural } from '../data/types';
import { DEPTH_LABEL, KINDS, KIND_LABEL, PLURAL, kindColor, teamColor, teamOf, topicName, TEAMS } from '../data/meta';
import { fmt, plural, word, Word } from '../lib/format';
import { href } from '../lib/router';
import { Dots } from '../components/EntryDrawer';
import { SCAN_MIN } from '../components/GateStrip';
import { yearOf } from '../data/derive';
import './topics.css';

interface TopicInfo {
  slug: string; name: string; total: number; counts: Record<KindPlural, number>;
  full: number; top: Entry[]; teams: Record<string, number>; recent: number;
  survey: Dataset['surveys'][number] | undefined; surveyTask: Dataset['tasks'][number] | undefined;
  gaps: string[]; scanTasks: { done: number; total: number };
}

export function Topics({ data, params }: { data: Dataset; params?: URLSearchParams }) {
  const focus = params?.get('t') ?? null;
  const info = useMemo<TopicInfo[]>(() => {
    const thisYear = new Date(data.summary.generated_at).getUTCFullYear();
    return [...data.summary.topics].sort((a, b) => b.total - a.total).map((t) => {
      const es = data.library.filter((e) => e.topics.includes(t.slug));
      const teams: Record<string, number> = {};
      for (const e of es) { const tm = teamOf(e.added_by); teams[tm] = (teams[tm] ?? 0) + 1; }
      const top = [...es].sort((a, b) => (b.relevance ?? 0) - (a.relevance ?? 0) || (b.read_depth === 'full' ? 1 : 0) - (a.read_depth === 'full' ? 1 : 0) || (yearOf(b) ?? 0) - (yearOf(a) ?? 0)).slice(0, 5);
      const counts = t.counts as Record<KindPlural, number>;
      const gaps: string[] = [];
      if (!counts.datasets) gaps.push('no datasets');
      if ((counts.code ?? 0) < 3) gaps.push(counts.code ? `only ${word(counts.code)} code ${plural(counts.code, 'repo')}` : 'no code');
      const informal = (counts.blogs ?? 0) + (counts.threads ?? 0) + (counts.talks ?? 0);
      if (informal < 2) gaps.push('almost no informal writing');
      const tasks = data.tasks.filter((x) => x.kind === 'scan' && (x.topics ?? []).includes(t.slug));
      return {
        slug: t.slug, name: t.name, total: t.total, counts, teams, top,
        full: es.filter((e) => e.read_depth === 'full' || e.read_depth === 'ran').length,
        recent: es.filter((e) => (yearOf(e) ?? 0) >= thisYear - 2).length,
        survey: data.surveys.find((s) => s.topic === t.slug || s.id === t.slug),
        surveyTask: data.tasks.find((x) => x.kind === 'survey' && (x.topics ?? []).includes(t.slug)),
        gaps, scanTasks: { done: tasks.filter((x) => x.status === 'done').length, total: tasks.length },
      };
    });
  }, [data]);

  useEffect(() => {
    if (!focus) return;
    const el = document.getElementById(`topic-${focus}`);
    if (el) setTimeout(() => el.scrollIntoView({ behavior: 'smooth', block: 'start' }), 60);
  }, [focus]);

  const maxKind = useMemo(() => Math.max(1, ...info.flatMap((t) => Object.values(t.counts))), [info]);
  const withGaps = info.filter((t) => t.gaps.length).length;
  const surveyed = info.filter((t) => t.survey).length;

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow"><span className="tick" />Topics</p>
        <h1 className="display">{Word(info.length)} research topics, <em>{word(surveyed)} with a survey</em>, {word(withGaps)} with visible gaps.</h1>
        <p className="lede">
          Each panel shows what kind of evidence the agents have found for a topic, where it is thin, and how far the topic is through the gate.
          A survey needs at least 20 cited entries including 10 papers, 3 code repositories, 2 informal sources and 5 full reads. Kind bars share one square-root scale across topics, so small counts stay visible and hatched rows mean none.
        </p>
        <nav className="toc" aria-label="Jump to topic">
          {info.map((t) => (
            <a key={t.slug} href={href('/topics', { t: t.slug })} aria-current={focus === t.slug ? 'true' : undefined}>
              {topicName(t.slug)} <span className="num faint">{fmt(t.total)}</span>
            </a>
          ))}
        </nav>
      </section>

      <section className="wrap">
        <div className="topics">
          {info.map((t) => <TopicPanel key={t.slug} t={t} maxKind={maxKind} focused={focus === t.slug} />)}
        </div>
      </section>
    </>
  );
}

function TopicPanel({ t, maxKind, focused }: { t: TopicInfo; maxKind: number; focused: boolean }) {
  const stage = t.survey?.gate.passes ? (t.survey.status === 'reviewed' ? 'Survey reviewed' : t.survey.reviewed_by.filter(Boolean).length ? 'Survey passes gate, revisions requested' : 'Survey passes gate')
    : t.survey ? 'Survey in progress' : t.surveyTask?.status === 'claimed' ? 'Survey claimed' : t.total >= SCAN_MIN ? 'Scanned, survey open' : 'Scanning';
  const stageOn = !!t.survey?.gate.passes;
  return (
    <article id={`topic-${t.slug}`} className={`topic ${focused ? 'focused' : ''}`} aria-labelledby={`th-${t.slug}`}>
      <header className="topic-h">
        <div>
          <h2 id={`th-${t.slug}`} className="h2">{topicName(t.slug)}</h2>
          {t.name.toLowerCase() !== topicName(t.slug).toLowerCase() && <p className="small muted topic-full">{t.name}</p>}
        </div>
        <div className="topic-n">
          <span className="serif num">{fmt(t.total)}</span>
          <span className="small muted">sources, {fmt(t.full)} read in full</span>
        </div>
      </header>

      <div className="topic-body">
        <div className="topic-kinds" role="table" aria-label="Sources by kind">
          {KINDS.map((k) => {
            const v = t.counts[PLURAL[k]] ?? 0;
            return (
              <a key={k} role="row" className={`kbar ${v === 0 ? 'zero' : ''}`} href={href('/library', { topic: t.slug, kind: k })}>
                <span role="cell" className="kl">{KIND_LABEL[k]}</span>
                <span role="cell" className="kt"><i style={{ width: `${Math.max(v ? 1.5 : 0, Math.sqrt(v / maxKind) * 100)}%`, background: kindColor(k) }} /></span>
                <span role="cell" className="kv num">{v === 0 ? 'none' : fmt(v)}</span>
              </a>
            );
          })}
        </div>

        <div className="topic-side">
          <div className={`stage ${stageOn ? 'on' : ''}`}>
            <span className="stage-k">Stage</span>
            <span className="stage-v">{stage}</span>
            {t.survey && !t.survey.gate.passes && t.survey.gate.missing.length > 0 && (
              <ul className="missing">{t.survey.gate.missing.slice(0, 3).map((m) => <li key={m}>{m}</li>)}</ul>
            )}
            {t.survey?.gate.passes && <span className="small muted">{fmt(t.survey.sources)} sources cited{t.survey.reviewed_by.filter(Boolean).length ? `, ${t.survey.status === 'reviewed' ? 'reviewed' : 'review filed'} by ${t.survey.reviewed_by.filter(Boolean).join(', ')}` : ''}</span>}
            {!t.survey && t.surveyTask && <span className="small muted">Task <span className="mono">{t.surveyTask.id}</span> is {t.surveyTask.status}{t.surveyTask.owner ? ` by ${t.surveyTask.owner}` : ''}</span>}
          </div>
          {t.gaps.length > 0 && (
            <div className="gaps">
              <span className="stage-k">Gaps</span>
              <span className="gaps-v">{t.gaps.join(', ')}</span>
            </div>
          )}
          <div className="who">
            <span className="stage-k">Found by</span>
            <span className="who-bar" aria-label={TEAMS.map((tm) => `${tm} ${t.teams[tm] ?? 0}`).join(', ')}>
              {TEAMS.filter((tm) => t.teams[tm]).map((tm) => <i key={tm} style={{ flex: t.teams[tm], background: teamColor(tm) }} title={`${tm}: ${t.teams[tm]}`} />)}
            </span>
            <span className="small muted">{TEAMS.filter((tm) => t.teams[tm]).map((tm) => `${tm} ${fmt(t.teams[tm])}`).join(', ')}</span>
          </div>
        </div>

        <div className="topic-top">
          <span className="stage-k">Most relevant</span>
          <ol>
            {t.top.map((e) => (
              <li key={e.id}>
                <a href={href('/library', { e: e.id, topic: t.slug })}>
                  <span className="tt">{e.title}</span>
                  <span className="tm"><Dots n={e.relevance ?? 0} /> <i className="sw round" style={{ background: kindColor(e.kind) }} /> {yearOf(e) ?? ''} {e.read_depth === 'full' ? <span>{DEPTH_LABEL.full.toLowerCase()}</span> : null}</span>
                </a>
              </li>
            ))}
          </ol>
          <a className="more small" href={href('/library', { topic: t.slug, sort: 'relevance' })}>All {fmt(t.total)} in the library</a>
        </div>
      </div>
    </article>
  );
}
