import { lazy, Suspense, useMemo, type ComponentType } from 'react';
import type { Dataset } from '../data/types';
import { derive } from '../data/derive';
import { HACK_START, KINDS, KIND_LABEL, PLURAL, kindColor, teamColor, topicName, TEAMS } from '../data/meta';
import { fmt, Word, word, plural, clockET, ago, parseT } from '../lib/format';
import { SourceField } from '../components/SourceField';
import { StackedArea, CompositionBar } from '../components/charts';
import { GateStrip, gateStats } from '../components/GateStrip';

// Lane G's HeroSwarm (dashboard/src/graph) mounts in the hero slot when present; SourceField is the fallback.
const heroMods = import.meta.glob<{ HeroSwarm?: ComponentType<{ onSelect?: (e: { id: string }) => void; className?: string }> }>('../graph/index.tsx');
const heroLoader = Object.values(heroMods)[0];
const HeroSwarm = heroLoader ? lazy(() => heroLoader().then((m) => ({ default: m.HeroSwarm! }))) : null;

export function Overview({ data }: { data: Dataset }) {
  const d = useMemo(() => derive(data), [data]);
  const s = data.summary;
  const topicsSorted = useMemo(() => [...s.topics].sort((a, b) => b.total - a.total), [s.topics]);
  const fieldTopics = useMemo(() => topicsSorted.map((t) => t.slug), [topicsSorted]);
  const growth = useMemo(() => d.buckets.map((b) => ({ t: b.t, values: b.byTeam })), [d.buckets]);
  const teamSeries = TEAMS.map((t) => ({ key: t, label: t, color: teamColor(t) }));
  const gs = gateStats(data);
  const researchers = new Set(data.agents.map((a) => a.team)).size;
  const fullPct = Math.round((d.fullReads / Math.max(1, s.counts.total)) * 100);
  const delta = d.lastHour - d.prevHour;
  const topKindLastHour = useMemo(() => {
    const m = new Map<string, number>();
    for (const a of d.agentsLastHour) for (const [k, v] of Object.entries(a.kinds)) m.set(k, (m.get(k) ?? 0) + (v ?? 0));
    return [...m.entries()].sort((a, b) => b[1] - a[1])[0]?.[0];
  }, [d.agentsLastHour]);
  const maxAgentN = d.agentsLastHour[0]?.n ?? 1;
  const gen = parseT(s.generated_at) ?? d.now;

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow reveal"><span className="tick" />Live from the hackathon, {clockET(gen)} ET</p>
        <h1 className="display reveal" style={{ ['--i' as string]: 1 }}>
          {Word(researchers)} researchers and <span className="n">{fmt(data.agents.length)}</span> agents have catalogued{' '}
          <span className="n">{fmt(s.counts.total)}</span> sources on swarm behaviour,{' '}
          {d.sinceStart >= s.counts.total
            ? <em>all of it in the {word(Math.max(1, Math.round((d.now - HACK_START) / 3600e3)))} hours since noon.</em>
            : <em><span className="n">{fmt(d.sinceStart)}</span> of them since noon.</em>}
        </h1>
        <p className="lede reveal" style={{ ['--i' as string]: 2 }}>
          The lab runs on one rule: no hypothesis before a prior-art survey passes a mechanical gate.
          Agents scan the literature, write surveys, review each other across teams, and only then propose experiments.
          This page reads the repository and shows where that pipeline stands.
        </p>
      </section>

      <section className="wrap reveal" style={{ ['--i' as string]: 3 }} aria-label="Every source in the library">
        {HeroSwarm ? (
          <Suspense fallback={<div className="skel" style={{ height: 360 }} />}>
            <HeroSwarm onSelect={(e) => { window.location.hash = `/library?e=${encodeURIComponent(e.id)}`; }} />
          </Suspense>
        ) : (
          <>
            <div className="hero">
              <div className="hero-field">
                <SourceField entries={data.library} times={d.entryTimes} start={d.buckets[0]?.t ?? d.first} end={d.now}
                  topics={fieldTopics} height={300} />
              </div>
              <div className="hero-key" aria-hidden="true">
                {topicsSorted.map((t) => (
                  <div key={t.slug}><span>{topicName(t.slug)}</span><b>{fmt(t.total)}</b></div>
                ))}
              </div>
            </div>
            <div className="hero-axis" aria-hidden="true">
              <span>{clockET(d.buckets[0]?.t ?? d.first)} ET{(d.buckets[0]?.t ?? 0) === HACK_START ? ', hackathon starts' : ''}</span>
                            <span>{clockET(d.now)} ET, latest export</span>
            </div>
            <div className="legend" style={{ marginTop: 10 }}>
              {KINDS.map((k) => (
                <span key={k}><i className="sw round" style={{ background: kindColor(k) }} />{KIND_LABEL[k]} <span className="muted num">{fmt(s.counts[PLURAL[k]])}</span></span>
              ))}
            </div>
            <p className="hero-caption">Each dot is one source an agent catalogued, placed by when it was added (left to right) and its primary topic (rows). Larger dots were read in full.</p>
          </>
        )}
      </section>

      <section className="wrap section">
        <div className="ledger" style={{ ['--cols' as string]: 5 }}>
          <div>
            <div className="label">Sources per hour</div>
            <div className="value">{fmt(d.perHourAvg)}</div>
            <div className="note">average since the first source, <b>{fmt(s.counts.papers)}</b> papers</div>
          </div>
          <div>
            <div className="label">Added in the last hour</div>
            <div className="value">{fmt(d.lastHour)}</div>
            <div className="note">{delta === 0 ? 'same as the hour before' : `${delta > 0 ? '+' : ''}${fmt(delta)} on the hour before`}</div>
          </div>
          <div>
            <div className="label">Read in full or run</div>
            <div className="value">{fmt(d.fullReads)}<small>{fullPct}%</small></div>
            <div className="note">the rest are abstracts and skims</div>
          </div>
          <div>
            <div className="label">Agents working</div>
            <div className="value">{fmt(d.activeAgents)}<small>of {fmt(data.agents.length)}</small></div>
            <div className="note">{fmt(s.tasks.claimed)} tasks claimed, {fmt(s.tasks.open)} open</div>
          </div>
          <div>
            <div className="label">Surveys past the gate</div>
            <div className="value">{fmt(gs.surveyPass)}<small>of {fmt(s.topics.length)} topics</small></div>
            <div className="note">{fmt(s.hypotheses)} {plural(s.hypotheses, 'hypothesis', 'hypotheses')}, {fmt(s.experiments)} {plural(s.experiments, 'experiment')}</div>
          </div>
        </div>
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div>
            <h2 className="h2">The prior-art gate</h2>
            <p className="reading">
              Within a topic, nothing moves to the next stage until the last one is done, and CI enforces it. {Word(gs.scanned)} of {word(s.topics.length)} topics have a scanned literature;{' '}
              {gs.surveyPass ? `${word(gs.surveyPass)} ${plural(gs.surveyPass, 'survey has', 'surveys have')} passed the gate` : 'no survey has passed the gate yet'}
              {gs.reviewed ? `, ${word(gs.reviewed)} cleared by another team's reviewer.` : gs.inReview ? `, and its cross-team review asked for revisions.` : '.'}
            </p>
          </div>
          <a className="more" href="#/method">Research path</a>
        </div>
        <GateStrip data={data} />
      </section>

      <section className="wrap section">
        <div className="grid-12">
          <div className="span-7">
            <div className="section-head">
              <div>
                <h2 className="h2">Producing now</h2>
                <p className="reading">
                  {d.lastHour > 0
                    ? <>{Word(d.agentsLastHour.length)} {plural(d.agentsLastHour.length, 'agent')} added {fmt(d.lastHour)} sources in the last hour{topKindLastHour ? <>, mostly {KIND_LABEL[topKindLastHour as keyof typeof KIND_LABEL].toLowerCase()}</> : null}.</>
                    : <>No new sources in the last hour. The last one landed {ago(d.now)}.</>}
                </p>
              </div>
              <a className="more" href="#/agents">All agents</a>
            </div>
            {d.agentsLastHour.length ? (
              <ul className="rows">
                {d.agentsLastHour.slice(0, 8).map((a) => (
                  <li key={a.agent} className="producer">
                    <span className="sw round" style={{ background: teamColor(a.team) }} aria-label={`team ${a.team}`} />
                    <span className="who"><span className="team">{a.team}/</span>{a.agent.split('/')[1] ?? a.agent}</span>
                    <span className="n">{fmt(a.n)}</span>
                    <div className="bar" style={{ width: `${(a.n / maxAgentN) * 100}%` }}>
                      <CompositionBar height={4} parts={KINDS.map((k) => ({ key: k, value: a.kinds[k] ?? 0, color: kindColor(k), label: KIND_LABEL[k] }))} />
                    </div>
                  </li>
                ))}
              </ul>
            ) : <p className="empty-note">Quiet hour. Agents may be writing surveys or reviews, which do not add library entries.</p>}
          </div>

          <div className="span-5">
            <div className="section-head">
              <div>
                <h2 className="h2">Waiting on a human</h2>
                <p className="reading">{d.humanAsks.length ? `${Word(d.humanAsks.length)} ${plural(d.humanAsks.length, 'item needs', 'items need')} a person, not an agent.` : 'Nothing is blocked on a person right now.'}</p>
              </div>
            </div>
            {d.humanAsks.length ? (
              <ul className="rows">
                {d.humanAsks.slice(0, 7).map((a, i) => (
                  <li key={i} className="ask">
                    <span className="k">{a.kind === 'blocked' ? 'Blocked' : a.kind === 'review' ? 'Review' : 'Task'}</span>
                    <span className="t">{a.href ? <a href={a.href} target="_blank" rel="noreferrer">{a.title}</a> : a.title}</span>
                    <span className="d">{[a.who && (a.kind === 'blocked' ? a.who : `for ${a.who}`), a.detail].filter(Boolean).join(', ')}</span>
                  </li>
                ))}
              </ul>
            ) : <p className="empty-note">Agents drop asks here by opening a task with <span className="mono">for: &lt;researcher&gt;</span>.</p>}
            <div style={{ marginTop: 28 }}>
              <h3 className="h3">Task board</h3>
              <p className="reading small" style={{ marginTop: 2 }}>{fmt(s.tasks.done)} done, {fmt(s.tasks.claimed)} claimed by an agent, {fmt(s.tasks.open)} open.</p>
              <div style={{ marginTop: 10 }}>
                <CompositionBar height={10} parts={[
                  { key: 'done', value: s.tasks.done, color: 'var(--ink-2)', label: 'Done' },
                  { key: 'claimed', value: s.tasks.claimed, color: 'var(--accent)', label: 'Claimed' },
                  { key: 'open', value: s.tasks.open, color: 'var(--rule-strong)', label: 'Open' },
                ]} />
              </div>
              <div className="legend" style={{ marginTop: 8 }}>
                <span><i className="sw" style={{ background: 'var(--ink-2)' }} />Done</span>
                <span><i className="sw" style={{ background: 'var(--accent)' }} />Claimed</span>
                <span><i className="sw" style={{ background: 'var(--rule-strong)' }} />Open</span>
              </div>
            </div>
          </div>
        </div>
      </section>


      <section className="wrap section">
        <div className="grid-12">
          <div className="span-7">
            <div className="section-head">
              <div>
                <h2 className="h2">Growth since the start</h2>
                <p className="reading">Running total of sources by the team whose agents added them.</p>
              </div>
              <a className="more" href="#/timeline">Timeline</a>
            </div>
            <StackedArea rows={growth} series={teamSeries} cumulative height={240} marker={{ t: HACK_START, label: 'Noon' }} />
            <div className="legend" style={{ marginTop: 8 }}>
              {d.teams.map((t) => (
                <span key={t.team}><i className="sw" style={{ background: teamColor(t.team) }} />{t.team} <span className="muted num">{fmt(t.entries)} sources, {t.agents} agents</span></span>
              ))}
            </div>
          </div>
          <div className="span-5">
            <div className="section-head">
              <div>
                <h2 className="h2">Coverage by topic</h2>
                <p className="reading">Mix of source kinds per topic. Gaps are flagged.</p>
              </div>
              <a className="more" href="#/topics">Topics</a>
            </div>
            <div>
              {topicsSorted.map((t) => {
                const gaps = (['datasets', 'code'] as const).filter((k) => (t.counts[k] ?? 0) === 0);
                return (
                  <a key={t.slug} className="trow" href={`#/topics?t=${t.slug}`}>
                    <span className="tn">{topicName(t.slug)}{gaps.length ? <span className="flag">no {gaps.join(' or ')}</span> : null}</span>
                    <span className="tb"><CompositionBar total={topicsSorted[0].total} height={7}
                      parts={KINDS.map((k) => ({ key: k, value: t.counts[PLURAL[k]] ?? 0, color: kindColor(k), label: KIND_LABEL[k] }))} /></span>
                    <span className="tv">{fmt(t.total)}</span>
                  </a>
                );
              })}
            </div>
          </div>
        </div>
      </section>
    </>
  );
}
