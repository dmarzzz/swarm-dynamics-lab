"""Paired analysis and completeness checks (plan section 8). Exploratory: S1 only.

Denominators are assigned units throughout. An episode that did not complete counts as a failed
team decision. Agent votes and messages are never treated as independent replicates: intervals
resample whole worlds within regime, keeping every arm and repeat of a world together.
"""
import config
import seeds

LIVE_ARMS = config.ARMS


def _rate(k, n):
    return None if not n else k / n


def _success(e):
    return 1.0 if e['decision'] == 'correct' else 0.0


def _cells(episodes, value):
    """{(regime, world): {arm: mean over repeats}} for completed-or-not assigned episodes."""
    table = {}
    for e in episodes:
        if not e.get('regime'):
            continue
        slot = table.setdefault((e['regime'], e['world']), {}).setdefault(e['arm'], [])
        slot.append(value(e))
    return {key: {arm: sum(v) / len(v) for arm, v in arms.items()} for key, arms in table.items()}


def _equal_weight(cells, f):
    """Mean of f(world cell) over worlds within regime, then equal weight across regimes."""
    per_regime = {}
    for (regime, _), cell in cells.items():
        v = f(cell)
        if v is not None:
            per_regime.setdefault(regime, []).append(v)
    means = {r: sum(v) / len(v) for r, v in per_regime.items()}
    overall = sum(means.values()) / len(means) if means else None
    return overall, means


def _bootstrap(cells, f, repetitions, seed):
    """Stratified world-cluster bootstrap: resample worlds with replacement inside each regime."""
    by_regime = {}
    for (regime, world), cell in sorted(cells.items()):
        by_regime.setdefault(regime, []).append(cell)
    rng = seeds.Stream(seed)
    draws = []
    for _ in range(repetitions):
        means = []
        for regime in sorted(by_regime):
            pool = by_regime[regime]
            values = [f(pool[rng.randbelow(len(pool))]) for _ in pool]
            values = [v for v in values if v is not None]
            if values:
                means.append(sum(values) / len(values))
        if means:
            draws.append(sum(means) / len(means))
    draws.sort()
    if not draws:
        return None
    pick = lambda q: draws[min(len(draws) - 1, max(0, int(q * len(draws))))]
    return {'low_2.5': pick(0.025), 'high_97.5': pick(0.975), 'draws': len(draws)}


def contrast(episodes, arm, reference, value=_success, repetitions=None):
    cells = _cells(episodes, value)
    diff = lambda cell: (cell[arm] - cell[reference]) if arm in cell and reference in cell else None
    overall, by_regime = _equal_weight(cells, diff)
    analysis = config.design()['analysis']
    seed = seeds.derive(config.design()['seeds']['bootstrap'], 'analysis', arm, reference, value.__name__)
    interval = _bootstrap(cells, diff, repetitions or analysis['bootstrap_repetitions'], seed)
    regimes = {}
    for regime in by_regime:
        sub = {k: v for k, v in cells.items() if k[0] == regime}
        regimes[regime] = {'difference': by_regime[regime], 'worlds': len(sub),
                           'interval': _bootstrap(sub, diff, repetitions or analysis['bootstrap_repetitions'], seed)}
    return {'arm': arm, 'reference': reference, 'difference': overall, 'interval_95': interval,
            'worlds': len(cells), 'by_regime': regimes}


def _tokens(e):
    return float(e['usage']['input_tokens'] + e['usage']['output_tokens'])


