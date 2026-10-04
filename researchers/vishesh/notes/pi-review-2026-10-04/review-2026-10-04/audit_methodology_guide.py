"""Read-only recomputation and mutation tests of retained guide artifacts; no runs.

All temporary mutations are disposable copies inside the review directory.
The original harness run() and validator main() are deliberately never called.
"""
import copy
import hashlib
import json
import math
from pathlib import Path
import re
import shutil
import statistics
import sys
import tempfile
from collections import Counter, defaultdict

sys.dont_write_bytecode = True
BASE = Path(__file__).resolve().parents[1]
ROOT = BASE / 'agent-experiment-guide'
REVIEW = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / 'scripts'))
import validate
import toy_harness as toy
from contracts import canonical, digest, check

def load(path):
    return json.loads(path.read_text())

def lines(path):
    return [json.loads(x) for x in path.read_text().splitlines()]

def dump(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + '\n')

def write_lines(path, values):
    path.write_text(''.join(canonical(v).decode() + '\n' for v in values))

folder = ROOT / 'examples/collective-sensing/output'
config = load(folder / 'config.resolved.json')
planned = load(folder / 'planned-runs.json')
outcomes = lines(folder / 'outcomes.jsonl')
events = lines(folder / 'events.jsonl')
summary = load(folder / 'summary.json')
manifest = load(folder / 'manifest.json')
package = load(ROOT / 'PACKAGE-MANIFEST.json')
report = {'scope': 'Retained-artifact recomputation and local validator fault probes only; no new experiments or model calls.'}
report['saved_verify_output'] = list(validate.verify_output(folder))
report['package_hashes'] = {'listed': len(package['files']), 'mismatches': [p for p, h in package['files'].items() if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]}
actual = {str(p.relative_to(ROOT)) for p in ROOT.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name != 'PACKAGE-MANIFEST.json'}
report['package_hashes']['unlisted'] = sorted(actual - set(package['files']))
report['source_hash_mismatches'] = [p for p, h in manifest['source_sha256'].items() if hashlib.sha256((ROOT / p).read_bytes()).hexdigest() != h]
report['json_files_parsed'] = sum(1 for p in ROOT.rglob('*.json') if load(p) is not None)
for name in ['agent-definition', 'context-access', 'run-config']:
    check(load(ROOT / f'templates/{name}.json'), load(ROOT / f'schemas/{name}.schema.json'))
toy.validate_config(config)
report['templates_structural_validation'] = 'pass'
report['relative_links_missing'] = []
for path in ROOT.rglob('*.md'):
    for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
        target = target.strip('<>').split('#')[0]
        if target and '://' not in target and not (path.parent / target).exists():
            report['relative_links_missing'].append({'path': str(path.relative_to(BASE)), 'target': target})

by_run = defaultdict(list)
for e in events:
    by_run[e['run_id']].append(e)
expected_keys = {(f's{s:03d}', r, c) for s in range(config['scenarios']) for r in range(config['replicates']) for c in config['conditions']}
assert {(p['scenario_id'], p['replicate'], p['condition']) for p in planned} == expected_keys
assert {(o['scenario_id'], o['replicate'], o['condition']) for o in outcomes} == expected_keys
by_plan = {p['run_id']: p for p in planned}
for o in outcomes:
    trace = by_run[o['run_id']]
    assert all(o[k] == by_plan[o['run_id']][k] for k in by_plan[o['run_id']])
    world = toy.initialize(config, int(o['scenario_id'][1:]), o['replicate'])
    observations = [e for e in trace if e['type'] == 'observation']
    decisions = [e for e in trace if e['type'] == 'decision']
    assert Counter(e['agent_id'] for e in observations) == Counter(f'a{i}' for i in range(config['agents']))
    assert Counter(e['agent_id'] for e in decisions) == Counter(f'a{i}' for i in range(config['agents']))
    by_agent = {e['agent_id']: e for e in observations}
    for d in decisions:
        i = int(d['agent_id'][1:])
        observed = by_agent[d['agent_id']]['payload']
        assert observed['own_signal'] == world['signals'][i]
        sources = ([i] if o['condition'] == 'no_communication' else sorted({i, (i-1) % config['agents'], (i+1) % config['agents']}) if o['condition'] == 'provenance_ring' else list(range(config['agents'])))
        expected_evidence = [{'source_id': s, 'value': world['signals'][s]} for s in sources for _ in range(config['repeated_source_copies'] if s == 0 else 1)]
        assert observed['evidence'] == expected_evidence
        values = [world['signals'][s] for s in sources] if o['condition'].startswith('provenance') else [x['value'] for x in expected_evidence]
        predicted = int(sum(values) * 2 > len(values)) if sum(values) * 2 != len(values) else world['signals'][i]
        assert d['payload']['value'] == predicted
    evaluation = next(e['payload'] for e in trace if e['type'] == 'evaluation')
    assert evaluation['truth'] == world['truth']
    assert o['decisions'] == len(decisions)
    assert trace[-1]['payload']['status'] == o['status'] == 'completed'
    assert trace[-1]['payload']['decisions'] == o['decisions']
    assert evaluation['group_correct'] == o['group_correct']
