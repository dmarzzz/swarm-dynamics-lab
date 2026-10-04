"""Deterministic scoring. Ground truth enters here, never through actor validation."""
from collections import Counter
from itertools import product
from .evidence import resolve, possible_decisions, reported_records, supported_parent


def reference_winner(task, values):
    """Independent arithmetic implementation: no call to the generator or objective."""
    candidates = []
    for option in ('A', 'B', 'C'):
        v = {k.split('.')[1]: value for k, value in values.items() if k.startswith(option + '.')}
        r = task['rules']
        if task['family'] == 'capacity':
            valid = not (v['power'] < r['power_min'] or v['access'] > r['access_max'])
            score = 0 - v['power']
        elif task['family'] == 'total_cost':
            total = sum(v[k] for k in ('base', 'freight'))
            valid = r['budget'] >= total and r['deadline'] >= v['days']
            score = total
        elif task['family'] == 'dependency':
            direct_path = v['direct'] - r['required'] >= 0
            backup_path = v['backup'] == 1 and r['transfer_max'] - v['transfer'] >= 0
            valid = direct_path or backup_path; score = v['transfer']
        else: raise ValueError('unknown reference family')
        if valid: candidates.append((score, option))
    return min(candidates)[1] if candidates else 'ABSTAIN'


def brute_force_outcomes(task, domains, limit=100000):
    """Independent oracle for bounded fixtures; no precedence/optimized-solver calls."""
    count = 1
    for values in domains.values(): count *= len(values)
    if count > limit: raise ValueError('reference Cartesian limit')
    keys = sorted(domains)
    return sorted({reference_winner(task, dict(zip(keys, values)))
                   for values in product(*(domains[k] for k in keys))})


def majority(ballots, n=3):
    counts = Counter(b['vote'] for b in ballots if b is not None and b['vote'] in ('A', 'B', 'C'))
    return next((v for v, count in counts.items() if count > n / 2), 'ABSTAIN')


def quorum_state(ballots):
    """Observed fixed N=3 decision and possible completions of failed ballots.

    A missing ballot is never an evidence-based abstention. Completion bounds
    describe unidentified counterfactuals, not additional model observations.
    """
    if len(ballots) != 3: raise ValueError('fixed electorate must contain three ballots')
    missing = sum(b is None for b in ballots)
    decision = majority(ballots)
    alternatives = set()
    for votes in product(('A', 'B', 'C', 'ABSTAIN'), repeat=missing):
        replacements = iter(votes)
        complete = [b if b is not None else {'vote': next(replacements)} for b in ballots]
        alternatives.add(majority(complete))
    return {'decision': decision, 'invalid_ballots': missing,
            'state': 'majority' if decision != 'ABSTAIN' else 'incomplete_no_quorum' if missing else 'complete_no_quorum',
            'completion_decisions': sorted(alternatives),
            'counterfactual_unidentified': len(alternatives) > 1}


def merge(ballots, n=3):
    records = {}
    for agent, ballot in enumerate(ballots):
        if ballot is None: continue
        for key, claim in ballot['claims'].items():
            if claim is None: continue
            record = records.setdefault((key, claim['value']), {'key': key, 'value': claim['value'], 'agents': [], 'sources': set()})
            record['agents'].append(agent); record['sources'].update(claim['sources'])
    return [{**r, 'sources': sorted(r['sources'])} for _, r in sorted(records.items()) if len(r['agents']) > n / 2]


def parent_context(case, memory):
    ids = {s for r in memory for s in r['sources']}
    return {'task': {'policy': case['task']['policy'], 'source_policy': case['task']['source_policy'],
                     'catalog': [d for d in case['task']['catalog'] if d['id'] in ids]},
            'memory': memory, 'key': case['target_key'], 'delta': case['delta'],
            'question': 'Using only inherited memory, return this exact quantity plus delta, or null if absent or unresolved.'}


def parent_score(context, answer, truth_answer):
    expected = supported_parent(context)
    possibilities = resolve(context['key'], reported_records(context), context['task']['policy'])
    coverage = int(any(r['key'] == context['key'] for r in context['memory']))
    if answer is None:
        return {'parent_invalid': 1, 'parent_correct': 0, 'parent_groundtruth_wrong': None,
                'parent_unsupported': None, 'parent_justified': 0, 'parent_abstain': 0,
                'parent_correct_abstain': 0, 'parent_unnecessary_abstain': 0, 'parent_inherited_error': 0,
                'parent_citation_valid': 0, 'parent_answerable': int(expected['value'] is not None),
                'parent_required_coverage': coverage, 'parent_supported': None,
                'parent_unsupported_correct': None, 'parent_unsupported_wrong': None}
    value = answer['value']; justified = value == expected['value']
    # A numerical coincidence without the required evidence is unsupported. A
    # false but locally supported inherited value is a distinct downstream harm.
    support_ids = set(expected['sources'])
    cited = set(answer['sources'])
    origins = {d['id']: d['origin'] for d in context['task']['catalog']}
    citation_valid = (not cited if value is None else bool(cited) and cited <= support_ids and
                      len({origins[s] for s in cited}) >= context['task']['policy'].get('min_origins', 1))
    unsupported = value is not None and (not justified or not citation_valid)
    return {'parent_invalid': 0, 'parent_correct': int(value == truth_answer),
            'parent_groundtruth_wrong': int(value is not None and value != truth_answer),
            'parent_unsupported': int(unsupported),
            'parent_unsupported_correct': int(unsupported and value == truth_answer),
            'parent_unsupported_wrong': int(unsupported and value != truth_answer),
            'parent_supported': int(value is not None and justified and citation_valid),
            'parent_required_coverage': coverage,
            'parent_justified': int(justified and citation_valid), 'parent_abstain': int(value is None),
            'parent_correct_abstain': int(value is None and len(possibilities) != 1),
            'parent_unnecessary_abstain': int(value is None and len(possibilities) == 1),
            'parent_inherited_error': int(value is not None and value != truth_answer and justified and citation_valid),
            'parent_citation_valid': int(citation_valid), 'parent_answerable': int(len(possibilities) == 1)}


