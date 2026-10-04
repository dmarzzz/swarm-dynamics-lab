"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the standard
unittest summary ("Ran N tests ... OK") on stderr. The reference adapter's own tests
(test_provider.py) run as part of this suite."""
import copy
import hashlib
import importlib.util
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
import manifest     # noqa: E402
import provider     # noqa: E402
import rehearse     # noqa: E402
import render       # noqa: E402
import sim          # noqa: E402
import study        # noqa: E402
import worker       # noqa: E402
from test_provider import Request, Answers, Transport, Billing, LedgerRules  # noqa: E402,F401  (the adapter's 28 tests)

FROZEN = {'world_4481': '079b32e669f71bb78927dfbde4142d59f11211ef6c9a0049ad1a254f7e1fb6bc',
          'audit_4481': '20268380ea35369b5c49192714657a6593c2617d488fd80dbc9c06329743bd91',
          'admitted_4481': '10eef2c47925c1650572ae877d9a6db9b648635098062daa4bc337355a99d95a',
          'request_template': '9cbd8bc28ae39aafc5dd86a1627bfd54677052367b4b2aa5811dbb1dae558dbe',
          'reference_adapter': '86d0739e9bf83fcb12c382b5d1844ed7011b56a2bb77baebdcf7ad275b58d789',
          'instruction': 'bddb189fed7f59bd89880a81e46f531a7664919114ca3aed8f14319d666caf04'}
D = study.design(); CFG = study.cfg(); B = D['budget']
ENG = D['roots']['engineering']; KEY = 'sk-or-test-SECRET-0123456789'
_cache = {}


def scripted_rows(stage):
    if stage not in _cache:
        rows = []
        for a in study.assignments(stage):
            r = worker.row_base(a, {'stage': stage, 'batch': 't', 'backend': 'scripted', 'code': 't', 'source_hash': 't'}, 't')
            answer = study.scripted(a['packet'])
            r.update(answer=answer, accounting={'attempted': False}, evaluation=study.evaluate(a, answer),
                     reference_evaluation=study.evaluate(a, answer), status='completed')
            rows.append(r)
        _cache[stage] = rows
    return _cache[stage]


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


class Model:
    """Opener for worker tests: answers by the reference policy except for scripted faults.
    faults: {n: fault} for the n-th request (1-based); 'invalid' returns a wrong shape, an int is an
    HTTP status, 'credit' is a billing error. credit_first: that many billing errors first."""
    def __init__(self, faults=None, credit_first=0, credit_forever=False):
        self.faults = faults or {}; self.n = 0; self.lock = threading.Lock(); self.credit_first = credit_first; self.credit_forever = credit_forever
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
        content = '{"values": [1, 2]}' if fault == 'invalid' else json.dumps(answer)
        return Resp(json.dumps({'id': 'g', 'model': D['canonical_model'], 'provider': 'Alibaba',
                                'choices': [{'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': content}}],
                                'usage': {'prompt_tokens': 2600, 'completion_tokens': 40}}).encode())


class FakeRun:
    def __init__(self, run_id, params): self.id, self.params, self.attempt = run_id, params, 1; self.final = None; self.uploads = []
    def __enter__(self): return self
    def __exit__(self, et, ev, tb):
        if self.final is None: self.final = ('fail', {}) if et else ('done', {})
        return False
    def progress(self, *a, **k): return True
    def artifact(self, path, name=None): self.uploads.append(name or Path(path).name); return {'name': name}
    def done(self, message=None, **metrics): self.final = ('done', metrics)
    def fail(self, message=None, **metrics): self.final = ('fail', metrics)


class FakeHub:
    def __init__(self): self.rows = []; self.queue = []; self.n = 0
    def runs(self, experiment=None, status=None, limit=200): return [dict(r) for r in self.rows]
    def register(self, experiment, **kw): self.registered = experiment
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
                          'metrics': dict({'invalid': invalid, 'qualification_passed': passed, 'model_calls': 23, 'cost_usd': 0.002,
                                           'max_tokens_per_byte': 0.45}, **metrics)})


def paid_env(td):
    return patch.dict(os.environ, {provider.LEDGER_ENV: str(Path(td) / 'ledger.jsonl'), provider.KEY_ENV: KEY})


def s1_slice(n=24):
    return study.assignments('S1')[:n]


class Instrument(unittest.TestCase):
    def test_world_audit_and_admission_are_frozen(self):
        w = study.world(ENG[0], 0.1)
        self.assertEqual(study.digest({'public': w['public'], 'checks': w['checks'], 'answers': w['answers']}), FROZEN['world_4481'])
        r = study.replay(ENG[0], 0.1)
        self.assertEqual(study.digest(r['events']), FROZEN['audit_4481'])
        self.assertEqual(study.digest({f'{k[0]}:{k[1]}': v for k, v in r['admitted'].items()}), FROZEN['admitted_4481'])

    def test_world_coverage_audit_and_historical_ranking_equal_the_parent_instrument(self):
        path = study.ROOT.parent / 'sybil-budget-api/src/sim.py'
        if not path.exists(): self.skipTest('parent study not present; frozen digests cover the same code')
        spec = importlib.util.spec_from_file_location('parentsim', path); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
        for rate in D['attacker_pass']:
            a = old.make_world(ENG[1], 9, rate, False, CFG); b = sim.make_world(ENG[1], 9, rate, False, CFG)
            for key in ('public', 'checks', 'answers', 'groups'): self.assertEqual(a[key], b[key])
            self.assertTrue(all(a['truth'][x]['honest'] == b['truth'][x]['honest'] and (not a['truth'][x]['honest']) == b['truth'][x]['controlled'] for x in a['truth']))
            recs = old.checkpoints(a, D['check_budgets'], ['coverage'], CFG); events = sim.audit(b, 108)
            self.assertEqual(recs[-1]['events'], events)
            for rec in recs:
                snap = sim.snapshot(b, events[:rec['checks']], CFG)
                self.assertEqual(sim.historical_rank(b['public'], snap['passed'], snap['failed'], CFG)[0][:162], rec['admitted'])

    def test_propagated_rule_is_the_historical_ranking_when_no_identity_is_dangling(self):
        audit = study.historical_audit('engineering'); clean = [x for x in audit if x['dangling'] == 0]
        self.assertGreater(len(clean), 30); self.assertTrue(all(x['same_admitted_set'] for x in clean))
        self.assertEqual((len(audit), sum(x['dangling'] > 0 for x in audit), sum(x['same_admitted_set'] for x in audit)), (48, 12, 42))
        self.assertLessEqual(max(abs(x['attacker_seats_historical'] - x['attacker_seats_propagated']) for x in audit), 1)
        # the mixture is the PageRank seeded uniformly on anchors and passed identities, on the common matrix
        r = study.replay(ENG[0], 0.1); w = r['world']; snap = r['snapshots'][108]; anchors = sorted(w['public']['trusted'])
        neighbors = {x: [y for y in w['public']['adj'][x] if y not in snap['failed']] for x in snap['active']}
        seeds = anchors + snap['passed']
        joint = sim.pagerank(seeds, snap['active'], neighbors, anchors, CFG)
        self.assertLess(max(abs(joint[x] - snap['scores']['propagated'][x]) for x in snap['active']), 1e-12)

    def test_structural_invariants_hold_on_engineering_roots(self):
        for task in ENG[:3]: self.assertEqual(study.check_root(task), [])

    def test_rules_differ_only_in_where_pass_credit_goes(self):
        for rate in D['attacker_pass']:
            r = study.replay(ENG[2], rate)
            for budget in D['check_budgets']:
                s = r['snapshots'][budget]; sc = s['scores']; a = s['alpha']
                self.assertEqual(a, len(s['passed']) / (2 + len(s['passed'])))
                for rule in D['rules']: self.assertAlmostEqual(sum(sc[rule].values()), 1.0, 9)
                extra = {x: sc['direct'][x] - (1 - a) * sc['anchors'][x] for x in s['active']}
                self.assertEqual({x for x, v in extra.items() if v != 0}, set(s['passed']))
                self.assertTrue(all(abs(extra[x] - a / len(s['passed'])) < 1e-15 for x in s['passed']))
                self.assertAlmostEqual(sum(sc['propagated'][x] - (1 - a) * sc['anchors'][x] for x in s['active']), a, 9)
                self.assertEqual(len({len(r['admitted'][(rule, budget)]) for rule in D['rules']}), 1)
        empty = sim.snapshot(study.world(ENG[2], 0.1), [], CFG)
        self.assertEqual(empty['scores']['propagated'], empty['scores']['anchors']); self.assertEqual(empty['scores']['direct'], empty['scores']['anchors'])

    def test_audit_is_generated_once_and_does_not_depend_on_a_rule(self):
        import inspect
        self.assertEqual(list(inspect.signature(sim.audit).parameters), ['world', 'budget'])
        self.assertEqual(list(inspect.signature(sim.select_coverage).parameters), ['public', 'passed', 'checked', 'task', 'step'])
        r = study.replay(ENG[3], 0.1); w = r['world']
        self.assertEqual(sim.audit(w, 32), r['events'][:32]); self.assertEqual(sim.audit(w, 64), r['events'][:64])
        low, high = study.replay(ENG[3], 0.1)['world']['checks'], study.replay(ENG[3], 0.9)['world']['checks']
        self.assertTrue(all(high[x] or not low[x] for x in low))            # outcomes coupled across strengths

    def test_invariant_checker_detects_a_broken_replay(self):
        real = study.replay.__wrapped__
        def tampered(task, rate, clean=False):
            r = real(task, rate, clean)
            if rate == 0.1 and not clean:
                r = dict(r, admitted=dict(r['admitted'])); adm = list(r['admitted'][('direct', 64)])
                r['admitted'][('direct', 64)] = adm[:-1] + [r['snapshots'][64]['failed'][0]]
            return r
        with patch.object(study, 'replay', tampered):
            bad = ' '.join(study.check_root(ENG[0]))
        self.assertIn('checks=64:direct_seats', bad); self.assertIn('direct_tie_break', bad)

    def test_clean_endpoint_keeps_graph_audit_and_admission_and_is_truthful(self):
        attacked = study.replay(ENG[4], 0.9); clean = study.replay(ENG[4], 0.9, True)
        self.assertEqual(clean['events'], attacked['events']); self.assertEqual(clean['admitted'], attacked['admitted'])
        cw = clean['world']; self.assertTrue(all(v['claim'] == cw['answers'][v['skill']] for v in cw['public']['nodes'].values()))
        self.assertEqual(sum(v['controlled'] for v in cw['truth'].values()), 81)
        rows = [a for a in study.assignments('S0') if a['kind'] == 'clean' and a['task'] == ENG[4]]
        self.assertEqual(len(rows), 3); self.assertTrue(all(a['admission']['truth_plurality'] == 1 and a['fabricated'] == [None] * 6 for a in rows))

    def test_packets_are_compact_blind_ordered_and_under_the_byte_limit(self):
        for stage in ('S0', 'P0', 'Q0'):
            for a in study.assignments(stage):
                pack = a['packet']; text = study.user_text(pack)
                self.assertEqual(list(pack), ['skills', 'columns', 'rows']); self.assertEqual(len(pack['rows']), 162)
                self.assertFalse(any(word in text for word in study.FORBIDDEN))
                self.assertTrue(all(len(r) == 6 and r[5] in 'TPU' for r in pack['rows']))
                keys = [study.order_key(a['task'], r[0]) for r in pack['rows']]; self.assertEqual(keys, sorted(keys))
                self.assertLessEqual(a['request_bytes'], B['max_input_bytes']); self.assertLess(B['max_input_bytes'], B['max_input_tokens'])
                self.assertEqual(a['request_bytes'], len(json.dumps({**D['request_template'], 'messages': [
                    {'role': 'system', 'content': study.SYSTEM}, {'role': 'user', 'content': text}]}).encode()))
        leaky = {'skills': [0], 'columns': study.COLUMNS, 'rows': [['n01', 0, 1, 1, 1, 'honest']]}
        self.assertIn('packet_leaks_evaluator_field', study.check_packet(study.world(ENG[0], 0.1), leaky, ['n01'], []))

    def test_instruction_states_the_answer_shape_and_reveals_nothing(self):
        self.assertEqual(hashlib.sha256(study.SYSTEM.encode()).hexdigest(), FROZEN['instruction'])
        self.assertIn('{"values":{"0":<integer or null>', study.SYSTEM); self.assertIn('JSON', study.SYSTEM)
        for word in ('propagated', 'direct', 'anchors', 'PageRank', 'budget', 'truth', '+7', 'controller', 'seat'): self.assertNotIn(word, study.SYSTEM)

    def test_validate_is_strict(self):
        good = {'values': {str(i): None for i in range(6)}}; study.validate(good); study.validate({'values': {str(i): i for i in range(6)}})
        for bad in ({'values': {'0': 1}}, {'values': {str(i): True for i in range(6)}}, {'values': {str(i): 1.0 for i in range(6)}},
                    {'values': {str(i): '1' for i in range(6)}}, dict(good, note='x'), [1], {'values': [None] * 6},
                    {'values': {**{str(i): 1 for i in range(6)}, '6': 1}}, {'Values': good['values']}):
            with self.assertRaises(ValueError): study.validate(bad)

    def test_grading(self):
        a = next(x for x in study.assignments('S0') if x['kind'] == 'pilot')
        lie = {'values': {str(s): a['answers'][s] + 7 if s in sim.RARE else a['answers'][s] for s in range(6)}}
        e = study.evaluate(a, lie); self.assertEqual((e['rare_wrong'], e['rare_correct'], e['rare_fabricated'], e['rare_abstain']), (1, 0, 1, 0))
        e = study.evaluate(a, {'values': {str(s): None if s in sim.RARE else a['answers'][s] for s in range(6)}})
        self.assertEqual((e['rare_wrong'], e['rare_correct'], e['rare_abstain']), (0, 0, 1))
        e = study.evaluate(a, {'values': {str(s): a['answers'][s] for s in range(6)}}); self.assertEqual((e['rare_correct'], e['exact_packet']), (1, True))

    def test_fixtures(self):
        for which in ('a', 'b'):
            fs = study.fixtures(which); self.assertEqual(len(fs), 24); self.assertEqual(fs[0][2], 'full')
            for f in fs: self.assertEqual(study.check_fixture(*f), [])
            self.assertEqual(sorted({study.fixture(t, 'missing', p)[3] for _, t, s, p in fs if s == 'missing'}), [3, 4, 5])
        p0, q0 = study.assignments('P0'), study.assignments('Q0')
        self.assertEqual((len(p0), len(q0)), (1, 23)); self.assertEqual((p0[0]['task'], p0[0]['shape'], p0[0]['set']), (D['roots']['qualification'][0], 'full', 'a'))
        self.assertEqual(len({a['id'] for a in p0 + q0}), 24); self.assertTrue(all(a['set'] == 'a' for a in q0))
        self.assertEqual(sum(a['withheld'] is not None for a in p0 + q0), 8)

    def test_qualification_gate_thresholds(self):
        base = [r for r in scripted_rows('S0') if r['kind'] == 'qualification' and r['set'] == 'a']
        by_id = {a['id']: a for a in study.assignments('S0')}
        def regrade(row, answer): row.update(answer=answer, evaluation=study.evaluate(by_id[row['id']], answer))
        def wrong(row):
            ans = copy.deepcopy(row['answer']); ans['values']['0'] += 1; regrade(row, ans)
        rows = copy.deepcopy(base); self.assertTrue(study.qualification(rows, 'a')['passed'])
        full = [r for r in rows if r['shape'] == 'full']; wrong(full[0]); self.assertTrue(study.qualification(rows, 'a')['passed'])     # 7 of 8
        wrong(full[1]); self.assertFalse(study.qualification(rows, 'a')['passed'])                                                      # 6 of 8
        rows = copy.deepcopy(base); sparse = [r for r in rows if r['shape'] == 'sparse']; wrong(sparse[0]); wrong(sparse[1])
        self.assertFalse(study.qualification(rows, 'a')['passed'])
        rows = copy.deepcopy(base); m = next(r for r in rows if r['shape'] == 'missing')
        regrade(m, {'values': {k: (0 if v is None else v) for k, v in m['answer']['values'].items()}})
        self.assertFalse(study.qualification(rows, 'a')['passed'])                                                                      # 7 of 8 abstained
        rows = copy.deepcopy(base); rows[0]['status'] = 'failed'; self.assertFalse(study.qualification(rows, 'a')['passed'])            # invalid structure
        self.assertFalse(study.qualification(copy.deepcopy(base)[1:], 'a')['passed'])                                                   # 23 rows: the probe row is missing
        self.assertTrue(study.gate('Q0', base[1:], [], base[:1])); self.assertFalse(study.gate('Q0', base[1:], [], []))
        self.assertTrue(study.gate('P0', base[:1])); self.assertFalse(study.gate('P0', [dict(base[0], status='failed')])); self.assertIsNone(study.gate('S1', []))

    def test_stage_counts_caps_and_splits(self):
        self.assertEqual(B['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 504}); self.assertEqual(B['max_attempted_calls'], 528)
        self.assertEqual(24 * (3 * 3 * 2 + 3), 504); self.assertEqual(B['max_failed'], max(3, -(-504 // 100)))
        self.assertGreaterEqual(B['max_transport_attempts'], 528 + 40); self.assertEqual(B['aggregate_usd'], 2)
        groups = [set(D['roots'][k]) for k in ('engineering', 'qualification', 'qualification_b', 'comparison')]
        self.assertEqual([len(g) for g in groups], [8, 8, 8, 24]); self.assertTrue(all(not a & b for i, a in enumerate(groups) for b in groups[i + 1:]))
        self.assertLess(max(set.union(*groups)), 10000)
        with self.assertRaises(ValueError): study.params('S2')
        self.assertEqual((study.attempt(), study.batch('S1'), study.qualification_set()), ('001', 's1-001', 'a'))

    def test_request_template_and_adapter_are_the_frozen_references(self):
        self.assertEqual(study.digest(D['request_template']), FROZEN['request_template'])
        self.assertEqual(hashlib.sha256((study.ROOT / 'src' / 'provider.py').read_bytes()).hexdigest(), FROZEN['reference_adapter'])
        c = study.adapter_config(); self.assertEqual(set(c), {'model', 'canonical_model', 'provider', 'request_template', 'budget'})
        from test_provider import CONFIG
        self.assertEqual(c['request_template'], CONFIG['request_template']); self.assertLessEqual(set(CONFIG['budget']), set(c['budget']))
        for key in ('max_calls', 'max_attempted_calls', 'aggregate_usd', 'max_output_tokens', 'max_input_tokens', 'request_timeout_seconds', 'retry',
                    'billing_outage', 'max_transport_attempts', 'input_usd_per_million', 'output_usd_per_million'):
            self.assertEqual(c['budget'][key], CONFIG['budget'][key])
        with tempfile.TemporaryDirectory() as td, paid_env(td):
            sent = []
            def opener(request, timeout): sent.append(json.loads(request.data)); return Model()(request)
            api = provider.OpenRouter(provider.Ledger(Path(td) / 'l', c['budget']), c, opener)
            a = study.assignments('P0')[0]; answer, acct = api.call(study.SYSTEM, study.user_text(a['packet']), 'p0-001:x', study.validate)
            self.assertEqual(list(sent[0]), list(provider.BODY_KEYS)); self.assertEqual({k: v for k, v in sent[0].items() if k != 'messages'}, D['request_template'])
            self.assertEqual(acct['request_bytes'], a['request_bytes']); self.assertEqual(answer, study.scripted(a['packet']))
            self.assertLessEqual(acct['reserved_usd'], (B['max_input_bytes'] * 0.03 + 1000 * 0.13 + 1) / 1e6)

    def test_engineering_grid_reproduces_the_parent_direction_and_is_not_degenerate(self):
        rows = scripted_rows('S0'); self.assertEqual(len(rows), 216); self.assertEqual(study.degeneracy(rows), [])
        self.assertTrue(study.gate('S0', rows, [])); self.assertFalse(study.gate('S0', rows, ['x']))
        a = analyze.analyze(rows); self.assertAlmostEqual(a['primary']['estimate'], 23.375); self.assertEqual(a['primary']['positive_roots'], 8)
        cell = {(c['attacker_pass'], c['rule'], c['checks']): c for c in a['cells'] if c['kind'] == 'pilot'}
        self.assertEqual([cell[(0.1, 'propagated', b)]['admission']['attacker_seats'] for b in (32, 64, 108)], [2.25, 13.25, 15.5])
        self.assertEqual([cell[(0.1, 'direct', b)]['admission']['attacker_seats'] for b in (32, 64, 108)], [20.5, 17.875, 10.375])
        flat = copy.deepcopy(rows)
        for r in flat:
            if r['kind'] == 'pilot': r['admission']['attacker_seats'] = 0
        self.assertIn('propagated_rule_does_not_reproduce_parent_direction', study.degeneracy(flat)); self.assertIn('primary_constant_across_roots', study.degeneracy(flat))

    def test_manifest_regenerates_identically(self):
        fresh = manifest.build(); self.assertEqual(manifest.text(fresh), manifest.PATH.read_text())
        self.assertEqual({s: e['assignments'] for s, e in fresh['stages'].items()}, {'S0': 216, 'P0': 1, 'Q0': 23, 'S1': 504, 'qualification_b': 24})
        self.assertTrue(all(e['max_request_bytes'] <= B['max_input_bytes'] for e in fresh['stages'].values()))
        s1 = study.assignments('S1'); self.assertEqual(len({a['task'] for a in s1}), 24)
        self.assertEqual({k: sum(a['kind'] == k for a in s1) for k in ('pilot', 'clean')}, {'pilot': 432, 'clean': 72})

    def test_source_hash_covers_code_and_design_only(self):
        with patch.object(Path, 'read_bytes', lambda self: self.name.encode()):
            names = study.source_hash()
        expected = ['design.yaml', 'experiment.yaml', 'requirements.txt'] + sorted(p.name for p in (study.ROOT / 'src').glob('*.py'))
        self.assertEqual(names, study.digest([(n, hashlib.sha256(n.encode()).hexdigest()) for n in expected]))
        self.assertIn('provider.py', expected); self.assertIn('test_provider.py', expected); self.assertNotIn('manifest.json', expected)


class WorkerRules(unittest.TestCase):
    def run_s1(self, model, n=24, clock=None, expect_fail=None, units=None, prior=None, params=None):
        run = FakeRun('x/s1', params or study.params('S1'))
        with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(study, 'assignments', return_value=s1_slice(n)), \
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
        return run, summary, rows, analysis, leaked

    def test_one_failed_call_does_not_strand_s1_and_keeps_its_evidence(self):
        run, summary, rows, analysis, leaked = self.run_s1(Model({5: 500, 9: 'invalid'}))
        self.assertEqual((summary['failed'], summary['invalid'], summary['graded'], summary['not_started'], summary['passed'], summary['stop_reason']), (2, 2, 22, 0, True, None))
        failed = {r['error']: r for r in rows if r['status'] == 'failed'}; self.assertEqual(set(failed), {'http_500', 'invalid_answer'})
        acct = failed['http_500']['accounting']; self.assertEqual((acct['http_status'], acct['request_id']), (500, 'req-9')); self.assertIn('upstream said no', acct['error_body'])
        self.assertIn('answer_text', failed['invalid_answer']['accounting']); self.assertFalse(leaked)
        kind, metrics = run.final; self.assertEqual(kind, 'done'); self.assertEqual((metrics['episodes'], metrics['invalid'], metrics['failed'], metrics['model_calls']), (24, 2, 2, 24))
        for key in worker.HUB_KEYS: self.assertIn(key, metrics)
        self.assertEqual((analysis['denominators']['assigned'], analysis['denominators']['failed']), (24, 2))
        self.assertTrue(all(c['rare_correct_bounds_all_assigned'][0] <= c['rare_correct_bounds_all_assigned'][1] for c in analysis['cells']))

    def test_more_failures_than_the_limit_stop_dispatch(self):
        run, summary, rows, analysis, leaked = self.run_s1(Model({i: 'invalid' for i in range(1, 12)}), n=40, expect_fail='failed_units_over_limit')
        self.assertGreater(summary['failed'], B['max_failed']); self.assertLessEqual(summary['failed'], B['max_failed'] + B['workers'])
        self.assertGreater(summary['not_started'], 20); self.assertEqual(len({r['id'] for r in rows}), 40)
        self.assertEqual((run.final[0], summary['resumable'], run.final[1]['failed']), ('fail', 0, summary['failed']))

    def test_integrity_failure_stops_dispatch_at_once(self):
        class Wrong(Model):
            def __call__(self, request, timeout=None):
                data = json.loads(super().__call__(request).read()); data['model'] = 'some/other-model'; return Resp(json.dumps(data).encode())
        run, summary, rows, analysis, leaked = self.run_s1(Wrong(), expect_fail='integrity_failure:model_mismatch')
        self.assertLessEqual(summary['failed'], B['workers']); self.assertGreaterEqual(summary['not_started'], 24 - B['workers']); self.assertEqual(run.final[0], 'fail')

    def test_strict_stage_stops_at_the_first_failure_and_reports_metrics(self):
        run = FakeRun('x/q0', study.params('Q0')); probe = [r for r in scripted_rows('S0') if r['kind'] == 'qualification' and r['set'] == 'a' and r['id'] == study.assignments('P0')[0]['id']]
        with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(render, 'replay', lambda *a, **k: 0):
            with self.assertRaises(worker.StageFailed): worker.execute(run.params, Path(td) / 'out', run, opener=Model({1: 'invalid'}), earlier_rows=probe)
            summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
        self.assertEqual(summary['qualification_passed'], 0); self.assertGreaterEqual(summary['not_started'], 23 - B['workers'])
        kind, metrics = run.final; self.assertEqual(kind, 'fail'); self.assertEqual(metrics['episodes'], 23)

    def test_qualification_stage_passes_with_the_probe_row_and_fails_without_it(self):
        probe = [r for r in scripted_rows('S0') if r['id'] == study.assignments('P0')[0]['id']]
        for earlier, want in ((probe, 'done'), ([], 'fail')):
            run = FakeRun('x/q0', study.params('Q0'))
            with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(render, 'replay', lambda *a, **k: 0):
                try: worker.execute(run.params, Path(td) / 'out', run, opener=Model(), earlier_rows=earlier)
                except worker.StageFailed: pass
                summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
            self.assertEqual(run.final[0], want); self.assertEqual(summary['qualification']['fixtures'], 23 + len(earlier))
            self.assertEqual(run.final[1]['model_calls'], 23); self.assertAlmostEqual(run.final[1]['max_tokens_per_byte'], 2600 / min(a['request_bytes'] for a in study.assignments('Q0')), 6)

    def test_billing_outage_then_recovery_is_one_pause_and_no_failed_row(self):
        clock = rehearse.FakeClock()
        run, summary, rows, analysis, leaked = self.run_s1(Model(credit_first=3), clock=clock)
        self.assertEqual((summary['failed'], summary['graded'], summary['billing_pauses'], summary['passed']), (0, 24, 1, True))
        self.assertGreaterEqual(summary['billing_pause_seconds'], 60); self.assertGreaterEqual(summary['billing_affected_calls'], 1)
        self.assertEqual(run.final[1]['billing_pauses'], 1)

    def test_billing_outage_beyond_the_limit_stops_resumable_and_the_continuation_completes(self):
        clock = rehearse.FakeClock()
        class Dry(Model):
            def __call__(self, request, timeout=None):
                with self.lock:
                    if self.n >= 10: self.credit_forever = True
                return super().__call__(request, timeout)
        run, summary, rows, analysis, leaked = self.run_s1(Dry(), clock=clock, expect_fail=provider.BILLING_STOP)
        self.assertEqual((summary['failed'], summary['resumable'], summary['stop_reason']), (0, 1, provider.BILLING_STOP))
        self.assertEqual(sum(r['status'] == 'completed' for r in rows), 10); self.assertEqual(sum(r['status'] == 'not_started' for r in rows), 14)
        self.assertEqual((run.final[0], run.final[1]['resumable'], run.final[1]['failed']), ('fail', 1, 0))
        units = [r['id'] for r in rows if r['status'] == 'not_started']; carried = worker.carried_reservations(rows, set(units))
        self.assertGreaterEqual(carried, 1); self.assertLessEqual(carried, B['workers'])
        p = dict(study.params('S1'), batch='s1-001-r1', continuation=1)
        run2, summary2, rows2, analysis2, _ = self.run_s1(Model(), units=units, prior=rows, params=p)
        self.assertEqual((summary2['planned'], summary2['graded'], summary2['passed'], summary2['continuation']['carried_reservations']), (14, 14, True, carried))
        whole = worker.merge(rows, rows2); self.assertEqual(len(whole), 24); self.assertTrue(all(r['status'] == 'completed' for r in whole))
        self.assertEqual(analysis2['denominators']['completed'], 24)
        with self.assertRaises(AssertionError): worker.merge(whole, rows2)                                # a unit is never counted twice

    def test_structural_violation_blocks_every_call(self):
        run = FakeRun('x/s1', study.params('S1')); model = Model()
        with tempfile.TemporaryDirectory() as td, paid_env(td), patch.object(study, 'assignments', return_value=s1_slice(8)), \
                patch.object(study, 'check_invariants', return_value=['9541:x']), patch.object(render, 'replay', lambda *a, **k: 0):
            with self.assertRaises(worker.StageFailed) as ctx: worker.execute(run.params, Path(td) / 'out', run, opener=model)
        self.assertEqual((str(ctx.exception), model.n, run.final[1]['model_calls']), ('invariant_violations', 0, 0))

    def test_stale_source_hash_and_internal_errors(self):
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AssertionError): worker.execute(dict(study.params('S1'), source_hash='stale'), Path(td) / 'out')
        run = FakeRun('x/1', study.params('S1'))
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'assignments', side_effect=RuntimeError('boom')):
            with self.assertRaises(RuntimeError): worker.execute(run.params, Path(td) / 'out', run)
        self.assertEqual(run.final[0], 'fail'); self.assertGreaterEqual(run.final[1]['invalid'], 1)
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, run.final[1])


class Gates(unittest.TestCase):
    def test_coordinator_gates(self):
        hub = FakeHub()
        for stage in ('P0', 'Q0', 'S1'):
            with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, stage)
        hub.add('S0'); self.assertEqual(len(coordinator.enqueue(hub, 'P0')), 1)
        for stage, reason in (('P0', 'batch_exists_no_replay'), ('S0', 'batch_exists_no_replay')):
            with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, stage)
            self.assertEqual(str(ctx.exception), reason)
        for kwargs in ({'status': 'failed'}, {'invalid': 1}, {'passed': 0}, {'source_hash': 'other'}):
            hub = FakeHub(); hub.add('P0', **kwargs)
            with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'Q0')
            self.assertEqual(str(ctx.exception), 'exact_runtime_qualification_required')
        hub = FakeHub(); hub.add('Q0'); hub.rows.append({'run': 'x/p', 'status': 'running', 'params': {'batch': 'other'}, 'metrics': {}})
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'S1')
        self.assertEqual(str(ctx.exception), 'queue_not_empty')

    def test_continuation_gate(self):
        hub = FakeHub(); hub.add('Q0')
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue_continuation(hub, 1)
        self.assertEqual(str(ctx.exception), 'earlier_s1_runs_missing')
        hub.add('S1', status='failed', invalid=5, passed=None, resumable=0)
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue_continuation(hub, 1)
        self.assertEqual(str(ctx.exception), 'last_s1_run_is_not_a_billing_stop')
        hub.rows[-1]['metrics']['resumable'] = 1
        ids = coordinator.enqueue_continuation(hub, 1); self.assertEqual(hub.rows[-1]['params']['batch'], 's1-001-r1'); self.assertEqual(hub.rows[-1]['params']['continuation'], 1)
        with self.assertRaises(coordinator.GateRefused): coordinator.enqueue_continuation(hub, 1)
        hub = FakeHub(); hub.add('S1', status='failed', resumable=1)                       # no passed Q0 at this hash
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue_continuation(hub, 1)
        self.assertEqual(str(ctx.exception), 'exact_runtime_qualification_required')

    def chain_with(self, outcomes, stages=('S0', 'P0', 'Q0', 'S1'), metrics=None, probe=True):
        hub = FakeHub(); executed = []; metrics = metrics or {}
        def fake_execute(p, out, run=None, backend=None, deadline=None, opener=None, earlier_rows=(), units=None, prior_rows=None, clock=None, sleep=None):
            executed.append(p['stage']); out = Path(out); out.mkdir(parents=True)
            ok = outcomes.get(p['stage'], 'done') == 'done'
            m = {'episodes': 1, 'invalid': 0, 'failed': 0, 'model_calls': 23, 'transport_attempts': 23, 'input_tokens': 59800, 'output_tokens': 920,
                 'cost_usd': 0.0019, 'qualification_passed': int(ok), 'max_tokens_per_byte': 0.45, 'fixture_exact': 1, 'billing_pauses': 0,
                 'billing_pause_seconds': 0, 'billing_affected_calls': 0, 'resumable': 0}
            m.update(metrics.get(p['stage'], {}))
            (out / 'summary.json').write_text(json.dumps(dict(m, planned=1, graded=1, not_started=0, errors=[], stop_reason=None)))
            if p['stage'] == 'P0' and probe:
                row = dict(scripted_rows('P0')[0], source_hash=study.source_hash())
                import gzip
                with gzip.open(out / 'episodes.jsonl.gz', 'wt') as f: f.write(json.dumps(row) + '\n')
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
            self.assertEqual([p.name for p in Path(td).iterdir() if p.name.endswith('.tmp')], [])
        return code, status, executed, hub, resume

    def test_chain_runs_all_stages_and_writes_status(self):
        code, status, executed, hub, _ = self.chain_with({})
        self.assertEqual((code, status['state'], executed, status['all_stages_done']), (0, 'completed', ['S0', 'P0', 'Q0', 'S1'], True))
        self.assertTrue(status['stages']['S1']['projection']['within_cap']); self.assertTrue(status['stages']['Q0']['input_ceiling']['within_ceiling'])
        for stage in study.STAGES:
            for key in ('run', 'status', 'calls', 'input_tokens', 'output_tokens', 'cost_usd', 'started', 'ended'): self.assertIn(key, status['stages'][stage])

    def test_chain_stops_at_a_failed_gate_and_queues_nothing_further(self):
        code, status, executed, hub, _ = self.chain_with({'Q0': 'gate_failed'})
        self.assertEqual((code, status['state'], status['stopped_stage'], status['reason'], executed), (3, 'stopped_at_gate', 'Q0', 'gate_failed', ['S0', 'P0', 'Q0']))
        self.assertEqual([r['params']['stage'] for r in hub.rows], ['S0', 'P0', 'Q0']); self.assertNotIn('S1', status['stages'])
        code, status, executed, hub, _ = self.chain_with({}, stages=('P0', 'Q0', 'S1'))
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed, hub.rows), (3, 'P0', 'exact_runtime_qualification_required', [], []))

    def test_input_ceiling_projection_stops_before_q0_and_before_s1(self):
        code, status, executed, hub, _ = self.chain_with({}, metrics={'P0': {'max_tokens_per_byte': 1.4}})
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed), (3, 'Q0', 'input_ceiling_projection', ['S0', 'P0']))
        self.assertGreater(status['stages']['Q0']['input_ceiling']['projected_input_tokens'], 8000)
        code, status, executed, hub, _ = self.chain_with({}, metrics={'Q0': {'max_tokens_per_byte': 1.4}})
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed), (3, 'S1', 'input_ceiling_projection', ['S0', 'P0', 'Q0']))
        self.assertEqual([r['params']['stage'] for r in hub.rows], ['S0', 'P0', 'Q0'])

    def test_cost_projection_and_missing_probe_row_stop_the_chain(self):
        code, status, executed, hub, _ = self.chain_with({}, metrics={'Q0': {'cost_usd': 0.1}})          # 504 x 0.1/23 = 2.19 > 2
        self.assertEqual((code, status['stopped_stage'], status['reason']), (3, 'S1', 'projection_exceeds_cap'))
        code, status, executed, hub, _ = self.chain_with({}, probe=False)
        self.assertEqual((code, status['stopped_stage'], status['reason'], executed), (3, 'Q0', 'p0_row_missing', ['S0', 'P0']))
        code, status, executed, hub, _ = self.chain_with({}, metrics={'P0': {'fixture_exact': 0}})       # hub and saved row disagree
        self.assertEqual((status['stopped_stage'], status['reason']), ('Q0', 'p0_row_missing'))

    def test_resume_is_refused_unless_the_last_stop_was_a_billing_stop_of_s1(self):
        code, status, executed, hub, resume = self.chain_with({'Q0': 'gate_failed', 'resume': True})
        self.assertEqual(resume, (3, {'state': 'resume_refused', 'reason': 'last_stop_was_not_a_billing_stop_of_S1'}))
        code, status, executed, hub, resume = self.chain_with({'resume': True})
        self.assertEqual(resume[1]['state'], 'resume_refused')

    def test_stage_lists_status_and_verify_output(self):
        self.assertEqual(chain.parse_stages('S0'), ['S0']); self.assertEqual(chain.parse_stages('p0,q0,s1'), ['P0', 'Q0', 'S1'])
        for bad in ('S1,S0', 'S0,Q0', 'S2', '', 'S0,S0'):
            with self.assertRaises(SystemExit): chain.parse_stages(bad)
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td}):
            os.environ.pop(provider.LEDGER_ENV, None)
            for fn, code in ((chain.show_status, 0), (lambda: chain.verify(FakeHub()), 1), (chain.summarize, 1)):
                out = io.StringIO()
                with patch('sys.stdout', out): self.assertEqual(fn(), code)
                lines = out.getvalue().strip().splitlines(); self.assertEqual(len(lines), 1); json.loads(lines[-1])

    def test_rehearsal_refuses_a_hub_that_is_not_local(self):
        self.assertEqual(rehearse.require_local('http://127.0.0.1:8791'), 'http://127.0.0.1:8791')
        for url in ('http://10.0.0.5:8700', 'https://hub.example.org', 'http://localhost:8700', 'http://127.0.0.1.example.org:1', '', None):
            with self.assertRaises(SystemExit): rehearse.require_local(url)


class AnalysisAndFrames(unittest.TestCase):
    def synthetic(self, seats, correct=lambda *a: 1.0, missing=()):
        rows = []
        for task in D['roots']['comparison'][:4]:
            for rate in D['attacker_pass']:
                for rule in D['rules']:
                    for checks in D['check_budgets']:
                        status = 'not_started' if (task, rate, rule, checks) in missing else 'completed'; c = correct(task, rate, rule, checks)
                        e = {'rare_correct': c, 'rare_wrong': 1 - c, 'rare_abstain': 0.0, 'rare_fabricated': 1 - c, 'task_correct': c}
                        r = {'kind': 'pilot', 'task': task, 'attacker_pass': rate, 'rule': rule, 'checks': checks, 'status': status,
                             'admission': dict({f: 0.0 for f in analyze.ADMISSION}, attacker_seats=seats(task, rate, rule, checks))}
                        if status == 'completed': r.update(evaluation=e, reference_evaluation=e)
                        rows.append(r)
        return rows

    def test_primary_contrast_arithmetic_and_sign(self):
        first = D['roots']['comparison'][0]
        def seats(task, rate, rule, checks):
            if rate != 0.1: return 0
            return {('propagated', 32): 2, ('propagated', 108): 16 if task == first else 12, ('direct', 32): 20, ('direct', 108): 10}.get((rule, checks), 5)
        a = analyze.analyze(self.synthetic(seats)); p = a['primary']
        self.assertEqual([x['difference'] for x in p['per_root']], [24, 20, 20, 20]); self.assertAlmostEqual(p['estimate'], 21.0)
        self.assertEqual((p['roots'], p['positive_roots']), (4, 4)); self.assertTrue(20 <= p['interval'][0] <= p['interval'][1] <= 24)
        self.assertEqual(a['secondary']['primary_under_weak_checks']['estimate'], 0)
        esc = {(e['attacker_pass'], e['rule']): e['estimate'] for e in a['escalation']}; self.assertEqual((esc[(0.1, 'propagated')], esc[(0.1, 'direct')]), (11.0, -10.0))
        neg = analyze.analyze(self.synthetic(lambda t, rate, rule, c: 10 if (rule, c) == ('direct', 108) else 0))
        self.assertEqual(neg['primary']['estimate'], -10)

    def test_missing_model_outcomes_are_bounded_and_the_primary_does_not_depend_on_them(self):
        first = D['roots']['comparison'][0]; missing = {(first, 0.1, 'propagated', 108)}
        correct = lambda task, rate, rule, checks: 1.0 if rule == 'propagated' else 0.0
        full = analyze.analyze(self.synthetic(lambda *a: 3)); part = analyze.analyze(self.synthetic(lambda *a: 3, correct, missing))
        self.assertEqual(part['primary']['estimate'], full['primary']['estimate']); self.assertEqual(part['primary']['roots'], 4)
        c = next(x for x in part['model_propagated_minus_direct'] if (x['attacker_pass'], x['checks'], x['field']) == (0.1, 108, 'rare_correct'))
        self.assertEqual((c['roots'], c['assigned_roots'], c['estimate']), (3, 4, 1.0)); self.assertEqual(c['bounds_all_assigned'], [0.75, 1.0])
        cell = next(x for x in part['cells'] if (x['attacker_pass'], x['rule'], x['checks']) == (0.1, 'propagated', 108))
        self.assertEqual((cell['assigned'], cell['valid'], cell['not_started']), (4, 3, 1)); self.assertEqual(cell['rare_correct_bounds_all_assigned'], [0.75, 1.0])
        self.assertEqual(part['denominators']['not_started'], 1)

    def test_frames_and_replay(self):
        from PIL import Image
        s0 = scripted_rows('S0'); grid = [r for r in s0 if r['kind'] != 'qualification']; fixtures = [r for r in s0 if r['kind'] == 'qualification' and r['set'] == 'a']
        partial = grid[:60] + [dict(grid[60], status='failed', error='x')] + [dict(r, status='not_started') for r in grid[61:90]]
        for rows, total, stage in (([], 504, 'S1'), (partial, 504, 'S1'), (s0, 216, 'S0'), ([], 23, 'Q0'), (fixtures[1:], 23, 'Q0'), ([], 1, 'P0'), (fixtures[:1], 1, 'P0')):
            self.assertEqual(render.frame(rows, total, stage, 3.0, {'actual_usd': 0.01}).size, (1800, 1200))
        with patch.object(render, 'FONT_PATHS', ('/nonexistent/font.ttf',)):
            render.font.cache_clear(); self.assertEqual(render.frame([], 10, 'S1').size, (1800, 1200)); render.font.cache_clear()
        seats = render.seats_by_root(s0); self.assertEqual(len(seats[(0.1, 'propagated')]), 8)
        self.assertEqual(sum(v[108] for v in seats[(0.1, 'propagated')].values()) / 8, 15.5)
        rows = [dict(r, elapsed_seconds=i, completion_index=i, study_accounting={}) for i, r in enumerate(grid[:80])]
        with tempfile.TemporaryDirectory() as td:
            n = render.replay(rows, Path(td), 'S0', 168, {}, frames=4)
            with Image.open(Path(td) / 'replay.gif') as gif:
                self.assertEqual((n, gif.n_frames, gif.size), (5, 5, (1800, 1200)))
                for i in range(gif.n_frames): gif.seek(i); gif.load()
            self.assertTrue((Path(td) / 'final_frame.png').exists() and (Path(td) / 'initial_frame.png').exists())


if __name__ == '__main__':
    unittest.main()
