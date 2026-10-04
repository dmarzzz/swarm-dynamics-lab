"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the standard
unittest summary ("Ran N tests ... OK") on stderr.

Three groups: the instrument and its scorer (Instrument, Analysis), one stage and the chain against an
in-memory hub and a local stub of the model endpoint (Stage, Chain), and the reference adapter's own
tests, copied unchanged from researchers/dmarz/notes/pipeline/reference/test_openrouter_provider.py
(Request, Answers, Transport, Billing, LedgerRules)."""
import copy
import gzip
import hashlib
import io
import json
import os
from pathlib import Path
import socket
import sys
import tempfile
import threading
import unittest
import urllib.error
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))

from PIL import Image  # noqa: E402

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

orp = provider
D = study.design(); B = D['budget']; MAIN = D['layouts']['main']; ENG = D['layouts']['engineering']
FROZEN = {  # a change here is a change of the instrument
    'main_layouts': '9a8ee6dfa6a6039d3cffdf016665da1a212c510943f1798a5764685287e589c5',
    'system_prompt': 'f981dfe98990431b88ef0c4081c9c6a11d48401b20a1354aad99c1a4b6bbe992',
    'first_main_request': 'e9f6de829af8f2c73aa730f5396ecc35c53a176a1f9f009752e0f09c755619d0'}
TEST_KEY = 'sk-or-selftest-SECRET-not-a-credential'
PROGRAM_TEMPLATE = {'model': 'qwen/qwen3.7-flash',
                    'provider': {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True},
                    'reasoning': {'enabled': False}, 'max_tokens': 1000, 'response_format': {'type': 'json_object'}}
REFERENCE_ADAPTER_SHA256 = '86d0739e9bf83fcb12c382b5d1844ed7011b56a2bb77baebdcf7ad275b58d789'
_cache = {}


def rows_for(stage, name='optimal'):
    """Completed rows a scripted policy would produce for a stage (evaluator side, no call)."""
    key = (stage, name)
    if key not in _cache: _cache[key] = study.policy_rows(study.assignments(stage), name)
    return copy.deepcopy(_cache[key])


def grid_rows(by_representation, kind='main'):
    return analyze.scripted_rows(kind, by_representation)


def p0_rows(served='Alibaba', **accounting):
    return [dict(rows_for('P0')[0], accounting=dict({'response_provider': served, 'input_tokens': 600}, **accounting))]


def probe_row():
    return [dict(p0_rows()[0], source_hash=study.source_hash())]


class FakeRun:
    def __init__(self, run_id, params, row=None):
        self.id, self.params, self.attempt = run_id, params, 1; self.final = None; self.row = row; self.messages = []
        self.artifacts = {}
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
    def add(self, stage, status='done', invalid=0, passed=1, source_hash=None, **metrics):
        p = study.params(stage); p['source_hash'] = source_hash or p['source_hash']
        self.rows.append({'run': f'x/{stage}{len(self.rows)}', 'status': status, 'params': p, 'artifacts': [],
                          'metrics': dict({'invalid': invalid, 'qualification_passed': passed, 'model_calls': 23, 'cost_usd': 0.0005}, **metrics)})
    def row(self, batch): return next(r for r in self.rows if r['params'].get('batch') == batch)


class Env(unittest.TestCase):
    """A temporary results directory, ledger and credential alias; the adapter's waits take no time."""
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.dir = Path(self.tmp.name)
        self.env = patch.dict(os.environ, {provider.KEY_ENV: TEST_KEY, 'STUDY_RESULTS_DIR': str(self.dir / 'results'),
                                           provider.LEDGER_ENV: str(self.dir / 'ledger' / 'ledger.jsonl')})
        self.env.start(); self.clock = rehearse.Clock()
        self.patches = [patch.object(worker, 'CLOCK', self.clock.now), patch.object(worker, 'SLEEP', self.clock.sleep),
                        patch.object(render, 'replay', lambda rows, total, out, stage, frames=8: Path(out, 'replay.gif').write_bytes(b'GIF89a') and 1)]
        for p in self.patches: p.start()
        self.n = 0

    def tearDown(self):
        for p in self.patches: p.stop()
        self.env.stop(); self.tmp.cleanup()

    def stage(self, stage, stub, run=None, fresh_ledger=False, **kw):
        """Run one stage through worker.execute. Returns (summary or None, reason or None, rows, directory)."""
        self.n += 1; out = self.dir / f'stage-{self.n}'
        if stage == 'Q0': kw.setdefault('probe_rows', probe_row())
        env = {provider.LEDGER_ENV: str(self.dir / f'ledger-{self.n}.jsonl')} if fresh_ledger else {}
        with patch.dict(os.environ, env):
            try: summary, reason = worker.execute(study.params(stage), out, run, opener=stub, **kw), None
            except worker.StageFailed as exc: summary, reason = None, str(exc)
        return summary, reason, chain.read_jsonl(out / chain.ROWS), out

    def ledger(self):
        return provider.Ledger(os.environ[provider.LEDGER_ENV], B).transact()


