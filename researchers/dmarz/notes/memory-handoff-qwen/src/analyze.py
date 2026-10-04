"""Paired analysis of memory-handoff-qwen from saved rows. Recomputable: `chain.py verify` runs it again.

The unit is the root. Every assigned cell stays in its denominator. A failed or not-started call
has an unknown outcome bounded by 0 and 1: contrasts are reported as bounds over all assigned
roots plus the complete-case estimate with its denominator. Nothing is dropped, imputed or re-run.
"""
import math
import random

import sim
import study

PRIMARY_STATES = ('misquote', 'stale')
SEPARATE_STATES = ('copies', 'contradiction', 'false_original')
MEASURES = ('correct', 'abstain', 'inherited_error', 'other_wrong', 'supported', 'supported_wrong', 'unsupported_correct',
            'unsupported_wrong', 'correct_abstain', 'unnecessary_abstain', 'citation_valid')


def mean(values):
    values = [v for v in values if v is not None]
    return math.fsum(values) / len(values) if values else None


def wilson(k, n, z=1.959963984540054):
    if not n:
        return None
    p = k / n; denom = 1 + z * z / n; centre = (p + z * z / (2 * n)) / denom
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / denom
    return [max(0.0, centre - half), min(1.0, centre + half)]


def bootstrap(values, draws, seed):
    """95% percentile interval of the mean over whole roots. None unless every root is observed."""
    if not values or any(v is None for v in values):
        return None
    rng = random.Random(seed); n = len(values); means = []
    for _ in range(draws):
        means.append(math.fsum(values[rng.randrange(n)] for _ in range(n)) / n)
    means.sort()
    return [means[int(0.025 * draws)], means[min(draws - 1, int(0.975 * draws))]]


def observed(row, measure):
    """0 or 1 for a completed row, None (unknown) otherwise."""
    return row['evaluation'][measure] if row is not None and row['status'] == 'completed' else None


def bounds(value):
    return (value, value) if value is not None else (0, 1)


def paired(rows_by, roots, plus, minus, measure, draws, seed):
    """Root-level contrast sum(plus cells) - sum(minus cells), each side averaged over its cells.
    `plus` and `minus` are lists of (state, policy). Returns estimate, bounds and every root value."""
    out = []
    for root in roots:
        p = [observed(rows_by.get((root, s, pol)), measure) for s, pol in plus]
        m = [observed(rows_by.get((root, s, pol)), measure) for s, pol in minus]
        complete = all(v is not None for v in p + m)
        value = (math.fsum(p) / len(p) - math.fsum(m) / len(m)) if complete else None
        low = math.fsum(bounds(v)[0] for v in p) / len(p) - math.fsum(bounds(v)[1] for v in m) / len(m)
        high = math.fsum(bounds(v)[1] for v in p) / len(p) - math.fsum(bounds(v)[0] for v in m) / len(m)
        out.append({'root': root, 'value': value, 'lower': low, 'upper': high})
    values = [r['value'] for r in out]
    complete = [v for v in values if v is not None]
    return {'estimate': mean(complete), 'roots': len(complete), 'assigned_roots': len(roots),
            'bounds_all_assigned': [mean(r['lower'] for r in out), mean(r['upper'] for r in out)] if out else [None, None],
            'interval95': bootstrap(values, draws, seed),
            'negative': sum(v < 0 for v in complete), 'zero': sum(v == 0 for v in complete), 'positive': sum(v > 0 for v in complete),
            'root_values': out}


