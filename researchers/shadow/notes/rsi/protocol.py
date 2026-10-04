#!/usr/bin/env python3
"""Small offline protocol primitives. Does not dispatch bundles or pay anyone."""
import copy
import hashlib
import json
import re
from pathlib import Path

VERSION = 'swarm-trace/0.2.0'
REVISION = 'e07f4ebacb08f56db8c4c882d117720333fbca04'


def loads(text):
    """Decode without silently accepting duplicate keys or NaN/Infinity."""
    def pairs(items):
        value = {}
        for key, item in items:
            if key in value: raise ValueError('duplicate JSON key')
            value[key] = item
        return value
    def constant(_): raise ValueError('nonfinite JSON number')
    return json.loads(text, object_pairs_hook=pairs, parse_constant=constant)


def canonical(value):
    """SLJ-1: ASCII-only JSON, sorted keys, no whitespace, safe integers only.
    This restricted wire profile avoids inventing an incomplete JCS serializer.
    Raw UTF-8 content is committed as bytes, not passed through this function.
    """
    def check(x):
        if x is None or isinstance(x, bool): return
        if isinstance(x, int) and abs(x) <= 9007199254740991: return
        if isinstance(x, str) and x.isascii(): return
        if isinstance(x, list):
            for v in x: check(v)
            return
        if isinstance(x, dict) and all(isinstance(k, str) and k.isascii() for k in x):
            for v in x.values(): check(v)
            return
        raise ValueError('SLJ-1 requires ASCII strings and safe integer numbers')
    check(value)
    return json.dumps(value, sort_keys=True, separators=(',', ':'), ensure_ascii=True, allow_nan=False).encode('ascii')


def sha(data): return hashlib.sha256(data).hexdigest()


def commitment(slot, body, nonce):
    if slot not in ('prompt', 'response', 'tool-arguments', 'tool-result') or len(nonce) != 32:
        raise ValueError('invalid commitment domain or nonce')
    domain = ('swarm-content/0.2.0/' + slot + '\x00').encode('ascii')
    return sha(domain + nonce + len(body).to_bytes(8, 'big') + body)


def record_hash(record):
    value = copy.deepcopy(record)
    value['integrity'].pop('record_hash', None)
    value['integrity'].pop('signature', None)
    return sha(b'swarm-record/0.2.0\x00' + canonical(value))


def seal_record(record):
    record['integrity']['record_hash'] = record_hash(record)
    return record


def validate(record):
    # JSON Schema is a shape check, NOT a signature or authorization check.
    import jsonschema
    schema = loads(Path(__file__).with_name('trace.schema.json').read_text())
    jsonschema.Draft202012Validator(schema, format_checker=jsonschema.FormatChecker()).validate(record)
    canonical(record)
    kind = record['record_type']
    if kind == 'content_public': return
    if record_hash(record) != record['integrity']['record_hash']:
        raise ValueError('record digest mismatch')
    if kind == 'event':
        if record['span_id'] == record['parent_span_id']:
            raise ValueError('self-parent')
        attrs = record['attributes']
        if attrs.get('gen_ai.agent.id') is not None and attrs['gen_ai.agent.id'] != record['agent_id']:
            raise ValueError('agent identity mismatch')
        cached = sum(attrs.get(k, 0) for k in ('gen_ai.usage.cache_read.input_tokens', 'gen_ai.usage.cache_write.input_tokens'))
        if 'gen_ai.usage.input_tokens' in attrs and cached > attrs['gen_ai.usage.input_tokens']:
            raise ValueError('cached input exceeds total input')
        if record['source']['mode'] == 'historical-import' and record['market']['eligible']:
            raise ValueError('historical imports are ineligible for live auctions')
    if kind == 'bundle':
        if record['inclusion']['epoch_min'] > record['inclusion']['epoch_max']:
            raise ValueError('reversed inclusion window')
        if record['kind'].startswith('backrun-') and not record['inclusion']['after_release']:
            raise ValueError('backruns must wait for owner release')
        if sum(record['rebates'].values()) != 10000:
            raise ValueError('rebate shares must total 10000 bps')
        if record['orderflow_bid']['funded_microusd'] and not record['orderflow_bid']['escrow_receipt_hash']:
            raise ValueError('bid has no funding receipt')
        ids = [a['action_id'] for a in record['body']]
        if len(ids) != len(set(ids)):
            raise ValueError('duplicate action IDs')
        seen = set()
        for a in record['body']:
            if any(d not in seen for d in a['depends_on']):
                raise ValueError('bundle body must be topologically ordered')
            seen.add(a['action_id'])
        if len(record['trigger_event_ids']) != len(set(record['trigger_event_ids'])) or len(record['trigger_event_ids']) != len(record['source_event_hashes']):
            raise ValueError('ambiguous source references')


