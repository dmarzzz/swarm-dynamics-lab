"""Visible-evidence reasoning; this module never receives evaluator truth."""
from itertools import product


def resolve(key, records, policy):
    """Return supported alternatives after PUBLIC precedence, not a hidden truth test.

    Multiple copies of one origin never create independent support. A newer version
    supersedes only the same origin, then declared authority ranks apply across origins.
    Equal-rank contradictions are retained. Empty means missing/insufficient evidence.
    """
    relevant = [r for r in records if key in r['facts']]
    latest = {}
    for r in relevant:
        latest[r['origin']] = max(latest.get(r['origin'], -1), r['version'])
    relevant = [r for r in relevant if r['version'] == latest[r['origin']]]
    if not relevant:
        return {}
    rank = max(policy['ranks'][r['authority']] for r in relevant)
    relevant = [r for r in relevant if policy['ranks'][r['authority']] == rank]
    alternatives = {}
    for r in relevant:
        v = r['facts'][key]
        item = alternatives.setdefault(v, {'sources': set(), 'origins': set()})
        item['sources'].add(r['id'])
        item['origins'].add(r['origin'])
    return {v: {'sources': sorted(s['sources']), 'origins': sorted(s['origins'])}
            for v, s in sorted(alternatives.items())
            if len(s['origins']) >= policy.get('min_origins', 1)}


def objective(family, v, rules):
    """Lower scores win; None denotes an infeasible option."""
    if family == 'capacity':
        return -v['power'] if v['power'] >= rules['power_min'] and v['access'] <= rules['access_max'] else None
    if family == 'total_cost':
        return v['base'] + v['freight'] if v['base'] + v['freight'] <= rules['budget'] and v['days'] <= rules['deadline'] else None
    if family == 'dependency':
        return v['transfer'] if v['direct'] >= rules['required'] or (v['backup'] == 1 and v['transfer'] <= rules['transfer_max']) else None
    raise ValueError('unknown task family')


def domains_from_evidence(task, records):
    return {k: sorted(resolve(k, records, task['policy'])) or task['domains'][k]
            for k in task['fact_keys']}


def possible_decisions(task, records):
    """Exactly enumerate per-option states, then factor the winner constraint.

    Independence of the declared finite fields permits this factorization. It is
    checked against a separate full Cartesian reference on bounded test cases.
    """
    domains = domains_from_evidence(task, records)
    outcomes = {}
    for option in task['options']:
        keys = [k for k in task['fact_keys'] if k.startswith(option + '.')]
        outcomes[option] = {objective(task['family'], dict(zip([k.split('.')[1] for k in keys], values)), task['rules'])
                            for values in product(*(domains[k] for k in keys))}
    possible = []
    for option, scores in outcomes.items():
        for score in scores - {None}:
            if all(other == option or None in other_scores or
                   any(s is not None and (score, option) < (s, other) for s in other_scores)
                   for other, other_scores in outcomes.items()):
                possible.append(option)
                break
    if all(None in scores for scores in outcomes.values()):
        possible.append('ABSTAIN')
    return sorted(possible)


def justified_choice(task, records):
    choices = possible_decisions(task, records)
    return choices[0] if len(choices) == 1 else 'ABSTAIN'


def reported_records(context):
    """Reconstruct visible testimony, preserving document origins across copies.

    This deliberately does not verify peers' claimed values against hidden docs.
    The scorer audits those citations separately after the actor has responded.
    """
    task = context['task']
    catalog = {d['id']: d for d in task['catalog']}
    records = list(context.get('documents', []))
    messages = context.get('reports', []) + context.get('private_history', []) + context.get('board', [])
    if 'memory' in context:
        messages += [{'claims': {r['key']: {'value': r['value'], 'sources': r['sources']}}} for r in context['memory']]
    for message in messages:
        for key, claim in message.get('claims', {}).items():
            if claim is not None:
                for source in claim['sources']:
                    records.append({**catalog[source], 'facts': {key: claim['value']}})
    return records


def supported_parent(context):
    values = resolve(context['key'], reported_records(context), context['task']['policy'])
    if len(values) != 1:
        return {'value': None, 'sources': []}
    value, support = next(iter(values.items()))
    return {'value': value + context['delta'], 'sources': support['sources']}
