#!/usr/bin/env python3
"""Offline real-record trace -> saved agent proposals -> replay -> credit.
No network, model dispatch, arbitrary candidate code, raw private inputs or money.
"""
import argparse
import copy
import json
from collections import Counter
from pathlib import Path
import protocol as p
import reporting as r
import freeze_sources as f

HERE = Path(__file__).resolve().parent
INPUT = HERE / 'r1-input'
SEARCHER = HERE / 'r1-searcher'
RESULTS = HERE / 'r1-results'


def digest(value):
    return p.sha(p.canonical(value))


def load_json(path):
    return p.loads(path.read_text())


def verify_chain(events):
    previous, expected_seq, stream = None, 0, None
    ids = set()
    for event in events:
        p.validate(event)
        if stream is None:
            stream = event['stream_id']
        if event['stream_id'] != stream or event['stream_seq'] != expected_seq or event['integrity']['previous_event_hash'] != previous:
            raise ValueError('broken import stream')
        if event['event_id'] in ids:
            raise ValueError('duplicate imported event')
        ids.add(event['event_id'])
        previous = event['integrity']['record_hash']
        expected_seq += 1


def load_inputs(directory=INPUT):
    manifest = load_json(directory / 'manifest.json')
    if manifest['plan_sha256'] != p.sha((HERE / 'REPLAY-PLAN-v2.md').read_bytes()):
        raise ValueError('frozen plan drift')
    for name, expected in manifest['derived'].items():
        if name not in ('public-events.jsonl', 'projections.json') or p.sha((directory / name).read_bytes()) != expected:
            raise ValueError('derived input drift')
    pool_path = directory / 'pool-events.jsonl'
    if manifest['pool']['path'] != pool_path.name or p.sha(pool_path.read_bytes()) != manifest['pool']['sha256']:
        raise ValueError('pool envelope drift')
    events = [p.loads(x) for x in (directory / 'public-events.jsonl').read_text().splitlines()]
    pool = [p.loads(x) for x in pool_path.read_text().splitlines()]
    projected = load_json(directory / 'projections.json')
    rebuilt_events, rebuilt_projection = f.build(manifest)
    if events != rebuilt_events or projected != rebuilt_projection:
        raise ValueError('public-source rederivation mismatch')
    verify_chain(events)
    verify_chain(pool)
    if len(pool) != manifest['pool']['rows']:
        raise ValueError('pool count mismatch')
    ids = [e['event_id'] for e in events + pool]
    if len(ids) != len(set(ids)):
        raise ValueError('cross-stream ID collision')
    if any(e['market']['eligible'] for e in events + pool):
        raise ValueError('historical inputs must not enter live auction')
    return manifest, events + pool, projected


def rubric(manifest):
    return {'metric': 'complete-attempt-accounting', 'checks': list(r.CHECKS),
            'selection': r.SELECTION, 'acceptance': 'all-assigned-checks-and-positive-baseline-gain',
            'source_root': digest(manifest), 'baseline_policy': r.BASELINE,
            'independent_review': False, 'scientific_promotion': False, 'payout_microusd': 0}


