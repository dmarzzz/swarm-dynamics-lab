"""Offline selftests: no network, no model call. Run: python3 src/selftest.py"""
import gzip
import hashlib
import importlib.util
import io
import json
import os
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import yaml
from PIL import Image

import analyze
import chain
import coordinator
import manifest
import provider
import rehearse
import render
import sim
import study
import worker

D = study.design()
ENV = {'SWARM_MODEL_API_KEY': 'selftest-not-a-key', 'SWARM_MODEL_WORKSPACE_ID': 'selftest'}
VALUES = {str(i): None for i in range(6)}


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def message(text=None, model=None, stop='end_turn', content=None, usage=None):
    return {'id': 'msg_test', 'type': 'message', 'role': 'assistant', 'model': model or D['model'], 'stop_reason': stop,
            'usage': {'input_tokens': 1000, 'output_tokens': 300} if usage is None else usage,
            'content': content if content is not None else [
                {'type': 'thinking', 'thinking': '', 'signature': 'x'},
                {'type': 'text', 'text': text if text is not None else json.dumps({'values': VALUES})}]}


def http_error(code, retry_after=None):
    headers = {'retry-after': str(retry_after)} if retry_after is not None else {}
    return urllib.error.HTTPError(provider.MESSAGES_URL, code, 'error', headers, io.BytesIO(b'{}'))


class Script:
    """An opener that plays a list of outcomes for the messages endpoint and answers every count."""
    def __init__(self, outcomes, count_outcomes=None):
        self.outcomes, self.count_outcomes = list(outcomes), list(count_outcomes or [])
        self.sent, self.timeouts = [], []

    def __call__(self, request, timeout=None):
        self.sent.append((request.full_url, json.loads(request.data), dict(request.header_items())))
        self.timeouts.append(timeout)
        if request.full_url == provider.COUNT_URL:
            item = self.count_outcomes.pop(0) if self.count_outcomes else {'input_tokens': 1000}
        else:
            item = self.outcomes.pop(0)
        if isinstance(item, BaseException):
            raise item
        return Resp(json.dumps(item).encode())

    def messages(self):
        return [s for s in self.sent if s[0] == provider.MESSAGES_URL]


class Clock:
    def __init__(self):
        self.now, self.sleeps = 0.0, []

    def __call__(self):
        return self.now

    def sleep(self, seconds):
        self.sleeps.append(seconds)
        self.now += seconds


def api(td, outcomes, count_outcomes=None, name='ledger'):
    clock = Clock()
    opener = Script(outcomes, count_outcomes)
    ledger = provider.Ledger(Path(td) / name)
    return provider.Anthropic(ledger, opener, clock=clock, sleep=clock.sleep), opener, clock, ledger


PACKET = {'skills': list(range(6)), 'reports': []}


class FakeRun:
    def __init__(self, hub, run_id, params):
        self.hub, self.id, self.params, self.attempt, self.experiment = hub, run_id, params, 1, study.EXPERIMENT
        self._finished = False

    def __enter__(self):
        self.hub.record[self.id]['status'] = 'running'
        return self

    def __exit__(self, et, ev, tb):
        if not self._finished:
            self.done() if et is None else self.fail(str(ev))
        return False

    def progress(self, *a, **k):
        return True

    def artifact(self, path, name=None):
        self.hub.record[self.id]['artifacts'][name or Path(path).name] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        return {'name': name}

    def _end(self, status, message, metrics):
        self._finished = True
        self.hub.record[self.id].update(status=status, message=message)
        self.hub.record[self.id]['metrics'].update(metrics)

    def done(self, message=None, **metrics):
        self._end('done', message, metrics)

    def fail(self, message=None, **metrics):
        self._end('failed', message, metrics)


class FakeHub:
    """In-memory stand-in for the hub client module (register, enqueue, runs, next_run, get_run)."""
    def __init__(self):
        self.record, self.queue, self.registered = {}, [], []

    def register(self, experiment, **spec):
        self.registered.append(experiment)

    def runs(self, experiment=None, status=None, limit=200):
        return [{'run': k, 'params': v['params'], 'status': v['status'], 'metrics': v['metrics']} for k, v in self.record.items()]

    def enqueue(self, experiment, params_list, tags=None, **k):
        ids = []
        for p in params_list:
            run_id = f'{experiment}/{len(self.record):04d}'
            self.record[run_id] = {'params': dict(p), 'status': 'planned', 'metrics': {}, 'artifacts': {}}
            self.queue.append(run_id)
            ids.append(run_id)
        return ids

    def next_run(self, experiment=None):
        if not self.queue:
            return None
        run_id = self.queue.pop(0)
        self.record[run_id]['status'] = 'assigned'
        return FakeRun(self, run_id, dict(self.record[run_id]['params']))

    def get_run(self, run_id):
        r = self.record.get(run_id)
        return r and {'run': run_id, 'status': r['status'], 'metrics': r['metrics'], 'params': r['params'],
                      'artifacts': [{'name': n, 'sha256': h} for n, h in r['artifacts'].items()]}


def hub_run(stage, status='done', invalid=0, passed=1, source_hash=None, batch=None):
    p = study.params(stage)
    return {'params': {**p, 'source_hash': source_hash or p['source_hash'], 'batch': batch or p['batch']},
            'status': status, 'metrics': {'invalid': invalid, 'qualification_passed': passed}}