class Instrument(unittest.TestCase):
    def test_layouts_are_deterministic_frozen_and_fresh(self):
        self.assertEqual(sim.layout(3000), sim.layout(3000))
        self.assertEqual(study.digest([sim.layout(s) for s in MAIN]), FROZEN['main_layouts'])
        self.assertEqual(study.digest(study.SYSTEM), FROZEN['system_prompt'])
        self.assertEqual(study.assignments('S1')[0]['input_hash'], FROZEN['first_main_request'])
        w = sim.layout(3000)
        self.assertEqual(len(sim.CELLS), 36); self.assertNotEqual(w['report_cell'], w['unknown_cell'])
        self.assertEqual(sim.NAMESPACE, D['rng_namespace'])
        for bad in (-1, 10000, '3000', 3000.0):
            with self.assertRaises(ValueError): sim.layout(bad)

    def test_source_files_of_the_copy_are_the_recorded_ones(self):
        src = D['source_instrument']; base = study.ROOT.parents[3] / src['study'] / 'src'
        if not base.is_dir(): self.skipTest('phantom-coast source not in this checkout')
        for name in ('contract', 'design', 'engine'):
            self.assertEqual(hashlib.sha256((base / f'{name}.py').read_bytes()).hexdigest(), src[f'{name}_sha256'])

    def test_adapter_is_the_reference_adapter_unchanged(self):
        self.assertEqual(hashlib.sha256((study.ROOT / 'src' / 'provider.py').read_bytes()).hexdigest(), REFERENCE_ADAPTER_SHA256)
        self.assertEqual(D['request_template'], PROGRAM_TEMPLATE)
        self.assertEqual((D['model'], D['canonical_model'], D['provider']), ('qwen/qwen3.7-flash', 'qwen/qwen3.7-flash-20260727', 'alibaba'))
        self.assertEqual((B['input_usd_per_million'], B['output_usd_per_million'], B['aggregate_usd']), (0.03, 0.13, 2))
        self.assertEqual((B['max_output_tokens'], B['max_input_tokens'], B['workers'], B['request_timeout_seconds']), (1000, 8000, 4, 120))
        config = study.provider_config()
        for key in ('max_calls', 'max_attempted_calls', 'aggregate_usd', 'max_output_tokens', 'max_input_tokens', 'max_input_bytes',
                    'max_visible_chars', 'request_timeout_seconds', 'retry', 'billing_outage', 'max_transport_attempts',
                    'input_usd_per_million', 'output_usd_per_million'):
            self.assertIn(key, config['budget'])
        self.assertEqual(B['retry'], {'transport_retries': 2, 'retryable_http_status': [429, 502, 503, 529],
                                      'backoff_seconds': [2, 6], 'retry_after_cap_seconds': 20})
        self.assertEqual((B['billing_outage']['retry_every_seconds'], B['billing_outage']['max_wait_seconds']), (60, 1200))
        self.assertGreaterEqual(B['max_transport_attempts'], B['max_attempted_calls'] + 40)

    def test_score_reproduces_the_pc5_rule_at_its_two_conditions_and_generalizes(self):
        w = sim.layout(ENG[0]); rc, uc = w['report_cell'], w['unknown_cell']
        # PC5: reliability 0.8 (e 0.20), UNKNOWN 0.25 -> explore optimal, checking costs 0.05; reliability 0.2 -> check optimal, exploring costs 0.55
        for e, best, wrong, regret in ((0.20, uc, rc, 0.05), (0.80, rc, uc, 0.55)):
            self.assertTrue(sim.score(w, e, 0.25, best)['optimal']); self.assertEqual(sim.score(w, e, 0.25, best)['expected_regret'], 0)
            self.assertEqual(sim.score(w, e, 0.25, wrong)['expected_regret'], regret); self.assertFalse(sim.score(w, e, 0.25, wrong)['optimal'])
            none = sim.score(w, e, 0.25, None)
            self.assertEqual(none['action'], 'no_inspection'); self.assertAlmostEqual(none['expected_loss'], e + 0.25)
            self.assertGreater(none['expected_loss'], sim.score(w, e, 0.25, wrong)['expected_loss'])
        for e, u in study.cases():
            check, explore = sim.score(w, e, u, rc), sim.score(w, e, u, uc)
            self.assertEqual((check['expected_loss'], explore['expected_loss']), (u, e))
            self.assertEqual(check['optimal'], e > u); self.assertEqual(explore['optimal'], e < u)
            self.assertAlmostEqual(check['expected_regret'] + explore['expected_regret'], abs(e - u))
            self.assertEqual(sim.score(w, e, u, '9,9')['action'], 'no_inspection')
        for e, u in ((0.25, 0.25), (0, 0.5), (1.0, 0.5), (0.123, 0.5), (1, 0.5)):
            with self.assertRaises(ValueError): sim.score(w, e, u, rc)

    def test_minimum_loss_action_is_recomputed_independently_from_the_rendered_consequences(self):
        """No use of sim.score or sim.optimal_action: the expected cost of each action is the sum of probability x cost
        over the records parsed from the text the model is sent, in each representation."""
        seen = 0
        for stage in study.STAGES:
            for a in study.assignments(stage):
                _, block, _ = study.split_block(study.user_for(a)); records = study.PARSE[a['representation']](block)
                cost = {}
                for r in records:
                    if r['action'] != 'either': cost[r['action']] = cost.get(r['action'], 0.0) + float(r['probability']) * float(r['cost'])
                self.assertEqual(sorted(cost), sorted(a['legal_cells']))
                best = min(cost, key=cost.get); worst = max(cost, key=cost.get); gap = round(cost[worst] - cost[best], 12)
                self.assertGreater(gap, 0.04)                                        # never a tie
                self.assertEqual(best, study.policy('optimal', a))
                self.assertEqual(study.evaluate(a, best)['expected_regret'], 0); self.assertEqual(study.evaluate(a, worst)['expected_regret'], gap)
                self.assertAlmostEqual(study.evaluate(a, worst)['expected_loss'], cost[worst]); self.assertEqual(study.evaluate(a, best)['margin'], gap)
                w = study.layout(a['layout'])                                        # the cheaper action is to check exactly when e > U
                self.assertEqual(best == w['report_cell'], a['error'] > a['unknown_cost']); seen += 1
        self.assertEqual(seen, 744)

    def test_reservation_leaves_a_wide_margin_over_the_expected_cost(self):
        """Per call the adapter reserves request bytes as input tokens plus the full 1,000-token output limit. The
        expected cost at the planning ratio (2.5 characters per token) and 20 output tokens is several times smaller,
        so a price somewhat above the snapshot does not breach the reservation."""
        for stage in ('P0', 'Q0', 'S1'):
            for a in study.assignments(stage)[:48]:
                body = dict(D['request_template'], messages=[{'role': 'system', 'content': study.SYSTEM}, {'role': 'user', 'content': study.user_for(a)}])
                size = len(json.dumps(body).encode())
                reserve = size * B['input_usd_per_million'] + B['max_output_tokens'] * B['output_usd_per_million']
                expected = a['content_bytes'] / study.CHARS_PER_TOKEN_FLOOR * B['input_usd_per_million'] + 20 * B['output_usd_per_million']
                self.assertGreater(reserve, 7 * expected); self.assertLess(reserve, 250)        # millionths of a dollar
        self.assertLess(600 * 250 / 1e6, B['aggregate_usd'] / 10)                              # every call at its full reservation is under a tenth of the cap

    def test_report_truth_is_coupled_and_calibrated_across_error_probabilities(self):
        w = dict(sim.layout(ENG[0]))
        for draw, want in ((0.1, (False, False, False, True)), (0.3, (False, False, True, True)), (0.6, (False, False, True, True)),
                           (0.85, (False, True, True, True)), (0.97, (True, True, True, True))):
            w['truth_draw'] = draw
            self.assertEqual(tuple(sim.score(w, e, 0.25 if e != 0.25 else 0.1, None)['report_actually_false'] for e in (0.05, 0.20, 0.50, 0.80))[::1],
                             tuple(draw >= 1 - e for e in (0.05, 0.20, 0.50, 0.80)))
        false = sum(sim.layout(s)['truth_draw'] >= 0.5 for s in range(4000, 4400))
        self.assertTrue(160 <= false <= 240)

    def test_the_optimum_changes_across_the_twelve_cases_and_constant_policies_lose(self):
        best = {(e, u): sim.optimal_action(e, u) for e, u in study.cases()}
        self.assertEqual(len(best), 12); self.assertEqual(sorted(best.values()).count('check'), 6)
        self.assertEqual({k for k, v in best.items() if v == 'check'}, {(0.2, 0.1), (0.5, 0.1), (0.5, 0.25), (0.8, 0.1), (0.8, 0.25), (0.8, 0.75)})
        c = analyze.calibration()
        self.assertAlmostEqual(c['mean_regret']['always_check'], 0.15); self.assertAlmostEqual(c['mean_regret']['always_explore'], 2.05 / 12)
        self.assertEqual(c['mean_regret']['optimal'], 0); self.assertAlmostEqual(c['largest_possible_contrast'], 3.85 / 12)
        self.assertGreater(c['mean_regret']['always_first'], 0.1); self.assertGreater(c['mean_regret']['always_second'], 0.1)
        for line in c['cases']:
            self.assertEqual(line['optimal'], 0); self.assertAlmostEqual(line['always_check'] + line['always_explore'], line['margin'])
            self.assertEqual(line['always_check'] > 0, line['optimal_action'] == 'explore')
        self.assertEqual(analyze.discrimination(), []); self.assertEqual(analyze.discrimination('main'), [])

    def test_both_actions_are_legal_in_every_request_of_every_stage(self):
        for stage in study.STAGES:
            for a in study.assignments(stage):
                w = study.layout(a['layout']); text = study.user_for(a)
                self.assertEqual(sorted(a['legal_cells']), sorted([w['report_cell'], w['unknown_cell']])); self.assertEqual(len(set(a['legal_cells'])), 2)
                for cell in a['legal_cells']:
                    self.assertEqual(study.validate({'inspect': cell}, a['legal_cells']), {'inspect': cell})
                    self.assertIn(f'{{"inspect": "{cell}"}}', text)
                self.assertEqual({sim.action_of(w, c) for c in a['legal_cells']}, {'check', 'explore'})

    def test_the_two_representations_hold_exactly_the_same_facts_and_nothing_more(self):
        seen = 0
        for stage in study.STAGES:
            for a in study.assignments(stage):
                if a['representation'] != 'prose': continue
                w = study.layout(a['layout']); records = study.shown(sim.consequences(w, a['error'], a['unknown_cost'])); seen += 1
                prose = study.user_text(w, a['error'], a['unknown_cost'], 'prose'); table = study.user_text(w, a['error'], a['unknown_cost'], 'table')
                (h1, b1, t1), (h2, b2, t2) = study.split_block(prose), study.split_block(table)
                self.assertEqual((h1, t1), (h2, t2))                                         # identical outside the block
                self.assertEqual(study.parse_prose(b1), records); self.assertEqual(study.parse_table(b2), records)   # same facts
                self.assertEqual(study.render_prose(study.parse_prose(b1)), b1)              # nothing more: the block is a function of the facts
                self.assertEqual(study.render_table(study.parse_table(b2)), b2)
                self.assertEqual(sorted(study.numbers(b1)), sorted(study.numbers(b2)))       # same numbers, with multiplicity
                self.assertEqual(len(records), 6); self.assertEqual(len(study.numbers(b1)), 12)
                self.assertEqual(set(__import__('re').findall(r'\d,\d', b1)), set(a['legal_cells']))
                for block in (b1, b2):
                    for word in ('expected', 'optimal', 'best', 'better', 'should', 'prefer', 'total', 'sum', 'average', 'regret'):
                        self.assertNotIn(word, block.lower())
                # no number in either block is a derived quantity: every number is 0.00, 1.00, e, 1 - e or U
                self.assertLessEqual(set(study.numbers(b1)), {'0.00', '1.00', study.fmt(a['error']), study.fmt(1 - a['error']), study.fmt(a['unknown_cost'])})
        self.assertEqual(seen, (144 + 24 + 576) // 2)

    def test_the_equal_information_check_detects_a_representation_that_says_more_or_less(self):
        a = study.assignments('S1')[0]; base = study.check_request(a); self.assertEqual(base, [])
        original = dict(study.RENDER)
        def hint(records): return original['table'](records) + '\nexpected cost | inspect first | 0.25'
        def fewer(records): return original['prose'](records).replace(' with probability 1.00', '', 1)
        def changed(records): return original['table'](records).replace('1.00 | 0.00', '0.90 | 0.00', 1)
        def recommends(records): return original['prose'](records) + '\nThe better action is the first one.'
        for rep, tampered in (('table', hint), ('prose', fewer), ('table', changed), ('prose', recommends)):
            with patch.dict(study.RENDER, {rep: tampered}):
                found = [v for x in study.assignments('S1')[:4] for v in study.check_request(dict(x, input_hash=study.digest([study.SYSTEM, study.user_for(x)])))]
            self.assertTrue(found, rep); self.assertTrue(any('block' in v or 'representations' in v or 'numbers' in v for v in found), found)
        for bad in ('junk', study.TABLE_HEADER + '\ninspect 1,1 | 1,1 | something else | 1.00 | 0.00'):
            with self.assertRaises(ValueError): study.parse_table(bad)
        with self.assertRaises(ValueError): study.parse_prose('If you inspect 1,1: it is fine.')

    def test_within_a_layout_only_e_and_u_and_the_representation_change(self):
        for seed in MAIN + ENG: self.assertEqual(study.check_layout(seed, study.cases()), [])
        original = study.user_text
        def leaky(w, e, u, rep): return original(w, e, u, rep) + (' Take care.' if e > u else '')
        with patch.object(study, 'user_text', leaky): self.assertTrue(study.check_layout(MAIN[0], study.cases()))
        def shifted(w, e, u, rep): return original(w, e, u, rep).replace('1.00, at cost 0.00', f'{0.9 + e / 10:.2f}, at cost 0.00', 1)
        with patch.object(study, 'user_text', shifted): self.assertTrue(study.check_layout(MAIN[0], study.cases()))
        # across the 24 requests of a layout the cells, labels, measurements and listing order never change
        mine = [a for a in study.assignments('S1') if a['layout'] == MAIN[0]]
        self.assertEqual(len(mine), 24); self.assertEqual(len({tuple(a['legal_cells']) for a in mine}), 1)
        self.assertEqual(len({study.user_for(a).split('Report, older')[0] for a in mine}), 1)

    def test_requests_hold_no_truth_seed_optimum_or_evaluator_word(self):
        for stage in study.STAGES:
            for a in study.assignments(stage):
                w = study.layout(a['layout']); text = study.user_for(a); low = (study.SYSTEM + text).lower()
                for word in study.FORBIDDEN: self.assertNotIn(word, low)
                self.assertNotIn(str(a['layout']), text); self.assertNotIn(repr(w['truth_draw'])[:8], text)
                shown = dict(pair.split(' ') for pair in text.split('cells): ')[1].split('\n')[0].split('; '))
                self.assertEqual(len(shown), 34); self.assertNotIn(w['unknown_cell'], shown); self.assertNotIn(w['report_cell'], shown)
                self.assertTrue(all(w['truth'][c] == label for c, label in shown.items()))
                self.assertNotIn(a['id'], text); self.assertNotIn(a['kind'], low)
        leak = dict(study.assignments('S1')[0])
        with patch.object(study, 'SYSTEM', study.SYSTEM + ' The optimal cell is listed first.'):
            self.assertIn(f'{leak["id"]}:forbidden_text', study.check_request(leak))

    def test_listing_order_and_report_label_are_balanced(self):
        combos = {}
        for s in MAIN:
            w = study.layout(s); key = (w['legal_order'][0] == w['report_cell'], w['report_label']); combos[key] = combos.get(key, 0) + 1
        self.assertEqual(sorted(combos.values()), [6, 6, 6, 6])
        self.assertEqual(len({(study.layout(s)['legal_order'][0] == study.layout(s)['report_cell'], study.layout(s)['report_label']) for s in ENG}), 4)

    def test_local_validation_is_strict(self):
        legal = ['3,3', '0,2']
        self.assertEqual(study.validate({'inspect': '0,2'}, legal), {'inspect': '0,2'})
        for bad in ({'inspect': '1,1'}, {'inspect': '3, 3'}, {'inspect': ' 3,3'}, {'inspect': [3, 3]}, {'inspect': None}, {'inspect': 33},
                    {'inspect': '3,3', 'reason': 'x'}, {'Inspect': '3,3'}, {}, ['3,3'], '3,3', None, {'inspect': '3,3', 'inspect2': '0,2'},
                    {'inspect': 'check'}, {'inspect': True}):
            with self.assertRaises(ValueError): study.validate(bad, legal)

    def test_stage_counts_caps_and_disjoint_splits(self):
        counts = {s: len(study.assignments(s)) for s in study.STAGES}
        self.assertEqual(counts, {'S0': 144, 'P0': 1, 'Q0': 23, 'S1': 576})
        self.assertEqual(B['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 576}); self.assertEqual(B['max_attempted_calls'], 600)
        self.assertEqual(B['max_failed'], 6)
        ids = [a['id'] for s in study.STAGES for a in study.assignments(s)]
        self.assertEqual(len(set(ids)), 144 + 576)            # P0 and Q0 are the active qualification set, which S0 also answers
        s1 = study.assignments('S1')
        self.assertEqual(len({a['layout'] for a in s1}), 24); self.assertEqual(len({(a['error'], a['unknown_cost']) for a in s1}), 12)
        for seed in MAIN:
            mine = [a for a in s1 if a['layout'] == seed]
            self.assertEqual(sorted((a['error'], a['unknown_cost'], a['representation']) for a in mine),
                             sorted((e, u, r) for e, u in study.cases() for r in study.REPRESENTATIONS))
        L = D['layouts']; groups = [L['engineering'], L['qualification_a'], L['qualification_b'], L['main']]
        self.assertEqual(len({s for g in groups for s in g}), sum(len(g) for g in groups)); self.assertLess(max(max(g) for g in groups), 10000)
        self.assertEqual(study.check_design(), []); self.assertEqual(study.check_invariants('S0'), [])
        self.assertLess(study.largest_request_bytes('S1'), B['max_input_bytes'])
        self.assertLess(study.largest_request_bytes('S1') / study.CHARS_PER_TOKEN_FLOOR, B['max_input_tokens'] / 5)
        self.assertEqual(D['stages']['S2'], {'enabled': False})

    def test_qualification_fixtures_are_clear_dominance_choices_with_both_actions_legal(self):
        q = D['qualification']; main = set(study.cases())
        for g in ('a', 'b'):
            fx = study.fixtures(g); self.assertEqual(len(fx), 24); self.assertEqual(len({a['layout'] for a in fx}), 12)
            for a in fx:
                self.assertGreaterEqual(round(abs(a['error'] - a['unknown_cost']), 12), q['min_margin'])
                self.assertNotIn((a['error'], a['unknown_cost']), main); self.assertEqual(len(set(a['legal_cells'])), 2)
                self.assertEqual(study.check_request(a), [])
            self.assertEqual([study.evaluate(a, study.policy('optimal', a))['optimal_action'] for a in fx], ['check'] * 12 + ['explore'] * 12)
        pairs = lambda g: {(a['error'], a['unknown_cost']) for a in study.fixtures(g)}
        self.assertFalse(pairs('a') & pairs('b')); self.assertFalse({a['layout'] for a in study.fixtures('a')} & {a['layout'] for a in study.fixtures('b')})
        self.assertEqual(study.active_set(), 'a'); self.assertEqual(q['repairs_allowed'], 1)
        self.assertEqual(study.assignments('P0')[0]['id'], study.fixtures('a')[0]['id'])
        self.assertEqual([a['id'] for a in study.assignments('Q0')], [a['id'] for a in study.fixtures('a')[1:]])

    def test_qualification_gate_thresholds(self):
        fx = lambda name='optimal', g='a': study.policy_rows(study.fixtures(g), name)
        ok = study.qualification(fx()); self.assertTrue(ok['passed']); self.assertEqual((ok['prose']['optimal'], ok['table']['optimal'], ok['valid']), (12, 12, 24))
        def miss(rows, rep, n):
            hit = 0
            for r in rows:
                if r['representation'] == rep and hit < n:
                    wrong = next(c for c in r['legal_cells'] if c != r['answer']['inspect'])
                    r.update(answer={'inspect': wrong}, evaluation=study.evaluate(r, wrong)); hit += 1
            return rows
        self.assertTrue(study.qualification(miss(fx(), 'prose', 1))['passed'])                       # 11 of 12 passes
        self.assertTrue(study.qualification(miss(miss(fx(), 'prose', 1), 'table', 1))['passed'])
        two = study.qualification(miss(fx(), 'table', 2)); self.assertFalse(two['passed']); self.assertEqual(len(two['misses']), 2)
        invalid = fx(); invalid[5].update(status='failed'); self.assertFalse(study.qualification(invalid)['passed'])   # valid structure throughout
        self.assertFalse(study.qualification(fx()[:23])['passed']); self.assertFalse(study.qualification(fx() + fx()[:1])['passed'])
        self.assertFalse(study.qualification(fx()[:12] + fx(g='b')[12:])['passed'])                  # one set only
        for name in study.POLICIES[1:]:
            for g in ('a', 'b'):
                r = study.qualification(fx(name, g)); self.assertFalse(r['passed']); self.assertEqual((r['prose']['optimal'], r['table']['optimal']), (6, 6))
        s0 = study.scripted_qualification(rows_for('S0')); self.assertTrue(s0['a']['passed'] and s0['b']['passed'])

    def test_gates_per_stage_and_q0_needs_the_probe_row(self):
        self.assertTrue(study.gate('S0', rows_for('S0'))); self.assertFalse(study.gate('S0', rows_for('S0'), ['x']))
        self.assertFalse(study.gate('S0', rows_for('S0', 'always_check')))
        self.assertTrue(study.gate('P0', p0_rows())); self.assertTrue(study.gate('P0', p0_rows('alibaba/intl'))); self.assertIsNone(study.gate('S1', rows_for('S1')))
        for served in (None, 'DeepInfra', '', 7): self.assertFalse(study.gate('P0', p0_rows(served)))     # the response must name the pinned provider
        self.assertFalse(study.gate('P0', rows_for('P0')))
        failed = p0_rows(); failed[0]['status'] = 'failed'; self.assertFalse(study.gate('P0', failed))
        self.assertFalse(study.gate('P0', rows_for('Q0')[:1]))                                       # not the probe fixture
        q0 = rows_for('Q0')
        self.assertTrue(study.gate('Q0', q0, (), probe_row())); self.assertFalse(study.gate('Q0', q0))
        self.assertFalse(study.gate('Q0', q0, (), [dict(probe_row()[0], source_hash='0' * 64)]))
        self.assertFalse(study.gate('Q0', q0, (), [dict(q0[0], source_hash=study.source_hash())]))
        wrong_probe = probe_row(); other = next(c for c in wrong_probe[0]['legal_cells'] if c != wrong_probe[0]['answer']['inspect'])
        wrong_probe[0].update(answer={'inspect': other}, evaluation=study.evaluate(wrong_probe[0], other))
        self.assertTrue(study.gate('Q0', q0, (), wrong_probe))                                       # the probe's miss is the one allowed miss
        second = next(r for r in q0 if r['representation'] == wrong_probe[0]['representation'])
        other = next(c for c in second['legal_cells'] if c != second['answer']['inspect'])
        second.update(answer={'inspect': other}, evaluation=study.evaluate(second, other))
        self.assertFalse(study.gate('Q0', q0, (), wrong_probe))                                      # two misses in one representation
        probe = study.probe_gate(p0_rows(response_model=D['canonical_model'], finish_reason='stop', reasoning_tokens=0, latency_seconds=1.5,
                                         response_id='gen-1', provider_reported_usd=0.00002))
        self.assertTrue(probe['passed'] and probe['provider_is_pinned']); self.assertAlmostEqual(probe['tokens_per_byte'], 600 / study.assignments('P0')[0]['content_bytes'])
        self.assertEqual((probe['response_model'], probe['response_provider'], probe['response_id'], probe['finish_reason'], probe['reasoning_tokens'],
                          probe['latency_seconds'], probe['provider_reported_usd']), (D['canonical_model'], 'Alibaba', 'gen-1', 'stop', 0, 1.5, 0.00002))

    def test_design_check_detects_an_uninformative_design(self):
        def with_design(change):
            d = copy.deepcopy(D); change(d); study._assignments.cache_clear()
            try:
                with patch.object(study, 'design', lambda: d): return study.check_design()
            finally: study._assignments.cache_clear()
        self.assertIn('optimum_must_change_across_the_twelve_cases', with_design(lambda d: d.update(unknown_costs=[0.85, 0.90, 0.95])))
        self.assertIn('qualification_a:margin_below_stated_minimum', with_design(lambda d: d['qualification']['fixtures_a'].__setitem__(0, [0.60, 0.05])))
        self.assertIn('qualification_pairs_not_disjoint', with_design(lambda d: d['qualification']['fixtures_b'].__setitem__(0, [0.90, 0.05])))
        self.assertTrue(with_design(lambda d: d['qualification']['fixtures_a'].reverse()))
        self.assertIn('order_and_label_not_balanced_over_main_layouts', with_design(lambda d: d['layouts'].update(main=list(range(3000, 3048, 2)))))
        self.assertIn('max_failed_rule', with_design(lambda d: d['budget'].update(max_failed=3)))
        self.assertIn('S1:call_cap_differs_from_assignments', with_design(lambda d: d['budget']['max_calls'].update(S1=600)))
        self.assertEqual(study.check_design(), [])

    def test_manifest_regenerates_identically(self):
        fresh = manifest.text(manifest.build())
        self.assertEqual(manifest.PATH.read_text(), fresh); self.assertLess(len(fresh), 300_000)
        m = json.loads(fresh)
        self.assertEqual({s: (e['assignments'], e['max_calls']) for s, e in m['stages'].items()},
                         {'S0': (144, 0), 'P0': (1, 1), 'Q0': (23, 23), 'S1': (576, 576)})
        self.assertEqual(m['stages']['S1']['distinct_inputs'], 576); self.assertEqual(m['qualification_set'], 'a')

    def test_source_hash_covers_code_and_design_only(self):
        names = ['design.yaml', 'experiment.yaml', 'requirements.txt'] + sorted(p.name for p in (study.ROOT / 'src').glob('*.py'))
        self.assertEqual(len(names), 14)
        want = study.digest([(n, hashlib.sha256((study.ROOT / ('src' if n.endswith('.py') else '') / n).read_bytes()).hexdigest()) for n in names])
        self.assertEqual(study.source_hash(), want)
        self.assertEqual({study.params(s)['backend'] for s in ('P0', 'Q0', 'S1')}, {'openrouter'}); self.assertEqual(study.params('S0')['backend'], 'scripted')
        self.assertEqual([study.batch(s) for s in study.STAGES], ['s0-001', 'p0-001', 'q0-001', 's1-001'])

    def test_the_stub_derives_the_optimum_from_the_request_text_alone(self):
        for stage in study.STAGES:
            for a in study.assignments(stage):
                text = study.user_for(a)
                self.assertEqual(rehearse.reference_answer(text, 'optimal'), {'inspect': study.policy('optimal', a)})
                self.assertEqual(rehearse.reference_answer(text, 'always_first'), {'inspect': a['legal_cells'][0]})


class Analysis(unittest.TestCase):
    def test_primary_contrast_sign_pairing_and_interval(self):
        zero = analyze.analyze(grid_rows({'prose': 'optimal', 'table': 'optimal'}))['primary']
        self.assertEqual((zero['estimate'], zero['layouts'], zero['assigned_layouts'], zero['zero']), (0.0, 24, 24, 24))
        better = analyze.analyze(grid_rows({'prose': 'always_check', 'table': 'optimal'}))
        self.assertAlmostEqual(better['primary']['estimate'], -0.15); self.assertEqual(better['primary']['negative'], 24)
        self.assertAlmostEqual(better['representations']['prose']['mean_regret'], 0.15); self.assertEqual(better['representations']['table']['mean_regret'], 0)
        worse = analyze.analyze(grid_rows({'prose': 'optimal', 'table': 'always_explore'}))['primary']
        self.assertAlmostEqual(worse['estimate'], 2.05 / 12); self.assertEqual(worse['positive'], 24)
        # a mixture: the table helps on the first 12 layouts only
        rows = [r for r in grid_rows({'prose': 'always_check', 'table': 'optimal'}) if r['layout'] < MAIN[12]] + \
               [r for r in grid_rows({'prose': 'optimal', 'table': 'optimal'}) if r['layout'] >= MAIN[12]]
        p = analyze.analyze(rows)['primary']; values = [-0.15] * 12 + [0.0] * 12
        mean = sum(values) / 24; sd = (sum((v - mean) ** 2 for v in values) / 23) ** 0.5; se = sd / 24 ** 0.5
        self.assertAlmostEqual(p['estimate'], mean); self.assertAlmostEqual(p['standard_error'], se)
        self.assertAlmostEqual(p['interval95'][0], mean - 2.0687 * se); self.assertAlmostEqual(p['interval95'][1], mean + 2.0687 * se)
        self.assertEqual((p['negative'], p['zero'], p['positive']), (12, 12, 0))
        self.assertAlmostEqual(p['range'][0], -0.15); self.assertAlmostEqual(p['leave_one_out_range'][0], (sum(values) - 0) / 23)
        self.assertAlmostEqual(p['bounds_all_assigned'][0], mean); self.assertAlmostEqual(p['bounds_all_assigned'][1], mean)
        self.assertAlmostEqual(p['largest_possible'], 3.85 / 12)

    def test_every_stratum_and_cell_is_reported(self):
        a = analyze.analyze(grid_rows({'prose': 'always_first', 'table': 'always_second'}))
        self.assertEqual(len(a['strata']), 12); self.assertEqual(len(a['cells']), 24); self.assertEqual(len(a['layouts']), 24)
        for c in a['cells']: self.assertEqual((c['assigned'], c['valid'], c['check'] + c['explore']), (24, 24, 24))
        for s in a['strata']:
            self.assertEqual(s['pairs'], 24); self.assertEqual(s['prose']['optimal'] + s['table']['optimal'], 24)   # each layout: one format right
            self.assertAlmostEqual(s['table_minus_prose'], 0.0)
        self.assertEqual(a['representations']['prose']['first_listed_share'], 1.0); self.assertEqual(a['representations']['table']['first_listed_share'], 0.0)
        self.assertAlmostEqual(a['comparators']['always_check'], 0.15)

    def test_missing_outcomes_are_bounded_not_dropped(self):
        rows = grid_rows({'prose': 'always_check', 'table': 'optimal'})
        victim = next(r for r in rows if r['layout'] == MAIN[3] and r['representation'] == 'table' and (r['error'], r['unknown_cost']) == (0.05, 0.75))
        victim.update(status='failed', failure='http_500', accounting={'attempted': True, 'http_status': 500, 'error_body': '{"error":"x"}', 'request_id': 'req_9'})
        victim.pop('answer'); victim.pop('evaluation')
        gone = next(r for r in rows if r['layout'] == MAIN[7] and r['representation'] == 'prose' and (r['error'], r['unknown_cost']) == (0.8, 0.1))
        gone.update(status='not_started', stop='provider_credit_balance_low'); gone.pop('answer'); gone.pop('evaluation')
        a = analyze.analyze(rows); p = a['primary']
        self.assertEqual((p['layouts'], p['assigned_layouts']), (22, 24)); self.assertAlmostEqual(p['estimate'], -0.15)
        lo, hi = p['bounds_all_assigned']
        # layout 3: table regret unknown in [0, 0.70], prose (always check) 0.70 there; layout 7: prose unknown in [0, 0.70], table 0
        self.assertAlmostEqual(lo, (22 * -0.15 + (-0.15) + (-0.15 - 0.70 / 12)) / 24); self.assertAlmostEqual(hi, (22 * -0.15 + (-0.15 + 0.70 / 12) + (-0.15)) / 24)
        self.assertLessEqual(lo, p['estimate']); self.assertGreaterEqual(hi, p['estimate'])
        cell = next(c for c in a['cells'] if (c['error'], c['unknown_cost'], c['representation']) == (0.05, 0.75, 'table'))
        self.assertEqual((cell['assigned'], cell['valid'], cell['failed']), (24, 23, 1)); self.assertAlmostEqual(cell['regret_bounds'][1], 0.70 / 24)
        self.assertEqual(a['units'], {'assigned': 576, 'valid': 574, 'failed': 1, 'not_started': 1})
        incomplete = [x for x in a['layouts'] if not x['complete']]
        self.assertEqual([x['layout'] for x in incomplete], [MAIN[3], MAIN[7]]); self.assertTrue(all(x['value'] is None for x in incomplete))
        f = a['failures']
        self.assertEqual((f['units_without_a_valid_answer'], f['failed'], f['not_started']), (2, 1, 1))
        self.assertEqual(f['by_category'], {'http_500': 1, 'provider_credit_balance_low': 1})
        unit = next(u for u in f['units'] if u['status'] == 'failed')
        self.assertEqual((unit['http_status'], unit['error_body'], unit['request_id'], unit['error']), (500, '{"error":"x"}', 'req_9', 0.05))

    def test_reliable_source_regression_is_flagged(self):
        rows = grid_rows({'prose': 'optimal', 'table': 'optimal'})
        def spoil(case, n):
            hit = 0
            for r in rows:
                if r['representation'] == 'table' and (r['error'], r['unknown_cost']) == case and hit < n:
                    wrong = next(c for c in r['legal_cells'] if c != r['answer']['inspect'])
                    r.update(answer={'inspect': wrong}, evaluation=study.evaluate(r, wrong)); hit += 1
        spoil((0.2, 0.25), 3); spoil((0.05, 0.1), 2); spoil((0.8, 0.25), 9)
        a = analyze.analyze(rows); rs = a['reliable_source']
        self.assertEqual(rs['strata'], 6); self.assertEqual(rs['worst_optimal_table_minus_prose'], -3)
        self.assertEqual(rs['flagged'], [{'error': 0.2, 'unknown_cost': 0.25, 'optimal_table_minus_prose': -3}])
        self.assertFalse(next(s for s in a['strata'] if (s['error'], s['unknown_cost']) == (0.8, 0.25))['regression'])   # not a reliable source
        self.assertGreater(a['primary']['estimate'], 0)

    def test_combine_replaces_only_units_left_not_started(self):
        base = rows_for('S1')[:3]; base[1] = dict(base[1], status='not_started'); base[2] = dict(base[2], status='failed')
        later = [dict(r, batch='s1-001-r1', status='completed') for r in rows_for('S1')[:3]]
        final = study.combine(base + later)
        self.assertEqual([r.get('batch') for r in final], [None, 's1-001-r1', None]); self.assertEqual([r['status'] for r in final], ['completed', 'completed', 'failed'])
        self.assertEqual(worker.unanswered_reservations([dict(base[1], accounting={'attempted': True}), dict(base[1], accounting={'attempted': False}), base[0]]), 1)

    def test_frames_for_empty_partial_failed_and_final_states(self):
        rows = grid_rows({'prose': 'always_check', 'table': 'optimal'})
        rows[5].update(status='failed', failure='timeout', accounting={}); rows[5].pop('answer'); rows[5].pop('evaluation')
        for sample in ([], rows[:40], rows, rows_for('S0'), rows_for('Q0')):
            im = render.frame(sample, 576, 'S1', 12.0, {'committed_usd': 0.01, 'cap_usd': 2})
            self.assertEqual(im.size, (1800, 1200)); self.assertGreater(len(set(im.resize((90, 60)).getdata())), 3)
        with tempfile.TemporaryDirectory() as td:
            n = render.replay(rows[:60], 576, Path(td), 'S1')
            with Image.open(Path(td) / 'replay.gif') as gif:
                self.assertEqual(gif.n_frames, n); self.assertEqual(gif.size, (900, 600))
            self.assertLess((Path(td) / 'replay.gif').stat().st_size, 2_000_000)


class Stage(Env):
    def test_offline_scripted_stage_writes_every_artifact_and_reports_the_calibration(self):
        run = FakeRun('x/s0', study.params('S0'))
        summary, reason, rows, out = self.stage('S0', None, run)
        self.assertIsNone(reason); self.assertTrue(summary['passed']); self.assertEqual((summary['planned'], summary['graded'], summary['model_calls']), (144, 144, 0))
        self.assertEqual(summary['invariant_violations'], []); self.assertEqual(summary['qualification_passed'], 1)
        self.assertAlmostEqual(summary['calibration']['mean_regret']['always_explore'], 2.05 / 12)
        self.assertEqual(sorted(run.artifacts), sorted(worker.ARTIFACTS)); self.assertEqual(run.final[0], 'done')
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd', 'qualification_passed'): self.assertIn(key, run.final[1])
        with Image.open(out / 'final_frame.png') as im: self.assertEqual(im.size, (1800, 1200))
        self.assertFalse(Path(os.environ[provider.LEDGER_ENV]).exists())                 # a scripted stage opens no ledger

    def test_a_broken_instrument_fails_the_scripted_stage(self):
        with patch.object(analyze, 'discrimination', lambda kind='engineering': ['analytic_policy_must_have_zero_regret']):
            summary, reason, rows, out = self.stage('S0', None)
        self.assertEqual(reason, 'invariant_violations')

    def test_probe_makes_exactly_one_call_and_measures_tokens_per_byte(self):
        stub = rehearse.Stub('optimal'); run = FakeRun('x/p0', study.params('P0'))
        summary, reason, rows, out = self.stage('P0', stub, run)
        self.assertIsNone(reason); self.assertEqual((stub.requests, summary['model_calls'], summary['qualification_passed']), (1, 1, 1))
        a = study.assignments('P0')[0]; self.assertAlmostEqual(summary['probe']['tokens_per_byte'], (a['content_bytes'] // 3) / a['content_bytes'])
        self.assertAlmostEqual(run.final[1]['probe_tokens_per_byte'], summary['probe']['tokens_per_byte'])
        probe = summary['probe']       # the raw response metadata of the one call is in the summary
        self.assertEqual((probe['response_model'], probe['response_provider'], probe['response_id'], probe['finish_reason'], probe['reasoning_tokens']),
                         (D['canonical_model'], 'Alibaba', 'gen-rehearsal', 'stop', 0))
        self.assertIsNotNone(probe['latency_seconds']); self.assertIn('provider_reported_usd', probe); self.assertGreater(probe['reserved_usd'], 8 * probe['actual_usd'])
        acc = rows[0]['accounting']
        self.assertEqual((acc['finish_reason'], acc['reasoning_tokens'], acc['response_provider'], acc['response_model']), ('stop', 0, 'Alibaba', D['canonical_model']))
        self.assertEqual(self.ledger()['calls_by_stage'], {'P0': 1})

    def test_probe_fails_on_a_bad_interface(self):
        def reasoning(n, payload): payload['usage']['completion_tokens_details']['reasoning_tokens'] = 40; return payload
        def other_model(n, payload): payload['model'] = 'qwen/qwen3.7-plus'; return payload
        def other_provider(n, payload): payload['provider'] = 'DeepInfra'; return payload
        def cut(n, payload): payload['choices'][0]['finish_reason'] = 'length'; return payload
        def prose(n, payload): payload['choices'][0]['message']['content'] = 'I would inspect 3,3.'; return payload
        def no_usage(n, payload): payload['usage'] = {}; return payload
        for mutate, category in ((reasoning, 'unexpected_reasoning_tokens'), (other_model, 'model_mismatch'), (other_provider, 'provider_mismatch'),
                                 (cut, 'truncated_output'), (prose, 'invalid_json'), (no_usage, 'missing_usage')):
            with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {provider.LEDGER_ENV: str(Path(td) / 'l.jsonl')}):
                run = FakeRun('x/p0', study.params('P0'))
                summary, reason, rows, out = self.stage('P0', rehearse.Stub('optimal', mutate=mutate), run)
            self.assertIsNotNone(reason, category); self.assertEqual(rows[0]['failure'], category); self.assertEqual(rows[0]['status'], 'failed')
            self.assertEqual(run.final[0], 'fail'); self.assertEqual(run.final[1]['qualification_passed'], 0); self.assertEqual(run.final[1]['invalid'], 1)
        # the adapter accepts a response that names no provider; the probe gate does not
        def unnamed(n, payload): payload.pop('provider'); return payload
        run = FakeRun('x/p0', study.params('P0'))
        with patch.dict(os.environ, {provider.LEDGER_ENV: str(self.dir / 'unnamed.jsonl')}):
            summary, reason, rows, out = self.stage('P0', rehearse.Stub('optimal', mutate=unnamed), run)
        self.assertEqual(reason, 'gate_failed'); self.assertEqual(rows[0]['status'], 'completed')
        self.assertEqual((run.final[0], run.final[1]['qualification_passed'], run.final[1]['invalid']), ('fail', 0, 0))

    def test_strict_stage_stops_at_the_first_failed_call_and_every_unit_is_recorded(self):
        stub = rehearse.Stub('optimal', fail_messages={3}); run = FakeRun('x/q0', study.params('Q0'))
        summary, reason, rows, out = self.stage('Q0', stub, run)
        self.assertEqual(reason, 'invalid_rows'); self.assertEqual(len(rows), 23)
        statuses = [r['status'] for r in rows]
        self.assertEqual(statuses.count('failed'), 1); self.assertGreaterEqual(statuses.count('not_started'), 23 - 3 - B['workers'])
        self.assertLessEqual(stub.requests, 3 + B['workers'])
        self.assertEqual(run.final[0], 'fail'); self.assertEqual(run.final[1]['qualification_passed'], 0)
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, run.final[1])
        self.assertEqual(run.final[1]['episodes'], 23); self.assertEqual(run.final[1]['invalid'], 23 - statuses.count('completed'))

    def test_qualification_gate_uses_all_24_rows_and_a_failed_gate_reports_the_misses(self):
        summary, reason, rows, out = self.stage('Q0', rehearse.Stub('optimal'))
        self.assertIsNone(reason); q = summary['qualification']; self.assertEqual((q['assigned'], q['valid'], q['prose']['optimal'], q['table']['optimal']), (24, 24, 12, 12))
        summary, reason, rows, out = self.stage('Q0', rehearse.Stub('optimal'), fresh_ledger=True, probe_rows=None)
        self.assertEqual(reason, 'probe_row_unavailable')
        run = FakeRun('x/q0', study.params('Q0'))
        summary, reason, rows, out = self.stage('Q0', rehearse.Stub('always_first'), run, fresh_ledger=True, probe_rows=probe_row())
        self.assertEqual(reason, 'gate_failed'); self.assertEqual(run.final[1]['invalid'], 0); self.assertEqual(run.final[1]['qualification_passed'], 0)
        report = json.loads((out / 'failures.json').read_text())
        self.assertEqual(len(report['qualification_misses']), 12)          # always-first is wrong in 6 of 12 fixtures per representation
        miss = report['qualification_misses'][0]
        self.assertIn('CONSEQUENCES', miss['user']); self.assertIn(miss['answer']['inspect'], miss['user']); self.assertNotEqual(miss['answer']['inspect'], miss['optimal_cell'])

    def test_main_stage_continues_after_failed_calls_and_keeps_their_evidence(self):
        def bad(n, payload):
            if n == 5: payload['choices'][0]['message']['content'] = json.dumps({'inspect': '9,9'})
            if n == 9: payload['choices'][0]['message']['content'] = json.dumps({'inspect': study.assignments('S1')[8]['legal_cells'][0], 'why': 'x'})
            if n == 11: payload['choices'][0]['message']['content'] = 'not json'
            return payload
        stub = rehearse.Stub('optimal', fail_messages={20}, mutate=bad); run = FakeRun('x/s1', study.params('S1'))
        summary, reason, rows, out = self.stage('S1', stub, run)
        self.assertIsNone(reason); self.assertTrue(summary['passed']); self.assertEqual((summary['failed'], summary['graded'], summary['not_started']), (4, 572, 0))
        self.assertEqual(stub.requests, 576)                                        # no answer and no HTTP 500 was re-sent
        failed = {r['failure']: r for r in rows if r['status'] == 'failed'}
        self.assertEqual(sorted(failed), ['http_500', 'invalid_answer', 'invalid_json'])
        self.assertEqual((failed['http_500']['accounting']['http_status'], failed['http_500']['accounting']['request_id']), (500, 'req_rehearsal'))
        self.assertIn('rehearsal injected failure', failed['http_500']['accounting']['error_body'])
        self.assertEqual(failed['invalid_json']['accounting']['answer_text'], 'not json'); self.assertTrue(failed['invalid_json']['accounting']['usage_reported'])
        self.assertNotIn(TEST_KEY, (out / 'episodes.jsonl').read_text()); self.assertNotIn('Bearer', (out / 'episodes.jsonl').read_text())
        self.assertNotIn(TEST_KEY, Path(os.environ[provider.LEDGER_ENV]).read_text())
        self.assertEqual(run.final[0], 'done'); self.assertEqual((run.final[1]['failed'], run.final[1]['invalid'], run.final[1]['episodes']), (4, 4, 576))
        self.assertIn('4 failed (limit 6)', run.message)
        analysis = json.loads((out / 'analysis.json').read_text())
        self.assertEqual(analysis['failures']['by_category'], {'http_500': 1, 'invalid_answer': 2, 'invalid_json': 1})
        self.assertLess(analysis['primary']['layouts'], 24); self.assertEqual(analysis['primary']['assigned_layouts'], 24)
        self.assertLessEqual(analysis['primary']['bounds_all_assigned'][0], 0); self.assertGreaterEqual(analysis['primary']['bounds_all_assigned'][1], 0)
        self.assertEqual(self.ledger()['calls_by_stage'], {'S1': 576}); self.assertEqual(self.ledger()['usage_reported_calls'], 575)

    def test_main_stage_stops_when_failed_units_exceed_the_limit(self):
        stub = rehearse.Stub('optimal', fail_from=30); run = FakeRun('x/s1', study.params('S1'))
        summary, reason, rows, out = self.stage('S1', stub, run)
        self.assertEqual(reason, 'failed_units_over_limit')
        failed = sum(r['status'] == 'failed' for r in rows); self.assertTrue(B['max_failed'] < failed <= B['max_failed'] + B['workers'])
        self.assertEqual(sum(r['status'] == 'completed' for r in rows), 29); self.assertEqual(sum(r['status'] == 'not_started' for r in rows), 576 - 29 - failed)
        self.assertEqual(run.final[0], 'fail'); self.assertEqual(run.final[1]['failed'], failed)
        self.assertFalse(json.loads((out / 'summary.json').read_text())['resumable'])

    def test_integrity_failures_stop_the_main_stage_at_once(self):
        def other_model(n, payload):
            if n == 10: payload['model'] = 'qwen/qwen3.7-plus'
            return payload
        summary, reason, rows, out = self.stage('S1', rehearse.Stub('optimal', mutate=other_model))
        self.assertEqual(reason, 'integrity_failure'); self.assertEqual([r['failure'] for r in rows if r['status'] == 'failed'], ['model_mismatch'])
        self.assertGreaterEqual(sum(r['status'] == 'not_started' for r in rows), 576 - 10 - B['workers'])
        tight = copy.deepcopy(B); tight['aggregate_usd'] = 0.001
        with patch.dict(os.environ, {provider.LEDGER_ENV: str(self.dir / 'small.jsonl')}), patch.object(worker, 'ledger_budget', lambda budget, stage, reissued: tight):
            summary, reason, rows, out = self.stage('S1', rehearse.Stub('optimal'))
        self.assertEqual(reason, 'integrity_failure'); self.assertEqual({r['failure'] for r in rows if r['status'] == 'failed'}, {'aggregate_budget_exhausted'})
        self.assertGreater(sum(r['status'] == 'not_started' for r in rows), 400)
        with patch.dict(os.environ, {provider.LEDGER_ENV: str(self.dir / 'late.jsonl')}):
            summary, reason, rows, out = self.stage('S1', rehearse.Stub('optimal'), deadline=worker.time.monotonic() - 1)
        self.assertEqual(reason, 'integrity_failure'); self.assertIn('stage_deadline', {r.get('failure') for r in rows})

    def test_short_billing_outage_is_a_pause_and_a_long_one_stops_without_failing_anything(self):
        stub = rehearse.Stub('optimal', credit_first=3); run = FakeRun('x/p0', study.params('P0'))
        summary, reason, rows, out = self.stage('P0', stub, run)
        self.assertIsNone(reason); self.assertEqual((summary['billing_pauses'], summary['billing_affected_calls'], summary['failed']), (1, 1, 0))
        self.assertTrue(180 <= summary['billing_pause_seconds'] < 185); self.assertEqual(self.clock.waits, [60, 60, 60])
        self.assertEqual(rows[0]['accounting']['attempts'], 4); self.assertEqual(run.final[1]['billing_pauses'], 1)
        self.assertEqual(self.ledger()['transport_attempts'], 4); self.assertEqual(self.ledger()['attempted_calls'], 1)
        # an outage that outlasts 1,200 s in the main stage
        self.clock.waits.clear(); run = FakeRun('x/s1', study.params('S1'))
        summary, reason, rows, out = self.stage('S1', rehearse.Stub('optimal', credit_from=11), run)
        self.assertEqual(reason, provider.BILLING_STOP); saved = json.loads((out / 'summary.json').read_text())
        self.assertEqual((saved['failed'], saved['graded'], saved['not_started'], saved['resumable']), (0, 10, 566, True))
        self.assertEqual(sum(self.clock.waits), 1200); self.assertTrue(1200 <= saved['billing_pause_seconds'] < 1205)
        self.assertTrue(1 <= saved['unanswered_reservations'] <= B['workers'])
        self.assertTrue(all(r.get('stop') == provider.BILLING_STOP for r in rows if r['status'] == 'not_started'))
        self.assertEqual(run.final[0], 'fail'); self.assertEqual((run.final[1]['failed'], run.final[1]['billing_pauses']), (0, 1))
        self.assertIn(provider.BILLING_STOP, run.message)
        owner = next(r for r in rows if (r.get('accounting') or {}).get('attempts', 0) > 2)
        self.assertEqual(owner['accounting']['http_status'], 402); self.assertIn('Insufficient credits', owner['accounting']['error_body'])
        # the continuation holds exactly the units left not started; the caps rise only by the unanswered reservations
        units = [r['id'] for r in rows if r['status'] == 'not_started']
        p = dict(study.params('S1'), batch='s1-001-r1', continuation=1); self.n += 1; out2 = self.dir / 'continuation'
        cont = worker.execute(p, out2, opener=rehearse.Stub('optimal'), units=units, prior_rows=rows)
        self.assertTrue(cont['passed']); self.assertEqual((cont['planned'], cont['graded'], cont['stage_units']['completed']), (566, 566, 576))
        ledger = self.ledger()
        self.assertEqual(ledger['calls_by_stage']['S1'], 576 + saved['unanswered_reservations']); self.assertEqual(ledger['usage_reported_calls'], 577)
        again = [r['id'] for r in chain.read_jsonl(out2 / chain.ROWS)]
        self.assertEqual(sorted(again), sorted(units)); self.assertFalse(set(again) & {r['id'] for r in rows if r['status'] == 'completed'})

    def test_continuation_cap_is_raised_only_by_unanswered_reservations(self):
        self.assertIs(worker.ledger_budget(B, 'S1', 0), B)
        raised = worker.ledger_budget(B, 'S1', 3)
        self.assertEqual((raised['max_calls']['S1'], raised['max_attempted_calls'], raised['aggregate_usd'], raised['max_transport_attempts']),
                         (579, 603, B['aggregate_usd'], B['max_transport_attempts']))
        self.assertEqual(B['max_calls']['S1'], 576)
        # without the raise, the continuation of a full stage could not reserve its last calls
        ledger = provider.Ledger(self.dir / 'cap.jsonl', B)
        for i in range(576): ledger.transact({'type': 'reserve', 'call_id': f's1-001:{i}', 'micro_usd': 1})
        with self.assertRaises(provider.CallFailure) as cm: ledger.transact({'type': 'reserve', 'call_id': 's1-001-r1:x', 'micro_usd': 1})
        self.assertEqual(cm.exception.category, 'stage_call_cap_reached')
        provider.Ledger(self.dir / 'cap.jsonl', worker.ledger_budget(B, 'S1', 1)).transact({'type': 'reserve', 'call_id': 's1-001-r1:x', 'micro_usd': 1})

    def test_stage_refuses_a_stale_source_hash_a_wrong_batch_or_unknown_units(self):
        for change, kw in ((dict(source_hash='0' * 64), {}), (dict(batch='s1-002'), {}), (dict(backend='scripted'), {}), ({}, dict(units=['nope'], prior_rows=[]))):
            run = FakeRun('x/s1', study.params('S1')); self.n += 1
            with self.assertRaises(AssertionError):
                worker.execute(dict(study.params('S1'), **change), self.dir / f'refused-{self.n}', run, opener=rehearse.Stub('optimal'), **kw)
            self.assertEqual(run.final[0], 'fail')
            for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, run.final[1])
            self.assertGreaterEqual(run.final[1]['invalid'], 1)
        with patch.dict(os.environ, {provider.KEY_ENV: ''}):
            with self.assertRaises(provider.CallFailure): worker.execute(study.params('P0'), self.dir / 'nokey', opener=rehearse.Stub('optimal'))

    def test_a_structural_violation_blocks_every_call_of_a_paid_stage(self):
        stub = rehearse.Stub('optimal')
        with patch.object(study, 'check_invariants', lambda stage: ['x:both_actions_must_be_legal']):
            summary, reason, rows, out = self.stage('S1', stub)
        self.assertEqual(reason, 'invariant_violations'); self.assertEqual(stub.requests, 0); self.assertTrue(all(r['status'] == 'not_started' for r in rows))


class Chain(Env):
    def test_coordinator_gates(self):
        hub = FakeHub()
        self.assertEqual(coordinator.check(hub, 'S0')[1], None)
        for stage, before in (('P0', 'S0'), ('Q0', 'P0'), ('S1', 'Q0')):
            hub = FakeHub()
            with self.assertRaises(coordinator.GateRefused): coordinator.check(hub, stage)
            for kw in (dict(status='failed'), dict(invalid=1), dict(passed=0), dict(source_hash='0' * 64), dict(status='running')):
                hub = FakeHub(); hub.add(before, **kw)
                with self.assertRaises(coordinator.GateRefused): coordinator.check(hub, stage)
            hub = FakeHub(); hub.add(before); self.assertEqual(coordinator.check(hub, stage)[1]['params']['stage'], before)
            hub.add(before)
            with self.assertRaises(coordinator.GateRefused) as cm: coordinator.check(hub, stage)        # exactly one
            self.assertEqual(str(cm.exception), 'exact_runtime_qualification_required')
            hub = FakeHub(); hub.add(before); hub.add(stage, status='failed')
            with self.assertRaises(coordinator.GateRefused) as cm: coordinator.check(hub, stage)        # no replay of a batch
            self.assertEqual(str(cm.exception), 'batch_exists_no_replay')
        hub = FakeHub(); hub.add('Q0')
        with self.assertRaises(coordinator.GateRefused): coordinator.check_continuation(hub, 1)         # no stopped S1
        hub.add('S1', status='failed'); self.assertEqual(coordinator.check_continuation(hub, 1)[0]['batch'], 's1-001-r1')
        with self.assertRaises(coordinator.GateRefused): coordinator.check_continuation(hub, 2)
        ids = coordinator.enqueue_continuation(hub, 1); self.assertEqual(hub.rows[-1]['params']['continuation'], 1); self.assertEqual(len(ids), 1)
        with self.assertRaises(coordinator.GateRefused): coordinator.check_continuation(hub, 1)

    def run_chain(self, stub, stages=None, hub=None):
        hub = hub or FakeHub()
        with patch('sys.stdout', io.StringIO()) as out: code = chain.run_chain(stages or list(study.STAGES), sr=hub, opener=stub)
        return code, hub, json.loads(out.getvalue().strip().splitlines()[-1])

    def verify(self, hub):
        with patch('sys.stdout', io.StringIO()) as out: code = chain.verify(hub)
        lines = out.getvalue().strip().splitlines(); self.assertEqual(len(lines), 1)
        return code, json.loads(lines[0])

    def test_chain_runs_all_stages_writes_status_and_verifies(self):
        code, hub, last = self.run_chain(rehearse.Stub('optimal'))
        self.assertEqual(code, 0); self.assertEqual(last, {'state': 'completed', 'stages': list(study.STAGES)})
        status = chain.read_status()
        self.assertEqual((status['state'], status['all_stages_done'], status['source_hash']), ('completed', True, study.source_hash()))
        self.assertEqual({s: (e['status'], e['calls'], e['valid']) for s, e in status['stages'].items()},
                         {'S0': ('done', 0, 144), 'P0': ('done', 1, 1), 'Q0': ('done', 23, 23), 'S1': ('done', 576, 576)})
        self.assertEqual([(r['params']['batch'], r['status']) for r in hub.rows], [('s0-001', 'done'), ('p0-001', 'done'), ('q0-001', 'done'), ('s1-001', 'done')])
        self.assertEqual(status['ledger']['attempted_calls'], 600); self.assertLess(status['ledger']['committed_usd'], 0.05)
        projection = status['stages']['S1']['projection']
        self.assertTrue(projection['within_cap'] and projection['input_ceiling_ok']); self.assertLess(projection['projected_input_tokens'], 8000)
        self.assertFalse(list(chain.status_path().parent.glob('.chain-status-*')))                 # atomic replace left no temporary file
        code, report = self.verify(hub); self.assertEqual(code, 0, report); self.assertTrue(report['ok'])
        self.assertEqual(report['manifest_digest'], manifest.load()['digest'])
        self.assertEqual(report['stages']['S1']['units']['primary_estimate'], 0.0); self.assertTrue(report['stages']['S1']['units']['every_unit_exactly_once'])
        with patch('sys.stdout', io.StringIO()) as out: self.assertEqual(chain.show_status(), 0)
        shown = json.loads(out.getvalue().strip().splitlines()[-1]); self.assertEqual(shown['chain']['state'], 'completed'); self.assertEqual(shown['ledger']['attempted_calls'], 600)
        # verify detects a changed saved answer
        s1 = Path(status['stages']['S1']['directory']); rows = chain.read_jsonl(s1 / chain.ROWS)
        other = next(c for c in rows[0]['legal_cells'] if c != rows[0]['answer']['inspect']); rows[0]['answer'] = {'inspect': other}
        with gzip.open(s1 / chain.ROWS, 'wt') as f:
            for r in rows: f.write(json.dumps(r, sort_keys=True) + '\n')
        code, report = self.verify(hub); self.assertEqual(code, 1)
        self.assertFalse(report['stages']['S1']['checks']['artifact_checksums']); self.assertFalse(report['stages']['S1']['checks']['answers_regraded'])
        # a second chain at the same source hash is refused: no batch is replayed
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), hub=hub)
        self.assertEqual((code, last['reason']), (3, 'batch_exists_no_replay'))

    def test_chain_stops_at_a_failed_qualification_and_queues_nothing_further(self):
        stub = rehearse.Stub('always_first'); code, hub, last = self.run_chain(stub)
        self.assertEqual(code, 3); self.assertEqual(last, {'state': 'stopped_at_gate', 'stage': 'Q0', 'reason': 'gate_failed'})
        self.assertEqual([(r['params']['batch'], r['status']) for r in hub.rows], [('s0-001', 'done'), ('p0-001', 'done'), ('q0-001', 'failed')])
        self.assertEqual(stub.requests, 24); status = chain.read_status()
        self.assertEqual((status['state'], status['stopped_stage'], status['reason']), ('stopped_at_gate', 'Q0', 'gate_failed')); self.assertNotIn('S1', status['stages'])
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S1'], hub)
        self.assertEqual((code, last['reason']), (3, 'exact_runtime_qualification_required')); self.assertEqual(len(hub.rows), 3)
        with patch('sys.stdout', io.StringIO()) as out: self.assertEqual(chain.resume(sr=hub, opener=rehearse.Stub('optimal')), 3)
        self.assertEqual(json.loads(out.getvalue())['state'], 'resume_refused')

    def test_chain_in_parts_and_the_two_projection_gates_before_s1(self):
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S0', 'P0'])
        self.assertEqual(code, 0)
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['Q0'], hub); self.assertEqual(code, 0)      # Q0 finds P0's row by the hub run and its checksum
        honest = copy.deepcopy(hub.rows)
        hub.row('p0-001')['metrics']['probe_tokens_per_byte'] = 5.0
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S1'], hub)
        self.assertEqual((code, last['reason']), (3, 'input_ceiling_projection')); self.assertEqual(len(hub.rows), 3)
        self.assertGreater(chain.read_status()['stages']['S1']['projection']['projected_input_tokens'], 8000)
        hub.rows = copy.deepcopy(honest); hub.row('q0-001')['metrics']['cost_usd'] = 0.09          # USD 0.0039 per call x 576 = USD 2.25
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S1'], hub)
        self.assertEqual((code, last['reason']), (3, 'projection_exceeds_cap')); self.assertEqual(len(hub.rows), 3)
        hub.rows = copy.deepcopy(honest); del hub.row('q0-001')['metrics']['cost_usd']
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S1'], hub); self.assertEqual((code, last['reason']), (3, 'projection_exceeds_cap'))
        hub.rows = copy.deepcopy(honest)
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S1'], hub); self.assertEqual(code, 0)
        self.assertEqual(self.verify(hub)[0], 0)

    def test_q0_is_refused_when_the_probe_row_does_not_match_the_hub(self):
        code, hub, last = self.run_chain(rehearse.Stub('optimal'), ['S0', 'P0'])
        path = Path(chain.read_status()['stages']['P0']['directory']) / chain.ROWS
        rows = chain.read_jsonl(path); rows[0]['answer'] = {'inspect': rows[0]['legal_cells'][1]}
        with gzip.open(path, 'wt') as f: f.write(json.dumps(rows[0]) + '\n')
        stub = rehearse.Stub('optimal'); code, hub, last = self.run_chain(stub, ['Q0'], hub)
        self.assertEqual((code, last['reason'], stub.requests), (3, 'probe_row_unavailable', 0)); self.assertEqual(len(hub.rows), 2)

    def test_billing_stop_then_resume_counts_every_unit_once(self):
        code, hub, last = self.run_chain(rehearse.Stub('optimal', credit_from=2 + 23 + 100))
        self.assertEqual(code, 3); self.assertEqual(last, {'state': 'stopped_at_gate', 'stage': 'S1', 'reason': provider.BILLING_STOP})
        first = chain.read_status()['stages']['S1']
        self.assertEqual((first['status'], first['failed'], first['valid'], first['resumable']), ('failed', 0, 100, True))
        with patch('sys.stdout', io.StringIO()): self.assertEqual(chain.resume(sr=hub, opener=rehearse.Stub('optimal', credit_from=201)), 3)   # a second outage
        with patch('sys.stdout', io.StringIO()) as out: self.assertEqual(chain.resume(sr=hub, opener=rehearse.Stub('optimal')), 0)
        self.assertEqual(json.loads(out.getvalue().strip().splitlines()[-1])['continuation'], 's1-001-r2')
        status = chain.read_status(); s1 = status['stages']['S1']
        self.assertEqual((status['state'], s1['status'], s1['completed_by'], len(s1['continuations'])), ('completed', 'done', 's1-001-r2', 2))
        self.assertEqual([(r['params']['batch'], r['status']) for r in hub.rows][3:], [('s1-001', 'failed'), ('s1-001-r1', 'failed'), ('s1-001-r2', 'done')])
        code, report = self.verify(hub); self.assertEqual(code, 0, report)
        u = report['stages']['S1']['units']
        self.assertEqual((u['assigned'], u['completed'], u['failed'], u['not_started'], u['answered_calls']), (576, 576, 0, 0, 576))
        self.assertTrue(u['every_unit_exactly_once'] and u['no_unit_answered_twice'])
        orphans = sum(e['unanswered_reservations'] for e in [s1] + s1['continuations'])
        self.assertEqual(status['ledger']['calls_by_stage']['S1'], 576 + orphans); self.assertEqual(status['ledger']['usage_reported_calls'], 600)
        self.assertLessEqual(status['ledger']['transport_attempts'], B['max_transport_attempts'])
        with patch('sys.stdout', io.StringIO()) as out: self.assertEqual(chain.resume(sr=hub, opener=rehearse.Stub('optimal')), 3)
        self.assertEqual(json.loads(out.getvalue())['reason'], 'last_stop_was_not_a_billing_stop_of_S1')

    def test_chain_status_of_another_source_version_is_set_aside(self):
        chain.write_status({'experiment': study.EXPERIMENT, 'source_hash': 'f' * 64, 'stages': {'S0': {'status': 'done'}}, 'state': 'completed'})
        code, hub, last = self.run_chain(None, ['S0'])
        self.assertEqual(code, 0); self.assertTrue((chain.status_path().parent / 'chain-status-ffffffffffff.json').exists())
        self.assertEqual(chain.read_status()['source_hash'], study.source_hash())

    def test_stage_lists_must_be_ordered_and_contiguous(self):
        self.assertEqual(chain.parse_stages('S0,P0,Q0,S1'), ['S0', 'P0', 'Q0', 'S1']); self.assertEqual(chain.parse_stages('p0, q0'), ['P0', 'Q0'])
        for bad in ('S0,Q0', 'P0,S0', 'S2', '', 'S0,S0'):
            with self.assertRaises(SystemExit): chain.parse_stages(bad)

    def test_verify_fails_without_a_chain_and_an_internal_error_still_closes_the_run(self):
        code, report = self.verify(FakeHub()); self.assertEqual(code, 1); self.assertFalse(report['ok'])
        hub = FakeHub()
        with patch.object(worker.study, 'check_invariants', side_effect=RuntimeError('boom')):
            with patch('sys.stdout', io.StringIO()) as out: code = chain.run_chain(['S0'], sr=hub, opener=None)
        self.assertEqual(code, chain.EXIT_INTERNAL); self.assertEqual(json.loads(out.getvalue())['reason'], 'internal_RuntimeError')
        self.assertEqual(hub.rows[0]['status'], 'failed')
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, hub.rows[0]['metrics'])

    def test_rehearsal_refuses_a_hub_that_is_not_local(self):
        self.assertEqual(rehearse.require_local('http://127.0.0.1:8123'), 'http://127.0.0.1:8123')
        for url in ('http://localhost:8123', 'https://hub.example.org', 'http://10.0.0.5:8000', '', None, 'http://127.0.0.1.example.org'):
            with self.assertRaises(SystemExit): rehearse.require_local(url)
        with self.assertRaises(AssertionError):
            rehearse.Stub('optimal')(urllib.request.Request('https://example.org/v1', data=b'{}'))
        with self.assertRaises(urllib.error.HTTPError):          # a body with any key beyond the frozen template is rejected by the stub
            body = dict(D['request_template'], messages=[{'role': 'system', 'content': 's'}, {'role': 'user', 'content': 'u'}], temperature=0)
            rehearse.Stub('optimal')(urllib.request.Request(provider.URL, data=json.dumps(body).encode()))


