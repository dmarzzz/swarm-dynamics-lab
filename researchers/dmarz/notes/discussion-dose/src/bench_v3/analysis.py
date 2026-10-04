"""Assigned-denominator summaries and paired-world descriptive contrasts."""
from collections import defaultdict


def reconcile(manifest, rows, events):
    assigned = [r['id'] for r in manifest['assignments']]
    ids = [r['id'] for r in rows]
    if len(set(assigned)) != len(assigned) or len(set(ids)) != len(ids):
        raise ValueError('duplicate episode identifiers')
    if set(ids) - set(assigned): raise ValueError('unassigned episode')
    starts = [e for e in events if e['kind'] == 'call_start']
    terminals = [e for e in events if e['kind'] in ('call_response', 'provider_failure')]
    call_ids = [e['call_id'] for e in starts]; completed_ids = [e['call_id'] for e in terminals]
    if len(set(call_ids)) != len(call_ids) or len(set(completed_ids)) != len(completed_ids):
        raise ValueError('duplicate call identifiers')
    if set(completed_ids) - set(call_ids): raise ValueError('unstarted response')
    missing_usage = [e['call_id'] for e in terminals if not all(type(e.get('usage', {}).get(k)) is int for k in ('input_tokens', 'output_tokens'))]
    return {'assigned': len(assigned), 'terminal': len(rows), 'missing': sorted(set(assigned) - set(ids)),
            'planned_calls': manifest['planned_calls'], 'started_calls': len(starts), 'terminal_calls': len(terminals),
            'physical_model_calls': sum(bool(e.get('dispatched')) for e in terminals),
            'unresolved_calls': sorted(set(call_ids) - set(completed_ids)),
            'provider_failures': sum(e['kind'] == 'provider_failure' for e in events),
            'validation_failures': sum(e['kind'] == 'validation_failure' for e in events),
            'usage_missing_calls': len(missing_usage) if manifest['scientific'] else None,
            'input_tokens': sum(e.get('usage', {}).get('input_tokens', 0) for e in terminals) if manifest['scientific'] else None,
            'output_tokens': sum(e.get('usage', {}).get('output_tokens', 0) for e in terminals) if manifest['scientific'] else None}


def contrast(assignments, rows, metric, stratum):
    by_id = {r['id']: r for r in rows}
    worlds = sorted({a['world'] for a in assignments if a['kind'] == 'swarm' and a['stratum'] == stratum})
    pairs = []
    for world in worlds:
        lower = upper = 0; missing = 0; values = {}
        for attack, arm, sign in ((True, 'board', 1), (False, 'board', -1), (True, 'private', -1), (False, 'private', 1)):
            ident = f'{world}:{int(attack)}:{arm}'
            value = by_id.get(ident, {}).get('evaluation', {}).get(metric)
            values[ident] = value
            if value is None:
                missing += 1; lower += min(0, sign); upper += max(0, sign)
            else:
                lower += sign * value; upper += sign * value
        pairs.append({'world': world, 'values': values, 'contrast': lower if missing == 0 else None,
                      'lower': lower, 'upper': upper, 'unidentified_cells': missing})
    n = len(pairs)
    return {'metric': metric, 'stratum': stratum, 'worlds': n, 'per_world': pairs,
            'mean': sum(r['contrast'] for r in pairs) / n if n and all(r['contrast'] is not None for r in pairs) else None,
            'missing_outcome_lower': sum(r['lower'] for r in pairs) / n if n else None,
            'missing_outcome_upper': sum(r['upper'] for r in pairs) / n if n else None,
            'uncertainty': 'descriptive only; no confidence interval for the six-world engineering screen'}


def summarize(manifest, rows, events):
    groups = defaultdict(list)
    assigned_groups = defaultdict(int)
    def key(a):
        return ':'.join(str(a.get(k, '')) for k in ('kind', 'stratum', 'attack', 'arm', 'state'))
    for a in manifest['assignments']: assigned_groups[key(a)] += 1
    for r in rows: groups[key(r)].append(r)
    cells = {}
    for name, n in assigned_groups.items():
        records = groups[name]
        metrics = sorted({m for r in records for m in r['evaluation']})
        cells[name] = {'assigned': n, 'terminal': len(records), 'missing': n - len(records), 'metrics': {}}
        for metric in metrics:
            values = [r['evaluation'][metric] for r in records if r['evaluation'].get(metric) is not None]
            total = sum(values)
            cells[name]['metrics'][metric] = {'sum': total, 'observed': len(values), 'assigned': n,
                                              'observed_mean': total / len(values) if values else None,
                                              'assigned_observed_sum_over_n': total / n}
    costs = defaultdict(lambda: {'input_tokens': 0, 'output_tokens': 0, 'calls': 0, 'physical_model_calls': 0, 'missing_usage': 0})
    for e in events:
        if e['kind'] not in ('call_response', 'provider_failure'): continue
        label = e['label']; group = label.rsplit(':', 1)[-1] if ':' in label else 'memory'
        costs[group]['calls'] += 1
        costs[group]['physical_model_calls'] += bool(e.get('dispatched'))
        costs[group]['missing_usage'] += int(bool(e.get('dispatched')) and not all(k in e.get('usage', {}) for k in ('input_tokens', 'output_tokens')))
        for token in ('input_tokens', 'output_tokens'): costs[group][token] += e.get('usage', {}).get(token, 0)
    for group in costs.values():
        if not manifest['scientific']:
            group['input_tokens'] = group['output_tokens'] = group['estimated_cost_usd'] = None
        else:
            rates = manifest['model_config']
            group['estimated_cost_usd'] = (group['input_tokens'] * rates['input_usd_per_million'] + group['output_tokens'] * rates['output_usd_per_million']) / 1e6
            if group['missing_usage']:
                group['observed_usage_cost_usd'] = group['estimated_cost_usd']; group['estimated_cost_usd'] = None
    return {'schema': manifest['schema'], 'scientific': manifest['scientific'],
            'reconciliation': reconcile(manifest, rows, events), 'cells': cells, 'resources': dict(costs),
            'primary': contrast(manifest['assignments'], rows, 'parent_groundtruth_wrong', 'resolvable'),
            'safety': contrast(manifest['assignments'], rows, 'parent_unsupported', 'ambiguous'),
            'interpretation': 'Scripted controls validate measurement only.' if not manifest['scientific'] else 'Exploratory engineering screen, not a powered effect estimate.'}
