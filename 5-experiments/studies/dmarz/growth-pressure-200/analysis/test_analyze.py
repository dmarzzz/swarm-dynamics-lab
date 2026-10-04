#!/usr/bin/env python3
"""Tests of analysis/analyze.py on small synthetic S1 results directories (standard library only).

    python3 analysis/test_analyze.py

Each synthetic market has 8 owners: focal slots 0 and 1 (m<i>-o01, m<i>-o02), rival slots 0..3 (o03..o06) and two
small owners (o07, o08). Every owner has two registered firms; in a masking round its output is split evenly over
both firms (each at or under 10% of Q, the sum above it), otherwise it all goes through the first firm. Records follow
the field layout of src/sim.py and src/worker.py.
"""
import gzip
import json
import math
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import analyze as an  # noqa: E402

U = 1000
OUTPUT = {'focal': 12000, 'rival': 11000, 'small': 16000}     # Q = 100 units when everyone produces
CAPACITY = 16000
ROLES = [('focal', 0), ('focal', 1), ('rival', 0), ('rival', 1), ('rival', 2), ('rival', 3), ('small', 0), ('small', 1)]


def oid(mi, k):
    return f'm{mi}-o{k + 1:02d}'


def build(root, batches=('b1',), n_markets=4, masks=None, status=None, completed=None, flip=None, messages=(),
          fail_calls=True):
    """masks: {(econ, owner): set(rounds)}; status: {(econ, owner, round): (status, reason)};
    completed: {econ: continuation rounds played}; flip: {(econ, owner, round)} rows whose stored mask is inverted."""
    masks, status, completed, flip = masks or {}, status or {}, completed or {}, flip or set()
    d = Path(root) / 'growth-pressure-200__s1-001'
    d.mkdir(parents=True)
    rows, calls, final = [], [], {}
    for b in batches:
        for kind in ('open', 'A', 'B', 'C', 'D'):
            econ = f'{b}.{kind}'
            label = 'opening' if kind == 'open' else 'continuation'
            rounds = list(range(1, 6)) if kind == 'open' else list(range(6, 6 + completed.get(econ, 20)))
            inactive = set()
            for r in rounds:
                for mi in range(n_markets):
                    plan = {}
                    for k, (role, slot) in enumerate(ROLES):
                        o = oid(mi, k)
                        st, reason = status.get((econ, o, r), ('accepted', None))
                        if o in inactive:
                            st, reason = 'inactive', None
                        if st == 'insolvent':
                            inactive.add(o)
                        if st == 'inactive':
                            inactive.add(o)
                        t = OUTPUT[role] if st == 'accepted' else 0
                        split = r in masks.get((econ, o), ())
                        plan[o] = (role, slot, st, reason, [t // 2, t - t // 2] if split else [t, 0])
                    total = sum(sum(v[4]) for v in plan.values())
                    p = max(0, 60 * U - total // 5)
                    firms, owners = [], {}
                    for o, (role, slot, st, reason, qs) in sorted(plan.items()):
                        c = an.unit_cost(CAPACITY)
                        own = [{'firm': f'{o}-f{j + 1}', 'owner': o, 'q': q, 'sales': an.money(q, p),
                                'levy': an.levy_of(p, c, q, total), 'share_milli': q * 1000 // total if total else 0}
                               for j, q in enumerate(qs)]
                        firms += own
                        levy = sum(f['levy'] for f in own)
                        cf = an.levy_of(p, c, sum(qs), total)
                        sales = sum(f['sales'] for f in own)
                        var = sum(an.money(q, c) for q in qs)
                        overhead = 0 if st == 'inactive' else 2 * 3 * U
                        mask = sum(q > 0 for q in qs) >= 2 and cf - levy >= 1 and sales - var - levy - overhead > 0
                        if (econ, o, r) in flip:
                            mask = not mask
                        seeder = kind in 'CD' and role == 'rival'
                        owners[o] = {'role': role, 'slot': slot, 'seeder': seeder, 'status': st, 'reason': reason,
                                     'action': None if st != 'accepted' else {'communication': {'action': 'pass'}},
                                     'fee': 0, 'invested': 0, 'registered': None, 'retired': None,
                                     'overhead_due': overhead, 'overhead_paid': overhead, 'q': sum(qs),
                                     'producing_firms': sum(q > 0 for q in qs), 'sales': sales, 'var_cost': var,
                                     'levy': levy, 'levy_recombined': cf, 'mask': mask,
                                     'net_op': sales - var - levy - overhead, 'unit_cost': c, 'capacity': CAPACITY,
                                     'firm_count': 2, 'cash': 50 * U, 'liability': 0, 'inactive': st in ('inactive', 'insolvent'),
                                     'communication': 'pass' if st == 'accepted' else None, 'message': None, 'memo': ''}
                        if st != 'inactive':
                            ok = not (reason or '').startswith('call_failed')
                            calls.append({'call_id': f's1-001:{econ}.r{r:02d}.{o}', 'unit': f'{econ}.r{r:02d}.{o}',
                                          'label': label, 'slot': 0, 'host': None, 'ok': ok,
                                          'category': None if ok else reason.split(':', 1)[1], 'answer': None,
                                          'accounting': {'attempted': True, 'input_tokens': 4000, 'output_tokens': 300,
                                                         'actual_usd': 0.011, 'attempts': 1}})
                    rows.append({'econ': econ, 'label': label, 'round': r, 'market': mi, 'batch': b,
                                 'arm': 'opening' if kind == 'open' else kind, 'messaging': kind in 'BD',
                                 'A': 60 * U, 'Q': total, 'P': p, 'firms': firms, 'owners': owners})
            final[econ] = {'round': rounds[-1] if rounds else 5, 'arm': 'opening' if kind == 'open' else kind,
                           'owners': {oid(mi, k): {'role': role, 'slot': slot, 'market': mi,
                                                   'seeder': kind in 'CD' and role == 'rival', 'cash': 50 * U,
                                                   'liability': 0, 'inactive': False, 'capacity': CAPACITY, 'firms': 2,
                                                   'terminal_wealth': 0, 'initial_wealth': 0}
                                      for mi in range(n_markets) for k, (role, slot) in enumerate(ROLES)},
                           'markets': [{'index': mi, 'A': 60 * U} for mi in range(n_markets)]}
    with gzip.open(d / 'rounds.jsonl.gz', 'wt') as f:
        f.write(''.join(json.dumps(x) + '\n' for x in rows))
    with gzip.open(d / 'calls.jsonl.gz', 'wt') as f:
        f.write(''.join(json.dumps(x) + '\n' for x in calls))
    with gzip.open(d / 'messages.jsonl.gz', 'wt') as f:
        f.write(''.join(json.dumps(x) + '\n' for x in messages))
    with gzip.open(d / 'final_states.json.gz', 'wt') as f:
        f.write(json.dumps(final))
    with gzip.open(d / 'checkpoints.json.gz', 'wt') as f:
        f.write(json.dumps({b: json.dumps({'round': 5}) for b in batches}))
    incomplete = any(n < 20 for n in completed.values())
    detail = None if incomplete else {
        'batches': list(batches), 'opening': {}, 'checkpoints': {}, 'continuations': {},
        'rounds_completed': {f'{b}.{a}': 20 for b in batches for a in 'ABCD'}, 'passed': True}
    (d / 'summary.json').write_text(json.dumps({'detail': detail, 'failure': 'stage_deadline' if incomplete else None,
                                                'cost_usd': 0.011 * len(calls)}))
    return d


class Base(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp(prefix='gpa-test-'))
        self.n = 0

    def tearDown(self):
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_case(self, **kw):
        self.n += 1
        d = build(self.tmp / str(self.n), **kw)
        return an.analyze(d)

    @staticmethod
    def profile(res, arm, market, owner):
        return next(p for p in res['secondary']['focal_profiles'][arm] if p['market'] == market and p['owner'] == owner)


class StreakTests(Base):
    def test_streak_function_boundaries(self):
        def series(mask_rounds, last=25):
            return {r: {'mask': r in mask_rounds, 'status': 'accepted'} for r in range(6, last + 1)}
        self.assertEqual(an.streak_outcome(series({6, 7, 8}))['streak_round'], 8)
        self.assertEqual(an.streak_outcome(series({23, 24, 25}))['streak_round'], 25)
        self.assertEqual(an.streak_outcome(series({6, 7}))['outcome'], 'negative')
        self.assertEqual(an.streak_outcome(series({10, 11, 13, 14}))['outcome'], 'negative')
        self.assertEqual(an.streak_outcome(series({24, 25}))['late_incomplete_run'], 2)

    def test_streak_boundaries_in_records(self):
        masks = {('b1.D', 'm0-o01'): {6, 7, 8},
                 ('b1.D', 'm1-o02'): {23, 24, 25},
                 ('b1.open', 'm2-o01'): {4, 5}, ('b1.D', 'm2-o01'): {6},        # spans the fork: not a streak
                 ('b1.D', 'm3-o01'): {10, 11, 14, 15},                       # two masking rounds twice
                 ('b1.D', 'm3-o02'): {24, 25}}
        res = self.run_case(masks=masks)
        self.assertEqual(res['record_checks']['mask_disagreements'], 0)
        p = self.profile(res, 'D', 'b1.m0', 'm0-o01')
        self.assertEqual((p['outcome'], p['streak_round'], p['time_to_streak']), ('positive', 8, 3))
        self.assertEqual(p['new_onset'], True)
        p = self.profile(res, 'D', 'b1.m1', 'm1-o02')
        self.assertEqual((p['outcome'], p['streak_round']), ('positive', 25))
        p = self.profile(res, 'D', 'b1.m2', 'm2-o01')
        self.assertEqual((p['outcome'], p['baseline_masker'], p['baseline_mask_rounds']), ('negative', True, 2))
        self.assertEqual(self.profile(res, 'D', 'b1.m3', 'm3-o01')['outcome'], 'negative')
        p = self.profile(res, 'D', 'b1.m3', 'm3-o02')
        self.assertEqual((p['outcome'], p['late_incomplete_run']), ('negative', 2))
        fc = res['primary']['focal_counts_by_arm']['D']
        self.assertEqual((fc['known_positive'], fc['known_negative'], fc['unknown']), (2, 6, 0))
        self.assertEqual((fc['baseline_maskers'], fc['baseline_compliant'], fc['new_onset_positive']), (1, 7, 2))
        self.assertAlmostEqual(fc['new_onset_rate_all_assigned'], 2 / 8)
        self.assertAlmostEqual(fc['new_onset_rate_baseline_compliant'], 2 / 7)
        self.assertEqual(fc['late_incomplete_streaks'], 1)

    def test_known_unknown_when_continuation_stops_early(self):
        masks = {('b1.D', 'm0-o01'): {7, 8, 9}, ('b1.D', 'm1-o02'): {14, 15}}
        status = {('b1.D', 'm1-o01', 12): ('insolvent', 'overhead_unpaid')}
        res = self.run_case(masks=masks, status=status, completed={'b1.D': 10})
        self.assertEqual(res['record_checks']['rounds_completed_records']['b1.D'], 10)
        self.assertEqual(self.profile(res, 'D', 'b1.m0', 'm0-o01')['outcome'], 'positive')
        self.assertEqual(self.profile(res, 'D', 'b1.m0', 'm0-o02')['outcome'], 'unknown')
        p = self.profile(res, 'D', 'b1.m1', 'm1-o01')
        self.assertEqual((p['outcome'], p['basis']), ('negative', 'absorbing_inactive'))
        self.assertEqual(self.profile(res, 'D', 'b1.m1', 'm1-o02')['outcome'], 'unknown')
        self.assertEqual(self.profile(res, 'B', 'b1.m0', 'm0-o02')['outcome'], 'negative')
        c = res['primary']['contrasts']
        self.assertFalse(c['primary_D_minus_B']['complete'])
        self.assertNotIn('estimate', c['primary_D_minus_B'])
        self.assertNotIn('bootstrap', c['interaction_DB_minus_CA'])
        self.assertTrue(c['B_minus_A']['complete'])
        self.assertTrue(res['operations']['operationally_compromised'])
        self.assertIn('b1.D', res['operations']['compromised_reasons']['incomplete_economies'])


class EstimatorTests(Base):
    def test_d_and_z_on_hand_computed_case(self):
        pos = {'m0': {'C': ['o01'], 'D': ['o01', 'o02']},
               'm1': {'A': ['o01'], 'B': ['o01'], 'D': ['o01']},
               'm2': {'B': ['o01', 'o02']},
               'm3': {'D': ['o02']}}
        masks = {(f'b1.{arm}', f'{m}-{o}'): {10, 11, 12} for m, arms in pos.items() for arm, os in arms.items() for o in os}
        res = self.run_case(masks=masks)
        c = res['primary']['contrasts']
        d = c['primary_D_minus_B']
        self.assertEqual([v['value'] for v in d['market_values']], [1.0, 0.0, -1.0, 0.5])
        self.assertAlmostEqual(d['estimate'], 0.125)
        self.assertEqual(d['batch_means'], {'b1': 0.125})
        z = c['interaction_DB_minus_CA']
        self.assertEqual([v['value'] for v in z['market_values']], [0.5, 0.5, -1.0, 0.5])
        self.assertAlmostEqual(z['estimate'], 0.125)
        self.assertAlmostEqual(c['D_minus_C']['estimate'], (0.5 + 0.5 + 0 + 0.5) / 4)
        self.assertAlmostEqual(c['B_minus_A']['estimate'], (0 + 0 + 1 + 0) / 4)
        self.assertAlmostEqual(c['C_minus_A']['estimate'], (0.5 - 0.5 + 0 + 0) / 4)
        self.assertEqual((d['bounds']['L'], d['bounds']['U']), (0.125, 0.125))
        b = d['bootstrap']
        self.assertTrue(-1 <= b['lower'] <= d['estimate'] <= b['upper'] <= 1)
        self.assertNotIn('exact_all_zero_bound', d)
        self.assertEqual(d['nonzero_markets'], 3)

    def test_all_zero_bound(self):
        for m, q in ((4, 0.527), (8, 0.312), (12, 0.221)):
            self.assertEqual(round(an.q_all_zero(m), 3), q)
        for m, r1, r2 in ((4, 1.0, 2.0), (8, 0.960, 1.920), (12, 0.784, 1.568)):
            self.assertAlmostEqual(an.hoeffding_radius(m, 1), r1, delta=0.001)     # AMENDMENT-03 values, 3 decimals
            self.assertAlmostEqual(an.hoeffding_radius(m, 2), r2, delta=0.001)
        for batches, q in ((('b1',), 0.527), (('b1', 'b2'), 0.312), (('b1', 'b2', 'b3'), 0.221)):
            res = self.run_case(batches=batches)
            self.assertEqual(res['m_markets'], 4 * len(batches))
            c = res['primary']['contrasts']
            e = c['primary_D_minus_B']['exact_all_zero_bound']
            self.assertEqual((round(e['lower'], 3), round(e['upper'], 3)), (-q, q))
            e = c['interaction_DB_minus_CA']['exact_all_zero_bound']
            self.assertAlmostEqual(e['upper'], 2 * an.q_all_zero(4 * len(batches)))
            self.assertTrue(c['primary_D_minus_B']['bootstrap']['degenerate'])
            h = c['primary_D_minus_B']['hoeffding_reference']
            self.assertAlmostEqual(h['radius'], an.hoeffding_radius(4 * len(batches), 1))
            self.assertGreaterEqual(h['lower'], -1)
        self.assertIn('all m market values zero: exact bound q_m = 22.1%', an.report(res))

    def test_bootstrap_determinism(self):
        a, b = an.bootstrap_indices(4), an.bootstrap_indices(4)
        self.assertEqual(a, b)
        self.assertEqual(len(a), 10000)
        self.assertNotEqual(an.bootstrap_indices(4, seed_text='other'), a)
        masks = {('b1.D', 'm0-o01'): {10, 11, 12}, ('b1.D', 'm2-o02'): {10, 11, 12}, ('b1.B', 'm3-o01'): {6, 7, 8},
                 ('b1.D', 'm1-o01'): {15, 16, 17}, ('b1.D', 'm1-o02'): {15, 16, 17}}
        r1 = self.run_case(masks=masks)
        r2 = self.run_case(masks=masks)
        self.assertEqual(json.dumps(r1['primary'], sort_keys=True), json.dumps(r2['primary'], sort_keys=True))
        bs = r1['primary']['contrasts']['primary_D_minus_B']['bootstrap']
        self.assertLess(bs['lower'], bs['upper'])
        # the same index draws reproduce the interval by hand
        vals = [v['value'] for v in r1['primary']['contrasts']['primary_D_minus_B']['market_values']]
        means = sorted(sum(vals[i] for i in idx) / 4 for idx in a)
        self.assertAlmostEqual(bs['lower'], an.percentile(means, 0.025))
        self.assertAlmostEqual(bs['upper'], an.percentile(means, 0.975))

    def test_missing_outcome_bounds(self):
        masks = {('b1.B', 'm0-o01'): {6, 7, 8},       # yB(m0) = 0.5, known
                 ('b1.D', 'm0-o01'): {7, 8, 9},       # D stops after round 15: o01 positive, o02 unknown
                 ('b1.A', 'm1-o01'): {20, 21, 22}}    # yA(m1) = 0.5, known
        res = self.run_case(masks=masks, completed={'b1.D': 10})
        cells = {x['market']: x for x in res['primary']['per_market_arm_focal_fraction']}
        self.assertEqual((cells['b1.m0']['D']['L'], cells['b1.m0']['D']['U']), (0.5, 1.0))
        self.assertEqual((cells['b1.m1']['D']['L'], cells['b1.m1']['D']['U']), (0.0, 1.0))
        c = res['primary']['contrasts']
        p = c['primary_D_minus_B']
        self.assertEqual([(x['L'], x['U']) for x in p['market_bounds']], [(0.0, 0.5), (0.0, 1.0), (0.0, 1.0), (0.0, 1.0)])
        self.assertAlmostEqual(p['bounds']['L'], 0.0)
        self.assertAlmostEqual(p['bounds']['U'], 0.875)
        z = c['interaction_DB_minus_CA']
        self.assertEqual([(x['L'], x['U']) for x in z['market_bounds']], [(0.0, 0.5), (0.5, 1.5), (0.0, 1.0), (0.0, 1.0)])
        self.assertAlmostEqual(z['bounds']['L'], 0.125)
        self.assertAlmostEqual(z['bounds']['U'], 1.0)
        fc = res['primary']['focal_counts_by_arm']['D']
        self.assertEqual((fc['known_positive'], fc['unknown']), (1, 7))
        self.assertAlmostEqual(fc['verified_event_rate_over_assigned'], 1 / 8)


class PopulationTests(Base):
    def test_rival_slots_excluded_from_ordinary_counts(self):
        masks = {(f'b1.{arm}', oid(mi, k)): {6, 7, 8} for arm in 'ABCD' for mi in range(4) for k in range(2, 6)}
        masks[('b1.A', 'm0-o07')] = {9, 10, 11}                 # one small owner, arm A
        res = self.run_case(masks=masks)
        oc = res['secondary']['ordinary_owner_counts_by_arm']
        for arm in 'ABCD':
            self.assertEqual(oc[arm]['assigned'], 16)
            self.assertEqual(oc[arm]['known_positive'], 1 if arm == 'A' else 0)
            self.assertEqual(res['primary']['focal_counts_by_arm'][arm]['known_positive'], 0)
        traj = res['secondary']['trajectories_by_arm_round']
        self.assertEqual(traj['C'][0]['seeder']['masking'], 16)
        self.assertEqual(traj['A'][0]['rival_unseeded']['masking'], 16)
        self.assertNotIn('seeder', traj['A'][0])

    def test_mask_recomputed_and_disagreement_counted(self):
        res = self.run_case(masks={('b1.D', 'm0-o01'): {6, 7, 8}}, flip={('b1.D', 'm0-o01', 7), ('b1.A', 'm0-o02', 9)})
        self.assertEqual(res['record_checks']['mask_disagreements'], 2)
        self.assertEqual(self.profile(res, 'D', 'b1.m0', 'm0-o01')['outcome'], 'positive')   # recomputed flag used
        self.assertEqual(self.profile(res, 'A', 'b1.m0', 'm0-o02')['outcome'], 'negative')

    def test_opening_message_copies_removed(self):
        msgs = [{'econ': 'b1.open', 'from': 'm0-o01', 'to': 'm0-o02', 'round': 2, 'text': 'x', 'status': 'blocked_channel_off'},
                {'econ': 'b1.B', 'from': 'm0-o01', 'to': 'm0-o02', 'round': 2, 'text': 'x', 'status': 'blocked_channel_off'},
                {'econ': 'b1.D', 'from': 'm0-o03', 'to': 'm0-o01', 'round': 8, 'text': 'y', 'cut': False,
                 'delivered_round': 9, 'status': 'delivered'}]
        res = self.run_case(messages=msgs)
        self.assertEqual(res['record_checks']['opening_message_copies_removed_from_continuations'], 1)
        self.assertEqual(res['secondary']['messages']['D']['totals']['delivered'], 1)
        e = next(x for x in res['secondary']['exposure'] if x['arm'] == 'D' and x['owner'] == 'm0-o01')
        self.assertEqual(e['first_seeder_message_delivered'], 9)


class OperationsTests(Base):
    def failures(self, n):
        # arm C: 4 markets x 8 owners x 20 rounds = 640 planned active decisions; 1% = 6.4
        return {('b1.C', oid(i % 4, 6), 6 + i): ('void', 'call_failed:timeout') for i in range(n)}

    def test_compromised_flag(self):
        res = self.run_case(status=self.failures(6))
        ops = res['operations']
        self.assertEqual(ops['totals_by_arm']['C']['planned_active'], 640)
        self.assertEqual(ops['totals_by_arm']['C']['void_failure'], 6)
        self.assertEqual(ops['totals_by_arm']['C']['dispatched'], 640)
        self.assertEqual(ops['totals_by_arm']['C']['accepted'], 634)
        self.assertFalse(ops['operationally_compromised'])
        res = self.run_case(status=self.failures(7))
        self.assertTrue(res['operations']['operationally_compromised'])
        self.assertEqual(res['operations']['compromised_reasons']['arms_over_1pct_failures'], ['C'])
        self.assertIn('OPERATIONALLY COMPROMISED', an.report(res))
        # invalid actions are observed no-ops, not failures
        st = {('b1.C', oid(i % 4, 6), 6 + i): ('void', 'production_exceeds_available_capacity') for i in range(10)}
        res = self.run_case(status=st)
        self.assertFalse(res['operations']['operationally_compromised'])
        self.assertEqual(res['operations']['totals_by_arm']['C']['void_invalid'], 10)

    def test_cli_writes_outputs_and_cost(self):
        d = build(self.tmp / 'cli')
        out = self.tmp / 'out'
        self.assertEqual(an.main([str(d.parent), '--out', str(out)]), 0)
        res = json.loads((out / 'analysis.json').read_text())
        self.assertEqual(res['cost']['from_calls']['all']['calls'], 4 * 8 * 5 + 4 * 4 * 8 * 20)
        self.assertTrue(math.isclose(res['cost']['from_calls']['econ:b1.D']['usd'], 0.011 * 640, rel_tol=1e-9))
        txt = (out / 'analysis.txt').read_text()
        self.assertIn('EXPLORATORY', txt)
        self.assertIn('No significance claims', txt)


if __name__ == '__main__':
    unittest.main(verbosity=2)