# ---------------------------------------------------------------------------------------------------
# The reference adapter's tests, copied unchanged from
# researchers/dmarz/notes/pipeline/reference/test_openrouter_provider.py (`orp` is src/provider.py).
# ---------------------------------------------------------------------------------------------------
CONFIG = {
    'model': 'qwen/qwen3.7-flash',
    'canonical_model': 'qwen/qwen3.7-flash-20260727',
    'provider': 'alibaba',
    'request_template': {'model': 'qwen/qwen3.7-flash',
                         'provider': {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True},
                         'reasoning': {'enabled': False}, 'max_tokens': 1000,
                         'response_format': {'type': 'json_object'}},
    'budget': {'max_calls': {'S0': 0, 'P0': 1, 'Q0': 23, 'S1': 504}, 'max_attempted_calls': 528,
               'aggregate_usd': 2, 'max_output_tokens': 1000, 'max_input_tokens': 8000, 'max_input_bytes': 40000,
               'max_visible_chars': 4000, 'request_timeout_seconds': 120,
               'retry': {'transport_retries': 2, 'retryable_http_status': [429, 502, 503, 529],
                         'backoff_seconds': [2, 6], 'retry_after_cap_seconds': 20},
               'billing_outage': {'retry_every_seconds': 60, 'max_wait_seconds': 1200},
               'max_transport_attempts': 640,
               'input_usd_per_million': 0.03, 'output_usd_per_million': 0.13},
}
KEY = 'sk-or-test-SECRET-0123456789'


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def ok(content='{"answer": 7}', model='qwen/qwen3.7-flash-20260727', provider='Alibaba', finish='stop', usage=None, **extra):
    body = {'id': 'gen-1', 'model': model, 'provider': provider,
            'choices': [{'finish_reason': finish, 'message': {'role': 'assistant', 'content': content}}],
            'usage': usage if usage is not None else {'prompt_tokens': 900, 'completion_tokens': 12, 'total_tokens': 912}}
    body.update(extra)
    return body