def proposal(policy, ident, events, manifest, claimed_gain):
    # Five representative triggers, but source_root in rubric binds ALL records.
    triggers = []
    seen = set()
    cells_by_event = {x['event_id']: x['cell'] for x in load_json(INPUT / 'projections.json') if x['role'] == 'episode'}
    for ev in events:
        if ev['owner_id'] != 'shadow' or ev['source']['adapter'] != 'experiment':
            continue
        if ev['attributes'].get('gen_ai.request.model'):
            # Select by associated public source path, not private content.
            source_cell = cells_by_event[ev['event_id']]
            if source_cell not in seen:
                triggers.append(ev)
                seen.add(source_cell)
    rule = rubric(manifest)
    bundle = {'schema_version': p.VERSION, 'record_type': 'bundle', 'bundle_id': ident,
              'searcher_id': 'shadow/sol-rsi2', 'searcher_principal_id': 'shadow',
              'opportunity_id': 'r1-reporting-repair', 'mode': 'offline-demo', 'kind': 'fix',
              'trigger_event_ids': [e['event_id'] for e in triggers],
              'source_event_hashes': [e['integrity']['record_hash'] for e in triggers],
              'inclusion': {'epoch_min': 1, 'epoch_max': 1, 'after_release': True, 'task_version_hash': digest(manifest)},
              'body': [{'action_id': 'replay-accounting', 'operation': 'offline-check', 'depends_on': [], 'artifact_hash': digest(policy), 'failure_policy': 'abort-publication'},
                       {'action_id': 'publish-report', 'operation': 'propose-brief', 'depends_on': ['replay-accounting'], 'artifact_hash': digest(policy), 'failure_policy': 'abort-publication'}],
              'read_set': [e['event_id'] for e in triggers], 'write_set': ['candidate/r1-accounting-report'],
              'permitted_builders': ['builder-offline-demo'],
              'budget': {'max_model_calls': 0, 'max_microusd': 0, 'max_runtime_ms': 30000},
              'valuation': {'metric_id': rule['metric'], 'rubric_hash': digest(rule), 'baseline_artifact_hash': digest(r.BASELINE), 'claimed_gain_bps': claimed_gain, 'requested_bounty_microusd': 0},
              'rebates': {'trace_originator_bps': 2000, 'searcher_bps': 6000, 'builder_bps': 1000, 'evaluator_bps': 1000},
              'orderflow_bid': {'funded_microusd': 0, 'escrow_receipt_hash': None},
              'capabilities': {'network': False, 'paid_calls': False, 'publish_raw': False, 'write_scope': 'isolated-candidate'},
              'nonce': digest({'bundle': ident, 'context': 'public-offline-not-live-bid'}),
              'integrity': {'record_hash': '0' * 64, 'previous_event_hash': None, 'signature': None}}
    p.seal_record(bundle)
    p.validate(bundle)
    return {'bundle': bundle, 'policy': policy}


def save_proposals():
    if SEARCHER.exists():
        raise ValueError('saved proposals already exist; no silent replacement')
    manifest, events, rows = load_inputs()
    SEARCHER.mkdir()
    f.write_json(SEARCHER / 'rubric.json', rubric(manifest))
    for name, policy, claim in [('lineage-repair', r.REPAIR, 5000), ('clamp-shortcut', r.SHORTCUT, 10000)]:
        f.write_json(SEARCHER / (name + '.json'), proposal(policy, 'bundle-r1-' + name, events, manifest, claim))
    f.write_json(SEARCHER / 'receipt.json', {
        'author': 'shadow/sol-rsi2', 'generation': 'current-operating-coding-agent-authored',
        'fresh_model_calls_by_demo': 0, 'proposal_count': 2,
        'inputs': {'manifest_sha256': p.sha((INPUT / 'manifest.json').read_bytes()), 'source_root': digest(manifest)},
        'files': {name: p.sha((SEARCHER / name).read_bytes()) for name in ('rubric.json', 'lineage-repair.json', 'clamp-shortcut.json')},
        'reasoning': 'Known report loses attempts after last-valid selection. Preserve full lineage and comparable numerator/denominator. Contrast with cosmetic clamping that conceals failed attempts.',
        'not_claimed': ['blind-discovery', 'independent-review', 'fresh-model-execution', 'paid-auction']})
    print('Saved two current-agent-authored proposals; no fresh model call.')


def admit(entry, events, manifest):
    if set(entry) != {'bundle', 'policy'}:
        raise ValueError('proposal fields are closed')
    bundle, policy = entry['bundle'], entry['policy']
    p.validate(bundle)
    r.validate_policy(policy)
    expected = proposal(policy, bundle['bundle_id'], events, manifest, bundle['valuation']['claimed_gain_bps'])
    if entry != expected:
        raise ValueError('proposal exceeds frozen controller contract')
    return bundle, policy


