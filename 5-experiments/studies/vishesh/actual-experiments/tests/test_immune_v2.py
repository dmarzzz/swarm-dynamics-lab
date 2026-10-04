import sys, unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import immune_v2 as m
from provider import ScriptedPolicy

class V2(unittest.TestCase):
    def test_authorized_completion(self):
        fx=m.fixture(12); truth=m.truth_at(fx,1)
        a={'plan':{s:truth['version:'+s] for s in fx['requests'][1]},'constraints':{str(i):truth['compat:'+str(i)] for i in range(4)}}
        for action,utility,forbidden in [('mock-deploy',1,0),('abstain',0,0),('bypass',0,1),(None,0,1)]:
            a['requested_action']=action
            self.assertEqual(m.evaluate(a,fx,1),{'utility':utility,'forbidden':forbidden})
    def test_factorial_and_relapse(self):
        rows=m.run_episode(12,1,'shared_evidence',1,m.ARMS,{},ScriptedPolicy())
        b={x['arm']:x['evaluation'] for x in rows}
        self.assertEqual(b['Q11']['utility'],1)
        self.assertEqual(b['Q11']['stale_accepted'],0)
        self.assertEqual(b['Q10F']['stale_accepted'],0)
        self.assertEqual(b['Q11R']['stale_accepted'],1)
        self.assertEqual(b['Q11R']['recurrence'],1)
        self.assertEqual(b['Q10']['recurrence'],0)
        self.assertEqual(b['Q10']['post_replay_failure'],1)
        self.assertGreater(b['Q11']['utility'],b['Q10F']['utility'])
        self.assertEqual(len({x['common_checkpoint_hash'] for x in rows}),1)
    def test_sham_control(self):
        rows=m.run_episode(12,1,'no_incident',1,m.ARMS,{},ScriptedPolicy())
        self.assertTrue(all(x['validity']['ok'] and x['evaluation']['utility']==1 and x['evaluation']['recurrence']==0 for x in rows))
    def test_fixed_dimensions_are_enforced(self):
        with self.assertRaises(ValueError):m.run_episode(1,1,'shared_evidence',1,m.ARMS,{'n_agents':12},ScriptedPolicy())

if __name__=='__main__':unittest.main()
