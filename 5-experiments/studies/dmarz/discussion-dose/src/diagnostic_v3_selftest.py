"""Offline D1 software fixtures; no saved Q0 substitutes and no model calls."""
import copy
from datetime import datetime, timezone, timedelta
import io
from itertools import product
import json
from pathlib import Path
import socket
import tempfile
import unittest
from unittest.mock import patch
import urllib.error

import diagnostic_v3 as d
from bench_v3.contracts import strict_json, validate
from bench_v3.failures import safe_failure
from bench_v3.journal import Journal, read_events
from bench_v3.policies import Scripted, anthropic
from bench_v3.portable_audit import summary_equal
from bench_v3.scoring import majority, quorum_state, merge, evaluate
from bench_v3.worlds import make_case, memory_fixtures
from providers import ProviderFailure
from tasks import digest


def fixtures():
    """Unit-only contexts from public development records, NOT real Q0 requests."""
    plan = d.read(d.DEFAULT_PLAN)
    memory = {f['id']: f for f in memory_fixtures()}
    inputs = {}
    for row in plan['selected']:
        if row['group'] == 'memory': context = memory[row['label']]['context']
        else:
            world = int(row['label'].split(':')[0])
            case = make_case(world, 'resolvable' if world <= 20003 else 'ambiguous')
            context = {'task': case['task'], 'documents': case['documents'],
                       'read_ledger': [r['id'] for r in case['documents']], 'reports': [], 'board': [], 'private_history': []}
        request = {'phase': row['phase'], 'context': context}
        inputs[row['q0_call_id']] = {'selected': {**row, 'request_sha256': digest(request)}, 'request': request}
    schedule = []
    for index, row in enumerate(plan['proposed_schedule']):
        request = inputs[row['q0_call_id']]['request']
        schedule.append({**row, 'call_id': f'd1-{index:03d}', 'request_sha256': digest(request),
                         'provider_body_sha256': digest(d.body(request, row['model'])), 'reservation_microusd': 50000})
    frozen = {'schema': d.VERSION, 'attempt': d.ATTEMPT, 'schedule': schedule, 'source_hashes': d.source_hashes(),
              'counts_per_model': {'diagnostic': 6, 'report_snapshot': 18, 'memory': 36},
              'source_commit': '0' * 40, 'launch_owner': 'dmarz/discussion-bench-v3',
              'public_plan': {'url': 'https://example.invalid/plan', 'sha256': '0' * 64},
              'worst_case_reservation_microusd': 6000000}
    return frozen, inputs


class NativeMock:
    scientific = True
    def __init__(self, model):
        self.model = model; self.calls = 0; self.last_usage = {}; self.last_response_text = None; self.last_model = None
    def complete(self, request):
        self.calls += 1
        answer = Scripted().complete(request)
        self.last_model = self.model
        self.last_usage = {'input_tokens': 100, 'output_tokens': 10}
        self.last_response_text = json.dumps(answer)
        return answer