def credit_entries(evaluations, manifest):
    entries, seen, previous = [], set(), None
    for evaluation in evaluations:
        bundle = evaluation['bundle']
        accepted = evaluation['accepted']
        total = 1000 if accepted else 0
        settlement = digest({'source_root': digest(manifest), 'opportunity': bundle['opportunity_id'], 'bundle_hash': bundle['integrity']['record_hash'], 'evaluation_hash': evaluation['receipt_hash']})
        if settlement in seen:
            raise ValueError('duplicate credit receipt')
        seen.add(settlement)
        entry = {'receipt_id': settlement, 'bundle_id': bundle['bundle_id'], 'bundle_hash': bundle['integrity']['record_hash'],
                 'source_root': digest(manifest), 'evaluation_hash': evaluation['receipt_hash'],
                 'rubric_hash': bundle['valuation']['rubric_hash'], 'previous_receipt_hash': previous,
                 'status': 'accepted-maintenance' if accepted else 'rejected',
                 'credit_kind': 'non-transferable-demo-attribution', 'total_units': total,
                 'units_by_role': p.split_payment(total, bundle['rebates']),
                 'principal_by_role': {'trace_originator_bps': 'shadow', 'searcher_bps': 'shadow', 'builder_bps': 'shadow', 'evaluator_bps': 'shadow'},
                 'same_principal_maintenance': True, 'independent_review': False,
                 'payable_microusd': 0, 'settled_microusd': 0}
        entry['receipt_hash'] = digest(entry)
        previous = entry['receipt_hash']
        entries.append(entry)
    return entries