report['independent_all_record_semantic_audit'] = 'pass: every planned unit, truth, agent ID, observation, routing, policy decision, endpoint and terminal count'
report['counts'] = {'planned': len(planned), 'outcomes': len(outcomes), 'events': len(events), 'agent_decisions': sum(e['type'] == 'decision' for e in events), 'scenario_clusters': config['scenarios'], 'paired_worlds': config['scenarios'] * config['replicates']}
report['recomputed_results'] = {k: summary[k] for k in ['condition_means', 'mean_paired_difference', 'scenario_cluster_percentile_ci_95', 'planning_example_only']}

# Algebraic integration of known policies: no sampled worlds or policy execution.
def mean_polynomial(coeffs, a=.55, b=.90):
    return sum(c * (b ** (i+1) - a ** (i+1)) / (i+1) for i, c in enumerate(coeffs)) / (b-a)
report['analytic_population_expected_accuracy'] = {'naive_global': mean_polynomial([0, 0, 4, -6, 5, -2]), 'provenance_global': mean_polynomial([0, 0, 0, 10, -15, 6]), 'no_communication': mean_polynomial([0, 1]), 'provenance_ring': mean_polynomial([0, 0, 3, -2])}
report['analytic_population_expected_difference'] = report['analytic_population_expected_accuracy']['provenance_global'] - report['analytic_population_expected_accuracy']['naive_global']

def refresh_files(p, es=None, os=None, ps=None):
    if es is not None:
        previous = {}
        for e in es:
            e['prev_hash'] = previous.get(e['run_id'], '0' * 64)
            e.pop('event_hash', None)
            e['event_hash'] = digest(e)
            previous[e['run_id']] = e['event_hash']
        if os is not None:
            for o in os:
                o['final_event_hash'] = previous[o['run_id']]
        write_lines(p / 'events.jsonl', es)
    if os is not None:
        write_lines(p / 'outcomes.jsonl', os)
        dump(p / 'summary.json', toy.summarize(config, os))
    if ps is not None:
        dump(p / 'planned-runs.json', ps)
    m = load(p / 'manifest.json')
    m['output_sha256'] = {name: hashlib.sha256((p / name).read_bytes()).hexdigest() for name in m['output_sha256']}
    dump(p / 'manifest.json', m)

def probe(name, mutate):
    with tempfile.TemporaryDirectory(prefix='guide-validator-probe-', dir=REVIEW) as temp:
        p = Path(temp) / 'copy'
        shutil.copytree(folder, p)
        mutate(p)
        try:
            validate.verify_output(p)
            result = 'ACCEPTED_INVALID_COPY'
        except Exception as error:
            result = 'rejected:' + type(error).__name__
    return {'name': name, 'result': result}

def wrong_source_hash(p):
    m = load(p / 'manifest.json')
    m['source_sha256']['scripts/toy_harness.py'] = '0' * 64
    dump(p / 'manifest.json', m)

def wrong_plan(p):
    ps = copy.deepcopy(planned)
    ps[0]['condition'] = 'not-a-condition'
    refresh_files(p, ps=ps)

def wrong_truth(p):
    es, os = copy.deepcopy(events), copy.deepcopy(outcomes)
    rid = os[0]['run_id']
    decision_values = [e['payload']['value'] for e in es if e['run_id'] == rid and e['type'] == 'decision']
    for e in es:
        if e['run_id'] == rid and e['type'] == 'evaluation':
            e['payload']['truth'] = 1 - e['payload']['truth']
            e['payload']['score'] = sum(d == e['payload']['truth'] for d in decision_values) / len(decision_values)
            e['payload']['group_correct'] = (sum(decision_values) * 2 > len(decision_values)) == e['payload']['truth']
            os[0]['score'] = e['payload']['score']
            os[0]['group_correct'] = e['payload']['group_correct']
    refresh_files(p, es, os)

def duplicate_agent(p):
    es, os = copy.deepcopy(events), copy.deepcopy(outcomes)
    rid = os[0]['run_id']
    for e in es:
        if e['run_id'] == rid and e['type'] == 'decision':
            e['agent_id'] = 'a0'
    refresh_files(p, es, os)

def wrong_status(p):
    os = copy.deepcopy(outcomes)
    os[0]['status'] = 'failed'
    os[0]['decisions'] = 999
    refresh_files(p, os=os)

report['validator_fault_probes'] = [probe(name, fn) for name, fn in [('wrong_source_hash', wrong_source_hash), ('planned_condition_disagrees_with_outcome', wrong_plan), ('evaluation_truth_disagrees_with_initialized_world', wrong_truth), ('all_five_decisions_same_agent_id', duplicate_agent), ('failed_outcome_with_wrong_decision_count', wrong_status)]]
edge_config = copy.deepcopy(config)
edge_config['bootstrap_samples'] = 1
toy.validate_config(edge_config)
edge_ci = toy.summarize(edge_config, outcomes)['scenario_cluster_percentile_ci_95']
report['one_resample_edge_probe'] = {'accepted_config': True, 'reported_ci_95': edge_ci, 'zero_width': edge_ci[0] == edge_ci[1]}
dump(REVIEW / 'methodology-guide-checks.json', report)
print(json.dumps(report, indent=2))
