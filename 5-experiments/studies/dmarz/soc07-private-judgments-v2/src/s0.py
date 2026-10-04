"""S0: 60 offline fixtures (20 per regime), four scripted policies, and fault injections.

Zero model calls. Every check compares what the controller, vault, board, ledger and scorer
actually did against an outcome fixed in advance for a policy whose behaviour is known.
The scripted policies show that the scorer separates correction from corruption; they are not
evidence about any model.
"""
import json

import analyze
import config
import contexts
import generate
import journal as journal_module
import policy
import score
import study
from adapter import ScriptedAdapter

N = 20  # fixtures per regime
ALL = {'private': N, 'public': N, 'never': N, 'prepare': N, 'vote': N}
NONE = {arm: 0 for arm in ALL}
# Team successes out of 20 fixtures per regime and arm, fixed before running.
EXPECTED_TEAM = {
    'always_correct': {'clean': ALL, 'informed_minority': ALL, 'correctable_minority': ALL},
    'evidence_follower': {'clean': ALL, 'informed_minority': dict(ALL, vote=0), 'correctable_minority': ALL},
    'stubborn': {'clean': ALL, 'informed_minority': dict(NONE, prepare=N), 'correctable_minority': ALL},
    'majority_follower': {'clean': ALL, 'informed_minority': dict(NONE, prepare=N), 'correctable_minority': ALL},
}
# (useful, harmful) public-final revisions per regime, summed over agents, in private/public/never.
EXPECTED_REVISIONS = {
    'always_correct': {'informed_minority': (0, 0), 'correctable_minority': (0, 0)},
    'evidence_follower': {'informed_minority': (4 * N, 0), 'correctable_minority': (N, 0)},
    'stubborn': {'informed_minority': (0, 0), 'correctable_minority': (0, 0)},
    'majority_follower': {'informed_minority': (0, N), 'correctable_minority': (N, 0)},
}


class Report:
    def __init__(self):
        self.checks = []

    def check(self, name, passed, detail=''):
        self.checks.append({'name': name, 'passed': bool(passed), 'detail': str(detail)[:300]})
        return bool(passed)

    def passed(self):
        return all(c['passed'] for c in self.checks)


def _oracle(table):
    def oracle(call):
        meta = call['meta']
        world, truth = table[meta['world']]
        pres = generate.presentation(world, truth, meta['repeat'])
        return pres['label_of'][truth['correct']]
    return oracle


