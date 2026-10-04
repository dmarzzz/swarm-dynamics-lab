"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the standard
unittest summary ("Ran N tests ... OK") on stderr. The reference adapter's own tests
(test_provider.py) run as part of this suite. S1's 1,440 packets are not rebuilt here (about 2.5
minutes); `python3 src/manifest.py --check` and S1's own pre-dispatch invariants cover them."""
import ast
import gzip
import hashlib
import io
import json
import math
import os
import sys
import tempfile
import threading
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The suite is independent of the launched model: the launcher's setup runs it with STUDY_MODEL and
# STUDY_PROVIDER set. Tests exercise the first model unless they pin another one explicitly.
for _name in ('STUDY_MODEL', 'STUDY_PROVIDER'):
    os.environ.pop(_name, None)

import analyze      # noqa: E402
import chain        # noqa: E402
import coordinator  # noqa: E402
import manifest     # noqa: E402
import provider     # noqa: E402
import rehearse     # noqa: E402
import render       # noqa: E402
import study        # noqa: E402
import worker       # noqa: E402
from test_provider import Request, Answers, Transport, Billing, LedgerRules  # noqa: E402,F401  (the adapter's own tests)
import openai_provider  # noqa: E402
import test_openai_provider as _toa  # noqa: E402
# the OpenAI reference adapter's own tests, under distinct names
OpenAIRequest, OpenAICost, OpenAIAnswers, OpenAITransport = _toa.Request, _toa.Cost, _toa.Answers, _toa.Transport
OpenAIBilling, OpenAIStubServer, OpenAILedgerRules = _toa.Billing, _toa.StubServer, _toa.LedgerRules

D = study.design(); B = study.budget(); SPEC = study.spec(); PD = study.parent_design()
KEY = 'sk-or-test-SECRET-0123456789'
REFERENCE = Path(__file__).resolve().parents[2] / 'pipeline' / 'reference'
_cache = {}
QWEN_FROZEN = 'ff8c2ad3d250e2117636e88d5438c946c23945155c51f94f086372cc06cbdd4f'


def scripted_rows(stage):
    if stage not in _cache:
        rows = []
        for a in study.assignments(stage):
            r = worker.row_base(a, {'stage': stage, 'batch': 't', 'backend': 'scripted', 'code': 't', 'source_hash': 't', 'model': 't'}, 't')
            answer = study.scripted(a['packet'])
            r.update(answer=answer, accounting={'attempted': False}, evaluation=study.evaluate(a, answer),
                     reference_evaluation=study.evaluate(a, answer), status='completed')
            rows.append(r)
        _cache[stage] = rows
    return _cache[stage]


def pilot_slice(n=24):
    """Stand-in S1 units for worker tests: the first n attacked engineering assignments of S0."""
    return [a for a in study.assignments('S0') if a['kind'] == 'pilot'][:n]


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def reply(content, tokens=24000):
    return Resp(json.dumps({'id': 'g', 'model': SPEC['canonical_model'], 'provider': 'Alibaba',
                            'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': content}}],
                            'usage': {'prompt_tokens': tokens, 'completion_tokens': 40}}).encode())


class Model:
    """Opener for worker tests: answers by the reference policy except for scripted faults.
    faults: {n: fault} for the n-th request (1-based); 'invalid' returns a wrong shape, an int is an
    HTTP status. credit_first: that many billing errors first."""
    def __init__(self, faults=None, credit_first=0, credit_forever=False, shape=None):
        self.faults = faults or {}; self.n = 0; self.lock = threading.Lock(); self.credit_first = credit_first
        self.credit_forever = credit_forever; self.shape = shape
    def __call__(self, request, timeout=None):
        with self.lock:
            if self.credit_forever or self.credit_first > 0:
                self.credit_first -= 1
                raise urllib.error.HTTPError(provider.URL, 402, 'x', {}, io.BytesIO(b'{"error":{"message":"Insufficient credits"}}'))
            self.n += 1; fault = self.faults.get(self.n)
        body = json.loads(request.data)
        if isinstance(fault, int):
            raise urllib.error.HTTPError(provider.URL, fault, 'x', {'x-request-id': 'req-9'}, io.BytesIO(b'{"error":{"message":"upstream said no"}}'))
        answer = study.scripted(json.loads(body['messages'][1]['content']))
        content = '{"values": [1, 2]}' if fault == 'invalid' else (self.shape or json.dumps)(answer)
        return reply(content)


class FakeRun:
    def __init__(self, run_id, params): self.id, self.params, self.attempt = run_id, params, 1; self.final = None; self.uploads = []
    def __enter__(self): return self
    def __exit__(self, et, ev, tb):
        if self.final is None: self.final = ('fail', {}) if et else ('done', {})
        return False
    def progress(self, *a, **k): return True
    def artifact(self, path, name=None): self.uploads.append(name or Path(path).name); return {'name': name}
    def done(self, message=None, **metrics): self.final = ('done', metrics); self.message = message
    def fail(self, message=None, **metrics): self.final = ('fail', metrics); self.message = message


