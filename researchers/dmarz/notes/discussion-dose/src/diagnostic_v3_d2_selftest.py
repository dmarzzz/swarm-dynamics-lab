"""Offline D2 software checks. No model call, no network, no retained Q0 records."""
import copy
from collections import Counter
from datetime import datetime, timezone, timedelta
import io
import json
from pathlib import Path
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
import urllib.error

import diagnostic_v3_d2 as d
from bench_v3.contracts import strict_json
from bench_v3.journal import read_events
from bench_v3.worlds import make_case
from tasks import digest

KEY = {'SWARM_MODEL_API_KEY': 'unit-test-sentinel'}


def fixture():
    """A frozen-manifest stand-in built without git, network or retained records."""
    rows = d.schedule()
    frozen = {'schema': d.VERSION, 'attempt': d.ATTEMPT, 'parent_attempt': d.PARENT, 'schedule': rows,
              'source_hashes': d.source_hashes(), 'source_commit': '0' * 40, 'launch_owner': 'dmarz/v3-d2-opus',
              'public_plan': {'url': 'https://example.invalid/plan', 'sha256': '0' * 64},
              'reservation_by_model_microusd': {m: sum(r['reservation_microusd'] for r in rows if r['model'] == m) for m in d.MODELS},
              'compatibility_probe': d.probe_record(),
              'worst_case_reservation_microusd': sum(r['reservation_microusd'] for r in rows) + d.probe_record()['reservation_microusd']}
    return frozen, {r['item']: r for r in d.items()}


class NativeMock(d.ScriptedD2):
    """Stands in for a dispatched provider: sets the model, usage and raw text."""
    scientific = True

    def __init__(self, model, behavior='oracle', usage=True, returned=None):
        super().__init__(behavior); self.model = model; self.usage = usage; self.returned = returned or model

    def complete(self, request):
        answer = super().complete(request)
        self.last_model = self.returned
        self.last_usage = {'input_tokens': 300, 'output_tokens': 10} if self.usage else {}
        self.last_response_text = json.dumps(answer)
        return answer


def run(providers, scientific, **kwargs):
    frozen, inputs = fixture()
    folder = tempfile.TemporaryDirectory(); root = Path(folder.name)
    ledger = root / 'ledger'; ledger.mkdir()
    result = d.execute(frozen, inputs, root / 'out', ledger, providers, scientific, **kwargs)
    return folder, root, frozen, inputs, result


def scripted(behavior):
    return {m: d.ScriptedD2(behavior) for m in d.MODELS}


def native(behavior='oracle', **kwargs):
    return {m: NativeMock(m, behavior, **kwargs) for m in d.MODELS}


