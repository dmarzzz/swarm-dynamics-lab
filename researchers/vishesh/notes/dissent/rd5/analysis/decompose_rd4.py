"""Retrospective RD4 arithmetic only. No model, scenario constructor, or network."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parents[1] / 'rd4' / 'results' / 'combined'
ARMS = ('original-gate', 'symmetric-gate', 'always-check')
CLASSIFICATION = {
    '13e56b8640a7': 'transport_and_downstream_budget',
    '6dd7a1db979b': 'unresolved_interpretation_and_downstream_budget',
    '294ed0f1b3dc': 'recovery_not_admitted',
    'a1424d89c5a1': 'initial_build_admission_deferred',
}


def main():
    records = json.loads((SOURCE / 'records.json').read_text())
    calls = {c['request_sha256']: c for c in json.loads((SOURCE / 'calls.json').read_text())}
    summary = json.loads((SOURCE / 'summary.json').read_text())
    indexed = {(r['case_id'], r['arm'], r['epoch']): r for r in records}
    assert len(indexed) == len(records) == 576
    outcomes, selected = {}, []
    for arm in ARMS:
        rows = [r for r in records if r['arm'] == arm]
        assert len(rows) == 96
        counts = collections.Counter()
        for r in rows:
            if r['correct_completion']:
                continue
            assert r['case_id'] in CLASSIFICATION, 'Unclassified noncorrect root'
            counts[CLASSIFICATION[r['case_id']]] += 1
            selected.append({k: r[k] for k in ('case_id', 'scenario', 'arm', 'epoch', 'final', 'reason', 'status', 'checks')}
                            | {'group': CLASSIFICATION[r['case_id']],
                               'gold': r['evaluator']['gold_action'],
                               'current_before': r['actor']['current_decision'],
                               'request_hashes': r['request_hashes']})
        correct = sum(r['correct_completion'] for r in rows)
        assert correct == summary['by_arm'][arm]['correct_on_time']
        assert correct + sum(counts.values()) == 96
        outcomes[arm] = {'assigned': 96, 'correct': correct, 'noncorrect': 96 - correct,
                         'noncorrect_groups': dict(counts)}
    pairs = {}
    for left, right in (('original-gate', 'always-check'), ('symmetric-gate', 'always-check'), ('symmetric-gate', 'original-gate')):
        differences = []
        for root, epoch in sorted({(r['case_id'], r['epoch']) for r in records}):
            l, r = indexed[root, left, epoch], indexed[root, right, epoch]
            difference = int(l['correct_completion']) - int(r['correct_completion'])
            if difference:
                differences.append({'case_id': root, 'epoch': epoch, 'difference': difference,
                                    'left_action': l['final'], 'right_action': r['final'],
                                    'left_reason': l['reason'], 'right_reason': r['reason']})
        assert sum(x['difference'] for x in differences) == outcomes[left]['correct'] - outcomes[right]['correct']
        pairs[left + '_minus_' + right] = differences
    examples = []
    for root, epoch, arm in [('294ed0f1b3dc', 3, 'original-gate'), ('294ed0f1b3dc', 3, 'symmetric-gate'),
                             ('6dd7a1db979b', 0, 'always-check'), ('a1424d89c5a1', 0, 'symmetric-gate')]:
        row = indexed[root, arm, epoch]
        for key in row['request_hashes']:
            call = calls[key]
            examples.append({'case_id': root, 'epoch': epoch, 'arm': arm, 'request_sha256': key,
                             'action': call.get('checked', {}).get('action'),
                             'probabilities': call.get('checked', {}).get('probabilities'),
                             'check_record': call['request']['state'].get('check_record')})
    result = {
        'kind': 'retrospective_saved_data_decomposition',
        'new_native_calls': 0,
        'source_sha256': {name: hashlib.sha256((SOURCE/name).read_bytes()).hexdigest()
                          for name in ('records.json', 'calls.json', 'summary.json')},
        'classification_note': 'Descriptive root groups from the published post-mortem. Not counterfactual repair effects. No outcome is replaced or imputed.',
        'by_arm': outcomes, 'paired_accuracy_differences': pairs,
        'all_noncorrect_checking_rows': selected, 'selected_native_decisions': examples,
        'assertions': {'all_288_checking_rows_accounted': True, 'all_26_noncorrect_rows_classified': len(selected) == 26,
                       'paired_differences_match_summaries': True},
    }
    assert result['assertions']['all_26_noncorrect_rows_classified']
    (HERE/'rd4-failure-decomposition.json').write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'by_arm': outcomes, 'paired_accuracy_differences': pairs, 'new_native_calls': 0}))


if __name__ == '__main__':
    main()