class FakeHub:
    def __init__(self): self.rows = []; self.queue = []; self.n = 0; self.experiments = set()
    def runs(self, experiment=None, status=None, limit=200):
        self.experiments.add(experiment); return [dict(r) for r in self.rows]
    def register(self, experiment, **kw): self.registered = (experiment, kw)
    def enqueue(self, experiment, params_list, tags=None):
        ids = []
        for p in params_list:
            self.n += 1; rid = f'{experiment}/{self.n:08d}'; ids.append(rid)
            self.rows.append({'run': rid, 'status': 'planned', 'params': p, 'metrics': {}}); self.queue.append(rid)
        return ids
    def next_run(self, experiment=None):
        if not self.queue: return None
        rid = self.queue.pop(0); row = next(r for r in self.rows if r['run'] == rid); row['status'] = 'running'
        run = FakeRun(rid, row['params']); self.live = (run, row); return run
    def settle(self):
        run, row = self.live; row['status'] = 'done' if run.final[0] == 'done' else 'failed'; row['metrics'] = run.final[1]
    def add(self, stage, status='done', invalid=0, passed=1, source_hash=None, batch=None, **metrics):
        p = study.params(stage); p['source_hash'] = source_hash or p['source_hash']; p['batch'] = batch or p['batch']
        self.rows.append({'run': f'x/{stage}{len(self.rows)}', 'status': status, 'params': p,
                          'metrics': dict({'invalid': invalid, 'qualification_passed': passed, 'model_calls': 48, 'cost_usd': 0.035,
                                           'max_tokens_per_byte': 0.45}, **metrics)})


def paid_env(td):
    return patch.dict(os.environ, {provider.LEDGER_ENV: str(Path(td) / 'ledger.jsonl'), provider.KEY_ENV: KEY})


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# ----------------------------------------------------------------------------- parent identity
class ParentIdentity(unittest.TestCase):
    def test_parent_files_are_the_pinned_ones_and_sim_is_a_byte_copy(self):
        pin = D['parent']; p = study.parent_dir()
        self.assertEqual(sha(p / 'design.yaml'), pin['design_sha256']); self.assertEqual(sha(p / 'src' / 'sim.py'), pin['sim_sha256'])
        self.assertEqual(sha(p / 'src' / 'study.py'), pin['study_sha256']); self.assertEqual(sha(p / 'manifest.json'), pin['manifest_sha256'])
        self.assertEqual(sha(p / 'records' / 's1-episodes.jsonl.gz'), pin['s1_episodes_sha256'])
        self.assertEqual(sha(Path(__file__).resolve().parent / 'sim.py'), pin['sim_sha256'])

    def test_probe_and_qualification_packets_equal_the_parents_code_and_manifest(self):
        for stage in ('P0', 'Q0'):
            self.assertEqual(study.parent_equivalence(stage), [], stage)

    def test_a_changed_packet_is_detected(self):
        rows = study.assignments('P0'); rows[0]['packet']['reports'][0]['claim'] += 1
        rows[0]['packet_hash'] = study.digest(rows[0]['packet'])
        with patch.object(study, 'assignments', return_value=rows):
            bad = study.parent_equivalence('P0')
        self.assertIn('P0:manifest_lines_differ_from_parent', bad); self.assertTrue(any('packet_text_differs' in b for b in bad))

    def test_cells_roots_and_counts_are_the_parents(self):
        counts = {s: study.design()['stages'][s]['assignments'] for s in study.STAGES}
        self.assertEqual(counts, {s: PD['stages'][s]['assignments'] for s in study.STAGES})
        self.assertEqual(B['max_calls'], PD['budget']['max_calls']); self.assertEqual(B['max_attempted_calls'], 1489)
        self.assertEqual((PD['worlds'][0], PD['worlds'][-1], len(PD['worlds'])), (7800, 7823, 24))
        m = manifest.load()
        self.assertEqual({s: m['stages'][s]['assignments'] for s in study.STAGES}, counts)
        self.assertLessEqual(max(m['stages'][s]['max_request_bytes'] for s in study.STAGES), B['max_input_bytes'])