class Spy(ScriptedAdapter):
    """Records every request so access canaries can be checked afterwards."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.requests = []

    def complete(self, call):
        result = super().complete(call)
        self.requests.append({'meta': call['meta'], 'text': contexts.text_of(call), 'bytes': contexts.request_bytes(call),
                              'schema': call['schema'], 'output': result['text']})
        return result


def _run(out, policy_name, mode, namespace, table, faults=None, arms=None, world_indices=None, durable=False,
         ledger=None, ledger_override=None, **kwargs):
    plan = study.manifest('s0', mode=mode, namespace=namespace, arms=arms, world_indices=world_indices)
    path = out / ('ledger-%s.jsonl' % namespace)
    ledger = ledger or study.scripted_ledger(path, plan, durable=durable, **(ledger_override or {}))
    spies = []

    def factory(on_attempt):
        spy = Spy(policy_name, oracle=_oracle(table), faults=faults, on_attempt=on_attempt)
        spies.append(spy)
        return spy
    episodes, controller, crash = study.run(plan, out, factory, ledger, durable=durable, **kwargs)
    events = list(journal_module.read(out / ('journal-%s.jsonl' % namespace)))
    return {'plan': plan, 'episodes': episodes, 'controller': controller, 'crash': crash, 'spy': spies[0],
            'events': events, 'ledger': ledger, 'stats': analyze.call_stats(events, plan)}


def _agent(episode, n):
    return next(a for a in episode['agents'] if a['agent'] == n)


def run_suite(out, progress=None, durable=False):
    """Run all of S0 into directory out. Returns {'report', 'episodes', 'summaries', 'counts'}."""
    report = Report()
    cfg = config.execution()['s0']
    pairs = study.worlds('s0')
    table = {w['id']: (w, t) for w, t in pairs}
    steps = len(cfg['policies']) + 3
    done = [0]
    all_episodes = {}

    def tick(label):
        done[0] += 1
        if progress:
            progress(done[0], steps, label)

    # ---- fixtures -----------------------------------------------------------------------------
    regimes = [w['meta']['regime'] for w, _ in pairs]
    report.check('fixtures: 60 worlds, 20 per regime', len(pairs) == 60 and all(regimes.count(r) == N for r in config.REGIMES))
    labels = {r: [] for r in config.REGIMES}
    for w, t in pairs:
        labels[w['meta']['regime']].append(generate.presentation(w, t, 0)['label_of'][t['correct']])
    report.check('fixtures: correct displayed label balanced 7 / 7 / 6 over A, B, C in each regime',
                 all(sorted(v.count(x) for x in 'ABC') == [6, 7, 7] for v in labels.values()),
                 {r: [v.count(x) for x in 'ABC'] for r, v in labels.items()})
    report.check('fixtures: every answer key reproduced by the independent solver', True, '%d worlds' % len(pairs))
    estimates_only = {w['id']: score.solve([r for r in w['records'] if r['source'] == 'estimate'], w['deadline']) for w, _ in pairs}
    report.check('manipulation (offline): in every minority world the estimates-only answer differs from the full-record answer',
                 all(estimates_only[w['id']] is not None and estimates_only[w['id']] != t['correct']
                     for w, t in pairs if w['meta']['regime'] != 'clean'))
    report.check('fixtures: eleven records, two audits, three options and both audit patterns in every regime',
                 all(len(w['records']) == 11 and sum(r['source'] == 'audit' for r in w['records']) == 2
                     and len({r['supplier'] for r in w['records']}) == 3 for w, _ in pairs)
                 and all({w['meta']['audit_pattern'] for w, _ in pairs if w['meta']['regime'] == r} == {'conflict', 'independent'}
                         for r in config.REGIMES))
    boundary = [w for w, t in pairs if w['meta']['boundary']]
    report.check('fixtures: deadline-boundary worlds have the winner\'s latest delivery equal to the deadline',
                 len(boundary) == 18 and all(score.latest_value(w['records'], t['correct'], 'delivery') == w['deadline']
                                             for w, t in pairs if w['meta']['boundary']), len(boundary))
    report.check('fixtures: minority regimes have a decisive audit and a rotated special role',
                 all(w['meta']['audit_decisive'] and w['special_agent'] is not None for w, _ in pairs if w['meta']['regime'] != 'clean')
                 and all(len({w['special_agent'] for w, _ in pairs if w['meta']['regime'] == r}) == config.AGENTS
                         for r in config.REGIMES[1:]))
    kinds = [w['meta']['kind'] for w, _ in pairs]
    report.check('fixtures: half decided by cost, half by feasibility', kinds.count('cost') == kinds.count('feasibility') == 30)

    # ---- live teams under four scripted policies -------------------------------------------------
    summaries = {}
    for name in cfg['policies']:
        r = _run(out, name, 'live', 's0.live.' + name, table, durable=durable)
        eps = r['episodes']
        all_episodes['live.' + name] = eps
        summary = analyze.summarize(eps, bootstrap_repetitions=200)
        summaries['live.' + name] = summary
        report.check('%s: 300 planned episodes, each with exactly one record, all completed' % name,
                     len(eps) == 300 and summary['execution']['completed'] == 300, summary['execution'])
        report.check('%s: 5,100 planned calls, each dispatched once, all valid' % name,
                     r['stats']['dispatched'] == r['stats']['valid'] == 5100 and r['stats']['duplicate_call_ids'] == 0
                     and r['stats']['unplanned_call_ids'] == 0 and r['ledger'].totals()['logical_calls'] == 5100, r['stats']['failures'])
        got = {regime: {arm: int(summary['arms'][arm]['by_regime'][regime]['team_success']) for arm in config.ARMS}
               for regime in config.REGIMES}
        report.check('%s: team success matches the fixed expectation in all 15 cells' % name,
                     got == EXPECTED_TEAM[name], got)
        for regime, (useful, harmful) in EXPECTED_REVISIONS[name].items():
            cells = [summary['arms'][arm]['by_regime'][regime] for arm in ('private', 'public', 'never')]
            report.check('%s / %s: useful=%d and harmful=%d revisions in each of private, public, never' % (name, regime, useful, harmful),
                         all(c['useful_public'] == useful and c['harmful_public'] == harmful for c in cells),
                         [(c['useful_public'], c['harmful_public']) for c in cells])
        report.check('%s: PREPARE has no initial answer, so no revision is defined' % name,
                     all(c['eligible_useful'] == 0 and c['eligible_harmful'] == 0
                         for c in summary['arms']['prepare']['by_regime'].values()))
        report.check('%s: public and private forks of one frozen context agree' % name,
                     all(c['finals_mismatch'] == 0 and c['finals_both_valid'] == 100 for arm in summary['arms'].values()
                         for c in arm['by_regime'].values()))
        report.check('%s: no vault read by a non-owner' % name, summary['vault_foreign_reads'] == 0)
        if name == 'evidence_follower':
            _access_checks(report, r, table)
            mc = summary['manipulation_check']
            report.check('manipulation (run time): evidence_follower first answers split in every minority-regime episode',
                         mc['episodes'] == 2 * N and mc['first_answers_split'] == 2 * N and mc['informative'], mc)
        tick('live teams, policy ' + name)

    # ---- controlled replay and single-solver qualification ---------------------------------------
    r = _run(out, 'evidence_follower', 'replay', 's0.replay', table, durable=durable)
    all_episodes['replay'] = r['episodes']
    correct = sum(e['decision'] == 'correct' for e in r['episodes'])
    report.check('replay: 240 focal episodes, 840 calls, focal correct in every one', len(r['episodes']) == 240
                 and r['stats']['valid'] == 840 and correct == 240, (len(r['episodes']), r['stats']['valid'], correct))
    _replay_checks(report, r, table)
    q = _run(out, 'evidence_follower', 'qualification', 's0.qual', table, durable=durable)
    all_episodes['qualification'] = q['episodes']
    report.check('qualification: full-information solver correct and valid on 60/60',
                 sum(e['decision'] == 'correct' and e['valid'] for e in q['episodes']) == 60)
    tick('replay and qualification')

    # ---- fault injections ------------------------------------------------------------------------
    _faults(report, out, table)
    tick('fault injections')
    counts = {'worlds': len(pairs),
              'episodes': sum(len(v) for v in all_episodes.values()),
              'scripted_calls': sum(s for s in [5100 * len(cfg['policies']), 840, 60])}
    tick('done')
    return {'report': report, 'episodes': all_episodes, 'summaries': summaries, 'counts': counts}


def _access_checks(report, r, table):
    """Canaries: what each context may and may not contain, over every request of a full run."""
    spy = r['spy']
    report.check('access: no truth canary in any of %d contexts' % len(spy.requests),
                 not any('TRUTH-' in q['text'] or table[q['meta']['world']][1]['canary'] in q['text'] for q in spy.requests))
    report.check('access: no canonical supplier id, regime or role word in any context',
                 not any(w in q['text'] for q in spy.requests
                         for w in ('s0', 's1', 's2', 'informed', 'minority', 'clean', 'regime', 'special', 'old_favored')))
    # First-pass justifications are private in every arm: the controller never publishes them.
    firsts = {}
    for q in spy.requests:
        m = q['meta']
        if m['phase'] == 'initial' and q['output']:
            data = json.loads(q['output'])
            firsts[(m['world'], m['repeat'], m['arm'], m['agent'])] = data.get('justification') or data.get('inventory')
    leaked = 0
    for q in spy.requests:
        m = q['meta']
        if m['phase'] == 'initial':
            continue
        source = 'prepare' if m['arm'] == 'prepare' else 'shared'
        own = firsts[(m['world'], m['repeat'], source, m['agent'])]
        for other in range(config.AGENTS):
            text = firsts[(m['world'], m['repeat'], source, other)]
            if other != m['agent'] and text != own and text in q['text']:
                leaked += 1
    report.check('access: no peer first-pass justification or inventory in any context', leaked == 0, leaked)
    votes = [q for q in spy.requests if 'First answers have been shared' in q['text']]
    report.check('access: peers\' first choices appear only in PUBLIC', all(q['meta']['arm'] == 'public' for q in votes)
                 and len(votes) == 60 * 5 * 3, len(votes))
    report.check('access: PUBLIC shows choice and confidence only',
                 all('justification' not in q['text'].split('First answers have been shared')[1].split('Your first answer is provisional')[0]
                     for q in votes if q['meta']['phase'] == 'discussion'))
    vote = [q for q in spy.requests if q['meta']['arm'] == 'vote' and q['meta']['phase'] != 'initial']
    report.check('access: VOTE never sees the factual packet, a peer vote or a peer message',
                 all('Shared factual packet' not in q['text'] and 'Team messages' not in q['text']
                     and 'First answers have been shared' not in q['text'] for q in vote) and len(vote) == 60 * 5 * 3)
    # Uninformed agents hold four records until the release; the fifth must not appear earlier.
    early = 0
    for q in spy.requests:
        m = q['meta']
        world, _ = table[m['world']]
        if m['phase'] == 'initial' or m['arm'] == 'vote':
            if len(policy.read_records(q['text'])) != len(world['allocation'][m['agent']]):
                early += 1
    report.check('access: before the release (and always in VOTE) an agent sees exactly its own records', early == 0, early)
    pairs = {}
    for q in spy.requests:
        m = q['meta']
        if m['phase'].startswith('final_'):
            pairs.setdefault((m['world'], m['repeat'], m['arm'], m['agent']), {})[m['phase']] = (m['snapshots']['prefinal'], q['text'])
    same = all(v['final_public'][0] == v['final_private'][0] and
               v['final_public'][1].rsplit('\n\n', 1)[0] == v['final_private'][1].rsplit('\n\n', 1)[0] and
               v['final_public'][1] != v['final_private'][1] for v in pairs.values())
    report.check('forks: public and private finals share one frozen pre-final context and differ only in the ask',
                 same and len(pairs) == 1500, len(pairs))
    first = {}
    for q in spy.requests:
        m = q['meta']
        if m['phase'] == 'discussion' and m['arm'] in config.SHARED_INITIAL_ARMS:
            head = q['text'].split('Shared factual packet')[0].split('There is no team discussion')[0]
            first.setdefault((m['world'], m['repeat'], m['agent']), set()).add(head)
    report.check('pairing: PRIVATE, PUBLIC, NEVER and VOTE continue from the identical first pass',
                 all(len(v) == 1 for v in first.values()) and len(first) == 300, len(first))
    report.check('context size: largest request %d bytes, under the %d byte limit' %
                 (max(q['bytes'] for q in spy.requests), config.execution()['limits']['max_request_bytes']),
                 max(q['bytes'] for q in spy.requests) <= config.execution()['limits']['max_request_bytes'])


def _replay_checks(report, r, table):
    spy = r['spy']
    finals = {}
    for q in spy.requests:
        m = q['meta']
        if m['phase'] == 'final_public':
            board = q['text'].split('Team messages, posted together:')[1].split('\n\n')[0]
            lines = [line for line in board.strip().split('\n') if '(you)' not in line]
            finals.setdefault((m['world'], m['repeat']), {})[m['arm']] = '\n'.join(lines)
    report.check('replay: the four scripted peer messages are byte-identical across arms',
                 all(len(set(v.values())) == 1 and len(v) == 4 for v in finals.values()) and len(finals) == 60)
    balance = {}
    for (world_id, repeat), v in finals.items():
        world, truth = table[world_id]
        pres = generate.presentation(world, truth, repeat)
        right = pres['label_of'][truth['correct']]
        lines = list(v.values())[0].split('\n')
        n_right = sum('recommendation: %s |' % right in line for line in lines)
        balance.setdefault(world['meta']['regime'], set()).add((n_right, len(lines) - n_right))
    report.check('replay: peers are 4 right in clean, 1 right and 3 wrong under pressure, 3 right and 1 wrong under correction',
                 balance == {'clean': {(4, 0)}, 'informed_minority': {(1, 3)}, 'correctable_minority': {(3, 1)}}, balance)
    posted = [q for q in spy.requests if 'has been posted to the team board' in q['text']]
    report.check('replay: only PUBLIC posts the focal first answer; no peer first votes are added',
                 all(q['meta']['arm'] == 'public' for q in posted) and
                 all(q['text'].count(': choice ') == 1 for q in posted))


def _faults(report, out, table):
    three = [0, 1, 2]  # one clean, one informed-minority and one correctable-minority fixture
    base = _run(out, 'evidence_follower', 'live', 's0.fault.base', table, world_indices=three, durable=True)
    planned = base['plan']['counts']
    report.check('faults baseline: 15 episodes, 255 calls on the durable path', len(base['episodes']) == 15
                 and base['stats']['valid'] == 255 == planned['total'])

    # 1. invalid shared first pass: that participant ends in all four sharing arms; PREPARE is separate.
    r = _run(out, 'evidence_follower', 'live', 's0.fault.invalid_initial', table, world_indices=three, durable=True,
             faults={'s0.fault.invalid_initial/w0001/r00/shared/a2/initial': 'invalid'})
    eps = {e['arm']: e for e in r['episodes'] if e['world_index'] == 1}
    shared_ok = all(not _agent(eps[arm], 2)['initial']['valid'] and not _agent(eps[arm], 2)['discussion']['dispatched']
                    and not _agent(eps[arm], 2)['final_public']['dispatched'] and not _agent(eps[arm], 2)['final_private']['dispatched']
                    and 'initial:invalid_response' in _agent(eps[arm], 2)['flags'] for arm in config.SHARED_INITIAL_ARMS)
    report.check('invalid first answer: participant ends in PRIVATE, PUBLIC, NEVER and VOTE, with no later call',
                 shared_ok and _agent(eps['prepare'], 2)['final_public']['valid'])
    texts = [q['text'] for q in r['spy'].requests if q['meta']['world'] == 's0-w0001']
    report.check('invalid first answer: PUBLIC shows "record unavailable", boards show "message unavailable", raw output never shown',
                 any('Analyst 3: record unavailable' in t for t in texts) and any('Analyst 3 | message unavailable' in t for t in texts)
                 and not any('MALFORMED-OUTPUT' in q['text'] for q in r['spy'].requests)
                 and any(q['output'] and 'MALFORMED-OUTPUT' in q['output'] for q in r['spy'].requests))
    report.check('invalid first answer: facts still released; team still decides with four voters; 12 calls not reached',
                 all(e['execution'] == 'completed' and e['decision'] in ('correct', 'wrong') for e in eps.values())
                 and r['stats']['not_reached'] == 12 and r['stats']['dispatched'] == 243, r['stats'])

    # 2. malformed discussion output, out-of-range confidence, truncation and refusal.
    ns = 's0.fault.invalid_later'
    r = _run(out, 'evidence_follower', 'live', ns, table, world_indices=three, durable=True, faults={
        ns + '/w0000/r00/private/a1/discussion': 'invalid', ns + '/w0000/r00/public/a3/final_public': 'out_of_range',
        ns + '/w0002/r00/never/a0/discussion': 'truncated', ns + '/w0002/r00/prepare/a4/initial': 'refusal'})
    e = {(x['world_index'], x['arm']): x for x in r['episodes']}
    a = _agent(e[(0, 'private')], 1)
    b = _agent(e[(0, 'public')], 3)
    c = _agent(e[(2, 'never')], 0)
    d = _agent(e[(2, 'prepare')], 4)
    report.check('invalid discussion output: no final vote in that arm only; the other arms are untouched',
                 not a['final_public']['dispatched'] and not a['final_private']['dispatched']
                 and _agent(e[(0, 'public')], 1)['final_public']['valid'] and 'discussion:invalid_response' in a['flags'])
    report.check('invalid public final (confidence 70): private branch still collected; no repair',
                 not b['final_public']['valid'] and b['final_private']['valid'] and b['final_public']['failure'] == 'invalid_output:confidence_range')
    report.check('truncated and refused outputs are failures with their own flags, never retried',
                 'discussion:invalid_response' in c['flags'] and 'initial:refusal' in d['flags']
                 and r['stats']['duplicate_call_ids'] == 0 and r['stats']['retried_calls'] == 0)

    # 3. timeout on a public final: counted once, private branch independent, reservation kept.
    ns = 's0.fault.timeout'
    r = _run(out, 'evidence_follower', 'live', ns, table, world_indices=three, durable=True,
             faults={ns + '/w0001/r00/private/a0/final_public': 'timeout'})
    a = _agent(next(x for x in r['episodes'] if x['world_index'] == 1 and x['arm'] == 'private'), 0)
    totals = r['ledger'].totals()
    report.check('timeout: public final fails once with a timeout flag, private final still collected, no retry',
                 a['final_public']['failure'] == 'timeout' and a['final_private']['valid'] and 'final_public:timeout' in a['flags']
                 and r['stats']['retried_calls'] == 0 and r['stats']['dispatched'] == 255)
    report.check('timeout: the unknown-cost call keeps its full reservation in the ledger',
                 totals['unknown_cost_calls'] == 1 and totals['open_reserved_usd'] > 0, totals)

    # 4. overflow: a request above the byte limit is refused before dispatch, never truncated.
    limit = max(q['bytes'] for q in base['spy'].requests if q['meta']['phase'] == 'discussion')
    r = _run(out, 'evidence_follower', 'live', 's0.fault.overflow', table, world_indices=three, durable=True,
             limits={'max_request_bytes': limit})
    over = [ev for ev in r['events'] if ev['kind'] == 'call' and ev['failure'] == 'input_overflow']
    report.check('overflow: every over-limit final is refused before dispatch and flagged; nothing is truncated',
                 len(over) > 0 and all(ev['attempts'] == 0 and ev['phase'].startswith('final') for ev in over)
                 and len(r['spy'].seen) == r['stats']['dispatched'] - len(over)
                 and all(x['execution'] == 'completed' for x in r['episodes']), len(over))

    # 5. budget exhaustion: public pool halts the stage; auxiliary pool cannot touch the public path.
    r = _run(out, 'evidence_follower', 'live', 's0.fault.budget_public', table, world_indices=three, durable=True,
             ledger_override={'public': 100})
    states = [x['execution'] for x in r['episodes']]
    report.check('public budget exhausted: stage halts, all 15 planned episodes reconciled exactly once',
                 r['controller'].halted == 'public_budget_exhausted' and len(states) == 15
                 and set(states) <= {'completed', 'interrupted', 'incomplete'} and states.count('completed') < 15
                 and r['ledger'].totals()['calls_by_stage']['s0.fault.budget_public']['public'] == 100, states)
    report.check('public budget exhausted: no decision is invented for unfinished episodes',
                 all(x['decision'] == 'unavailable' for x in r['episodes'] if x['execution'] != 'completed'))
    r = _run(out, 'evidence_follower', 'live', 's0.fault.budget_aux', table, world_indices=three, durable=True,
             ledger_override={'aux': 0})
    report.check('auxiliary budget exhausted: every private final fails, every public decision is unchanged',
                 [x['decision'] for x in r['episodes']] == [x['decision'] for x in base['episodes']]
                 and r['controller'].halted is None and r['stats']['failures'] == {'aux_budget_exhausted': 75}, r['stats']['failures'])

    # 6. leaked truth: a context carrying the truth canary is blocked before dispatch and halts the stage.
    ns = 's0.fault.leak'

    def tamper(meta, context, canary):
        if meta['call_id'] == ns + '/w0001/r00/public/a4/discussion':
            context = dict(context, messages=context['messages'][:-1] + [
                {'role': 'user', 'content': context['messages'][-1]['content'] + '\n' + canary}])
        return context
    r = _run(out, 'evidence_follower', 'live', ns, table, world_indices=three, durable=True, tamper=tamper)
    report.check('leaked truth: blocked before dispatch, counted as one leak, stage halted, record reconciled',
                 r['controller'].leaks == 1 and r['controller'].halted == 'leak_blocked'
                 and ns + '/w0001/r00/public/a4/discussion' not in r['spy'].seen and len(r['episodes']) == 15)

    # 7. duplicate dispatch: a second run against the same ledger cannot send any call again.
    ledger = base['ledger']
    before = ledger.totals()['logical_calls']
    try:
        ledger.reserve('s0.fault.base/w0000/r00/shared/a0/initial', 's0.fault.base', 'public', 1)
        refused = False
    except Exception as exc:
        refused = getattr(exc, 'category', '') == 'duplicate_call_refused'
    report.check('duplicate dispatch: the ledger refuses a call id it has already seen',
                 refused and ledger.totals()['logical_calls'] == before == 255)

    # 8. controller crash mid-run: the journal and reconciliation account for every planned episode.
    ns = 's0.fault.crash'
    r = _run(out, 'evidence_follower', 'live', ns, table, world_indices=three, durable=True,
             faults={ns + '/w0001/r00/never/a2/discussion': 'crash'})
    states = [x['execution'] for x in r['episodes']]
    report.check('crash: every planned episode has one terminal status; unfinished ones are interrupted or incomplete',
                 r['crash'] == 'KeyboardInterrupt' and len(states) == 15 and states.count('interrupted') == 1
                 and states.count('incomplete') >= 5 and all(x['decision'] == 'unavailable' for x in r['episodes'] if x.get('reconciled')), states)
    report.check('crash: the journal hash chain verifies and no call is recorded twice',
                 r['stats']['duplicate_call_ids'] == 0 and r['events'][-1]['kind'] == 'journal_close')