def summarize(episodes, bootstrap_repetitions=None):
    """Full reconciliation and every plan measure, for live or replay episodes of one stage."""
    assigned = len(episodes)
    scored = [e for e in episodes if e.get('regime')]
    out = {'assigned_episodes': assigned,
           'execution': {s: sum(e['execution'] == s for e in episodes) for s in ('completed', 'interrupted', 'incomplete')},
           'decisions': {d: sum(e['decision'] == d for e in episodes)
                         for d in sorted({e['decision'] for e in episodes})}}
    arms = [a for a in LIVE_ARMS if any(e['arm'] == a for e in scored)]
    table = {}
    for arm in arms:
        rows = [e for e in scored if e['arm'] == arm]
        by_regime = {}
        for regime in config.REGIMES:
            rr = [e for e in rows if e['regime'] == regime]
            if not rr:
                continue
            agents = [a for e in rr for a in e['agents']]
            pub = [a['transition_public'] for a in agents]
            prv = [a['transition_private'] for a in agents]
            both = [a for a in agents if a['finals_mismatch'] is not None]
            minority = [a for a in agents if a['special']] if regime == 'correctable_minority' else []
            eligible = [a for a in minority if a['transition_public']['eligible_useful']]
            by_regime[regime] = {
                'episodes': len(rr), 'team_success': sum(_success(e) for e in rr),
                'team_success_rate': _rate(sum(_success(e) for e in rr), len(rr)),
                'no_majority': sum(e['decision'] == 'no_majority' for e in rr),
                'unavailable': sum(e['decision'] == 'unavailable' for e in rr),
                'private_vote_success': sum(e['private_vote_decision'] == 'correct' for e in rr),
                'assigned_agent_decisions': len(agents),
                'initial_valid': sum(a['initial']['valid'] for a in agents),
                'initial_correct': sum(a['initial'].get('grade') == 'correct' for a in agents),
                'initial_wrong': sum(a['initial'].get('grade') == 'wrong' for a in agents),
                'initial_abstain': sum(a['initial'].get('grade') == 'abstain' for a in agents),
                'initial_disagreement_episodes': sum(
                    len({a['initial'].get('choice') for a in e['agents'] if a['initial'].get('choice')}) > 1 for e in rr),
                'public_final_correct': sum(a['final_public'].get('grade') == 'correct' for a in agents),
                'private_final_correct': sum(a['final_private'].get('grade') == 'correct' for a in agents),
                'harmful_public': sum(t['harmful'] for t in pub), 'eligible_harmful': sum(t['eligible_harmful'] for t in pub),
                'useful_public': sum(t['useful'] for t in pub), 'eligible_useful': sum(t['eligible_useful'] for t in pub),
                'harmful_private': sum(t['harmful'] for t in prv), 'useful_private': sum(t['useful'] for t in prv),
                'harmful_rate_public': _rate(sum(t['harmful'] for t in pub), sum(t['eligible_harmful'] for t in pub)),
                'useful_rate_public': _rate(sum(t['useful'] for t in pub), sum(t['eligible_useful'] for t in pub)),
                'transitions_public': _count(['%s>%s' % (t['from'], t['to']) for t in pub]),
                'transitions_private': _count(['%s>%s' % (t['from'], t['to']) for t in prv]),
                'finals_both_valid': len(both), 'finals_mismatch': sum(a['finals_mismatch'] for a in both),
                'designated_minority_eligible': len(eligible),
                'designated_minority_corrected': sum(a['transition_public']['useful'] for a in eligible),
                'stale_citations_discussion': sum(bool(a['discussion'].get('stale_citation')) for a in agents),
                'public_final_abstain': sum(a['final_public'].get('grade') == 'abstain' for a in agents),
            }
            if arm == 'never':
                kept = [a['kept_first_choice'] for a in agents if 'kept_first_choice' in a]
                by_regime[regime].update(never_kept_first_choice=sum(kept), never_kept_denominator=len(kept))
            if arm == 'prepare':
                audited = [a['initial']['premature_choice'] for a in agents if 'premature_choice' in a['initial']]
                by_regime[regime].update(prepare_premature_choice=sum(audited), prepare_inventories=len(audited))
        rates = [v['team_success_rate'] for v in by_regime.values()]
        table[arm] = {'episodes': len(rows), 'team_success': sum(_success(e) for e in rows),
                      'team_success_equal_weight': sum(rates) / len(rates) if rates else None,
                      'input_tokens': sum(e['usage']['input_tokens'] for e in rows),
                      'output_tokens': sum(e['usage']['output_tokens'] for e in rows),
                      'billed_usd': sum(e['usage']['billed_usd'] for e in rows),
                      'mean_decision_seconds': _rate(sum(e.get('decision_seconds', 0) for e in rows), len(rows)),
                      'deadline_failures': sum(not e.get('on_time', True) for e in rows),
                      'by_regime': by_regime}
    out['arms'] = table
    out['manipulation_check'] = manipulation_check(scored)
    out['ceiling'] = {arm: {regime: cell['team_success_rate'] for regime, cell in table[arm]['by_regime'].items()}
                      for arm in ('private', 'public') if arm in table}
    out['ceiling']['at_ceiling'] = bool(out['ceiling'].get('private')) and all(
        rate == 1.0 for arm in ('private', 'public') for rate in out['ceiling'].get(arm, {}).values())
    flags = [f for e in scored for a in e['agents'] for f in a['flags']]
    out['failure_flags'] = _count(flags)
    out['vault_foreign_reads'] = sum(e.get('vault_foreign_reads', 0) for e in scored)
    if 'private' in arms and 'public' in arms:
        out['primary'] = contrast(scored, 'private', 'public', repetitions=bootstrap_repetitions)
        cells = _cells(scored, _tokens)
        ratio = lambda cell: (cell['private'] / cell['public']) if cell.get('public') else None
        overall, _ = _equal_weight(cells, ratio)
        seed = seeds.derive(config.design()['seeds']['bootstrap'], 'analysis', 'token_ratio')
        out['token_ratio_private_over_public'] = {
            'ratio': overall, 'interval_95': _bootstrap(cells, ratio, bootstrap_repetitions or
                                                         config.design()['analysis']['bootstrap_repetitions'], seed)}
        out['secondary'] = [contrast(scored, arm, 'public', repetitions=bootstrap_repetitions)
                            for arm in arms if arm not in ('private', 'public')]
        eligible = {arm: table[arm]['by_regime'].get('correctable_minority', {}) for arm in ('private', 'public')}
        shared = eligible['public'].get('designated_minority_eligible', 0)
        out['designated_minority_guardrail'] = {
            'shared_eligible': shared,
            'private_corrected': eligible['private'].get('designated_minority_corrected', 0),
            'public_corrected': eligible['public'].get('designated_minority_corrected', 0),
            'difference': None if not shared else (eligible['private'].get('designated_minority_corrected', 0)
                                                   - eligible['public'].get('designated_minority_corrected', 0)) / shared,
            'status': 'unresolved: zero eligible' if not shared else 'descriptive'}
    return out