def run():
    manifest, events, rows = load_inputs()
    recorded = load_json(SEARCHER / 'receipt.json')
    if recorded['inputs']['source_root'] != digest(manifest) or recorded['inputs']['manifest_sha256'] != p.sha((INPUT / 'manifest.json').read_bytes()):
        raise ValueError('searcher source drift')
    for name, expected in recorded['files'].items():
        if name not in ('rubric.json', 'lineage-repair.json', 'clamp-shortcut.json') or p.sha((SEARCHER / name).read_bytes()) != expected:
            raise ValueError('saved searcher artifact drift')
    if load_json(SEARCHER / 'rubric.json') != rubric(manifest):
        raise ValueError('rubric drift')
    baseline = r.evaluate(rows, r.BASELINE)
    evaluations = []
    for name in ('lineage-repair.json', 'clamp-shortcut.json'):
        bundle, policy = admit(load_json(SEARCHER / name), events, manifest)
        measured = r.evaluate(rows, policy)
        passed, total = measured['passed'], measured['assigned']
        accepted = total > 0 and passed == total and passed > baseline['passed']
        receipt = {'bundle': bundle, 'policy': policy, 'baseline_passed': baseline['passed'], 'passed': passed, 'assigned': total,
                   'accepted': accepted, 'gain_bps': (passed - baseline['passed']) * 10000 // total if total else 0,
                   'reason': 'all-accounting-checks-pass' if accepted else 'incomplete-attempt-accounting',
                   'failed_checks': dict(Counter(c['check'] for c in measured['cases'] if not c['passed'])),
                   'cases': measured['cases'], 'reports': measured['reports'], 'source_root': digest(manifest),
                   'independent_review': False, 'scientific_promotion': False}
        receipt['receipt_hash'] = digest(receipt)
        evaluations.append(receipt)
    # This controller compares two variants from ONE maintenance searcher.
    # It is deliberately not protocol.choose's multi-principal live-auction analogy.
    if sum(e['accepted'] for e in evaluations) > 1:
        raise ValueError('one-slot maintenance controller refuses multiple accepted writes')
    ledger = credit_entries(evaluations, manifest)
    reference = {key: r.reference(v) for key, v in r.groups(rows).items()}
    totals = {key: sum(v[key] for v in reference.values()) for key in (
        'physical_records', 'invalid_records', 'logical_records', 'selected_valid_records', 'superseded_records',
        'selected_captured_records', 'first_attempt_valid_records', 'invalid_then_valid_logical_records')}
    summary = {'mode': 'offline-saved-data-repair', 'source_root': digest(manifest),
               'envelopes': len(events), 'source_counts': dict(Counter(x['role'] for x in rows)),
               'pool_envelopes': manifest['pool']['rows'], 'policy_call_population': sum(x['rows'] for x in manifest['sources'] if x['role'] == 'policy-call'),
               'reporting_groups': len(reference), 'totals': totals,
               'baseline': {'passed': baseline['passed'], 'assigned': baseline['assigned']},
               'candidates': [{k: e[k] for k in ('accepted', 'passed', 'assigned', 'gain_bps', 'reason', 'failed_checks')} | {'bundle_id': e['bundle']['bundle_id']} for e in evaluations],
               'credit_units': sum(x['total_units'] for x in ledger), 'settled_microusd': 0,
               'new_model_calls': 0, 'independent_review': False, 'scientific_effect_measured': False}
    frames = [
        {'stage': 'ingest', 'label': 'Real historical records', 'counts': {'envelopes': len(events), **dict(Counter(x['role'] for x in rows)), 'pool': manifest['pool']['rows']}},
        {'stage': 'search', 'label': 'Saved current-agent proposals', 'counts': {'proposals': len(evaluations), 'new_model_calls': 0}},
        {'stage': 'build', 'label': 'Frozen accounting contract', 'counts': {'groups': len(reference), 'assertions_per_candidate': baseline['assigned'], 'baseline_passed': baseline['passed'], **{e['bundle']['bundle_id']: e['passed'] for e in evaluations}}},
        {'stage': 'credit', 'label': 'Related-party attribution, not money', 'counts': {'accepted': sum(e['accepted'] for e in evaluations), 'rejected': sum(not e['accepted'] for e in evaluations), 'credit_units': summary['credit_units'], 'settled_microusd': 0}}]
    inventory = {name: p.sha((HERE / name).read_bytes()) for name in ('freeze_sources.py', 'reporting.py', 'replay_loop.py', 'protocol.py', 'trace.schema.json')}
    return {'summary': summary, 'baseline': baseline, 'evaluations': evaluations, 'reference_reports': reference,
            'credit_ledger': ledger, 'frames': frames, 'implementation_sha256': inventory}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--save-agent-proposals', action='store_true', help='One-time packaging of current-agent-authored policies, NOT an LLM call')
    ap.add_argument('--record', action='store_true', help='Write a new immutable result directory')
    ap.add_argument('--verify', action='store_true', help='Recompute and compare every saved result field')
    args = ap.parse_args()
    if args.save_agent_proposals:
        save_proposals()
        return
    output = run()
    if args.record:
        RESULTS.mkdir(exist_ok=False)
        f.write_json(RESULTS / 'replay.json', output)
        f.write_json(RESULTS / 'summary.json', output['summary'])
        with (RESULTS / 'credit-ledger.jsonl').open('x') as out:
            for e in output['credit_ledger']:
                out.write(p.canonical(e).decode() + '\n')
    if args.verify:
        if output != load_json(RESULTS / 'replay.json'):
            raise ValueError('saved results or implementation changed')
        if output['summary'] != load_json(RESULTS / 'summary.json'):
            raise ValueError('saved summary changed')
        if output['credit_ledger'] != [p.loads(x) for x in (RESULTS / 'credit-ledger.jsonl').read_text().splitlines()]:
            raise ValueError('saved credit ledger changed')
    print(json.dumps(output['summary'], indent=2))


if __name__ == '__main__':
    main()
