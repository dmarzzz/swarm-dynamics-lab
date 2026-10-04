import copy
import importlib.util
import json
import unittest
from pathlib import Path
import loop_world as w
from native_provider import wire, validate_wire

ROOT = Path(__file__).resolve().parent
spec = importlib.util.spec_from_file_location('loop_candidate', ROOT.parent / 'controller-study/next-contract/candidate.py')
candidate = importlib.util.module_from_spec(spec)
spec.loader.exec_module(candidate)


class LoopTests(unittest.TestCase):
    def test_public_comparator_feasible_varied_cases(self):
        for seed in range(17100, 17140):
            for case in w.worlds(seed):
                for arm in w.ARMS:
                    r = w.episode(case, arm)
                    self.assertTrue(r['architecture_pass'], (seed, case['id'], arm))
                    self.assertTrue(r['proposal_pass'])
                    self.assertEqual(4, len(r['trace']))

    def test_hidden_modes_have_identical_initial_observation(self):
        cases = w.worlds(17001)
        for group in (cases[:3], cases[3:6]):
            obs = [w.observe(c, c['initial'], 1, []) for c in group]
            self.assertEqual(obs[0], obs[1]); self.assertEqual(obs[1], obs[2])
            serialized = json.dumps(obs[0])
            for name in ('failed_first', 'due_tick', '"seed"', '"mode"', '"root"'):
                self.assertNotIn(name, serialized)

    def test_true_failure_then_retry(self):
        r = w.episode(w.worlds(17001)[1], 'guard')
        self.assertEqual([False, False, True, True], [x['healthy'] for x in r['trace']])
        self.assertEqual(['deploy', 'inspect', 'deploy', 'inspect'], [x['executed'].split(':')[0] for x in r['trace']])
        self.assertFalse(r['trace'][1]['state']['probe']['checks']['processes_live'])
        self.assertTrue(r['verified_repair'])

    def test_pending_completion_invalidates_probe(self):
        r = w.episode(w.worlds(17001)[2], 'verification_required')
        self.assertEqual('pending', r['trace'][1]['state']['operation']['status'])
        o = r['trace'][2]['observation']
        self.assertEqual('completed', o['operation']['status'])
        self.assertLess(o['cached_probe']['epoch'], o['current_epoch'])
        self.assertTrue(r['trace'][1]['forced_inspection'])
        self.assertTrue(r['trace'][2]['forced_inspection'])

    def test_acknowledgement_does_not_reveal_success(self):
        cases = w.worlds(17001)
        results = [w.episode(c, 'guard')['trace'][0]['result'] for c in cases[:3]]
        self.assertEqual(1, len(set(results)))

    def test_live_configuration_fault_is_real_and_guard_allows_fix(self):
        for case in w.worlds(17001)[6:8]:
            self.assertTrue(all(case['initial']['live'].values()))
            self.assertFalse(all(w.cases.f.health(case['fixture'], case['initial']).values()))
            o = w.observe(case, case['initial'], 1, [])
            aid = w.choose(o)['action_id']
            self.assertIsNone(w.classify(o, aid))
            self.assertTrue(w.episode(case, 'guard')['architecture_pass'])
            service = o['roles_to_services']['worker']
            restart = f'deploy:{service}:{o["deployed"][service]}'
            self.assertEqual('incompatible', w.classify(o, restart))

    def test_negative_controls(self):
        for c in w.worlds(17001)[:8]:
            self.assertFalse(w.episode(c, 'guard', lambda o: {'action_id': 'wait'})['architecture_pass'])
        for c in w.worlds(17001)[8:]:
            def restart(o):
                s = o['roles_to_services']['worker']
                return {'action_id': f'deploy:{s}:{o["deployed"][s]}'}
            self.assertFalse(w.episode(c, 'unprotected_control', restart)['architecture_pass'])
        def never_inspect(o):
            return w.choose(o) if o['tick'] == 1 else {'action_id': 'wait'}
        self.assertFalse(w.episode(w.worlds(17001)[0], 'guard', never_inspect)['architecture_pass'])
        forced = w.episode(w.worlds(17001)[0], 'verification_required', never_inspect)
        self.assertTrue(forced['architecture_pass'])
        self.assertFalse(forced['proposal_pass'])
        self.assertTrue(forced['trace'][1]['forced_inspection'])
        self.assertFalse(forced['trace'][1]['voluntary_inspection'])

    def test_forced_agreement_is_not_independent_initiative(self):
        r = w.episode(w.worlds(17001)[0], 'verification_required')
        x = r['trace'][1]
        self.assertTrue(x['proposed_inspection']); self.assertTrue(x['forced_inspection'])
        self.assertFalse(x['voluntary_inspection']); self.assertFalse(x['substituted'])

    def test_wire_bound_and_separate_diagnosis_on_reference_and_deviations(self):
        maximum = 0
        for case in w.worlds(17001):
            initial = w.observe(case, case['initial'], 1, [])
            for aid in initial['legal_actions']:
                for arm in w.ARMS:
                    def policy(o):
                        return {'action_id': aid} if o['tick'] == 1 else w.choose(o)
                    r = w.episode(case, arm, policy)
                    for row in r['trace']:
                        o = row['observation']
                        d = w.reference.labels(o)
                        for request in (candidate.diagnosis_request(o), candidate.action_request(case, o, d, 'justification_first')):
                            body = wire(request, 'anthropic/claude-opus-4.6')
                            validate_wire(body)
                            maximum = max(maximum, len(json.dumps(body).encode()))
        self.assertLessEqual(maximum, 8000)
        print('maximum tested serialized wire bytes:', maximum)