def http(status, body='{"error":{"message":"x"}}', headers=None):
    return urllib.error.HTTPError(orp.URL, status, 'err', headers or {}, io.BytesIO(body.encode() if isinstance(body, str) else body))


class Clock:
    def __init__(self): self.t = 0.0; self.sleeps = []
    def now(self): return self.t
    def sleep(self, s): self.sleeps.append(s); self.t += s


def validate(obj):
    if not isinstance(obj, dict) or set(obj) != {'answer'} or type(obj['answer']) is not int:
        raise ValueError('schema')
    return obj


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {orp.KEY_ENV: KEY}); self.env.start()
        self.sent = []; self.clock = Clock()

    def tearDown(self):
        self.env.stop(); self.tmp.cleanup()

    def adapter(self, script, config=CONFIG):
        """script: list of responses in order; a dict is a 200 body, an exception is raised."""
        script = list(script)
        def opener(request, timeout):
            self.sent.append({'url': request.full_url, 'body': json.loads(request.data), 'timeout': timeout,
                              'headers': dict(request.header_items())})
            item = script.pop(0)
            if isinstance(item, BaseException): raise item
            return Resp(json.dumps(item).encode() if not isinstance(item, bytes) else item)
        self.ledger = orp.Ledger(Path(self.tmp.name) / 'ledger.jsonl', config['budget'])
        return orp.OpenRouter(self.ledger, config, opener, self.clock.now, self.clock.sleep)

    def failure(self, api, call_id='s1-001:a'):
        with self.assertRaises(orp.CallFailure) as cm:
            api.call('SYS', 'USER', call_id, validate)
        return cm.exception