class DiagnosticTests(unittest.TestCase):
    def test_all_625_fixed_electorates_and_counterfactuals(self):
        for votes in product(('A', 'B', 'C', 'ABSTAIN', None), repeat=3):
            ballots = [{'vote': v} if v else None for v in votes]
            state = quorum_state(ballots)
            count = {v: votes.count(v) for v in ('A', 'B', 'C')}
            expected = next((v for v in ('A', 'B', 'C') if count[v] >= 2), 'ABSTAIN')
            self.assertEqual(state['decision'], expected)
            complete = set()
            for replacements in product(('A', 'B', 'C', 'ABSTAIN'), repeat=votes.count(None)):
                it = iter(replacements); filled = [v if v else next(it) for v in votes]
                complete.add(next((v for v in ('A', 'B', 'C') if filled.count(v) >= 2), 'ABSTAIN'))
            self.assertEqual(state['completion_decisions'], sorted(complete))
            if expected != 'ABSTAIN': self.assertEqual(state['state'], 'majority')
            elif None in votes: self.assertEqual(state['state'], 'incomplete_no_quorum')

    def test_poisoned_memory_majority_survives_invalid_ballot(self):
        case = make_case(20001, 'resolvable')
        key = case['target_key']; corpus = copy.deepcopy(case['documents'])
        source = next(r for r in corpus if key in r['facts'])['id']
        claim = {'value': case['false_value'], 'sources': [source]}
        ballot = {'vote': case['target'], 'claims': {k: claim if k == key else None for k in case['truth']}}
        ballots = [ballot, None, ballot]; memory = merge(ballots)
        result = evaluate(case, corpus, ballots, memory, None, ballots)
        self.assertEqual(result['vote_target'], 1)
        self.assertEqual(result['memory_false_target'], 1)
        self.assertEqual(result['vote_target_completion_lower'], 1)

    def test_incomplete_no_quorum_not_evidence_abstention(self):
        case = make_case(20001, 'resolvable')
        result = evaluate(case, case['documents'], [None] * 3, [], None, [None] * 3)
        self.assertEqual(result['vote_incomplete_no_quorum'], 1)
        self.assertIsNone(result['vote_correct_abstain'])
        self.assertIsNone(result['vote_unnecessary_abstain'])
        self.assertEqual((result['vote_correct_completion_lower'], result['vote_correct_completion_upper']), (0, 1))

    def test_failure_allowlist_and_secret_class_names(self):
        class SecretURLClass(RuntimeError): pass
        failures = [(TimeoutError('https://private.example/key'), 'provider_timeout'),
                    (urllib.error.URLError(socket.timeout()), 'provider_timeout'),
                    (urllib.error.URLError('private.example/key'), 'provider_transport_error'),
                    (ProviderFailure('secret', 'provider_http_429'), 'provider_rate_limit'),
                    (ProviderFailure('secret', 'provider_credit_balance_low', 400), 'provider_credit_balance_low'),
                    (ProviderFailure('secret', 'provider_schema_refusal'), 'provider_schema_refusal'),
                    (ProviderFailure('secret', 'https://private.example/key'), 'provider_unknown'),
                    (SecretURLClass('secret'), 'provider_unknown'),
                    (ValueError('secret'), 'provider_malformed_output')]
        for exc, reason in failures:
            result = safe_failure(exc)
            self.assertEqual(result['reason'], reason)
            self.assertNotIn('secret', json.dumps(result).lower())
            self.assertNotIn('private', json.dumps(result))
        result = safe_failure(urllib.error.HTTPError('https://private.example', 503, 'secret', {}, io.BytesIO(b'secret')))
        self.assertEqual(result, {'reason': 'provider_http_error', 'http_status_class': '5xx'})

    def test_portable_only_approved_continuous_cell_aggregates(self):
        a = {'cells': {'x': {'metrics': {'memory_key_coverage': {'sum': 3.0, 'observed': 6, 'assigned': 6}}}}}
        b = copy.deepcopy(a); b['cells']['x']['metrics']['memory_key_coverage']['sum'] += 4.44e-16
        self.assertTrue(summary_equal(a, b))
        b['cells']['x']['metrics']['memory_key_coverage']['sum'] += 1e-6
        self.assertFalse(summary_equal(a, b))
        for name in ('observed', 'assigned'):
            b = copy.deepcopy(a); b['cells']['x']['metrics']['memory_key_coverage'][name] += 1
            self.assertFalse(summary_equal(a, b))
        self.assertFalse(summary_equal({'vote_correct': 1}, {'vote_correct': 0}))
        self.assertFalse(summary_equal({'cost': 1.0}, {'cost': 1.0 + 4.44e-16}))
        self.assertFalse(summary_equal({'request': {'x': 1.0}}, {'request': {'x': 1.0 + 4.44e-16}}))

    def test_native_request_model_is_only_difference_and_no_thinking(self):
        _, inputs = fixtures()
        with patch.dict('os.environ', {'SWARM_MODEL_API_KEY': 'unit-test-sentinel'}):
            providers = {m: anthropic(d.config(m, 500)) for m in d.MODELS}
        for item in inputs.values():
            request = item['request']; d.reject_gold(request)
            bodies = [providers[m].request_body(request) for m in d.MODELS]
            self.assertEqual(bodies[0], d.body(request, d.MODELS[0]))
            self.assertEqual({k: v for k, v in bodies[0].items() if k != 'model'},
                             {k: v for k, v in bodies[1].items() if k != 'model'})
            self.assertNotIn('thinking', bodies[0]); self.assertEqual(bodies[0]['temperature'], 0)
            self.assertEqual(bodies[0]['max_tokens'], 2000)

    def test_closed_holdout_gold_and_missing_saved_requests_rejected(self):
        with self.assertRaises(ValueError): d.reject_gold({'context': {'truth': {}}})
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaises(FileNotFoundError): d.saved_inputs(Path(folder), d.DEFAULT_PLAN)
        self.assertEqual(d.read(d.DEFAULT_PLAN)['holdout_opened'], False)

    def test_scripted_120_calls_journal_denominators_and_duplicate_guard(self):
        frozen, inputs = fixtures()
        with tempfile.TemporaryDirectory() as folder, patch('urllib.request.urlopen', side_effect=AssertionError('unit test network')):
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            providers = {m: Scripted() for m in d.MODELS}
            result = d.execute(frozen, inputs, root / 'out', ledger, providers, False)
            self.assertEqual(result['terminal'], 120); self.assertEqual(result['physical_calls'], 0)
            events = read_events(root / 'out/events.jsonl')
            self.assertEqual(len([e for e in events if e['kind'] == 'call_start']), 120)
            summary = d.read(root / 'out/summary.json')
            for row in summary['models'].values():
                self.assertEqual((row['assigned_calls'], row['terminal']), (60, 60))
                self.assertFalse(row['diagnostic_gate']['eligible_for_separate_fresh_qualification'])
            with self.assertRaises(FileExistsError):
                d.execute(frozen, inputs, root / 'alternate', ledger, providers, False)
            self.assertEqual([p.calls for p in providers.values()], [60, 60])

    def test_paid_mock_valid_response_audit_detects_resigned_score_and_raw_tampering(self):
        frozen, inputs = fixtures()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            result = d.execute(frozen, inputs, root / 'out', ledger, {m: NativeMock(m) for m in d.MODELS}, True, {'unit': True})
            self.assertEqual(result['physical_calls'], 120)
            with patch.object(d, 'verify_manifest', return_value=(frozen, inputs)):
                checked = d.audit(root / 'out', root, d.DEFAULT_PLAN)
                self.assertEqual(checked['outcomes_recomputed'], 120)
                events = read_events(root / 'out/events.jsonl')
                terminal = next(e for e in events if e['kind'] == 'call_terminal')
                terminal['record']['score']['evaluation']['parent_correct'] = 42
                self.resign(root / 'out/events.jsonl', events)
                with self.assertRaisesRegex(ValueError, 'score mismatch'): d.audit(root / 'out', root, d.DEFAULT_PLAN)

    def resign(self, path, events):
        previous = '0' * 64
        for seq, event in enumerate(events):
            event['seq'] = seq; event['previous'] = previous
            event['hash'] = digest({k: v for k, v in event.items() if k != 'hash'})
            previous = event['hash']
        path.write_text(''.join(json.dumps(e) + '\n' for e in events))

    def test_timeouts_keep_assigned_and_usage_unknown_no_retries(self):
        frozen, inputs = fixtures()
        class Timeout(NativeMock):
            def complete(self, request):
                self.calls += 1; self.last_usage = {}; raise TimeoutError('secret endpoint')
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            providers = {m: Timeout(m) for m in d.MODELS}
            d.execute(frozen, inputs, root / 'out', ledger, providers, True, {'unit': True})
            summary = d.read(root / 'out/summary.json')
            for row in summary['models'].values():
                self.assertEqual(row['failures']['provider_timeout'], 60)
                self.assertEqual(len(row['usage_missing_calls']), 60)
                self.assertFalse(row['actual_cost_complete'])
                self.assertEqual(row['groups']['diagnostic']['assigned'], 6)
                self.assertEqual(row['report_quorums'][0]['state'], 'incomplete_no_quorum')
            self.assertEqual([p.calls for p in providers.values()], [60, 60])
            self.assertNotIn('secret endpoint', (root / 'out/events.jsonl').read_text())

    def test_interrupted_call_is_unresolved_and_never_resubmitted(self):
        frozen, inputs = fixtures()
        class Interrupt(NativeMock):
            def complete(self, request): self.calls += 1; raise KeyboardInterrupt()
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            with self.assertRaises(KeyboardInterrupt):
                d.execute(frozen, inputs, root / 'out', ledger, {m: Interrupt(m) for m in d.MODELS}, True, {'unit': True})
            with patch.object(d, 'verify_manifest', return_value=(frozen, inputs)):
                checked = d.audit(root / 'out', root, d.DEFAULT_PLAN, True)
            self.assertEqual(checked['summary']['unresolved'], ['d1-000'])
            with self.assertRaises(FileExistsError):
                d.execute(frozen, inputs, root / 'other', ledger, {m: NativeMock(m) for m in d.MODELS}, True, {'unit': True})

    def test_model_mismatch_stops_without_fallback(self):
        frozen, inputs = fixtures()
        class Wrong(NativeMock):
            def complete(self, request):
                answer = super().complete(request); self.last_model = 'not-the-requested-model'; return answer
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            result = d.execute(frozen, inputs, root / 'out', ledger, {m: Wrong(m) for m in d.MODELS}, True, {'unit': True})
            self.assertEqual(result['terminal'], 1)
            summary = d.read(root / 'out/summary.json')
            self.assertEqual(summary['assigned_calls'], 120)
            self.assertEqual(sum(x['unstarted'] for x in summary['models'].values()), 119)

    def evidence(self):
        return {'schema': 'd1-owner-preflight-v1', 'manifest_sha256': '0' * 64,
                'launch_owner': 'dmarz/discussion-bench-v3', 'server': 'sim-discussion-d1',
                'claim_id': 'dmarz-discussion-d1', 'claim_until': (datetime.now(timezone.utc) + timedelta(hours=6)).isoformat(),
                'checks': {k: True for k in d.CHECKS}, 'evidence_sha256': '1' * 64,
                'shared_model_spend_usd': 4.387237, 'reserved_other_model_spend_usd': 0,
                'model_availability': list(d.MODELS), 'request_compatibility_verified': True,
                'lifecycle_mode': 'owner-controlled-local-cleanup', 'hub_run': 'discussion-dose-v3/v3-d1-a1'}

    def test_owner_mode_truthfully_allows_no_cloud_retrieval(self):
        e = self.evidence(); e['checks']['rehearsal_cloud_retrieval'] = False
        self.assertEqual(d.owner_evidence(e, '0' * 64)['lifecycle_mode'], 'owner-controlled-local-cleanup')
        e['lifecycle_mode'] = 'owner-controlled-always-on'
        with self.assertRaises(ValueError): d.owner_evidence(e, '0' * 64)

    def test_incomplete_rehearsal_expired_claim_and_wrong_server_fail_closed(self):
        for change in ('rehearsal_upload', 'claim_until', 'server', 'model_availability', 'manifest_sha256'):
            e = self.evidence()
            if change == 'rehearsal_upload': e['checks'][change] = False
            elif change == 'claim_until': e[change] = datetime.now(timezone.utc).isoformat()
            elif change == 'server': e[change] = 'sim-discussion-v3'
            elif change == 'model_availability': e[change] = ['other-model']
            else: e[change] = '2' * 64
            with self.assertRaises(ValueError): d.owner_evidence(e, '0' * 64)

    def test_hub_progress_no_actor_context_and_indexed_publish(self):
        from types import SimpleNamespace
        calls = []
        class Reporter:
            def progress(self, *args, **kwargs): calls.append(('progress', args, kwargs))
            def artifact(self, *args): calls.append(('artifact', args))
            def done(self, **kwargs): calls.append(('done', kwargs))
            def fail(self, **kwargs): calls.append(('fail', kwargs))
        sr = SimpleNamespace(get_run=lambda _: {'status': 'running', 'params': {'manifest_sha256': '0' * 64}}, Run=lambda *a: Reporter())
        frozen, inputs = fixtures()
        with tempfile.TemporaryDirectory() as folder, patch.dict('sys.modules', {'swarm_report': sr}):
            root = Path(folder); ledger = root / 'ledger'; ledger.mkdir()
            observer = d.HubProgress('discussion-dose-v3/v3-d1-a1-rehearsal', '0' * 64, False)
            d.execute(frozen, inputs, root / 'out', ledger, {m: Scripted() for m in d.MODELS}, False, observer=observer)
            observer.finish(root / 'out', {'ok': True})
            self.assertEqual(observer.terminal, 120)
            self.assertTrue(any(c[0] == 'artifact' for c in calls))
            index = d.read(root / 'out/upload/artifact-index.json')
            self.assertIn('events.jsonl', [e['name'] for e in index['files']])
            for call in calls:
                if call[0] == 'progress': self.assertNotIn('documents', json.dumps(call))


if __name__ == '__main__': unittest.main(verbosity=2)