# ----------------------------------------------------------------------------- request and answers
class RequestAndAnswers(unittest.TestCase):
    def test_system_prompt_is_the_parents_plus_the_answer_shape(self):
        tree = ast.parse((study.parent_dir() / 'src' / 'provider.py').read_text())
        parent = next(n.value.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', '') == 'SYSTEM')
        self.assertEqual(study.PARENT_SYSTEM, parent)
        self.assertTrue(study.SYSTEM.startswith(parent + '\n')); self.assertIn('JSON', study.SYSTEM)
        shape = json.loads(study.SHAPE.splitlines()[1].replace('<integer or null>', 'null'))
        self.assertEqual(shape, {'values': {str(s): None for s in range(6)}})

    def test_request_body_is_the_frozen_template_plus_messages(self):
        tree = json.loads((Path(__file__).resolve().parents[2] / 'overnight-program-2026-10-04' / 'selected-model.json').read_text())
        self.assertEqual(SPEC['request_template'], tree['request_template'])
        with patch.dict(os.environ, {provider.KEY_ENV: KEY}): api = provider.OpenRouter(None, study.adapter_config())
        a = study.assignments('P0')[0]
        body = api.body(study.SYSTEM, study.user_text(a['packet']))
        self.assertEqual(len(json.dumps(body).encode()), a['request_bytes'])
        self.assertEqual(body['messages'][1]['content'], study.actor_text(a['packet']))
        self.assertEqual(sha(Path(__file__).resolve().parent / 'provider.py'), sha(REFERENCE / 'openrouter_provider.py'))

    def test_validate_accepts_harmless_variants_of_a_correct_answer(self):
        exact = {'values': {'0': 31, '1': 44, '2': 25, '3': 29, '4': 53, '5': None}}
        variants = [exact,
                    {'values': {'5': None, '4': 53, '3': 29, '2': 25, '1': 44, '0': 31}},                    # key order
                    {'values': dict(exact['values'], **{'3': 29.0})},                                      # integral number
                    {'values': dict(exact['values'], **{'3': '29', '4': ' 53 '})},                         # integer text
                    dict(exact, note='plurality of passed reports')]                                       # extra top-level key
        for v in variants:
            out = study.validate(v)
            self.assertEqual(out['values'], exact['values'], v); self.assertEqual(study.validate(out), out)    # idempotent
        self.assertNotIn('normalized', study.validate(exact))
        self.assertEqual(study.validate(variants[3])['normalized'], ['integer_text:3', 'integer_text:4'])
        for bad in ({'values': dict(exact['values'], **{'3': True})}, {'values': dict(exact['values'], **{'3': 29.5})},
                    {'values': dict(exact['values'], **{'3': 'twenty-nine'})}, {'values': dict(exact['values'], **{'6': 1})},
                    {'values': {k: v for k, v in exact['values'].items() if k != '5'}}, {'values': dict(exact['values'], **{'3': {'value': 29}})},
                    {'answer': exact['values']}, [exact], {'values': [31, 44]}):
            with self.assertRaises(ValueError): study.validate(bad)

    def test_harmless_variants_pass_the_adapter_end_to_end(self):
        """Lesson from the flagship's stopped probe: a correct answer written slightly differently
        must not become a failed call. Each variant goes through the real adapter and the validator."""
        a = study.assignments('P0')[0]; truth = study.scripted(a['packet'])['values']
        texts = [json.dumps({'values': truth}), json.dumps({'values': truth}, indent=2), '\n ' + json.dumps({'values': truth}) + '\n',
                 json.dumps({'values': {k: (str(v) if v is not None else None) for k, v in truth.items()}}),
                 json.dumps({'values': {k: (float(v) if v is not None else None) for k, v in truth.items()}}),
                 json.dumps({'reasoning': 'counted reports', 'values': truth})]
        for text in texts:
            with tempfile.TemporaryDirectory() as td, paid_env(td):
                api = provider.OpenRouter(provider.Ledger(Path(td) / 'l.jsonl', B), study.adapter_config(), opener=lambda r, timeout=None: reply(text))
                answer, acct = api.call(study.SYSTEM, study.user_text(a['packet']), 'p0-001-qwen:' + a['id'], study.validate)
            self.assertTrue(study.evaluate(a, answer)['exact_packet'], text)
        # Pinned limitation of the unchanged reference adapter: text around the JSON object is invalid_json.
        with tempfile.TemporaryDirectory() as td, paid_env(td):
            api = provider.OpenRouter(provider.Ledger(Path(td) / 'l.jsonl', B), study.adapter_config(),
                                      opener=lambda r, timeout=None: reply('```json\n' + json.dumps({'values': truth}) + '\n```'))
            with self.assertRaises(provider.CallFailure) as ctx:
                api.call(study.SYSTEM, study.user_text(a['packet']), 'p0-001-qwen:' + a['id'], study.validate)
        self.assertEqual(ctx.exception.category, 'invalid_json')

    def test_grading_breakdown(self):
        a = next(x for x in study.assignments('S0') if x['kind'] == 'pilot'); ans = a['answers']
        def g(v): return study.evaluate(a, {'values': {str(s): v(s) for s in range(6)}})
        right, lie, null, other = g(lambda s: ans[s]), g(lambda s: ans[s] + 7 if s in study.RARE else ans[s]), g(lambda s: None), g(lambda s: ans[s] + 1)
        self.assertEqual((right['rare_accuracy'], right['rare_wrong'], right['rare_fabricated']), (1, 0, 0))
        self.assertEqual((lie['rare_accuracy'], lie['rare_fabricated'], lie['rare_other_wrong'], lie['rare_wrong']), (0, 1, 0, 1))
        self.assertEqual((null['rare_null'], null['rare_wrong'], null['rare_accuracy']), (1, 0, 0))
        self.assertEqual((other['rare_other_wrong'], other['rare_fabricated']), (1, 0))
        for e in (right, lie, null, other):
            self.assertAlmostEqual(e['rare_accuracy'] + e['rare_fabricated'] + e['rare_other_wrong'] + e['rare_null'], 1)
        q = next(x for x in study.assignments('Q0'))
        self.assertEqual(study.evaluate(q, {'values': {str(s): q['answers'][s] + 7 for s in range(6)}})['rare_fabricated'], 0)   # no attacker in clean packets


class Gate(unittest.TestCase):
    def rows(self, edit=None):
        rows = [dict(r, evaluation=dict(r['evaluation'])) for r in scripted_rows('Q0')]
        if edit: edit(rows)
        return rows

    def wrong(self, r):
        a = next(x for x in study.assignments('Q0') if x['id'] == r['id'])
        vals = dict(study.scripted(a['packet'])['values']); k = next(k for k, v in vals.items() if v is not None); vals[k] += 1
        r['evaluation'] = study.evaluate(a, {'values': vals})

    def test_the_parents_thresholds(self):
        self.assertTrue(study.qualification(self.rows())['passed'])
        by = lambda rows, c: [r for r in rows if r['carriers'] == c]
        self.assertTrue(study.qualification(self.rows(lambda rows: self.wrong(by(rows, 1)[0])))['passed'])            # 15/16 exact >= 0.90
        self.assertFalse(study.qualification(self.rows(lambda rows: [self.wrong(r) for r in by(rows, 9)[:2]]))['passed'])  # 14/16 < 0.90
        def invent(rows):
            r = next(r for r in rows if r['withheld'] is not None); r['evaluation']['missing_correct'] = 0
        self.assertFalse(study.qualification(self.rows(invent))['passed'])
        def invalid(rows): rows[0]['status'] = 'failed'
        self.assertFalse(study.qualification(self.rows(invalid))['passed'])
        self.assertFalse(study.qualification(self.rows()[:47])['passed'])
        self.assertEqual(PD['qualification']['fact_accuracy'], 0.95); self.assertEqual(PD['qualification']['exact_packet_rate'], 0.9)


class Models(unittest.TestCase):
    def test_each_model_has_its_own_batches_hub_experiment_ledger_and_results(self):
        self.assertEqual(D['model_ladder'], ['qwen/qwen3.7-flash', 'gpt-6-sol'])
        with patch.dict(os.environ, {'STUDY_MODEL': 'qwen/qwen3.7-flash', 'STUDY_RESULTS_DIR': '/r'}):
            self.assertEqual([study.batch(s) for s in study.STAGES], ['s0-001-qwen', 'p0-001-qwen', 'q0-001-qwen', 's1-001-qwen'])
            self.assertEqual((study.hub_experiment(), study.params('P0')['model'], study.params('P0')['backend'], study.params('S0')['backend']),
                             ('sybil-scarcity-xmodel-qwen', 'qwen/qwen3.7-flash', 'openrouter', 'scripted'))
            self.assertEqual((study.ledger_path('/l/ledger.jsonl'), str(study.results_dir())), ('/l/ledger-qwen.jsonl', '/r/qwen'))
        os.environ.pop('STUDY_MODEL', None); self.assertEqual(study.model(), 'qwen/qwen3.7-flash')
        with patch.dict(os.environ, {'STUDY_MODEL': 'claude-opus-5-5'}), self.assertRaises(ValueError) as ctx: study.model()
        self.assertEqual(str(ctx.exception), 'model_not_in_ladder')
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_RESULTS_DIR': '/r'}):
            self.assertEqual([study.batch(s) for s in study.STAGES], ['s0-001-solnone', 'p0-001-solnone', 'q0-001-solnone', 's1-001-solnone'])
            self.assertEqual((study.hub_experiment(), study.params('P0')['backend'], study.route(), study.ledger_path('/l/ledger.jsonl'), str(study.results_dir())),
                             ('sybil-scarcity-xmodel-solnone', 'openai', openai_provider, '/l/ledger-solnone.jsonl', '/r/solnone'))

    def test_qwen_configuration_is_unchanged_from_the_first_code_commit(self):
        # the Qwen chain launched at code commit 2753b03d; its request, caps and prices must not move
        s = D['models']['qwen/qwen3.7-flash']
        self.assertEqual(study.digest([s, D['budget'], D['parent'], D['primary_contrast'], D['analysis']]), QWEN_FROZEN)

    def test_gpt6_sol_configuration_passes_the_reference_adapter_and_its_arithmetic(self):
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol'}):
            c = study.adapter_config(); b = c['budget']
            self.assertIs(openai_provider.check_config(c), c)
            self.assertEqual(c['request_template'], {'model': 'gpt-6-sol', 'reasoning_effort': 'none', 'max_completion_tokens': 2000,
                                                     'response_format': {'type': 'json_object'}})
            self.assertEqual(dict(b['prices']), openai_provider.PRICES['gpt-6-sol']); self.assertEqual((b['aggregate_usd'], b['workers']), (150, 2))
            self.assertEqual(b['retry']['retryable_http_status'], [429, 500, 502, 503, 504])
            p = b['prices']; largest = manifest.load()['stages']['S1']['max_request_bytes'] + 200        # sol body is a few bytes longer
            reserve = (largest * max(p['input'], p['cache_write']) + b['max_output_tokens'] * p['output']) * b['reservation_margin'] / 1e6
            self.assertLess(reserve, 0.35)                                                               # about USD 0.33 per call
            self.assertLess(reserve * (b['workers'] + b['max_failed']), 0.05 * b['aggregate_usd'])      # open + unsettled failed calls
            expected_high = b['max_attempted_calls'] * (24000 * p['cache_write'] + 600 * p['output']) / 1e6
            self.assertLess(expected_high, b['aggregate_usd'])                                          # USD 98 at the cache-write bound
            self.assertLessEqual(largest * 0.7, b['max_input_tokens'])
            with patch.dict(os.environ, {openai_provider.KEY_ENV: 'sk-proj-test'}):
                api = study.make_backend(None, c)
                a = study.assignments('P0')[0]; body = api.body(study.SYSTEM, study.user_text(a['packet']))
            self.assertEqual(list(body), list(openai_provider.BODY_KEYS)); self.assertEqual(body['messages'][1]['content'], study.actor_text(a['packet']))
            self.assertIn('json', study.SYSTEM.lower())
        self.assertEqual(sha(Path(__file__).resolve().parent / 'openai_provider.py'), sha(REFERENCE / 'openai_provider.py'))

    def test_budget_arithmetic(self):
        self.assertEqual(B['max_failed'], max(3, math.ceil(0.01 * B['max_calls']['S1'])))
        self.assertEqual(sum(B['max_calls'].values()), B['max_attempted_calls'])
        reserve = (B['max_input_bytes'] * B['input_usd_per_million'] + B['max_output_tokens'] * B['output_usd_per_million']) * B['reservation_margin'] / 1e6
        self.assertLess(reserve * (B['workers'] + B['max_failed']), B['aggregate_usd'] / 10)       # open plus unsettled failed calls
        expected = B['max_attempted_calls'] * (25000 * B['input_usd_per_million'] + 60 * B['output_usd_per_million']) / 1e6
        self.assertLess(expected * 3, B['aggregate_usd'])
        self.assertLess(B['max_input_tokens'], 32000)


# ----------------------------------------------------------------------------- worker
class WorkerRules(unittest.TestCase):
    def run_s1(self, model, n=24, clock=None, expect_fail=None, units=None, prior=None, params=None, ledger_dir=None, config=None):
        run = FakeRun('x/s1', params or study.params('S1'))
        with tempfile.TemporaryDirectory() as td, paid_env(ledger_dir or td), patch.object(study, 'assignments', return_value=pilot_slice(n)), \
                patch.object(study, 'adapter_config', return_value=config or study.adapter_config()), \
                patch.object(study, 'check_invariants', return_value=[]), patch.object(render, 'replay', lambda *a, **k: 0):
            kw = dict(clock=clock.now, sleep=clock.sleep) if clock else {}
            try:
                worker.execute(run.params, Path(td) / 'out', run, opener=model, units=units, prior_rows=prior, **kw); failed = None
            except worker.StageFailed as exc: failed = str(exc)
            self.assertEqual(failed, expect_fail)
            summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
            rows = [json.loads(line) for line in (Path(td) / 'out' / 'episodes.jsonl').read_text().splitlines()]
            analysis = json.loads((Path(td) / 'out' / 'analysis.json').read_text())
            leaked = any(KEY in p.read_text(errors='ignore') for p in Path(td).rglob('*') if p.is_file() and p.suffix != '.gz')
            ledgers = sorted(p.name for p in Path(ledger_dir or td).glob('ledger*'))
        return run, summary, rows, analysis, leaked, ledgers

    def test_failed_calls_do_not_strand_s1_keep_their_evidence_and_stay_in_the_denominator(self):
        run, summary, rows, analysis, leaked, ledgers = self.run_s1(Model({5: 500, 9: 'invalid'}))
        self.assertEqual((summary['failed'], summary['invalid'], summary['graded'], summary['not_started'], summary['passed'], summary['stop_reason']), (2, 2, 22, 0, True, None))
        failed = {r['error']: r for r in rows if r['status'] == 'failed'}; self.assertEqual(set(failed), {'http_500', 'invalid_answer'})
        acct = failed['http_500']['accounting']; self.assertEqual((acct['http_status'], acct['request_id']), (500, 'req-9')); self.assertIn('upstream said no', acct['error_body'])
        self.assertIn('answer_text', failed['invalid_answer']['accounting']); self.assertFalse(leaked); self.assertEqual(ledgers, ['ledger-qwen.jsonl'])
        self.assertTrue(all(r['model'] == 'qwen/qwen3.7-flash' for r in rows))
        kind, metrics = run.final; self.assertEqual(kind, 'done'); self.assertEqual((metrics['episodes'], metrics['invalid'], metrics['failed'], metrics['model_calls']), (24, 2, 2, 24))
        for key in worker.HUB_KEYS: self.assertIn(key, metrics)
        self.assertEqual((analysis['denominators']['assigned'], analysis['denominators']['failed']), (24, 2))
        self.assertTrue(all(c['rare_accuracy_bounds_all_assigned'][0] <= c['rare_accuracy_bounds_all_assigned'][1] for c in analysis['cells']))

    def test_normalized_answers_are_recorded(self):
        def as_text(answer): return json.dumps({'values': {k: (str(v) if v is not None else None) for k, v in answer['values'].items()}})
        run, summary, rows, analysis, leaked, _ = self.run_s1(Model(shape=as_text), n=6)
        self.assertEqual((summary['graded'], summary['normalized_answers']), (6, 6)); self.assertTrue(all(r['answer']['normalized'] for r in rows))

    def test_more_failures_than_the_limit_stop_dispatch(self):
        run, summary, rows, analysis, leaked, _ = self.run_s1(Model({i: 'invalid' for i in range(1, 30)}), n=60, expect_fail='failed_units_over_limit')
        self.assertGreater(summary['failed'], B['max_failed']); self.assertLessEqual(summary['failed'], B['max_failed'] + B['workers'])
        self.assertGreater(summary['not_started'], 30); self.assertEqual(len({r['id'] for r in rows}), 60)
        self.assertEqual((run.final[0], summary['resumable'], run.final[1]['failed']), ('fail', 0, summary['failed']))

    def test_integrity_failure_stops_dispatch_at_once(self):
        class Wrong(Model):
            def __call__(self, request, timeout=None):
                data = json.loads(super().__call__(request).read()); data['model'] = 'some/other-model'; return Resp(json.dumps(data).encode())
        run, summary, rows, analysis, leaked, _ = self.run_s1(Wrong(), expect_fail='integrity_failure:model_mismatch')
        self.assertLessEqual(summary['failed'], B['workers']); self.assertGreaterEqual(summary['not_started'], 24 - B['workers']); self.assertEqual(run.final[0], 'fail')

    def test_billing_outage_then_recovery_is_one_pause_and_no_failed_row(self):
        clock = rehearse.FakeClock()
        run, summary, rows, analysis, leaked, _ = self.run_s1(Model(credit_first=3), clock=clock)
        self.assertEqual((summary['failed'], summary['graded'], summary['billing_pauses'], summary['passed']), (0, 24, 1, True))
        self.assertGreaterEqual(summary['billing_pause_seconds'], 60)

    def test_billing_outage_beyond_the_limit_stops_resumable_and_the_continuation_completes(self):
        clock = rehearse.FakeClock()
        class Dry(Model):
            def __call__(self, request, timeout=None):
                with self.lock:
                    if self.n >= 10: self.credit_forever = True
                return super().__call__(request, timeout)
        config = study.adapter_config(); config = dict(config, budget=dict(config['budget'], max_calls=dict(config['budget']['max_calls'], S1=24), max_attempted_calls=24))
        with tempfile.TemporaryDirectory() as shared:
            run, summary, rows, analysis, leaked, _ = self.run_s1(Dry(), clock=clock, expect_fail=provider.BILLING_STOP, ledger_dir=shared, config=config)
            self.assertEqual((summary['failed'], summary['resumable'], summary['stop_reason'], summary['model_calls']), (0, 1, provider.BILLING_STOP, 10))
            units = [r['id'] for r in rows if r['status'] == 'not_started']; self.assertEqual(len(units), 14)
            p = dict(study.params('S1'), batch='s1-001-qwen-r1', continuation=1)
            run2, summary2, rows2, analysis2, _, _ = self.run_s1(Model(), units=units, prior=rows, params=p, ledger_dir=shared, config=config)
            self.assertEqual((summary2['planned'], summary2['graded'], summary2['passed'], summary2['model_calls']), (14, 14, True, 14))
            end = provider.Ledger(Path(shared) / 'ledger-qwen.jsonl', config['budget']).transact()
            self.assertEqual((end['calls_by_batch']['s1-001-qwen'], end['attempted_calls'], end['usage_reported_calls']), (24, 24, 24))
        whole = worker.merge(rows, rows2); self.assertEqual(len(whole), 24); self.assertTrue(all(r['status'] == 'completed' for r in whole))
        with self.assertRaises(AssertionError): worker.merge(whole, rows2)

    def test_probe_reports_raw_metadata_and_qualification_uses_its_own_48_rows(self):
        run = FakeRun('x/p0', study.params('P0'))
        with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(render, 'replay', lambda *a, **k: 0):
            worker.execute(run.params, Path(td) / 'out', run, opener=Model())
            summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
        probe = summary['probe']; size = study.assignments('P0')[0]['request_bytes']
        self.assertEqual((probe['response_model'], probe['response_provider'], probe['finish_reason'], probe['exact'], probe['input_tokens']),
                         (SPEC['canonical_model'], 'Alibaba', 'stop', True, 24000))
        self.assertAlmostEqual(probe['tokens_per_byte'], 24000 / size)
        kind, metrics = run.final; self.assertEqual((kind, metrics['qualification_passed'], metrics['fixture_exact']), ('done', 1, 1))
        self.assertIn('provider=Alibaba', run.message)
        for opener, want in ((Model(), 'done'), (Model({3: 'invalid'}), 'fail')):
            run = FakeRun('x/q0', study.params('Q0'))
            with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(render, 'replay', lambda *a, **k: 0):
                try: worker.execute(run.params, Path(td) / 'out', run, opener=opener)
                except worker.StageFailed: pass
                summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
            self.assertEqual(run.final[0], want)
            if want == 'done': self.assertEqual((summary['qualification']['structurally_valid'], run.final[1]['model_calls']), (48, 48))

    def test_gpt6_sol_stage_runs_through_the_openai_adapter_and_a_billing_stop_is_resumable(self):
        clock = rehearse.FakeClock()
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol', openai_provider.KEY_ENV: KEY}):
            config = study.adapter_config()
            config = dict(config, budget=dict(config['budget'], max_calls=dict(config['budget']['max_calls'], S1=24), max_attempted_calls=24))
            stub = rehearse.Stub('reference', credit_after=10)
            with tempfile.TemporaryDirectory() as shared:
                run, summary, rows, analysis, leaked, ledgers = self.run_s1(stub, clock=clock, expect_fail='provider_billing_stopped', ledger_dir=shared, config=config)
                self.assertEqual((summary['failed'], summary['resumable'], summary['model_calls'], ledgers), (0, 1, 10, ['ledger-solnone.jsonl']))
                self.assertTrue(all(r['model'] == 'gpt-6-sol' for r in rows)); self.assertFalse(leaked)
                done = [r for r in rows if r['status'] == 'completed']
                self.assertTrue(all(r['accounting']['reasoning_tokens'] == 0 and r['accounting']['cost_source'] == 'computed_from_pinned_prices' for r in done))
                stub.restore(); units = [r['id'] for r in rows if r['status'] == 'not_started']
                p = dict(study.params('S1'), batch='s1-001-solnone-r1', continuation=1)
                run2, summary2, rows2, _, _, _ = self.run_s1(stub, units=units, prior=rows, params=p, ledger_dir=shared, config=config)
                self.assertEqual((summary2['graded'], summary2['passed']), (14, True))
                end = openai_provider.Ledger(Path(shared) / 'ledger-solnone.jsonl', config['budget']).transact()
                self.assertEqual((end['calls_by_batch']['s1-001-solnone'], end['usage_reported_calls']), (24, 24))
        hub = FakeHub()
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td, 'STUDY_MODEL': 'gpt-6-sol'}):
            chain.write_status({'source_hash': study.source_hash(), 'state': 'stopped_at_gate', 'stopped_stage': 'S1',
                                'reason': 'provider_billing_stopped', 'stages': {'S1': {'batch': 's1-001-solnone'}}})
            out = io.StringIO()
            with patch('sys.stdout', out): code = chain.resume(sr=hub)
        self.assertNotEqual(json.loads(out.getvalue().strip().splitlines()[-1]).get('reason'), 'last_stop_was_not_a_billing_stop_of_S1')

    def test_structural_violation_blocks_every_call(self):
        run = FakeRun('x/s1', study.params('S1')); model = Model()
        with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(study, 'assignments', return_value=pilot_slice(8)), \
                patch.object(study, 'check_invariants', return_value=['S1:manifest_lines_differ_from_parent']), patch.object(render, 'replay', lambda *a, **k: 0):
            with self.assertRaises(worker.StageFailed) as ctx: worker.execute(run.params, Path(td) / 'out', run, opener=model)
        self.assertEqual((str(ctx.exception), model.n, run.final[1]['model_calls']), ('invariant_violations', 0, 0))

    def test_stale_source_hash(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AssertionError): worker.execute(dict(study.params('S1'), source_hash='stale'), Path(td) / 'out')