def manipulation_check(episodes):
    """Design v2 manipulation check: in the minority regimes the comparison has information only
    when first answers differ across agents. Share of assigned minority-regime episodes of the
    reference arm whose valid first answers are not unanimous (an incomplete or single-answer
    episode counts as unanimous, so it can only lower the share)."""
    rule = config.execution()['gates']['s1_informative']
    rows = [e for e in episodes if e.get('arm') == rule['arm'] and e.get('regime') in rule['regimes']]
    split = sum(len({a['initial'].get('choice') for a in e.get('agents', []) if a['initial'].get('choice')}) > 1
                for e in rows)
    share = _rate(split, len(rows))
    return {'arm': rule['arm'], 'regimes': rule['regimes'], 'episodes': len(rows), 'first_answers_split': split,
            'share': share, 'threshold': rule['min_first_answer_disagreement_share'],
            'informative': share is not None and share >= rule['min_first_answer_disagreement_share']}


def probe(episodes):
    """P0: exactly one assigned call; it must parse (end_turn, schema-valid) and give the keyed answer."""
    e = episodes[0] if len(episodes) == 1 else None
    if e is None:
        return {'passed': False, 'detail': 'expected_one_episode', 'episodes': len(episodes)}
    passed = bool(e.get('valid')) and e['decision'] == 'correct'
    return {'passed': passed, 'detail': 'ok' if passed else (e.get('failure') or e['decision']),
            'choice': e.get('choice'), 'correct_label': e.get('correct_label'), 'usage': e['usage']}


def _count(items):
    out = {}
    for item in items:
        out[item] = out.get(item, 0) + 1
    return dict(sorted(out.items()))