class FakeResponse(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def api(content, stop='end_turn', model=d.OPUS, usage=None, **extra):
    usage = {'input_tokens': 250, 'output_tokens': 40} if usage is None else usage
    return FakeResponse(json.dumps({'model': model, 'stop_reason': stop, 'content': content, 'usage': usage, **extra}).encode())


class D2Tests(unittest.TestCase):
    # ------------------------------------------------------------ facts, labels, leakage
    def test_canonical_table_matches_generator_and_holds_values_only(self):
        table = d.canonical_table()
        self.assertEqual([w['world'] for w in table['worlds']], list(d.WORLDS))
        self.assertEqual(sum(len(w['facts']) for w in table['worlds']), 48)
        self.assertEqual(Counter(w['family'] for w in table['worlds']), {'capacity': 2, 'total_cost': 2, 'dependency': 2})
        for w in table['worlds']:
            self.assertEqual(set(w), {'world', 'family', 'instructions', 'rules', 'options', 'facts'})
            case = make_case(w['world'], 'resolvable' if w['world'] <= 20003 else 'ambiguous')
            self.assertEqual(w['facts'], case['truth']); self.assertEqual(w['instructions'], case['task']['instructions'])
            self.assertEqual(w['rules'], case['task']['rules'])

    def test_eighteen_option_predicates_by_direct_arithmetic(self):
        labels = d.gold(); feasible = infeasible = 0
        for w in d.canonical_table()['worlds']:
            r = w['rules']
            for option in d.OPTIONS:
                v = {k.split('.')[1]: x for k, x in w['facts'].items() if k.startswith(option + '.')}
                if w['family'] == 'capacity': direct = v['power'] >= r['power_min'] and v['access'] <= r['access_max']
                elif w['family'] == 'total_cost': direct = v['base'] + v['freight'] <= r['budget'] and v['days'] <= r['deadline']
                else: direct = v['direct'] >= r['required'] or (v['backup'] == 1 and v['transfer'] <= r['transfer_max'])
                self.assertEqual(labels[w['world']]['feasible'][option], direct)
                self.assertEqual(d.text_predicate(w['instructions'], v), direct)
                feasible += direct; infeasible += not direct
            self.assertEqual([o for o in d.OPTIONS if labels[w['world']]['feasible'][o]], [labels[w['world']]['winner']])
        self.assertEqual((feasible, infeasible), (6, 12))
        self.assertEqual([labels[w]['winner'] for w in d.WORLDS], ['A', 'A', 'C', 'C', 'C', 'B'])

    def test_no_evaluator_label_or_prior_output_in_any_actor_input(self):
        rows = d.items(); self.assertEqual(len(rows), 24)
        for row in rows:
            request = row['request']; d.reject_gold(request)
            self.assertEqual(set(request), {'phase', 'context'})
            task = request['context']['task']
            if row['probe'] == 'decision':
                self.assertEqual(set(request['context']), {'task', 'facts'})
                self.assertEqual(set(task), {'family', 'instructions', 'rules', 'options'})
                self.assertEqual(len(request['context']['facts']), 6 if task['family'] == 'capacity' else 9)
            else:
                self.assertEqual(set(request['context']), {'task', 'option', 'facts'})
                self.assertEqual(set(task), {'family', 'instructions', 'rules'})
                self.assertTrue(all(k.startswith(row['option'] + '.') for k in request['context']['facts']))
            text = json.dumps(request)
            for word in ('catalog', 'domains', 'documents', 'claims', 'truth', 'winner', 'target', 'source_policy'):
                self.assertNotIn(word, text)
        for bad in ({'context': {'gold': 'A'}}, {'context': {'task': {'winner': 'A'}}}, {'x': [{'feasible': True}]},
                    {'context': {'documents': []}}, {'evidence_allowed_choices': ['A']}):
            with self.assertRaises(ValueError): d.reject_gold(bad)
        # Every option appears exactly once in the atomic set, and all three in each decision.
        self.assertEqual(sorted((r['world'], r['option']) for r in rows if r['probe'] == 'feasibility'),
                         [(w, o) for w in d.WORLDS for o in d.OPTIONS])

    # ------------------------------------------------------------ pairing and order
    def test_schedule_pairs_order_and_allocation(self):
        rows = d.schedule(); self.assertEqual(rows, d.schedule()); self.assertTrue(d.check_schedule(rows))
        self.assertEqual(len(rows), 72)
        self.assertEqual(Counter(r['model'] for r in rows), {m: 24 for m in d.MODELS})
        for model in d.MODELS:
            self.assertEqual(Counter(r['probe'] for r in rows if r['model'] == model), {'decision': 6, 'feasibility': 18})
        by_item = {}
        for r in rows: by_item.setdefault(r['item'], []).append(r)
        self.assertEqual(len(by_item), 24)
        for group in by_item.values():
            self.assertEqual(len({r['request_sha256'] for r in group}), 1)
            self.assertEqual([r['call_id'] for r in group], sorted(r['call_id'] for r in group))
            numbers = [int(r['call_id'][3:]) for r in group]; self.assertEqual(numbers, list(range(numbers[0], numbers[0] + 3)))
        for position in range(3):
            self.assertEqual(Counter(g[position]['model'] for g in by_item.values()), {m: 8 for m in d.MODELS})
        haiku_first = sum([r['model'] for r in g].index(d.HAIKU) < [r['model'] for r in g].index(d.SONNET) for g in by_item.values())
        self.assertEqual(haiku_first, 12)
        for probe, repeats in (('decision', 1), ('feasibility', 3)):
            orders = Counter(tuple(r['model'] for r in g) for g in by_item.values() if g[0]['probe'] == probe)
            self.assertEqual(set(orders.values()), {repeats}); self.assertEqual(len(orders), 6)
        # Frozen order: a change of interpreter or seed must not silently reorder the run.
        self.assertEqual(digest([(r['call_id'], r['item'], r['model']) for r in rows]), ORDER_DIGEST)
        broken = copy.deepcopy(rows); broken[0]['model'] = broken[1]['model']
        with self.assertRaises(ValueError): d.check_schedule(broken)
        with self.assertRaises(ValueError): d.check_schedule(rows[:-1])

    def test_reservation_is_inside_the_dollar_cap(self):
        rows = d.schedule(); totals = {m: sum(r['reservation_microusd'] for r in rows if r['model'] == m) for m in d.MODELS}
        self.assertLess(sum(totals.values()), d.BUDGET_CAP_USD * 1_000_000)
        for row in rows:
            s = d.SETTINGS[row['model']]; size = len(json.dumps(d.body(d.items()[0]['request'], row['model'])).encode())
            self.assertGreaterEqual(row['reservation_microusd'], s['max_output_tokens'] * s['output_usd_per_million'])
            self.assertGreater(size, 0)
        self.assertEqual({m: (s['input_usd_per_million'], s['output_usd_per_million']) for m, s in d.SETTINGS.items()},
                         {d.OPUS: (4, 20), d.SONNET: (3, 15), d.HAIKU: (1, 5)})

    # ------------------------------------------------------------ contracts
    def test_strict_response_contracts(self):
        self.assertEqual(d.validate({'vote': 'ABSTAIN'}, 'd2_decision'), {'vote': 'ABSTAIN'})
        self.assertEqual(d.validate({'feasible': False}, 'd2_feasibility'), {'feasible': False})
        for bad in ({'vote': 'D'}, {'vote': 'A', 'claims': {}}, {'vote': None}, {}, ['A'], {'feasible': True}, 'A'):
            with self.assertRaises(ValueError): d.validate(bad, 'd2_decision')
        for bad in ({'feasible': 1}, {'feasible': 'true'}, {'feasible': None}, {'feasible': True, 'vote': 'A'}, {}, {'vote': 'A'}):
            with self.assertRaises(ValueError): d.validate(bad, 'd2_feasibility')
        with self.assertRaises(ValueError): d.validate({'vote': 'A'}, 'ballot')
        with self.assertRaises(ValueError): strict_json('{"vote": "A", "vote": "B"}')
        for phase, key in (('d2_decision', 'vote'), ('d2_feasibility', 'feasible')):
            s = d.schema(phase); self.assertEqual((s['required'], s['additionalProperties'], list(s['properties'])), ([key], False, [key]))
        self.assertEqual(d.schema('d2_decision')['properties']['vote']['enum'], ['A', 'B', 'C', 'ABSTAIN'])
        self.assertEqual(d.schema('d2_feasibility')['properties']['feasible'], {'type': 'boolean'})

    def test_native_serialization_per_model(self):
        with patch.dict('os.environ', KEY): adapters = {m: d.provider(m, 5) for m in d.MODELS}
        self.assertIs(type(adapters[d.HAIKU]), d.Anthropic); self.assertIs(type(adapters[d.SONNET]), d.Anthropic)
        self.assertIs(type(adapters[d.OPUS]), d.OpusAdaptive)
        for row in d.items():
            request = row['request']; bodies = {m: adapters[m].request_body(request) for m in d.MODELS}
            for m in d.MODELS: self.assertEqual(bodies[m], d.body(request, m))
            # Comparison arms: D1 settings, model identity the only difference.
            self.assertEqual({**bodies[d.HAIKU], 'model': d.SONNET}, bodies[d.SONNET])
            for m in (d.HAIKU, d.SONNET):
                self.assertEqual(set(bodies[m]), {'model', 'system', 'messages', 'temperature', 'max_tokens', 'output_config'})
                self.assertEqual((bodies[m]['temperature'], bodies[m]['max_tokens']), (0, 2000))
                self.assertEqual(set(bodies[m]['output_config']), {'format'})
            # Opus arm: no sampling or thinking field, explicit effort, wider output ceiling, no fallback.
            opus = bodies[d.OPUS]
            self.assertEqual(set(opus), {'model', 'system', 'messages', 'max_tokens', 'output_config'})
            for absent in ('temperature', 'top_p', 'top_k', 'thinking', 'fallbacks', 'tools', 'tool_choice'): self.assertNotIn(absent, opus)
            self.assertEqual((opus['max_tokens'], opus['output_config']['effort']), (4000, 'medium'))
            # Actor-visible text and schema are identical for all three models.
            for m in d.MODELS:
                self.assertEqual(bodies[m]['system'], d.SYSTEM)
                self.assertEqual(bodies[m]['messages'], [{'role': 'user', 'content': json.dumps(request, sort_keys=True)}])
                self.assertEqual(bodies[m]['output_config']['format'], {'type': 'json_schema', 'schema': d.schema(request['phase'])})

    # ------------------------------------------------------------ Opus adapter boundary
    def opus(self, cap=5):
        with patch.dict('os.environ', KEY): return d.provider(d.OPUS, cap)

    def test_opus_adapter_reads_text_after_thinking_blocks(self):
        request = d.items()[1]['request']; thinking = {'type': 'thinking', 'thinking': '', 'signature': 's'}
        for content in ([thinking, {'type': 'text', 'text': '{"feasible": true}'}],
                        [{'type': 'text', 'text': '{"feasible": true}'}],
                        [thinking, {'type': 'redacted_thinking', 'data': 'x'}, {'type': 'text', 'text': '{"feasible": true}'}]):
            adapter = self.opus()
            with patch('urllib.request.urlopen', return_value=api(content)) as call:
                self.assertEqual(adapter.complete(request), {'feasible': True})
            sent = json.loads(call.call_args[0][0].data)
            self.assertEqual(sent, d.body(request, d.OPUS)); self.assertNotIn('temperature', sent)
            self.assertEqual((adapter.calls, adapter.last_model, adapter.last_usage), (1, d.OPUS, {'input_tokens': 250, 'output_tokens': 40}))
            self.assertAlmostEqual(adapter.actual_cost_usd, (250 * 4 + 40 * 20) / 1e6); self.assertEqual(adapter.usage_missing_calls, 0)

    def test_opus_adapter_failures_are_classified_and_never_retried(self):
        request = d.items()[1]['request']; text = {'type': 'text', 'text': '{"feasible": true}'}
        cases = [(api([text, text]), 'provider_malformed_output'),
                 (api([text, {'type': 'thinking', 'thinking': ''}]), 'provider_malformed_output'),
                 (api([{'type': 'tool_use', 'id': 'x', 'name': 'n', 'input': {}}, text]), 'provider_malformed_output'),
                 (api([]), 'provider_malformed_output'),
                 (api([{'type': 'text', 'text': '{"feasible": true}' + ' ' * 4000}]), 'provider_malformed_output'),
                 (api([{'type': 'thinking', 'thinking': ''}], stop='max_tokens'), 'provider_incomplete'),
                 (api([], stop='refusal', stop_details={'type': 'refusal', 'category': 'bio'}), 'provider_schema_refusal'),
                 (api([text], usage={'input_tokens': 1, 'output_tokens': 1, 'cache_read_input_tokens': 5}), 'provider_accounting_error'),
                 (api([{'type': 'text', 'text': '{"feasible": true, "feasible": false}'}]), 'provider_malformed_output')]
        for response, reason in cases:
            adapter = self.opus()
            with patch('urllib.request.urlopen', return_value=response) as call:
                with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
            self.assertEqual(d.safe_failure(caught.exception)['reason'], reason)
            self.assertEqual((call.call_count, adapter.calls), (1, 1))
        # A refusal is its own category with an allowlisted class; a truncated answer is not a refusal.
        adapter = self.opus()
        with patch('urllib.request.urlopen', return_value=api([], stop='refusal', stop_details={'type': 'refusal', 'category': 'bio', 'explanation': 'private text'})):
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual((caught.exception.public_reason, adapter.last_stop_reason, adapter.last_refusal_category), ('provider_schema_refusal', 'refusal', 'bio'))
        with patch('urllib.request.urlopen', return_value=api([], stop='refusal', stop_details={'category': 'https://private.invalid'})):
            with self.assertRaises(d.ProviderFailure): adapter.complete(request)
        self.assertEqual(adapter.last_refusal_category, 'other')
        with patch('urllib.request.urlopen', return_value=api([{'type': 'thinking', 'thinking': ''}], stop='max_tokens')):
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual((caught.exception.public_reason, adapter.last_stop_reason, adapter.last_refusal_category), ('provider_incomplete', 'max_tokens', None))
        adapter = self.opus()
        error = urllib.error.HTTPError('https://private.invalid', 400, 'secret', {}, io.BytesIO(b'{"error": {"message": "temperature is not supported"}}'))
        with patch('urllib.request.urlopen', side_effect=error):
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual(d.safe_failure(caught.exception), {'reason': 'provider_http_error', 'http_status_class': '4xx'})
        self.assertNotIn('secret', str(caught.exception)); self.assertEqual(adapter.usage_missing_calls, 1)
        adapter = self.opus()
        with patch('urllib.request.urlopen', side_effect=TimeoutError('private')):
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual(d.safe_failure(caught.exception)['reason'], 'provider_timeout'); self.assertEqual(adapter.calls, 1)

    def test_adapter_call_and_dollar_limits(self):
        request = d.items()[1]['request']; text = [{'type': 'text', 'text': '{"feasible": true}'}]
        adapter = self.opus()
        with patch('urllib.request.urlopen', side_effect=lambda *a, **k: api(text)):
            for _ in range(24): adapter.complete(request)
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual((caught.exception.public_reason, adapter.calls), ('provider_local_limit', 24))
        adapter = self.opus(cap=0.1)  # one reservation is about USD 0.089
        with patch('urllib.request.urlopen', side_effect=lambda *a, **k: api(text)) as call:
            adapter.complete(request)
            with self.assertRaises(d.ProviderFailure) as caught: adapter.complete(request)
        self.assertEqual((caught.exception.public_reason, call.call_count), ('provider_local_limit', 1))
        with patch.dict('os.environ', KEY): haiku = d.provider(d.HAIKU, 5)
        with patch('urllib.request.urlopen', return_value=api(text, model=d.HAIKU)) as call:
            self.assertEqual(haiku.complete(request), {'feasible': True})
        self.assertEqual(json.loads(call.call_args[0][0].data), d.body(request, d.HAIKU))
        with patch('urllib.request.urlopen', return_value=api([{'type': 'thinking', 'thinking': ''}] + text, model=d.HAIKU)):
            with self.assertRaises(d.ProviderFailure): haiku.complete(request)

    # ------------------------------------------------------------ compatibility probe
    def test_probe_is_synthetic_single_and_gates_the_batch(self):
        record = d.probe_record(); frozen, inputs = fixture()
        self.assertNotIn(record['request_sha256'], {r['request_sha256'] for r in frozen['schedule']})
        self.assertEqual((record['model'], record['calls'], record['counts_toward_results']), (d.OPUS, 1, False))
        d.reject_gold(d.PROBE_REQUEST)
        self.assertLess(frozen['worst_case_reservation_microusd'], d.BUDGET_CAP_USD * 1_000_000)
        text = [{'type': 'thinking', 'thinking': ''}, {'type': 'text', 'text': '{"feasible": true}'}]
        with tempfile.TemporaryDirectory() as folder, patch.dict('os.environ', KEY), \
                patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)), patch.object(d, 'validate_preflight', lambda *a: {}):
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir(); manifest = root / 'manifest.json'; d.write_new(manifest, frozen)
            with patch('urllib.request.urlopen', return_value=api(text)) as call:
                result = d.probe(manifest, None, None, ledger, root / 'probe.json')
            self.assertEqual((result['status'], result['physical_calls'], call.call_count), ('probe-passed', 1, 1))
            self.assertEqual(json.loads(call.call_args[0][0].data), d.body(d.PROBE_REQUEST, d.OPUS))
            receipt = d.validate_probe(frozen, manifest, root / 'probe.json')
            self.assertEqual((receipt['status'], receipt['response'], receipt['counts_toward_results']), ('valid', {'feasible': True}, False))
            # One probe per attempt: a second one is refused before any request is sent.
            with patch('urllib.request.urlopen', return_value=api(text)) as call:
                with self.assertRaises(FileExistsError): d.probe(manifest, None, None, ledger, root / 'probe2.json')
            self.assertEqual(call.call_count, 0)
            # A rejected setting (HTTP 400) blocks the batch and spends no assignment.
            other = root / 'ledger2'; other.mkdir()
            error = urllib.error.HTTPError('https://private.invalid', 400, 'secret', {}, io.BytesIO(b'{}'))
            with patch('urllib.request.urlopen', side_effect=error):
                result = d.probe(manifest, None, None, other, root / 'failed.json')
            self.assertEqual((result['status'], result['http_status_class']), ('probe-failed-batch-blocked', '4xx'))
            with self.assertRaises(ValueError): d.validate_probe(frozen, manifest, root / 'failed.json')
            self.assertFalse((other / 'v3-d2-a1.started.json').exists())
            for change in (dict(manifest_sha256='0' * 64), dict(returned_model='claude-opus-5'), dict(physical_calls=2),
                           dict(counts_toward_results=True), dict(request_sha256='0' * 64)):
                forged = root / ('forged-' + next(iter(change)) + '.json'); d.write_new(forged, {**d.read(root / 'probe.json'), **change})
                with self.assertRaises(ValueError): d.validate_probe(frozen, manifest, forged)
            # No probe after the batch has started.
            (ledger / 'v3-d2-a1.started.json').write_text('{}')
            with self.assertRaises(ValueError): d.probe(manifest, None, None, ledger, root / 'late.json')

    # ------------------------------------------------------------ controls and scoring
    def summary(self, providers, scientific=True):
        folder, root, frozen, inputs, result = run(providers, scientific)
        with folder: return read_events(root / 'out/events.jsonl'), d.read(root / 'out/summary.json'), result

    def test_known_answer_controls_discriminate(self):
        # always_feasible ranks all three options by the objective: by hand that picks the
        # true winner only in 20001 (18/18 power tie, A first) and 20004 (C has the most power).
        expected = {'oracle': (6, 18, 6, 12), 'always_infeasible': (0, 12, 0, 12), 'always_feasible': (2, 6, 6, 0), 'wrong_vote': (0, 18, 6, 12)}
        for behavior, (canonical, atomic, tp, tn) in expected.items():
            _, summary, result = self.summary(native(behavior))
            self.assertEqual((result['terminal'], result['physical_calls']), (72, 72))
            for model in d.MODELS:
                m = summary['models'][model]
                self.assertEqual((m['canonical']['correct'], m['atomic']['correct'], m['atomic']['true_positive'], m['atomic']['true_negative']),
                                 (canonical, atomic, tp, tn), behavior)
                self.assertEqual((m['atomic']['always_infeasible_baseline_correct'], m['atomic']['above_always_infeasible_baseline']), (12, atomic > 12))
                self.assertEqual(m['screen']['model_qualified'], False)
        _, oracle, _ = self.summary(native('oracle')); m = oracle['models'][d.OPUS]
        self.assertEqual(m['screen'], {'canonical_pass': True, 'atomic_pass': True, 'complete_valid_usage': True,
                                       'reading': 'both_screens_pass_nominate_separate_contract_test', 'model_qualified': False})
        self.assertEqual(m['composition'], {'derived_correct': 6, 'missing': 0, 'none_predicted_feasible': 0,
                                            'multiple_predicted_feasible': 0, 'disagrees_with_canonical_vote': 0, 'assigned': 6})
        self.assertEqual({f: (v['canonical_correct'], v['atomic_correct']) for f, v in m['families'].items()},
                         {'capacity': (2, 6), 'total_cost': (2, 6), 'dependency': (2, 6)})
        _, low, _ = self.summary(native('always_infeasible')); m = low['models'][d.SONNET]
        self.assertEqual((m['canonical']['abstain'], m['composition']['none_predicted_feasible'], m['composition']['derived_correct']), (6, 6, 0))
        self.assertEqual(m['screen']['reading'], 'atomic_fail_inspect_predicate_task_interface_semantics')
        _, high, _ = self.summary(native('always_feasible')); m = high['models'][d.HAIKU]
        self.assertEqual((m['atomic']['false_positive'], m['composition']['multiple_predicted_feasible']), (12, 6))
        self.assertEqual(m['canonical']['constraint_violation'] + m['canonical']['correct'], 6)
        _, wrong, _ = self.summary(native('wrong_vote')); m = wrong['models'][d.OPUS]
        self.assertEqual((m['canonical']['wrong_nonabstain'], m['canonical']['constraint_violation'], m['composition']['disagrees_with_canonical_vote']), (6, 6, 6))
        self.assertEqual(m['screen']['reading'], 'atomic_pass_canonical_fail_focus_on_decision_composition')
        self.assertEqual((m['screen']['canonical_pass'], m['screen']['atomic_pass']), (False, True))

    def test_canonical_pass_with_atomic_fail_is_reported_inconsistent(self):
        class Split(NativeMock):
            def complete(self, request):
                self.behavior = 'oracle' if request['phase'] == 'd2_decision' else 'always_infeasible'
                return super().complete(request)
        _, summary, _ = self.summary({m: Split(m) for m in d.MODELS}); m = summary['models'][d.OPUS]
        self.assertEqual((m['canonical']['correct'], m['atomic']['correct']), (6, 12))
        self.assertEqual(m['screen']['reading'], 'canonical_pass_atomic_fail_inconsistent_not_repaired')
        self.assertEqual((m['screen']['canonical_pass'], m['screen']['atomic_pass']), (True, False))

    def test_paired_items_and_model_differences(self):
        providers = {d.OPUS: NativeMock(d.OPUS, 'oracle'), d.SONNET: NativeMock(d.SONNET, 'always_infeasible'), d.HAIKU: NativeMock(d.HAIKU, 'always_feasible')}
        _, summary, _ = self.summary(providers); pairs = summary['paired_items']
        self.assertEqual(len(pairs), 24); self.assertEqual(Counter(p['probe'] for p in pairs), {'decision': 6, 'feasibility': 18})
        self.assertEqual(sum(p['opus_minus_sonnet'] for p in pairs), (6 + 18) - (0 + 12))
        self.assertEqual(sum(p['opus_minus_haiku'] for p in pairs), 24 - sum(p['correct'][d.HAIKU] for p in pairs))
        self.assertTrue(all(p['correct'][d.OPUS] == 1 for p in pairs))
        self.assertEqual(summary['observed_usage_cost_microusd'], 24 * (300 * 4 + 10 * 20) + 24 * (300 * 3 + 10 * 15) + 24 * (300 * 1 + 10 * 5))

    def test_scripted_rehearsal_is_never_a_screen_result(self):
        events, summary, result = self.summary({m: d.ScriptedD2(d.REHEARSAL_CONTROLS[m]) for m in d.MODELS}, scientific=False)
        self.assertEqual((result['terminal'], result['physical_calls']), (72, 0)); self.assertFalse(summary['scientific'])
        self.assertEqual({m: summary['models'][m]['atomic']['correct'] for m in d.MODELS}, {d.OPUS: 18, d.SONNET: 12, d.HAIKU: 6})
        for model in d.MODELS:
            m = summary['models'][model]
            self.assertEqual((m['screen']['canonical_pass'], m['screen']['atomic_pass'], m['screen']['reading']),
                             (False, False, 'scripted_rehearsal_not_model_evidence'))
            self.assertEqual((m['physical_calls_observed'], m['observed_usage_cost_microusd']), (0, 0))
        self.assertTrue(all(not e['record']['dispatched'] for e in events if e['kind'] == 'call_terminal'))

    # ------------------------------------------------------------ invalid, missing, accounting
    def test_invalid_and_missing_answers_are_never_correct(self):
        _, summary, _ = self.summary(native('malformed'))
        for model in d.MODELS:
            m = summary['models'][model]
            self.assertEqual((m['valid'], m['canonical']['invalid'], m['atomic']['invalid']), (0, 6, 18))
            self.assertEqual((m['canonical']['correct'], m['atomic']['correct'], m['composition']['missing']), (0, 0, 6))
            self.assertEqual(m['failures'], {'provider_malformed_output': 24})
            self.assertEqual(m['screen']['reading'], 'incomplete_or_invalid_no_screen_reading')
            self.assertTrue(all(w['canonical_correct'] is None and w['composition']['derived_choice'] is None for w in m['worlds']))
        self.assertTrue(all(p['opus_minus_haiku'] is None for p in summary['paired_items']))

    def test_one_invalid_atomic_answer_makes_that_derived_decision_missing(self):
        class OneBad(NativeMock):
            def complete(self, request):
                answer = super().complete(request)
                if request['phase'] == 'd2_feasibility' and request['context']['option'] == 'B' and '20003' in self.target:
                    if request['context']['facts'].get('B.direct') == 16: return {'feasible': 'no'}
                return answer
        providers = native(); bad = OneBad(d.OPUS); bad.target = '20003'; providers[d.OPUS] = bad
        _, summary, _ = self.summary(providers); m = summary['models'][d.OPUS]
        self.assertEqual((m['atomic']['invalid'], m['atomic']['correct'], m['composition']['missing'], m['composition']['derived_correct']), (1, 17, 1, 5))
        world = next(w for w in m['worlds'] if w['world'] == 20003)
        self.assertEqual((world['atomic_predictions']['B'], world['composition']['state'], world['composition']['derived_correct']), (None, 'missing', None))
        self.assertEqual((m['screen']['atomic_pass'], m['screen']['canonical_pass'], m['screen']['complete_valid_usage']), (False, False, False))
        self.assertEqual(summary['models'][d.SONNET]['screen']['atomic_pass'], True)

    def test_timeout_is_preserved_as_unknown_and_not_resubmitted(self):
        class Timeout(NativeMock):
            def complete(self, request):
                if self.calls == 3:
                    self.calls += 1; self.last_usage = {}; self.last_response_text = None; self.last_model = None
                    raise TimeoutError('https://private.invalid/secret')
                return super().complete(request)
        providers = native(); providers[d.SONNET] = Timeout(d.SONNET)
        events, summary, result = self.summary(providers)
        self.assertEqual((result['terminal'], result['physical_calls']), (72, 72)); self.assertEqual(providers[d.SONNET].calls, 24)
        failed = [e['record'] for e in events if e['kind'] == 'call_terminal' and e['record']['status'] != 'valid']
        self.assertEqual(len(failed), 1)
        self.assertEqual((failed[0]['status'], failed[0]['reason'], failed[0]['dispatch_state'], failed[0]['response']),
                         ('provider_failure', 'provider_timeout', 'outcome_unknown', None))
        self.assertNotIn('private', json.dumps(events))
        m = summary['models'][d.SONNET]
        self.assertEqual((m['valid'], m['usage_missing_calls'], m['actual_cost_complete']), (23, [failed[0]['call_id']], False))
        self.assertEqual(m['screen']['reading'], 'incomplete_or_invalid_no_screen_reading')
        self.assertEqual(len([e for e in events if e['kind'] == 'call_start']), 72)

    def test_missing_usage_is_unknown_cost_not_zero(self):
        providers = native(); providers[d.HAIKU] = NativeMock(d.HAIKU, usage=False)
        _, summary, _ = self.summary(providers); m = summary['models'][d.HAIKU]
        self.assertEqual((len(m['usage_missing_calls']), m['actual_cost_complete'], m['observed_usage_cost_microusd']), (24, False, 0))
        self.assertEqual((m['canonical']['correct'], m['screen']['canonical_pass'], m['screen']['complete_valid_usage']), (6, False, False))
        self.assertEqual(summary['models'][d.OPUS]['observed_usage_cost_microusd'], 24 * (300 * 4 + 10 * 20))

    def test_returned_model_mismatch_stops_dispatch(self):
        providers = native(); providers[d.OPUS] = NativeMock(d.OPUS, returned='claude-opus-5')
        events, summary, result = self.summary(providers)
        self.assertEqual(result['terminal'], 1 + [r['model'] for r in d.schedule()].index(d.OPUS))
        self.assertEqual([e['reason'] for e in events if e['kind'] == 'dispatch_stopped'], ['provider_model_mismatch'])
        m = summary['models'][d.OPUS]
        self.assertEqual((m['started'], m['valid'], m['unstarted'], m['failures']), (1, 0, 23, {'provider_model_mismatch': 1}))
        self.assertEqual(summary['assigned_calls'], 72)

    def test_stop_marker_and_deadline_keep_the_assigned_denominator(self):
        frozen, inputs = fixture()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir(); (ledger / 'v3-d2-a1.stop').write_text('stop')
            result = d.execute(frozen, inputs, root / 'out', ledger, native(), True)
            self.assertEqual((result['terminal'], result['assigned']), (0, 72))
            summary = d.read(root / 'out/summary.json')
            self.assertEqual({m: summary['models'][m]['unstarted'] for m in d.MODELS}, {m: 24 for m in d.MODELS})
        ticks = iter([0, 0, 10, 20, 4000, 4000])
        folder, root, frozen, inputs, result = run(native(), True, clock=lambda: next(ticks))
        with folder:
            self.assertEqual(result['terminal'], 3)
            self.assertEqual([e['reason'] for e in read_events(root / 'out/events.jsonl') if e['kind'] == 'dispatch_stopped'], ['deadline_or_owner_stop'])

    def test_duplicate_dispatch_is_refused_even_with_another_output(self):
        folder, root, frozen, inputs, _ = run(native(), True)
        with folder:
            marker = (root / 'ledger/v3-d2-a1.started.json').read_bytes(); again = native()
            with self.assertRaises(FileExistsError): d.execute(frozen, inputs, root / 'other', root / 'ledger', again, True)
            self.assertFalse((root / 'other').exists()); self.assertEqual(sum(p.calls for p in again.values()), 0)
            self.assertEqual((root / 'ledger/v3-d2-a1.started.json').read_bytes(), marker)
            with self.assertRaises(ValueError): d.execute(frozen, inputs, root / 'out', root / 'ledger', again, True)
            with self.assertRaises(ValueError): d.execute(frozen, inputs, root / 'third', root / 'absent-ledger', again, True)
            # The rehearsal marker is separate and cannot stand in for, or block, the paid attempt.
            d.execute(frozen, inputs, root / 'rehearsal', root / 'ledger', scripted('oracle'), False)
            self.assertTrue((root / 'ledger/v3-d2-a1-zero-model-rehearsal.started.json').exists())

    def test_rehearsal_cli_path_with_injected_failure(self):
        frozen, inputs = fixture()
        with tempfile.TemporaryDirectory() as folder, patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)):
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            result = d.rehearse(root / 'manifest.json', None, root / 'out', ledger, failure_call=5)
            self.assertEqual((result['terminal'], result['physical_calls']), (72, 0))
            rows = d.read(root / 'out/outcomes.json'); failed = [r for r in rows if r['status'] != 'valid']
            self.assertEqual([(r['call_id'], r['reason'], r['dispatch_state']) for r in failed], [('d2-005', 'provider_timeout', 'terminal')])
            self.assertEqual(d.audit(root / 'out', None)['outcomes_recomputed'], 72)
            with self.assertRaises(ValueError): d.rehearse(root / 'manifest.json', None, root / 'slow', ledger, delay=60)
            with self.assertRaises(ValueError): d.rehearse(root / 'manifest.json', None, root / 'bad', ledger, failure_call=72)

    # ------------------------------------------------------------ audit
    def test_audit_recomputes_and_detects_tampering(self):
        folder, root, frozen, inputs, _ = run(native(), True)
        with folder, patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)):
            out = root / 'out'; checked = d.audit(out, None)
            self.assertEqual((checked['ok'], checked['requests_verified'], checked['outcomes_recomputed']), (True, 72, 72))
            self.assertEqual(checked['summary'], d.read(out / 'summary.json'))
            original = (out / 'summary.json').read_text()
            (out / 'summary.json').write_text(original.replace('"correct": 6', '"correct": 5', 1))
            with self.assertRaises(ValueError): d.audit(out, None)
            (out / 'summary.json').write_text(original)
            lines = (out / 'events.jsonl').read_text().splitlines()
            index = next(i for i, line in enumerate(lines) if '"call_terminal"' in line)
            (out / 'events.jsonl').write_text('\n'.join(lines[:index] + [lines[index].replace('"feasible": true', '"feasible": false').replace('"vote": "A"', '"vote": "B"')] + lines[index + 1:]) + '\n')
            with self.assertRaises(ValueError): d.audit(out, None)
            (out / 'events.jsonl').write_text('\n'.join(lines[:-1]) + '\n')
            with self.assertRaises(ValueError): d.audit(out, None)
            partial = d.audit(out, None, allow_interrupted=True)
            self.assertEqual((partial['complete_journal'], partial['outcomes_recomputed']), (False, 72))

    def test_audit_rejects_a_rescored_but_internally_consistent_journal(self):
        frozen, inputs = fixture()
        class Flattering(NativeMock):
            pass
        folder, root, _, _, _ = run(native('wrong_vote'), True)
        with folder, patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)):
            out = root / 'out'; events = read_events(out / 'events.jsonl'); rebuilt = []; previous = '0' * 64
            for event in events:
                event = {k: v for k, v in event.items() if k != 'hash'}
                if event['kind'] == 'call_terminal' and event['record']['probe'] == 'decision':
                    event['record']['score']['evaluation'].update(correct=1, wrong_nonabstain=0, constraint_violation=0, feasible_choice=1)
                event['previous'] = previous; event['hash'] = digest(event); previous = event['hash']; rebuilt.append(event)
            (out / 'events.jsonl').write_text(''.join(json.dumps(e, sort_keys=True) + '\n' for e in rebuilt))
            with self.assertRaises(ValueError) as caught: d.audit(out, None)
            self.assertIn('score mismatch', str(caught.exception))

    # ------------------------------------------------------------ admission evidence
    def evidence(self, **changes):
        base = {'schema': 'd2-operator-preflight-v1', 'manifest_sha256': 'a' * 64, 'launch_owner': 'dmarz/v3-d2-opus',
                'server': d.SERVER, 'claim_id': d.CLAIM,
                'claim_until': (datetime.now(timezone.utc) + timedelta(hours=3)).isoformat(),
                'hub_run': 'discussion-dose-v3/v3-d2-a1', 'rehearsal_summary_sha256': 'b' * 64,
                'rehearsal_readback_verified': True, 'duplicate_refusal_verified': True, 'budget_cap_usd': 5,
                'reviewer': 'dmarz/fleet-monitor', 'review_kind': 'same-researcher-check-under-owner-waiver',
                'go_recorded_utc': datetime.now(timezone.utc).isoformat()}
        base.update(changes); return base

    def test_operator_evidence_fails_closed(self):
        self.assertEqual(d.operator_evidence(self.evidence(), 'a' * 64)['server'], 'sim-dmarz-3')
        bad = [dict(manifest_sha256='c' * 64), dict(server='sim-dmarz-5'), dict(claim_id='dmarz-discussion-d1'),
               dict(claim_until=(datetime.now(timezone.utc) + timedelta(minutes=30)).isoformat()),
               dict(hub_run='discussion-dose-v3/v3-d1-a1'), dict(rehearsal_summary_sha256=''),
               dict(rehearsal_readback_verified=False), dict(duplicate_refusal_verified='yes'), dict(budget_cap_usd=500),
               dict(review_kind='independent-review'), dict(reviewer=''), dict(schema='d1-owner-preflight-v1')]
        for change in bad:
            with self.assertRaises(ValueError): d.operator_evidence(self.evidence(**change), 'a' * 64)
        missing = self.evidence(); del missing['reviewer']
        with self.assertRaises(ValueError): d.operator_evidence(missing, 'a' * 64)
        with self.assertRaises(ValueError): d.operator_evidence({**self.evidence(), 'extra': 1}, 'a' * 64)

    def test_preflight_receipt_must_be_current_and_match(self):
        frozen, _ = fixture()
        with tempfile.TemporaryDirectory() as folder:
            manifest = Path(folder) / 'manifest.json'; d.write_new(manifest, frozen); sha = d.fingerprint(manifest)['sha256']
            def receipt(**changes):
                proof = {'schema': 'd2-preflight-pass-v1', 'manifest_sha256': sha, 'operator_evidence': self.evidence(manifest_sha256=sha),
                         'checked_utc': datetime.now(timezone.utc).isoformat(),
                         'available_models': {m: {'id': m, 'max_tokens': 64000} for m in d.MODELS},
                         'serialized_requests_verified': 72, 'worst_case_reservation_usd': frozen['worst_case_reservation_microusd'] / 1e6,
                         'budget_cap_usd': 5, 'model_calls_dispatched': 0,
                         'public_plan_verification': {'url': frozen['public_plan']['url'], 'sha256': frozen['public_plan']['sha256'],
                                                      'public_raw_hash_matches': True, 'public_page_markers_verified': True}}
                proof.update(changes); path = Path(folder) / f'p{len(list(Path(folder).iterdir()))}.json'; d.write_new(path, proof); return path
            self.assertEqual(d.validate_preflight(frozen, manifest, receipt())['schema'], 'd2-preflight-pass-v1')
            stale = (datetime.now(timezone.utc) - timedelta(minutes=31)).isoformat()
            for change in (dict(checked_utc=stale), dict(model_calls_dispatched=1), dict(serialized_requests_verified=48),
                           dict(available_models={d.OPUS: {}}), dict(worst_case_reservation_usd=1.0), dict(budget_cap_usd=500),
                           dict(public_plan_verification={'url': 'x', 'sha256': 'y', 'public_raw_hash_matches': True, 'public_page_markers_verified': True})):
                with self.assertRaises(ValueError): d.validate_preflight(frozen, manifest, receipt(**change))

    def test_model_metadata_check_is_a_get_and_requires_exact_ids(self):
        seen = []
        def fake(req, timeout=None):
            seen.append((req.get_method(), req.full_url, req.data))
            return FakeResponse(json.dumps({'id': req.full_url.rsplit('/', 1)[1], 'max_tokens': 64000}).encode())
        with patch.dict('os.environ', KEY), patch('urllib.request.urlopen', side_effect=fake):
            self.assertEqual(sorted(d.check_models()), sorted(d.MODELS))
        self.assertEqual([(m, u.rsplit('/', 2)[1], body) for m, u, body in seen], [('GET', 'models', None)] * 3)
        with patch.dict('os.environ', KEY), patch('urllib.request.urlopen', return_value=FakeResponse(b'{"id": "claude-opus-5"}')):
            with self.assertRaises(ValueError): d.check_models()
        with patch.dict('os.environ', {}, clear=True):
            with self.assertRaises(ValueError): d.check_models()

    # ------------------------------------------------------------ hub observer
    def test_hub_observer_reports_counters_and_honest_labels(self):
        calls = []
        class Run:
            def __init__(self, run, experiment, params): calls.append(('attach', run, experiment))
            def progress(self, step, total, message=None, **metrics): calls.append(('progress', step, total, message, metrics))
            def done(self, message=None, **metrics): calls.append(('done', message, metrics))
            def fail(self, message=None, **metrics): calls.append(('fail', message, metrics))
            def artifact(self, path, name=None): calls.append(('artifact', Path(path).name))
        state = {'status': 'running', 'params': {'manifest_sha256': 'm' * 64}}
        fake = types.SimpleNamespace(get_run=lambda run: state, Run=Run)
        with patch.dict(sys.modules, {'swarm_report': fake}):
            with self.assertRaises(ValueError): d.HubProgress('discussion-dose-v3/v3-d2-a1', 'm' * 64, False)
            with self.assertRaises(ValueError): d.HubProgress('discussion-dose-v3/v3-d2-a1-rehearsal', 'x' * 64, False)
            observer = d.HubProgress('discussion-dose-v3/v3-d2-a1-rehearsal', 'm' * 64, False)
            folder, root, frozen, inputs, _ = run({m: d.ScriptedD2(d.REHEARSAL_CONTROLS[m]) for m in d.MODELS}, False, observer=observer)
            with folder, patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)):
                observer.finish(root / 'out', d.audit(root / 'out', None))
                self.assertEqual(d.read(root / 'out/reporting.json'), {'observer_failures': 0})
                self.assertTrue((root / 'out/audit.json').exists())
            progress = [c for c in calls if c[0] == 'progress']
            self.assertEqual((progress[-1][1], progress[-1][2]), (72, 72))
            self.assertTrue(all('SCRIPTED REHEARSAL, NOT MODEL EVIDENCE' in c[3] for c in progress))
            self.assertEqual(progress[-1][4], {'assigned_calls': 72, 'started_calls': 72, 'terminal_calls': 72, 'physical_model_calls': 0,
                                               'invalid_calls': 0, 'observed_usage_cost_usd': 0.0, 'usage_missing_calls': 0, 'qualification_passed': 0})
            self.assertEqual([c[0] for c in calls if c[0] in ('done', 'fail')], ['done'])
            self.assertIn('Not model evidence', next(c for c in calls if c[0] == 'done')[1])
            self.assertIn('artifact-index.json', [c[1] for c in calls if c[0] == 'artifact'])
            calls.clear(); observer = d.HubProgress('discussion-dose-v3/v3-d2-a1', 'm' * 64, True)
            providers = native(); providers[d.OPUS] = NativeMock(d.OPUS, 'malformed')
            folder, root, frozen, inputs, _ = run(providers, True, observer=observer)
            with folder, patch.object(d, 'verify_manifest', lambda manifest, q0: (frozen, inputs)):
                observer.finish(root / 'out', d.audit(root / 'out', None))
            self.assertEqual([c[0] for c in calls if c[0] in ('done', 'fail')], ['fail'])
            final = next(c for c in calls if c[0] == 'fail')[2]
            self.assertEqual((final['invalid_calls'], final['physical_model_calls']), (24, 72))
            self.assertAlmostEqual(final['observed_usage_cost_usd'], 24 * (300 * 4 + 10 * 20 + 300 * 3 + 10 * 15 + 300 + 50) / 1e6)
            text = json.dumps([c for c in calls if c[0] in ('progress', 'done', 'fail')])
            for private in ('vote', 'feasible"', 'correct'): self.assertNotIn(private, text)


# Digest of the frozen (call id, item, model) order; identical on Python 3.9 and 3.12.
ORDER_DIGEST = '29bf22351c10b89deb151594a4993ddb058142213a70eda9574121fdbffb2bea'


if __name__ == '__main__': unittest.main()
