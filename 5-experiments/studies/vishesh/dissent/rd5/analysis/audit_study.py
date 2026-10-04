"""Audit saved H5 requests, actions, state replay and all-assigned arithmetic."""
import argparse
from collections import Counter, defaultdict
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import sys
import tempfile

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'src'))
from common import digest
from rd5_cli import execute
from rd5_runtime import validate_packet

p = argparse.ArgumentParser()
p.add_argument('results', type=Path)
p.add_argument('--output', type=Path, required=True)
a = p.parse_args()
load = lambda name: json.loads((a.results/name).read_text())
packet, rows, calls, summary, manifest = [load(n) for n in ('packet.json', 'records.json', 'calls.json', 'summary.json', 'manifest.json')]
validate_packet(packet)
assert packet['stage'] == 'H5' and summary['origin'] == 'native-jev'
assert len({c['identity'] for c in calls}) == len(calls)
by_call = {c['identity']: c for c in calls}
by_row = {r['id']: r for r in rows}
assert len(by_row) == len(rows)
assert set(by_row) == {x['id'] for x in packet['assignments']}
assert all(m['status'] == 'terminal' for m in manifest)

class Saved:
    def __init__(self):
        self.calls = []
    def healthy(self):
        return True
    def resolve(self, identity, request):
        c = by_call[identity]
        assert c['status'] == 'completed' and c['request'] == request
        assert digest(request) == c['request_sha256'] == c['checked']['request_sha256']
        assert c['checked']['served_model'] == packet['served_model']
        assert digest(request) in packet['allowed'][identity]
        assert identity not in {x['identity'] for x in self.calls}
        self.calls.append(deepcopy(c))
        return c['checked']['action']

with tempfile.TemporaryDirectory() as directory:
    backend = Saved()
    replay = execute(packet, backend, Path(directory))
    assert json.loads((Path(directory)/'records.json').read_text()) == rows
    assert json.loads((Path(directory)/'manifest.json').read_text()) == manifest
    assert replay == summary and backend.calls == calls

# Separate arithmetic directly from saved actions and authored truth, without summarize().
roots = {r['id']: r for r in packet['definition']['roots']}
counts = {}
for arm in ('B0', 'B1', 'B2'):
    own = [r for r in rows if r['arm'] == arm]
    assert len(own) == 24
    correct = sum(r['status'] == 'completed' and r['action'] == roots[r['root']]['truth'][r['epoch']] for r in own)
    defer = sum(r['action'] == 'DEFER' for r in own)
    checks = sum(r['checks_after']-r['checks_before'] for r in own)
    inference = sum(r['inference_attempted'] for r in own)
    for key, value in [('correct', correct), ('defer', defer), ('physical_checks', checks), ('inference_attempts', inference)]:
        assert summary['by_arm'][arm][key] == value
    counts[arm] = {'assigned': 24, 'correct': correct, 'defer': defer, 'physical_checks': checks, 'inference_calls': inference}

# Semantic diagnostic from literal numeric fields under the declared 10..30 rule.
# This is retrospective scoring of delivered evidence, never a replacement native answer.
diagnostics = []
for call in calls:
    request = call['request']
    state = request['state']
    readings = [f['value'] for c in state['evidence_cards'] for f in c['explicit_facts'] if f['field'] == 'reading']
    expected = 'DEFER' if not readings or len(set(readings)) != 1 else ('PROCEED' if 10 <= readings[0] <= 30 else 'HOLD')
    row = by_row[call['identity']]
    diagnostics.append({'id': call['identity'], 'root': row['root'], 'arm': row['arm'], 'tick': row['tick'],
                        'decision_at': row['decision_at'], 'reading': readings[0] if readings else None,
                        'expected_from_delivered_evidence': expected, 'observed': call['checked']['action'],
                        'interpretation_correct': expected == call['checked']['action'],
                        'probabilities': call['checked']['probabilities'], 'confidence': call['checked']['confidence'],
                        'request_sha256': digest(request)})
decisive = [d for d in diagnostics if d['reading'] is not None]
misses = [d for d in decisive if not d['interpretation_correct']]
# Retrospective deterministic reference: apply the explicit numeric rule to the
# delivered card only, under the unchanged acquisition/state/resource machinery.
# This is a scripted diagnostic, not a new native cohort or a preregistered endpoint.
class NumericReference:
    def __init__(self):
        self.calls = []
    def healthy(self):
        return True
    def resolve(self, identity, request):
        values = [f['value'] for c in request['state']['evidence_cards'] for f in c['explicit_facts'] if f['field'] == 'reading']
        action = 'DEFER' if not values or len(set(values)) != 1 else ('PROCEED' if 10 <= values[0] <= 30 else 'HOLD')
        self.calls.append({'identity': identity, 'status': 'scripted_reference'})
        return action

with tempfile.TemporaryDirectory() as directory:
    reference = NumericReference()
    ref_summary = execute(packet, reference, Path(directory))
    ref_counts = {arm: ref_summary['by_arm'][arm]['correct'] for arm in ('B0','B1','B2')}
reference_diagnostic = {'origin': 'retrospective_scripted_numeric_reference_NOT_NATIVE',
                        'new_model_calls': 0, 'native_primary_result_unchanged': True,
                        'correct_by_arm': ref_counts,
                        'B2_minus_B1_correct': ref_counts['B2']-ref_counts['B1'],
                        'interpretation_related_correct_decision_shortfall': {arm: ref_counts[arm]-counts[arm]['correct'] for arm in counts},
                        'limitation': 'Exact literal numeric fields in an authored task; state machinery is shared, not an independent implementation or evidence that native repair works.'}
out = {'analysis_type': 'retrospective saved-response audit; no new model calls', 'native_rows': len(rows),
       'native_calls': len(calls), 'saved_request_and_state_replay_exact': True, 'separate_all_assigned_arithmetic_passed': True,
       'by_arm': counts, 'B2_minus_B1_correct': counts['B2']['correct']-counts['B1']['correct'],
       'B1_minus_B0_correct': counts['B1']['correct']-counts['B0']['correct'],
       'decisive_interpretations': len(decisive), 'decisive_correct': len(decisive)-len(misses),
       'decisive_misses': misses, 'all_call_diagnostics': diagnostics,
       'retrospective_reference': reference_diagnostic,
       'artifact_sha256': {n: hashlib.sha256((a.results/n).read_bytes()).hexdigest() for n in ('packet.json','calls.json','records.json','manifest.json','summary.json')}}
a.output.write_text(json.dumps(out, indent=2)+'\n')
print(json.dumps({k: v for k,v in out.items() if k not in ('all_call_diagnostics','artifact_sha256')}))
