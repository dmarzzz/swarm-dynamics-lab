#!/usr/bin/env python3
"""Validate this package and exercise the offline toy, without third-party packages."""
import copy
import hashlib
import json
import re
import tempfile
from collections import defaultdict
from pathlib import Path
from contracts import check, digest
import toy_harness as toy

ROOT = Path(__file__).resolve().parents[1]


def load(path):
    return json.loads(path.read_text())


def verify_output(folder):
    config = load(folder/'config.resolved.json')
    planned = load(folder/'planned-runs.json')
    outcomes = [json.loads(x) for x in (folder/'outcomes.jsonl').read_text().splitlines()]
    events = [json.loads(x) for x in (folder/'events.jsonl').read_text().splitlines()]
    manifest = load(folder/'manifest.json')
    for name, expected in manifest['output_sha256'].items():
        assert hashlib.sha256((folder/name).read_bytes()).hexdigest() == expected
    assert digest(config) == manifest['configuration_sha256']
    assert len({x['run_id'] for x in planned}) == len(planned)
    assert len(outcomes) == len(planned)
    assert {x['run_id'] for x in planned} == {x['run_id'] for x in outcomes}
    event_schema = load(ROOT/'schemas/event.schema.json')
    outcome_schema = load(ROOT/'schemas/outcome.schema.json')
    by_run = defaultdict(list)
    pairs = defaultdict(set)
    for event in events:
        check(event, event_schema)
        by_run[event['run_id']].append(event)
    assert set(by_run) == {x['run_id'] for x in planned}
    for outcome in outcomes:
        check(outcome, outcome_schema)
        trace = by_run[outcome['run_id']]
        previous = '0'*64
        for i, event in enumerate(trace):
            assert all(event[k] == outcome[k] for k in ['study_id','scenario_id','replicate','condition'])
            assert event['seq'] == i and event['prev_hash'] == previous
            assert event['parent_seq'] == (i-1 if i else None)
            unhashed = dict(event); actual = unhashed.pop('event_hash')
            assert digest(unhashed) == actual
            previous = actual
        assert trace[0]['type'] == 'run_start' and trace[-1]['type'] == 'run_end'
        assert sum(e['type'] == 'run_end' for e in trace) == 1
        assert previous == outcome['final_event_hash']
        assert trace[0]['payload']['initial_sha256'] == outcome['initial_sha256']
        assert digest(toy.initialize(config, int(outcome['scenario_id'][1:]), outcome['replicate'])) == outcome['initial_sha256']
        pairs[outcome['scenario_id'], outcome['replicate']].add(outcome['initial_sha256'])
        actions = [e['payload']['value'] for e in trace if e['type'] == 'decision']
        evaluations = [e for e in trace if e['type'] == 'evaluation']
        assert len(evaluations) == 1 and len(actions) == config['agents']
        truth = evaluations[0]['payload']['truth']
        # Replay scored events independently of policy and environment generator.
        score = sum(x == truth for x in actions)/len(actions)
        assert score == outcome['score'] == evaluations[0]['payload']['score']
        assert (int(2*sum(actions)>len(actions)) == truth) == outcome['group_correct']
        assert outcome['api_calls'] == 0 and outcome['api_cost_usd'] == 0
        if outcome['condition'] == 'no_communication':
            for event in trace:
                if event['type'] == 'observation':
                    assert {x['source_id'] for x in event['payload']['evidence']} == {int(event['agent_id'][1:])}
    assert all(len(hashes) == 1 for hashes in pairs.values())
    assert load(folder/'summary.json') == toy.summarize(config, outcomes)
    return len(outcomes), len(events)


def main():
    for path in ROOT.rglob('*.json'):
        load(path)
    for name in ['agent-definition','context-access','run-config']:
        check(load(ROOT/f'templates/{name}.json'), load(ROOT/f'schemas/{name}.schema.json'))
    config = load(ROOT/'examples/collective-sensing/config.json')
    toy.validate_config(config)
    # Nontrivial oracle: duplicate evidence flips naive majority but not provenance-aware majority.
    world = {'truth':1,'quality':.7,'signals':[0,0,1,1,1]}
    evidence = toy.observe(world, 'naive_global', 2, 3)
    assert toy.decide(evidence, 'naive_global', 1) == 0
    assert toy.decide(evidence, 'provenance_global', 1) == 1
    assert len({x['source_id'] for x in toy.observe(world, 'provenance_ring', 2, 3)}) == 3
    # Reset isolation and matched initialization.
    a = toy.initialize(config, 0, 0); b = toy.initialize(config, 0, 0)
    assert a == b
    a['signals'][0] = 99
    assert b['signals'][0] != 99
    for key, value in [('agents',4),('mode','live'),('conditions',['naive_global','naive_global'])]:
        bad = copy.deepcopy(config); bad[key] = value
        try:
            toy.validate_config(bad)
        except ValueError:
            pass
        else:
            raise AssertionError('Invalid config accepted')
    with tempfile.TemporaryDirectory(prefix='agent-guide-validation-') as temp:
        p = Path(temp)
        toy.run(config, p/'a'); toy.run(config, p/'b')
        counts = verify_output(p/'a')
        assert counts == verify_output(p/'b')
        assert all(f.read_bytes() == (p/'b'/f.name).read_bytes() for f in (p/'a').iterdir())
        try:
            toy.run(config, p/'a')
        except FileExistsError:
            pass
        else:
            raise AssertionError('Existing output was overwritten')
        # Recorded corruption must fail integrity verification.
        trace = p/'a/events.jsonl'
        trace.write_text(trace.read_text().replace('scripted-majority-v1', 'scripted-majority-v2', 1))
        try:
            verify_output(p/'a')
        except AssertionError:
            pass
        else:
            raise AssertionError('Corruption not detected')
    # Check relative file links (anchors and external URLs excluded).
    for path in ROOT.rglob('*.md'):
        for target in re.findall(r'\]\(([^)]+)\)', path.read_text()):
            target = target.strip('<>').split('#')[0]
            if not target or '://' in target:
                continue
            assert (path.parent/target).exists(), (path.name, target)
    print(f'PASS: templates, schemas, {counts[0]} runs, {counts[1]} events, pairing, replay, reset, corruption and overwrite rejection, links.')


if __name__ == '__main__':
    main()