def analyze(rows):
    """`rows`: one final row per assignment (study.combine of a stage's runs). Only main-grid rows
    enter the comparison; other stages get an empty comparison with the same shape of note."""
    d = study.design(); a = d['analysis']; draws, seed = a['bootstrap_draws'], a['bootstrap_seed']
    main = [r for r in rows if r['kind'] == 'main']
    if not main:
        return {'cells': [], 'note': 'this stage has no comparison rows'}
    roots = sorted({r['root'] for r in main})
    by = {(r['root'], r['state'], r['policy']): r for r in main}
    cells = []
    for state in sim.STATES:
        for policy in sim.POLICIES:
            group = [by[(root, state, policy)] for root in roots if (root, state, policy) in by]
            done = [r for r in group if r['status'] == 'completed']
            cell = {'state': state, 'policy': policy, 'assigned': len(group), 'observed': len(done),
                    'failed': sum(r['status'] == 'failed' for r in group), 'not_started': sum(r['status'] == 'not_started' for r in group),
                    'distinct_packets': len({r['packet_hash'] for r in group})}
            for m in MEASURES:
                k = sum(r['evaluation'][m] for r in done)
                cell[m] = k
                cell[m + '_rate'] = k / len(done) if done else None
                cell[m + '_bounds'] = [k / len(group), (k + len(group) - len(done)) / len(group)] if group else [None, None]
            cells.append(cell)
    cell_of = {(c['state'], c['policy']): c for c in cells}
    primary = paired(by, roots, [(s, 'content') for s in PRIMARY_STATES], [(s, 'metadata') for s in PRIMARY_STATES],
                     'inherited_error', draws, seed)
    primary['definition'] = 'inherited error under content minus under metadata, mean of the misquote and stale states within each root'
    primary['by_state'] = {s: paired(by, roots, [(s, 'content')], [(s, 'metadata')], 'inherited_error', draws, seed) for s in PRIMARY_STATES}
    guard = {'definition': 'clean state, value equals truth plus delta', 'by_policy': {}}
    for policy in sim.POLICIES:
        c = cell_of[('clean', policy)]
        guard['by_policy'][policy] = {'assigned': c['assigned'], 'observed': c['observed'], 'correct': c['correct'], 'rate': c['correct_rate'],
                                      'wilson95': wilson(c['correct'], c['observed']), 'bounds_all_assigned': c['correct_bounds']}
    guard['content_minus_raw'] = paired(by, roots, [('clean', 'content')], [('clean', 'raw')], 'correct', draws, seed)
    guard['content_minus_metadata'] = paired(by, roots, [('clean', 'content')], [('clean', 'metadata')], 'correct', draws, seed)
    forgetting = {'definition': 'clean-memory correct completion under raw minus under reset, paired by root',
                  'raw_minus_reset': paired(by, roots, [('clean', 'raw')], [('clean', 'reset')], 'correct', draws, seed),
                  'reset_abstain_rate': mean(c['abstain_rate'] for c in cells if c['policy'] == 'reset'),
                  'reset_inherited_error': sum(c['inherited_error'] for c in cells if c['policy'] == 'reset')}
    separate = {s: {p: {m: cell_of[(s, p)][m + '_rate'] for m in ('correct', 'abstain', 'inherited_error', 'supported', 'supported_wrong',
                                                               'unsupported_correct', 'unsupported_wrong')}
                    for p in sim.POLICIES} for s in SEPARATE_STATES}
    other = {name: paired(by, roots, [(s, plus) for s in states], [(s, minus) for s in states], 'inherited_error', draws, seed)
             for name, states, plus, minus in (
                 ('metadata_minus_raw_stale', ('stale',), 'metadata', 'raw'),
                 ('metadata_minus_raw_copies', ('copies',), 'metadata', 'raw'),
                 ('content_minus_raw_misquote_stale', PRIMARY_STATES, 'content', 'raw'),
                 ('content_minus_raw_false_original', ('false_original',), 'content', 'raw'))}
    retrieval = {}
    for policy in sim.POLICIES:
        group = [r for r in main if r['policy'] == policy]
        logs = [r.get('retrieval') or {} for r in group]
        retrieval[policy] = {'assignments': len(group),
                             'registry_lookups': sum(x.get('registry_lookups', 0) for x in logs),
                             'records_retrieved': sum(x.get('records_retrieved', 0) for x in logs),
                             'bytes': sum(x.get('bytes', 0) for x in logs),
                             'seconds': math.fsum(x.get('seconds', 0) for x in logs),
                             'input_tokens': sum((r.get('accounting') or {}).get('input_tokens', 0) for r in group),
                             'output_tokens': sum((r.get('accounting') or {}).get('output_tokens', 0) for r in group),
                             'cost_usd': math.fsum((r.get('accounting') or {}).get('actual_usd', 0) for r in group)}
    return {'unit': 'root', 'roots': len(roots), 'assigned': len(main),
            'observed': sum(r['status'] == 'completed' for r in main),
            'failed': sum(r['status'] == 'failed' for r in main), 'not_started': sum(r['status'] == 'not_started' for r in main),
            'distinct_packets': len({r['packet_hash'] for r in main}),
            'primary': primary, 'utility_guard': guard, 'forgetting': forgetting, 'separate_states': separate,
            'secondary_contrasts': other, 'cells': cells, 'retrieval': retrieval,
            'scope': 'one handoff per assignment; not a multi-generation result'}


def headline(analysis):
    """The numbers reported to the hub for S1."""
    if not analysis.get('cells'):
        return {}
    g = analysis['utility_guard']['by_policy']
    out = {'inherited_error_content_minus_metadata': analysis['primary']['estimate']}
    for policy in sim.POLICIES:
        out['clean_correct_' + policy] = g[policy]['rate']
    return {k: v for k, v in out.items() if v is not None}
