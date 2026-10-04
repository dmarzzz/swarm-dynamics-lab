"""Independent retrospective references for saved S0; no provider calls."""
import hashlib
import itertools
import json
import math
from pathlib import Path

BASE = Path(__file__).resolve().parent

def require(ok, message):
    if not ok:
        raise ValueError(message)

def majority(bits):
    require(len(bits) % 2 == 1, 'majority needs odd sample')
    return 'ONE' if sum(bits) > len(bits) // 2 else 'ZERO'

def references(reports):
    require(len(reports) == 9, 'expected nine reports')
    require(len({r['report_id'] for r in reports}) == 9, 'duplicate report')
    roots = {}
    for r in reports:
        require(type(r['bit']) is int and r['bit'] in (0, 1), 'invalid bit')
        require(r['visible_root'] in ('r0', 'r1', 'r2'), 'invalid root')
        require(r['q'] in (.65, .8), 'invalid reliability')
        value = (r['bit'], r['q'])
        require(r['visible_root'] not in roots or roots[r['visible_root']] == value,
                'inconsistent descendants')
        roots[r['visible_root']] = value
    require(len(roots) == 3, 'expected three roots')
    require(len({v[1] for v in roots.values()}) == 1, 'unequal reliability')
    require([sum(r['visible_root'] == k for r in reports) for k in sorted(roots)] == [7, 1, 1],
            'unexpected multiplicities')
    return majority([r['bit'] for r in reports]), majority([v[0] for v in roots.values()])

def analyze(manifest, receipts):
    assignments = manifest['assignments']
    require(len(assignments) == len(receipts) == 32, 'expected 32 assignments and receipts')
    ids = {a['id'] for a in assignments}
    require(len(ids) == 32, 'duplicate assignment')
    require(len({r['id'] for r in receipts}) == 32, 'duplicate receipt')
    require(ids == {r['id'] for r in receipts}, 'receipt ID mismatch')
    indexed = {r['id']: r for r in receipts}
    cases = {}
    for a in assignments:
        r = indexed[a['id']]
        digest = hashlib.sha256(json.dumps(a['request'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        require(digest == a['request_sha256'] == r['request_sha256'], 'request digest mismatch')
        require(r['status'] == 'complete', 'incomplete receipt')
        reports = a['request']['state']['reports']
        naive, dedup = references(reports)
        require(dedup == a['expected'], 'frozen label mismatch')
        require(a['q'] == reports[0]['q'], 'q mismatch')
        response = r['response']
        require(response['model'] == 'typesafe/jev-1.13-20260917' and response['provider'] == 'TypeSafe', 'model drift')
        answer = response['answers']['decision']
        scores = answer['probabilities']
        require(set(scores) == {'ZERO', 'ONE', 'DEFER'}, 'invalid score keys')
        require(all(isinstance(v, (float, int)) and math.isfinite(v) and 0 <= v <= 1 for v in scores.values()), 'invalid scores')
        require(abs(sum(scores.values()) - 1) < 1e-9, 'scores do not sum to one')
        require(answer['choice'] in scores and scores[answer['choice']] == max(scores.values()), 'choice-score mismatch')
        c = cases.setdefault(a['case'], {'case': a['case'], 'q': a['q'], 'reports': reports,
                 'count_all': naive, 'count_roots': dedup, 'conflict': naive != dedup,
                 'request_sha256': digest, 'observations': []})
        require(c['request_sha256'] == digest, 'nonidentical repeat')
        c['observations'].append({'id': a['id'], 'repeat': a['repeat'], 'choice': answer['choice'],
                    'choice_scores': scores, 'correct': answer['choice'] == dedup})
    require(len(cases) == 16, 'expected 16 configurations')
    for c in cases.values():
        require(sorted(o['repeat'] for o in c['observations']) == [1, 2], 'repeat mismatch')
        c['observations'].sort(key=lambda o: o['repeat'])
    require({(c['q'], tuple(next(r['bit'] for r in c['reports'] if r['visible_root'] == k) for k in ('r0','r1','r2'))) for c in cases.values()} == set(itertools.product((.65,.8), itertools.product((0,1), repeat=3))), 'incomplete factorial')
    rows = list(cases.values())
    totals = {'calls': 32, 'configurations': 16, 'bit_patterns': 8, 'reliability_settings': 2,
              'model_correct': sum(o['correct'] for c in rows for o in c['observations']),
              'count_all_correct': sum(2 * (not c['conflict']) for c in rows), 'count_roots_correct': 32,
              'pairs_agree': sum(c['observations'][0]['choice'] == c['observations'][1]['choice'] for c in rows)}
    strata = {name: {'calls': 2*sum(c['conflict'] == flag for c in rows),
                     'model_correct': sum(o['correct'] for c in rows if c['conflict'] == flag for o in c['observations'])}
              for name, flag in [('conflict', True), ('agreement', False)]}
    changes = {}
    methods = ['model', 'count_all', 'count_roots']
    for left, right in itertools.combinations(methods, 2):
        pairs = [(o['choice'] if left == 'model' else c[left], c[right], c['count_roots']) for c in rows for o in c['observations']]
        changes[left+'->'+right] = {'choices_changed': sum(a != b for a,b,y in pairs),
                                 'corrected': sum(a != y and b == y for a,b,y in pairs),
                                 'spoiled': sum(a == y and b != y for a,b,y in pairs)}
    return {'analysis_type': 'retrospective_descriptive_reanalysis', 'new_model_calls': 0,
            'scope': 'Exact MAP labels on saved full-lineage S0 inputs; not world-truth accuracy or a randomized model comparison.',
            'totals': totals, 'strata': strata, 'paired_method_changes': changes, 'cases': rows}

def main():
    src = BASE / 'results/QM-S0-02'
    data = analyze(json.loads((src/'manifest.json').read_text()), [json.loads(s) for s in (src/'receipts.jsonl').read_text().splitlines()])
    data['input_sha256'] = {n: hashlib.sha256((src/n).read_bytes()).hexdigest() for n in ('manifest.json','receipts.jsonl')}
    out = BASE / 'analysis/iteration-3'
    out.mkdir(parents=True, exist_ok=True)
    (out/'comparisons.json').write_text(json.dumps(data, indent=2)+'\n')
    template = (BASE/'case-explorer-template.html').read_text()
    (out/'cases.html').write_text(template.replace('__DATA__', json.dumps(data).replace('<', '\\u003c')))
    print(json.dumps({k:v for k,v in data.items() if k != 'cases'}, indent=2))

if __name__ == '__main__':
    main()