# ----------------------------------------------------------------------------- gates and chain
class Gates(unittest.TestCase):
    def test_coordinator_gates_use_the_models_hub_experiment(self):
        hub = FakeHub()
        for stage in ('P0', 'Q0', 'S1'):
            with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, stage)
        hub.add('S0'); coordinator.enqueue(hub, 'P0')
        self.assertEqual(hub.registered[0], 'sybil-scarcity-xmodel-qwen'); self.assertIn('[qwen/qwen3.7-flash]', hub.registered[1]['title'])
        self.assertEqual(hub.experiments, {'sybil-scarcity-xmodel-qwen'})
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'P0')
        self.assertEqual(str(ctx.exception), 'batch_exists_no_replay')
        for kwargs in ({'status': 'failed'}, {'invalid': 1}, {'passed': 0}, {'source_hash': 'other'}):
            hub = FakeHub(); hub.add('P0', **kwargs)
            with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'Q0')
            self.assertEqual(str(ctx.exception), 'exact_runtime_qualification_required')

    def chain_with(self, outcomes, stages=('S0', 'P0', 'Q0', 'S1'), metrics=None):
        hub = FakeHub(); executed = []; metrics = metrics or {}
        def fake_execute(p, out, run=None, backend=None, deadline=None, opener=None, earlier_rows=(), units=None, prior_rows=None, clock=None, sleep=None):
            executed.append(p['stage']); out = Path(out); out.mkdir(parents=True)
            ok = outcomes.get(p['stage'], 'done') == 'done'
            m = {'episodes': 1, 'invalid': 0, 'failed': 0, 'model_calls': 48, 'transport_attempts': 48, 'input_tokens': 1150000, 'output_tokens': 2000,
                 'cost_usd': 0.035, 'qualification_passed': int(ok), 'max_tokens_per_byte': 0.45, 'fixture_exact': 1, 'billing_pauses': 0,
                 'billing_pause_seconds': 0, 'billing_affected_calls': 0, 'resumable': 0}
            m.update(metrics.get(p['stage'], {}))
            (out / 'summary.json').write_text(json.dumps(dict(m, planned=1, graded=1, not_started=0, errors=[], stop_reason=None)))
            (run.done if ok else run.fail)('x', **m); hub.settle()
            if not ok: raise worker.StageFailed(outcomes[p['stage']])
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td}), patch.object(worker, 'execute', fake_execute), \
                patch('sys.stdout', io.StringIO()):
            os.environ.pop(provider.LEDGER_ENV, None)
            code = chain.run_chain(list(stages), sr=hub); status = chain.read_status()
            resume = None
            if outcomes.get('resume'):
                out = io.StringIO()
                with patch('sys.stdout', out): resume = (chain.resume(sr=hub), json.loads(out.getvalue().strip().splitlines()[-1]))
            where = chain.status_path()
        return code, status, executed, hub, resume, where

    def test_chain_runs_all_stages_and_writes_status(self):
        code, status, executed, hub, _, where = self.chain_with({})
        self.assertEqual((code, status['state'], executed, status['all_stages_done'], status['model']), (0, 'completed', ['S0', 'P0', 'Q0', 'S1'], True, 'qwen/qwen3.7-flash'))
        self.assertEqual(where.parent.name, 'qwen')
        self.assertTrue(status['stages']['S1']['projection']['within_cap']); self.assertTrue(status['stages']['Q0']['input_ceiling']['within_ceiling'])

    def test_ledger_totals_read_the_models_own_ledger(self):
        with tempfile.TemporaryDirectory() as td, paid_env(td):
            self.assertIsNone(chain.ledger_totals())
            provider.Ledger(study.ledger_path(os.environ[provider.LEDGER_ENV]), B).transact({'type': 'reserve', 'call_id': 'p0-001-qwen:x', 'micro_usd': 5})
            self.assertFalse(Path(os.environ[provider.LEDGER_ENV]).exists())
            self.assertEqual(chain.ledger_totals()['attempted_calls'], 1)

    def test_chain_stops_at_a_failed_qualification_and_queues_nothing_further(self):
        code, status, executed, hub, _, _ = self.chain_with({'Q0': 'gate_failed'})
        self.assertEqual((code, status['state'], status['stopped_stage'], status['reason'], executed), (3, 'stopped_at_gate', 'Q0', 'gate_failed', ['S0', 'P0', 'Q0']))
        self.assertEqual([r['params']['stage'] for r in hub.rows], ['S0', 'P0', 'Q0'])

    def test_input_ceiling_projection_stops_before_q0_and_before_s1(self):
        largest = manifest.load()['stages']['Q0']['max_request_bytes']; tpb = (B['max_input_tokens'] + 100) / largest
        code, status, executed, hub, _, _ = self.chain_with({}, metrics={'P0': {'max_tokens_per_byte': tpb}})
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed), (3, 'Q0', 'input_ceiling_projection', ['S0', 'P0']))
        code, status, executed, hub, _, _ = self.chain_with({}, metrics={'Q0': {'max_tokens_per_byte': tpb}})
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed), (3, 'S1', 'input_ceiling_projection', ['S0', 'P0', 'Q0']))

    def test_cost_projection_stops_before_s1(self):
        code, status, executed, hub, _, _ = self.chain_with({}, metrics={'Q0': {'cost_usd': 0.15}})       # 1440 x 0.15/48 = 4.5 > 4
        self.assertEqual((code, status['stopped_stage'], status['reason']), (3, 'S1', 'projection_exceeds_cap'))

    def test_resume_is_refused_unless_the_last_stop_was_a_billing_stop_of_s1(self):
        _, _, _, _, resume, _ = self.chain_with({'Q0': 'gate_failed', 'resume': True})
        self.assertEqual(resume, (3, {'state': 'resume_refused', 'reason': 'last_stop_was_not_a_billing_stop_of_S1'}))

    def test_rehearsal_refuses_a_hub_that_is_not_local(self):
        with self.assertRaises(SystemExit): rehearse.require_local('http://10.0.0.5:8080')
        self.assertEqual(rehearse.require_local('http://127.0.0.1:9'), 'http://127.0.0.1:9')


