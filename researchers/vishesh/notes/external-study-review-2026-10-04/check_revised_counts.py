"""Saved-data checks for revised-review denominators; no model/network/runtime imports."""
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[3]
NOTES = ROOT / 'researchers/vishesh/notes'
inputs = []

def read(relative):
    p = NOTES / relative
    raw = p.read_bytes()
    inputs.append({'path': str(p.relative_to(ROOT)), 'sha256': hashlib.sha256(raw).hexdigest()})
    return raw.decode()

spec = json.loads(read('decision-models/quorum-of-mirrors/spec/QM-Q1-02.json'))
receipts = {r['id']: r for r in map(json.loads, read('decision-models/quorum-of-mirrors/results/QM-Q1-02/receipts.jsonl').splitlines())}
peers = []
for a in spec['assignments']:
    if a['context'] != 'peer':
        continue
    state = a['request']['state']
    priors = state['prior_decisions']
    focal = next(p['choice'] for p in priors if p['slot'] == state['focal_slot'])
    others = [p['choice'] for p in priors if p['slot'] != state['focal_slot'] and p.get('status') == 'available']
    target = 'ONE' if sum(a['bits']) > len(a['bits']) / 2 else 'ZERO'
    assert target == a['expected']
    choice = receipts[a['id']]['response']['answers']['decision']['choice']
    peers.append({'id': a['id'], 'lineage': a['lineage'], 'focal_matches_generator': focal == target,
                  'three_others_oppose': len(others) == 3 and all(x != focal for x in others),
                  'native_opposes_supplied_focal': choice != focal, 'native_matches_peer_choice': all(choice == x for x in others)})
assert len(peers) == 8 and all(all(r[k] for k in ('focal_matches_generator', 'three_others_oppose', 'native_opposes_supplied_focal', 'native_matches_peer_choice')) for r in peers)
assert sum(r['lineage'] == 'full' for r in peers) == 4

comparison = json.loads(read('external-influence-v2/local-agents/evidence/S1/comparison.json'))
pairs = comparison['pairs']
clean = [r for r in pairs if r['assignment']['world'] == 'clean']
with_instruction = [r for r in pairs if r['assignment']['world'] in ('clean', 'instruction')]
procurement = [r for r in pairs if r['assignment']['domain'] == 'procurement']
correct = lambda rows: sum(r['historical']['evaluation']['correct'] for r in rows)
external = {'clean_correct': correct(clean), 'clean_assigned': len(clean),
            'clean_plus_instruction_correct': correct(with_instruction), 'clean_plus_instruction_assigned': len(with_instruction),
            'procurement_support_exactly_075': sum(r['historical']['evaluation']['citation_support'] == .75 for r in procurement),
            'procurement_assigned': len(procurement),
            'unchanged_target_vote_vectors': sum(r['historical']['evaluation']['target_votes_before'] == r['historical']['evaluation']['target_votes_after'] for r in pairs),
            'assigned': len(pairs)}
assert external == {'clean_correct': 13, 'clean_assigned': 15, 'clean_plus_instruction_correct': 18, 'clean_plus_instruction_assigned': 20, 'procurement_support_exactly_075': 15, 'procurement_assigned': 20, 'unchanged_target_vote_vectors': 50, 'assigned': 50}

usage = json.loads(read('phantom-coast/pc2/results/S1-A1-summary.json'))['usage_by_policy']
phantom = {'team': usage['team'], 'uniform': usage['uniform'],
           'call_ratio': usage['team']['calls'] / usage['uniform']['calls'],
           'known_cost_ratio': usage['team']['known_cost_usd'] / usage['uniform']['known_cost_usd'],
           'limit': 'One team call invalid with unresolved charge; cost ratio uses known spend, not settled total cost.'}
assert usage['team']['calls'] == 1280 and usage['uniform']['calls'] == 96

# Derive standalone calls from the actual six-case results table; the shared-prefix
# collection total is separate and must not equal the sum of these alternatives.
report = read('influence-swarms/scenario/RESULTS-D2.md')
rows = {}
for line in report.splitlines():
    if line.startswith('| '):
        cols = [x.strip() for x in line.strip('|').split('|')]
        if cols[0] in ('Generalist', 'Team with ballots'):
            rows[cols[0]] = {'acceptable': int(cols[1]), 'cases': 6, 'standalone_calls': int(cols[4]), 'standalone_cost_usd': float(cols[5].lstrip('$'))}
assert rows['Generalist']['standalone_calls'] == 24 and rows['Team with ballots']['standalone_calls'] == 54
result = {'method': 'Owning saved-data arithmetic check; not independent replication or review of private traces.',
          'inputs': inputs, 'quorum_peer_rows': peers,
          'quorum_limit': 'Prior choices were authored fixtures, not a measured earlier native turn. Partial-lineage cases remain ungraded; report copying and peer majority are confounded.',
          'external_influence_v2': external, 'phantom_pc2': phantom, 'influence_d2_standalone': rows}
output = HERE / 'revised-counts.json'
output.write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps({'status': 'pass', 'source_files': len(inputs), 'quorum_peer_cases': len(peers), 'external_paired_rows': len(pairs), 'output': str(output.relative_to(ROOT))}))
