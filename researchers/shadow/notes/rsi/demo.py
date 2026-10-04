#!/usr/bin/env python3
"""Offline bundle example: real public envelopes, synthetic contract evaluation.
No source content, model calls, worker dispatch, network or real settlement.
"""
import copy
import json
from pathlib import Path
import protocol as p

HERE = Path(__file__).resolve().parent


def fixture():
    events = [p.loads(line) for line in (HERE / 'examples/pool-events.jsonl').read_text().splitlines()]
    for event in events: p.validate(event)
    first = events[0]
    # Synthetic cases are authored for a metadata-contract demonstration, not
    # claimed as independently held-out scientific evaluation.
    cases = [
        {'field': 'billed_microusd', 'input': None, 'expected': None},
        {'field': 'billed_microusd', 'input': 0, 'expected': 0},
        {'field': 'tool_calls', 'input': None, 'expected': None},
        {'field': 'tool_calls', 'input': [], 'expected': []},
    ]
    baseline_outputs = [c['input'] if c['input'] is not None else 0 if c['field'] == 'billed_microusd' else [] for c in cases]
    candidate_outputs = [c['input'] for c in cases]
    baseline_bps = sum(o == c['expected'] for o, c in zip(baseline_outputs, cases)) * 2500
    candidate_bps = sum(o == c['expected'] for o, c in zip(candidate_outputs, cases)) * 2500
    rubric_hash = p.sha(p.canonical({'metric': 'typed-missingness', 'cases': cases}))
    baseline_hash = p.sha(p.canonical(baseline_outputs))
    patch = {'action': 'preserve-unknown-not-zero', 'checks': ['missing-cost-is-null', 'known-zero-is-zero', 'missing-tools-is-null', 'observed-empty-tools-is-empty']}
    patch_hash = p.sha(p.canonical(patch))
    task_version = p.sha(p.canonical({'opportunity': 'metadata-contract-001', 'rubric_hash': rubric_hash, 'source_event_hash': first['integrity']['record_hash']}))
    bundle = {'schema_version': p.VERSION, 'record_type': 'bundle', 'bundle_id': 'bundle-null-preservation',
        'searcher_id': 'searcher-metadata', 'searcher_principal_id': 'principal-metadata', 'opportunity_id': 'metadata-contract-001',
        'mode': 'offline-demo', 'kind': 'fix', 'trigger_event_ids': [first['event_id']], 'source_event_hashes': [first['integrity']['record_hash']],
        'inclusion': {'epoch_min': 1, 'epoch_max': 1, 'after_release': False, 'task_version_hash': task_version},
        'body': [{'action_id': 'check-contract', 'operation': 'offline-check', 'depends_on': [], 'artifact_hash': patch_hash, 'failure_policy': 'abort-publication'},
                 {'action_id': 'propose-fix', 'operation': 'propose-brief', 'depends_on': ['check-contract'], 'artifact_hash': patch_hash, 'failure_policy': 'abort-publication'}],
        'read_set': [first['event_id']], 'write_set': ['candidate/metadata-contract'], 'permitted_builders': ['builder-offline-demo'],
        'budget': {'max_model_calls': 0, 'max_microusd': 0, 'max_runtime_ms': 1000},
        'valuation': {'metric_id': 'typed-missingness', 'rubric_hash': rubric_hash, 'baseline_artifact_hash': baseline_hash, 'claimed_gain_bps': 5000, 'requested_bounty_microusd': 1000000},
        'rebates': {'trace_originator_bps': 2000, 'searcher_bps': 6000, 'builder_bps': 1000, 'evaluator_bps': 1000},
        'orderflow_bid': {'funded_microusd': 0, 'escrow_receipt_hash': None},
        'capabilities': {'network': False, 'paid_calls': False, 'publish_raw': False, 'write_scope': 'isolated-candidate'},
        'nonce': '11' * 32, 'integrity': {'record_hash': '0' * 64, 'previous_event_hash': None, 'signature': None}}
    p.seal_record(bundle)
    flashy = copy.deepcopy(bundle)
    flashy.update(bundle_id='bundle-overclaim', searcher_id='searcher-overclaim', searcher_principal_id='principal-overclaim')
    flashy['valuation']['claimed_gain_bps'] = 10000
    flashy['nonce'] = '22' * 32
    p.seal_record(flashy)
    policy = {'opportunity_id': bundle['opportunity_id'], 'builder_id': 'builder-offline-demo', 'reviewer_id': 'reviewer-fixture',
              'epoch': 1, 'task_version_hash': task_version, 'max_runtime_ms': 1000, 'bounty_cap_microusd': 1000000,
              'rubric_hash': rubric_hash, 'metric_id': 'typed-missingness', 'baseline_artifact_hash': baseline_hash, 'gain_value_microusd': 4000000}
    evaluations = {
        b['bundle_id']: {'bundle_hash': b['integrity']['record_hash'], 'reviewer_id': 'reviewer-fixture', 'rubric_hash': rubric_hash,
                         'baseline_bps': baseline_bps, 'candidate_bps': candidate_bps if b is bundle else baseline_bps,
                         'review_passed': b is bundle, 'guardrails_passed': True}
        for b in (bundle, flashy)
    }
    return events, [bundle, flashy], evaluations, policy, {'cases': cases, 'baseline_outputs': baseline_outputs, 'candidate_outputs': candidate_outputs, 'patch': patch}


def main():
    events, bundles, evaluations, policy, evaluation_fixture = fixture()
    result = p.choose(bundles, {e['event_id']: e for e in events}, evaluations, policy)
    expected = {'winner': 'bundle-null-preservation', 'evaluated_gain_bps': 5000, 'controller_net_value_microusd': 1000000,
                'rejected': [{'bundle_id': 'bundle-overclaim', 'reason': 'review or guardrail failed'}],
                'hypothetical_bounty_split_microusd': {'trace_originator_bps': 200000, 'searcher_bps': 600000, 'builder_bps': 100000, 'evaluator_bps': 100000},
                'settled_microusd': 0, 'mode': 'offline-demo-no-payments'}
    assert result == expected
    saved = HERE / 'examples/worked-bundle.json'
    payload = {'bundle': bundles[0], 'competitor': bundles[1], 'controller_policy': policy, 'evaluations': evaluations,
               'evaluation_fixture': evaluation_fixture, 'result': result,
               'provenance': 'real imported envelope; synthetic developer-owned evaluation, unsigned, no live inclusion or payment'}
    if saved.exists(): assert p.loads(saved.read_text()) == payload, 'saved example differs'
    else: saved.write_text(json.dumps(payload, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    print('Source envelopes are real; the 2/4 -> 4/4 test and $1 split are synthetic offline illustrations.')
    print('No real payment, independent research effect, live auction or policy promotion is claimed.')


if __name__ == '__main__': main()