def synthetic_rows(outcomes):
    """Minimal S1-shaped rows for the primary cells: outcomes[c][task] is a rare accuracy or None (missing)."""
    rows = []
    p = D['primary_contrast']
    for c, by_task in outcomes.items():
        for task, value in by_task.items():
            r = {'kind': 'pilot', 'task': task, 'carriers': c, 'checks': p['checks'], 'attacker_pass': p['attacker_pass'],
                 'arm': p['arm'], 'id': f'{c}-{task}', 'packet_hash': f'h{c}-{task}', 'admitted_hash': f'a{task}',
                 'audit_hash': f'u{task}', 'order_hash': f'o{task}', 'status': 'completed' if value is not None else 'not_started',
                 'scripted_evaluation': {'rare_accuracy': 0.0},
                 'diagnostics': {'truth_available': 1.0, 'carrier_survival': 0.5, 'all_three_survive': True,
                                 'original_outside_retention': 0.5, 'attacker_seat_share': 0.1, 'false_seat_share': 0.1,
                                 'original_outside_admitted': 120, 'attacker_admitted': 48, 'carriers_admitted_per_fact': [1, 1, 1],
                                 'rare_truthful_reports': {'3': 1, '4': 1, '5': 1}, 'rare_false_reports': {'3': 16, '4': 16, '5': 16}}}
            if value is not None:
                r['evaluation'] = {'rare_accuracy': value, 'task_accuracy': value, 'rare_wrong': 1 - value, 'rare_null': 0.0,
                                   'correct': [True] * 6}
            rows.append(r)
    return rows


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.pilot = {rate: study.pilot_assignments(7790, rate) for rate in D['attacker_pass']}
        cls.rows = []
        for rate in D['attacker_pass']:
            for a in cls.pilot[rate][2]:
                r = {k: a[k] for k in study.ROW_KEYS}
                answer = study.scripted(a['packet'])
                r.update(status='completed', answer=answer, evaluation=study.evaluate(a, answer),
                         scripted_evaluation=study.evaluate(a, answer), accounting={'attempted': False, 'actual_usd': 0},
                         elapsed_seconds=1.0, study_accounting={})
                cls.rows.append(r)

    # ---------------------------------------------------------------- instrument and manipulation

    def test_simulator_matches_parent_at_972(self):
        psim, pstudy, hashes = study.load_parent()
        self.assertEqual(hashes['sim'], D['parent']['sim_sha256'])
        self.assertEqual(hashes['study'], D['parent']['study_sha256'])
        self.assertIsNot(psim, sim)
        pcfg = pstudy.cfg_for(972)
        for key in ('core', 'community', 'admission_seats', 'pagerank_restart', 'pagerank_iterations', 'honest_check_pass'):
            self.assertEqual(pcfg[key], study.cfg()[key])
        for rate in D['attacker_pass']:
            world = self.pilot[rate][0]
            parent = psim.make_world(7790, 27, rate, False, pcfg)
            self.assertEqual(parent, world)
            self.assertEqual(psim.checkpoints(parent, D['audit_checks'], D['arms'], pcfg),
                             sim.checkpoints(world, D['audit_checks'], D['arms'], study.cfg()))

    def test_c81_packet_byte_identical_to_parent_code(self):
        psim, pstudy, _ = study.load_parent()
        pcfg = pstudy.cfg_for(972)
        compared = 0
        for task in D['engineering_worlds']:
            for rate in D['attacker_pass']:
                rows = self.pilot[rate][2] if task == 7790 else study.pilot_assignments(task, rate)[2]
                mine = {(a['arm'], a['checks']): a for a in rows if a['carriers'] == 81}
                parent = psim.make_world(task, 27, rate, False, pcfg)
                for rec in psim.checkpoints(parent, D['audit_checks'], D['arms'], pcfg):
                    theirs = pstudy.packet(parent, rec['admitted'], rec['passed'], 'visible', rec['arm'])
                    a = mine[(rec['arm'], rec['checks'])]
                    self.assertEqual(json.dumps(theirs, sort_keys=True).encode(), study.actor_text(a['packet']).encode())
                    self.assertEqual(pstudy.digest(theirs), a['packet_hash'])
                    # The user message the provider sends is the same bytes the parent provider sent.
                    self.assertEqual(provider.request_body(a['packet'])['messages'][0]['content'], json.dumps(theirs, sort_keys=True))
                    compared += 1
        self.assertEqual(compared, 24)

    def test_prompt_and_schema_equal_parent(self):
        src = study.ROOT.parent / 'sybil-scale-api' / 'src' / 'provider.py'
        _, pstudy, _ = study.load_parent()
        saved = sys.modules.get('study')
        sys.modules['study'] = pstudy
        try:
            spec = importlib.util.spec_from_file_location('parent_provider', src)
            parent = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(parent)
        finally:
            sys.modules['study'] = saved
        self.assertEqual(parent.SYSTEM, provider.SYSTEM)
        self.assertEqual(parent.SCHEMA, provider.SCHEMA)

    def test_all_s0_invariants_hold_on_an_engineering_root(self):
        result = study.pilot_invariants((7791, 0.9))
        self.assertTrue(all(result.values()), result)
        self.assertEqual(len(result), 12)
        fixtures = study.fixture_invariants()
        self.assertTrue(all(fixtures.values()), fixtures)

    def test_carriers_nested_uniform_seed_independent_of_strength(self):
        a, b = self.pilot[0.1][1], self.pilot[0.9][1]
        self.assertEqual(a, b)
        other = study.carrier_order(study.base_world(7791, 0.1))
        world = self.pilot[0.1][0]
        for s in study.RARE:
            self.assertEqual(len(set(a[s])), 81)
            self.assertNotEqual(a[s], sorted(a[s]))
            self.assertNotEqual(a[s], other[s])
            self.assertTrue(all(world['truth'][x]['specialist'] and world['public']['nodes'][x]['skill'] == s for x in a[s]))
            for small, large in zip(D['carriers'], D['carriers'][1:]):
                self.assertTrue(set(a[s][:small]) < set(a[s][:large]))
        # The permutation does not read audit or admission outcomes: tampering with them changes nothing.
        tampered = dict(world, checks={k: not v for k, v in world['checks'].items()})
        self.assertEqual(study.carrier_order(tampered), a)

    def test_audit_and_packet_order_identical_across_carrier_counts(self):
        for rate in D['attacker_pass']:
            cells = {}
            for a in self.pilot[rate][2]:
                cells.setdefault((a['arm'], a['checks']), []).append(a)
            self.assertEqual(len(cells), 6)
            for group in cells.values():
                self.assertEqual([a['carriers'] for a in group], D['carriers'])
                self.assertEqual(len({(a['admitted_hash'], a['audit_hash'], a['order_hash']) for a in group}), 1)
                self.assertEqual(len({json.dumps(a['verification_events']) for a in group}), 1)
                for a in group:
                    self.assertEqual(len(a['packet']['reports']), 486)
                    self.assertEqual([(r['node'], r['age'], r['activity'], r['verification']) for r in a['packet']['reports']],
                                     [(r['node'], r['age'], r['activity'], r['verification']) for r in group[0]['packet']['reports']])

    def test_actor_input_has_no_truth_ownership_or_carrier_role(self):
        for a in self.pilot[0.1][2]:
            self.assertTrue(study._leak_free(a['packet']))
            self.assertEqual(set(json.loads(study.actor_text(a['packet']))), {'skills', 'reports'})
        leaky = json.loads(json.dumps(self.pilot[0.1][2][0]['packet']))
        leaky['reports'][0]['honest'] = True
        self.assertFalse(study._leak_free(leaky))
        leaky = json.loads(json.dumps(self.pilot[0.1][2][0]['packet']))
        leaky['carriers'] = 1
        self.assertFalse(study._leak_free(leaky))

    def test_evaluator_grades_wrong_null_and_invalid_answers(self):
        a = self.pilot[0.1][2][0]
        truth = {'values': {str(s): a['answers'][s] for s in range(6)}}
        self.assertEqual(study.evaluate(a, truth)['rare_accuracy'], 1)
        wrong = {'values': {**truth['values'], '3': a['answers'][3] + 7}}
        graded = study.evaluate(a, wrong)
        self.assertAlmostEqual(graded['rare_accuracy'], 2 / 3)
        self.assertAlmostEqual(graded['rare_wrong'], 1 / 3)
        null = study.evaluate(a, {'values': {**truth['values'], '4': None}})
        self.assertAlmostEqual(null['rare_null'], 1 / 3)
        self.assertAlmostEqual(null['rare_accuracy'], 2 / 3)
        self.assertTrue(study._grading_ok(a))
        for vals in ({'0': True}, {str(i): True for i in range(6)}, {str(i): 1.5 for i in range(6)}, {str(i): '1' for i in range(6)}):
            with self.assertRaises(ValueError):
                study.validate({'values': vals})
        with self.assertRaises(ValueError):
            study.validate({'values': VALUES, 'extra': 1})

    def test_clean_fixtures_and_probe(self):
        q0 = study.assignments('Q0')
        self.assertEqual(len(q0), 48)
        self.assertEqual({a['task'] for a in q0}, set(D['qualification_worlds']))
        for profile in (1, 9, 81):
            group = [a for a in q0 if a['carriers'] == profile]
            self.assertEqual(len(group), 16)
            self.assertEqual(sum(a['withheld'] is not None for a in group), 8)
        self.assertEqual({s: sum(a['withheld'] == s for a in q0) for s in study.RARE}, {3: 8, 4: 8, 5: 8})
        for a in q0:
            reports = a['packet']['reports']
            self.assertEqual(len(reports), 486)
            self.assertTrue(all(r['claim'] == a['answers'][r['skill']] for r in reports))
            for s in study.RARE:
                self.assertEqual(sum(r['skill'] == s for r in reports), 0 if s == a['withheld'] else a['carriers'])
            self.assertEqual(a['expected'][str(a['withheld'])] if a['withheld'] else None, None)
            self.assertTrue(study.evaluate(a, study.scripted(a['packet']))['exact_packet'])
        p0 = study.assignments('P0')
        self.assertEqual(len(p0), 1)
        self.assertEqual((p0[0]['task'], p0[0]['carriers'], p0[0]['withheld'], p0[0]['kind']), (7790, 81, None, 'probe'))
        self.assertNotIn(7790, D['worlds'] + D['qualification_worlds'])

    def test_qualification_thresholds(self):
        q0 = study.assignments('Q0')

        def rows(mutate=None):
            out = []
            for i, a in enumerate(sorted(q0, key=lambda a: (a['carriers'], a['task'], str(a['withheld'])))):
                answer = study.scripted(a['packet'])
                r = {k: a[k] for k in study.ROW_KEYS}
                r['status'] = 'completed'
                if mutate:
                    answer = mutate(i, a, answer) or answer
                if answer == 'failed':
                    r['status'] = 'failed'
                else:
                    r['evaluation'] = study.evaluate(a, answer)
                out.append(r)
            return out
        self.assertTrue(study.qualification(rows())['passed'])
        # One wrong packet in a profile: 15/16 exact (0.9375) and 95/96 fields still pass.
        one = lambda i, a, ans: {'values': {**ans['values'], '0': 1}} if i == 0 else None
        self.assertTrue(study.qualification(rows(one))['passed'])
        # Two wrong packets in one profile: 14/16 exact = 0.875 fails.
        two = lambda i, a, ans: {'values': {**ans['values'], '0': 1}} if i in (0, 2) else None
        q = study.qualification(rows(two))
        self.assertFalse(q['passed'])
        self.assertEqual([g['passed'] for g in q['groups']], [False, True, True])
        # A value for a withheld rare fact fails the abstention rule even when everything else is right.
        first_withheld = next(i for i, a in enumerate(sorted(q0, key=lambda a: (a['carriers'], a['task'], str(a['withheld'])))) if a['withheld'])
        invent = lambda i, a, ans: {'values': {**ans['values'], str(a['withheld']): 55}} if i == first_withheld else None
        self.assertFalse(study.qualification(rows(invent))['passed'])
        # One structurally invalid call fails the gate.
        failed = lambda i, a, ans: 'failed' if i == 5 else None
        q = study.qualification(rows(failed))
        self.assertFalse(q['passed'])
        self.assertEqual(q['structurally_valid'], 47)
        self.assertFalse(study.qualification(rows()[:47])['passed'])

    def test_probe_gate(self):
        a = study.assignments('P0')[0]
        row = {k: a[k] for k in study.ROW_KEYS}
        good = dict(row, status='completed', evaluation=study.evaluate(a, study.scripted(a['packet'])), accounting={'usage_reported': True})
        self.assertTrue(study.probe_gate([good])['passed'])
        wrong = dict(good, evaluation=study.evaluate(a, {'values': {**study.scripted(a['packet'])['values'], '3': 1}}))
        self.assertFalse(study.probe_gate([wrong])['passed'])
        self.assertFalse(study.probe_gate([dict(good, status='failed')])['passed'])
        self.assertFalse(study.probe_gate([dict(good, accounting={})])['passed'])
        self.assertFalse(study.probe_gate([good, good])['passed'])
        self.assertFalse(study.probe_gate([])['passed'])

    def test_design_counts_splits_and_caps(self):
        groups = [set(D[k]) for k in ('worlds', 'qualification_worlds', 'engineering_worlds')]
        self.assertTrue(all(not a & b for i, a in enumerate(groups) for b in groups[i + 1:]))
        self.assertLess(max(set.union(*groups)), 10000)
        self.assertEqual(D['worlds'], list(range(7800, 7824)))
        self.assertEqual(D['qualification_worlds'], list(range(7900, 7908)))
        self.assertEqual(D['engineering_worlds'], [7790, 7791])
        cells = len(D['carriers']) * len(D['audit_checks']) * len(D['attacker_pass']) * len(D['arms'])
        self.assertEqual(cells, 60)
        self.assertEqual(D['stages']['S1']['assignments'], cells * len(D['worlds']))
        self.assertEqual(D['stages']['S0']['assignments'], cells * 2 + 48)
        b = D['budget']
        self.assertEqual(b['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 48, 'S1': 1440})
        self.assertEqual(b['max_attempted_calls'], 1489)
        self.assertEqual(sum(b['max_calls'].values()), b['max_attempted_calls'])
        self.assertEqual({s: D['stages'][s]['assignments'] for s in ('P0', 'Q0', 'S1')}, {'P0': 1, 'Q0': 48, 'S1': 1440})
        self.assertEqual((D['model'], D['effort'], b['max_output_tokens'], b['input_usd_per_million'], b['output_usd_per_million']),
                         ('claude-opus-5-5', 'low', 8000, 4, 20))
        self.assertEqual(b['retries'], 0)
        self.assertEqual([study.params(s)['batch'] for s in study.STAGES], ['s0-001', 'p0-001', 'q0-001', 's1-001'])
        self.assertGreaterEqual(b['chain_timeout_seconds'], b['stage_timeout_seconds'] + chain.DRAIN_SECONDS)

    # ---------------------------------------------------------------- provider and ledger

    def test_request_body_has_exactly_the_contract_keys(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, _, _ = api(td, [message()])
            answer, account = client.call(PACKET, 'p0-001:a')
        self.assertEqual(answer['values'], VALUES)
        (count_url, count_body, _), (url, body, headers) = opener.sent
        self.assertEqual(list(body), ['model', 'max_tokens', 'system', 'messages', 'output_config'])
        self.assertEqual(set(body), {'model', 'max_tokens', 'system', 'messages', 'output_config'})
        for forbidden in ('thinking', 'temperature', 'top_p', 'top_k', 'tool_choice', 'tools', 'fallbacks', 'stop_sequences', 'metadata'):
            self.assertNotIn(forbidden, body)
            self.assertNotIn(forbidden, count_body)
        self.assertEqual(body['model'], 'claude-opus-5-5')
        self.assertEqual(body['max_tokens'], 8000)
        self.assertEqual(set(body['output_config']), {'effort', 'format'})
        self.assertEqual(body['output_config']['effort'], 'low')
        self.assertEqual(body['output_config']['format'], {'type': 'json_schema', 'schema': provider.SCHEMA})
        self.assertEqual([m['role'] for m in body['messages']], ['user'])          # no assistant prefill
        self.assertEqual(body['messages'][0]['content'], json.dumps(PACKET, sort_keys=True))
        self.assertEqual(list(count_body), ['model', 'system', 'messages', 'output_config'])
        self.assertEqual((count_url, url), (provider.COUNT_URL, provider.MESSAGES_URL))
        self.assertEqual({k.lower() for k in headers}, {'content-type', 'x-api-key', 'anthropic-version', 'anthropic-workspace-id'})
        b = D['budget']
        self.assertEqual(account['actual_usd'], (1000 * b['input_usd_per_million'] + 300 * b['output_usd_per_million']) / 1e6)
        self.assertEqual(account['reserved_usd'], ((int(1000 * 1.02) + 64) * 4 + 8000 * 20) / 1e6)
        self.assertEqual((account['attempts'], account['count_attempts'], account['usage_reported']), (1, 1, True))

    def test_thinking_and_redacted_thinking_blocks_are_dropped(self):
        text = {'type': 'text', 'text': json.dumps({'values': {**VALUES, '0': 12}})}
        content = [{'type': 'thinking', 'thinking': '', 'signature': 'a'}, {'type': 'redacted_thinking', 'data': 'opaque'},
                   {'type': 'thinking', 'thinking': 'summary', 'signature': 'b'}, text]
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, _, _, _ = api(td, [message(content=content), message(content=[text, text]), message(content=[]),
                                       message(content=[{'type': 'tool_use', 'id': 't', 'name': 'x', 'input': {}}]),
                                       message(text='not json'), message(text=json.dumps({'values': {'0': 1}})),
                                       message(text=' ' * 501)])
            answer, _ = client.call(PACKET, 'q0-001:a')
            self.assertEqual(answer['values']['0'], 12)
            for i, category in enumerate(['invalid_structured_answer'] * 5 + ['answer_too_long']):
                with self.assertRaises(provider.CallFailure) as failure:
                    client.call(PACKET, f'q0-001:b{i}')
                self.assertEqual(failure.exception.category, category)
                self.assertTrue(failure.exception.accounting['usage_reported'])

    def test_refusal_and_other_response_failures_have_their_own_category(self):
        cases = [(message(stop='refusal', content=[]), 'refusal'), (message(stop='max_tokens'), 'nonterminal_output'),
                 (message(model='claude-opus-5'), 'model_mismatch'), (message(usage={}), 'missing_usage'),
                 (message(usage={'input_tokens': 1000, 'output_tokens': 1, 'cache_read_input_tokens': 5}), 'unexpected_cache_usage'),
                 (message(usage={'input_tokens': 10 ** 6, 'output_tokens': 1}), 'reservation_bound_breached'),
                 ([1, 2], 'invalid_response_body')]
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, ledger = api(td, [c[0] for c in cases])
            for i, (_, category) in enumerate(cases):
                with self.assertRaises(provider.CallFailure) as failure:
                    client.call(PACKET, f'q0-001:c{i}')
                self.assertEqual(failure.exception.category, category)
                self.assertEqual(failure.exception.accounting['attempts'], 1)     # never retried
            self.assertEqual(len(opener.messages()), len(cases))
            self.assertEqual(clock.sleeps, [])
            self.assertEqual(ledger.transact()['transport_attempts'], len(cases))
        with patch.dict(os.environ, {'SWARM_MODEL_API_KEY': '', 'SWARM_MODEL_WORKSPACE_ID': ''}), tempfile.TemporaryDirectory() as td:
            with self.assertRaises(provider.CallFailure) as failure:
                provider.Anthropic(provider.Ledger(Path(td) / 'l'))
            self.assertEqual(failure.exception.category, 'missing_credential_alias')

    def test_transport_retry_only_for_429_and_529(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            # 429 then success.
            client, opener, clock, ledger = api(td, [http_error(429), message()], name='a')
            _, account = client.call(PACKET, 's1-001:a')
            self.assertEqual((account['attempts'], clock.sleeps, len(opener.messages())), (2, [2], 2))
            self.assertEqual((ledger.transact()['attempted_calls'], ledger.transact()['transport_attempts']), (1, 2))
            # 529, 529, success.
            client, opener, clock, ledger = api(td, [http_error(529), http_error(529), message()], name='b')
            _, account = client.call(PACKET, 's1-001:a')
            self.assertEqual((account['attempts'], clock.sleeps), (3, [2, 6]))
            self.assertEqual((ledger.transact()['attempted_calls'], ledger.transact()['transport_attempts']), (1, 3))
            # Three 429s in a row: failure http_429 after 3 attempts, one reservation kept in full.
            client, opener, clock, ledger = api(td, [http_error(429)] * 3 + [message()], name='c')
            with self.assertRaises(provider.CallFailure) as failure:
                client.call(PACKET, 's1-001:a')
            self.assertEqual((failure.exception.category, failure.exception.accounting['attempts']), ('http_429', 3))
            self.assertEqual((len(opener.messages()), clock.sleeps), (3, [2, 6]))
            totals = ledger.transact()
            self.assertEqual((totals['attempted_calls'], totals['transport_attempts'], totals['usage_reported_calls']), (1, 3, 0))
            self.assertEqual(totals['committed_usd'], failure.exception.accounting['reserved_usd'])
            # A 500 and a timeout are never retried.
            for name, error, category in (('d', http_error(500), 'http_500'), ('e', TimeoutError('t'), 'transport_TimeoutError'),
                                          ('f', urllib.error.URLError('x'), 'transport_URLError'), ('g', http_error(400), 'http_400')):
                client, opener, clock, _ = api(td, [error, message()], name=name)
                with self.assertRaises(provider.CallFailure) as failure:
                    client.call(PACKET, 's1-001:a')
                self.assertEqual((failure.exception.category, failure.exception.accounting['attempts']), (category, 1))
                self.assertEqual((len(opener.messages()), clock.sleeps), (1, []))

    def test_retry_after_is_honoured_capped_and_inside_the_request_budget(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, _ = api(td, [http_error(429, retry_after=11), http_error(529, retry_after=500), message()], name='a')
            _, account = client.call(PACKET, 's1-001:a')
            self.assertEqual(clock.sleeps, [11, 20])                    # honoured, then capped at 20 s
            self.assertEqual(account['latency_seconds'], 31)
            sent = [t for (u, _, _), t in zip(opener.sent, opener.timeouts) if u == provider.MESSAGES_URL]
            self.assertEqual(sent, [300, 289, 269])                    # one shared 300 s budget
            # retry-after below the backoff does not shorten it; an unreadable header is ignored.
            client, _, clock, _ = api(td, [http_error(429, retry_after=0), http_error(429, retry_after='soon'), message()], name='b')
            client.call(PACKET, 's1-001:a')
            self.assertEqual(clock.sleeps, [2, 6])
            # No retry when the wait would not fit in what is left of the request budget.
            client, opener, clock, _ = api(td, [http_error(429), message()], name='c')
            client.b = dict(D['budget'], request_timeout_seconds=2.5)
            with self.assertRaises(provider.CallFailure) as failure:
                client.call(PACKET, 's1-001:a')
            self.assertEqual((failure.exception.category, failure.exception.accounting['attempts'], clock.sleeps), ('http_429', 1, []))

    def test_count_tokens_uses_the_same_retry_rule(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, ledger = api(td, [message()], count_outcomes=[http_error(529), {'input_tokens': 900}], name='a')
            _, account = client.call(PACKET, 's1-001:a')
            self.assertEqual((account['count_attempts'], account['attempts'], account['counted_input_tokens'], clock.sleeps), (2, 1, 900, [2]))
            self.assertEqual(ledger.transact()['transport_attempts'], 1)        # only messages attempts count toward the cap
            for name, outcomes, category in (('b', [http_error(429)] * 3, 'count_http_429'), ('c', [http_error(500)], 'count_http_500'),
                                             ('d', [{'input_tokens': 0}], 'count_missing'), ('e', [TimeoutError()], 'count_transport_TimeoutError')):
                client, opener, clock, ledger = api(td, [message()], count_outcomes=outcomes, name=name)
                with self.assertRaises(provider.CallFailure) as failure:
                    client.call(PACKET, 's1-001:a')
                self.assertEqual(failure.exception.category, category)
                self.assertFalse(failure.exception.accounting['attempted'])
                self.assertEqual(ledger.transact()['attempted_calls'], 0)       # nothing reserved, nothing sent to messages
                self.assertEqual(opener.messages(), [])

    def test_ledger_call_caps_dollar_cap_and_attempt_cap(self):
        b = D['budget']
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger')

            def reserve(call_id, micro=1):
                return ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': micro})

            def refused(call_id, category, micro=1):
                with self.assertRaises(provider.CallFailure) as failure:
                    reserve(call_id, micro)
                self.assertEqual(failure.exception.category, category)
            reserve('p0-001:a')
            refused('p0-001:a', 'duplicate_call_refused')
            refused('p0-001:b', 'stage_call_cap_exhausted')          # P0 is capped at one call
            refused('p0-002:a', 'stage_call_cap_exhausted')          # a later attempt shares the stage cap
            refused('s0-001:a', 'stage_call_cap_exhausted')          # S0 may make no call
            refused('s2-001:a', 'unknown_stage_refused')
            refused('nonsense', 'unknown_stage_refused')
            for i in range(48):
                reserve(f'q0-001:{i}')
            refused('q0-001:48', 'stage_call_cap_exhausted')
            self.assertEqual(ledger.transact()['calls_by_stage'], {'P0': 1, 'Q0': 48})
            # Dollar cap: settled calls count their actual cost, open ones their full reservation.
            cap = int(b['aggregate_usd'] * 1_000_000)
            reserve('s1-001:open', 1000)
            reserve('s1-001:settled', 5000)
            ledger.transact({'type': 'response', 'call_id': 's1-001:settled', 'actual_micro_usd': 100, 'input_tokens': 7, 'output_tokens': 3})
            committed = 49 + 1000 + 100
            self.assertEqual(ledger.transact()['committed_usd'], committed / 1e6)
            refused('s1-001:over', 'aggregate_budget_exhausted', cap - committed + 1)
            reserve('s1-001:fits', cap - committed)
            refused('s1-001:one-more', 'aggregate_budget_exhausted', 1)
            totals = ledger.transact()
            self.assertEqual((totals['input_tokens'], totals['output_tokens'], totals['usage_reported_calls']), (7, 3, 1))
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger')
            for i in range(1440):
                ledger.transact({'type': 'reserve', 'call_id': f's1-001:{i}', 'micro_usd': 1})
            with self.assertRaises(provider.CallFailure) as failure:
                ledger.transact({'type': 'reserve', 'call_id': 's1-001:1440', 'micro_usd': 1})
            self.assertEqual(failure.exception.category, 'stage_call_cap_exhausted')
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'design', lambda: dict(D, budget=dict(b, max_transport_attempts=3, max_attempted_calls=2))):
            ledger = provider.Ledger(Path(td) / 'ledger')
            ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1})
            with self.assertRaises(provider.CallFailure) as failure:
                ledger.transact({'type': 'attempt', 'call_id': 's1-001:zz', 'n': 1})
            self.assertEqual(failure.exception.category, 'attempt_without_reservation')
            for n in (1, 2, 3):
                ledger.transact({'type': 'attempt', 'call_id': 's1-001:a', 'n': n})
            with self.assertRaises(provider.CallFailure) as failure:
                ledger.transact({'type': 'attempt', 'call_id': 's1-001:a', 'n': 4})
            self.assertEqual(failure.exception.category, 'transport_attempt_cap_exhausted')
            ledger.transact({'type': 'reserve', 'call_id': 's1-001:b', 'micro_usd': 1})
            with self.assertRaises(provider.CallFailure) as failure:
                ledger.transact({'type': 'reserve', 'call_id': 'q0-001:c', 'micro_usd': 1})
            self.assertEqual(failure.exception.category, 'study_call_cap_exhausted')

    def test_attempt_cap_refuses_before_sending(self):
        b = D['budget']
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), \
                patch.object(study, 'design', lambda: dict(D, budget=dict(b, max_transport_attempts=2))):
            client, opener, clock, ledger = api(td, [http_error(429), http_error(429), message()])
            with self.assertRaises(provider.CallFailure) as failure:
                client.call(PACKET, 's1-001:a')
            self.assertEqual(failure.exception.category, 'transport_attempt_cap_exhausted')
            self.assertEqual((failure.exception.accounting['attempts'], len(opener.messages())), (2, 2))

    # ---------------------------------------------------------------- worker

    def run_worker(self, stage, backend=None, opener=None, deadline=None, clock=None):
        hub = FakeHub()
        run = FakeRun(hub, 'run/0', study.params(stage))
        hub.record['run/0'] = {'params': run.params, 'status': 'running', 'metrics': {}, 'artifacts': {}}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            failure = summary = None
            if opener is not None and backend is None:
                c = clock or Clock()
                backend = provider.Anthropic(provider.Ledger(Path(td) / 'ledger'), opener, clock=c, sleep=c.sleep)
            try:
                summary = worker.execute(run.params, Path(td) / 'out', run, backend=backend,
                                         ledger_path=Path(td) / 'ledger', deadline=deadline)
            except worker.StageFailed as exc:
                failure, summary = exc.reason, exc.summary
            rows = [json.loads(line) for line in (Path(td) / 'out' / 'episodes.jsonl').read_text().splitlines()] if (Path(td) / 'out' / 'episodes.jsonl').exists() else []
            files = sorted(p.name for p in (Path(td) / 'out').iterdir()) if (Path(td) / 'out').exists() else []
        return hub.record['run/0'], summary, failure, rows, files

    def test_worker_first_failure_stops_dispatch_and_failed_run_reports_usage(self):
        class Broken:
            def __init__(self):
                self.calls = 0

            def call(self, packet, call_id):
                self.calls += 1
                raise provider.CallFailure('injected_failure', {'attempted': True, 'attempts': 1, 'reserved_usd': 0.25})
        backend = Broken()
        record, summary, failure, rows, _ = self.run_worker('Q0', backend=backend)
        self.assertEqual(failure, 'invalid_rows:injected_failure')
        self.assertEqual(record['status'], 'failed')
        for key in worker.REQUIRED_METRICS:
            self.assertIn(key, record['metrics'])
        self.assertEqual(record['metrics']['qualification_passed'], 0)
        self.assertEqual((record['metrics']['episodes'], record['metrics']['invalid']), (48, 48))
        self.assertLessEqual(backend.calls, 4)                      # only requests already in flight finish
        self.assertEqual(record['metrics']['model_calls'], backend.calls)
        self.assertEqual(len(rows), 48)
        self.assertEqual(len({r['id'] for r in rows}), 48)
        self.assertEqual(sum(r['status'] == 'failed' for r in rows), backend.calls)
        self.assertEqual(sum(r['status'] == 'not_started' for r in rows), 48 - backend.calls)
        self.assertEqual((summary['not_started'], summary['graded'], summary['gate']['passed']), (48 - backend.calls, 0, False))

    def test_worker_success_reports_usage_and_retries_only_transport(self):
        a = study.assignments('P0')[0]
        text = json.dumps(study.scripted(a['packet']))
        usage = {'input_tokens': 23000, 'output_tokens': 40}
        opener = Script([http_error(429), message(text=text, usage=usage)], count_outcomes=[{'input_tokens': 23000}])
        record, summary, failure, rows, files = self.run_worker('P0', opener=opener)
        self.assertIsNone(failure)
        self.assertEqual(record['status'], 'done')
        expected = {'episodes': 1, 'invalid': 0, 'model_calls': 1, 'input_tokens': 23000, 'output_tokens': 40,
                    'cost_usd': (23000 * 4 + 40 * 20) / 1e6, 'transport_attempts': 2, 'qualification_passed': 1}
        for key, value in expected.items():
            self.assertEqual(record['metrics'][key], value)
        self.assertEqual(rows[0]['accounting']['attempts'], 2)
        self.assertEqual(summary['probe_measurement']['input_tokens'], 23000)
        self.assertAlmostEqual(summary['probe_measurement']['chain_projection_usd_at_probe_cost'], 0.0928 * 1489)
        self.assertTrue(set(worker.ARTIFACTS) <= set(record['artifacts']))
        self.assertTrue(set(worker.ARTIFACTS) <= set(files))
        # A wrong probe answer fails the gate and the run, with usage still reported.
        wrong = json.dumps({'values': {**study.scripted(a['packet'])['values'], '5': 11}})
        record, summary, failure, _, _ = self.run_worker('P0', opener=Script([message(text=wrong, usage=usage)]))
        self.assertEqual((failure, record['status'], record['metrics']['qualification_passed']), ('qualification_failed', 'failed', 0))
        self.assertEqual((record['metrics']['invalid'], record['metrics']['model_calls'], record['metrics']['input_tokens']), (0, 1, 23000))

    def test_worker_deadline_stops_dispatch_and_crash_still_reports_usage(self):
        import time as _time
        record, summary, failure, rows, _ = self.run_worker('Q0', opener=Script([]), deadline=_time.monotonic() - 1)
        self.assertEqual(failure, 'invalid_rows:stage_deadline')
        self.assertEqual({r.get('error') for r in rows if r['status'] == 'failed'}, {'stage_deadline'})
        self.assertEqual(record['metrics']['model_calls'], 0)
        self.assertEqual(sum(r['status'] == 'not_started' for r in rows) + sum(r['status'] == 'failed' for r in rows), 48)
        with patch.object(render, 'replay', side_effect=RuntimeError('boom')):
            record, summary, failure, rows, _ = self.run_worker('Q0', opener=rehearse.Stub('plurality'))
        self.assertEqual((failure, record['status']), ('internal_RuntimeError', 'failed'))
        for key in worker.REQUIRED_METRICS:
            self.assertIn(key, record['metrics'])
        self.assertEqual((record['metrics']['model_calls'], record['metrics']['qualification_passed']), (48, 0))
        # A runtime that does not match the queued source hash refuses before doing anything.
        hub = FakeHub()
        run = FakeRun(hub, 'run/0', dict(study.params('P0'), source_hash='0' * 64))
        hub.record['run/0'] = {'params': run.params, 'status': 'running', 'metrics': {}, 'artifacts': {}}
        with tempfile.TemporaryDirectory() as td, self.assertRaises(worker.StageFailed):
            worker.execute(run.params, Path(td) / 'out', run, ledger_path=Path(td) / 'l')
        self.assertEqual(hub.record['run/0']['status'], 'failed')

    # ---------------------------------------------------------------- gates and chain

    def test_coordinator_gates(self):
        other = 'f' * 64
        cases = [
            ('S0', [], None),
            ('S0', [hub_run('S0')], 'batch_exists_no_replay'),
            ('P0', [], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0')], None),
            ('P0', [hub_run('S0', status='failed')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', status='running')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', invalid=1)], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', passed=0)], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', source_hash=other)], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0'), hub_run('S0', batch='s0-002')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0'), hub_run('S0', status='failed', batch='s0-002')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0'), hub_run('S0', source_hash=other, batch='s0-000')], None),
            ('P0', [hub_run('S0'), hub_run('P0', status='failed')], 'batch_exists_no_replay'),
            ('Q0', [hub_run('S0')], 'exact_runtime_qualification_required:P0'),
            ('Q0', [hub_run('S0'), hub_run('P0')], None),
            ('S1', [hub_run('S0'), hub_run('P0')], 'exact_runtime_qualification_required:Q0'),
            ('S1', [hub_run('S0'), hub_run('P0'), hub_run('Q0', status='failed', invalid=0, passed=0)], 'exact_runtime_qualification_required:Q0'),
            ('S1', [hub_run('S0'), hub_run('P0'), hub_run('Q0')], None),
        ]
        for stage, runs, refusal in cases:
            if refusal:
                with self.assertRaises(ValueError) as failure:
                    coordinator.gate(runs, stage, study.params(stage))
                self.assertEqual(str(failure.exception), refusal)
            else:
                coordinator.gate(runs, stage, study.params(stage))
        hub = FakeHub()
        ids = coordinator.enqueue(hub, 'S0')
        self.assertEqual((len(ids), hub.registered, hub.record[ids[0]]['params']), (1, [study.EXPERIMENT], study.params('S0')))
        with self.assertRaises(ValueError):
            coordinator.enqueue(hub, 'S0')
        with self.assertRaises(ValueError):
            coordinator.enqueue(hub, 'P0')
        self.assertEqual(len(hub.record), 1)

    def test_chain_stage_lists_and_projection_rule(self):
        for text, expected in (('S0,P0,Q0,S1', ['S0', 'P0', 'Q0', 'S1']), ('S0', ['S0']), ('p0, q0 ,s1', ['P0', 'Q0', 'S1']), ('Q0', ['Q0'])):
            self.assertEqual(chain.parse_stages(text), expected)
        for text in ('', 'S0,Q0', 'P0,S0', 'S0,S0', 'S2', 'S0,P0,S1'):
            with self.assertRaises(ValueError):
                chain.parse_stages(text)
        ok = chain.projection_check(0.0949, 4.7)
        self.assertTrue(ok['passed'])
        self.assertAlmostEqual(ok['projected_s1_usd'], 1440 * 0.0949)
        self.assertFalse(chain.projection_check(0.16, 4.7)['passed'])          # 230.40 > 215.30
        self.assertFalse(chain.projection_check(0.0949, 100)['passed'])        # 136.66 > 120 left

    def test_chain_runs_gates_stops_on_projection_and_verify_detects_tampering(self):
        invariants = {'checks': {'mocked_in_this_test': True}, 'passed': True, 'jobs': 0}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), patch.object(study, 'check_invariants', lambda: invariants):
            root, ledger = Path(td) / 'results', Path(td) / 'ledger' / 'l.jsonl'
            hub = FakeHub()
            # Paid stages refuse to start, and queue nothing, without their environment.
            with patch.dict(os.environ, {'SWARM_MODEL_API_KEY': ''}):
                self.assertEqual(chain.run_chain(['P0'], hub, root, ledger), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['reason'], hub.record), ('stopped_at_gate', 'missing_environment:SWARM_MODEL_API_KEY', {}))
            # P0 without S0 is refused by the gate; nothing is queued.
            self.assertEqual(chain.run_chain(['P0'], hub, root, ledger, opener=rehearse.Stub()), chain.EXIT_STOPPED)
            self.assertEqual((chain.read_status(root)['reason'], hub.record), ('exact_runtime_qualification_required:S0', {}))
            # S0, P0, Q0 with a stub whose calls are expensive (the whole output limit).
            stub = rehearse.Stub('plurality', output_tokens=8000)
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0'], hub, root, ledger, opener=stub), chain.EXIT_DONE)
            status = chain.read_status(root)
            self.assertEqual(status['state'], 'completed')
            self.assertEqual([status['stages'][s]['status'] for s in ('S0', 'P0', 'Q0')], ['done'] * 3)
            self.assertEqual([status['stages'][s]['calls'] for s in ('S0', 'P0', 'Q0')], [0, 1, 48])
            for s in ('S0', 'P0', 'Q0'):
                for key in ('run', 'status', 'calls', 'input_tokens', 'output_tokens', 'cost_usd', 'started', 'ended'):
                    self.assertIn(key, status['stages'][s])
            self.assertEqual(stub.message_calls, 49)
            self.assertFalse((root / (chain.STATUS_FILE + '.tmp')).exists())
            # Replay of a finished batch is refused.
            self.assertEqual(chain.run_chain(['S0'], hub, root, ledger), chain.EXIT_STOPPED)
            self.assertEqual(chain.read_status(root)['reason'], 'batch_exists_no_replay')
            # S1: the projection from Q0's measured cost exceeds the remaining cap, so nothing is queued.
            before = len(hub.record)
            self.assertEqual(chain.run_chain(['S1'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'S1', 'projection_exceeds_cap'))
            self.assertFalse(status['stages']['S1']['projection']['passed'])
            self.assertGreater(status['stages']['S1']['projection']['projected_s1_usd'], status['stages']['S1']['projection']['remaining_cap_usd'])
            self.assertEqual((len(hub.record), stub.message_calls), (before, 49))
            self.assertEqual(status['stages']['Q0']['status'], 'done')           # earlier stages stay recorded
            # verify: checksums against the hub, regraded rows, recomputed summary and analysis.
            real = json.loads((study.ROOT / 'manifest.json').read_text())
            report = chain.verify(hub, root)
            self.assertTrue(report['ok'], report)
            self.assertEqual(set(report['stages']), {'S0', 'P0', 'Q0'})
            self.assertEqual(real['stages']['Q0']['count'], 48)
            out = Path(status['stages']['Q0']['results_dir'])
            rows = analyze.read_rows(out / 'episodes.jsonl.gz')
            rows[0]['evaluation']['exact_packet'] = not rows[0]['evaluation']['exact_packet']
            with gzip.open(out / 'episodes.jsonl.gz', 'wt') as f:
                for r in rows:
                    f.write(json.dumps(r, sort_keys=True) + '\n')
            report = chain.verify(hub, root)
            self.assertFalse(report['ok'])
            self.assertFalse(report['stages']['Q0']['checks']['grades_recomputed'])
            self.assertFalse(report['stages']['Q0']['checks']['artifacts_match_hub'])
            self.assertTrue(report['stages']['P0']['ok'])
            # status prints chain state and ledger totals without any credential.
            state = chain.chain_status(root, ledger)
            self.assertEqual((state['ledger']['attempted_calls'], state['chain']['state']), (49, 'stopped_at_gate'))
            self.assertNotIn('selftest-not-a-key', json.dumps(state))

    def test_chain_stops_at_failed_qualification(self):
        invariants = {'checks': {'mocked_in_this_test': True}, 'passed': True, 'jobs': 0}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), patch.object(study, 'check_invariants', lambda: invariants):
            root, ledger, hub, stub = Path(td) / 'results', Path(td) / 'l.jsonl', FakeHub(), rehearse.Stub('invent')
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0', 'S1'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'Q0', 'qualification_failed'))
            self.assertNotIn('S1', status['stages'])
            stages = [r['params']['stage'] for r in hub.record.values()]
            self.assertEqual(stages, ['S0', 'P0', 'Q0'])
            q0 = [r for r in hub.record.values() if r['params']['stage'] == 'Q0'][0]
            self.assertEqual((q0['status'], q0['metrics']['qualification_passed'], q0['metrics']['model_calls'], q0['metrics']['invalid']), ('failed', 0, 48, 0))
            self.assertEqual(stub.message_calls, 49)

    # ---------------------------------------------------------------- analysis and rendering

    def test_primary_contrast_bootstrap_and_missing_outcome_bounds(self):
        tasks = D['worlds']
        full = {1: {t: (1 / 3 if i % 2 else 0.0) for i, t in enumerate(tasks)}, 81: {t: 1.0 for t in tasks}}
        result = analyze.analyze(synthetic_rows(full))['primary']
        self.assertEqual((result['roots'], result['complete_roots']), (24, 24))
        self.assertAlmostEqual(result['mean'], 1 / 6 - 1)
        lo, hi = result['interval']
        self.assertTrue(-1 <= lo < result['mean'] < hi <= -2 / 3)
        self.assertEqual(result['interval'], analyze.analyze(synthetic_rows(full))['primary']['interval'])   # fixed seed
        self.assertAlmostEqual(result['all_assigned_bounds'][0], result['mean'])
        missing = {1: dict(full[1]), 81: dict(full[81])}
        missing[1][tasks[0]] = None
        missing[81][tasks[1]] = None
        result = analyze.analyze(synthetic_rows(missing))
        primary = result['primary']
        self.assertEqual((primary['roots'], primary['complete_roots']), (24, 22))      # no root is dropped
        self.assertIsNone(primary['mean'])
        self.assertIsNone(primary['interval'])
        lo, hi = primary['all_assigned_bounds']
        # Root 0: unknown minus 1 is in [-1, 0]; root 1: 1/3 minus unknown is in [-2/3, 1/3]. Never zero-imputed.
        rest = sum(full[1][t] - 1 for t in tasks[2:])
        self.assertAlmostEqual(lo, (rest - 1 - 2 / 3) / 24)
        self.assertAlmostEqual(hi, (rest + 0 + 1 / 3) / 24)
        self.assertAlmostEqual(primary['complete_case_mean'], rest / 22)
        cell = next(c for c in result['cells'] if c['carriers'] == 1)
        self.assertEqual((cell['assigned'], cell['valid'], cell['missing']), (24, 23, 1))
        self.assertIsNone(cell['rare_accuracy']['interval'])
        self.assertAlmostEqual(cell['rare_accuracy']['all_assigned_bounds'][1] - cell['rare_accuracy']['all_assigned_bounds'][0], 1 / 24)

    def test_analysis_reports_all_60_cells_invariance_and_diagnostics(self):
        result = analyze.analyze(self.rows)
        self.assertEqual((result['cell_count'], len(result['cells'])), (60, 60))
        self.assertTrue(all(c['assigned'] == 1 == c['valid'] for c in result['cells']))
        self.assertEqual(result['invariance'], {'matched_cells': 12, 'violations': 0})
        self.assertEqual((len(result['carrier_contrasts']), len(result['policy_contrasts']), len(result['policy_by_rarity_interactions'])), (48, 30, 6))
        self.assertEqual(result['duplicate_packets']['assignments'], 60)
        for c in result['cells']:
            self.assertEqual(c['scripted_rare_accuracy'], c['model']['rare_accuracy'])   # scripted rows: model == plurality
            self.assertLessEqual(c['conditional_on_truth_survival']['numerator'], c['conditional_on_truth_survival']['denominator'])
            for name in analyze.DIAGNOSTICS:
                self.assertIsNotNone(c['diagnostics'][name])
        tampered = [dict(r) for r in self.rows]
        tampered[0]['admitted_hash'] = 'different'
        self.assertEqual(analyze.analyze(tampered)['invariance']['violations'], 1)
        self.assertEqual(json.loads(json.dumps(result)), json.loads(json.dumps(analyze.analyze(self.rows))))

    def test_frames_initial_progress_failure_final_and_replay(self):
        for stage, rows, total in (('S1', [], 1440), ('S0', self.rows[:7], 168), ('Q0', [], 48), ('P0', [], 1)):
            self.assertEqual(render.frame(rows, total, stage).size, (1800, 1200))
        failed = dict(self.rows[0], status='failed', error='http_500')
        failed.pop('evaluation')
        not_started = dict(self.rows[1], status='not_started')
        not_started.pop('evaluation')
        partial = render.frame([failed, not_started] + self.rows[2:20], 1440, 'S1', 12, {'actual_usd': 1.5, 'committed_usd': 2.0, 'attempted_calls': 20})
        self.assertEqual(partial.size, (1800, 1200))
        self.assertNotEqual(partial.tobytes(), render.frame([], 1440, 'S1').tobytes())
        probe = study.assignments('P0')[0]
        row = {k: probe[k] for k in study.ROW_KEYS}
        ok = dict(row, status='completed', evaluation=study.evaluate(probe, study.scripted(probe['packet'])),
                  scripted_evaluation={}, accounting={'input_tokens': 23536, 'counted_input_tokens': 23536, 'output_tokens': 38, 'actual_usd': 0.0949, 'latency_seconds': 2.9})
        self.assertEqual(render.frame([ok], 1, 'P0').size, (1800, 1200))
        self.assertEqual(render.frame([dict(row, status='failed', error='refusal', scripted_evaluation={})], 1, 'P0').size, (1800, 1200))
        with tempfile.TemporaryDirectory() as td:
            frames = render.replay(self.rows, Path(td), 'S1', 60)
            self.assertEqual(frames, 33)
            with Image.open(Path(td) / 'replay.gif') as gif:
                self.assertEqual((gif.n_frames, gif.size), (33, (1800, 1200)))
                for i in range(gif.n_frames):
                    gif.seek(i)
                    gif.load()
            for name in ('initial_frame.png', 'final_frame.png'):
                with Image.open(Path(td) / name) as im:
                    self.assertEqual(im.size, (1800, 1200))
            self.assertEqual(render.replay([], Path(td), 'S1', 60), 1)
        self.assertIsNotNone(render.font(20))

    # ---------------------------------------------------------------- package consistency

    def test_manifest_regenerates_identically(self):
        built = manifest.build()
        self.assertEqual({s: built['stages'][s]['count'] for s in study.STAGES}, {'S0': 168, 'P0': 1, 'Q0': 48, 'S1': 1440})
        for s in study.STAGES:
            ids = [line.split()[0] for line in built['stages'][s]['assignments']]
            self.assertEqual(len(set(ids)), len(ids))
        self.assertEqual(built['source_hash'], study.source_hash())
        committed = (study.ROOT / 'manifest.json').read_text()
        self.assertEqual(committed, manifest.render(built))
        self.assertLess(len(committed), 300_000)

    def test_ready_file_matches_design_and_source(self):
        ready = yaml.safe_load((study.ROOT / 'READY.yaml').read_text())
        b = D['budget']
        self.assertEqual(set(ready), {'contract', 'study', 'experiment', 'stages', 'model', 'effort', 'max_calls', 'max_calls_total',
                                      'usd_cap', 'chain_timeout_seconds', 'selftests', 'source_hash'})
        self.assertEqual((ready['contract'], ready['study'], ready['experiment']), ('ready-chain-v1', study.EXPERIMENT, study.EXPERIMENT))
        self.assertEqual(ready['stages'], list(study.STAGES))
        self.assertEqual((ready['model'], ready['effort']), (D['model'], D['effort']))
        self.assertEqual((ready['max_calls'], ready['max_calls_total']), (b['max_calls'], b['max_attempted_calls']))
        self.assertEqual((ready['usd_cap'], ready['chain_timeout_seconds']), (b['aggregate_usd'], b['chain_timeout_seconds']))
        self.assertEqual(ready['source_hash'], study.source_hash())
        self.assertEqual(ready['selftests'], unittest.defaultTestLoader.loadTestsFromTestCase(Tests).countTestCases())
        experiment = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
        self.assertEqual(experiment['id'], study.EXPERIMENT)
        self.assertTrue(set(worker.REQUIRED_METRICS) | {'qualification_passed', experiment['primary_metric']} <= set(experiment['metrics']))

    def test_outputs_stay_out_of_the_committed_tree_and_no_secret_in_source(self):
        with patch.dict(os.environ, {'STUDY_RESULTS_DIR': '/nonexistent/elsewhere'}):
            self.assertEqual(study.results_root(), Path('/nonexistent/elsewhere'))
        with patch.dict(os.environ, {'STUDY_RESULTS_DIR': ''}):
            self.assertEqual(study.results_root(), study.ROOT / 'results')
        self.assertIn('results/', (study.ROOT / '.gitignore').read_text().split())
        import re
        for path in sorted(study.ROOT.rglob('*')):
            if path.is_file() and path.suffix in ('.py', '.md', '.yaml', '.json', '.txt') and 'results' not in path.parts:
                text = path.read_text()
                self.assertIsNone(re.search(r'sk-ant-[A-Za-z0-9]', text), path)
                for address in re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text):
                    self.assertEqual(address, '127.0.0.1', path)


if __name__ == '__main__':
    unittest.main()
