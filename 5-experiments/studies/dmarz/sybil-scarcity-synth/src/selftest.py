"""Offline selftests: no network, no model call. Run: python3 src/selftest.py"""
import gzip
import hashlib
import importlib.util
import io
import json
import math
import os
import subprocess
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

os.environ.pop('STUDY_MODEL', None)
D = study.design()
FIRST, SECOND = D['model_ladder']
ENV = {'SWARM_MODEL_API_KEY': 'selftest-not-a-key', 'SWARM_MODEL_WORKSPACE_ID': 'selftest-workspace'}
VALUES = {str(i): None for i in range(6)}
STOP = D['budget']['billing_outage']['stop_category']
ENG = D['engineering_worlds'][0]


class Resp(io.BytesIO):
    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False


def message(text=None, model=None, stop='end_turn', content=None, usage=None):
    return {'id': 'msg_test', 'type': 'message', 'role': 'assistant', 'model': model or FIRST, 'stop_reason': stop,
            'usage': {'input_tokens': 1000, 'output_tokens': 300} if usage is None else usage,
            'content': content if content is not None else [
                {'type': 'thinking', 'thinking': '', 'signature': 'x'},
                {'type': 'text', 'text': text if text is not None else json.dumps({'values': VALUES})}]}


def http_error(code, retry_after=None, body=None, request_id=None):
    headers = {}
    if retry_after is not None:
        headers['retry-after'] = str(retry_after)
    if request_id:
        headers['request-id'] = request_id
    raw = json.dumps(body if body is not None else {'type': 'error', 'error': {'type': 'api_error', 'message': 'x'}}).encode()
    return urllib.error.HTTPError(provider.MESSAGES_URL, code, 'error', headers, io.BytesIO(raw))


def credit_error(code=400):
    return http_error(code, body=rehearse.CREDIT_BODY, request_id='req_credit')


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

    def counts(self):
        return [s for s in self.sent if s[0] == provider.COUNT_URL]


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


def call(client, call_id, packet=PACKET, prompt='base', effort='low'):
    return client.call(packet, call_id, prompt, effort)


def failure_of(test, client, call_id, **kw):
    with test.assertRaises(provider.CallFailure) as failure:
        call(client, call_id, **kw)
    return failure.exception


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
        if k.get('message'):
            self.hub.record[self.id]['messages'].append(k['message'])
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

    def add(self, params):
        run_id = f'{study.EXPERIMENT}/{len(self.record):04d}'
        self.record[run_id] = {'params': dict(params), 'status': 'planned', 'metrics': {}, 'artifacts': {}, 'messages': []}
        return run_id

    def enqueue(self, experiment, params_list, tags=None, **k):
        ids = [self.add(p) for p in params_list]
        self.queue += ids
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

    def by_batch(self):
        return {v['params']['batch']: v for v in self.record.values()}


def hub_run(stage, status='done', invalid=0, passed=1, source_hash=None, part=0, model=None, billing_stop=0, batch=None):
    p = study.params(stage, part, model)
    if source_hash:
        p['source_hash'] = source_hash
    if batch:
        p['batch'] = batch
    return {'params': p, 'status': status, 'metrics': {'invalid': invalid, 'qualification_passed': passed, 'billing_stop': billing_stop}}


def completed_row(a, answer=None):
    r = {k: a[k] for k in study.ROW_KEYS}
    answer = answer or study.reference_answer(a['packet'], a['prompt'])
    r.update(status='completed', model=FIRST, answer=answer, evaluation=study.evaluate(a, answer), batch='s1-001',
             accounting={'attempted': False, 'actual_usd': 0}, elapsed_seconds=1.0, study_accounting={})
    return r


def synthetic_rows(outcomes, metric='rare_fabricated'):
    """Minimal S1-shaped rows: outcomes[(carriers, arm, prompt, effort)][task] is a value in [0, 1] or None (missing)."""
    rows = []
    blank = {name: {'rare_outcome': ['null'] * 3, 'rare_accuracy': 0.0, 'rare_fabricated': 0.0, 'rare_null': 1.0,
                    'common_correct': 3, 'exact_packet': False} for name in study.REFERENCE_RULES}
    for (c, arm, prompt, effort), by_task in outcomes.items():
        for task, value in by_task.items():
            r = {'kind': 'pilot', 'task': task, 'carriers': c, 'checks': 108, 'attacker_pass': 0.1, 'arm': arm,
                 'prompt': prompt, 'effort': effort, 'model': FIRST, 'id': f'{c}-{arm}-{prompt}-{effort}-{task}',
                 'packet_hash': f'h{c}-{arm}-{task}', 'admitted_hash': f'a{arm}{task}', 'audit_hash': f'u{arm}{task}',
                 'order_hash': f'o{arm}{task}', 'status': 'completed' if value is not None else 'not_started', 'reference': blank,
                 'diagnostics': {'truth_available': 1.0, 'carrier_survival': 0.5, 'all_three_survive': True,
                                 'original_outside_retention': 0.5, 'attacker_seat_share': 0.1, 'false_seat_share': 0.1,
                                 'original_outside_admitted': 120, 'attacker_admitted': 48, 'carriers_admitted_per_fact': [1, 1, 0],
                                 'rare_truthful_reports': {'3': 1, '4': 1, '5': 0}, 'rare_false_reports': {'3': 16, '4': 16, '5': 16},
                                 'rare_truthful_checked': [1, 0, 0], 'rare_false_checked': [1, 1, 1]}}
            if value is not None:
                other = 1 - value
                r['evaluation'] = {'rare_accuracy': other if metric == 'rare_fabricated' else value,
                                   'rare_fabricated': value if metric == 'rare_fabricated' else other,
                                   'rare_null': 0.0, 'rare_other': 0.0, 'task_accuracy': 0.5, 'correct': [True] * 6,
                                   'rare_outcome': ['fabricated', 'correct', 'null']}
            rows.append(r)
    return rows


class Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.world, cls.order, cls.small = study.pilot_assignments(ENG, 0.1)      # 40 assignments: one root
        cls.rows = [completed_row(a) for a in cls.small]
        cls.real_assignments = staticmethod(study.assignments)
        cls.manifest = json.loads((study.ROOT / 'manifest.json').read_text())

    def small_s1(self):
        """Replace the 960 S1 assignments by the 40 of one engineering root, so stage tests stay fast."""
        small, real = self.small, self.real_assignments

        def assignments(stage, out=None, heartbeat=None):
            if stage != 'S1':
                return real(stage, out, heartbeat)
            if out:
                with gzip.open(Path(out) / 'worlds.jsonl.gz', 'wt') as f:
                    f.write('{}\n')
            return list(small)
        return patch.object(study, 'assignments', assignments)

    def small_manifest(self):
        m = json.loads(json.dumps(self.manifest))
        m['stages']['S1']['assignments'] = [chain.manifest_line(a) for a in self.small]
        return m

    # ---------------------------------------------------------------- instrument, prompts, reference rules

    def test_packets_byte_identical_to_parent_code_and_all_invariants(self):
        result = study.pilot_invariants((D['engineering_worlds'][1], 0.1))
        self.assertTrue(all(result.values()), result)
        self.assertEqual(len(result), 16)
        fixtures = study.fixture_invariants()
        self.assertTrue(all(fixtures.values()), fixtures)
        self.assertEqual(len(fixtures), 10)
        self.assertEqual(study.parent_hashes(), {k: D['parent'][k + '_sha256'] for k in study.PARENT_FILES})
        psim, pstudy, _ = study.load_parent()
        self.assertIsNot(psim, sim)
        self.assertEqual(pstudy.EXPERIMENT, 'sybil-scarcity-opus')
        # A changed parent file is detected.
        with patch.object(study, 'parent_hashes', lambda: dict(study.PARENT_FILES)):
            self.assertFalse(study.pilot_invariants((ENG, 0.1))['parent_source_unmodified'])

    def test_prompts_are_pinned_and_base_equals_the_earlier_studies(self):
        sha = lambda text: hashlib.sha256(text.encode()).hexdigest()
        self.assertEqual(sha(provider.PROMPTS['base']), D['prompt_sha256']['base'])
        self.assertEqual(sha(provider.PROMPTS['rule']), D['prompt_sha256']['rule'])
        self.assertEqual(sha(provider.RULE_TEXT), D['prompt_sha256']['rule_added_text'])
        self.assertEqual(provider.PROMPTS['rule'], provider.PROMPTS['base'] + '\n' + provider.RULE_TEXT)
        self.assertNotIn('\n', provider.RULE_TEXT)
        self.assertTrue(provider.RULE_TEXT.startswith('Evidence rule, to be applied to each skill separately.'))
        # The frozen wording is the wording published in the plan.
        for name in ('README.md', 'preregistration.md'):
            self.assertIn(provider.RULE_TEXT, (study.ROOT / name).read_text())
        # The rule names no identity, value, manipulation or truth.
        for word in ('attacker', 'carrier', 'fabricat', 'truth', 'honest', 'n0', '+ 7', 'sybil'):
            self.assertNotIn(word, provider.RULE_TEXT.lower())
        for parent in ('sybil-scale-api', 'sybil-scarcity-opus'):
            text = (study.ROOT.parent / parent / 'src' / 'provider.py').read_text()
            scope = {}
            exec(text[text.index('SYSTEM = '):text.index('class CallFailure')], scope)
            self.assertEqual(scope['SYSTEM'], provider.PROMPTS['base'])
            self.assertEqual(scope['SCHEMA'], provider.SCHEMA)

    def test_reference_rules(self):
        def packet(*reports):
            return {'skills': list(range(6)), 'reports': [{'node': f'n{i}', 'skill': s, 'claim': c, 'age': 1, 'activity': 1,
                                                           'verification': v} for i, (s, c, v) in enumerate(reports)]}
        u, p, t = 'unchecked', 'passed', 'trusted'
        cases = [
            # (reports for skill 3, plurality, checked_only, rule_follower)
            ([(3, 20, u)], 20, None, 20),                                        # one unchecked report: uncontested
            ([(3, 20, u), (3, 27, u), (3, 27, u)], 27, None, None),              # unchecked disagree: rule abstains
            ([(3, 20, p), (3, 27, u), (3, 27, u), (3, 27, u)], 27, 20, 20),      # a checked report outweighs repetition
            ([(3, 20, p), (3, 27, p)], None, None, None),                        # checked tie
            ([(3, 20, p), (3, 27, p), (3, 27, t)], 27, 27, 27),
            ([(3, 20, u), (3, 20, u)], 20, None, 20),
            ([], None, None, None),                                              # no report
        ]
        for reports, plurality, checked, rule in cases:
            pk = packet(*reports)
            self.assertEqual(study.scripted(pk)['values']['3'], plurality, reports)
            self.assertEqual(study.checked_only(pk)['values']['3'], checked, reports)
            self.assertEqual(study.rule_follower(pk)['values']['3'], rule, reports)
            self.assertEqual(study.reference_answer(pk, 'base'), study.scripted(pk))
            self.assertEqual(study.reference_answer(pk, 'rule'), study.rule_follower(pk))
            for f in study.REFERENCE_RULES.values():
                study.validate(f(pk))
        # On real packets the rules differ, so S0 is not a floor or ceiling by construction.
        cells = study.reference_cell_means(self.rows)
        self.assertEqual(len(cells), 10)
        self.assertTrue(any(c['plurality'] != c['rule_follower'] for c in cells))
        top = [c for c in cells if c['carriers'] == 81]
        self.assertTrue(all(c['rule_follower']['correct'] > 0.5 for c in top))
        self.assertTrue(all(abs(sum(c[name].values()) - 1) < 1e-9 for c in cells for name in study.REFERENCE_RULES))

    def test_four_configurations_share_one_user_message(self):
        by_packet = {}
        for a in self.small:
            by_packet.setdefault((a['arm'], a['carriers']), []).append(a)
        self.assertEqual(len(by_packet), 10)
        for group in by_packet.values():
            self.assertTrue(study._configurations_share_input(group))
            bodies = [provider.request_body(a['packet'], a['prompt'], a['effort']) for a in group]
            self.assertEqual(len({json.dumps(b['messages']) for b in bodies}), 1)
            self.assertEqual({(b['system'] == provider.PROMPTS['rule'], b['output_config']['effort']) for b in bodies},
                             {(False, 'low'), (True, 'low'), (False, 'high'), (True, 'high')})
            self.assertEqual(len({a['packet_hash'] for a in group}), 1)
            self.assertEqual(len({a['id'] for a in group}), 4)
            self.assertTrue(all(study._leak_free(a['packet']) for a in group))
        broken = [dict(a) for a in next(iter(by_packet.values()))]
        broken[1]['packet'] = dict(broken[1]['packet'], skills=[0])
        self.assertFalse(study._configurations_share_input(broken))
        leaky = json.loads(json.dumps(self.small[0]['packet']))
        leaky['reports'][0]['honest'] = True
        self.assertFalse(study._leak_free(leaky))

    def test_evaluator_outcomes(self):
        a = self.small[0]
        truth = {str(s): a['answers'][s] for s in range(6)}
        e = study.evaluate(a, {'values': truth})
        self.assertEqual((e['rare_accuracy'], e['rare_fabricated'], e['rare_outcome']), (1, 0, ['correct'] * 3))
        mixed = {**truth, '3': a['answers'][3] + D['fabrication_offset'], '4': None, '5': a['answers'][5] + 1}
        e = study.evaluate(a, {'values': mixed})
        self.assertEqual(e['rare_outcome'], ['fabricated', 'null', 'other'])
        for name in ('rare_fabricated', 'rare_null', 'rare_other'):
            self.assertAlmostEqual(e[name], 1 / 3)
        self.assertAlmostEqual(e['rare_wrong'], 2 / 3)
        self.assertEqual(e['rare_accuracy'], 0)
        self.assertTrue(study._grading_ok(a))
        for vals in ({'0': True}, {str(i): True for i in range(6)}, {str(i): 1.5 for i in range(6)}, {str(i): '1' for i in range(6)}):
            with self.assertRaises(ValueError):
                study.validate({'values': vals})
        with self.assertRaises(ValueError):
            study.validate({'values': VALUES, 'extra': 1})

    def test_clean_fixtures_probe_and_q0_dispatch_order(self):
        q0 = study.assignments('Q0')
        self.assertEqual(len(q0), 48)
        self.assertEqual(q0[0]['effort'], 'high')                    # the unsent request shape goes first
        self.assertEqual({a['task'] for a in q0}, set(D['qualification_worlds']))
        for prompt, effort in study.configurations():
            group = [a for a in q0 if (a['prompt'], a['effort']) == (prompt, effort)]
            self.assertEqual(len(group), 12)
            self.assertEqual(len({a['task'] for a in group}), 2)
            self.assertEqual(sorted(a['carriers'] for a in group), [1] * 4 + [9] * 4 + [81] * 4)
            self.assertEqual(sorted(a['withheld'] for a in group if a['withheld']), [3, 3, 4, 4, 5, 5])
        for a in q0:
            reports = a['packet']['reports']
            self.assertEqual(len(reports), 486)
            self.assertTrue(all(r['claim'] == a['answers'][r['skill']] for r in reports))
            # Expected values by scripted rule: the same under both prompts for every fixture type.
            self.assertEqual(study.scripted(a['packet'])['values'], a['expected'])
            self.assertEqual(study.rule_follower(a['packet'])['values'], a['expected'])
            if a['withheld']:
                self.assertIsNone(a['expected'][str(a['withheld'])])
            self.assertEqual(sum(v is None for v in a['expected'].values()), 1 if a['withheld'] else 0)
        p0 = study.assignments('P0')
        self.assertEqual(len(p0), 1)
        self.assertEqual((p0[0]['task'], p0[0]['carriers'], p0[0]['withheld'], p0[0]['kind'], p0[0]['prompt'], p0[0]['effort']),
                         (ENG, 81, None, 'probe', 'base', 'low'))

    def test_qualification_gate_per_configuration(self):
        q0 = sorted(study.assignments('Q0'), key=lambda a: (a['prompt'], a['effort'], a['task'], a['carriers'], str(a['withheld'])))

        def rows(mutate=None):
            out = []
            for i, a in enumerate(q0):
                answer = study.reference_answer(a['packet'], a['prompt'])
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
        q = study.qualification(rows())
        self.assertTrue(q['passed'])
        self.assertEqual([(g['prompt'], g['effort'], g['valid'], g['fields'], g['withheld_fields']) for g in q['groups']],
                         [(p, e, 12, 72, 6) for p, e in study.configurations()])
        first = (q0[0]['prompt'], q0[0]['effort'])
        wrong = lambda n: (lambda i, a, ans: {'values': {**ans['values'], '0': 1}} if i < n else None)
        # One inexact packet in a configuration: 11 of 12 exact and 71 of 72 fields still pass.
        self.assertTrue(study.qualification(rows(wrong(1)))['passed'])
        # Two inexact packets in one configuration fail it; the others still pass.
        q = study.qualification(rows(wrong(2)))
        self.assertFalse(q['passed'])
        self.assertEqual([g['passed'] for g in q['groups']], [(g['prompt'], g['effort']) != first for g in q['groups']])
        # Four wrong fields in one packet: 11 of 12 exact but 68 of 72 fields is below 0.95.
        four = lambda i, a, ans: {'values': {**ans['values'], '0': 1, '1': 1, '2': 1, **({} if a['withheld'] == 3 else {'3': 1})}} if i == 1 else None
        target = q0[1]
        q = study.qualification(rows(four))
        if target['withheld'] != 3:
            self.assertFalse(q['passed'])
        # A value for a withheld rare fact fails the gate even when everything else is right.
        withheld = next(i for i, a in enumerate(q0) if a['withheld'])
        invent = lambda i, a, ans: {'values': {**ans['values'], str(a['withheld']): 55}} if i == withheld else None
        self.assertFalse(study.qualification(rows(invent))['passed'])
        # A null for a present single-carrier fact (what an over-cautious reading of the rule would do).
        single = next(i for i, a in enumerate(q0) if a['carriers'] == 1 and not a['withheld'] and a['prompt'] == 'rule')
        abstain = lambda i, a, ans: {'values': {**ans['values'], '3': None, '4': None, '5': None}} if i in (single,) else None
        q = study.qualification(rows(abstain))
        self.assertTrue(q['passed'])                                  # one such packet is inside the gate
        both = [i for i, a in enumerate(q0) if a['carriers'] == 1 and (a['prompt'], a['effort']) == (q0[single]['prompt'], q0[single]['effort'])]
        abstain_all = lambda i, a, ans: {'values': {**ans['values'], '3': None, '4': None, '5': None}} if i in both else None
        self.assertFalse(study.qualification(rows(abstain_all))['passed'])
        # One structurally invalid call, or a missing row, fails the gate.
        q = study.qualification(rows(lambda i, a, ans: 'failed' if i == 5 else None))
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

    def test_design_counts_fresh_splits_caps_and_sizing(self):
        groups = [set(D[k]) for k in ('worlds', 'qualification_worlds', 'engineering_worlds')]
        self.assertTrue(all(not a & b for i, a in enumerate(groups) for b in groups[i + 1:]))
        self.assertLess(max(set.union(*groups)), 10000)
        self.assertEqual((D['worlds'], D['qualification_worlds'], D['engineering_worlds']),
                         (list(range(7600, 7624)), list(range(7700, 7708)), [7590, 7591]))
        parent = yaml.safe_load((study.ROOT.parent / 'sybil-scarcity-opus' / 'design.yaml').read_text())
        earlier = set(parent['worlds']) | set(parent['qualification_worlds']) | set(parent['engineering_worlds'])
        self.assertFalse(set.union(*groups) & earlier)
        self.assertEqual((D['audit_checks'], D['attacker_pass'], D['carriers'], D['arms']), ([108], [0.1], [1, 3, 9, 27, 81], ['random', 'coverage']))
        self.assertEqual(study.configurations(), [('base', 'low'), ('rule', 'low'), ('base', 'high'), ('rule', 'high')])
        packets = len(D['carriers']) * len(D['arms'])
        self.assertEqual(D['stages']['S1']['assignments'], packets * 4 * len(D['worlds']))
        self.assertEqual(D['stages']['S0']['assignments'], packets * 4 * 2 + 48)
        self.assertEqual(D['analysis']['cells'], packets * 4)
        b = D['budget']
        self.assertEqual(b['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 48, 'S1': 960})
        self.assertEqual(b['max_attempted_calls'], 1009)
        self.assertEqual(sum(b['max_calls'].values()), b['max_attempted_calls'])
        self.assertEqual({s: D['stages'][s]['assignments'] for s in ('P0', 'Q0', 'S1')}, {'P0': 1, 'Q0': 48, 'S1': 960})
        self.assertEqual((b['max_output_tokens'], b['workers'], b['retries'], b['error_body_chars']), (16000, 2, 0, 2000))
        # Failure rule: max_failed is the larger of 3 and 1% of the stage's units, rounded up.
        self.assertEqual(b['max_failed'], {'S1': max(3, math.ceil(0.01 * b['max_calls']['S1']))})
        self.assertEqual(b['max_failed']['S1'], 10)
        outage = b['billing_outage']
        self.assertEqual((outage['retry_every_seconds'], outage['max_wait_seconds'], outage['http_status'], outage['body_match']),
                         (60, 1200, [400, 402, 403], 'credit balance'))
        resends = outage['max_wait_seconds'] // outage['retry_every_seconds']
        self.assertGreaterEqual(b['max_transport_attempts'], b['max_attempted_calls'] + 2 * b['workers'] * (resends + 1))
        # Timeouts: the stage limit holds the stated per-call assumption at two in flight; the chain adds drain time.
        self.assertGreaterEqual(b['stage_timeout_seconds'], (480 * 5 + 480 * 115) / b['workers'])
        self.assertGreaterEqual(b['chain_timeout_seconds'], b['stage_timeout_seconds'] + outage['max_wait_seconds'] + chain.DRAIN_SECONDS)
        # Dollar cap: sized for a full chain on the more expensive model at the stated output allowance.
        for name, prices in D['models'].items():
            expected = (1009 * 23650 * prices['input_usd_per_million'] + (505 * 500 + 504 * 4000) * prices['output_usd_per_million']) / 1e6
            self.assertLess(expected, b['aggregate_usd'])
            self.assertEqual(set(D['efforts']) - set(prices['efforts']), set())
        self.assertEqual(D['primary_contrast']['metric'], 'rare_fabricated')

    def test_pool_workers_do_not_inherit_the_chain_sigterm_handler(self):
        code = ('import sys, signal\n'
                f'sys.path.insert(0, {str(study.ROOT / "src")!r})\n'
                'import chain, study\n'
                'def terminate(signum, frame):\n'
                '    raise chain.Terminated()\n'
                'signal.signal(signal.SIGTERM, terminate)\n'
                f'jobs = [("probe", {ENG}, None)] * 3\n'
                'out = list(study._map(study._prepare, jobs))\n'
                'print("prepared", len(out))\n')
        done = subprocess.run([sys.executable, '-c', code], capture_output=True, text=True, timeout=120)
        self.assertEqual(done.returncode, 0, done.stderr)
        self.assertIn('prepared 3', done.stdout)
        self.assertNotIn('Traceback', done.stderr)
        self.assertNotIn('Terminated', done.stderr)

    # ---------------------------------------------------------------- model ladder

    def test_model_ladder_default_override_batches_and_refusal(self):
        self.assertEqual(D['model_ladder'], ['claude-opus-5-5', 'claude-opus-5'])
        self.assertEqual((study.model(), D['model']), (FIRST, FIRST))
        self.assertEqual([study.params(s)['batch'] for s in study.STAGES], ['s0-001', 'p0-001', 'q0-001', 's1-001'])
        self.assertEqual([study.params(s)['model'] for s in study.STAGES], ['scripted', FIRST, FIRST, FIRST])
        self.assertEqual(set(study.params('S1')), {'stage', 'backend', 'batch', 'source_hash', 'code', 'model'})
        with patch.dict(os.environ, {'STUDY_MODEL': SECOND}):
            self.assertEqual(study.model(), SECOND)
            self.assertEqual([study.params(s)['batch'] for s in study.STAGES], ['s0-001', 'p0-001-opus-5', 'q0-001-opus-5', 's1-001-opus-5'])
            self.assertEqual([study.params(s)['model'] for s in study.STAGES], ['scripted', SECOND, SECOND, SECOND])
            self.assertEqual((study.params('S1', 2)['batch'], study.params('S1', 2)['continues']), ('s1-001-opus-5-r2', 's1-001-opus-5'))
            self.assertEqual(provider.request_body(PACKET, 'rule', 'high')['model'], SECOND)
            self.assertEqual(provider.stage_of('s1-001-opus-5-r2:abc'), 'S1')
        self.assertEqual(study.params('S1', 1)['batch'], 's1-001-r1')
        self.assertEqual(provider.stage_of('q0-001:abc'), 'Q0')
        for bad in ('claude-sonnet-5-5', 'claude-opus-4-8', 'opus'):
            with patch.dict(os.environ, {'STUDY_MODEL': bad}):
                with self.assertRaises(ValueError):
                    study.model()
                with self.assertRaises(ValueError):
                    study.params('P0')
                with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), self.assertRaises(ValueError):
                    provider.Anthropic(provider.Ledger(Path(td) / 'l'))
                self.assertEqual(chain.main(['status']), chain.EXIT_USAGE)
        with self.assertRaises(provider.CallFailure):
            provider.request_body(PACKET, 'base', 'low', 'claude-sonnet-5-5')
        # The assignments, and so the manifest, do not depend on the model.
        with patch.dict(os.environ, {'STUDY_MODEL': SECOND}):
            self.assertEqual([chain.manifest_line(a) for a in study.assignments('Q0')], self.manifest['stages']['Q0']['assignments'])

    def test_prices_per_model_in_reservation_and_settled_cost(self):
        usage = {'input_tokens': 20000, 'output_tokens': 1000}
        expected = {FIRST: (4, 20), SECOND: (5, 25)}
        for name, (inp, out) in expected.items():
            self.assertEqual((D['models'][name]['input_usd_per_million'], D['models'][name]['output_usd_per_million']), (inp, out))
            with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, dict(ENV, STUDY_MODEL=name)):
                client, opener, _, ledger = api(td, [message(model=name, usage=usage)], count_outcomes=[{'input_tokens': 20000}])
                _, account = call(client, study.params('P0')['batch'] + ':a')
                self.assertEqual(opener.messages()[0][1]['model'], name)
                self.assertEqual(account['model'], name)
                self.assertAlmostEqual(account['actual_usd'], (20000 * inp + 1000 * out) / 1e6)
                self.assertAlmostEqual(account['reserved_usd'], ((int(20000 * 1.02) + 64) * inp + 16000 * out) / 1e6)
                totals = ledger.transact()
                self.assertEqual((totals['models'], totals['calls_by_stage']), ([name], {'P0': 1}))
                self.assertAlmostEqual(totals['actual_usd'], account['actual_usd'])
                # A response from another model is an integrity failure; a second model in one ledger is refused.
                other = SECOND if name == FIRST else FIRST
                client2, _, _, _ = api(td, [message(model=other)], name='ledger')
                self.assertEqual(failure_of(self, client2, study.params('Q0')['batch'] + ':b').category, 'model_mismatch')
                with patch.dict(os.environ, {'STUDY_MODEL': other}):
                    client3, opener3, _, _ = api(td, [message(model=other)], name='ledger')
                    self.assertEqual(failure_of(self, client3, study.params('Q0')['batch'] + ':c').category, 'ledger_model_mismatch')
                    self.assertEqual(opener3.messages(), [])
        self.assertIn('model_mismatch', provider.INTEGRITY_FAILURES)
        self.assertIn('ledger_model_mismatch', provider.INTEGRITY_FAILURES)

    def test_coordinator_gates_per_model_and_continuations(self):
        other = 'f' * 64
        gate = lambda stage, runs, part=0, model=None: coordinator.gate(runs, stage, study.params(stage, part, model))
        s0, p0, q0 = hub_run('S0'), hub_run('P0'), hub_run('Q0')
        cases = [
            ('S0', [], None), ('S0', [s0], 'batch_exists_no_replay'),
            ('P0', [], 'exact_runtime_qualification_required:S0'), ('P0', [s0], None),
            ('P0', [hub_run('S0', status='failed')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', status='running')], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', invalid=1)], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', passed=0)], 'exact_runtime_qualification_required:S0'),
            ('P0', [hub_run('S0', source_hash=other)], 'exact_runtime_qualification_required:S0'),
            ('P0', [s0, hub_run('S0', batch='s0-002')], 'exact_runtime_qualification_required:S0'),
            ('P0', [s0, hub_run('P0', status='failed')], 'batch_exists_no_replay'),
            ('Q0', [s0], 'exact_runtime_qualification_required:P0'), ('Q0', [s0, p0], None),
            ('S1', [s0, p0], 'exact_runtime_qualification_required:Q0'),
            ('S1', [s0, p0, hub_run('Q0', status='failed', passed=0)], 'exact_runtime_qualification_required:Q0'),
            ('S1', [s0, p0, q0], None),
        ]
        for stage, runs, refusal in cases:
            if refusal:
                with self.assertRaises(ValueError) as failure:
                    gate(stage, runs)
                self.assertEqual(str(failure.exception), refusal, (stage, refusal))
            else:
                gate(stage, runs)
        # Model ladder: one S0 serves both models; P0 and Q0 are per model.
        p0b, q0b = hub_run('P0', model=SECOND), hub_run('Q0', model=SECOND)
        gate('P0', [s0, p0, q0], model=SECOND)                                     # needs only the model-free S0
        for stage, runs in (('Q0', [s0, p0]), ('Q0', [s0, p0, q0]), ('S1', [s0, p0, q0, p0b])):
            with self.assertRaises(ValueError) as failure:                         # a P0 or Q0 of the other model never qualifies
                gate(stage, runs, model=SECOND)
            self.assertIn('exact_runtime_qualification_required', str(failure.exception))
        gate('Q0', [s0, p0, p0b], model=SECOND)
        gate('S1', [s0, p0, p0b, q0b], model=SECOND)
        with self.assertRaises(ValueError):
            gate('S1', [s0, p0b, q0b])                                             # first model's S1 behind the second model's Q0
        with self.assertRaises(ValueError) as failure:
            coordinator.gate([s0], 'P0', dict(study.params('P0'), model='claude-sonnet-5-5'))
        self.assertEqual(str(failure.exception), 'model_not_in_ladder')
        # Continuations: only after a billing stop, with the next number; the chain then counts as one run.
        stopped = hub_run('S1', status='failed', invalid=900, passed=0, billing_stop=1)
        gate('S1', [s0, p0, q0, stopped], part=1)
        for runs, part in (([s0, p0, q0], 1), ([s0, p0, q0, hub_run('S1', status='failed', invalid=5)], 1),
                           ([s0, p0, q0, hub_run('S1')], 1), ([s0, p0, q0, stopped], 2)):
            with self.assertRaises(ValueError) as failure:
                gate('S1', runs, part=part)
            self.assertEqual(str(failure.exception), 'continuation_requires_billing_stop')
        q_stop = hub_run('Q0', status='failed', invalid=40, passed=0, billing_stop=1)
        q_cont = hub_run('Q0', part=1)
        gate('Q0', [s0, p0, q_stop], part=1)
        gate('S1', [s0, p0, q_stop, q_cont])                                       # stopped original + passed continuation
        with self.assertRaises(ValueError):
            gate('S1', [s0, p0, q_stop])
        with self.assertRaises(ValueError):
            gate('S1', [s0, p0, hub_run('Q0', status='failed', invalid=40, passed=0), q_cont])
        hub = FakeHub()
        ids = coordinator.enqueue(hub, 'S0')
        self.assertEqual((len(ids), hub.registered, hub.record[ids[0]]['params']), (1, [study.EXPERIMENT], study.params('S0')))
        with self.assertRaises(ValueError):
            coordinator.enqueue(hub, 'S0')
        with self.assertRaises(ValueError):
            coordinator.enqueue(hub, 'P0')
        self.assertEqual(len(hub.record), 1)

    # ---------------------------------------------------------------- provider and ledger

    def test_request_body_has_exactly_the_contract_keys(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, _, _ = api(td, [message(), message()])
            answer, account = call(client, 'p0-001:a')
            call(client, 'q0-001:b', prompt='rule', effort='high')
        self.assertEqual(answer['values'], VALUES)
        (count_url, count_body, _), (url, body, headers) = opener.sent[:2]
        self.assertEqual(list(body), ['model', 'max_tokens', 'system', 'messages', 'output_config'])
        for forbidden in ('thinking', 'temperature', 'top_p', 'top_k', 'tool_choice', 'tools', 'fallbacks', 'stop_sequences', 'metadata'):
            self.assertNotIn(forbidden, body)
            self.assertNotIn(forbidden, count_body)
        self.assertEqual((body['model'], body['max_tokens'], body['system']), ('claude-opus-5-5', 16000, provider.PROMPTS['base']))
        self.assertEqual(set(body['output_config']), {'effort', 'format'})
        self.assertEqual(body['output_config'], {'effort': 'low', 'format': {'type': 'json_schema', 'schema': provider.SCHEMA}})
        self.assertEqual([m['role'] for m in body['messages']], ['user'])          # no assistant prefill
        self.assertEqual(body['messages'][0]['content'], json.dumps(PACKET, sort_keys=True))
        self.assertEqual(list(count_body), ['model', 'system', 'messages', 'output_config'])
        self.assertEqual((count_url, url), (provider.COUNT_URL, provider.MESSAGES_URL))
        self.assertEqual({k.lower() for k in headers}, {'content-type', 'x-api-key', 'anthropic-version', 'anthropic-workspace-id'})
        second = opener.messages()[1][1]
        self.assertEqual((second['system'], second['output_config']['effort'], list(second)),
                         (provider.PROMPTS['rule'], 'high', list(body)))
        self.assertEqual({k: v for k, v in second.items() if k not in ('system', 'output_config')},
                         {k: v for k, v in body.items() if k not in ('system', 'output_config')})
        self.assertEqual((account['attempts'], account['count_attempts'], account['usage_reported'], account['count_fallback']), (1, 1, True, False))
        for prompt, effort in (('base', 'medium'), ('other', 'low'), ('rule', 'max')):
            with self.assertRaises(provider.CallFailure) as failure:
                provider.request_body(PACKET, prompt, effort)
            self.assertEqual(failure.exception.category, 'unknown_configuration')

    def test_thinking_and_redacted_thinking_blocks_are_dropped(self):
        text = {'type': 'text', 'text': json.dumps({'values': {**VALUES, '0': 12}})}
        content = [{'type': 'thinking', 'thinking': '', 'signature': 'a'}, {'type': 'redacted_thinking', 'data': 'opaque'},
                   {'type': 'thinking', 'thinking': 'summary', 'signature': 'b'}, text]
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, _, _, _ = api(td, [message(content=content), message(content=[text]), message(content=[text, text]), message(content=[]),
                                       message(content=[{'type': 'tool_use', 'id': 't', 'name': 'x', 'input': {}}]),
                                       message(text='not json'), message(text=json.dumps({'values': {'0': 1}})),
                                       message(text=' ' * 501)])
            self.assertEqual(call(client, 'q0-001:a')[0]['values']['0'], 12)
            self.assertEqual(call(client, 'q0-001:a2')[0]['values']['0'], 12)      # no thinking block at all is fine
            for i, category in enumerate(['invalid_structured_answer'] * 5 + ['answer_too_long']):
                failure = failure_of(self, client, f'q0-001:b{i}')
                self.assertEqual(failure.category, category)
                self.assertTrue(failure.accounting['usage_reported'])
                self.assertNotIn(category, provider.INTEGRITY_FAILURES)

    def test_refusal_and_other_response_failures_have_their_own_category(self):
        cases = [(message(stop='refusal', content=[]), 'refusal'), (message(stop='max_tokens'), 'nonterminal_output'),
                 (message(model='claude-opus-5'), 'model_mismatch'), (message(usage={}), 'missing_usage'),
                 (message(usage={'input_tokens': 1000, 'output_tokens': 1, 'cache_read_input_tokens': 5}), 'unexpected_cache_usage'),
                 (message(usage={'input_tokens': 10 ** 6, 'output_tokens': 1}), 'reservation_bound_breached'),
                 ([1, 2], 'invalid_response_body')]
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, ledger = api(td, [c[0] for c in cases])
            for i, (_, category) in enumerate(cases):
                failure = failure_of(self, client, f'q0-001:c{i}')
                self.assertEqual(failure.category, category)
                self.assertEqual(failure.accounting['attempts'], 1)     # never retried
            self.assertEqual((len(opener.messages()), clock.sleeps, ledger.transact()['transport_attempts']), (len(cases), [], len(cases)))
        with patch.dict(os.environ, {'SWARM_MODEL_API_KEY': '', 'SWARM_MODEL_WORKSPACE_ID': ''}), tempfile.TemporaryDirectory() as td:
            with self.assertRaises(provider.CallFailure) as failure:
                provider.Anthropic(provider.Ledger(Path(td) / 'l'))
            self.assertEqual(failure.exception.category, 'missing_credential_alias')

    def test_transport_retry_only_for_429_and_529(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, ledger = api(td, [http_error(429), message()], name='a')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['attempts'], clock.sleeps, len(opener.messages())), (2, [2], 2))
            self.assertEqual((ledger.transact()['attempted_calls'], ledger.transact()['transport_attempts']), (1, 2))
            client, opener, clock, ledger = api(td, [http_error(529), http_error(529), message()], name='b')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['attempts'], clock.sleeps), (3, [2, 6]))
            # Three 429s in a row: failure http_429 after 3 attempts, one reservation kept in full.
            client, opener, clock, ledger = api(td, [http_error(429)] * 3 + [message()], name='c')
            failure = failure_of(self, client, 's1-001:a')
            self.assertEqual((failure.category, failure.accounting['attempts'], failure.accounting['http_status']), ('http_429', 3, 429))
            self.assertEqual((len(opener.messages()), clock.sleeps), (3, [2, 6]))
            totals = ledger.transact()
            self.assertEqual((totals['attempted_calls'], totals['transport_attempts'], totals['usage_reported_calls']), (1, 3, 0))
            self.assertEqual(totals['committed_usd'], failure.accounting['reserved_usd'])
            # A 500, a 400 and a timeout are never retried.
            for name, error, category in (('d', http_error(500), 'http_500'), ('e', TimeoutError('t'), 'transport_TimeoutError'),
                                          ('f', urllib.error.URLError('x'), 'transport_URLError'), ('g', http_error(400), 'http_400')):
                client, opener, clock, _ = api(td, [error, message()], name=name)
                failure = failure_of(self, client, 's1-001:a')
                self.assertEqual((failure.category, failure.accounting['attempts']), (category, 1))
                self.assertEqual((len(opener.messages()), clock.sleeps), (1, []))
                self.assertNotIn(category, provider.INTEGRITY_FAILURES)

    def test_retry_after_is_honoured_capped_and_inside_the_request_budget(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, opener, clock, _ = api(td, [http_error(429, retry_after=11), http_error(529, retry_after=500), message()], name='a')
            _, account = call(client, 's1-001:a')
            self.assertEqual(clock.sleeps, [11, 20])                    # honoured, then capped at 20 s
            self.assertEqual(account['latency_seconds'], 31)
            sent = [t for (u, _, _), t in zip(opener.sent, opener.timeouts) if u == provider.MESSAGES_URL]
            self.assertEqual(sent, [600, 589, 569])                    # one shared request budget
            client, _, clock, _ = api(td, [http_error(429, retry_after=0), http_error(429, retry_after='soon'), message()], name='b')
            call(client, 's1-001:a')
            self.assertEqual(clock.sleeps, [2, 6])
            # No retry when the wait would not fit in what is left of the request budget.
            client, opener, clock, _ = api(td, [http_error(429), message()], name='c')
            client.b = dict(D['budget'], request_timeout_seconds=2.5)
            failure = failure_of(self, client, 's1-001:a')
            self.assertEqual((failure.category, failure.accounting['attempts'], clock.sleeps), ('http_429', 1, []))

    def test_failed_request_keeps_status_body_and_request_id_never_a_credential(self):
        secret, workspace = ENV['SWARM_MODEL_API_KEY'], ENV['SWARM_MODEL_WORKSPACE_ID']
        long_body = {'type': 'error', 'error': {'type': 'invalid_request_error',
                                               'message': 'bad request ' + secret + ' ' + workspace + ' ' + 'x' * 5000}}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            client, _, _, ledger = api(td, [http_error(400, body=long_body, request_id='req_abc123')])
            failure = failure_of(self, client, 's1-001:a')
            acc = failure.accounting
            self.assertEqual((failure.category, acc['http_status'], acc['request_id']), ('http_400', 400, 'req_abc123'))
            self.assertEqual(len(acc['error_body']), 2000)
            self.assertIn('bad request', acc['error_body'])
            stored = json.dumps(acc) + (Path(td) / 'ledger').read_text()
            for forbidden in (secret, workspace, 'x-api-key', 'anthropic-workspace-id'):
                self.assertNotIn(forbidden, stored)
            self.assertIn('[redacted]', acc['error_body'])
            # The same evidence is kept for a failed token count, and the call still proceeds.
            client, _, _, _ = api(td, [message()], count_outcomes=[http_error(400, body=long_body, request_id='req_count'), {'input_tokens': 900}], name='b')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['count_error']['http_status'], account['count_error']['request_id'], account['count_error']['category']),
                             (400, 'req_count', 'count_http_400'))
            self.assertNotIn(secret, json.dumps(account))

    def test_count_tokens_never_fails_a_call(self):
        packet = self.small[0]['packet']
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            # 400 then success: one re-send after 2 s, the counted value is used.
            client, opener, clock, _ = api(td, [message()], count_outcomes=[http_error(400), {'input_tokens': 900}], name='a')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['count_attempts'], account['counted_input_tokens'], account['count_fallback'], clock.sleeps), (2, 900, False, [2]))
            # 400 twice: fallback to the byte length of the request, and the call completes.
            usage = {'input_tokens': 23000, 'output_tokens': 40}
            client, opener, clock, ledger = api(td, [message(usage=usage)], count_outcomes=[http_error(400), http_error(400)], name='b')
            answer, account = call(client, 's1-001:a', packet=packet)
            size = len(json.dumps(provider.request_body(packet, 'base', 'low')).encode())
            self.assertEqual((account['count_attempts'], account['count_fallback'], account['counted_input_tokens'], clock.sleeps), (2, True, size, [2]))
            self.assertEqual((account['count_error']['category'], account['count_error']['http_status'], account['usage_reported']), ('count_http_400', 400, True))
            self.assertEqual(len(opener.counts()), 2)
            # The fallback reservation is at least the counted one on a sample packet (a token is at least one byte).
            self.assertGreater(size, 23537)
            self.assertGreaterEqual(client.reservation(size), client.reservation(23537))
            self.assertEqual(ledger.transact()['attempted_calls'], 1)
            # 429 three times: the retry rule, then the fallback (no further re-send).
            client, opener, clock, _ = api(td, [message()], count_outcomes=[http_error(429)] * 3, name='c')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['count_attempts'], account['count_fallback'], clock.sleeps), (3, True, [2, 6]))
            # 529 then success: retry rule only.
            client, _, clock, ledger = api(td, [message()], count_outcomes=[http_error(529), {'input_tokens': 900}], name='d')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['count_attempts'], account['attempts'], account['counted_input_tokens'], clock.sleeps), (2, 1, 900, [2]))
            self.assertEqual(ledger.transact()['transport_attempts'], 1)        # ordinary count attempts are not messages attempts
            # A timeout or a malformed body: one re-send, then the fallback.
            for name, outcomes in (('e', [TimeoutError(), TimeoutError()]), ('f', [{'input_tokens': 0}, {'nope': 1}]), ('g', [[1], TimeoutError()])):
                client, opener, clock, _ = api(td, [message()], count_outcomes=outcomes, name=name)
                _, account = call(client, 's1-001:a')
                self.assertEqual((account['count_fallback'], len(opener.counts()), len(opener.messages()), clock.sleeps), (True, 2, 1, [2]))

    def test_billing_outage_pauses_resends_and_stops(self):
        outage = D['budget']['billing_outage']
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV):
            # Credit error three times, then success: the call completes, one pause, nothing failed.
            client, opener, clock, ledger = api(td, [credit_error(), credit_error(402), credit_error(403), message()], name='a')
            answer, account = call(client, 's1-001:a')
            self.assertEqual(answer['values'], VALUES)
            self.assertEqual((account['billing_waits'], account['billing_pause'], account['attempts'], clock.sleeps), (3, 1, 4, [60, 60, 60]))
            self.assertEqual((account['billing_wait_seconds'], account['billing_error']['http_status'], account['billing_error']['request_id']), (180, 403, 'req_credit'))
            self.assertIn('credit balance', account['billing_error']['error_body'].lower())
            self.assertFalse(client.billing.paused())
            totals = ledger.transact()
            self.assertEqual((totals['attempted_calls'], totals['transport_attempts'], totals['released_calls'], totals['usage_reported_calls']), (1, 4, 0, 1))
            # An ordinary 400 is not a billing outage; neither is a credit message on another status.
            client, _, clock, _ = api(td, [http_error(400), message()], name='b')
            self.assertEqual((failure_of(self, client, 's1-001:a').category, clock.sleeps), ('http_400', []))
            client, _, clock, _ = api(td, [http_error(500, body=rehearse.CREDIT_BODY), message()], name='c')
            self.assertEqual((failure_of(self, client, 's1-001:a').category, clock.sleeps), ('http_500', []))
            # The outage outlasts the limit: 20 re-sends, then the stop category; the reservation is released.
            resends = outage['max_wait_seconds'] // outage['retry_every_seconds']
            client, opener, clock, ledger = api(td, [credit_error() for _ in range(40)], name='d')
            failure = failure_of(self, client, 's1-001:a')
            self.assertEqual(failure.category, STOP)
            self.assertNotIn(STOP, provider.INTEGRITY_FAILURES)
            self.assertEqual((len(opener.messages()), clock.sleeps, failure.accounting['billing_waits']), (resends + 1, [60] * resends, resends + 1))
            self.assertEqual((failure.accounting['attempted'], failure.accounting['released'], failure.accounting['attempts']), (False, True, resends + 1))
            totals = ledger.transact()
            self.assertEqual((totals['attempted_calls'], totals['released_calls'], totals['committed_usd'], totals['transport_attempts']), (0, 1, 0, resends + 1))
            self.assertFalse(client.billing.paused())
            # The released unit can be reserved again by a continuation run, under the same stage cap.
            client2, _, _, _ = api(td, [message()], name='d')
            call(client2, 's1-001-r1:a')
            self.assertEqual(ledger.transact()['calls_by_stage'], {'S1': 1})
            # The same rule on the token-counting endpoint: re-sends are recorded as attempts; nothing is reserved on a stop.
            client, opener, clock, ledger = api(td, [message()], count_outcomes=[credit_error(), credit_error(), {'input_tokens': 900}], name='e')
            _, account = call(client, 's1-001:a')
            self.assertEqual((account['billing_waits'], account['count_attempts'], account['counted_input_tokens'], clock.sleeps), (2, 3, 900, [60, 60]))
            self.assertEqual(ledger.transact()['transport_attempts'], 2 + 1)
            client, opener, clock, ledger = api(td, [message()], count_outcomes=[credit_error() for _ in range(40)], name='f')
            failure = failure_of(self, client, 's1-001:a')
            self.assertEqual((failure.category, failure.accounting['attempted'], opener.messages(), ledger.transact()['attempted_calls']), (STOP, False, [], 0))

    def test_ledger_caps_release_and_attempt_cap(self):
        b = D['budget']
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger')

            def reserve(call_id, micro=1):
                return ledger.transact({'type': 'reserve', 'call_id': call_id, 'micro_usd': micro, 'model': FIRST})

            def refused(event, category):
                with self.assertRaises(provider.CallFailure) as failure:
                    ledger.transact(event)
                self.assertEqual(failure.exception.category, category)
                self.assertIn(category, provider.INTEGRITY_FAILURES)
            r = lambda call_id, micro=1: {'type': 'reserve', 'call_id': call_id, 'micro_usd': micro, 'model': FIRST}
            reserve('p0-001:a')
            refused(r('p0-001:a'), 'duplicate_call_refused')
            refused(r('p0-001:b'), 'stage_call_cap_exhausted')          # P0 is capped at one call
            refused(r('p0-002:a'), 'stage_call_cap_exhausted')          # a later attempt shares the stage cap
            refused(r('s0-001:a'), 'stage_call_cap_exhausted')          # S0 may make no call
            refused(r('s2-001:a'), 'unknown_stage_refused')
            refused(r('nonsense'), 'unknown_stage_refused')
            refused({'type': 'bogus', 'call_id': 'p0-001:a'}, 'unknown_ledger_event')
            for i in range(48):
                reserve(f'q0-001:{i}')
            refused(r('q0-001:48'), 'stage_call_cap_exhausted')
            self.assertEqual(ledger.transact()['calls_by_stage'], {'P0': 1, 'Q0': 48})
            # Dollar cap: settled calls count their actual cost, open ones their full reservation.
            cap = int(b['aggregate_usd'] * 1_000_000)
            reserve('s1-001:open', 1000)
            reserve('s1-001:settled', 5000)
            ledger.transact({'type': 'response', 'call_id': 's1-001:settled', 'actual_micro_usd': 100, 'input_tokens': 7, 'output_tokens': 3})
            committed = 49 + 1000 + 100
            self.assertEqual(ledger.transact()['committed_usd'], committed / 1e6)
            refused(r('s1-001:over', cap - committed + 1), 'aggregate_budget_exhausted')
            # Release: only an open reservation, only for the billing stop; it frees the call and its dollars.
            refused({'type': 'release', 'call_id': 's1-001:settled', 'reason': STOP}, 'release_refused')
            refused({'type': 'release', 'call_id': 's1-001:none', 'reason': STOP}, 'release_refused')
            refused({'type': 'release', 'call_id': 's1-001:open', 'reason': 'http_500'}, 'release_refused')
            ledger.transact({'type': 'release', 'call_id': 's1-001:open', 'reason': STOP})
            totals = ledger.transact()
            self.assertEqual((totals['committed_usd'], totals['released_calls'], totals['calls_by_stage']['S1']), ((committed - 1000) / 1e6, 1, 1))
            refused(r('s1-001:open'), 'duplicate_call_refused')          # the same call id is never reserved twice
            reserve('s1-001:fits', cap - (committed - 1000))
            refused(r('s1-001:one-more'), 'aggregate_budget_exhausted')
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger')
            for i in range(960):
                ledger.transact({'type': 'reserve', 'call_id': f's1-001:{i}', 'micro_usd': 1, 'model': FIRST})
            with self.assertRaises(provider.CallFailure) as failure:
                ledger.transact({'type': 'reserve', 'call_id': 's1-001-r1:960', 'micro_usd': 1, 'model': FIRST})
            self.assertEqual(failure.exception.category, 'stage_call_cap_exhausted')
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), \
                patch.object(study, 'design', lambda: dict(D, budget=dict(b, max_transport_attempts=2, max_attempted_calls=1))):
            client, opener, clock, ledger = api(td, [http_error(429), http_error(429), message()])
            failure = failure_of(self, client, 's1-001:a')
            self.assertEqual(failure.category, 'transport_attempt_cap_exhausted')       # refused before sending
            self.assertEqual((failure.accounting['attempts'], len(opener.messages())), (2, 2))
            with self.assertRaises(provider.CallFailure) as refused_attempt:
                ledger.transact({'type': 'attempt', 'call_id': 's1-001:zz', 'n': 1})
            self.assertEqual(refused_attempt.exception.category, 'attempt_without_reservation')
            with self.assertRaises(provider.CallFailure) as capped:
                ledger.transact({'type': 'reserve', 'call_id': 'q0-001:c', 'micro_usd': 1, 'model': FIRST})
            self.assertEqual(capped.exception.category, 'study_call_cap_exhausted')

    # ---------------------------------------------------------------- worker

    def run_worker(self, stage, backend=None, opener=None, deadline=None, part=0, prior_dirs=(), td=None, name='out', small=True, model=None):
        hub = FakeHub()
        params = study.params(stage, part, model)
        run = FakeRun(hub, hub.add(params), params)
        own = tempfile.TemporaryDirectory() if td is None else None
        td = td or own.name
        clock = Clock()
        failure = summary = None
        try:
            with patch.dict(os.environ, ENV), (self.small_s1() if small else patch.object(study, 'EXPERIMENT', study.EXPERIMENT)):
                try:
                    summary = worker.execute(params, Path(td) / name, run, backend=backend, opener=opener, ledger_path=Path(td) / 'ledger',
                                             deadline=deadline, prior_dirs=prior_dirs, clock=clock, sleep=clock.sleep)
                except worker.StageFailed as exc:
                    failure, summary = exc.reason, exc.summary
            log = Path(td) / name / 'episodes.jsonl'
            rows = [json.loads(line) for line in log.read_text().splitlines()] if log.exists() else []
            files = sorted(p.name for p in (Path(td) / name).iterdir()) if (Path(td) / name).exists() else []
        finally:
            if own:
                own.cleanup()
        return hub.record[run.id], summary, failure, rows, files

    def test_strict_stage_first_failure_stops_dispatch_and_reports_usage(self):
        class Broken:
            def __init__(self):
                self.calls = 0

            def call(self, packet, call_id, prompt, effort):
                self.calls += 1
                raise provider.CallFailure('http_500', {'attempted': True, 'attempts': 1, 'reserved_usd': 0.4, 'http_status': 500, 'error_body': 'x'})
        backend = Broken()
        record, summary, failure, rows, _ = self.run_worker('Q0', backend=backend)
        self.assertEqual((failure, record['status']), ('invalid_rows:http_500', 'failed'))
        for key in worker.REQUIRED_METRICS:
            self.assertIn(key, record['metrics'])
        self.assertEqual((record['metrics']['qualification_passed'], record['metrics']['episodes'], record['metrics']['invalid']), (0, 48, 48))
        self.assertLessEqual(backend.calls, 2)                      # only requests already in flight finish
        self.assertEqual(record['metrics']['model_calls'], backend.calls)
        self.assertEqual((len(rows), len({r['id'] for r in rows})), (48, 48))
        self.assertEqual(sum(r['status'] == 'failed' for r in rows), backend.calls)
        self.assertEqual(sum(r['status'] == 'not_started' for r in rows), 48 - backend.calls)
        self.assertEqual((summary['not_started'], summary['graded'], summary['gate']['passed']), (48 - backend.calls, 0, False))
        self.assertTrue(all(r['model'] == FIRST and r['effort'] in ('low', 'high') for r in rows))
        self.assertEqual(rows[0]['accounting']['http_status'], 500)

    def test_s1_tolerates_a_failed_call_and_reports_bounds(self):
        stub = rehearse.Stub(fail_at={3})
        record, summary, failure, rows, files = self.run_worker('S1', opener=stub)
        self.assertIsNone(failure)
        self.assertEqual(record['status'], 'done')                        # within max_failed
        m = record['metrics']
        self.assertEqual((m['episodes'], m['invalid'], m['failed'], m['not_started'], m['model_calls'], m['billing_stop']), (40, 1, 1, 0, 40, 0))
        self.assertIn('1 failed', record['message'])
        failed = [r for r in rows if r['status'] == 'failed']
        self.assertEqual((len(failed), failed[0]['error'], failed[0]['accounting']['http_status']), (1, 'http_500', 500))
        self.assertIn('stub internal error', failed[0]['accounting']['error_body'])
        self.assertEqual((summary['failed'], summary['max_failed'], summary['failure'], summary['failure_categories']), (1, 10, None, ['http_500']))
        self.assertTrue(set(worker.ARTIFACTS) <= set(record['artifacts']) and set(worker.ARTIFACTS) <= set(files))
        # The failed call stays in its cell with bounds; nothing is dropped.
        analysis = analyze.analyze(rows)
        self.assertEqual(sum(c['assigned'] for c in analysis['cells']), 40)
        missing = [c for c in analysis['cells'] if c['missing']]
        self.assertEqual((len(missing), missing[0]['valid'], analysis['missing']['failed']), (1, 0, 1))
        self.assertEqual(missing[0]['rare_fabricated']['all_assigned_bounds'], [0.0, 1.0])
        self.assertIsNone(missing[0]['rare_fabricated']['interval'])
        # Recomputable from the saved rows.
        again = worker.summarize(summary['params'], rows, 40, None, summary['elapsed_seconds'], summary['initial_study_accounting'], summary['study_accounting'])
        self.assertEqual({k: again[k] for k in chain.SUMMARY_KEYS}, {k: summary[k] for k in chain.SUMMARY_KEYS})
        self.assertEqual(summary['by_effort']['low']['calls'] + summary['by_effort']['high']['calls'], 39)

    def test_s1_stops_when_failed_calls_exceed_the_limit(self):
        stub = rehearse.Stub(fail_at=set(range(1, 100)))
        record, summary, failure, rows, _ = self.run_worker('S1', opener=stub)
        m = record['metrics']
        self.assertIn(m['failed'], (11, 12))                              # the limit plus at most one call in flight
        self.assertEqual((record['status'], failure), ('failed', f'failed_calls_exceed_limit:{m["failed"]}'))
        self.assertEqual((m['episodes'], m['invalid'], m['not_started'], m['billing_stop']), (40, 40, 40 - m['failed'], 0))
        self.assertEqual(sum(r['status'] == 'not_started' for r in rows), 40 - m['failed'])
        self.assertEqual(len({r['id'] for r in rows}), 40)
        self.assertTrue(summary['failure'].startswith('failed_calls_exceed_limit:'))
        # Ten failures are still inside the limit.
        record, summary, failure, rows, _ = self.run_worker('S1', opener=rehearse.Stub(fail_at=set(range(1, 11))))
        self.assertEqual((record['status'], failure, record['metrics']['failed'], record['metrics']['not_started']), ('done', None, 10, 0))

    def test_integrity_failure_stops_dispatch_at_once(self):
        class WrongModel(rehearse.Stub):
            def __call__(self, request, timeout=None):
                response = super().__call__(request, timeout)
                if request.full_url == provider.MESSAGES_URL and self.answers == 3:
                    data = json.loads(response.getvalue())
                    data['model'] = 'claude-opus-4-8'
                    return Resp(json.dumps(data).encode())
                return response
        record, summary, failure, rows, _ = self.run_worker('S1', opener=WrongModel())
        self.assertEqual((record['status'], failure), ('failed', 'integrity:model_mismatch'))
        self.assertEqual(record['metrics']['failed'], 1)
        self.assertGreaterEqual(record['metrics']['not_started'], 35)
        import time as _time
        record, summary, failure, rows, _ = self.run_worker('S1', opener=rehearse.Stub(), deadline=_time.monotonic() - 1)
        self.assertEqual((failure, record['metrics']['model_calls']), ('integrity:stage_deadline', 0))
        self.assertEqual({r.get('error') for r in rows if r['status'] == 'failed'}, {'stage_deadline'})

    def test_billing_pause_then_stop_then_continuation_counts_every_unit_once(self):
        with tempfile.TemporaryDirectory() as td:
            # A pause that clears: no row fails, one pause is reported.
            record, summary, failure, rows, _ = self.run_worker('S1', opener=rehearse.Stub(credit_at=5, credit_times=3), td=td, name='clears')
            self.assertEqual((failure, record['status'], record['metrics']['failed'], record['metrics']['invalid']), (None, 'done', 0, 0))
            self.assertGreaterEqual(record['metrics']['billing_pauses'], 1)
            self.assertGreaterEqual(record['metrics']['billing_affected_calls'], 1)
            self.assertGreater(record['metrics']['billing_pause_seconds'], 0)
            self.assertEqual(record['metrics']['transport_attempts'], 40 + 3)
        with tempfile.TemporaryDirectory() as td:
            # One failed call, then an outage that does not clear.
            stub = rehearse.Stub(fail_at={2}, credit_from=9)
            record, summary, failure, rows, _ = self.run_worker('S1', opener=stub, td=td, name='part0')
            m = record['metrics']
            self.assertEqual((record['status'], failure, m['billing_stop'], m['failed']), ('failed', STOP, 1, 1))
            self.assertEqual(m['invalid'], m['failed'] + m['not_started'])
            self.assertEqual(m['model_calls'], 40 - m['not_started'])             # a stopped call made no model call
            stopped = [r for r in rows if r.get('stopped_by') == STOP]
            self.assertIn(len(stopped), (1, 2))
            self.assertTrue(all(r['status'] == 'not_started' and r['accounting']['released'] and 'error' not in r for r in stopped))
            self.assertEqual(summary['failure'], STOP)
            self.assertEqual(stub.answers, sum(r['status'] == 'completed' for r in rows))
            # A continuation is refused unless the previous part stopped on billing; then it runs exactly the open units.
            healthy = rehearse.Stub()
            record2, summary2, failure2, rows2, _ = self.run_worker('S1', opener=healthy, td=td, name='part1', part=1, prior_dirs=[Path(td) / 'part0'])
            m2 = record2['metrics']
            self.assertEqual((record2['status'], failure2), ('done', None))
            self.assertEqual((m2['episodes'], m2['invalid'], m2['failed'], m2['not_started'], m2['billing_stop']), (40, 1, 1, 0, 0))
            self.assertEqual(m2['model_calls'], m['not_started'])
            self.assertEqual(healthy.answers, m['not_started'])
            self.assertEqual({r['id'] for r in rows2}, {r['id'] for r in rows if r['status'] == 'not_started'})
            self.assertTrue(all(r['batch'] == 's1-001-r1' for r in rows2))
            combined = worker.combine([rows, rows2])
            self.assertEqual((len(combined), len({r['id'] for r in combined})), (40, 40))
            self.assertEqual((summary2['graded'], summary2['part'], summary2['part_units'], summary2['model_calls']), (39, 1, m['not_started'], 40))
            ledger = provider.Ledger(Path(td) / 'ledger').transact()
            self.assertEqual((ledger['calls_by_stage'], ledger['released_calls']), ({'S1': 40}, len(stopped)))
            analysis = json.loads((Path(td) / 'part1' / 'analysis.json').read_text())
            self.assertEqual((sum(c['assigned'] for c in analysis['cells']), sum(c['valid'] for c in analysis['cells'])), (40, 39))
            with self.assertRaises(ValueError):
                worker.combine([rows2, rows2])                                 # a unit recorded twice is an error
            # A second continuation has nothing to resume.
            record3, _, failure3, _, _ = self.run_worker('S1', opener=rehearse.Stub(), td=td, name='part2', part=2,
                                                         prior_dirs=[Path(td) / 'part0', Path(td) / 'part1'])
            self.assertEqual((record3['status'], failure3), ('failed', 'internal_RuntimeError'))

    def test_probe_success_reports_usage_and_crash_still_reports(self):
        a = study.assignments('P0')[0]
        text = json.dumps(study.scripted(a['packet']))
        usage = {'input_tokens': 23537, 'output_tokens': 38}
        opener = Script([http_error(429), message(text=text, usage=usage)], count_outcomes=[{'input_tokens': 23537}])
        record, summary, failure, rows, files = self.run_worker('P0', opener=opener)
        self.assertIsNone(failure)
        expected = {'episodes': 1, 'invalid': 0, 'failed': 0, 'model_calls': 1, 'input_tokens': 23537, 'output_tokens': 38,
                    'cost_usd': (23537 * 4 + 38 * 20) / 1e6, 'transport_attempts': 2, 'qualification_passed': 1, 'count_fallbacks': 0,
                    'billing_stop': 0, 'billing_pauses': 0, 'stage_calls_low': 1, 'stage_calls_high': 0}
        for key, value in expected.items():
            self.assertEqual(record['metrics'][key], value, key)
        self.assertEqual((rows[0]['accounting']['attempts'], rows[0]['model'], summary['model']), (2, FIRST, FIRST))
        self.assertAlmostEqual(summary['probe_measurement']['chain_projection_usd_at_probe_cost'], record['metrics']['cost_usd'] * 1009)
        self.assertTrue(set(worker.ARTIFACTS) <= set(record['artifacts']) and set(worker.ARTIFACTS) <= set(files))
        # A wrong probe answer fails the gate and the run, with usage still reported.
        wrong = json.dumps({'values': {**study.scripted(a['packet'])['values'], '5': 11}})
        record, summary, failure, _, _ = self.run_worker('P0', opener=Script([message(text=wrong, usage=usage)]))
        self.assertEqual((failure, record['status'], record['metrics']['qualification_passed'], record['metrics']['model_calls']), ('qualification_failed', 'failed', 0, 1))
        # A crash after the calls still reports usage.
        with patch.object(render, 'replay', side_effect=RuntimeError('boom')):
            record, summary, failure, rows, _ = self.run_worker('Q0', opener=rehearse.Stub())
        self.assertEqual((failure, record['status']), ('internal_RuntimeError', 'failed'))
        for key in worker.REQUIRED_METRICS:
            self.assertIn(key, record['metrics'])
        self.assertEqual((record['metrics']['model_calls'], record['metrics']['qualification_passed']), (48, 0))
        # A queued run for another source hash, another model or a wrong batch is refused before any call.
        for params in (dict(study.params('P0'), source_hash='0' * 64), study.params('P0', 0, SECOND), dict(study.params('P0'), batch='p0-002')):
            hub = FakeHub()
            run = FakeRun(hub, hub.add(params), params)
            with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), self.assertRaises(worker.StageFailed):
                worker.execute(run.params, Path(td) / 'out', run, ledger_path=Path(td) / 'l', opener=Script([]))
            self.assertEqual(hub.record[run.id]['status'], 'failed')

    # ---------------------------------------------------------------- chain

    def test_chain_stage_lists_and_projection_per_effort(self):
        for text, expected in (('S0,P0,Q0,S1', ['S0', 'P0', 'Q0', 'S1']), ('S0', ['S0']), ('p0, q0 ,s1', ['P0', 'Q0', 'S1']), ('Q0', ['Q0'])):
            self.assertEqual(chain.parse_stages(text), expected)
        for text in ('', 'S0,Q0', 'P0,S0', 'S0,S0', 'S2', 'S0,P0,S1'):
            with self.assertRaises(ValueError):
                chain.parse_stages(text)
        ok = chain.projection_check({'low': 0.0949, 'high': 0.13}, 5.0)
        self.assertTrue(ok['passed'])
        self.assertAlmostEqual(ok['projected_s1_usd'], 480 * 0.0949 + 480 * 0.13)
        self.assertEqual(ok['s1_calls_per_effort'], 480)
        self.assertFalse(chain.projection_check({'low': 0.0949, 'high': 0.40}, 5.0)['passed'])     # 45.6 + 192 > 235
        self.assertFalse(chain.projection_check({'low': 0.0949, 'high': 0.13}, 140.0)['passed'])   # 107.95 > 100 left

    def test_chain_gates_projection_stop_and_verify_detects_tampering(self):
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
            # S0, P0, Q0 with a stub whose high-effort calls use the whole output limit.
            stub = rehearse.Stub(output_tokens={'low': 40, 'high': 16000})
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0'], hub, root, ledger, opener=stub), chain.EXIT_DONE)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['model']), ('completed', FIRST))
            self.assertEqual([status['stages'][s]['status'] for s in ('S0', 'P0', 'Q0')], ['done'] * 3)
            self.assertEqual([status['stages'][s]['calls'] for s in ('S0', 'P0', 'Q0')], [0, 1, 48])
            for s in ('S0', 'P0', 'Q0'):
                for key in ('run', 'status', 'calls', 'input_tokens', 'output_tokens', 'cost_usd', 'started', 'ended'):
                    self.assertIn(key, status['stages'][s])
            self.assertEqual(stub.answers, 49)
            self.assertFalse((root / (chain.STATUS_FILE + '.tmp')).exists())
            # Replay of a finished batch is refused.
            self.assertEqual(chain.run_chain(['S0'], hub, root, ledger), chain.EXIT_STOPPED)
            self.assertEqual(chain.read_status(root)['reason'], 'batch_exists_no_replay')
            # S1: the per-effort projection from Q0's measured cost exceeds the remaining cap, so nothing is queued.
            before = len(hub.record)
            self.assertEqual(chain.run_chain(['S1'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'S1', 'projection_exceeds_cap'))
            projection = status['refused']['projection']
            self.assertFalse(projection['passed'])
            self.assertGreater(projection['q0_mean_cost_usd']['high'], projection['q0_mean_cost_usd']['low'])
            self.assertGreater(projection['projected_s1_usd'], projection['remaining_cap_usd'])
            self.assertEqual((len(hub.record), stub.answers), (before, 49))
            self.assertEqual(status['stages']['Q0']['status'], 'done')           # earlier stages stay recorded
            # resume is refused: nothing stopped on a billing outage.
            self.assertEqual(chain.run_chain([], hub, root, ledger, opener=stub, resume=True), chain.EXIT_STOPPED)
            self.assertEqual(len(hub.record), before)
            # verify: checksums against the hub, regraded rows, recomputed summary and analysis.
            report = chain.verify(hub, root)
            self.assertTrue(report['ok'], report)
            self.assertEqual((set(report['stages']), report['model']), ({'S0', 'P0', 'Q0'}, FIRST))
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
            self.assertEqual((state['ledger']['attempted_calls'], state['chain']['state'], state['model']), (49, 'stopped_at_gate', FIRST))
            self.assertNotIn('selftest-not-a-key', json.dumps(state))
            # A results directory of one model is refused for another model.
            with patch.dict(os.environ, {'STUDY_MODEL': SECOND}):
                self.assertEqual(chain.run_chain(['P0'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
                # status and verify read a directory as the model its attempt ran on, whatever the environment says.
                self.assertEqual((chain.chain_status(root, ledger)['model'], chain.verify(hub, root)['model']), (FIRST, FIRST))
                self.assertTrue(chain.verify(hub, root)['stages']['P0']['ok'])
                self.assertEqual(os.environ['STUDY_MODEL'], SECOND)
            self.assertEqual(len(hub.record), before)

    def test_chain_stops_at_failed_qualification(self):
        invariants = {'checks': {'mocked_in_this_test': True}, 'passed': True, 'jobs': 0}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), patch.object(study, 'check_invariants', lambda: invariants):
            root, ledger, hub, stub = Path(td) / 'results', Path(td) / 'l.jsonl', FakeHub(), rehearse.Stub('invent')
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0', 'S1'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'Q0', 'qualification_failed'))
            self.assertNotIn('S1', status['stages'])
            self.assertEqual([r['params']['stage'] for r in hub.record.values()], ['S0', 'P0', 'Q0'])
            q0 = hub.by_batch()['q0-001']
            self.assertEqual((q0['status'], q0['metrics']['qualification_passed'], q0['metrics']['model_calls'], q0['metrics']['invalid']), ('failed', 0, 48, 0))
            self.assertEqual(stub.answers, 49)

    def test_chain_s1_over_the_failure_limit_stops_and_is_verifiable(self):
        invariants = {'checks': {'mocked_in_this_test': True}, 'passed': True, 'jobs': 0}
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), patch.object(study, 'check_invariants', lambda: invariants), self.small_s1():
            root, ledger, hub = Path(td) / 'results', Path(td) / 'l.jsonl', FakeHub()
            stub = rehearse.Stub(fail_at=set(range(55, 200)))                 # S1 starts at request 50
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0', 'S1'], hub, root, ledger, opener=stub), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            s1 = hub.by_batch()['s1-001']
            self.assertEqual((status['state'], status['stopped_stage'], s1['status'], s1['metrics']['billing_stop']), ('stopped_at_gate', 'S1', 'failed', 0))
            self.assertTrue(status['reason'].startswith('failed_calls_exceed_limit:'))
            self.assertIn(s1['metrics']['failed'], (11, 12))
            self.assertEqual(s1['metrics']['invalid'], s1['metrics']['failed'] + s1['metrics']['not_started'])
            self.assertEqual(40 - s1['metrics']['invalid'], 5)                  # the five calls answered before the outage of answers
            report = chain.verify(hub, root, manifest=self.small_manifest())
            self.assertTrue(report['ok'], report)
            self.assertEqual((report['stages']['S1']['stage_failed'], report['stages']['S1']['failure']), (s1['metrics']['failed'], status['reason']))
            # Nothing is resumable: only a billing stop is.
            before = len(hub.record)
            self.assertEqual(chain.run_chain([], hub, root, ledger, opener=rehearse.Stub(), resume=True), chain.EXIT_STOPPED)
            self.assertEqual(len(hub.record), before)

    def test_chain_billing_stop_resume_and_second_model_relaunch(self):
        invariants = {'checks': {'mocked_in_this_test': True}, 'passed': True, 'jobs': 0}
        clock = Clock()
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, ENV), patch.object(study, 'check_invariants', lambda: invariants), self.small_s1():
            root, ledger, hub = Path(td) / 'results', Path(td) / 'l.jsonl', FakeHub()
            stub = rehearse.Stub(fail_at={52}, credit_from=60)                    # 1 probe + 48 Q0, then S1
            self.assertEqual(chain.run_chain(['S0', 'P0', 'Q0', 'S1'], hub, root, ledger, opener=stub, sleep=clock.sleep), chain.EXIT_STOPPED)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'S1', STOP))
            s1 = hub.by_batch()['s1-001']
            self.assertEqual((s1['status'], s1['metrics']['billing_stop'], s1['metrics']['failed']), ('failed', 1, 1))
            self.assertTrue(any('Billing pause' in m for m in s1['messages']) or s1['metrics']['billing_pauses'] >= 1)
            self.assertTrue(status['stages']['S1']['projection']['passed'])
            open_units = s1['metrics']['not_started']
            # The second model can be started on the same hub and source hash: own batches, ledger and directory.
            with patch.dict(os.environ, {'STUDY_MODEL': SECOND}):
                root2, ledger2, stub2 = Path(td) / 'results-opus-5', Path(td) / 'l-opus-5.jsonl', rehearse.Stub()
                self.assertEqual(chain.run_chain(['P0', 'Q0', 'S1'], hub, root2, ledger2, opener=stub2, sleep=clock.sleep), chain.EXIT_DONE)
                batches = hub.by_batch()
                for batch in ('p0-001-opus-5', 'q0-001-opus-5', 's1-001-opus-5'):
                    self.assertEqual((batches[batch]['status'], batches[batch]['params']['model']), ('done', SECOND))
                self.assertEqual(sum(r['params']['stage'] == 'S0' for r in hub.record.values()), 1)      # one S0 serves both
                totals = provider.Ledger(ledger2).transact()
                self.assertEqual((totals['models'], totals['calls_by_stage']), ([SECOND], {'P0': 1, 'Q0': 48, 'S1': 40}))
                self.assertAlmostEqual(totals['actual_usd'], (totals['input_tokens'] * 5 + totals['output_tokens'] * 25) / 1e6)
                report = chain.verify(hub, root2, manifest=self.small_manifest())
                self.assertTrue(report['ok'], report)
                self.assertEqual((report['model'], set(report['stages'])), (SECOND, {'P0', 'Q0', 'S1'}))
                rows = analyze.read_rows(Path(chain.read_status(root2)['stages']['S1']['results_dir']) / 'episodes.jsonl.gz')
                self.assertEqual({r['model'] for r in rows}, {SECOND})
                self.assertEqual(json.loads((Path(chain.read_status(root2)['stages']['S1']['results_dir']) / 'analysis.json').read_text())['model'], SECOND)
            # Resume the first model's stage: a continuation with exactly the open units, same ledger and caps.
            healthy = rehearse.Stub()
            self.assertEqual(chain.run_chain([], hub, root, ledger, opener=healthy, sleep=clock.sleep, resume=True), chain.EXIT_DONE)
            status = chain.read_status(root)
            self.assertEqual((status['state'], status['stages']['S1']['stage_status'], status['stages']['S1']['status']), ('completed', 'done', 'failed'))
            cont = status['stages']['S1']['continuations']
            self.assertEqual((len(cont), cont[0]['batch'], cont[0]['status'], cont[0]['calls'], healthy.answers), (1, 's1-001-r1', 'done', open_units, open_units))
            r1 = hub.by_batch()['s1-001-r1']
            self.assertEqual((r1['params']['continues'], r1['metrics']['invalid'], r1['metrics']['failed'], r1['metrics']['episodes']), ('s1-001', 1, 1, 40))
            self.assertEqual(provider.Ledger(ledger).transact()['calls_by_stage'], {'P0': 1, 'Q0': 48, 'S1': 40})
            report = chain.verify(hub, root, manifest=self.small_manifest())
            self.assertTrue(report['ok'], report)
            self.assertEqual((report['stages']['S1']['parts'], report['stages']['S1']['stage_valid'], report['stages']['S1']['checks']['no_unit_counted_twice']), (2, 39, True))
            self.assertIn('primary', report['stages']['S1'])
            # Nothing is left to resume, and mixing the two models' rows is refused by the analysis.
            before = len(hub.record)
            self.assertEqual(chain.run_chain([], hub, root, ledger, opener=healthy, resume=True), chain.EXIT_STOPPED)
            self.assertEqual(len(hub.record), before)
            first_rows = analyze.read_rows(Path(cont[0]['results_dir']) / 'episodes.jsonl.gz')
            with self.assertRaises(ValueError):
                analyze.analyze(first_rows + rows)

    # ---------------------------------------------------------------- analysis and rendering

    def test_primary_contrast_bootstrap_and_missing_outcome_bounds(self):
        tasks = D['worlds']
        base, rule = (1, 'random', 'base', 'low'), (1, 'random', 'rule', 'low')
        full = {base: {t: 1.0 for t in tasks}, rule: {t: (1 / 3 if i % 2 else 2 / 3) for i, t in enumerate(tasks)}}
        result = analyze.analyze(synthetic_rows(full))
        primary = result['primary']
        self.assertEqual((primary['metric'], primary['roots'], primary['complete_roots'], result['model']), ('rare_fabricated', 24, 24, FIRST))
        self.assertAlmostEqual(primary['mean'], 0.5)                      # base minus rule: positive = the rule reduces fabrication
        lo, hi = primary['interval']
        self.assertTrue(1 / 3 <= lo < 0.5 < hi <= 2 / 3)
        self.assertEqual(primary['interval'], analyze.analyze(synthetic_rows(full))['primary']['interval'])   # fixed seed
        missing = {base: dict(full[base]), rule: dict(full[rule])}
        missing[base][tasks[0]] = None
        missing[rule][tasks[1]] = None
        result = analyze.analyze(synthetic_rows(missing))
        primary = result['primary']
        self.assertEqual((primary['roots'], primary['complete_roots'], primary['mean'], primary['interval']), (24, 22, None, None))
        lo, hi = primary['all_assigned_bounds']
        # Root 0: unknown minus 2/3 is in [-2/3, 1/3]; root 1: 1 minus unknown is in [0, 1]. Never dropped, never zero.
        rest = sum(full[base][t] - full[rule][t] for t in tasks[2:])
        self.assertAlmostEqual(lo, (rest - 2 / 3 + 0) / 24)
        self.assertAlmostEqual(hi, (rest + 1 / 3 + 1) / 24)
        self.assertAlmostEqual(primary['complete_case_mean'], rest / 22)
        cell = next(c for c in result['cells'] if c['prompt'] == 'base')
        self.assertEqual((cell['assigned'], cell['valid'], cell['missing'], cell['rare_fabricated']['interval']), (24, 23, 1, None))
        self.assertAlmostEqual(cell['rare_fabricated']['all_assigned_bounds'][1] - cell['rare_fabricated']['all_assigned_bounds'][0], 1 / 24)

    def test_analysis_cells_contrasts_reference_and_conditionals(self):
        result = analyze.analyze(self.rows)
        self.assertEqual((result['cell_count'], len(result['cells'])), (40, 40))
        self.assertTrue(all(c['assigned'] == 1 == c['valid'] for c in result['cells']))
        self.assertEqual(result['invariance'], {'matched_cells': 2, 'violations': 0, 'packets': 10, 'configuration_violations': 0})
        self.assertEqual((len(result['secondary']), len(result['cost_side']), len(result['rule_minus_base_by_carriers'])), (7, 16, 60))
        self.assertEqual(result['replication_of_earlier_primary']['metric'], 'rare_accuracy')
        self.assertEqual({(c['carriers'], c['label'].split(':')[0]) for c in result['cost_side']}, {(27, 'cost side'), (81, 'cost side')})
        for c in result['cells']:
            follower = 'rule_follower' if c['prompt'] == 'rule' else 'plurality'
            for m in ('rare_accuracy', 'rare_fabricated'):
                self.assertAlmostEqual(c['reference'][follower]['model_minus_' + m], 0)     # scripted rows follow their prompt
                self.assertAlmostEqual(c[m]['mean_valid'], c['reference'][follower][m])
            self.assertEqual(c['rare_facts']['answered'], 3)
            self.assertEqual(sum(c['rare_facts'][o] for o in study.OUTCOMES), 3)
            for name in ('conditional_on_truth_admitted', 'conditional_on_checked_truth_admitted'):
                self.assertEqual(sum(c[name][o] for o in study.OUTCOMES), c[name]['denominator'])
            self.assertLessEqual(c['conditional_on_checked_truth_admitted']['denominator'], c['conditional_on_truth_admitted']['denominator'])
        self.assertEqual(len(result['reference_cells']), 10)
        tampered = [dict(r) for r in self.rows]
        tampered[0]['admitted_hash'] = 'different'
        tampered[1]['packet_hash'] = 'different'
        t = analyze.analyze(tampered)['invariance']
        self.assertEqual((t['violations'], t['configuration_violations']), (1, 1))
        self.assertEqual(json.loads(json.dumps(result)), json.loads(json.dumps(analyze.analyze(self.rows))))
        with self.assertRaises(ValueError):
            analyze.analyze(self.rows + [dict(self.rows[0], model=SECOND)])              # models are never pooled

    def test_frames_initial_progress_failure_final_and_replay(self):
        for stage, rows, total in (('S1', [], 960), ('S0', self.rows[:7], 128), ('Q0', [], 48), ('P0', [], 1)):
            self.assertEqual(render.frame(rows, total, stage).size, (1800, 1200))
        failed = dict(self.rows[0], status='failed', error='http_500')
        failed.pop('evaluation')
        not_started = dict(self.rows[1], status='not_started')
        not_started.pop('evaluation')
        partial = render.frame([failed, not_started] + self.rows[2:20], 960, 'S1', 12, {'actual_usd': 1.5, 'committed_usd': 2.0, 'attempted_calls': 20})
        self.assertEqual(partial.size, (1800, 1200))
        self.assertNotEqual(partial.tobytes(), render.frame([], 960, 'S1').tobytes())
        probe = study.assignments('P0')[0]
        row = {k: probe[k] for k in study.ROW_KEYS}
        ok = dict(row, status='completed', model=FIRST, evaluation=study.evaluate(probe, study.scripted(probe['packet'])),
                  accounting={'input_tokens': 23537, 'counted_input_tokens': 23537, 'output_tokens': 38, 'actual_usd': 0.0949, 'latency_seconds': 2.9})
        self.assertEqual(render.frame([ok], 1, 'P0').size, (1800, 1200))
        self.assertEqual(render.frame([dict(row, status='failed', error='refusal')], 1, 'P0').size, (1800, 1200))
        q0 = [dict({k: a[k] for k in study.ROW_KEYS}, status='completed', model=SECOND,
                   evaluation=study.evaluate(a, study.reference_answer(a['packet'], a['prompt'])),
                   accounting={'usage_reported': True, 'output_tokens': 40, 'latency_seconds': 3.0}) for a in study.assignments('Q0')]
        self.assertEqual(render.frame(q0, 48, 'Q0').size, (1800, 1200))
        with tempfile.TemporaryDirectory() as td:
            frames = render.replay(self.rows, Path(td), 'S1', 40)
            self.assertEqual(frames, 33)
            with Image.open(Path(td) / 'replay.gif') as gif:
                self.assertEqual((gif.n_frames, gif.size), (33, (1800, 1200)))
                for i in range(gif.n_frames):
                    gif.seek(i)
                    gif.load()
            for name in ('initial_frame.png', 'final_frame.png'):
                with Image.open(Path(td) / name) as im:
                    self.assertEqual(im.size, (1800, 1200))
            self.assertEqual(render.replay([], Path(td), 'S1', 40), 1)
        self.assertIsNotNone(render.font(20))

    # ---------------------------------------------------------------- package consistency

    def test_manifest_regenerates_identically(self):
        built = manifest.build()
        self.assertEqual({s: built['stages'][s]['count'] for s in study.STAGES}, {'S0': 128, 'P0': 1, 'Q0': 48, 'S1': 960})
        for s in study.STAGES:
            ids = [line.split()[0] for line in built['stages'][s]['assignments']]
            self.assertEqual(len(set(ids)), len(ids))
        s1 = [line.split() for line in built['stages']['S1']['assignments']]
        self.assertEqual({c: sum(x[1] == c for x in s1) for c in ('base-low', 'rule-low', 'base-high', 'rule-high')},
                         {'base-low': 240, 'rule-low': 240, 'base-high': 240, 'rule-high': 240})
        self.assertEqual(built['source_hash'], study.source_hash())
        self.assertEqual(built['prompt_sha256'], {k: D['prompt_sha256'][k] for k in ('base', 'rule')})
        committed = (study.ROOT / 'manifest.json').read_text()
        self.assertEqual(committed, manifest.render(built))
        self.assertLess(len(committed), 300_000)

    def test_ready_file_matches_design_and_source(self):
        ready = yaml.safe_load((study.ROOT / 'READY.yaml').read_text())
        b = D['budget']
        self.assertEqual(set(ready), {'contract', 'study', 'experiment', 'stages', 'model', 'model_ladder', 'effort', 'max_calls',
                                      'max_calls_total', 'usd_cap', 'chain_timeout_seconds', 'selftests', 'source_hash'})
        self.assertEqual((ready['contract'], ready['study'], ready['experiment']), ('ready-chain-v1', study.EXPERIMENT, study.EXPERIMENT))
        self.assertEqual(ready['stages'], list(study.STAGES))
        self.assertEqual((ready['model'], ready['model_ladder'], ready['effort']), (FIRST, D['model_ladder'], 'low'))
        self.assertEqual((ready['max_calls'], ready['max_calls_total']), (b['max_calls'], b['max_attempted_calls']))
        self.assertEqual((ready['usd_cap'], ready['chain_timeout_seconds']), (b['aggregate_usd'], b['chain_timeout_seconds']))
        self.assertEqual(ready['source_hash'], study.source_hash())
        self.assertEqual(ready['selftests'], unittest.defaultTestLoader.loadTestsFromTestCase(Tests).countTestCases())
        experiment = yaml.safe_load((study.ROOT / 'experiment.yaml').read_text())
        self.assertEqual(experiment['id'], study.EXPERIMENT)
        self.assertTrue(set(worker.REQUIRED_METRICS) | {'qualification_passed', experiment['primary_metric'], 'failed', 'count_fallbacks',
                                                        'billing_pauses', 'billing_pause_seconds', 'billing_affected_calls'} <= set(experiment['metrics']))
        self.assertIn('model', experiment['params'])

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
