"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the
standard unittest summary ("Ran N tests ... OK") on stderr."""
import copy
import importlib.util
import io
import json
import os
import socket
import sys
import tempfile
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

FROZEN = {  # sha256 of json.dumps(sort_keys=True); computed once from the parent generator
    'ring_clean_4919': 'de9d564b5b1e3d884a729eeba61b0a7877c9147bb7811f9efbebfac42c8fa0cd',
    'ring_clean_5139': 'a1ecd92e07914094ed17a9750627fb679a71fca46ebc83399993f89d208feaf2',
    'ring_parent_attack_4919': '3eb994716eb04c3390072f3fccbbf39fbea5581be06b955cf14e0847140aeb1e',
    'policies_parent_attack_4919': '371b6c17151d291ee871032a66e9d63d43bcfde3c5dd04769e5a7aa452daa599',
    'community_4821': '7cd2a783a6c44f7dc013bf96ea62e802cd65e04e2b09c52ef25a014958280a21'}
D = study.design(); CFG = study.cfg(); KS = D['attacker']['identities']
RING, COMMUNITY = D['roots']['engineering']['ring'][0], D['roots']['engineering']['community'][0]
_cache = {}


def scripted_rows(stage):
    """Rows as the worker would write them with the scripted backend (cached per process)."""
    if stage not in _cache:
        rows = []
        for a in study.assignments(stage):
            r = worker.row_base(a, {'stage': stage, 'backend': 'scripted', 'code': 'test', 'source_hash': 'test'}, 'test')
            answer = study.scripted(a['packet'])
            r.update(answer=answer, accounting={'attempted': False}, evaluation=study.evaluate(a, answer),
                     scripted_evaluation=study.evaluate(a, answer),
                     identity_evaluation=study.evaluate(a, study.scripted(a['packet'], by_identity=True)), status='completed')
            rows.append(r)
        _cache[stage] = rows
    return _cache[stage]


def policy_trace(mod, w):
    out = []
    for arm in sim.ARMS:
        passed = set(); failed = set(); checked = []
        for step in range(1, 13):
            if arm == 'no_verification': break
            node = mod.select_check(w['public'], arm, passed, failed, checked, w['task'], step)
            ok = w['checks'][node]; checked.append(node); (passed if ok else failed).add(node)
        order, _ = mod.rank(w['public'], passed, failed, CFG); out.append((arm, checked, order[:54]))
    return out


class Resp(io.BytesIO):
    def __enter__(self): return self
    def __exit__(self, *a): return False


def message(answer=None, **over):
    answer = answer or {'values': {str(i): None for i in range(6)}}
    data = {'model': D['model'], 'stop_reason': 'end_turn', 'usage': {'input_tokens': 1000, 'output_tokens': 300},
            'content': [{'type': 'thinking', 'thinking': '', 'signature': 'x'}, {'type': 'text', 'text': json.dumps(answer)}]}
    data.update(over); return data


def http_error(code, retry_after=None):
    headers = {'retry-after': str(retry_after)} if retry_after is not None else {}
    return urllib.error.HTTPError(provider.MESSAGES_URL, code, 'error', headers, io.BytesIO(b'{}'))


class Script:
    """Opener that plays a list of outcomes for the messages endpoint; count_tokens answers 1000."""
    def __init__(self, outcomes, count_outcomes=()):
        self.outcomes = list(outcomes); self.count_outcomes = list(count_outcomes); self.sent = []
    def __call__(self, request, timeout=None):
        self.sent.append((request.full_url, json.loads(request.data), timeout))
        if request.full_url == provider.COUNT_URL:
            item = self.count_outcomes.pop(0) if self.count_outcomes else {'input_tokens': 1000}
        else:
            item = self.outcomes.pop(0)
        if isinstance(item, Exception): raise item
        return Resp(json.dumps(item).encode())
    def message_requests(self): return [s for s in self.sent if s[0] == provider.MESSAGES_URL]


class Clock:
    def __init__(self): self.t = 0.0; self.waits = []
    def now(self): return self.t
    def sleep(self, s): self.waits.append(s); self.t += s


def adapter(td, script, clock=None, budget=None):
    clock = clock or Clock()
    with patch.dict(os.environ, {'SWARM_MODEL_API_KEY': 'k', 'SWARM_MODEL_WORKSPACE_ID': 'w'}):
        ledger = provider.Ledger(Path(td) / 'ledger', budget)
        return provider.Anthropic(ledger, script, clock.now, clock.sleep), ledger, clock


PACKET = {'skills': list(range(6)), 'reports': []}


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
    def __init__(self): self.rows = []; self.queue = []; self.registered = None; self.n = 0
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
    def add(self, stage, status='done', invalid=0, passed=1, source_hash=None):
        p = study.params(stage); p['source_hash'] = source_hash or p['source_hash']
        self.rows.append({'run': f'x/{stage}{len(self.rows)}', 'status': status, 'params': p,
                          'metrics': {'invalid': invalid, 'qualification_passed': passed, 'model_calls': 60,
                                      'input_tokens': 240000, 'output_tokens': 6000, 'cost_usd': 1.08}})


class Tests(unittest.TestCase):
    # ------------------------------------------------------------------ graph generators
    def test_ring_generator_matches_parent_instrument(self):
        for task in (4919, 5139):
            self.assertEqual(study.digest(sim.parent_make_world(task, 3, 0.0, True, CFG)), FROZEN[f'ring_clean_{task}'])
        w = sim.parent_make_world(4919, 3, 0.1, False, CFG)
        self.assertEqual(study.digest(w), FROZEN['ring_parent_attack_4919'])
        self.assertEqual(study.digest(policy_trace(sim, w)), FROZEN['policies_parent_attack_4919'])
        path = study.ROOT.parent / 'sybil-scale-xl/src/sim.py'
        if path.exists():   # the frozen digests above came from this file; compare directly when it is present
            spec = importlib.util.spec_from_file_location('parentsim', path); old = importlib.util.module_from_spec(spec); spec.loader.exec_module(old)
            for task in (4919, 8233):
                for clean in (True, False):
                    a = old.make_world(task, 3, 0.1, clean, CFG); b = sim.parent_make_world(task, 3, 0.1, clean, CFG)
                    for key in ('public', 'truth', 'checks', 'answers', 'groups', 'task'): self.assertEqual(a[key], b[key])
                    self.assertEqual(policy_trace(old, a), policy_trace(sim, b))
            for node in ('u000', 'u134'):
                for step in (1, 12): self.assertEqual(old.rng(8233, 'tie', step, node).random(), sim.tie_value(8233, step, node))

    def graph_invariants(self, family, task):
        w = sim.honest_world(family, task, CFG); pub = w['public']; adj = pub['adj']; g = w['groups']
        self.assertTrue(sim.connected({x: set(v) for x, v in adj.items()}))
        self.assertEqual([sum(v == i for v in g.values()) for i in (0, 1, 2)], [54, 27, 27])
        self.assertEqual(len(pub['trusted']), 2); self.assertTrue(all(g[x] == 0 for x in pub['trusted']))
        for x in adj:
            self.assertEqual(len(adj[x]), 7 if g[x] == 0 else 4); self.assertNotIn(x, adj[x])
            self.assertEqual(len(set(adj[x])), len(adj[x])); self.assertTrue(all(x in adj[y] for y in adj[x]))
        for group in (1, 2):
            self.assertEqual(sum(g[y] == 0 for x in adj if g[x] == group for y in adj[x]), 6)
            self.assertEqual(sum(g[y] not in (0, group) for x in adj if g[x] == group for y in adj[x]), 0)
        profiles = [sorted((v['skill'], v['age'], v['activity'], len(adj[x]), sum(g[y] == 0 for y in adj[x]))
                           for x, v in pub['nodes'].items() if g[x] == group) for group in (1, 2)]
        self.assertEqual(*profiles)
        self.assertTrue(all(v['honest'] for v in w['truth'].values()))
        self.assertEqual(sum(v['specialist'] for v in w['truth'].values()), 54)
        self.assertEqual(sorted({v['skill'] for x, v in pub['nodes'].items() if g[x] == 0}), [0, 1, 2])
        self.assertEqual(sorted({v['skill'] for x, v in pub['nodes'].items() if g[x] > 0}), [3, 4, 5])
        return w

    def test_ring_graph_invariants(self):
        for task in D['roots']['engineering']['ring'][:4]: self.graph_invariants('ring', task)

    def test_community_graph_invariants(self):
        for task in D['roots']['engineering']['community'][:6]:
            w = self.graph_invariants('community', task); adj = w['public']['adj']
            # exchanging the two halves (core A <-> core B, outside 1 <-> outside 2) is an automorphism
            def twin(x):
                i = int(x[1:]); return f'c{(i + 27 if i < 27 else i - 27 if i < 54 else i + 27 if i < 81 else i - 27):03d}'
            self.assertTrue(all(sorted(twin(y) for y in adj[x]) == adj[twin(x)] for x in adj))

    def test_community_graph_is_deterministic_and_its_own_generator(self):
        a = sim.community_make_world(COMMUNITY, CFG); b = sim.community_make_world(COMMUNITY, CFG)
        self.assertEqual(a, b); self.assertEqual(study.digest(a), FROZEN['community_4821'])
        self.assertNotEqual(a['public']['adj'], sim.community_make_world(COMMUNITY + 1, CFG)['public']['adj'])
        ring = sim.parent_make_world(COMMUNITY, 3, 0.0, True, CFG)
        degree_sequence = lambda w: sorted(len(v) for v in w['public']['adj'].values())
        self.assertEqual(degree_sequence(a), degree_sequence(ring))      # degree-matched
        triangles = lambda w: sum(len(set(w['public']['adj'][x]) & set(w['public']['adj'][y])) for x in w['public']['adj'] for y in w['public']['adj'][x])
        self.assertLess(triangles(a), triangles(ring) / 2)               # not a lattice: far fewer triangles

    # -------------------------------------------------------------------- the manipulation
    def test_structural_invariants_at_every_identity_allocation(self):
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            self.assertEqual(study.check_root(family, task), [])

    def test_attacker_totals_and_honest_world_are_fixed_across_identity_counts(self):
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            base = study.world(family, task, 0, 0.1); seen = set()
            for k in KS:
                w = study.world(family, task, k, 0.1); ids = w['identities']; honest = set(base['public']['nodes'])
                rows = sorted((r['skill'], r['claim'], r['order']) for x in ids for r in w['rows'][x])
                ends = sorted(t for x in ids for t in w['public']['adj'][x] if t in honest)
                seen.add(json.dumps([rows, ends, w['resources']['draws'], sorted(w['checks'].items()), w['public']['trusted']]))
                self.assertEqual((len(ids), len(rows), len(ends)), (k, 27, 27))
                self.assertEqual({len(w['rows'][x]) for x in ids}, {27 // k})
                self.assertEqual({sum(t in honest for t in w['public']['adj'][x]) for x in ids}, {27 // k})
                self.assertEqual(sorted(r[0] for r in rows), [3] * 9 + [4] * 9 + [5] * 9)
                self.assertEqual({x: w['rows'][x] for x in honest}, base['rows'])
                self.assertEqual({x: sorted(set(w['public']['adj'][x]) & honest) for x in honest}, base['public']['adj'])
                self.assertEqual(w['resources']['internal_links'], study.INTERNAL_LINKS['ring2'][k])
            self.assertEqual(len(seen), 1)

    def test_invariant_checker_detects_a_broken_manipulation(self):
        real = study.pilot.__wrapped__
        def tampered(family, task, k, rate):
            w, records = real(family, task, k, rate)
            if k == 3:
                w = copy.deepcopy(w); victim = sorted(w['checks'])[0]; w['checks'][victim] = not w['checks'][victim]
            if k == 9:
                w = copy.deepcopy(w); x = w['identities'][0]; w['rows'][x] = w['rows'][x][:-1]
            return w, records
        with patch.object(study, 'pilot', tampered):
            bad = ' '.join(study.check_root('ring', RING))
        self.assertIn('k=3:pass=0.1:honest_world_changed', bad); self.assertIn('k=9:pass=0.1:row_total', bad)
        self.assertIn('attacker_totals_changed', bad)

    def test_attacker_names_and_profiles_are_indistinguishable_by_construction(self):
        self.assertEqual(study.check_names('engineering'), [])
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            w = study.world(family, task, 27, 0.1)
            self.assertTrue(all(study.NAME.match(x) for x in w['public']['nodes']))
            outside = {(v['age'], v['activity']) for x, v in w['public']['nodes'].items() if w['groups'][x] in (1, 2)}
            self.assertTrue(all((w['public']['nodes'][x]['age'], w['public']['nodes'][x]['activity']) in outside for x in w['identities']))
            degrees = {len(w['public']['adj'][x]) for x in w['identities']}
            self.assertEqual(degrees, {5})   # 4 internal links and 1 attachment: an honest outside identity with one attachment

    def test_packets_hold_no_truth_or_ownership_and_keep_row_order(self):
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            orders = {}
            for k in KS:
                w, records = study.pilot(family, task, k, 0.1)
                for rec in records:
                    pack = study.packet(w, rec['admitted'], rec['passed'])
                    self.assertEqual(study.check_packet(w, pack, rec['admitted'], rec['passed'], rec['admission']), [])
                    self.assertEqual(set(pack), {'skills', 'reports'})
                    honest_rows = [(r['node'], r['skill']) for r in pack['reports'] if r['node'] not in w['identities']]
                    for i, a in enumerate(honest_rows[:-1]):
                        self.assertIn(orders.setdefault(frozenset((a, honest_rows[i + 1])), (a, honest_rows[i + 1])), [(a, honest_rows[i + 1])])
        leaky = {'skills': [0], 'reports': [{'node': 'u001', 'skill': 0, 'claim': 1, 'age': 1, 'activity': 1, 'verification': 'x', 'honest': True}]}
        w, records = study.pilot('ring', RING, 1, 0.1)
        self.assertIn('packet_leaks_evaluator_field', study.check_packet(w, leaky, [], [], records[0]['admission']))

    def test_manipulated_answer_is_graded_wrong_and_abstention_is_not(self):
        w = study.world('ring', RING, 27, 0.1); a = {'answers': w['answers'], 'fabricated': w['fabricated'],
            'expected': {str(s): w['answers'][s] for s in range(6)}, 'admission': {}}
        lie = {'values': {str(s): w['fabricated'][s] if s in sim.RARE else w['answers'][s] for s in range(6)}}
        e = study.evaluate(a, lie); self.assertEqual((e['rare_wrong'], e['rare_accuracy'], e['rare_fabricated'], e['rare_abstain']), (1, 0, 1, 0))
        null = {'values': {str(s): None if s in sim.RARE else w['answers'][s] for s in range(6)}}
        e = study.evaluate(a, null); self.assertEqual((e['rare_wrong'], e['rare_accuracy'], e['rare_abstain']), (0, 0, 1))
        e = study.evaluate(a, {'values': {str(s): w['answers'][s] for s in range(6)}}); self.assertEqual((e['rare_wrong'], e['rare_accuracy']), (0, 1))
        self.assertTrue(all(abs(w['fabricated'][s] - w['answers'][s]) == 7 for s in sim.RARE))

    def test_verification_attempts_are_coupled_and_never_exhausted(self):
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            low = study.world(family, task, 27, 0.1); high = study.world(family, task, 27, 0.9)
            self.assertTrue(all(high['attempts'][x] or not low['attempts'][x] for x in low['identities']))
            for k in KS:
                w, records = study.pilot(family, task, k, 0.9)
                self.assertEqual(w['attempts'][w['identities'][0]], low['resources']['draws'][0] < 0.9)
                self.assertTrue(all(r['admission']['attacker_checked'] <= min(k, r['checks']) for r in records))

    def test_check_policies_are_blind_to_ownership(self):
        for family, task in (('ring', RING), ('community', COMMUNITY)):
            w = study.world(family, task, 27, 0.1); public = json.loads(json.dumps(w['public']))
            self.assertEqual(set(public), {'nodes', 'adj', 'trusted'})
            self.assertTrue(all(set(v) == {'age', 'activity'} for v in public['nodes'].values()))
            for arm in ('degree', 'random', 'coverage'):
                first = sim.select_check(public, arm, set(), set(), [], task, 1)
                for v in w['truth'].values(): v['honest'] = not v['honest']      # the policy cannot see this
                self.assertEqual(first, sim.select_check(public, arm, set(), set(), [], task, 1))
                for v in w['truth'].values(): v['honest'] = not v['honest']
            import inspect
            self.assertEqual(list(inspect.signature(sim.select_check).parameters), ['public', 'arm', 'passed', 'failed', 'checked', 'task', 'step'])
            self.assertEqual(list(inspect.signature(sim.rank).parameters), ['public', 'passed', 'failed', 'cfg'])

    def test_plurality_rules(self):
        rows = [{'node': 'a', 'skill': 0, 'claim': 5}] * 3 + [{'node': 'b', 'skill': 0, 'claim': 7}, {'node': 'c', 'skill': 0, 'claim': 7},
                {'node': 'd', 'skill': 1, 'claim': 1}, {'node': 'e', 'skill': 1, 'claim': 2}]
        pack = {'skills': list(range(6)), 'reports': rows}
        self.assertEqual(study.scripted(pack)['values'], {'0': 5, '1': None, '2': None, '3': None, '4': None, '5': None})
        self.assertEqual(study.scripted(pack, by_identity=True)['values']['0'], 7)

    # ------------------------------------------------------------ fixtures and qualification
    def test_qualification_fixtures_are_clean_and_cover_each_load_regime(self):
        for family, task in study.roots('qualification')[::4] + [(D['probe']['family'], D['probe']['task'])]:
            for shape in D['qualification']['shapes']: self.assertEqual(study.check_fixture(family, task, shape), [])
        sizes = {a['shape']: len(a['packet']['reports']) for a in study.assignments('Q0')}
        self.assertEqual(sizes, {'full': 108, 'common_only': 54, 'sparse': 54, 'multirow1': 80, 'multirow3': 78, 'multirow9': 72})

    def test_stage_counts_and_caps(self):
        b = D['budget']; q = study.assignments('Q0'); p = study.assignments('P0')
        self.assertEqual((len(p), len(q)), (1, 60)); self.assertEqual(p[0]['kind'], 'probe')
        self.assertEqual((p[0]['family'], p[0]['task'], p[0]['shape']), ('ring', RING, 'multirow1'))
        self.assertEqual(b['max_calls'], {'S0': 0, 'P0': 1, 'Q0': 60, 'S1': 2688})
        self.assertEqual(b['max_attempted_calls'], sum(b['max_calls'].values()))
        self.assertEqual(24 * 2 * 2 * 4 * 7, b['max_calls']['S1'])
        self.assertEqual(sum(a['expected'][str(s)] is None for a in q for s in range(6)), 40)

    def test_qualification_gate_thresholds(self):
        rows = copy.deepcopy(scripted_rows('Q0'))
        self.assertTrue(study.qualification(rows)['passed'])
        def regrade(row, answer):
            a = next(x for x in study.assignments('Q0') if x['id'] == row['id']); row.update(answer=answer, evaluation=study.evaluate(a, answer))
        full = [r for r in rows if r['shape'] == 'full']
        wrong = copy.deepcopy(full[0]['answer']); wrong['values']['0'] += 1; regrade(full[0], wrong)
        self.assertTrue(study.qualification(rows)['passed'])             # 9 of 10 exact, 59 of 60 fields
        wrong = copy.deepcopy(full[1]['answer']); wrong['values']['0'] += 1; regrade(full[1], wrong)
        self.assertFalse(study.qualification(rows)['passed'])            # 8 of 10 exact
        rows = copy.deepcopy(scripted_rows('Q0')); sparse = next(r for r in rows if r['shape'] == 'sparse')
        regrade(sparse, {'values': {k: (0 if v is None else v) for k, v in sparse['answer']['values'].items()}})
        self.assertFalse(study.qualification(rows)['passed'])            # one withheld fact answered
        rows = copy.deepcopy(scripted_rows('Q0')); rows[0]['status'] = 'failed'
        self.assertFalse(study.qualification(rows)['passed'])            # a missing packet

    def test_probe_gate(self):
        a = study.assignments('P0')[0]; row = worker.row_base(a, study.params('P0'), 't')
        good = study.scripted(a['packet']); row.update(status='completed', evaluation=study.evaluate(a, good), accounting={'input_tokens': 5, 'output_tokens': 6})
        self.assertEqual(study.probe_gate([row]), {'count': 1, 'passed': True, 'input_tokens': 5, 'output_tokens': 6})
        bad = copy.deepcopy(good); bad['values']['3'] += 1; row.update(evaluation=study.evaluate(a, bad))
        self.assertFalse(study.gate('P0', [row])); row.update(status='failed'); self.assertFalse(study.gate('P0', [row]))
        self.assertIsNone(study.gate('S1', []))

    def test_splits_are_disjoint_and_below_the_holdout(self):
        groups = [set(D['roots'][split][f]) for split in ('engineering', 'qualification', 'comparison') for f in D['families']]
        self.assertEqual([len(g) for g in groups], [16, 16, 5, 5, 24, 24])
        self.assertTrue(all(not a & b for i, a in enumerate(groups) for b in groups[i + 1:]))
        self.assertLess(max(set.union(*groups)), 10000); self.assertEqual(D['roots']['reserved_holdout'], [10000, 19999])
        self.assertIn(D['probe']['task'], D['roots']['engineering'][D['probe']['family']])

    def test_invalid_answers(self):
        for answer in ({'values': {'0': True}}, {'values': {str(i): True for i in range(6)}}, {'values': {str(i): 1.5 for i in range(6)}},
                       {'values': {str(i): 1 for i in range(6)}, 'note': 'x'}, [1], {'values': {str(i): '1' for i in range(6)}}):
            with self.assertRaises(ValueError): study.validate(answer)
        study.validate({'values': {str(i): None for i in range(6)}})

    def test_engineering_grid_is_not_degenerate_and_matches_the_setup_record(self):
        rows = scripted_rows('S0'); self.assertEqual(len(rows), 1853)
        self.assertEqual(study.degeneracy(rows), [])
        self.assertTrue(study.gate('S0', rows, []))
        self.assertFalse(study.gate('S0', rows, ['x']))
        a = analyze.analyze(rows)
        self.assertAlmostEqual(a['primary']['estimate'], 0.40625); self.assertAlmostEqual(a['primary']['by_family']['ring']['mean'], 0.4791667, 6)
        self.assertAlmostEqual(a['primary']['by_family']['community']['mean'], 0.3333333, 6)
        self.assertAlmostEqual(a['secondary']['primary_under_unreliable_checks']['estimate'], -0.15625)
        self.assertEqual(a['denominators']['roots'], {'ring': 16, 'community': 16})
        flat = copy.deepcopy(rows)
        for r in flat:
            if r['kind'] == 'pilot': r['admission']['attacker_identities_admitted'] = 0; r['scripted_evaluation']['rare_wrong'] = 0
        self.assertEqual(len(study.degeneracy(flat)), 6)

    def test_manifest_regenerates_identically(self):
        fresh = manifest.build(); self.assertEqual(manifest.text(fresh), manifest.PATH.read_text())
        self.assertEqual({s: e['assignments'] for s, e in fresh['stages'].items()}, {'S0': 1853, 'P0': 1, 'Q0': 60, 'S1': 2688})
        self.assertLess(len(manifest.PATH.read_text()), 300000)
        s1 = study.assignments('S1')
        self.assertEqual(len({(a['family'], a['task']) for a in s1}), 48)
        self.assertTrue(all(54 <= len(a['packet']['reports']) <= 80 for a in s1))
        self.assertTrue(all(len(json.dumps(provider.SYSTEM)) + len(json.dumps(a['packet'])) + 2000 < D['budget']['max_input_bytes'] for a in s1))

    def test_source_hash_covers_code_and_design_only(self):
        with patch.object(Path, 'read_bytes', lambda self: self.name.encode()):
            names = study.source_hash()
        expected = ['design.yaml', 'experiment.yaml', 'requirements.txt'] + sorted(p.name for p in (study.ROOT / 'src').glob('*.py'))
        import hashlib
        self.assertEqual(names, study.digest([(n, hashlib.sha256(n.encode()).hexdigest()) for n in expected]))
        self.assertNotIn('manifest.json', expected); self.assertIn('rehearse.py', expected)

    # ----------------------------------------------------------------------------- adapter
    def test_request_body_has_exactly_the_contract_keys(self):
        with tempfile.TemporaryDirectory() as td:
            script = Script([message()]); api, ledger, _ = adapter(td, script)
            answer, acct = api.call(PACKET, 'q0-001:c1')
            url, body, _ = script.message_requests()[0]
            self.assertEqual(list(body), ['model', 'max_tokens', 'system', 'messages', 'output_config'])
            self.assertEqual(set(body['output_config']), {'effort', 'format'})
            self.assertEqual((body['model'], body['output_config']['effort'], body['max_tokens']), ('claude-opus-5-5', 'low', 8000))
            self.assertEqual(body['output_config']['format'], {'type': 'json_schema', 'schema': provider.SCHEMA})
            for banned in ('thinking', 'temperature', 'top_p', 'top_k', 'tool_choice', 'tools', 'fallbacks', 'stop_sequences', 'metadata'):
                self.assertNotIn(banned, body)
            self.assertEqual([m['role'] for m in body['messages']], ['user'])
            self.assertEqual(json.loads(body['messages'][0]['content']), PACKET)
            count_body = script.sent[0][1]; self.assertEqual(script.sent[0][0], provider.COUNT_URL)
            self.assertEqual(list(count_body), ['model', 'system', 'messages', 'output_config'])
            b = D['budget']; self.assertEqual(acct['actual_usd'], (1000 * b['input_usd_per_million'] + 300 * b['output_usd_per_million']) / 1e6)
            self.assertEqual((b['input_usd_per_million'], b['output_usd_per_million']), (4, 20))
            self.assertEqual(acct['reserved_usd'], ((int(1000 * 1.02) + 64) * 4 + 8000 * 20) / 1e6)
            for word in ('attacker', 'fabricated value for', 'truth', 'k =', 'split'): self.assertNotIn(word, provider.SYSTEM.replace('a fabricated value.', ''))
            # the sybil-scale-xl prompt plus exactly one sentence
            added = 'Each report row names the identity that submitted it, and one identity may submit several rows.\n'
            self.assertEqual(provider.SYSTEM.count(added), 1)
            import hashlib
            self.assertEqual(hashlib.sha256(provider.SYSTEM.replace(added, '').encode()).hexdigest(),
                             '29a224aa216e13c41f7ae41c32ec45ab7e5f7274dc33ebd2ef0ce19ff6774d1c')

    def test_thinking_and_redacted_thinking_blocks_are_dropped(self):
        with tempfile.TemporaryDirectory() as td:
            content = [{'type': 'thinking', 'thinking': '', 'signature': 'a'}, {'type': 'redacted_thinking', 'data': 'zzz'},
                       {'type': 'thinking', 'thinking': 'x', 'signature': 'b'}, {'type': 'text', 'text': json.dumps({'values': {str(i): i for i in range(6)}})}]
            api, _, _ = adapter(td, Script([message(content=content)]))
            answer, acct = api.call(PACKET, 'q0-001:c1'); self.assertEqual(answer['values']['5'], 5); self.assertEqual(acct['attempts'], 1)

    def test_refusal_is_its_own_failure_category(self):
        with tempfile.TemporaryDirectory() as td:
            api, ledger, _ = adapter(td, Script([message(stop_reason='refusal', content=[], stop_details={'type': 'refusal', 'category': 'cyber'})]))
            with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 'q0-001:c1')
            self.assertEqual(ctx.exception.category, 'refusal'); self.assertEqual(ctx.exception.accounting['refusal_category'], 'cyber')
            self.assertTrue(ctx.exception.accounting['usage_reported']); self.assertEqual(ledger.transact()['transport_attempts'], 1)

    def test_bad_responses_fail_without_retry(self):
        cases = [(message(stop_reason='max_tokens'), 'nonterminal_output'), (message(model='claude-other'), 'model_mismatch'),
                 (message(usage={'input_tokens': 5}), 'missing_usage'),
                 (message(usage={'input_tokens': 5, 'output_tokens': 5, 'cache_read_input_tokens': 3}), 'unexpected_cache_usage'),
                 (message(content=[{'type': 'text', 'text': '{"values": {}}'}]), 'invalid_structured_answer'),
                 (message(content=[{'type': 'text', 'text': 'x'}, {'type': 'text', 'text': 'y'}]), 'invalid_structured_answer'),
                 (message(content=[{'type': 'tool_use', 'id': 't', 'name': 'n', 'input': {}}]), 'invalid_structured_answer'),
                 (message(content=[{'type': 'text', 'text': json.dumps({'values': {str(i): None for i in range(6)}}) + ' ' * 2000}]), 'answer_too_long'),
                 (message(usage={'input_tokens': 90000, 'output_tokens': 300}), 'reservation_bound_breached')]
        for i, (data, category) in enumerate(cases):
            with tempfile.TemporaryDirectory() as td:
                script = Script([data, message()]); api, ledger, _ = adapter(td, script)
                with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, f'q0-001:c{i}')
                self.assertEqual(ctx.exception.category, category); self.assertEqual(len(script.message_requests()), 1)

    def test_retry_429_then_success(self):
        with tempfile.TemporaryDirectory() as td:
            script = Script([http_error(429), message()]); api, ledger, clock = adapter(td, script)
            answer, acct = api.call(PACKET, 's1-001:c1')
            self.assertEqual((acct['attempts'], clock.waits), (2, [2])); t = ledger.transact()
            self.assertEqual((t['attempted_calls'], t['transport_attempts'], t['usage_reported_calls']), (1, 2, 1))
            events = [json.loads(line)['type'] for line in (Path(td) / 'ledger').read_text().splitlines()]
            self.assertEqual(events, ['reserve', 'attempt', 'attempt', 'response'])      # reserved once, sent twice

    def test_retry_529_twice_then_success(self):
        with tempfile.TemporaryDirectory() as td:
            script = Script([http_error(529), http_error(529), message()]); api, ledger, clock = adapter(td, script)
            answer, acct = api.call(PACKET, 's1-001:c1'); self.assertEqual((acct['attempts'], clock.waits), (3, [2, 6]))

    def test_three_429_fail_with_three_attempts(self):
        with tempfile.TemporaryDirectory() as td:
            script = Script([http_error(429), http_error(429), http_error(429), message()]); api, ledger, clock = adapter(td, script)
            with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
            self.assertEqual((ctx.exception.category, ctx.exception.accounting['attempts']), ('http_429', 3))
            self.assertEqual(len(script.message_requests()), 3); self.assertTrue(ctx.exception.accounting['attempted'])
            self.assertEqual(ledger.transact()['committed_usd'], ctx.exception.accounting['reserved_usd'])   # full reservation kept

    def test_http_500_and_other_statuses_are_not_retried(self):
        for code in (500, 400, 401, 403, 404, 408, 409, 413, 502, 503):
            with tempfile.TemporaryDirectory() as td:
                script = Script([http_error(code), message()]); api, ledger, clock = adapter(td, script)
                with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
                self.assertEqual((ctx.exception.category, ctx.exception.accounting['attempts'], clock.waits), (f'http_{code}', 1, []))

    def test_timeout_and_transport_errors_are_not_retried(self):
        for exc, category in ((socket.timeout('t'), 'timeout'), (TimeoutError('t'), 'timeout'), (urllib.error.URLError(socket.timeout('t')), 'timeout'),
                              (urllib.error.URLError('refused'), 'transport_URLError'), (ConnectionResetError('r'), 'transport_ConnectionResetError')):
            with tempfile.TemporaryDirectory() as td:
                script = Script([exc, message()]); api, ledger, clock = adapter(td, script)
                with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
                self.assertEqual((ctx.exception.category, len(script.message_requests()), clock.waits), (category, 1, []))

    def test_retry_after_is_honoured_and_capped(self):
        for header, waited in ((9, 9), (300, 20), (1, 2), ('soon', 2)):
            with tempfile.TemporaryDirectory() as td:
                script = Script([http_error(429, header), message()]); api, ledger, clock = adapter(td, script)
                api.call(PACKET, 's1-001:c1'); self.assertEqual(clock.waits, [waited])
        with tempfile.TemporaryDirectory() as td:      # waits share the one request time budget
            script = Script([http_error(429, 20), http_error(429, 20), message()]); api, ledger, clock = adapter(td, script)
            clock.t = 0.0; api.b = dict(api.b, request_timeout_seconds=30)
            with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
            self.assertEqual((ctx.exception.category, ctx.exception.accounting['attempts'], clock.waits), ('http_429', 2, [20]))

    def test_transport_attempt_cap_refuses(self):
        budget = dict(D['budget'], max_transport_attempts=2)
        with tempfile.TemporaryDirectory() as td:
            script = Script([http_error(429), http_error(429), message()]); api, ledger, clock = adapter(td, script, budget=budget)
            with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
            self.assertEqual((ctx.exception.category, len(script.message_requests())), ('transport_attempt_cap_reached', 2))
            with self.assertRaises(provider.CallFailure): ledger.transact({'type': 'attempt', 'call_id': 'never-reserved', 'n': 1})

    def test_count_tokens_follows_the_same_retry_rule(self):
        with tempfile.TemporaryDirectory() as td:
            script = Script([message()], [http_error(529), {'input_tokens': 1000}]); api, ledger, clock = adapter(td, script)
            answer, acct = api.call(PACKET, 's1-001:c1'); self.assertEqual((acct['count_attempts'], acct['attempts'], clock.waits), (2, 1, [2]))
        with tempfile.TemporaryDirectory() as td:
            script = Script([message()], [http_error(500)]); api, ledger, clock = adapter(td, script)
            with self.assertRaises(provider.CallFailure) as ctx: api.call(PACKET, 's1-001:c1')
            self.assertEqual(ctx.exception.category, 'count_http_500'); self.assertFalse(ctx.exception.accounting['attempted'])
            self.assertEqual(ledger.transact()['attempted_calls'], 0); self.assertEqual(script.message_requests(), [])

    def test_missing_credentials_fail_closed(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(provider.CallFailure): provider.Anthropic(provider.Ledger(Path(td) / 'l'))

    # ------------------------------------------------------------------------------ ledger
    def test_ledger_duplicate_stage_cap_study_cap_and_dollar_cap(self):
        b = D['budget']
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger'); ledger.transact({'type': 'reserve', 'call_id': 'p0-001:a', 'micro_usd': 1})
            for call, category in (('p0-001:a', 'duplicate_call_refused'), ('p0-001:b', 'stage_call_cap_reached'), ('p0-002:b', 'stage_call_cap_reached'),
                                   ('s0-001:a', 'stage_call_cap_reached'), ('zz:a', 'stage_call_cap_reached')):
                with self.assertRaises(provider.CallFailure) as ctx: ledger.transact({'type': 'reserve', 'call_id': call, 'micro_usd': 1})
                self.assertEqual(ctx.exception.category, category)
            with self.assertRaises(provider.CallFailure) as ctx:
                ledger.transact({'type': 'reserve', 'call_id': 'q0-001:x', 'micro_usd': int(b['aggregate_usd'] * 1e6)})
            self.assertEqual(ctx.exception.category, 'aggregate_budget_exhausted')
            # settled calls count their actual cost, open or failed calls their full reservation
            ledger.transact({'type': 'reserve', 'call_id': 'q0-001:big', 'micro_usd': 50_000_000})
            ledger.transact({'type': 'response', 'call_id': 'q0-001:big', 'actual_micro_usd': 1000, 'input_tokens': 1, 'output_tokens': 1})
            room = int(b['aggregate_usd'] * 1e6) - 1000 - 1
            ledger.transact({'type': 'reserve', 'call_id': 'q0-001:fits', 'micro_usd': room})
            with self.assertRaises(provider.CallFailure): ledger.transact({'type': 'reserve', 'call_id': 'q0-001:over', 'micro_usd': 1})
            other = provider.Ledger(Path(td) / 'ledger')      # a second process sees the same state
            self.assertEqual(other.transact(), ledger.transact()); self.assertEqual(other.transact()['calls_by_stage'], {'P0': 1, 'Q0': 2})
        small = dict(b, max_calls={'S0': 0, 'P0': 5, 'Q0': 5, 'S1': 5}, max_attempted_calls=3)
        with tempfile.TemporaryDirectory() as td:
            ledger = provider.Ledger(Path(td) / 'ledger', small)
            for i in range(3): ledger.transact({'type': 'reserve', 'call_id': f's1-001:{i}', 'micro_usd': 1})
            with self.assertRaises(provider.CallFailure) as ctx: ledger.transact({'type': 'reserve', 'call_id': 'q0-001:z', 'micro_usd': 1})
            self.assertEqual(ctx.exception.category, 'study_call_cap_reached')

    def test_ledger_fails_closed_on_a_damaged_line(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'ledger'; path.write_text('{"type": "reserve", "call_id": "q0-001:a", "micro_usd": 1}\n{"type": "rese')
            with self.assertRaises(ValueError): provider.Ledger(path).transact()

    # ------------------------------------------------------------------------------ worker
    def fake_assignments(self, n=20):
        a = copy.deepcopy(study.assignments('Q0')[0]); a['kind'] = 'pilot'; a['shape'] = None; a['attacker_pass'] = 0.1; a['arm'] = 'coverage'
        return [dict(a, id=f'{i:020d}') for i in range(n)]

    def test_first_failure_stops_dispatch_and_every_assignment_is_recorded(self):
        class Broken:
            def call(self, packet, call_id): raise provider.CallFailure('injected_failure', {'attempted': True, 'attempts': 1})
        run = FakeRun('x/1', study.params('S1'))
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'assignments', return_value=self.fake_assignments()), \
                patch.object(render, 'replay', lambda *a, **k: 0), patch.dict(os.environ, {'STUDY_BUDGET_LEDGER': str(Path(td) / 'ledger')}):
            with self.assertRaises(worker.StageFailed): worker.execute(study.params('S1'), Path(td) / 'out', run, backend=Broken())
            summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
            rows = [json.loads(line) for line in (Path(td) / 'out' / 'episodes.jsonl').read_text().splitlines()]
        self.assertEqual((summary['terminal'], summary['invalid'], summary['passed'], summary['reason']), (20, 20, False, 'invalid_rows'))
        self.assertLessEqual(summary['started'], 4); self.assertGreaterEqual(summary['not_started'], 16)
        self.assertEqual(len({r['id'] for r in rows}), 20); self.assertEqual({r['status'] for r in rows}, {'failed', 'not_started'})
        kind, metrics = run.final; self.assertEqual(kind, 'fail')
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, metrics)
        self.assertEqual((metrics['episodes'], metrics['invalid']), (20, 20)); self.assertEqual(metrics['model_calls'], summary['started'])

    def test_success_and_gate_failure_both_report_final_metrics(self):
        for mode, want in (('plurality', 'done'), ('never_abstain', 'fail')):
            run = FakeRun('x/q0', study.params('Q0')); stub = rehearse.Stub(mode)
            with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_BUDGET_LEDGER': str(Path(td) / 'ledger'),
                    'SWARM_MODEL_API_KEY': 'k', 'SWARM_MODEL_WORKSPACE_ID': 'w'}):
                try: worker.execute(study.params('Q0'), Path(td) / 'out', run, opener=stub)
                except worker.StageFailed as exc: self.assertEqual(str(exc), 'gate_failed')
                summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
            kind, metrics = run.final; self.assertEqual(kind, want)
            self.assertEqual((metrics['episodes'], metrics['invalid'], metrics['model_calls'], metrics['transport_attempts']), (60, 0, 60, 60))
            self.assertEqual(metrics['qualification_passed'], 1 if want == 'done' else 0)
            self.assertGreater(metrics['input_tokens'], 0); self.assertEqual(metrics['output_tokens'], 60 * 40)
            self.assertAlmostEqual(metrics['cost_usd'], (metrics['input_tokens'] * 4 + metrics['output_tokens'] * 20) / 1e6)
            self.assertEqual(set(worker.ARTIFACTS) - set(run.uploads), set())
            self.assertEqual(summary['study_accounting']['attempted_calls'], 60)

    def test_structural_violation_blocks_every_call_of_a_paid_stage(self):
        run = FakeRun('x/q0', study.params('Q0')); stub = rehearse.Stub('plurality')
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'check_invariants', return_value=['ring:5139:full:row_count']), \
                patch.dict(os.environ, {'STUDY_BUDGET_LEDGER': str(Path(td) / 'ledger'), 'SWARM_MODEL_API_KEY': 'k', 'SWARM_MODEL_WORKSPACE_ID': 'w'}):
            with self.assertRaises(worker.StageFailed) as ctx: worker.execute(study.params('Q0'), Path(td) / 'out', run, opener=stub)
            summary = json.loads((Path(td) / 'out' / 'summary.json').read_text())
        self.assertEqual((str(ctx.exception), stub.messages, stub.counts), ('invariant_violations', 0, 0))
        self.assertEqual((summary['not_started'], summary['model_calls'], summary['qualification_passed']), (60, 0, 0))
        self.assertEqual((run.final[0], run.final[1]['invalid'], run.final[1]['model_calls']), ('fail', 60, 0))
        self.assertEqual(study.check_invariants('P0'), []); self.assertEqual(study.check_invariants('Q0'), [])

    def test_internal_error_still_closes_the_run_with_metrics(self):
        run = FakeRun('x/1', study.params('S1'))
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'assignments', side_effect=RuntimeError('boom')):
            with self.assertRaises(RuntimeError): worker.execute(study.params('S1'), Path(td) / 'out', run)
        kind, metrics = run.final; self.assertEqual(kind, 'fail'); self.assertGreaterEqual(metrics['invalid'], 1)
        for key in ('episodes', 'invalid', 'model_calls', 'input_tokens', 'output_tokens', 'cost_usd'): self.assertIn(key, metrics)

    def test_stage_refuses_a_stale_source_hash_or_too_many_assignments(self):
        p = dict(study.params('S1'), source_hash='stale')
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(AssertionError): worker.execute(p, Path(td) / 'out')
        with tempfile.TemporaryDirectory() as td, patch.object(study, 'assignments', return_value=self.fake_assignments(2)), \
                patch.dict(os.environ, {'STUDY_BUDGET_LEDGER': str(Path(td) / 'ledger')}):
            with self.assertRaises(AssertionError): worker.execute(study.params('P0'), Path(td) / 'out')

    # ------------------------------------------------------------------ gates and the chain
    def test_coordinator_gates(self):
        hub = FakeHub()
        for stage in ('P0', 'Q0', 'S1'):
            with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, stage)
        self.assertEqual(hub.rows, [])
        hub.add('S0'); ids = coordinator.enqueue(hub, 'P0'); self.assertEqual(len(ids), 1); self.assertEqual(hub.registered, 'sybil-split-opus')
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'P0')
        self.assertEqual(str(ctx.exception), 'batch_exists_no_replay')
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'S0')
        self.assertEqual(str(ctx.exception), 'batch_exists_no_replay')
        for kwargs in ({'status': 'failed'}, {'invalid': 1}, {'passed': 0}, {'source_hash': 'other'}):
            hub = FakeHub(); hub.add('P0', **kwargs)
            with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'Q0')
            self.assertEqual(str(ctx.exception), 'exact_runtime_qualification_required')
        hub = FakeHub(); hub.add('Q0'); hub.rows[0]['params']['batch'] = 'q0-000'; hub.add('Q0'); hub.rows[1]['params']['batch'] = 'q0-002'
        with self.assertRaises(coordinator.GateRefused): coordinator.enqueue(hub, 'S1')      # two qualifying runs: not exactly one
        hub = FakeHub(); hub.add('Q0'); hub.rows.append({'run': 'x/p', 'status': 'planned', 'params': {'batch': 'other'}, 'metrics': {}})
        with self.assertRaises(coordinator.GateRefused) as ctx: coordinator.enqueue(hub, 'S1')
        self.assertEqual(str(ctx.exception), 'queue_not_empty')
        hub = FakeHub(); hub.add('Q0'); self.assertEqual(len(coordinator.enqueue(hub, 'S1')), 1)
        with self.assertRaises(ValueError): study.params('S2')

    def chain_with(self, outcomes, stages=('S0', 'P0', 'Q0', 'S1'), q0_metrics=None):
        hub = FakeHub(); executed = []
        def fake_execute(p, out, run=None, backend=None, deadline=None, opener=None):
            executed.append(p['stage']); out = Path(out); out.mkdir(parents=True)
            ok = outcomes.get(p['stage'], 'done') == 'done'
            metrics = {'episodes': 1, 'invalid': 0, 'model_calls': 60, 'transport_attempts': 60, 'input_tokens': 240000, 'output_tokens': 2400,
                       'cost_usd': 1.008, 'qualification_passed': int(ok)}
            if p['stage'] == 'Q0' and q0_metrics: metrics.update(q0_metrics)
            (out / 'summary.json').write_text(json.dumps(dict(metrics, planned=1, graded=1, not_started=0, errors=[])))
            if outcomes.get(p['stage']) == 'crash': run.fail('x', **metrics); hub.settle(); raise RuntimeError('boom')
            (run.done if ok else run.fail)('x', **metrics); hub.settle()
            if not ok: raise worker.StageFailed('gate_failed')
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td}), patch.object(worker, 'execute', fake_execute), \
                patch('sys.stdout', io.StringIO()):
            os.environ.pop('STUDY_BUDGET_LEDGER', None)
            code = chain.run_chain(list(stages), sr=hub); status = chain.read_status()
            leftovers = [p.name for p in Path(td).iterdir() if p.name.endswith('.tmp')]
        self.assertEqual(leftovers, [])
        return code, status, executed, hub

    def test_chain_runs_all_stages_and_writes_status(self):
        code, status, executed, hub = self.chain_with({})
        self.assertEqual((code, status['state'], executed), (0, 'completed', ['S0', 'P0', 'Q0', 'S1']))
        self.assertTrue(status['all_stages_done']); self.assertTrue(status['stages']['S1']['projection']['within_cap'])
        for stage in study.STAGES:
            e = status['stages'][stage]
            for key in ('run', 'status', 'calls', 'input_tokens', 'output_tokens', 'cost_usd', 'started', 'ended'): self.assertIn(key, e)

    def test_chain_stops_at_a_failed_gate_and_queues_nothing_further(self):
        code, status, executed, hub = self.chain_with({'Q0': 'failed'})
        self.assertEqual((code, status['state'], status['stopped_stage'], status['reason']), (3, 'stopped_at_gate', 'Q0', 'gate_failed'))
        self.assertEqual(executed, ['S0', 'P0', 'Q0']); self.assertNotIn('S1', status['stages'])
        self.assertEqual([r['params']['stage'] for r in hub.rows], ['S0', 'P0', 'Q0']); self.assertEqual(hub.queue, [])
        code, status, executed, hub = self.chain_with({'P0': 'crash'})
        self.assertEqual((code, status['state'], status['stopped_stage'], executed), (1, 'stopped_at_gate', 'P0', ['S0', 'P0']))

    def test_chain_refuses_a_stage_whose_prerequisite_is_missing(self):
        code, status, executed, hub = self.chain_with({}, stages=('P0', 'Q0', 'S1'))
        self.assertEqual((code, status['state'], status['stopped_stage'], status['reason'], executed),
                         (3, 'stopped_at_gate', 'P0', 'exact_runtime_qualification_required', []))
        self.assertEqual(hub.rows, [])

    def test_chain_status_of_another_source_version_is_set_aside(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td}), patch('sys.stdout', io.StringIO()):
            os.environ.pop('STUDY_BUDGET_LEDGER', None)
            chain.write_status({'source_hash': 'an-older-source', 'stages': {'S0': {'status': 'done', 'run': 'old/1'}}, 'state': 'completed'})
            code = chain.run_chain(['P0'], sr=FakeHub()); status = chain.read_status()
            kept = json.loads((Path(td) / 'chain-status-an-older-sou.json').read_text())
        self.assertEqual((code, status['state'], list(status['stages']), status['source_hash']), (3, 'stopped_at_gate', ['P0'], study.source_hash()))
        self.assertEqual(kept['stages']['S0']['run'], 'old/1')

    def test_projection_gate_stops_before_s1(self):
        # Q0 at USD 0.10 per call projects 2,688 x 0.10 > USD 190
        code, status, executed, hub = self.chain_with({}, q0_metrics={'input_tokens': 1_500_000, 'output_tokens': 0, 'cost_usd': 6.0})
        self.assertEqual((code, status['state'], status['stopped_stage'], status['reason']), (3, 'stopped_at_gate', 'S1', 'projection_exceeds_cap'))
        self.assertEqual(executed, ['S0', 'P0', 'Q0']); self.assertEqual([r['params']['stage'] for r in hub.rows], ['S0', 'P0', 'Q0'])
        p = status['stages']['S1']['projection']; self.assertGreater(p['projected_usd'], p['remaining_usd'])
        self.assertFalse(chain.projection({'metrics': {}}).get('within_cap'))

    def test_stage_lists_must_be_ordered_and_contiguous(self):
        self.assertEqual(chain.parse_stages('S0'), ['S0']); self.assertEqual(chain.parse_stages('p0,q0,s1'), ['P0', 'Q0', 'S1'])
        for bad in ('S1,S0', 'S0,Q0', 'S2', '', 'S0,S0'):
            with self.assertRaises(SystemExit): chain.parse_stages(bad)

    def test_status_and_verify_print_one_json_line_and_verify_fails_without_a_chain(self):
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, {'STUDY_RESULTS_DIR': td}):
            os.environ.pop('STUDY_BUDGET_LEDGER', None)
            for fn, code in ((chain.show_status, 0), (lambda: chain.verify(FakeHub()), 1)):
                out = io.StringIO()
                with patch('sys.stdout', out): self.assertEqual(fn(), code)
                lines = out.getvalue().strip().splitlines(); self.assertEqual(len(lines), 1); json.loads(lines[-1])

    def test_rehearsal_refuses_a_hub_that_is_not_local(self):
        self.assertEqual(rehearse.require_local('http://127.0.0.1:8791'), 'http://127.0.0.1:8791')
        for url in ('http://10.0.0.5:8700', 'https://hub.example.org', 'http://localhost:8700', 'http://127.0.0.1.example.org:1', '', None):
            with self.assertRaises(SystemExit): rehearse.require_local(url)
        with self.assertRaises(AssertionError): rehearse.Stub('plurality')(type('R', (), {'full_url': 'https://example.org/v1/messages', 'data': b'{}'})())

    # ---------------------------------------------------------------------------- analysis
    def synthetic(self, wrong, missing=()):
        rows = []
        for family in D['families']:
            for task in D['roots']['comparison'][family][:3]:
                for rate in D['attacker']['attacker_pass']:
                    for arm in D['arms']:
                        for checks in ([0] if arm == 'no_verification' else D['check_budgets']):
                            for k in KS:
                                v = wrong(family, task, rate, arm, checks, k); status = 'not_started' if (task, arm, checks, k, rate) in missing else 'completed'
                                e = {'rare_wrong': v, 'rare_accuracy': 1 - v, 'rare_abstain': 0.0, 'rare_fabricated': v, 'task_accuracy': 1 - v / 2}
                                r = {'family': family, 'task': task, 'k': k, 'arm': arm, 'checks': checks, 'attacker_pass': rate, 'kind': 'pilot',
                                     'status': status, 'packet_hash': f'{task}', 'backend': 'anthropic',
                                     'admission': {f: 0.0 for f in analyze.ADMISSION}}
                                if status == 'completed': r.update(evaluation=e, scripted_evaluation=dict(e, rare_wrong=0.0), identity_evaluation=e, answer={'values': {}})
                                rows.append(r)
        return rows

    def test_primary_contrast_sign_weighting_and_interval(self):
        def wrong(family, task, rate, arm, checks, k):
            if (rate, checks, k) == (0.1, 12, 27) and arm == 'degree': return 1.0 if family == 'ring' else 1 / 3
            return 0.0
        a = analyze.analyze(self.synthetic(wrong))
        self.assertAlmostEqual(a['primary']['estimate'], (1.0 + 1 / 3) / 2); self.assertAlmostEqual(a['primary']['by_family']['ring']['mean'], 1.0)
        self.assertEqual(a['primary']['bounds_all_assigned'], [a['primary']['estimate']] * 2)
        self.assertEqual(a['primary']['interval'], [a['primary']['estimate']] * 2)      # no variation between roots
        self.assertAlmostEqual(a['secondary']['primary_under_unreliable_checks']['estimate'], 0.0)
        self.assertAlmostEqual(a['secondary']['primary_by_plurality']['estimate'], 0.0)
        self.assertAlmostEqual(a['secondary']['degree_minus_random']['estimate'], a['primary']['estimate'])
        neg = analyze.analyze(self.synthetic(lambda f, t, r, arm, c, k: 1.0 if (arm, c, k, r) == ('coverage', 12, 27, 0.1) else 0.0))
        self.assertAlmostEqual(neg['primary']['estimate'], -1.0)
        gap = [g for g in a['model_minus_plurality'] if (g['arm'], g['checks'], g['k'], g['attacker_pass'], g['field']) == ('degree', 12, 27, 0.1, 'rare_wrong')][0]
        self.assertAlmostEqual(gap['model_minus_plurality'], (1.0 + 1 / 3) / 2)
        self.assertEqual(a['test_retest'], {'packets_seen_more_than_once': 6, 'calls_in_those_groups': 6 * 56, 'groups_with_identical_answers': 6})

    def test_missing_outcomes_are_bounded_not_dropped(self):
        task = D['roots']['comparison']['ring'][0]
        rows = self.synthetic(lambda *a: 0.0, missing={(task, 'degree', 12, 27, 0.1)}); a = analyze.analyze(rows)
        p = a['primary']; self.assertEqual(p['by_family']['ring']['roots'], 2); self.assertEqual(p['assigned_roots'], {'ring': 3, 'community': 3})
        self.assertAlmostEqual(p['estimate'], 0.0); self.assertAlmostEqual(p['bounds_all_assigned'][0], 0.0); self.assertAlmostEqual(p['bounds_all_assigned'][1], (1 / 3) / 2)
        cell = [c for c in a['cells'] if (c['family'], c['arm'], c['checks'], c['k'], c['attacker_pass']) == ('ring', 'degree', 12, 27, 0.1)][0]
        self.assertEqual((cell['assigned'], cell['valid'], cell['not_started']), (3, 2, 1)); self.assertEqual(cell['rare_wrong_bounds_all_assigned'], [0.0, 1 / 3])
        self.assertEqual(a['denominators']['assigned'], len(rows)); self.assertEqual(a['denominators']['not_started'], 1)
        empty = analyze.analyze([dict(r, status='not_started') for r in rows])
        self.assertIsNone(empty['primary']['estimate']); self.assertEqual(empty['primary']['bounds_all_assigned'], [-2.0, 2.0])

    # ------------------------------------------------------------------------------ frames
    def test_frames_for_empty_partial_failed_and_final_states(self):
        s0 = scripted_rows('S0'); q0 = scripted_rows('Q0')
        partial = s0[:700] + [dict(s0[700], status='failed', error='x')] + [dict(r, status='not_started') for r in s0[701:900]]
        for rows, total, stage in (([], 2688, 'S1'), (partial, 1853, 'S1'), (s0, 1853, 'S0'), ([], 60, 'Q0'), (q0, 60, 'Q0'),
                                   ([dict(q0[0], status='failed')], 60, 'Q0'), ([], 1, 'P0'), (scripted_rows('P0'), 1, 'P0')):
            self.assertEqual(render.frame(rows, total, stage, 3.0, {'actual_usd': 1.0}).size, (1800, 1200))
        self.assertIsNotNone(render.font(20))
        with patch.object(render, 'FONT_PATHS', ('/nonexistent/font.ttf',)):
            render.font.cache_clear(); self.assertEqual(render.frame([], 10, 'S1').size, (1800, 1200)); render.font.cache_clear()
        means = render.cell_means(s0); key = ('ring', 0.1, 'degree', 12, 27)
        want = [r for r in s0 if r['kind'] == 'pilot' and (r['family'], r['attacker_pass'], r['arm'], r['checks'], r['k']) == key]
        self.assertEqual(means[key]['n'], 16); self.assertAlmostEqual(means[key]['wrong'], sum(r['evaluation']['rare_wrong'] for r in want) / 16)

    def test_replay_gif_decodes_and_ends_on_the_final_frame(self):
        from PIL import Image
        rows = [dict(r, elapsed_seconds=i, study_accounting={}) for i, r in enumerate(scripted_rows('S0')[:400])]
        with tempfile.TemporaryDirectory() as td:
            n = render.replay(rows, Path(td), 'S0', 1853, {}, frames=6)
            with Image.open(Path(td) / 'replay.gif') as gif:
                self.assertEqual((n, gif.n_frames, gif.size), (7, 7, (1800, 1200)))
                for i in range(gif.n_frames): gif.seek(i); gif.load()
            with Image.open(Path(td) / 'final_frame.png') as final: self.assertEqual(final.size, (1800, 1200))
            self.assertTrue((Path(td) / 'initial_frame.png').exists())


if __name__ == '__main__':
    unittest.main()