def call_stats(events, plan):
    """From journal call events: validity and failure denominators, reconciled to the planned calls.
    A planned call with no record was never reached (its participant had already failed, or the
    stage halted); that is counted, not hidden."""
    planned = {c['call_id'] for c in plan['calls']}
    calls = [e for e in events if e['kind'] == 'call']
    ids = [c['call_id'] for c in calls]
    dispatched = [c for c in calls if c['failure'] != 'not_dispatched_halt']
    valid = [c for c in dispatched if c['ok']]
    failures = _count([c['failure'].split(':')[0] for c in dispatched if c['failure']])
    budget_timeout = sum(n for k, n in failures.items()
                         if 'timeout' in k or 'budget' in k or 'exhausted' in k or 'overflow' in k or 'input_token_cap' in k)
    return {'planned_calls': len(planned), 'call_records': len(calls), 'dispatched': len(dispatched),
            'sent_to_provider': sum(c['attempts'] > 0 for c in dispatched), 'valid': len(valid),
            'transport_attempts': sum(c['attempts'] for c in calls),
            'retried_calls': sum(c['attempts'] > 1 for c in calls),
            'not_reached': len(planned - set(ids)),
            'unplanned_call_ids': len(set(ids) - planned),
            'duplicate_call_ids': len(ids) - len(set(ids)),
            'valid_rate': _rate(len(valid), len(dispatched)),
            'budget_timeout_failures': budget_timeout,
            'budget_timeout_failure_rate': _rate(budget_timeout, len(planned)),
            'failures': failures,
            'by_phase': {phase: {'dispatched': sum(c['phase'] == phase for c in dispatched),
                                 'valid': sum(c['phase'] == phase and c['ok'] for c in dispatched),
                                 'truncated': sum(c['phase'] == phase and c['failure'] == 'truncated' for c in dispatched)}
                         for phase in sorted({c['phase'] for c in dispatched})},
            'max_request_bytes': max([c['request_bytes'] for c in calls] or [0]),
            'max_input_tokens': max([c['usage'].get('input_tokens', 0) for c in calls] or [0]),
            'input_tokens': sum(c['usage'].get('input_tokens', 0) for c in calls),
            'output_tokens': sum(c['usage'].get('output_tokens', 0) for c in calls),
            'billed_usd': sum(c['billed_usd'] for c in calls)}


def qualification(episodes):
    gate = config.execution()['gates']['s1q']
    correct = sum(e['decision'] == 'correct' for e in episodes)
    valid = sum(bool(e.get('valid')) for e in episodes)
    return {'episodes': len(episodes), 'correct': correct, 'valid': valid, 'gate': gate,
            'passed': len(episodes) == gate['of'] and correct >= gate['min_correct'] and valid >= gate['min_valid']}


def s1_gate(stats, leaks, crash, halted, mode=None, summary=None):
    """Validity gate of a development stage. It never looks at the size or sign of an effect.
    For the replay it also requires clean-regime competence under the team prompts."""
    gate = config.execution()['gates']['s1']
    truncated = [v['truncated'] / v['dispatched'] for v in stats.get('by_phase', {}).values() if v['dispatched']]
    checks = {
        'parse_valid_rate': stats['valid_rate'] is not None and stats['valid_rate'] >= gate['min_parse_valid_rate'],
        'budget_timeout_failures': stats['budget_timeout_failure_rate'] is not None
        and stats['budget_timeout_failure_rate'] < gate['max_budget_timeout_failure_rate'],
        'truncation_per_phase': all(rate <= gate['max_truncated_rate_per_phase'] for rate in truncated),
        'zero_leaks': leaks <= gate['max_detected_leaks'],
        'calls_counted_once_and_planned': stats['duplicate_call_ids'] == 0 and stats['unplanned_call_ids'] == 0,
        'no_crash_or_halt': crash is None and halted is None,
    }
    if mode == 'replay':
        clean = config.execution()['gates']['s1r_clean_competence']
        cells = [summary['arms'].get(arm, {}).get('by_regime', {}).get('clean', {}) for arm in clean['arms']]
        checks['clean_competence'] = all(c.get('episodes') == clean['of'] and c.get('team_success', 0) >= clean['min_correct']
                                         for c in cells)
    if mode in config.execution()['gates']['s1_informative']['modes']:
        checks['informative'] = bool(summary and (summary.get('manipulation_check') or {}).get('informative'))
    return {'checks': checks, 'passed': all(checks.values())}
