"""Produce planning receipts from saved Q0 requests; never dispatch model calls."""
import argparse
import hashlib
import json
from collections import Counter
from pathlib import Path

from bench_v3.evidence import possible_decisions, reported_records


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def build_receipt(run):
    manifest = json.loads((run / 'manifest.json').read_text())
    events = [json.loads(s) for s in (run / 'events.jsonl').read_text().splitlines()]
    responses = {e['call_id']: e for e in events if e['kind'] == 'call_response'}
    selected = []
    totals = Counter()
    for e in events:
        if e['kind'] != 'call_start':
            continue
        parts = e['label'].split(':')
        group = 'memory' if len(parts) == 1 else parts[-1]
        if not (group == 'memory' or (len(parts) == 3 and parts[1] == '0' and
                                     group in ('diagnostic', 'report_snapshot'))):
            continue
        response = responses[e['call_id']]
        context = e['request']['context']
        choices = None if group == 'memory' else possible_decisions(context['task'], reported_records(context))
        if group != 'memory':
            assert len(choices) == 1 and choices[0] != 'ABSTAIN'
        totals[group] += 1
        for key in ('input_tokens', 'output_tokens'):
            totals[key] += response['usage'][key]
        selected.append({'q0_call_id': e['call_id'], 'label': e['label'], 'agent': e.get('agent'),
                         'phase': e['request']['phase'], 'group': group,
                         'request_sha256': digest(e['request']), 'evidence_allowed_choices': choices})
    assert [totals[k] for k in ('diagnostic', 'report_snapshot', 'memory')] == [6, 18, 36]
    assert len({r['q0_call_id'] for r in selected}) == len(selected) == 60
    selected.sort(key=lambda r: digest(['v3-d1-a1-order-v1', r['q0_call_id']]))
    models = ['claude-haiku-4-5-20251001', 'claude-sonnet-4-6']
    schedule = []
    for index, row in enumerate(selected):
        order = models if index % 2 == 0 else list(reversed(models))
        schedule.extend({'pair': index, 'model': model, 'q0_call_id': row['q0_call_id'],
                         'request_sha256': row['request_sha256']} for model in order)
    cost = (totals['input_tokens'] + 5 * totals['output_tokens']) / 1e6
    receipt = {'status': 'planning_only_not_a_launch_manifest', 'model_calls_dispatched': 0,
               'parent_attempt': 'v3-q0-a1', 'proposed_attempt': 'v3-d1-a1',
               'q0_manifest_sha256': hashlib.sha256((run / 'manifest.json').read_bytes()).hexdigest(),
               'q0_system_hash': manifest['system_hash'], 'selected': selected, 'counts': dict(totals),
               'planned_new_calls': 120, 'models': models, 'proposed_schedule': schedule,
               'q0_subset_observed_cost_usd': round(cost, 6),
               'both_models_cost_if_same_tokens_usd': round(4 * cost, 6),
               'fresh_qualification_reserved_ids': list(range(50001, 50007)),
               'fresh_qualification_generated': False, 'holdout_opened': False}
    return receipt


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run', type=Path)
    p.add_argument('output', type=Path)
    a = p.parse_args()
    receipt = build_receipt(a.run)
    a.output.write_text(json.dumps(receipt, sort_keys=True, indent=2) + '\n')
    print(json.dumps({k: receipt[k] for k in ('status', 'model_calls_dispatched', 'planned_new_calls',
                                             'counts', 'both_models_cost_if_same_tokens_usd')}))


if __name__ == '__main__':
    main()