# ----------------------------------------------------------------------------- analysis and frames
class Analysis(unittest.TestCase):
    def rows(self):
        out = []
        for i, task in enumerate((7800, 7801, 7802)):
            for c in (1, 81):
                acc = 1.0 if c == 81 else (0.0 if i < 2 else 1 / 3)
                out.append({'kind': 'pilot', 'task': task, 'arm': 'random', 'checks': 108, 'attacker_pass': 0.1, 'carriers': c, 'id': f'{task}-{c}',
                            'packet_hash': 'h', 'status': 'completed', 'model': 'm', 'diagnostics': {k: 0.5 for k in analyze.DIAGNOSTICS},
                            'evaluation': {f: 0.0 for f in analyze.OUTCOMES} | {'rare_accuracy': acc},
                            'reference_evaluation': {f: 0.0 for f in analyze.OUTCOMES}})
        return out

    def test_primary_arithmetic_and_missing_bounds(self):
        rows = self.rows(); p = analyze.analyze(rows)['primary']
        self.assertAlmostEqual(p['estimate_pp'], 100 * ((-1 - 1 - 2 / 3) / 3)); self.assertEqual((p['complete_roots'], p['assigned_roots']), (3, 3))
        rows[0]['status'] = 'failed'; p = analyze.analyze(rows)['primary']
        self.assertEqual((p['complete_roots'], p['assigned_roots']), (2, 3)); self.assertLess(p['bounds_pp'][0], p['estimate_pp']); self.assertLessEqual(p['estimate_pp'], p['bounds_pp'][1])

    def test_parent_rows_are_read_only_when_pinned(self):
        parent = analyze.parent_rows(); self.assertEqual(len(parent), 1440)
        self.assertTrue(all(r['status'] == 'completed' for r in parent.values()))
        with patch.dict(D['parent'], {'s1_episodes_sha256': '0' * 64}): self.assertIsNone(analyze.parent_rows())

    def test_frames_render_for_every_stage_and_without_fonts(self):
        rows = scripted_rows('S0'); q = scripted_rows('Q0')
        with tempfile.TemporaryDirectory() as td:
            for stage, rr in (('S0', []), ('S0', rows[:40]), ('S0', rows), ('Q0', q), ('P0', scripted_rows('P0'))):
                im = render.frame(rr, len(rows), stage); self.assertEqual(im.size, (1800, 1200))
            with patch.object(render, 'FONT_PATHS', ()):
                render.font.cache_clear(); render.frame(rows, len(rows), 'S0').save(Path(td) / 'x.png')
            render.font.cache_clear()
            self.assertGreater(render.replay(rows, Path(td), 'S0', len(rows)), 2)
            from PIL import Image
            with Image.open(Path(td) / 'replay.gif') as gif: self.assertGreater(gif.n_frames, 2)


class SourceHash(unittest.TestCase):
    def test_source_hash_covers_code_and_design_only(self):
        self.assertEqual(len(study.source_hash()), 64)
        with tempfile.TemporaryDirectory() as td:
            import shutil
            shutil.copytree(study.ROOT / 'src', Path(td) / 'src'); [shutil.copy(study.ROOT / f, Path(td) / f) for f in ('design.yaml', 'experiment.yaml', 'requirements.txt')]
            with patch.object(study, 'ROOT', Path(td)):
                before = study.source_hash(); (Path(td) / 'README.md').write_text('x'); self.assertEqual(study.source_hash(), before)
                (Path(td) / 'src' / 'render.py').write_text('# changed'); self.assertNotEqual(study.source_hash(), before)


if __name__ == '__main__':
    unittest.main()
