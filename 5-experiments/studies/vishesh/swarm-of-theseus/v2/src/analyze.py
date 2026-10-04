"""Assigned-denominator summaries and independent raw-response score audit."""
import argparse
from collections import Counter
import json
from pathlib import Path


def recompute(event):
    """Independent implementation: deliberately imports neither oracle nor vote parser."""
    decoded = []
    inv = {v: k for k, v in event['commands'].items()}
    ids = {c['id'] for c in event['cases']}
    for call in event['calls']:
        raw = call['result'].get('value')
        votes = {}
        if isinstance(raw, dict) and set(raw) == {'decisions', 'notebook'} and isinstance(raw['decisions'], list):
            counts = Counter(d['id'] for d in raw['decisions'] if isinstance(d, dict) and set(d) == {'id', 'command'} and isinstance(d['id'], str))
            for d in raw['decisions']:
                if not isinstance(d, dict) or set(d) != {'id', 'command'} or not isinstance(d['id'], str): continue
                if d['id'] in ids and counts[d['id']] == 1 and isinstance(d['command'], str) and d['command'] in inv:
                    votes[d['id']] = inv[d['command']]
        decoded.append(votes)
    out = []
    for c in event['cases']:
        truth_values = []
        for key in ('rule', 'stale_rule'):
            source = event['evaluator'][key][c['service_class']]
            val = c['evidence'][source]
            truth_values.append((source if val['signal'] else 'none') if event['scenario'] == 'incident'
                                else ('ship' if val['signal'] and val['fresh'] else 'hold'))
        choices = [d[c['id']] for d in decoded if c['id'] in d]
        counts = Counter(choices)
        action = next((x for x, count in counts.items() if count >= (1 if event['kind'] == 'qualification_step' else 2)), None)
        truth, stale = truth_values
        if event['kind'] == 'qualification_step':
            out.append({'id': c['id'], 'truth': truth, 'action': action, 'correct': action == truth, 'observed': action is not None})
            continue
        out.append({'id': c['id'], 'class': c['service_class'], 'truth': truth, 'stale_truth': stale,
                    'action': action, 'valid_votes': len(choices), 'agreement': max(counts.values(), default=0) / 3,
                    'correct': action == truth, 'observed': action is not None,
                    'stale_agreement': action == stale if action is not None else None,
                    'unnecessary_check': event['scenario'] == 'incident' and action not in (None, 'none') and truth == 'none',
                    'missed_hazard': event['scenario'] == 'incident' and truth != 'none' and action != truth})
    return out


def rate(rows, expected):
    correct = sum(r['correct'] for r in rows)
    observed = sum(r['observed'] for r in rows)
    return {'assigned': expected, 'correct': correct, 'observed': observed, 'missing': expected - observed,
            'conservative_accuracy': correct / expected if expected else None,
            'observed_accuracy': correct / observed if observed else None,
            'accuracy_bounds': [correct / expected, (correct + expected - observed) / expected] if expected else [None, None]}


