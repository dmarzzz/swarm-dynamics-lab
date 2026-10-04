import copy,unittest
import verification as study
class Paired(unittest.TestCase):
    def test_pairs_share_older_report_and_catalog(self):
        roots=study.roots();self.assertEqual(len(roots),12)
        for a,b in zip(roots[::2],roots[1::2]):
            self.assertEqual(a['root'],b['root']);self.assertEqual(a['older_report'],b['older_report']);self.assertEqual(a['fixture']['catalog'],b['fixture']['catalog']);self.assertEqual(a['initial']['deployed'],b['initial']['deployed'])
            oa=study.observation(a,a['initial'],1,[]);ob=study.observation(b,b['initial'],1,[]);self.assertEqual(oa['report_lineage']['older'],ob['report_lineage']['older']);self.assertTrue(study.public_reference.labels(oa)['probe_current']);self.assertNotEqual(oa['cached_probe']['live'],ob['cached_probe']['live'])
    def test_rule_feasible_and_repeats_exactly(self):
        for c in study.roots():
            for guarded in (False,True):
                a,s=study.simulate(c,guarded);b,t=study.simulate(c,guarded);self.assertEqual((a,s),(b,t));self.assertTrue(s['post_state_gate']);self.assertEqual(s['missed_repair'],0);self.assertEqual(s['served_opportunities'],1 if c['branch']=='confirmed' else 2)
                self.assertEqual(s['post_action_verified'],True if c['branch']=='confirmed' else None)
    def test_always_abstain_misses_real_repairs(self):
        for c in study.roots():
            if c['branch']=='confirmed':self.assertEqual(study.simulate(c,False,lambda o:{'action_id':'wait','reason':'control'})[1]['missed_repair'],1)
    def test_restart_harms_healthy_and_guard_is_explicit(self):
        for c in study.roots():
            if c['branch']!='contradicted':continue
            def restart(o):
                s=o['roles_to_services'][c['target_role']];return {'action_id':f'deploy:{s}:{o["deployed"][s]}','reason':'adversarial restart control'}
            _,raw=study.simulate(c,False,restart);trace,guarded=study.simulate(c,True,restart)
            self.assertEqual(raw['served_opportunities'],0);self.assertEqual(raw['unnecessary_executed'],2);self.assertEqual(guarded['served_opportunities'],2);self.assertEqual(guarded['unnecessary_executed'],0);self.assertEqual(guarded['unnecessary_proposed'],2);self.assertEqual(guarded['guard_denials'],2);self.assertFalse(guarded['proposal_restraint_pass']);self.assertTrue(all(x['action']['action']=='wait' and x['proposal']['action']=='deploy' for x in trace))
    def test_guard_has_no_hidden_state_and_does_not_repair(self):
        c=study.roots()[0];o=study.observation(c,c['initial'],1,[]);s=o['roles_to_services'][c['target_role']];a=study.cases.f.action('deploy',s,o['deployed'][s]);decision=study.admission(o,a);c['initial']['live'][c['target_role']]=True;self.assertEqual(decision,study.admission(o,a))
        stale=copy.deepcopy(o);stale['cached_probe']['epoch']-=1;self.assertEqual(study.admission(stale,a),(False,'current_liveness_required'))
if __name__=='__main__':unittest.main()

class Payload(unittest.TestCase):
    def test_actor_receives_true_current_observation_and_bounded_payload(self):
        import importlib.util
        from pathlib import Path
        base=Path(__file__).resolve().parent.parent/'controller-study'
        spec=importlib.util.spec_from_file_location('verification_candidate',base/'next-contract/candidate.py');candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
        from native_provider import wire,validate_wire
        for c in study.roots():
            o=study.observation(c,c['initial'],1,[]);self.assertEqual(o['cached_probe']['live'],c['initial']['live']);self.assertEqual(o['cached_probe']['checks'],study.cases.f.health(c['fixture'],c['initial']))
            for guarded in (False,True):
                frames,_=study.simulate(c,guarded)
                for x in frames:
                    o=x['observation'];d=study.public_reference.labels(o)
                    for q in [candidate.diagnosis_request(o),candidate.action_request(c,o,d,'justification_first')]:validate_wire(wire(q,'anthropic/claude-opus-4.6'))
