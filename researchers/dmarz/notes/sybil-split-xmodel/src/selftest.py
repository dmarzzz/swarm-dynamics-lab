"""Offline checks. No network, no model call, no hub. `python3 src/selftest.py` prints the
standard unittest summary ("Ran N tests ... OK") on stderr.

World, packet, fixture, gate, manifest, analysis and frame tests are the parent's (sybil-split-opus
selftest) with the Anthropic adapter tests removed; the reference OpenRouter adapter's own tests
(test_provider.py) run as part of this suite; the tests at the end are new: byte identity with the
parent, the two-model configuration, the answer validator's harmless variants, the probe through the
real adapter with a stubbed endpoint, and per-model gates."""
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
# The suite tests the code, not the chain it runs in: the launcher's setup step sets STUDY_MODEL,
# STUDY_PROVIDER and STUDY_REPLICATION for the chosen configuration, and the tests must give the same result
# under any of them. Tests that need a configuration set it themselves with patch.dict.
for _name in ('STUDY_MODEL', 'STUDY_PROVIDER', 'STUDY_REPLICATION'):
    os.environ.pop(_name, None)

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
from test_provider import Request, Answers, Transport, Billing, LedgerRules  # noqa: E402,F401  (the OpenRouter adapter's own tests)
from test_openai_provider import (Request as OpenAIRequest, Cost as OpenAICost, Answers as OpenAIAnswers,  # noqa: E402,F401
                                  Transport as OpenAITransport, Billing as OpenAIBilling, StubServer as OpenAIStubServer,
                                  LedgerRules as OpenAILedgerRules)   # the OpenAI adapter's own tests

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
            r = worker.row_base(a, {'stage': stage, 'backend': 'scripted', 'code': 'test', 'source_hash': 'test', 'batch': 'test', 'model': study.model_name()}, 'test')
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
        g = study.probe_gate([row]); self.assertEqual((g['count'], g['passed'], g['input_tokens'], g['output_tokens']), (1, True, 5, 6))
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
        self.assertTrue(all(len(json.dumps(study.SYSTEM)) + len(json.dumps(a['packet'])) + 2000 < D['budget']['max_input_bytes'] for a in s1))

    def test_source_hash_covers_code_and_design_only(self):
        with patch.object(Path, 'read_bytes', lambda self: self.name.encode()):
            names = study.source_hash()
        expected = ['design.yaml', 'experiment.yaml', 'requirements.txt'] + sorted(p.name for p in (study.ROOT / 'src').glob('*.py'))
        import hashlib
        self.assertEqual(names, study.digest([(n, hashlib.sha256(n.encode()).hexdigest()) for n in expected]))
        self.assertNotIn('manifest.json', expected); self.assertIn('rehearse.py', expected)

    # ----------------------------------------------------------------------------- adapter

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

    # -------------------------------------------------- new: parent identity and the two models
    def test_simulator_is_the_parent_file_byte_for_byte(self):
        import hashlib
        pinned = D['parent']['files_sha256']
        self.assertEqual(hashlib.sha256((study.ROOT / 'src' / 'sim.py').read_bytes()).hexdigest(), pinned['src/sim.py'])
        self.assertEqual(study.parent_files(), [])

    def test_system_prompt_is_the_parent_prompt_plus_the_shape(self):
        import ast
        tree = ast.parse((study.parent_dir() / 'src' / 'provider.py').read_text())
        parent = next(n.value.value for n in tree.body if isinstance(n, ast.Assign) and getattr(n.targets[0], 'id', None) == 'SYSTEM')
        self.assertEqual(parent, study.PARENT_SYSTEM)
        self.assertEqual(study.SYSTEM, parent + '\n\n' + study.SHAPE)
        for word in study.FORBIDDEN: self.assertNotIn(word, study.SHAPE)

    def test_probe_and_qualification_packets_equal_the_parents_own_code(self):
        parent = study.parent_packets()
        self.assertEqual(parent['source_hash'], D['parent']['source_hash'])
        for stage in ('P0', 'Q0'):
            mine = study.assignments(stage)
            self.assertEqual({a['id']: a['packet_hash'] for a in mine}, parent['stages'][stage])
            for a in mine:   # the user message is the parent's message: its SHA-256 is the parent's packet hash
                import hashlib
                self.assertEqual(hashlib.sha256(study.user_text(a['packet']).encode()).hexdigest(), a['packet_hash'])

    def test_parent_records_cover_exactly_the_s1_ids(self):
        rec = study.parent_s1_records()
        self.assertEqual(len(rec), 2688); self.assertTrue(all(r['status'] == 'completed' for r in rec.values()))
        self.assertEqual(set(rec), set(manifest.load()['stages']['S1']['ids'][i].split(':')[0] for i in range(2688)))

    def test_a_changed_parent_file_is_refused(self):
        with patch.dict(D['parent'], {'files_sha256': dict(D['parent']['files_sha256'], **{'src/sim.py': '0' * 64})}):
            self.assertEqual(study.parent_files(), ['parent_file_changed:src/sim.py'])
            self.assertEqual(study.check_parent_identity(()), ['parent_file_changed:src/sim.py'])

    def test_two_models_each_with_own_batches_and_route(self):
        self.assertEqual(D['model_ladder'], ['qwen/qwen3.7-flash', 'gpt-6-sol']); self.assertEqual(D['model'], D['model_ladder'][0])
        with patch.dict(os.environ, {'STUDY_MODEL': ''}):
            self.assertEqual(study.model_name(), 'qwen/qwen3.7-flash')
            self.assertEqual([study.batch(s) for s in study.STAGES], ['s0-001-qwen', 'p0-001-qwen', 'q0-001-qwen', 's1-001-qwen'])
            c = study.adapter_config(); sel = json.loads((study.ROOT.parent / 'overnight-program-2026-10-04/selected-model.json').read_text())
            self.assertEqual(c['request_template'], sel['request_template']); self.assertEqual(c['canonical_model'], sel['observed_canonical_slug'])
            self.assertEqual((c['budget']['aggregate_usd'], c['budget']['max_output_tokens'], c['budget']['input_usd_per_million'],
                              c['budget']['output_usd_per_million'], c['budget']['max_calls']['S1']), (3, 1000, 0.03, 0.13, 2688))
            self.assertEqual(study.params('P0')['backend'], 'openrouter'); self.assertEqual(study.params('S0')['backend'], 'scripted')
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol'}):
            self.assertEqual(study.batch('S1'), 's1-001-sol'); self.assertEqual(study.params('Q0')['model'], 'gpt-6-sol')
            self.assertEqual(study.params('Q0')['backend'], 'openai'); self.assertEqual(study.adapter_config()['request_template']['reasoning_effort'], 'low')
            self.assertEqual(study.adapter_config()['request_template']['max_completion_tokens'], 2000)
            import openai_provider
            c = study.adapter_config(); self.assertEqual(c['budget']['prices'], openai_provider.PRICES['gpt-6-sol'])
            self.assertEqual(c['budget']['aggregate_usd'], 90); self.assertIs(openai_provider.check_config(c), c)
            self.assertEqual(c['request_template'], {'model': 'gpt-6-sol', 'reasoning_effort': 'low', 'max_completion_tokens': 2000,
                                                     'response_format': {'type': 'json_object'}})
            self.assertIs(study.route(), openai_provider); self.assertEqual(study.route().BILLING_STOP, 'provider_billing_stopped')
        with patch.dict(os.environ, {'STUDY_MODEL': 'claude-opus-5-5'}):
            with self.assertRaises(ValueError): study.model_name()
        self.assertEqual(D['budget']['max_failed'], max(3, -(-2688 // 100)))

    def test_harmless_variants_of_a_correct_answer_pass_and_schema_violations_fail(self):
        a = study.assignments('P0')[0]; good = study.scripted(a['packet'])
        floats = {'values': {k: (None if v is None else float(v)) for k, v in reversed(list(good['values'].items()))}}
        self.assertEqual(study.validate(floats), good)
        self.assertTrue(study.evaluate(a, floats)['exact_packet'])
        for bad in ({'values': {k: (None if v is None else str(v)) for k, v in good['values'].items()}},
                    dict(good, reasoning='x'), good['values'], {'values': dict(good['values'], **{'6': 1})},
                    {'values': {k: (None if v is None else v + 0.5) for k, v in good['values'].items()}}):
            with self.assertRaises(ValueError): study.validate(bad)

    def probe_through_adapter(self, content, provider_name='Alibaba', model='', replication='', reasoning=0):
        """P0 run by the worker with the real adapter of `model` (and `replication`) and a stubbed endpoint returning `content`."""
        a = study.assignments('P0')[0]; conf = {'STUDY_MODEL': model, 'STUDY_REPLICATION': replication}
        with patch.dict(os.environ, conf): mod = study.route(); slug = study.adapter_config()['canonical_model']
        def opener(request, timeout=None):
            body = json.loads(request.data)
            self.assertEqual(request.full_url, mod.URL); self.assertEqual(list(body), list(mod.BODY_KEYS))
            self.assertEqual({k: body[k] for k in body if k != 'messages'}, study.adapter_config()['request_template'])
            self.assertEqual(body['messages'], [{'role': 'system', 'content': study.SYSTEM}, {'role': 'user', 'content': study.user_text(a['packet'])}])
            route = {'provider': provider_name} if mod is provider else {}
            return rehearse.Response(json.dumps({'id': 'gen-t', 'model': slug, **route,
                'choices': [{'index': 0, 'finish_reason': 'stop', 'message': {'role': 'assistant', 'content': content}}],
                'usage': {'prompt_tokens': 4000, 'completion_tokens': 40, 'completion_tokens_details': {'reasoning_tokens': reasoning}}}).encode())
        with tempfile.TemporaryDirectory() as td, patch.dict(os.environ, dict(conf, **{mod.KEY_ENV: 'k', provider.LEDGER_ENV: str(Path(td) / 'ledger')})):
            try:
                return worker.execute(study.params('P0'), Path(td) / 'p0', opener=opener, clock=lambda: 0.0, sleep=lambda s: None)
            except worker.StageFailed as exc:
                return {'passed': False, 'reason': str(exc)}

    def test_probe_accepts_harmless_variants_and_records_the_response(self):
        good = study.scripted(study.assignments('P0')[0]['packet'])['values']
        text = '\n {"values" : {' + ', '.join(f'"{k}": {"null" if v is None else float(v)}' for k, v in reversed(list(good.items()))) + '}}  '
        s = self.probe_through_adapter(text)
        self.assertTrue(s['passed']); self.assertEqual(s['probe']['response_provider'], 'Alibaba')
        self.assertEqual(s['probe']['finish_reason'], 'stop'); self.assertAlmostEqual(s['probe']['tokens_per_byte'], 4000 / s['probe']['request_bytes'])
        self.assertEqual(s['model_calls'], 1)

    def test_probe_fails_on_schema_violations_and_a_wrong_provider(self):
        good = study.scripted(study.assignments('P0')[0]['packet'])
        self.assertFalse(self.probe_through_adapter(json.dumps({'values': {k: str(v) for k, v in good['values'].items()}}))['passed'])
        self.assertFalse(self.probe_through_adapter('```json\n' + json.dumps(good) + '\n```')['passed'])
        self.assertFalse(self.probe_through_adapter(json.dumps(good), provider_name='Other')['passed'])
        self.assertTrue(self.probe_through_adapter(json.dumps(good))['passed'])

    def test_gpt_6_sol_probe_through_its_adapter(self):
        good = study.scripted(study.assignments('P0')[0]['packet'])
        s = self.probe_through_adapter(json.dumps(good), model='gpt-6-sol')
        self.assertTrue(s['passed']); self.assertEqual(s['params']['model'], 'gpt-6-sol'); self.assertEqual(s['params']['batch'], 'p0-001-sol')
        self.assertFalse(self.probe_through_adapter(json.dumps({'values': {k: str(v) for k, v in good['values'].items()}}), model='gpt-6-sol')['passed'])

    def test_effort_none_follow_up_configuration(self):
        import openai_provider
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_REPLICATION': 'r1'}):
            self.assertEqual(study.config_name(), 'gpt-6-sol/r1'); self.assertEqual(study.model_name(), 'gpt-6-sol')
            self.assertEqual([study.batch(s) for s in study.STAGES], ['s0-001-solnone', 'p0-001-solnone', 'q0-001-solnone', 's1-001-solnone'])
            c = study.adapter_config(); self.assertIs(openai_provider.check_config(c), c)
            # only reasoning_effort differs from the effort-low configuration; no sampling parameter is sent
            self.assertEqual(c['request_template'], {'model': 'gpt-6-sol', 'reasoning_effort': 'none', 'max_completion_tokens': 2000,
                                                     'response_format': {'type': 'json_object'}})
            self.assertFalse(set(c['request_template']) & set(openai_provider.SAMPLING_KEYS))
            self.assertEqual((c['model'], c['budget']['aggregate_usd'], c['budget']['prices']), ('gpt-6-sol', 90, openai_provider.PRICES['gpt-6-sol']))
            self.assertEqual(study.params('Q0')['model'], 'gpt-6-sol/r1')
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_REPLICATION': ''}):
            low = study.adapter_config()['request_template']
        self.assertEqual({k: v for k, v in low.items() if k != 'reasoning_effort'}, {k: v for k, v in c['request_template'].items() if k != 'reasoning_effort'})
        for bad in ({'STUDY_MODEL': '', 'STUDY_REPLICATION': 'r1'}, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_REPLICATION': 'r2'}):
            with patch.dict(os.environ, bad):
                with self.assertRaises(ValueError): study.config_name()

    def test_effort_none_probe_through_its_adapter(self):
        good = study.scripted(study.assignments('P0')[0]['packet'])
        s = self.probe_through_adapter(json.dumps(good), model='gpt-6-sol', replication='r1')
        self.assertTrue(s['passed']); self.assertEqual((s['params']['model'], s['params']['batch']), ('gpt-6-sol/r1', 'p0-001-solnone'))
        self.assertFalse(self.probe_through_adapter(json.dumps(good), model='gpt-6-sol', replication='r1', reasoning=12)['passed'])

    def test_suite_does_not_depend_on_the_launch_configuration(self):
        base = study.source_hash()
        for conf in ({}, {'STUDY_MODEL': 'gpt-6-sol'}, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_REPLICATION': 'r1'}, {'STUDY_PROVIDER': 'openai'}):
            with patch.dict(os.environ, conf):
                self.assertEqual(study.source_hash(), base)
                self.assertEqual([a['packet_hash'] for a in study.assignments('P0')], [a['packet_hash'] for a in scripted_rows('P0')])
                self.assertEqual(study.SYSTEM, study.PARENT_SYSTEM + '\n\n' + study.SHAPE)

    def test_gates_look_only_at_this_models_runs(self):
        hub = FakeHub()
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol'}): hub.add('S0'); hub.add('P0')
        with patch.dict(os.environ, {'STUDY_MODEL': ''}):
            with self.assertRaises(coordinator.GateRefused): coordinator.check(hub, 'P0')      # the other model's S0 does not count
            hub.add('S0'); p, before = coordinator.check(hub, 'P0'); self.assertEqual(p['batch'], 'p0-001-qwen')
            hub.rows.append({'run': 'x/other', 'status': 'running', 'params': dict(p, model='gpt-6-sol', batch='q0-001-sol'), 'metrics': {}})
            coordinator.check(hub, 'P0')                                                      # the other model running: allowed
            hub.rows.append({'run': 'x/planned', 'status': 'planned', 'params': dict(p, model='gpt-6-sol', batch='s1-001-sol'), 'metrics': {}})
            with self.assertRaises(coordinator.GateRefused): coordinator.check(hub, 'P0')      # a planned run of either model: refused
        hub = FakeHub()
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol'}): hub.add('S0')
        with patch.dict(os.environ, {'STUDY_MODEL': 'gpt-6-sol', 'STUDY_REPLICATION': 'r1'}):
            with self.assertRaises(coordinator.GateRefused): coordinator.check(hub, 'P0')      # the effort-low S0 does not admit effort none
            hub.add('S0'); self.assertEqual(coordinator.check(hub, 'P0')[0]['batch'], 'p0-001-solnone')


if __name__ == '__main__':
    unittest.main()
