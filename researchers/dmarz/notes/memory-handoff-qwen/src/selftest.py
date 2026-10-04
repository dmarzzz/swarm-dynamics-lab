"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the
standard unittest summary ("Ran N tests ... OK") on stderr.

The 28 tests of the reference adapter (test_openrouter_provider.py, an unmodified copy) run
against this study's provider.py as part of the same suite.
"""
import collections
import copy
import difflib
import gzip
import hashlib
import inspect
import io
import json
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

import analyze      # noqa: E402
import chain        # noqa: E402
import coordinator  # noqa: E402
import journal      # noqa: E402
import manifest     # noqa: E402
import provider     # noqa: E402
import rehearse     # noqa: E402
import render       # noqa: E402
import sim          # noqa: E402
import study        # noqa: E402
import worker       # noqa: E402

sys.modules.setdefault('openrouter_provider', provider)        # the reference tests import the adapter by its reference name
import test_openrouter_provider as reference_tests  # noqa: E402

D = study.design(); C = study.cfg(); B = D['budget']
KEY = 'selftest-key-not-a-credential-0123456789'
REPO = study.ROOT.parents[3]
TRUTH_FREE = lambda state, policy: (policy == 'reset' or state in ('copies', 'false_original')
                                    or (state in ('misquote', 'stale') and policy in ('raw', 'metadata')))
ALL_ROOTS = D['roots'] + D['engineering_roots'] + D['qualification']['roots_a'] + D['qualification']['roots_b']


class Capture(rehearse.Stub):
    """The rehearsal stub, keeping every request it was sent."""
    def __init__(self, *a, **k): super().__init__(*a, **k); self.bodies = []; self.headers = []
    def __call__(self, request, timeout=None):
        with self.lock: self.bodies.append(request.data); self.headers.append(dict(request.header_items()))
        return super().__call__(request, timeout)


class Clock:
    def __init__(self): self.t = 0.0; self.waits = []; self.lock = threading.Lock()
    def now(self):
        with self.lock: return self.t
    def sleep(self, s):
        with self.lock: self.waits.append(s); self.t += s


class FakeRun:
    def __init__(self, run_id, params, row=None):
        self.id, self.params, self.attempt = run_id, params, 1; self.final = None; self.row = row; self.messages = []; self.artifacts = {}
    def __enter__(self): return self
    def __exit__(self, et, ev, tb):
        if self.final is None: self.close('fail' if et else 'done', None, {})
        return False
    def progress(self, *a, **k):
        if k.get('message'): self.messages.append(k['message'])
        return True
    def artifact(self, path, name=None):
        name = name or Path(path).name; self.artifacts[name] = hashlib.sha256(Path(path).read_bytes()).hexdigest()
        if self.row is not None: self.row['artifacts'] = [{'name': n, 'sha256': h} for n, h in self.artifacts.items()]
        return {'name': name}
    def close(self, kind, message, metrics):
        self.final = (kind, metrics); self.message = message
        if self.row is not None: self.row.update(status='done' if kind == 'done' else 'failed', metrics=metrics)
    def done(self, message=None, **metrics): self.close('done', message, metrics)
    def fail(self, message=None, **metrics): self.close('fail', message, metrics)


class FakeHub:
    def __init__(self): self.rows = []; self.queue = []; self.registered = None; self.n = 0
    def runs(self, experiment=None, status=None, limit=200): return [copy.deepcopy(r) for r in self.rows]
    def get_run(self, run): return copy.deepcopy(next(r for r in self.rows if r['run'] == run))
    def register(self, experiment, **kw): self.registered = experiment
    def enqueue(self, experiment, params_list, tags=None):
        ids = []
        for p in params_list:
            self.n += 1; rid = f'{experiment}/{self.n:08d}'; ids.append(rid)
            self.rows.append({'run': rid, 'status': 'planned', 'params': p, 'metrics': {}, 'artifacts': []}); self.queue.append(rid)
        return ids
    def next_run(self, experiment=None):
        if not self.queue: return None
        rid = self.queue.pop(0); row = next(r for r in self.rows if r['run'] == rid); row['status'] = 'running'
        return FakeRun(rid, row['params'], row)
    def add(self, stage, status='done', invalid=0, passed=1, source_hash=None, batch=None, **metrics):
        p = study.params(stage); p['source_hash'] = source_hash or p['source_hash']; p['batch'] = batch or p['batch']
        self.rows.append({'run': f'x/{stage}{len(self.rows)}', 'status': status, 'params': p, 'artifacts': [],
                          'metrics': dict({'invalid': invalid, 'qualification_passed': passed, 'model_calls': 23, 'cost_usd': 0.001,
                                           'cost_per_call_usd': 0.00005, 'tokens_per_byte_max': 0.34}, **metrics)})


class Env:
    """A temporary results directory, ledger and credential alias for one test."""
    def __enter__(self):
        self.td = tempfile.TemporaryDirectory(); self.path = Path(self.td.name)
        self.patch = patch.dict(os.environ, {provider.KEY_ENV: KEY, provider.LEDGER_ENV: str(self.path / 'ledger' / 'ledger.jsonl'),
                                             'STUDY_RESULTS_DIR': str(self.path / 'results')})
        self.patch.start(); return self
    def __exit__(self, *a):
        self.patch.stop(); self.td.cleanup(); return False


def stage(name, env, stub, run=None, clock=None, **kw):
    """Run one stage through the worker and the real adapter with a stub endpoint. Returns (summary or None, rows, reason)."""
    out = env.path / 'results' / f'{name}-{len(list((env.path / "results").glob("*"))) if (env.path / "results").exists() else 0}'
    clock = clock or Clock()
    params = kw.pop('params', None) or study.params(name)
    try:
        summary = worker.execute(params, out, run, opener=stub, clock=clock.now, sleep=clock.sleep, **kw); reason = None
    except worker.StageFailed as exc:
        summary = json.loads((out / 'summary.json').read_text()) if (out / 'summary.json').exists() else None; reason = str(exc)
    rows = study.read_rows(out) if (out / 'episodes.jsonl.gz').exists() else []
    return summary, rows, reason, out


def probe_row(env):
    summary, rows, reason, _ = stage('P0', env, rehearse.Stub('reference'))
    assert reason is None and len(rows) == 1
    return rows[0]


def http(status, body=b'{"error":{"message":"x"}}', headers=None):
    return urllib.error.HTTPError(provider.URL, status, 'err', headers or {}, io.BytesIO(body))


def ok_response(answer, **over):
    data = {'id': 'gen-1', 'model': D['canonical_model'], 'provider': 'Alibaba',
            'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': answer if isinstance(answer, str) else json.dumps(answer)}}],
            'usage': {'prompt_tokens': 1200, 'completion_tokens': 20}}
    data.update(over); return data


def adapter(env, script):
    script = list(script); sent = []
    def opener(request, timeout=None):
        sent.append(json.loads(request.data)); item = script.pop(0)
        if isinstance(item, BaseException): raise item
        return rehearse.Response(json.dumps(item).encode())
    clock = Clock(); ledger = provider.Ledger(os.environ[provider.LEDGER_ENV], B)
    return provider.OpenRouter(ledger, study.provider_config(), opener, clock.now, clock.sleep), sent, clock, ledger


def synthetic(outcome, roots=None, missing=()):
    """S1-shaped rows with a chosen outcome per (root, state, policy); `missing` cells are not started."""
    rows = []
    for a in study.assignments('S1'):
        if roots is not None and a['root'] not in roots: continue
        r = {k: a[k] for k in study.ROW_KEYS}
        key = (a['root'], a['state'], a['policy'])
        if key in missing:
            r['status'] = 'not_started'
        else:
            e = a['evaluator']; kind = outcome(*key)
            value = {'T': e['truth_answer'], 'F': e['false_answer'], 'N': None, 'R': a['evaluator']['expected_value']}[kind]
            answer = {'value': value, 'sources': sim.reference(a['packet'])['sources'] if value is not None else []}
            r.update(status='completed', answer=answer, evaluation=study.evaluate(a, answer), accounting={}, retrieval=dict(a['retrieval'], seconds=0.0))
        rows.append(r)
    return rows


class Instrument(unittest.TestCase):
    def test_copied_resolver_and_decoder_are_textually_identical_to_bench_v3(self):
        # Hashes of the function text at swarm-lab commit ce2c87fe; the files themselves are compared when present.
        self.assertEqual(hashlib.sha256(inspect.getsource(sim.resolve).encode()).hexdigest(),
                         '2bb1c6055ac924894b46ce4c5317b826fc66148cc46d81e8d786ba6fbb404710')
        self.assertEqual(hashlib.sha256(inspect.getsource(sim.strict_json).encode()).hexdigest(),
                         '347754128dbe51e5da771ad54f6527dde23dda907057d311c11dec39a033c63c')
        bench = REPO / 'researchers/dmarz/notes/discussion-dose/src/bench_v3'
        if (bench / 'evidence.py').is_file():
            self.assertIn(inspect.getsource(sim.resolve), (bench / 'evidence.py').read_text())
            self.assertIn(inspect.getsource(sim.strict_json), (bench / 'contracts.py').read_text())
            for name, key in (('evidence.py', 'evidence_sha256'), ('scoring.py', 'scoring_sha256'), ('contracts.py', 'contracts_sha256'),
                              ('journal.py', 'journal_sha256'), ('worlds.py', 'worlds_sha256')):
                self.assertEqual(hashlib.sha256((bench / name).read_bytes()).hexdigest(), D['parent'][key], name)

    def test_adapter_copy_differs_from_the_reference_by_one_documented_change(self):
        reference = REPO / D['parent']['adapter']
        if not reference.is_file(): self.skipTest('reference adapter not in this checkout')
        self.assertEqual(hashlib.sha256(reference.read_bytes()).hexdigest(), D['parent']['adapter_sha256'])
        diff = list(difflib.unified_diff(reference.read_text().splitlines(), (study.ROOT / 'src/provider.py').read_text().splitlines(), lineterm='', n=0))
        removed = [l[1:] for l in diff if l.startswith('-') and not l.startswith('---')]
        added = [l[1:] for l in diff if l.startswith('+') and not l.startswith('+++')]
        self.assertEqual(removed, ['            obj = json.loads(text)'])
        self.assertIn('            obj = json.loads(text, object_pairs_hook=_no_duplicate_keys)', added)
        self.assertTrue(all('json.loads' not in l or '_no_duplicate_keys' in l for l in added))
        tests = REPO / 'researchers/dmarz/notes/pipeline/reference/test_openrouter_provider.py'
        self.assertEqual(tests.read_bytes(), (study.ROOT / 'src/test_openrouter_provider.py').read_bytes())

    def test_worlds_are_deterministic_balanced_and_collision_free(self):
        self.assertEqual(sim.world(5401, C), sim.world(5401, C))
        families = collections.Counter(sim.world(r, C)['family'] for r in D['roots'])
        self.assertEqual(dict(families), {f: 8 for f in sim.FAMILIES})
        for root in ALL_ROOTS:
            w = sim.world(root, C); d = w['delta']
            numbers = [w['truth'], w['false'], w['truth'] + d, w['false'] + d] + [x['value'] for x in w['distractors']] + [x['value'] + d for x in w['distractors']]
            self.assertEqual(len(set(numbers)), len(numbers)); self.assertGreaterEqual(min(numbers), 10)
            self.assertTrue(w['key'].endswith('.' + C['target_field'][w['family']]))
            self.assertTrue(C['false_offset'][0] <= abs(w['truth'] - w['false']) <= C['false_offset'][1])
            self.assertNotIn(w['key'], [x['key'] for x in w['distractors']])
        with self.assertRaises(ValueError): sim.world(10000, C)

    def test_every_design_invariant_holds(self):
        inv = study.check_invariants()
        self.assertEqual(len(inv['checks']), 25)
        for name, passed in inv['checks'].items():
            with self.subTest(name): self.assertTrue(passed)
        self.assertLessEqual(inv['sizes']['max_request_bytes'], 6000)

    def test_reference_equals_the_hand_written_table_in_every_cell(self):
        seen = collections.Counter()
        for a in study.assignments('S1') + study.assignments('S0'):
            ref = sim.reference(a['packet']); e = a['evaluator']
            want = {'T': e['truth_answer'], 'F': e['false_answer'], 'N': None}[C['expected'][a['state']][a['policy']]]
            self.assertEqual(ref['value'], want, a['id']); seen[(a['state'], a['policy'])] += 1
            self.assertEqual(ref['sources'] == [], want is None)
        self.assertEqual(len(seen), 24); self.assertEqual(set(seen.values()), {24 + 6 + 2})

    def test_changing_the_hidden_truth_changes_no_truth_free_message(self):
        """Counterfactual: move T far away. Every message of a cell where no genuine record or note
        carries the truth stays byte-identical; every other message changes."""
        free = carrying = 0
        for root in ALL_ROOTS:
            w = sim.world(root, C); other = dict(w, truth=w['truth'] + 1000)
            for state in sim.STATES:
                for policy in sim.POLICIES:
                    before = sim.render(sim.handoff(w, state, policy, C)[0]); after = sim.render(sim.handoff(other, state, policy, C)[0])
                    if TRUTH_FREE(state, policy):
                        self.assertEqual(before, after, (root, state, policy)); free += 1
                    else:
                        self.assertNotEqual(before, after, (root, state, policy)); carrying += 1
        self.assertEqual((free, carrying), (42 * 16, 42 * 8))

    def test_false_original_and_copies_never_show_the_truth(self):
        for root in ALL_ROOTS:
            w = sim.world(root, C); truth = {w['truth'], w['truth'] + w['delta']}
            for policy in sim.POLICIES:
                for state in ('false_original', 'copies'):
                    packet, _ = sim.handoff(w, state, policy, C)
                    self.assertFalse(truth & set(sim.numbers(packet)), (root, state, policy))
                    self.assertNotIn(str(w['truth']), [t for t in sim.render(packet).replace(',', ' ').replace('}', ' ').split() if t.isdigit()])
            packet, _ = sim.handoff(w, 'false_original', 'content', C)
            target = [r for r in packet['retrieved_records'] if w['key'] in r['facts']]
            self.assertEqual([(r['id'], r['facts'][w['key']]) for r in target], [(w['ids']['a'], w['false'])])
            self.assertEqual(sim.reference(packet)['value'], w['false'] + w['delta'])      # supported and wrong: retrieval does not repair it

    def test_content_retrieval_returns_store_records_only(self):
        for root in D['roots'][:6]:
            w = sim.world(root, C)
            for state in sim.STATES:
                records, notes, _ = sim.state_world(w, state, C); store = {r['id']: r for r in records}
                packet, log = sim.handoff(w, state, 'content', C)
                for r in packet['retrieved_records']: self.assertEqual(r, store[r['id']])
                cited = [s for n in notes for s in n['sources']]
                extra = [r['id'] for r in packet['retrieved_records'] if r['id'] not in cited]
                self.assertEqual(extra, [w['ids']['a2']] if state == 'stale' else [])
                self.assertEqual(log['records_retrieved'], len(cited) + len(extra)); self.assertEqual(log['registry_lookups'], len(cited))

    def test_messages_carry_no_label_and_one_constant_system_prompt(self):
        for a in study.assignments('S1')[:96] + study.assignments('S0'):
            text = study.user_text(a['packet']).lower()
            for word in study.FORBIDDEN_PACKET_TEXT: self.assertNotIn(word, text)
            self.assertEqual(json.loads(study.user_text(a['packet'])), a['packet'])
            body = study.request_body(a['packet'])
            self.assertEqual(body['messages'][0], {'role': 'system', 'content': study.SYSTEM})
        for label in ('misquote', 'stale', 'false_original', 'raw inheritance', 'metadata-only', 'content-bound', 'reset'):
            self.assertNotIn(label, study.SYSTEM.lower())
        self.assertIn('{"value": <integer or null>, "sources": [<record IDs>]}', study.SYSTEM)

    def test_validate_is_structural_and_strict(self):
        good = [{'value': 5, 'sources': ['rec-a']}, {'value': None, 'sources': []}, {'value': -3, 'sources': ['x', 'y']},
                {'value': None, 'sources': ['rec-a']}, {'value': 7, 'sources': []}]          # the last two are valid structure, scored unsupported
        for obj in good: self.assertEqual(study.validate(obj), obj)
        bad = [[], {'value': 5}, {'value': 5, 'sources': ['a'], 'note': 'x'}, {'value': '5', 'sources': []}, {'value': 5.0, 'sources': []},
               {'value': True, 'sources': []}, {'value': 10001, 'sources': []}, {'value': 5, 'sources': 'rec-a'}, {'value': 5, 'sources': [1]},
               {'value': 5, 'sources': ['a', 'a']}, {'value': 5, 'sources': ['']}, {'value': 5, 'sources': ['a'] * 0 + [str(i) for i in range(17)]}]
        for obj in bad:
            with self.assertRaises(ValueError): study.validate(obj)
        with self.assertRaises(ValueError): study.decode('{"value": 1, "value": 2, "sources": []}')
        with self.assertRaises(ValueError): study.decode('{"value": NaN, "sources": []}')

    def test_scorer_known_answers(self):
        cell = {(a['state'], a['policy']): a for a in study.assignments('S1') if a['root'] == 5401}
        a = cell[('misquote', 'content')]; e = a['evaluator']; ref = sim.reference(a['packet'])
        s = study.evaluate(a, ref); self.assertEqual((s['outcome'], s['supported'], s['correct'], s['inherited_error']), ('correct', 1, 1, 0))
        note = next(n for n in a['packet']['inherited_memory'] if n['key'] == a['packet']['task']['key'])
        s = study.evaluate(a, {'value': e['false_answer'], 'sources': note['sources']})        # keeps the note despite the record
        self.assertEqual((s['outcome'], s['supported'], s['inherited_error'], s['unsupported_wrong']), ('inherited_error', 0, 1, 1))
        s = study.evaluate(a, {'value': None, 'sources': []}); self.assertEqual((s['outcome'], s['unnecessary_abstain'], s['supported']), ('abstain', 1, 0))
        s = study.evaluate(a, {'value': ref['value'], 'sources': ['rec-unknown']}); self.assertEqual((s['correct'], s['citation_valid'], s['supported'], s['unsupported_correct']), (1, 0, 0, 1))
        s = study.evaluate(a, {'value': ref['value'], 'sources': []}); self.assertEqual((s['correct'], s['supported']), (1, 0))
        s = study.evaluate(a, {'value': 4321, 'sources': ref['sources']}); self.assertEqual((s['outcome'], s['other_wrong']), ('other_wrong', 1))
        self.assertEqual(study.evaluate(a, None)['invalid'], 1); self.assertIsNone(study.evaluate(a, None)['inherited_error'])
        a = cell[('false_original', 'content')]; s = study.evaluate(a, sim.reference(a['packet']))
        self.assertEqual((s['outcome'], s['supported'], s['supported_wrong'], s['correct']), ('inherited_error', 1, 1, 0))
        a = cell[('stale', 'metadata')]; s = study.evaluate(a, {'value': a['evaluator']['false_answer'], 'sources': [sim.world(5401, C)['ids']['a']]})
        self.assertEqual((s['outcome'], s['supported'], s['inherited_error']), ('inherited_error', 0, 1))   # an inherited error the packet does not support
        a = cell[('stale', 'content')]; s = study.evaluate(a, {'value': a['evaluator']['truth_answer'], 'sources': [sim.world(5401, C)['ids']['a']]})
        self.assertEqual((s['correct'], s['citation_valid'], s['supported']), (1, 0, 0))                      # cites the superseded record
        a = cell[('contradiction', 'raw')]; s = study.evaluate(a, {'value': None, 'sources': []}); self.assertEqual((s['correct_abstain'], s['supported']), (1, 1))
        s = study.evaluate(a, {'value': None, 'sources': ['rec-x']}); self.assertEqual((s['abstain'], s['citation_valid'], s['supported']), (1, 0, 0))
        a = cell[('copies', 'raw')]; w = sim.world(5401, C)
        s = study.evaluate(a, {'value': a['evaluator']['false_answer'], 'sources': [w['ids']['a']]}); self.assertEqual(s['citation_valid'], 0)   # one origin cited, two required
        s = study.evaluate(a, {'value': a['evaluator']['false_answer'], 'sources': [w['ids']['a'], w['ids']['c2']]}); self.assertEqual(s['supported'], 1)
        a = cell[('clean', 'raw')]; s = study.evaluate(a, sim.control(a['packet'], 'wrong_entity')); self.assertEqual((s['supported'], s['correct'], s['inherited_error']), (0, 0, 0))

    def test_scripted_controls_separate_and_the_primary_is_not_fixed_by_construction(self):
        table = study.control_table(D['engineering_roots'])
        self.assertEqual({k: v['primary'] for k, v in table.items()},
                         {'reference': -0.5, 'trust_memory': 0.0, 'version_blind': -1.0, 'abstain': 0.0, 'wrong_entity': 0.0})
        self.assertEqual(table['reference']['inherited_error'],
                         {'clean': {'raw': 0.0, 'metadata': 0.0, 'content': 0.0, 'reset': 0.0},
                          'misquote': {'raw': 1.0, 'metadata': 1.0, 'content': 0.0, 'reset': 0.0},
                          'stale': {'raw': 1.0, 'metadata': 0.0, 'content': 0.0, 'reset': 0.0},
                          'copies': {'raw': 1.0, 'metadata': 0.0, 'content': 0.0, 'reset': 0.0},
                          'contradiction': {'raw': 0.0, 'metadata': 0.0, 'content': 0.0, 'reset': 0.0},
                          'false_original': {'raw': 1.0, 'metadata': 1.0, 'content': 1.0, 'reset': 0.0}})
        self.assertEqual(table['abstain']['clean_correct'], {p: 0.0 for p in sim.POLICIES})
        self.assertEqual(table['trust_memory']['clean_correct']['content'], 1.0)

    def test_stage_counts_caps_and_splits(self):
        self.assertEqual({s: len(study.assignments(s)) for s in study.STAGES}, {'S0': 192, 'P0': 1, 'Q0': 23, 'S1': 576})
        self.assertEqual(B['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 576}); self.assertEqual(B['max_attempted_calls'], 600)
        self.assertEqual((B['max_failed'], B['aggregate_usd'], B['workers'], B['request_timeout_seconds']), (6, 2, 4, 120))
        self.assertEqual(B['max_failed'], max(3, -(-576 // 100)))
        self.assertGreaterEqual(B['max_transport_attempts'] - B['max_attempted_calls'], 40)
        self.assertEqual((B['billing_outage'], B['retry']['retryable_http_status'], B['retry']['transport_retries'], B['retry']['backoff_seconds']),
                         ({'retry_every_seconds': 60, 'max_wait_seconds': 1200}, [429, 502, 503, 529], 2, [2, 6]))
        self.assertEqual(D['request_template'], {'model': 'qwen/qwen3.7-flash', 'provider': {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True},
                                                 'reasoning': {'enabled': False}, 'max_tokens': 1000, 'response_format': {'type': 'json_object'}})
        fixtures = study.qualification_fixtures('a')
        self.assertEqual(study.assignments('P0')[0]['id'], fixtures[0]['id']); self.assertEqual([a['id'] for a in study.assignments('Q0')], [f['id'] for f in fixtures[1:]])
        self.assertFalse({f['root'] for f in fixtures} & {f['root'] for f in study.qualification_fixtures('b')})
        self.assertTrue(all(r < 10000 for r in ALL_ROOTS)); self.assertEqual(len(set(ALL_ROOTS)), 42)
        order = [a['id'] for a in study.assignments('S1')]; self.assertEqual(order, [a['id'] for a in study.assignments('S1')])
        self.assertNotEqual(order, sorted(order))                                # seeded shuffle, not grid order
        worst = study.largest_request_bytes('S1') / B['assumed_min_chars_per_token']
        self.assertLess(worst, B['max_input_tokens'] / 3)                         # comfortably under the 8,000-token ceiling

    def test_qualification_gate_allows_no_miss(self):
        rows = []
        for f in study.qualification_fixtures('a'):
            answer = study.scripted(f); r = {k: f[k] for k in study.ROW_KEYS}
            r.update(status='completed', answer=answer, evaluation=study.evaluate(f, answer)); rows.append(r)
        self.assertTrue(study.qualification(rows)['passed'])
        self.assertFalse(study.qualification(rows[1:])['passed'])                # 23 rows are not 24: the probe's row is required
        one = copy.deepcopy(rows); miss = next(r for r in one if r['state'] == 'contradiction' and r['policy'] == 'raw')
        answer = sim.control(next(f for f in study.qualification_fixtures('a') if f['id'] == miss['id'])['packet'], 'trust_memory')
        miss.update(answer=answer, evaluation=study.evaluate(next(f for f in study.qualification_fixtures('a') if f['id'] == miss['id']), answer))
        q = study.qualification(one); self.assertFalse(q['passed']); self.assertEqual((q['supported'], q['misses']), (23, [miss['id']]))
        failed = copy.deepcopy(rows); failed[5]['status'] = 'failed'; self.assertFalse(study.qualification(failed)['passed'])
        citation = copy.deepcopy(rows); c = next(r for r in citation if r['answer']['value'] is not None)
        f = next(x for x in study.qualification_fixtures('a') if x['id'] == c['id'])
        c['answer'] = {'value': c['answer']['value'], 'sources': []}; c['evaluation'] = study.evaluate(f, c['answer'])
        self.assertFalse(study.qualification(citation)['passed'])               # right value, no citation: not exact agreement

    def test_probe_gate_checks_the_interface_only(self):
        f = study.assignments('P0')[0]; base = {k: f[k] for k in study.ROW_KEYS}
        acc = {'usage_reported': True, 'input_tokens': 1200, 'response_model': D['canonical_model'], 'response_provider': 'Alibaba',
               'finish_reason': 'stop', 'reasoning_tokens': 0, 'request_bytes': 4000}
        wrong = {'value': 4321, 'sources': ['rec-x']}
        row = dict(base, status='completed', answer=wrong, evaluation=study.evaluate(f, wrong), accounting=acc)
        g = study.probe_gate([row]); self.assertTrue(g['passed']); self.assertFalse(g['agrees_with_reference'])
        for change in ({'response_model': 'qwen/qwen3.7-plus'}, {'response_provider': 'DeepInfra'}, {'finish_reason': 'length'},
                       {'reasoning_tokens': 12}, {'usage_reported': False}):
            self.assertFalse(study.probe_gate([dict(row, accounting=dict(acc, **change))])['passed'], change)
        self.assertFalse(study.probe_gate([dict(row, status='failed')])['passed']); self.assertFalse(study.probe_gate([])['passed'])
        self.assertAlmostEqual(study.tokens_per_byte([row]), 0.3)

    def test_manifest_regenerates_identically_and_source_hash_covers_code_and_design_only(self):
        self.assertEqual(manifest.render(manifest.build()), manifest.PATH.read_text())
        self.assertLess(manifest.PATH.stat().st_size, 300_000)
        m = manifest.load(); self.assertEqual(m['source_hash'], study.source_hash())
        self.assertEqual({s: m['stages'][s]['count'] for s in study.STAGES}, B['max_calls'] | {'S0': 192} if hasattr(dict, '__or__') else dict(B['max_calls'], S0=192))
        self.assertEqual(m['qualification_b_reserved']['count'], 24)
        hashed = sorted(p.name for p in [study.ROOT / 'design.yaml', study.ROOT / 'experiment.yaml', study.ROOT / 'requirements.txt'] + list((study.ROOT / 'src').glob('*.py')))
        self.assertIn('provider.py', hashed); self.assertIn('test_openrouter_provider.py', hashed)
        for outside in ('README.md', 'READY.yaml', 'manifest.json', 'preregistration.md', 'SETUP.md', 'RUN.md'): self.assertNotIn(outside, hashed)

    def test_ready_file_matches_the_design_and_the_source(self):
        import yaml
        path = study.ROOT / 'READY.yaml'
        if not path.exists(): self.skipTest('READY.yaml is written after the code is pinned')
        r = yaml.safe_load(path.read_text())
        self.assertEqual((r['contract'], r['study'], r['experiment'], r['stages']), ('ready-chain-v1', study.EXPERIMENT, study.EXPERIMENT, list(study.STAGES)))
        self.assertEqual((r['provider'], r['model'], r['max_calls'], r['max_calls_total'], r['usd_cap'], r['chain_timeout_seconds']),
                         ('openrouter', D['model'], B['max_calls'], B['max_attempted_calls'], B['aggregate_usd'], B['chain_timeout_seconds']))
        self.assertEqual(r['source_hash'], study.source_hash()); self.assertEqual(r['selftests'], TOTAL['tests'])

    def test_no_secret_address_or_token_in_the_package(self):
        import re
        for path in list((study.ROOT / 'src').glob('*.py')) + [p for p in study.ROOT.glob('*') if p.is_file()]:
            text = path.read_text(errors='replace')
            for pattern in (r'sk-or-v1-[0-9a-f]{16,}', r'sk-ant-[A-Za-z0-9_-]{16,}', r'\b(?!127\.0\.0\.1)(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}\b', r'SWARM_HUB_TOKEN\s*=\s*[\'"][A-Za-z0-9]{16,}'):
                self.assertIsNone(re.search(pattern, text), (path.name, pattern))


class Adapter(unittest.TestCase):
    def test_request_is_the_frozen_template_plus_two_messages_and_sizes_agree(self):
        a = study.assignments('S1')[0]
        with Env() as env:
            api, sent, _, _ = adapter(env, [ok_response(sim.reference(a['packet']))])
            answer, acct = api.call(study.SYSTEM, study.user_text(a['packet']), 's1-001:' + a['id'], study.validate)
        self.assertEqual(sent[0], study.request_body(a['packet'])); self.assertEqual(tuple(sent[0]), provider.BODY_KEYS)
        self.assertEqual(acct['request_bytes'], a['request_bytes']); self.assertEqual(answer, sim.reference(a['packet']))
        self.assertGreaterEqual(acct['reserved_usd'] * 1e6, a['request_bytes'] * 0.03 + 1000 * 0.13 - 1e-9)    # byte-based upper bound
        self.assertEqual({k: v for k, v in sent[0].items() if k != 'messages'}, D['request_template'])

    def test_duplicate_json_keys_and_invalid_answers_are_failed_calls_with_the_text_kept(self):
        cases = {'{"value": 1, "value": 2, "sources": []}': 'invalid_json', '{"value": 1, "sources": [], "sources": []}': 'invalid_json',
                 '{"value": "7", "sources": []}': 'invalid_answer', '{"value": 7}': 'invalid_answer', 'The value is 7.': 'invalid_json',
                 '```json\n{"value": 7, "sources": []}\n```': 'invalid_json'}
        with Env() as env:
            for n, (text, want) in enumerate(cases.items()):
                api, sent, _, _ = adapter(env, [ok_response(text)])
                with self.assertRaises(provider.CallFailure) as cm: api.call(study.SYSTEM, 'U', f's1-001:x{n}', study.validate)
                self.assertEqual(cm.exception.category, want, text); self.assertEqual(len(sent), 1)       # never retried
                self.assertEqual(cm.exception.accounting['answer_text'], text); self.assertTrue(cm.exception.accounting['usage_reported'])

    def test_failed_request_keeps_status_body_and_request_id_and_no_credential(self):
        with Env() as env:
            api, sent, _, ledger = adapter(env, [http(400, b'{"error":{"message":"bad request body"}}', {'x-request-id': 'req_9'})])
            with self.assertRaises(provider.CallFailure) as cm: api.call(study.SYSTEM, 'U', 's1-001:x', study.validate)
            acct = cm.exception.accounting
            self.assertEqual((cm.exception.category, acct['http_status'], acct['request_id']), ('http_400', 400, 'req_9'))
            self.assertIn('bad request body', acct['error_body'])
            self.assertNotIn(KEY, json.dumps(acct)); self.assertNotIn('Bearer', json.dumps(acct))
            self.assertNotIn(KEY, Path(os.environ[provider.LEDGER_ENV]).read_text())

    def test_billing_error_is_a_pause_and_then_a_distinct_stop(self):
        a = study.assignments('S1')[0]; credit = lambda: http(402, rehearse.CREDIT_BODY)
        with Env() as env:
            api, sent, clock, _ = adapter(env, [credit(), credit(), credit(), ok_response(sim.reference(a['packet']))])
            answer, acct = api.call(study.SYSTEM, study.user_text(a['packet']), 's1-001:a', study.validate)
            self.assertEqual((acct['attempts'], clock.waits, api.billing['billing_pauses'], api.billing['billing_affected_calls']), (4, [60, 60, 60], 1, 1))
        with Env() as env:
            api, sent, clock, ledger = adapter(env, [credit() for _ in range(40)])
            with self.assertRaises(provider.CallFailure) as cm: api.call(study.SYSTEM, 'U', 's1-001:a', study.validate)
            self.assertEqual((cm.exception.category, sum(clock.waits)), (provider.BILLING_STOP, 1200))
            with self.assertRaises(provider.CallFailure) as cm: api.call(study.SYSTEM, 'U', 's1-001:b', study.validate)
            self.assertEqual(cm.exception.category, provider.BILLING_STOP); self.assertFalse(cm.exception.accounting['attempted'])
            self.assertEqual(ledger.transact()['attempted_calls'], 1)


class Worker(unittest.TestCase):
    def test_offline_scripted_stage_passes_and_writes_every_artifact(self):
        with Env() as env:
            run = FakeRun('s0', study.params('S0'))
            summary, rows, reason, out = stage('S0', env, None, run=run)
            self.assertIsNone(reason); self.assertTrue(summary['passed'])
            self.assertEqual((summary['planned'], summary['graded'], summary['model_calls'], summary['cost_usd'], summary['qualification_passed']), (192, 192, 0, 0, 1))
            self.assertEqual(sorted(run.artifacts), sorted(worker.ARTIFACTS)); self.assertEqual(run.final[0], 'done')
            self.assertTrue(set(worker.REQUIRED_METRICS) <= set(run.final[1]))
            self.assertTrue(summary['gate']['qualification_a']['passed'] and summary['gate']['qualification_b']['passed'])
            html = (out / 'replay.html').read_text(); self.assertIn('SCRIPTED - NOT MODEL EVIDENCE', html)
            with gzip.open(out / 'events.jsonl.gz', 'rt') as f: events = journal.read_events(f)
            self.assertTrue(journal.call_ledger_complete(events)); self.assertEqual(sum(e['kind'] == 'terminal' for e in events), 192)

    def test_scripted_stage_fails_when_an_invariant_fails(self):
        broken = {'passed': False, 'checks': {'reference_equals_hand_table': False}, 'control_table': {}, 'sizes': {}}
        with Env() as env, patch.object(study, 'check_invariants', lambda: broken):
            run = FakeRun('s0', study.params('S0'))
            summary, rows, reason, _ = stage('S0', env, None, run=run)
            self.assertEqual(reason, 'invariant_failed:reference_equals_hand_table')
            self.assertEqual((run.final[0], run.final[1]['qualification_passed'], run.final[1]['model_calls']), ('fail', 0, 0))

    def test_probe_makes_exactly_one_call_and_records_tokens_per_byte(self):
        with Env() as env:
            stub = Capture('reference'); run = FakeRun('p0', study.params('P0'))
            summary, rows, reason, _ = stage('P0', env, stub, run=run)
            self.assertIsNone(reason); self.assertEqual((len(stub.bodies), summary['model_calls'], summary['qualification_passed']), (1, 1, 1))
            self.assertAlmostEqual(summary['tokens_per_byte_max'], (rows[0]['request_bytes'] // 3) / rows[0]['request_bytes'])
            self.assertIn('tokens_per_byte_max', run.final[1]); self.assertTrue(summary['gate']['probe']['agrees_with_reference'])

    def test_qualification_reads_the_probe_row_and_fails_without_it_before_any_call(self):
        with Env() as env:
            probe = probe_row(env)
            stub = Capture('reference'); run = FakeRun('q0', study.params('Q0'))
            summary, rows, reason, _ = stage('Q0', env, stub, run=run, probe_row=probe)
            self.assertIsNone(reason); q = summary['gate']['qualification']
            self.assertEqual((q['fixtures'], q['supported'], summary['model_calls'], len(stub.bodies)), (24, 24, 23, 23))
            self.assertEqual(summary['gate']['probe_row'], probe['id']); self.assertIsNotNone(run.final[1]['cost_per_call_usd'])
        with Env() as env:
            stub = Capture('reference'); run = FakeRun('q0', study.params('Q0'))
            summary, rows, reason, _ = stage('Q0', env, stub, run=run)            # no chain-status, no saved P0 row
            self.assertEqual(reason, 'probe_row_unavailable'); self.assertEqual(len(stub.bodies), 0)
            self.assertEqual({r['status'] for r in rows}, {'not_started'}); self.assertEqual((run.final[0], run.final[1]['qualification_passed']), ('fail', 0))

    def test_failed_qualification_stops_with_metrics_and_the_misses_named(self):
        with Env() as env:
            probe = probe_row(env); run = FakeRun('q0', study.params('Q0'))
            summary, rows, reason, _ = stage('Q0', env, rehearse.Stub('trust_memory'), run=run, probe_row=probe)
            self.assertEqual(reason, 'qualification_failed'); self.assertEqual(summary['invalid'], 0)
            misses = summary['gate']['qualification']['misses']; self.assertGreater(len(misses), 0)
            self.assertTrue(all(any(m.endswith(x) for x in ('-content', '-metadata', '-raw')) for m in misses))
            self.assertEqual((run.final[0], run.final[1]['qualification_passed'], run.final[1]['model_calls']), ('fail', 0, 23))

    def test_strict_stage_stops_at_the_first_failed_call(self):
        with Env() as env:
            probe = probe_row(env); run = FakeRun('q0', study.params('Q0'))
            summary, rows, reason, _ = stage('Q0', env, rehearse.Stub('reference', fail_messages={3}), run=run, probe_row=probe)
            self.assertEqual(reason, 'invalid_rows:http_500')
            counts = collections.Counter(r['status'] for r in rows)
            self.assertEqual(counts['failed'], 1); self.assertGreaterEqual(counts['not_started'], 23 - 3 - B['workers']); self.assertEqual(sum(counts.values()), 23)
            failed = next(r for r in rows if r['status'] == 'failed')
            self.assertEqual((failed['accounting']['http_status'], failed['error']), (500, 'http_500')); self.assertIn('rehearsal injected failure', failed['accounting']['error_body'])
            self.assertEqual(run.final[0], 'fail'); self.assertTrue(set(worker.REQUIRED_METRICS) <= set(run.final[1]))

    def test_main_stage_tolerates_failed_calls_up_to_the_limit_and_stops_beyond_it(self):
        with Env() as env:
            run = FakeRun('s1', study.params('S1'))
            summary, rows, reason, out = stage('S1', env, rehearse.Stub('reference', fail_messages={10, 200, 400}), run=run)
            self.assertIsNone(reason); self.assertTrue(summary['passed'])
            self.assertEqual((summary['failed'], summary['invalid'], summary['not_started'], summary['graded'], summary['model_calls']), (3, 3, 0, 573, 576))
            self.assertEqual(run.final[0], 'done'); self.assertEqual((run.final[1]['failed'], run.final[1]['invalid']), (3, 3)); self.assertIn('3 failed (limit 6)', run.message)
            a = json.loads((out / 'analysis.json').read_text())
            self.assertEqual((a['failed'], a['observed'], a['assigned']), (3, 573, 576))
            lo, hi = a['primary']['bounds_all_assigned']; self.assertLessEqual(lo, -0.5); self.assertGreaterEqual(hi, -0.5)
        with Env() as env:
            run = FakeRun('s1', study.params('S1'))
            summary, rows, reason, _ = stage('S1', env, rehearse.Stub('reference', fail_from=20), run=run)
            self.assertEqual(reason, 'failed_units_over_limit')
            self.assertTrue(B['max_failed'] < summary['failed'] <= B['max_failed'] + B['workers'])
            self.assertGreaterEqual(summary['not_started'], 576 - 19 - B['max_failed'] - 2 * B['workers'])
            self.assertEqual(run.final[0], 'fail'); self.assertFalse(summary['resumable'])

    def test_integrity_failure_stops_the_main_stage_at_once(self):
        class WrongModel(rehearse.Stub):
            def __call__(self, request, timeout=None):
                r = super().__call__(request, timeout)
                if self.requests == 5:
                    data = json.loads(r.getvalue()); data['model'] = 'qwen/qwen3.7-plus'; return rehearse.Response(json.dumps(data).encode())
                return r
        with Env() as env:
            summary, rows, reason, _ = stage('S1', env, WrongModel('reference'))
            self.assertEqual(reason, 'integrity_failure:model_mismatch'); self.assertEqual(summary['failed'], 1)
            self.assertGreaterEqual(summary['not_started'], 576 - 5 - B['workers'])

    def test_billing_stop_fails_nothing_and_a_continuation_finishes_every_unit_once(self):
        with Env() as env:
            run = FakeRun('s1', study.params('S1'))
            summary, rows, reason, _ = stage('S1', env, rehearse.Stub('reference', credit_from=30), run=run)
            self.assertEqual(reason, provider.BILLING_STOP)
            self.assertEqual((summary['failed'], summary['resumable'], summary['billing_pauses']), (0, True, 1)); self.assertEqual(summary['billing_pause_seconds'], 1200)
            self.assertEqual(summary['graded'], 29); self.assertEqual(summary['not_started'], 576 - 29)
            self.assertIn('billing_pauses', run.final[1]); self.assertEqual(run.final[0], 'fail')
            dangling = [r for r in rows if r['status'] == 'not_started' and (r.get('accounting') or {}).get('attempted')]
            self.assertTrue(0 < len(dangling) <= B['workers']); self.assertTrue(all(r['error'] == provider.BILLING_STOP for r in dangling))
            self.assertEqual(dangling[0]['accounting'].get('http_status', 402), 402)
            units = sorted(r['id'] for r in rows if r['status'] == 'not_started')
            params = dict(study.params('S1'), batch='s1-001-r1', continuation=1)
            more, rows2, reason2, out2 = stage('S1', env, rehearse.Stub('reference'), params=params, units=units, prior_rows=rows)
            self.assertIsNone(reason2); self.assertEqual((more['planned'], more['graded'], more['continuation']['reservation_allowance']), (547, 547, len(dangling)))
            final = study.combine(rows + rows2)
            self.assertEqual(len(final), 576); self.assertEqual({r['status'] for r in final}, {'completed'}); self.assertEqual(len({r['id'] for r in final}), 576)
            a = json.loads((out2 / 'analysis.json').read_text()); self.assertEqual((a['observed'], a['primary']['estimate']), (576, -0.5))
            ledger = provider.Ledger(os.environ[provider.LEDGER_ENV], B).transact()
            self.assertEqual((ledger['usage_reported_calls'], ledger['attempted_calls']), (576, 576 + len(dangling)))
            with self.assertRaises(worker.StageFailed):                              # a continuation needs its own batch name
                worker.execute(study.params('S1'), env.path / 'results' / 'bad', None, opener=rehearse.Stub('reference'), units=units[:2], prior_rows=rows)

    def test_short_billing_outage_is_only_a_pause(self):
        with Env() as env:
            probe = probe_row(env); run = FakeRun('q0', study.params('Q0'))
            summary, rows, reason, _ = stage('Q0', env, rehearse.Stub('reference', credit_at=(4, 3)), run=run, probe_row=probe)
            self.assertIsNone(reason); self.assertEqual((summary['failed'], summary['graded']), (0, 23)); self.assertGreaterEqual(summary['billing_pauses'], 1)
            self.assertGreater(summary['billing_pause_seconds'], 0); self.assertEqual(run.final[1]['billing_pauses'], summary['billing_pauses'])

    def test_stage_refuses_a_stale_source_hash_a_wrong_batch_and_a_missing_ledger_or_credential(self):
        with Env() as env:
            run = FakeRun('s1', dict(study.params('S1'), source_hash='0' * 64))
            with self.assertRaises(worker.StageFailed) as cm: worker.execute(run.params, env.path / 'a', run, opener=rehearse.Stub('reference'))
            self.assertEqual(str(cm.exception), 'runtime_source_mismatch'); self.assertEqual(run.final[0], 'fail'); self.assertTrue(set(worker.REQUIRED_METRICS) <= set(run.final[1]))
            with self.assertRaises(worker.StageFailed) as cm: worker.execute(dict(study.params('S1'), batch='s1-999'), env.path / 'b', None, opener=rehearse.Stub('reference'))
            self.assertEqual(str(cm.exception), 'batch_mismatch')
            with patch.dict(os.environ, {provider.KEY_ENV: ''}):
                with self.assertRaises(worker.StageFailed) as cm: worker.execute(study.params('P0'), env.path / 'c', None, opener=rehearse.Stub('reference'))
                self.assertEqual(str(cm.exception), 'missing_credential_alias')
            os.environ.pop(provider.LEDGER_ENV)
            with self.assertRaises(worker.StageFailed) as cm: worker.execute(study.params('P0'), env.path / 'd', None, opener=rehearse.Stub('reference'))
            self.assertEqual(str(cm.exception), 'persistent_budget_ledger_required')


class Chain(unittest.TestCase):
    """One full chain on an in-memory hub with the capturing stub, shared by the tests below."""
    @classmethod
    def setUpClass(cls):
        cls.env = Env().__enter__(); cls.hub = FakeHub(); cls.stub = Capture('reference'); clock = Clock()
        out = io.StringIO()
        with patch('sys.stdout', out):
            cls.code = chain.run_chain(list(study.STAGES), sr=cls.hub, opener=cls.stub, clock=clock.now, sleep=clock.sleep)
        cls.printed = out.getvalue(); cls.status = chain.read_status()

    @classmethod
    def tearDownClass(cls):
        cls.env.__exit__(None, None, None)

    def test_chain_runs_all_stages_behind_the_gates(self):
        self.assertEqual(self.code, 0); self.assertEqual(self.status['state'], 'completed'); self.assertTrue(self.status['all_stages_done'])
        self.assertEqual({s: self.status['stages'][s]['calls'] for s in study.STAGES}, B['max_calls'])
        self.assertEqual([r['status'] for r in self.hub.rows], ['done'] * 4); self.assertEqual(len(self.stub.bodies), 600)
        self.assertEqual(self.status['ledger']['attempted_calls'], 600); self.assertEqual(self.status['stages']['S1']['headline']['inherited_error_content_minus_metadata'], -0.5)
        p = self.status['stages']['S1']['projection']; self.assertTrue(p['within_cap'] and p['input_ceiling_ok'])
        self.assertLess(self.status['ledger']['committed_usd'], 0.1)
        self.assertEqual(len(self.printed.strip().splitlines()), 1)

    def test_wire_level_every_request_sent_is_the_frozen_body_of_its_packet_and_nothing_else(self):
        """What actually left the adapter: byte-for-byte the request built from each assignment's
        packet, no evaluator field, and no truth in any cell where no genuine record carries it."""
        sent = collections.Counter(self.stub.bodies)
        fixtures = study.qualification_fixtures('a') + study.assignments('S1')
        want = collections.Counter(json.dumps(study.request_body(a['packet'])).encode() for a in fixtures)
        self.assertEqual(sent, want); self.assertEqual(sum(sent.values()), 600)
        for raw in sent:
            body = json.loads(raw); text = raw.decode().lower()
            self.assertEqual(tuple(body), provider.BODY_KEYS); self.assertEqual(body['messages'][0]['content'], study.SYSTEM)
            for word in ('truth', 'expected', 'evaluator', 'false_answer', 'packet_hash', 'qualification', 'r54', 'r55'):
                self.assertNotIn(word, text)
            self.assertEqual(set(json.loads(body['messages'][1]['content'])), set(sim.PACKET_KEYS))
        for a in fixtures:
            if TRUTH_FREE(a['state'], a['policy']):
                w = sim.world(a['root'], C); raw = json.dumps(study.request_body(a['packet'])).encode()
                self.assertIn(raw, sent)
                message = json.loads(json.loads(raw)['messages'][1]['content'])
                self.assertFalse({w['truth'], w['truth'] + w['delta']} & set(sim.numbers(message)), a['id'])
        for headers in self.stub.headers:
            self.assertEqual(sorted(k.lower() for k in headers), ['authorization', 'content-type'])

    def test_verify_passes_and_detects_a_changed_answer_a_changed_row_and_a_broken_journal(self):
        def run_verify():
            out = io.StringIO()
            with patch('sys.stdout', out): code = chain.verify(self.hub)
            lines = out.getvalue().strip().splitlines(); self.assertEqual(len(lines), 1)
            return code, json.loads(lines[0])
        code, report = run_verify()
        self.assertEqual(code, 0, {s: [k for k, v in x.get('checks', {}).items() if not v] or x.get('error') for s, x in report['stages'].items()})
        u = report['stages']['S1']['units']; self.assertEqual((u['assigned'], u['completed'], u['primary_estimate'], u['every_unit_exactly_once']), (576, 576, -0.5, True))
        directory = Path(self.status['stages']['S1']['directory']); path = directory / 'episodes.jsonl.gz'; original = path.read_bytes()
        rows = study.read_rows(directory)
        victim = next(i for i, r in enumerate(rows) if r['answer']['value'] is not None)
        try:
            rows[victim]['answer']['value'] += 1
            with gzip.open(path, 'wt') as f:
                for r in rows: f.write(json.dumps(r, sort_keys=True) + '\n')
            code, report = run_verify(); self.assertEqual(code, 1)
            self.assertFalse(report['stages']['S1']['checks']['rows_regraded']); self.assertFalse(report['stages']['S1']['checks']['artifact_checksums'])
        finally:
            path.write_bytes(original)
        events = directory / 'events.jsonl.gz'; saved = events.read_bytes()
        try:
            with gzip.open(events, 'rt') as f: lines = f.read().splitlines()
            with gzip.open(events, 'wt') as f: f.write('\n'.join(lines[:10] + lines[11:]) + '\n')
            code, report = run_verify(); self.assertEqual(code, 1); self.assertFalse(report['stages']['S1']['checks']['journal_intact'])
        finally:
            events.write_bytes(saved)
        self.assertEqual(run_verify()[0], 0)

    def test_status_prints_one_json_line_and_resume_is_refused_after_a_completed_chain(self):
        for fn, code in ((chain.show_status, 0), (lambda: chain.resume(self.hub, opener=self.stub), 3)):
            out = io.StringIO()
            with patch('sys.stdout', out): self.assertEqual(fn(), code)
            lines = out.getvalue().strip().splitlines(); self.assertEqual(len(lines), 1); data = json.loads(lines[-1])
        self.assertEqual(data, {'state': 'resume_refused', 'reason': 'last_stop_was_not_a_billing_stop_of_S1'})

    def test_a_batch_is_never_queued_twice(self):
        for s in study.STAGES:
            with self.assertRaises(coordinator.GateRefused) as cm: coordinator.enqueue(self.hub, s)
            self.assertEqual(str(cm.exception), 'batch_exists_no_replay')

    def test_saved_analysis_reports_cells_guard_forgetting_and_retrieval(self):
        a = json.loads((Path(self.status['stages']['S1']['directory']) / 'analysis.json').read_text())
        self.assertEqual((a['roots'], a['assigned'], a['observed'], len(a['cells'])), (24, 576, 576, 24))
        self.assertEqual((a['primary']['estimate'], a['primary']['roots'], a['primary']['negative'], a['primary']['interval95']), (-0.5, 24, 24, [-0.5, -0.5]))
        self.assertEqual(len(a['primary']['root_values']), 24)
        self.assertEqual({p: a['utility_guard']['by_policy'][p]['correct'] for p in sim.POLICIES}, {'raw': 24, 'metadata': 24, 'content': 24, 'reset': 0})
        self.assertEqual(a['forgetting']['raw_minus_reset']['estimate'], 1.0)
        self.assertEqual(a['separate_states']['false_original']['content']['supported_wrong'], 1.0)
        self.assertEqual(a['separate_states']['contradiction']['raw']['abstain'], 1.0)
        r = a['retrieval']; self.assertEqual((r['raw']['bytes'], r['reset']['registry_lookups'], r['metadata']['records_retrieved']), (0, 0, 0))
        self.assertGreater(r['content']['records_retrieved'], r['content']['registry_lookups'] - 1); self.assertGreater(r['content']['bytes'], r['metadata']['bytes'])
        self.assertEqual(a['distinct_packets'], manifest.load()['stages']['S1']['distinct_packets'])


class Gates(unittest.TestCase):
    def test_coordinator_gates(self):
        hub = FakeHub()
        for s in ('P0', 'Q0', 'S1'):
            with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, s)
        self.assertEqual(len(coordinator.enqueue(hub, 'S0')), 1); self.assertEqual(hub.registered, study.EXPERIMENT)
        with self.assertRaises(coordinator.GateRefused) as cm: coordinator.enqueue(hub, 'P0')
        self.assertEqual(str(cm.exception), 'queue_not_empty')
        cases = (dict(status='failed'), dict(invalid=1), dict(passed=0), dict(source_hash='f' * 64))
        for bad in cases:
            hub = FakeHub(); hub.add('S0', **bad)
            with self.assertRaises(coordinator.GateRefused) as cm: coordinator.enqueue(hub, 'P0')
            self.assertEqual(str(cm.exception), 'exact_runtime_qualification_required:S0')
        hub = FakeHub(); hub.add('S0'); hub.add('S0', batch='s0-other')          # two runs of the previous stage: not exactly one
        with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, 'P0')
        hub = FakeHub(); hub.add('S0'); hub.add('P0'); hub.add('Q0')
        self.assertEqual(len(coordinator.enqueue(hub, 'S1')), 1)
        with self.assertRaises(coordinator.GateRefused) as cm: coordinator.check(FakeHubWith(hub, 'S1'), 'S1')
        self.assertEqual(str(cm.exception), 'batch_exists_no_replay')

    def test_continuation_gate(self):
        hub = FakeHub(); hub.add('S0'); hub.add('P0'); hub.add('Q0')
        with self.assertRaises(coordinator.GateRefused) as cm: coordinator.enqueue_continuation(hub, 1)
        self.assertEqual(str(cm.exception), 'stopped_main_stage_required')
        hub.add('S1', status='done', passed=None)
        with self.assertRaises(coordinator.GateRefused): coordinator.enqueue_continuation(hub, 1)          # S1 finished: nothing to continue
        hub.rows[-1]['status'] = 'failed'
        ids = coordinator.enqueue_continuation(hub, 1); row = next(r for r in hub.rows if r['run'] == ids[0])
        self.assertEqual((row['params']['batch'], row['params']['continuation'], row['params']['stage']), ('s1-001-r1', 1, 'S1'))
        hub.queue.clear(); row['status'] = 'failed'
        with self.assertRaises(coordinator.GateRefused) as cm: coordinator.enqueue_continuation(hub, 1)
        self.assertEqual(str(cm.exception), 'batch_exists_no_replay')
        self.assertEqual(len(coordinator.enqueue_continuation(hub, 2)), 1)

    def test_chain_stops_at_a_failed_gate_and_queues_nothing_further(self):
        with Env():
            hub = FakeHub(); out = io.StringIO(); clock = Clock()
            with patch('sys.stdout', out): code = chain.run_chain(list(study.STAGES), sr=hub, opener=rehearse.Stub('trust_memory'), clock=clock.now, sleep=clock.sleep)
            status = chain.read_status()
            self.assertEqual((code, status['state'], status['stopped_stage'], status['reason']), (3, 'stopped_at_gate', 'Q0', 'qualification_failed'))
            self.assertEqual([(r['params']['stage'], r['status']) for r in hub.rows], [('S0', 'done'), ('P0', 'done'), ('Q0', 'failed')])
            self.assertNotIn('S1', status['stages']); self.assertEqual(hub.queue, [])
            self.assertEqual(json.loads(out.getvalue().strip().splitlines()[-1]), {'state': 'stopped_at_gate', 'stage': 'Q0', 'reason': 'qualification_failed'})
            with patch('sys.stdout', io.StringIO()): self.assertEqual(chain.run_chain(['S1'], sr=hub, opener=rehearse.Stub('reference')), 3)
            self.assertEqual(chain.read_status()['reason'], 'exact_runtime_qualification_required:Q0')

    def test_projection_gates_stop_before_the_main_stage(self):
        for metrics, want in (({'cost_per_call_usd': 0.01}, 'projection_exceeds_cap'), ({'tokens_per_byte_max': 2.0}, 'input_ceiling_projection'),
                              ({'cost_per_call_usd': None}, 'qualification_usage_missing')):
            with Env():
                hub = FakeHub(); hub.add('S0'); hub.add('P0'); hub.add('Q0', **metrics)
                with patch('sys.stdout', io.StringIO()): code = chain.run_chain(['S1'], sr=hub, opener=rehearse.Stub('reference'))
                status = chain.read_status()
                self.assertEqual((code, status['reason'], status['stages']['S1']['status']), (3, want, 'refused')); self.assertEqual(hub.queue, [])
                self.assertFalse(any(r['params']['stage'] == 'S1' for r in hub.rows))
        hub = FakeHub(); hub.add('Q0')
        with Env():
            p = chain.projection(hub.rows[0])
            self.assertAlmostEqual(p['projected_usd'], 576 * 0.00005); self.assertEqual(p['largest_s1_request_bytes'], study.largest_request_bytes('S1'))
            self.assertAlmostEqual(p['projected_max_input_tokens'], 0.34 * study.largest_request_bytes('S1'))

    def test_stage_lists_must_be_ordered_and_contiguous(self):
        self.assertEqual(chain.parse_stages('S0'), ['S0']); self.assertEqual(chain.parse_stages('p0,q0,s1'), ['P0', 'Q0', 'S1'])
        for bad in ('S1,S0', 'S0,Q0', 'S2', '', 'S0,S0'):
            with self.assertRaises(SystemExit): chain.parse_stages(bad)

    def test_verify_fails_without_a_chain_and_status_of_another_source_version_is_set_aside(self):
        with Env() as env:
            out = io.StringIO()
            with patch('sys.stdout', out): self.assertEqual(chain.verify(FakeHub()), 1)
            self.assertEqual(len(out.getvalue().strip().splitlines()), 1)
            chain.write_status({'source_hash': 'old' * 4, 'stages': {}, 'state': 'completed'})
            hub = FakeHub()
            with patch('sys.stdout', io.StringIO()): chain.run_chain(['S0'], sr=hub)
            self.assertEqual(chain.read_status()['source_hash'], study.source_hash())
            self.assertTrue((env.path / 'results' / 'chain-status-oldoldoldold.json').exists())

    def test_rehearsal_refuses_a_hub_that_is_not_local_and_the_stub_rejects_a_changed_body(self):
        self.assertEqual(rehearse.require_local('http://127.0.0.1:8791'), 'http://127.0.0.1:8791')
        for url in ('http://10.0.0.5', 'https://hub.example.org', 'http://localhost:8700', 'http://127.0.0.1.example.org:1', '', None):
            with self.assertRaises(SystemExit): rehearse.require_local(url)
        body = study.request_body(study.assignments('P0')[0]['packet'])
        request = lambda b, url=provider.URL: type('R', (), {'full_url': url, 'data': json.dumps(b).encode(), 'header_items': lambda self: [('Authorization', 'Bearer x')]})()
        self.assertEqual(json.loads(rehearse.Stub('reference')(request(body)).read())['choices'][0]['finish_reason'], 'stop')
        for extra in ({'temperature': 0}, {'models': ['x']}, {'reasoning': {'enabled': True}}, {'max_tokens': 2000}):
            with self.assertRaises(urllib.error.HTTPError): rehearse.Stub('reference')(request(dict(body, **extra)))
        with self.assertRaises(AssertionError): rehearse.Stub('reference')(request(body, 'https://example.org/v1/chat/completions'))


class FakeHubWith:
    """A view of a hub whose queue is empty (the queued run counted as finished), for the replay check."""
    def __init__(self, hub, stage): self.rows = [dict(r, status='done') for r in hub.rows]
    def runs(self, experiment=None, status=None, limit=200): return [copy.deepcopy(r) for r in self.rows]


class Analysis(unittest.TestCase):
    def test_primary_contrast_definition_and_signs(self):
        table = C['expected']
        ref = analyze.analyze(synthetic(lambda root, s, p: table[s][p]))
        self.assertEqual((ref['primary']['estimate'], ref['primary']['bounds_all_assigned'], ref['primary']['roots']), (-0.5, [-0.5, -0.5], 24))
        self.assertEqual(ref['primary']['by_state']['misquote']['estimate'], -1.0); self.assertEqual(ref['primary']['by_state']['stale']['estimate'], 0.0)
        keep = analyze.analyze(synthetic(lambda root, s, p: 'F' if s in ('misquote', 'stale') and p in ('content', 'metadata') else table[s][p]))
        self.assertEqual(keep['primary']['estimate'], 0.0)
        half = analyze.analyze(synthetic(lambda root, s, p: 'F' if (s, p) == ('stale', 'metadata') and root % 2 else table[s][p]))
        self.assertEqual(half['primary']['estimate'], -0.75); self.assertEqual((half['primary']['negative'], half['primary']['positive']), (24, 0))
        lo, hi = half['primary']['interval95']; self.assertTrue(-1.0 <= lo < -0.75 < hi <= -0.5)
        self.assertEqual(half['primary']['interval95'], analyze.analyze(synthetic(lambda root, s, p: 'F' if (s, p) == ('stale', 'metadata') and root % 2 else table[s][p]))['primary']['interval95'])
        worse = analyze.analyze(synthetic(lambda root, s, p: 'N' if (s, p) == ('clean', 'content') and root < 5407 else table[s][p]))
        g = worse['utility_guard']; self.assertEqual((g['by_policy']['content']['correct'], g['content_minus_raw']['estimate']), (18, -0.25))
        self.assertLess(g['by_policy']['content']['wilson95'][0], 0.75); self.assertGreater(g['by_policy']['content']['wilson95'][1], 0.75)

    def test_missing_outcomes_are_bounded_not_dropped(self):
        table = C['expected']; missing = {(5401, 'misquote', 'content'), (5402, 'stale', 'metadata'), (5403, 'clean', 'content')}
        a = analyze.analyze(synthetic(lambda root, s, p: table[s][p], missing=missing))
        p = a['primary']; self.assertEqual((p['roots'], p['assigned_roots'], p['estimate']), (22, 24, -0.5)); self.assertIsNone(p['interval95'])
        by_root = {r['root']: r for r in p['root_values']}
        self.assertEqual((by_root[5401]['value'], by_root[5401]['lower'], by_root[5401]['upper']), (None, -0.5, 0.0))
        self.assertEqual((by_root[5402]['lower'], by_root[5402]['upper']), (-1.0, -0.5))
        self.assertAlmostEqual(p['bounds_all_assigned'][0], (-0.5 * 23 - 1.0) / 24); self.assertAlmostEqual(p['bounds_all_assigned'][1], (-0.5 * 23 + 0.0) / 24)
        cell = next(c for c in a['cells'] if (c['state'], c['policy']) == ('clean', 'content'))
        self.assertEqual((cell['assigned'], cell['observed'], cell['not_started'], cell['correct'], cell['correct_bounds']), (24, 23, 1, 23, [23 / 24, 1.0]))
        self.assertEqual(a['utility_guard']['by_policy']['content']['bounds_all_assigned'], [23 / 24, 1.0])
        self.assertEqual((a['assigned'], a['observed'], a['not_started']), (576, 573, 3))
        self.assertEqual(analyze.analyze([r for r in synthetic(lambda *k: 'N') if False]), {'cells': [], 'note': 'this stage has no comparison rows'})

    def test_combine_never_counts_a_unit_twice(self):
        rows = synthetic(lambda root, s, p: C['expected'][s][p], roots={5401})
        first = [dict(r, status='not_started') if i % 2 else r for i, r in enumerate(rows)]
        for r in first:
            if r['status'] == 'not_started': r.pop('answer', None)
        final = study.combine(first + [r for i, r in enumerate(rows) if i % 2] + rows[:3])
        self.assertEqual([r['id'] for r in final], [r['id'] for r in rows]); self.assertEqual({r['status'] for r in final}, {'completed'})

    def test_frames_replay_and_page_render_for_empty_partial_failed_and_final_states(self):
        assigned = study.assignments('S1'); rows = synthetic(lambda root, s, p: C['expected'][s][p])
        for i, r in enumerate(rows): r.update(completion_index=i + 1, elapsed_seconds=i * 0.5, packet_summary=study.packet_summary(assigned[i]), reference=sim.reference(assigned[i]['packet']), study_accounting={})
        rows[3].update(status='failed', error='http_500'); rows[3].pop('evaluation'); rows[4]['status'] = 'not_started'
        self.assertEqual(render.frame([], assigned, 'S1').size, (render.W, render.H))
        partial = render.frame(rows[:50], assigned, 'S1', elapsed=12.0, accounting={'attempted_calls': 50, 'actual_usd': 0.002})
        final = render.frame(rows, assigned, 'S1', headline=['primary: -0.500'])
        self.assertNotEqual(partial.tobytes(), final.tobytes())
        blue = final.getpixel((232 + 8 + 4, 128 + 10 + 4))                         # first square of clean x raw
        self.assertIn(blue, (render.COLORS['correct'], (255, 255, 255), render.BG))
        with tempfile.TemporaryDirectory() as td:
            n = render.replay(rows, assigned, Path(td), 'S1'); self.assertGreaterEqual(n, 10)
            from PIL import Image
            gif = Image.open(Path(td) / 'replay.gif'); self.assertEqual(gif.n_frames, n)
            units = worker.replay_units(assigned[:12], rows[:12])
            units[0]['answer'] = {'value': 1, 'sources': ['<script>alert(1)</script>']}
            journal.replay_html(units, Path(td) / 'replay.html', False)
            html = (Path(td) / 'replay.html').read_text(); self.assertNotIn('<script>alert', html); self.assertIn('Recorded model answers.', html)

    def test_journal_detects_tampering(self):
        j = journal.Journal(); j.emit('call_start', call_id='a'); j.emit('call_response', call_id='a'); j.emit('terminal', id='x', status='completed')
        lines = [json.dumps(e, sort_keys=True) for e in j.events]
        self.assertEqual(len(journal.read_events(lines)), 3); self.assertTrue(journal.call_ledger_complete(j.events))
        changed = json.loads(lines[1]); changed['call_id'] = 'b'
        with self.assertRaises(ValueError): journal.read_events([lines[0], json.dumps(changed), lines[2]])
        with self.assertRaises(ValueError): journal.read_events([lines[0], lines[2]])
        self.assertFalse(journal.call_ledger_complete(j.events[:1]))


TOTAL = {'tests': 0}


def load_tests(loader, tests, pattern):
    suite = unittest.TestSuite()
    for case in (Instrument, Adapter, Worker, Chain, Gates, Analysis):
        suite.addTests(loader.loadTestsFromTestCase(case))
    suite.addTests(loader.loadTestsFromModule(reference_tests))      # the reference adapter's own tests, against this study's copy
    TOTAL['tests'] = suite.countTestCases()
    return suite


if __name__ == '__main__':
    unittest.main()
