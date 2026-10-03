import { useMemo, useState } from 'react';
import type { Agent, Batch, Dataset } from '../data/types';
import { derive } from '../data/derive';
import { ACTIVE_STATES, TEAMS, teamColor, topicName } from '../data/meta';
import { ago, fmt, parseT, plural, Word, word } from '../lib/format';
import { Spark } from '../components/charts';
import { href } from '../lib/router';
import './agents.css';

const STATE_ORDER: Record<string, number> = { working: 0, active: 0, blocked: 1, idle: 2, done: 3, unknown: 4 };
const STATE_LABEL: Record<string, string> = { working: 'Working', blocked: 'Blocked', idle: 'Idle', done: 'Done', unknown: 'No status file' };

export function Agents({ data }: { data: Dataset }) {
  const d = useMemo(() => derive(data), [data]);
  const [teamF, setTeamF] = useState<string | null>(null);
  const [showAll, setShowAll] = useState(false);

  // Per-agent throughput on a shared 15-minute grid since the first bucket.
  const series = useMemo(() => {
    const start = d.buckets[0]?.t ?? 0;
    const n = d.buckets.length;
    const m = new Map<string, number[]>();
    for (const e of data.library) {
      const t = d.entryTimes.get(e.id);
      if (t == null) continue;
      const i = Math.min(n - 1, Math.max(0, Math.floor((t - start) / d.bucketMs)));
      const arr = m.get(e.added_by) ?? new Array(n).fill(0);
      arr[i]++;
      m.set(e.added_by, arr);
    }
    return m;
  }, [data.library, d]);
  const sparkMax = useMemo(() => Math.max(1, ...[...series.values()].flat()), [series]);

  const agents = useMemo(() => [...data.agents]
    .filter((a) => !teamF || a.team === teamF)
    .sort((a, b) => (STATE_ORDER[a.state] ?? 5) - (STATE_ORDER[b.state] ?? 5) || b.entries_added - a.entries_added), [data.agents, teamF]);
  const visible = showAll ? agents : agents.filter((a) => a.state !== 'unknown' || a.entries_added > 0).slice(0, 40);

  const batches = data.batches ?? [];
  const bcol = (s: string) => batches.filter((b) => (s === 'free' ? b.state === 'free' || b.state === 'unknown' : b.state === s));
  const free = bcol('free'), claimed = bcol('claimed'), closed = bcol('closed');
  const candTotal = batches.reduce((s, b) => s + (b.n_candidates || 0), 0);
  const candDone = closed.reduce((s, b) => s + (b.n_candidates || 0), 0);
  const bySource = useMemo(() => {
    const m = new Map<string, { free: number; claimed: number; closed: number }>();
    for (const b of batches) {
      const r = m.get(b.source) ?? { free: 0, claimed: 0, closed: 0 };
      if (b.state === 'closed') r.closed++; else if (b.state === 'claimed') r.claimed++; else r.free++;
      m.set(b.source, r);
    }
    return [...m.entries()].sort((a, b) => (b[1].free + b[1].claimed + b[1].closed) - (a[1].free + a[1].claimed + a[1].closed));
  }, [batches]);
  const unknownState = batches.length > 0 && batches.every((b) => b.state === 'unknown');

  const working = data.agents.filter((a) => ACTIVE_STATES.has(a.state)).length;
  const blocked = data.agents.filter((a) => a.state === 'blocked');

  return (
    <>
      <section className="wrap page-head">
        <p className="eyebrow"><span className="tick" />Agents and pipeline</p>
        <h1 className="display"><span className="n">{fmt(data.agents.length)}</span> agents across {word(new Set(data.agents.map((a) => a.team)).size)} teams. <em>{fmt(working)} working right now.</em></h1>
        <p className="lede">
          Each researcher runs their own agents. They coordinate only through the repository: claiming tasks with a lock file,
          pulling candidate batches from GitHub issues, and pushing every ten minutes. Nothing here is self-reported except the one-line status.
        </p>
      </section>

      <section className="wrap">
        <div className="ledger" style={{ ['--cols' as string]: 4 }}>
          {TEAMS.map((t) => {
            const tm = d.teams.find((x) => x.team === t);
            return (
              <div key={t}>
                <div className="label"><i className="sw round" style={{ background: teamColor(t) }} /> {t}</div>
                <div className="value">{fmt(tm?.entries ?? 0)}<small>sources</small></div>
                <div className="note">{tm?.agents ?? 0} {plural(tm?.agents ?? 0, 'agent')}, {tm?.active ?? 0} working</div>
              </div>
            );
          })}
          <div>
            <div className="label">Candidate batches</div>
            <div className="value">{fmt(closed.length)}<small>of {fmt(batches.length)} closed</small></div>
            <div className="note">{fmt(candDone)} of {fmt(candTotal)} candidates worked</div>
          </div>
        </div>
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div>
            <h2 className="h2">Batch board</h2>
            <p className="reading">
              Collectors (X, Apify, OpenAlex, link extraction) turn raw leads into deduplicated batches of about ten candidates, one GitHub issue each.
              Any agent claims a batch, catalogues it, and closes the issue.
              {unknownState ? ' Issue state is only available when CI has a GitHub token, so every batch shows as filed.' : ` ${Word(free.length)} free, ${word(claimed.length)} claimed, ${fmt(closed.length)} closed.`}
            </p>
          </div>
          <a className="more" href="https://github.com/dmarzzz/swarm-lab/issues?q=label%3Abatch" target="_blank" rel="noreferrer">Issues on GitHub</a>
        </div>
        <div className="board">
          <BatchCol title="Free" note="waiting for an agent" items={free} />
          <BatchCol title="Claimed" note="an agent is cataloguing" items={claimed} accent />
          <BatchCol title="Closed" note="catalogued and closed" items={closed} dim />
        </div>
        {bySource.length > 0 && (
          <div className="bysrc">
            {bySource.map(([src, r]) => (
              <div key={src} className="bysrc-row">
                <span className="mono">{src}</span>
                <span className="bysrc-bar" aria-label={`${src}: ${r.closed} closed, ${r.claimed} claimed, ${r.free} free`}>
                  {Array.from({ length: r.closed }, (_, i) => <i key={`c${i}`} className="c" />)}
                  {Array.from({ length: r.claimed }, (_, i) => <i key={`l${i}`} className="l" />)}
                  {Array.from({ length: r.free }, (_, i) => <i key={`f${i}`} className="f" />)}
                </span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className="wrap section">
        <div className="section-head">
          <div>
            <h2 className="h2">Roster</h2>
            <p className="reading">
              Sorted by state, then by sources added. Bars show sources added per 15 minutes on one shared scale, so a tall bar here is tall everywhere.
              {blocked.length ? ` ${Word(blocked.length)} ${plural(blocked.length, 'agent is', 'agents are')} blocked.` : ''}
            </p>
          </div>
          <div className="chips" role="group" aria-label="Filter by team">
            <button className="chip" aria-pressed={!teamF} onClick={() => setTeamF(null)}>All</button>
            {TEAMS.map((t) => (
              <button key={t} className="chip" aria-pressed={teamF === t} onClick={() => setTeamF(teamF === t ? null : t)}>
                <i className="sw round" style={{ background: teamColor(t) }} />{t}
              </button>
            ))}
          </div>
        </div>
        <div className="roster" role="table" aria-label="Agents">
          <div className="rrow rhead" role="row">
            <span role="columnheader">Agent</span><span role="columnheader">State</span><span role="columnheader">Doing</span>
            <span role="columnheader" className="r">Sources</span><span role="columnheader">Throughput</span><span role="columnheader" className="r">Last commit</span>
          </div>
          {visible.map((a) => <AgentRow key={a.id} a={a} now={d.now} spark={series.get(a.id)} max={sparkMax} />)}
        </div>
        {agents.length > visible.length && (
          <button className="btn-text" style={{ marginTop: 14 }} onClick={() => setShowAll(true)}>
            Show all {fmt(agents.length)} agents, including {fmt(agents.length - visible.length)} audit and helper ids without a status file
          </button>
        )}
      </section>
    </>
  );
}

function AgentRow({ a, now, spark, max }: { a: Agent; now: number; spark?: number[]; max: number }) {
  const [team, name] = a.id.split('/');
  const last = parseT(a.last_commit_at);
  const st = ACTIVE_STATES.has(a.state) ? 'working' : a.state in STATE_LABEL ? a.state : 'unknown';
  const stale = st === 'working' && last != null && now - last > 3 * 3600e3;
  return (
    <div className={`rrow st-${st}`} role="row">
      <span role="cell" className="ragent">
        <i className="sw round" style={{ background: teamColor(team) }} />
        <span className="mono"><span className="muted">{team}/</span>{name}</span>
      </span>
      <span role="cell"><span className={`state s-${st}`}>{STATE_LABEL[st]}{stale ? ', quiet 3h+' : ''}</span></span>
      <span role="cell" className="rdoing">
        {a.task ? <a className="mono rtask" href={`https://github.com/dmarzzz/swarm-lab/blob/main/tasks/${a.task}.md`} target="_blank" rel="noreferrer">{a.task}</a> : null}
        <span>{a.doing || <span className="faint">No status line</span>}</span>
      </span>
      <span role="cell" className="r num rn">{a.entries_added ? <a href={href('/library', { q: a.id })}>{fmt(a.entries_added)}</a> : <span className="faint">0</span>}</span>
      <span role="cell" className="rspark">{spark ? <Spark values={spark} maxV={max} width={140} height={22} color={teamColor(team)} /> : <span className="faint small">no sources</span>}</span>
      <span role="cell" className="r small muted">{last ? ago(last, now) : ''}</span>
    </div>
  );
}

function BatchCol({ title, note, items, accent, dim }: { title: string; note: string; items: Batch[]; accent?: boolean; dim?: boolean }) {
  const [more, setMore] = useState(false);
  const shown = more ? items : items.slice(0, 8);
  return (
    <div className={`bcol ${accent ? 'accent' : ''} ${dim ? 'dim' : ''}`}>
      <div className="bcol-h"><span className="h3">{title}</span><span className="num bcol-n">{fmt(items.length)}</span></div>
      <div className="small muted">{note}</div>
      <ul className="bcol-list">
        {shown.map((b) => (
          <li key={b.id}>
            <a href={b.url} target="_blank" rel="noreferrer">
              <span className="bsrc mono">{b.source}</span>
              <span className="btopic">{b.topic ? topicName(b.topic) : b.id}</span>
              <span className="bmeta num">{b.n_candidates} <span className="faint">#{b.number}</span></span>
            </a>
            {accent && b.assignees?.length ? <div className="bwho mono">{b.assignees.join(', ')}</div> : null}
          </li>
        ))}
        {!items.length && <li className="bempty">None</li>}
      </ul>
      {items.length > 8 && !more && <button className="btn-text" onClick={() => setMore(true)}>{fmt(items.length - 8)} more</button>}
    </div>
  );
}