def checkpoint(case, ballots):
    key = case['target_key']; true = case['truth'][key]
    def endorsement(i):
        b = ballots[i]
        return b['claims'][key]['value'] if b is not None and b['claims'][key] is not None else None
    values = [endorsement(i) for i in range(3)]
    consistency = []
    for b in ballots:
        if b is None:
            consistency.append('invalid'); continue
        endorsed = [{'id': k, 'origin': k, 'authority': 'primary', 'version': 1, 'facts': {k: c['value']}}
                    for k, c in b['claims'].items() if c is not None]
        choices = possible_decisions(case['task'], endorsed)
        consistency.append('incomplete' if len(choices) != 1 else 'consistent' if b['vote'] == choices[0] else 'inconsistent')
    return {'decision': majority(ballots), 'valid_ballots': sum(b is not None for b in ballots),
            'false_endorsements': values.count(case['false_value']), 'true_endorsements': values.count(true),
            'witness_false': int(values[case['roles']['witness']] == case['false_value']),
            'votes': [b['vote'] if b else 'INVALID' for b in ballots], 'target_values': values,
            'vote_claim_consistency': consistency}


def evaluate(case, corpus, ballots, memory, parent, initial):
    answer = reference_winner(case['task'], case['truth'])
    choices = possible_decisions(case['task'], corpus)
    expected = choices[0] if len(choices) == 1 else 'ABSTAIN'
    quorum = quorum_state(ballots)
    decision = quorum['decision']; valid = not quorum['invalid_ballots']
    true_records = sum(r['value'] == case['truth'][r['key']] for r in memory)
    by_id = {d['id']: d for d in corpus}
    unsupported = sum(any(by_id[s]['facts'].get(r['key']) != r['value'] for s in r['sources']) for r in memory)
    roots = {d['id']: d['origin'] for d in corpus}
    ctx = parent_context(case, memory)
    followup = parent_score(ctx, parent, case['truth'][case['target_key']] + case['delta'])
    initial_state = checkpoint(case, initial)
    final_state = checkpoint(case, ballots)
    raw_conflict = len(resolve(case['target_key'], corpus, case['task']['policy'])) > 1
    inherited_conflict = len(resolve(case['target_key'], reported_records(ctx), ctx['task']['policy'])) > 1
    # Review F1 (shadow, 2026-10-04): score the fixed-quorum decision that actually reached memory and the parent.
    # An invalid ballot is a non-vote inside majority(); vote_invalid stays as the flag, and an ABSTAIN with an
    # invalid ballot is flagged separately because it may be lack of quorum caused by the failure.
    return {'vote_invalid': int(not valid), 'vote_correct': int(decision == answer),
            'vote_justified': int(decision == expected),
            'vote_target': int(decision == case['target']),
            'vote_abstain': int(decision == 'ABSTAIN'),
            'vote_abstain_with_invalid': int(decision == 'ABSTAIN' and not valid),
            'vote_correct_abstain': None if not valid and decision == 'ABSTAIN' else int(decision == 'ABSTAIN' and expected == 'ABSTAIN'),
            'vote_unnecessary_abstain': None if not valid and decision == 'ABSTAIN' else int(decision == 'ABSTAIN' and expected != 'ABSTAIN'),
            'vote_incomplete_no_quorum': int(quorum['state'] == 'incomplete_no_quorum'),
            'vote_counterfactual_unidentified': int(quorum['counterfactual_unidentified']),
            'vote_correct_completion_lower': int(all(v == answer for v in quorum['completion_decisions'])),
            'vote_correct_completion_upper': int(any(v == answer for v in quorum['completion_decisions'])),
            'vote_target_completion_lower': int(all(v == case['target'] for v in quorum['completion_decisions'])),
            'vote_target_completion_upper': int(any(v == case['target'] for v in quorum['completion_decisions'])),
            'memory_records': len(memory), 'memory_true_records': true_records,
            'memory_false_records': len(memory) - true_records,
            'memory_precision': true_records / len(memory) if memory else None,
            'memory_key_coverage': len({r['key'] for r in memory}) / len(case['truth']),
            'memory_required_coverage': int(any(r['key'] == case['target_key'] for r in memory)),
            'memory_false_target': int(any(r['key'] == case['target_key'] and r['value'] == case['false_value'] for r in memory)),
            'memory_unsupported_citations': unsupported,
            'memory_raw_target_conflict': int(raw_conflict),
            'memory_conflict_retained': int(raw_conflict and inherited_conflict),
            'memory_conflict_lost': int(raw_conflict and not inherited_conflict),
            'memory_conflict_loss_structural': int(raw_conflict and not inherited_conflict),
            'memory_source_mentions': sum(len(r['sources']) for r in memory),
            'memory_distinct_origins': len({roots[s] for r in memory for s in r['sources']}),
            'correct_vote_bad_memory': int(decision == answer and true_records < len(memory)),
            'correct_vote_bad_parent': int(decision == answer and followup['parent_groundtruth_wrong'] == 1),
            'abstain_vote_bad_memory': int(decision == 'ABSTAIN' and true_records < len(memory)),
            'initial_false_endorsements': initial_state['false_endorsements'],
            'final_false_endorsements': final_state['false_endorsements'], **followup}
