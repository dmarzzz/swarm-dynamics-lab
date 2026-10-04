"""Descriptive saved-data analysis; no inference, retries, or imputation."""
import collections
import json
import sys
from pathlib import Path


def analyze(directory):
    directory = Path(directory)
    rows = json.loads((directory / 'records.json').read_text())
    calls = json.loads((directory / 'calls.json').read_text())
    failed = {c['request_sha256'] for c in calls if c['status'] != 'completed'}
    by_arm = {}
    indexed = {}
    affected = set()
    groups = collections.defaultdict(list)
    for row in rows:
        groups[row['arm'], row['case_id']].append(row)
        indexed[row['arm'], row['case_id'], row['epoch']] = row
    for (arm, root), group in groups.items():
        prior_failure = False
        for row in sorted(group, key=lambda r: r['epoch']):
            direct = bool(failed.intersection(row['request_hashes']))
            prior_failure |= direct
            if prior_failure:
                affected.add((arm, root, row['epoch']))
    for arm in dict.fromkeys(r['arm'] for r in rows):
        selected = [r for r in rows if r['arm'] == arm]
        uncertain = [r for r in selected if (arm, r['case_id'], r['epoch']) in affected]
        fixed_correct = sum(r['correct_completion'] for r in selected if (arm, r['case_id'], r['epoch']) not in affected)
        retained = [r for r in selected if r['reason'] == 'retained_closure']
        for r in retained:
            previous = [x for x in selected if x['case_id'] == r['case_id'] and x['epoch'] < r['epoch'] and x['closure'] in ('supported', 'withdrawn')]
            assert previous and r['final'] == previous[-1]['final'] and r['checks'] == 0 and r['model_calls'] == 0
        by_arm[arm] = {
            'assigned': len(selected),
            'correct': sum(r['correct_completion'] for r in selected),
            'direct_failure_rows': sum(bool(failed.intersection(r['request_hashes'])) for r in selected),
            'failure_or_downstream_rows': len(uncertain),
            'correct_count_sensitivity_bounds': [fixed_correct, fixed_correct + len(uncertain)],
            'retained_closure_rows': len(retained),
            'retained_closures_correct': sum(r['correct_completion'] for r in retained),
            'retained_closure_checks': sum(r['checks'] for r in retained),
            'noncorrect_reasons': dict(collections.Counter(r['reason'] for r in selected if not r['correct_completion'])),
            'noncorrect_rows': [{k: r[k] for k in ('case_id','scenario','condition','direction','epoch','final','status','reason')} | {'failure_or_downstream': (arm,r['case_id'],r['epoch']) in affected} for r in selected if not r['correct_completion']],
        }
    paired = {}
    for left, right in [('symmetric-gate','original-gate'),('symmetric-gate','always-check'),('original-gate','always-check')]:
        fixed_difference = 0
        uncertain_pairs = 0
        for root, epoch in {(r['case_id'],r['epoch']) for r in rows}:
            lkey, rkey = (left,root,epoch), (right,root,epoch)
            if lkey in affected or rkey in affected:
                uncertain_pairs += 1
            else:
                fixed_difference += int(indexed[lkey]['correct_completion']) - int(indexed[rkey]['correct_completion'])
        paired[left+' minus '+right] = {'uncertain_pairs':uncertain_pairs,'difference_on_unaffected_pairs':fixed_difference,'correct_difference_bounds': [fixed_difference-uncertain_pairs,fixed_difference+uncertain_pairs]}
    result = {
        'method': 'Conservative sensitivity: each directly failed row and every later row in that same arm/root may be correct or incorrect. Unaffected rows stay fixed. Bounds are not estimates or confidence intervals; they do not replace observed outcomes. Pairwise bounds let affected pairs differ arbitrarily and therefore ignore possible shared constraints.',
        'by_arm': by_arm, 'paired': paired,
        'closure_assertions_passed': True, 'native_calls': 0,
    }
    (directory/'analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'by_arm':{k:{a:b for a,b in v.items() if a not in ('noncorrect_rows','noncorrect_reasons')} for k,v in by_arm.items()},'paired':paired}))


if __name__ == '__main__':
    analyze(sys.argv[1])