class Request(Base):
    def test_body_is_exactly_the_template_plus_messages(self):
        api = self.adapter([ok()])
        answer, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7})
        body = self.sent[0]['body']
        self.assertEqual(tuple(body), orp.BODY_KEYS)
        self.assertEqual({k: body[k] for k in body if k != 'messages'}, CONFIG['request_template'])
        self.assertEqual(body['messages'], [{'role': 'system', 'content': 'SYS'}, {'role': 'user', 'content': 'USER'}])
        self.assertEqual(self.sent[0]['url'], 'https://openrouter.ai/api/v1/chat/completions')
        for forbidden in ('temperature', 'top_p', 'tools', 'tool_choice', 'models', 'route', 'fallbacks', 'usage', 'stream'):
            self.assertNotIn(forbidden, body)
        self.assertEqual(body['provider'], {'only': ['alibaba'], 'allow_fallbacks': False, 'require_parameters': True})
        self.assertEqual(body['reasoning'], {'enabled': False})

    def test_usage_cost_and_reservation(self):
        api = self.adapter([ok(usage={'prompt_tokens': 2000, 'completion_tokens': 300, 'cost': 0.0001})])
        _, acct = api.call('SYS', 'U' * 3000, 's1-001:a', validate)
        self.assertEqual((acct['input_tokens'], acct['output_tokens'], acct['attempts']), (2000, 300, 1))
        self.assertAlmostEqual(acct['computed_usd'], (2000 * 0.03 + 300 * 0.13) / 1e6)
        self.assertEqual(acct['provider_reported_usd'], 0.0001); self.assertEqual(acct['actual_usd'], 0.0001)
        # Byte-based upper bound: input tokens <= request bytes, full output limit.
        self.assertGreaterEqual(acct['reserved_usd'] * 1e6, acct['request_bytes'] * 0.03 + 1000 * 0.13 - 1e-9)
        self.assertGreater(acct['request_bytes'], 3000)
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['usage_reported_calls'], t['transport_attempts']), (1, 1, 1))
        self.assertAlmostEqual(t['committed_usd'], 0.0001)

    def test_cost_is_computed_when_the_provider_reports_none(self):
        api = self.adapter([ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertIsNone(acct['provider_reported_usd'])
        self.assertAlmostEqual(acct['actual_usd'], 29e-6)      # 900*0.03 + 12*0.13 = 28.56 micro-dollars, rounded up to 29
        self.assertGreaterEqual(acct['actual_usd'], acct['computed_usd'] - 1e-12)

    def test_reported_cost_above_the_reservation_is_an_integrity_failure(self):
        e = self.failure(self.adapter([ok(usage={'prompt_tokens': 10, 'completion_tokens': 5, 'cost': 1.0})]))
        self.assertEqual(e.category, 'reservation_bound_breached'); self.assertIn(e.category, orp.INTEGRITY)

    def test_model_and_provider_are_checked(self):
        self.assertEqual(self.failure(self.adapter([ok(model='qwen/qwen3.7-plus')])).category, 'model_mismatch')
        self.assertEqual(self.failure(self.adapter([ok(provider='DeepInfra')]), 's1-001:b').category, 'provider_mismatch')
        api = self.adapter([ok(model='qwen/qwen3.7-flash'), ok(provider=None)])
        api.call('SYS', 'USER', 's1-001:c', validate); api.call('SYS', 'USER', 's1-001:d', validate)

    def test_missing_credential(self):
        with patch.dict(os.environ, {orp.KEY_ENV: ''}):
            with self.assertRaises(orp.CallFailure) as cm: self.adapter([])
        self.assertEqual(cm.exception.category, 'missing_credential_alias')

    def test_input_size_limit_is_refused_before_any_reservation(self):
        api = self.adapter([])
        with self.assertRaises(orp.CallFailure) as cm: api.call('SYS', 'U' * 50000, 's1-001:big', validate)
        self.assertEqual(cm.exception.category, 'input_size_limit'); self.assertEqual(self.sent, [])
        self.assertEqual(self.ledger.transact()['attempted_calls'], 0)


class Answers(Base):
    def category(self, response, call_id='s1-001:a'):
        return self.failure(self.adapter([response]), call_id)

    def test_answer_failure_categories_are_distinct_and_never_retried(self):
        cases = {
            'refusal': ok(finish='content_filter'),
            'truncated_output': ok(finish='length'),
            'empty_answer': ok(content='   '),
            'invalid_json': ok(content='{"answer": 7'),
            'invalid_answer': ok(content='{"answer": "seven"}'),
            'answer_too_long': ok(content='{"answer": 7}' + ' ' * 5000),
            'nonterminal_output': ok(finish='tool_calls'),
            'missing_usage': ok(usage={}),
            'unexpected_reasoning_tokens': ok(usage={'prompt_tokens': 10, 'completion_tokens': 5,
                                                     'completion_tokens_details': {'reasoning_tokens': 3}}),
        }
        for want, response in cases.items():
            self.sent.clear()
            e = self.category(response, 's1-001:' + want)
            self.assertEqual(e.category, want); self.assertEqual(len(self.sent), 1, want)
            self.assertEqual(e.accounting['attempts'], 1)
        # More than 8,000 input tokens (the request must be that large for the byte-based reservation to hold).
        api = self.adapter([ok(usage={'prompt_tokens': 8001, 'completion_tokens': 5})])
        with self.assertRaises(orp.CallFailure) as cm: api.call('SYS', 'U' * 9000, 's1-001:ceiling', validate)
        self.assertEqual(cm.exception.category, 'input_ceiling_exceeded')
        refused = ok(); refused['choices'][0]['message']['refusal'] = 'I cannot help with that.'
        self.assertEqual(self.category(refused, 's1-001:r2').category, 'refusal')
        none = ok(); none['choices'] = []
        self.assertEqual(self.category(none, 's1-001:r3').category, 'empty_answer')

    def test_invalid_answers_keep_the_text_for_reading(self):
        e = self.category(ok(content='{"answer": "seven"}'))
        self.assertEqual(e.accounting['answer_text'], '{"answer": "seven"}')
        self.assertTrue(e.accounting['usage_reported'])

    def test_zero_reasoning_tokens_are_fine(self):
        api = self.adapter([ok(usage={'prompt_tokens': 10, 'completion_tokens': 5, 'completion_tokens_details': {'reasoning_tokens': 0}})])
        api.call('SYS', 'USER', 's1-001:a', validate)


class Transport(Base):
    def test_http_error_keeps_status_body_and_request_id_and_no_secret(self):
        e = self.failure(self.adapter([http(500, '{"error":{"message":"upstream exploded"}}', {'x-request-id': 'req_1'})]))
        self.assertEqual(e.category, 'http_500'); self.assertEqual(len(self.sent), 1)
        self.assertEqual((e.accounting['http_status'], e.accounting['request_id']), (500, 'req_1'))
        self.assertIn('upstream exploded', e.accounting['error_body'])
        self.assertNotIn(KEY, json.dumps(e.accounting)); self.assertNotIn('Bearer', json.dumps(e.accounting))
        self.assertNotIn(KEY, (Path(self.tmp.name) / 'ledger.jsonl').read_text())

    def test_body_is_truncated(self):
        e = self.failure(self.adapter([http(400, 'x' * 9000)]))
        self.assertEqual(len(e.accounting['error_body']), 2000); self.assertEqual(e.category, 'http_400')

    def test_retry_only_on_429_and_overload(self):
        api = self.adapter([http(429), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 2); self.assertEqual(self.clock.sleeps, [2])
        self.assertEqual(acct['earlier_http_status'], 429)       # evidence of the recovered attempt is kept
        self.clock.sleeps.clear()
        api = self.adapter([http(503), http(529), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:b', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(self.clock.sleeps, [2, 6])
        e = self.failure(self.adapter([http(429), http(429), http(429)]), 's1-001:c')
        self.assertEqual((e.category, e.accounting['attempts']), ('http_429', 3))
        for status in (400, 401, 403, 404, 408, 500):
            self.sent.clear()
            e = self.failure(self.adapter([http(status)]), f's1-001:s{status}')
            self.assertEqual((e.category, len(self.sent)), (f'http_{status}', 1))

    def test_retry_after_is_honoured_and_capped(self):
        api = self.adapter([http(429, headers={'retry-after': '9'}), http(429, headers={'retry-after': '300'}), ok()])
        api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(self.clock.sleeps, [9, 20])

    def test_timeouts_and_other_transport_errors_are_never_retried(self):
        for exc, want in ((socket.timeout('t'), 'timeout'), (TimeoutError('t'), 'timeout'),
                          (urllib.error.URLError(socket.timeout('t')), 'timeout'),
                          (urllib.error.URLError('refused'), 'transport_URLError'),
                          (ConnectionResetError('reset'), 'transport_ConnectionResetError')):
            self.sent.clear()
            e = self.failure(self.adapter([exc]), 's1-001:' + want + str(id(exc)))
            self.assertEqual((e.category, len(self.sent)), (want, 1))

    def test_retries_stay_inside_the_request_timeout(self):
        config = json.loads(json.dumps(CONFIG)); config['budget']['request_timeout_seconds'] = 5
        e = self.failure(self.adapter([http(429), http(429)], config))
        self.assertEqual((e.category, e.accounting['attempts']), ('http_429', 2))    # 2 s, then 6 s would pass the deadline

    def test_error_object_in_a_200_response(self):
        api = self.adapter([{'error': {'code': 502, 'message': 'provider returned error'}}, ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 2)
        e = self.failure(self.adapter([{'error': {'code': 400, 'message': 'bad request'}}]), 's1-001:b')
        self.assertEqual(e.category, 'http_400'); self.assertIn('bad request', e.accounting['error_body'])
        e = self.failure(self.adapter([{'error': {'message': 'no code'}}]), 's1-001:c')
        self.assertEqual(e.category, 'provider_error_200')

    def test_malformed_body(self):
        e = self.failure(self.adapter([b'<html>gateway</html>']))
        self.assertEqual(e.category, 'malformed_provider_response'); self.assertIn('gateway', e.accounting['error_body'])


class Billing(Base):
    CREDIT = '{"error":{"code":402,"message":"Insufficient credits. Add more using https://openrouter.ai/credits"}}'

    def test_detection(self):
        self.assertTrue(orp.is_billing_error(402, ''))
        self.assertTrue(orp.is_billing_error(400, 'Your credit balance is too low'))
        self.assertTrue(orp.is_billing_error(403, 'Key limit exceeded: insufficient Balance'))
        self.assertFalse(orp.is_billing_error(400, 'invalid request')); self.assertFalse(orp.is_billing_error(429, 'credit'))

    def test_outage_then_success_is_one_pause_and_no_failed_call(self):
        api = self.adapter([http(402, self.CREDIT)] * 3 + [ok()])
        answer, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(answer, {'answer': 7}); self.assertEqual(acct['attempts'], 4)
        self.assertEqual(self.clock.sleeps, [60, 60, 60])
        self.assertEqual(api.billing, {'billing_pauses': 1, 'billing_pause_seconds': 180.0, 'billing_affected_calls': 1})
        self.assertFalse(api.billing_stopped()); self.assertTrue(acct['billing_paused'])
        t = self.ledger.transact()
        self.assertEqual((t['attempted_calls'], t['transport_attempts'], t['usage_reported_calls']), (1, 4, 1))

    def test_credit_error_reported_as_400_or_inside_a_200(self):
        api = self.adapter([http(400, '{"error":{"message":"Your credit balance is too low"}}'),
                            {'error': {'code': 402, 'message': 'Insufficient credits'}}, ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(api.billing['billing_pauses'], 1)

    def test_outage_outlasting_the_limit_stops_with_the_distinct_category(self):
        api = self.adapter([http(402, self.CREDIT)] * 40)
        e = self.failure(api)
        self.assertEqual(e.category, orp.BILLING_STOP); self.assertEqual(e.category, 'provider_credit_balance_low')
        self.assertEqual(sum(self.clock.sleeps), 1200); self.assertEqual(e.accounting['attempts'], 21)
        self.assertTrue(api.billing_stopped()); self.assertEqual(api.billing['billing_pause_seconds'], 1200.0)
        before = len(self.sent)
        e2 = self.failure(api, 's1-001:next')                       # nothing further is sent or reserved
        self.assertEqual(e2.category, orp.BILLING_STOP); self.assertEqual(len(self.sent), before)
        self.assertFalse(e2.accounting['attempted']); self.assertEqual(self.ledger.transact()['attempted_calls'], 1)

    def test_retry_rule_applies_again_after_the_outage(self):
        api = self.adapter([http(402, self.CREDIT), http(429), ok()])
        _, acct = api.call('SYS', 'USER', 's1-001:a', validate)
        self.assertEqual(acct['attempts'], 3); self.assertEqual(self.clock.sleeps[0], 60)

    def test_other_calls_wait_during_the_pause_and_then_complete(self):
        gate = threading.Event(); order = []
        lock = threading.Lock(); state = {'credit': 2}
        def opener(request, timeout):
            user = json.loads(request.data)['messages'][1]['content']
            with lock:
                order.append(user)
                if state['credit'] > 0:
                    state['credit'] -= 1
                    raise http(402, self.CREDIT)
            return Resp(json.dumps(ok()).encode())
        def sleep(seconds):
            gate.wait(2)                                         # the owner's wait: until the second call has arrived
        ledger = orp.Ledger(Path(self.tmp.name) / 'ledger.jsonl', CONFIG['budget'])
        api = orp.OpenRouter(ledger, CONFIG, opener, sleep=sleep)
        results = {}
        def run(name):
            try: results[name] = api.call('SYS', name, 's1-001:' + name, validate)[1]
            except orp.CallFailure as exc: results[name] = exc
        first = threading.Thread(target=run, args=('one',)); first.start()
        while not order: pass
        second = threading.Thread(target=run, args=('two',)); second.start()
        gate.set(); first.join(10); second.join(10)
        self.assertFalse(first.is_alive() or second.is_alive())
        for name in ('one', 'two'):
            self.assertIsInstance(results[name], dict, results[name]); self.assertTrue(results[name]['usage_reported'])
        self.assertEqual(api.billing['billing_pauses'], 1)
        self.assertEqual(ledger.transact()['usage_reported_calls'], 2)


class LedgerRules(Base):
    def test_caps_and_duplicates(self):
        b = json.loads(json.dumps(CONFIG['budget'])); b['max_calls'] = {'P0': 1, 'Q0': 2, 'S1': 3}; b['max_attempted_calls'] = 5
        b['max_transport_attempts'] = 2
        ledger = orp.Ledger(Path(self.tmp.name) / 'l.jsonl', b)
        def reserve(call, usd=1): return ledger.transact({'type': 'reserve', 'call_id': call, 'micro_usd': usd})
        def refused(call, usd=1):
            with self.assertRaises(orp.CallFailure) as cm: reserve(call, usd)
            return cm.exception.category
        reserve('p0-001:a'); self.assertEqual(refused('p0-001:a'), 'duplicate_call_refused')
        self.assertEqual(refused('p0-001:b'), 'stage_call_cap_reached')
        self.assertEqual(refused('s2-001:a'), 'stage_call_cap_reached')          # unknown stage has no allowance
        reserve('q0-001:a'); reserve('q0-001:b'); reserve('s1-001:a')
        self.assertEqual(refused('s1-001:big', 2_000_001), 'aggregate_budget_exhausted')
        reserve('s1-001-r1:b')                                                    # a continuation batch counts as S1
        self.assertEqual(refused('s1-001:c'), 'study_call_cap_reached')
        with self.assertRaises(orp.CallFailure) as cm: ledger.transact({'type': 'attempt', 'call_id': 'nope'})
        self.assertEqual(cm.exception.category, 'attempt_without_reservation')
        ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'}); ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'})
        with self.assertRaises(orp.CallFailure) as cm: ledger.transact({'type': 'attempt', 'call_id': 'p0-001:a'})
        self.assertEqual(cm.exception.category, 'transport_attempt_cap_reached')
        t = ledger.transact()
        self.assertEqual(t['calls_by_stage'], {'P0': 1, 'Q0': 2, 'S1': 2}); self.assertEqual(t['transport_attempts'], 2)

    def test_settled_cost_replaces_the_reservation(self):
        ledger = orp.Ledger(Path(self.tmp.name) / 'l.jsonl', CONFIG['budget'])
        ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1_500_000})
        with self.assertRaises(orp.CallFailure): ledger.transact({'type': 'reserve', 'call_id': 's1-001:b', 'micro_usd': 600_000})
        ledger.transact({'type': 'response', 'call_id': 's1-001:a', 'actual_micro_usd': 100, 'input_tokens': 5, 'output_tokens': 1})
        ledger.transact({'type': 'reserve', 'call_id': 's1-001:b', 'micro_usd': 600_000})
        self.assertAlmostEqual(ledger.transact()['committed_usd'], 0.6001)

    def test_ledger_file_is_private_and_a_corrupt_line_fails_closed(self):
        path = Path(self.tmp.name) / 'l.jsonl'
        ledger = orp.Ledger(path, CONFIG['budget']); ledger.transact({'type': 'reserve', 'call_id': 's1-001:a', 'micro_usd': 1})
        self.assertEqual(oct(path.stat().st_mode & 0o777), '0o600')
        with path.open('a') as f: f.write('{"type": "reser')
        with self.assertRaises(Exception): ledger.transact()

    def test_stage_of(self):
        self.assertEqual([orp.stage_of(x) for x in ('p0-001:a', 'q0-002:b', 's1-001-r2:c')], ['P0', 'Q0', 'S1'])


if __name__ == '__main__':
    unittest.main()