def split_payment(total, shares):
    """Integer largest-remainder allocation; lexical role breaks exact ties."""
    if type(total) is not int or total < 0 or any(type(v) is not int or v < 0 for v in shares.values()) or sum(shares.values()) != 10000:
        raise ValueError('invalid payment allocation')
    amounts = {k: total * b // 10000 for k, b in shares.items()}
    order = sorted(shares, key=lambda k: (-(total * shares[k] % 10000), k))
    for k in order[:total - sum(amounts.values())]: amounts[k] += 1
    return amounts


def choose(bundles, events, evaluations, policy):
    """Deterministic OFFLINE one-slot quality auction. No signature/ACL claims.

    evaluations/policy are supplied by the test fixture, not bundle authors.
    Production must authenticate their controller/reviewer provenance separately.
    Claimed gains and searcher tips are deliberately not selection inputs.
    """
    import jsonschema
    accepted, rejected = [], []
    occupied_principals = set()
    # Prioritized by controller receipt order, never producer timestamps.
    for bundle in bundles:
        try:
            validate(bundle)
            if bundle['mode'] != 'offline-demo': raise ValueError('offline prototype refuses live proposals')
            if bundle['orderflow_bid']['funded_microusd'] != 0: raise ValueError('funded bids require a live escrow verifier outside this prototype')
            if bundle['searcher_principal_id'] in occupied_principals: raise ValueError('principal quota exceeded')
            occupied_principals.add(bundle['searcher_principal_id'])
            if bundle['opportunity_id'] != policy['opportunity_id']: raise ValueError('wrong opportunity')
            if policy['builder_id'] not in bundle['permitted_builders']: raise ValueError('builder not permitted')
            if not bundle['inclusion']['epoch_min'] <= policy['epoch'] <= bundle['inclusion']['epoch_max']: raise ValueError('expired or premature')
            if bundle['inclusion']['task_version_hash'] != policy['task_version_hash']: raise ValueError('stale task version')
            for eid, digest in zip(bundle['trigger_event_ids'], bundle['source_event_hashes']):
                event = events[eid]; validate(event)
                if event['integrity']['record_hash'] != digest: raise ValueError('source mutated')
                if policy['builder_id'] not in event['disclosure']['permitted_builders']: raise ValueError('source forbids builder')
                if event['disclosure']['release_state'] == 'withdrawn': raise ValueError('source withdrawn')
                if bundle['inclusion']['after_release'] and event['disclosure']['release_state'] != 'owner-authorized-public': raise ValueError('sealed result cannot be backrun before release')
                if bundle['rebates']['trace_originator_bps'] < event['market']['source_rebate_floor_bps']: raise ValueError('source rebate floor violated')
            if bundle['budget']['max_model_calls'] != 0 or bundle['budget']['max_microusd'] != 0: raise ValueError('zero-spend profile only')
            if bundle['budget']['max_runtime_ms'] > policy['max_runtime_ms']: raise ValueError('runtime cap exceeded')
            if bundle['valuation']['requested_bounty_microusd'] > policy['bounty_cap_microusd']: raise ValueError('bounty cap exceeded')
            ev = evaluations[bundle['bundle_id']]
            if ev['reviewer_id'] != policy['reviewer_id'] or ev['reviewer_id'] in (bundle['searcher_id'], bundle['searcher_principal_id']): raise ValueError('reviewer conflict')
            if ev['bundle_hash'] != bundle['integrity']['record_hash']: raise ValueError('evaluation binds wrong bundle')
            if ev['rubric_hash'] != policy['rubric_hash'] or bundle['valuation']['rubric_hash'] != policy['rubric_hash']: raise ValueError('rubric mismatch')
            if bundle['valuation']['metric_id'] != policy['metric_id']: raise ValueError('metric mismatch')
            if bundle['valuation']['baseline_artifact_hash'] != policy['baseline_artifact_hash']: raise ValueError('baseline mismatch')
            if not ev['review_passed'] or not ev['guardrails_passed']: raise ValueError('review or guardrail failed')
            for k in ('baseline_bps', 'candidate_bps'):
                if type(ev[k]) is not int or not 0 <= ev[k] <= 10000: raise ValueError('invalid evaluated score')
            gain = ev['candidate_bps'] - ev['baseline_bps']
            if gain <= 0: raise ValueError('no positive measured gain')
            value = policy['gain_value_microusd'] * gain // 10000 - bundle['valuation']['requested_bounty_microusd']
            if value <= 0: raise ValueError('nonpositive controller value')
            accepted.append((value, bundle['bundle_id'], bundle, gain))
        except jsonschema.ValidationError:
            rejected.append({'bundle_id': bundle.get('bundle_id', 'invalid'), 'reason': 'invalid schema'})
        except (ValueError, KeyError) as exc:
            rejected.append({'bundle_id': bundle.get('bundle_id', 'invalid'), 'reason': str(exc)})
    # One independent opportunity/slot; no combinatorial optimality claim.
    accepted.sort(key=lambda row: (-row[0], row[1]))
    if not accepted: return {'winner': None, 'rejected': rejected, 'settled_microusd': 0}
    value, bid, bundle, gain = accepted[0]
    return {'winner': bid, 'evaluated_gain_bps': gain, 'controller_net_value_microusd': value, 'rejected': rejected,
            'hypothetical_bounty_split_microusd': split_payment(bundle['valuation']['requested_bounty_microusd'], bundle['rebates']),
            'settled_microusd': 0, 'mode': 'offline-demo-no-payments'}