def summarize(root):
    root = Path(root); manifest = json.loads((root / 'manifest.json').read_text())
    events = [json.loads(p.read_text()) for p in sorted(root.glob('events/*.json'))]
    failures = Counter(); errors = Counter(); audit_errors = []
    for e in events:
        for call in e['calls']:
            if call['result'].get('error'): failures[call['result']['error']] += 1
            errors.update(call['validation_errors'])
        if recompute(e) != e['scores']:
            audit_errors.append(e['run'] + ':' + str(e['step']))
    result = {'status': 'measured_model_outputs', 'stage': manifest['stage'], 'same_author_audit': True,
              'audit_mismatches': audit_errors, 'provider_failures': dict(failures), 'validation_errors': dict(errors),
              'recorded_events': len(events), 'expected_events': sum(len(a['steps']) for a in manifest['assignments']),
              'process_compliance': 'see preflight receipts and outcomes; scientific validity is separate'}
    starts = [json.loads(p.read_text()) for p in root.glob('calls/*-started.json')]
    finishes = [json.loads(p.read_text()) for p in root.glob('calls/*-finished.json')]
    result['call_accounting'] = {
        'reserved_dispatches': len(starts), 'durable_results': len(finishes),
        'unfinished_or_ambiguous': len(starts) - len(finishes),
        'reserved_usd': sum(c['reserved_usd'] for c in starts),
        'actual_usd_with_usage': sum(c.get('actual_usd') or 0 for c in finishes),
        'usage_missing': len(starts) - sum(c.get('usage') is not None for c in finishes),
        'input_tokens_known': sum((c.get('usage') or {}).get('input_tokens', 0) for c in finishes),
        'output_tokens_known': sum((c.get('usage') or {}).get('output_tokens', 0) for c in finishes)}
    result['archive_bytes'] = {
        arm: [len(e['archive']['text'].encode()) for e in events if e.get('archive') and e['arm'] == arm]
        for arm in ('acquisition', 'rolling', 'evidence', 'frozen', 'none')}
    result['lineage_generations_at_endpoint'] = [
        {'run': e['run'], 'generations': [m['generation'] for m in e['crew_after']]}
        for e in events if e['kind'] == 'trajectory_step' and e['step'] == 9]
    if manifest['stage'].startswith('S0'):
        metrics = {}; passed = True
        for scenario in ('release', 'incident', 'migration'):
            metrics[scenario] = {}
            for arm in ('ceiling', 'learner'):
                for step in (0, 5):
                    selected = [e for e in events if e['scenario'] == scenario and e['arm'] == arm and e['step'] == step]
                    rows = [r for e in selected for r in e['scores']]
                    m = rate(rows, 12)
                    metrics[scenario][f'{arm}-{step}'] = m
                    if arm == 'ceiling' and m['conservative_accuracy'] < .90: passed = False
                    if arm == 'learner' and step == 0 and m['conservative_accuracy'] < .75: passed = False
        passed = passed and len(events) == 24 and not failures and not errors and not audit_errors
        result.update({'qualification_passed': passed, 'metrics': metrics})
    else:
        metrics = {}; contrasts = []
        for scenario in ('release', 'incident', 'migration'):
            for seed in (400, 401):
                per_arm = {}
                for arm in ('rolling', 'evidence', 'frozen', 'none'):
                    selected = [e for e in events if e['scenario'] == scenario and e['seed'] == seed and e['arm'] == arm and e['step'] >= 8]
                    rows = [r for e in selected for r in e['scores']]
                    m = rate(rows, 12)
                    m['class_A'] = rate([r for r in rows if r['class'] == 'A'], 6)
                    m['class_B'] = rate([r for r in rows if r['class'] == 'B'], 6)
                    m['stale_agreement_observed'] = (sum(r['stale_agreement'] is True for r in rows) / m['observed'] if m['observed'] else None)
                    m['unnecessary_checks'] = sum(r['unnecessary_check'] for r in rows)
                    m['missed_hazards_in_recorded_events'] = sum(r['missed_hazard'] for r in rows)
                    m['missing_entire_event_tickets'] = 12 - len(rows)
                    # Distinguish understandable old commands from valid current commands.
                    intended_correct = 0; valid_commands = 0; failures_count = 0
                    for event in selected:
                        known = {v: k for k, v in event['commands'].items()}
                        if scenario == 'migration': known.update({'console1/ship': 'ship', 'console1/hold': 'hold'})
                        for call in event['calls']:
                            failures_count += bool(call['result'].get('error'))
                            raw = call['result'].get('value')
                            ds = raw.get('decisions', []) if isinstance(raw, dict) else []
                            if not isinstance(ds, list): ds = []
                            for row in event['scores']:
                                matches = [d for d in ds if isinstance(d, dict) and d.get('id') == row['id']]
                                if len(matches) != 1: continue
                                command = matches[0].get('command')
                                if not isinstance(command, str): continue
                                valid_commands += command in event['commands'].values()
                                intended_correct += known.get(command) == row['truth']
                    m['command_validity_per_assigned_member_case'] = valid_commands / 36
                    m['intended_semantic_accuracy_per_assigned_member_case'] = intended_correct / 36
                    m['provider_failures'] = failures_count
                    per_arm[arm] = m
                metrics[f'{scenario}:{seed}'] = per_arm
                if scenario != 'migration':
                    e, r = per_arm['evidence'], per_arm['rolling']
                    contrasts.append({'world': f'{scenario}:{seed}',
                                      'conservative_difference': e['conservative_accuracy'] - r['conservative_accuracy'],
                                      'identified_without_missingness': e['missing'] == r['missing'] == 0,
                                      'bounds': [e['accuracy_bounds'][0] - r['accuracy_bounds'][1], e['accuracy_bounds'][1] - r['accuracy_bounds'][0]],
                                      'unchanged_class_difference': e['class_B']['conservative_accuracy'] - r['class_B']['conservative_accuracy']})
        primary = sum(c['conservative_difference'] for c in contrasts) / 4
        unchanged = sum(c['unchanged_class_difference'] for c in contrasts) / 4
        result.update({'metrics': metrics, 'paired_worlds': contrasts, 'primary_conservative_difference': primary,
                       'primary_bounds': [sum(c['bounds'][i] for c in contrasts) / 4 for i in (0, 1)],
                       'unchanged_class_difference': unchanged,
                       'useful_signal_threshold_met': primary >= .10 and unchanged >= -.05 and not audit_errors and all(c['identified_without_missingness'] for c in contrasts),
                       'inference': 'Four primary worlds only; descriptive, no significance or culture claim. Migration excluded.'})
    (root / 'summary.json').write_text(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('root'); a = p.parse_args()
    print(json.dumps(summarize(a.root), indent=2))
