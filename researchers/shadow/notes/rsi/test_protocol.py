import copy
import json
import unittest
from pathlib import Path
import jsonschema
import demo
import pool_to_spec
import protocol as p


class ProtocolTests(unittest.TestCase):
    def setUp(self):
        self.events, self.bundles, self.evals, self.policy, self.fixture = demo.fixture()
        self.eventmap = {e['event_id']: e for e in self.events}

    def run_choice(self, bundles=None, events=None, evaluations=None, policy=None):
        return p.choose(bundles or self.bundles, events or self.eventmap, evaluations or self.evals, policy or self.policy)

    def rebind(self, bundle):
        p.seal_record(bundle)
        self.evals[bundle['bundle_id']]['bundle_hash'] = bundle['integrity']['record_hash']

    def test_public_schema_and_hash_chain(self):
        previous = None
        for index, event in enumerate(self.events):
            p.validate(event)
            self.assertEqual(event['integrity']['previous_event_hash'], previous)
            self.assertEqual(event['stream_seq'], index)
            self.assertFalse(event['market']['eligible'])
            self.assertIsNone(event['outcome']['score'])
            self.assertIsNone(event['tool_calls'])
            self.assertIsNone(event['cost']['billed_microusd'])
            previous = event['integrity']['record_hash']
        for line in (Path(__file__).parent / 'examples/pool-content-public.jsonl').read_text().splitlines(): p.validate(json.loads(line))

    def test_commitments_are_salted_and_domain_separated(self):
        a = p.commitment('prompt', b'example', bytes(32))
        self.assertNotEqual(a, p.commitment('prompt', b'example', bytes([1]) * 32))
        self.assertNotEqual(a, p.commitment('response', b'example', bytes(32)))
        self.assertNotEqual(a, p.commitment('prompt', b'other', bytes(32)))

    def test_canonicalization_rejects_ambiguous_numbers(self):
        for value in (1.0, float('nan'), 2**54, '\u00e9'):
            with self.assertRaises(ValueError): p.canonical({'x': value})
        self.assertEqual(p.canonical({'b': 2, 'a': 1}), b'{"a":1,"b":2}')

    def test_duplicate_keys_and_nonfinite_json_rejected(self):
        for text in ('{"x":1,"x":2}', '{"x":NaN}', '{"x":Infinity}'):
            with self.assertRaises(ValueError): p.loads(text)

    def test_tamper_and_unknown_content_fields_rejected(self):
        changed = copy.deepcopy(self.events[0]); changed['attributes']['gen_ai.usage.output_tokens'] = 1
        with self.assertRaises(ValueError): p.validate(changed)
        changed = copy.deepcopy(self.events[0]); changed['content']['raw_prompt'] = 'injected'
        p.seal_record(changed)
        with self.assertRaises(jsonschema.ValidationError): p.validate(changed)

    def test_adapter_projects_not_redacts(self):
        task = 'x' * 120
        row = {'request': json.dumps({'messages': [{'role': 'user', 'content': task}]}), 'response': 'PRIVATE_SENTINEL',
               'model': 'claude-fable-5-1', 'provider': 'anthropic', 'status': 200,
               'ts': '2026-10-04T00:00:12Z', 'usage': {'input_tokens': 2, 'output_tokens': 3, 'cache_read_input_tokens': 4, 'cache_creation_input_tokens': 5},
               'latency_ms': 20, 'ttfb_ms': 10, 'label': 'PRIVATE_SENTINEL', 'authorization': 'PRIVATE_SENTINEL'}
        record, content, local = pool_to_spec.convert(row, task, 0, 'test-stream', None)
        text = p.canonical([record, content]).decode()
        self.assertNotIn('PRIVATE_SENTINEL', text)
        self.assertNotIn(task, text)
        self.assertEqual(record['attributes']['gen_ai.usage.input_tokens'], 11)
        self.assertNotIn('gen_ai.response.model', record['attributes'])
        self.assertEqual(record['timing']['observed_at'], '2026-10-04T00:00:00Z')
        digest = p.commitment('response', row['response'].encode(), bytes.fromhex(local['response']['nonce_hex']))
        self.assertEqual(digest, record['content']['response']['commitment'])
        with self.assertRaises(ValueError): pool_to_spec.convert(row, 'y' * 120, 0, 'test-stream', None)

    def test_unsigned_or_historical_live_eligibility_rejected(self):
        changed = copy.deepcopy(self.events[0]); changed['market']['eligible'] = True; p.seal_record(changed)
        with self.assertRaises(jsonschema.ValidationError): p.validate(changed)
        self.bundles[0]['mode'] = 'proposal'; self.rebind(self.bundles[0])
        self.assertIsNone(self.run_choice()['winner'])

    def test_poisoned_bundle_is_rejected_without_stopping_valid_batch(self):
        poisoned = copy.deepcopy(self.bundles[1]); poisoned['injected_raw_content'] = 'PRIVATE_SENTINEL'; p.seal_record(poisoned)
        result = self.run_choice(bundles=[poisoned, self.bundles[0]])
        self.assertEqual(result['winner'], 'bundle-null-preservation')
        self.assertEqual(result['rejected'][0]['reason'], 'invalid schema')
        self.assertNotIn('PRIVATE_SENTINEL', json.dumps(result))

    def test_higher_claimed_gain_does_not_win(self):
        result = self.run_choice()
        self.assertEqual(result['winner'], 'bundle-null-preservation')
        self.assertEqual(result['settled_microusd'], 0)

    def test_front_running_guard_cannot_be_switched_off(self):
        bundle = self.bundles[0]; bundle['kind'] = 'backrun-review'; self.rebind(bundle)
        self.assertIsNone(self.run_choice()['winner'])
        bundle['inclusion']['after_release'] = True; self.rebind(bundle)
        result = self.run_choice()
        self.assertIsNone(result['winner'])
        self.assertIn('sealed result', result['rejected'][0]['reason'])

    def test_budget_and_rubric_cannot_be_replaced_by_searcher(self):
        for field in ('max_model_calls', 'max_microusd'):
            original = copy.deepcopy(self.bundles[0])
            self.bundles[0]['budget'][field] = 1; self.rebind(self.bundles[0])
            self.assertIsNone(self.run_choice()['winner'])
            self.bundles[0] = original; self.rebind(original)
        self.bundles[0]['valuation']['rubric_hash'] = 'a' * 64; self.rebind(self.bundles[0])
        self.assertIsNone(self.run_choice()['winner'])

    def test_expiry_and_builder_intersection(self):
        self.policy['epoch'] = 2
        self.assertIsNone(self.run_choice()['winner'])
        self.policy['epoch'] = 1
        changed = copy.deepcopy(self.events[0]); changed['disclosure']['permitted_builders'] = ['another-builder']; p.seal_record(changed)
        self.eventmap[changed['event_id']] = changed
        for bundle in self.bundles:
            bundle['source_event_hashes'] = [changed['integrity']['record_hash']]; self.rebind(bundle)
        self.assertIsNone(self.run_choice()['winner'])

    def test_principal_quota_and_conflicted_reviewer(self):
        duplicate = copy.deepcopy(self.bundles[0]); duplicate['bundle_id'] = 'duplicate'; p.seal_record(duplicate)
        result = self.run_choice(bundles=[self.bundles[0], duplicate])
        self.assertEqual(result['rejected'][0]['reason'], 'principal quota exceeded')
        self.evals[self.bundles[0]['bundle_id']]['reviewer_id'] = self.bundles[0]['searcher_id']
        self.assertIsNone(self.run_choice()['winner'])

    def test_dag_cycle_rebate_floor_and_payout_conservation(self):
        bundle = self.bundles[0]; bundle['body'][0]['depends_on'] = ['propose-fix']; self.rebind(bundle)
        self.assertIsNone(self.run_choice()['winner'])
        bundle['body'][0]['depends_on'] = []
        bundle['rebates']['trace_originator_bps'] = 1000; bundle['rebates']['searcher_bps'] = 7000; self.rebind(bundle)
        self.assertIsNone(self.run_choice()['winner'])
        for amount in (0, 1, 7, 1000001):
            self.assertEqual(sum(p.split_payment(amount, bundle['rebates']).values()), amount)
        with self.assertRaises(ValueError): p.split_payment(1, {'a': 9000})


if __name__ == '__main__': unittest.main()