class PreparationTests(unittest.TestCase):
    def test_packet_balanced_cost_and_disabled(self):
        import prepare
        p = prepare.packet()
        self.assertEqual(40, len(p['assignments']))
        self.assertEqual(320, p['episodes'] * p['ticks_per_episode'] * p['calls_per_tick'])
        self.assertFalse(p['native_dispatch_enabled'])
        self.assertAlmostEqual(p['max_calls'] * p['max_request_usd'], p['model_max_usd'])
        self.assertAlmostEqual(p['prior_reserved_usd'] + p['model_max_usd'], p['required_model_cap_usd'])
        self.assertEqual(40, len({tuple(x.values()) for x in p['assignments']}))

    def test_seal_refuses_overwrite_without_reading_cases(self):
        import prepare
        import tempfile
        with tempfile.TemporaryDirectory() as folder:
            private, public = Path(folder)/'private.json', Path(folder)/'seal.json'
            receipt = prepare.seal(private, public)
            self.assertFalse(receipt['opened_for_development'])
            self.assertEqual(0o600, private.stat().st_mode & 0o777)
            with self.assertRaises(FileExistsError):
                prepare.seal(private, public)

    def test_exact_public_plan_contract(self):
        spec = importlib.util.spec_from_file_location('loop_public_plan', ROOT.parent.parent/'experiment-documentation/public_plan.py')
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        module.validate({'id':'immune-response-v3','description':'TLDR: bounded repair and verification loop',
                         'url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/researchers/vishesh/notes/immune-response-v3/verification-loop/PLAN.md'},
                        (ROOT/'PLAN.md').read_text(),
                        'Compare guard and required inspection across failed, delayed and configuration repairs; fixed outcomes, authored feasibility only.')

class InstrumentTests(unittest.TestCase):
    def test_wrong_diagnosis_is_preserved_and_fails_qualification(self):
        import loop_instrument as i
        case = w.worlds(17001)[0]
        r = w.episode(case, 'guard')
        diagnoses = [w.reference.labels(x['observation']) for x in r['trace']]
        self.assertTrue(i.qualification(r, diagnoses)['full_model_qualification'])
        diagnoses[0]['fault'] = 'none'
        q, _ = i.request(case, r['trace'][0]['observation'], 'action', diagnoses[0])
        self.assertEqual('none', q['observation']['diagnosis']['fault'])
        self.assertFalse(i.qualification(r, diagnoses)['full_model_qualification'])
        with self.assertRaises(ValueError):
            i.qualification(r, diagnoses[:3])

    def test_strict_schema_and_order(self):
        import loop_instrument as i
        case = w.worlds(17001)[0]
        o = w.observe(case, case['initial'], 1, [])
        d = w.reference.labels(o)
        i.validate_action(case, o, d, {'reason':'Current evidence.', 'action_id':'inspect'})
        with self.assertRaisesRegex(ValueError, 'action_field_order'):
            i.validate_action(case, o, d, {'action_id':'inspect', 'reason':'Current evidence.'})

if __name__ == '__main__':
    unittest.main()
