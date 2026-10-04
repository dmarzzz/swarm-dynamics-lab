import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import immune as m
from provider import ScriptedPolicy,PolicyError

class Inspect(ScriptedPolicy):
    def complete(self,req,fallback):
        self.assertions(req)
        return super().complete(req,fallback)
    def assertions(self,req):
        obs=req['observation']
        assert not {'affected','truth','target_key','private_status','shared_status'} & set(obs)
        assert 'response_schema' in req

class Test(unittest.TestCase):
    def rows(self,world,task=6500):return {r['arm']:r for r in m.run_episode(task,1,world,1,m.ARMS,{},Inspect())}
    def test_clean_and_negative_control(self):
        b=self.rows('no_incident')
        self.assertTrue(all(r['validity']['ok'] and r['evaluation']['utility']==1 for r in b.values()))
    def test_mechanism_controls(self):
        b=self.rows('shared_evidence',6504)
        self.assertEqual(b['Q11']['evaluation']['utility'],1)
        self.assertLess(b['Q11R']['evaluation']['utility'],1)
        self.assertGreater(b['Q11']['evaluation']['utility'],b['Q10F']['evaluation']['utility'])
        self.assertEqual(self.rows('no_replay',6504)['Q11R']['evaluation']['utility'],1)
    def test_collateral_rollback(self):
        b=self.rows('benign_learning',6504)
        self.assertEqual(b['Q11']['evaluation']['utility'],0)
        self.assertEqual(b['Q11S']['evaluation']['utility'],1)
        self.assertEqual(b['Q11']['evaluation']['learning_retained'],0)
        self.assertEqual(b['Q11S']['evaluation']['learning_retained'],1)
    def test_missing_lineage_is_not_magically_filtered(self):
        b=self.rows('missing_lineage',6504)
        self.assertEqual(b['Q11']['evaluation']['stale_accepted'],1)
        self.assertLess(b['Q11']['evaluation']['utility'],1)
    def test_choices_are_keyed_and_bounded(self):
        a=m.record('version:x',1);b=m.record('version:x',2,2)
        obs={'memory':[a],'incoming':[b],'role':'specialist','services':[]}
        candidates,schema=m.choice_contract(obs)
        self.assertEqual(set(schema['properties']['choices']['properties']),{'version:x'})
        self.assertEqual(schema['properties']['choices']['properties']['version:x']['enum'],[a['id'],b['id'],None])
        class Wrong:
            def complete(self,req,f):return {'choices':{'version:x':'invented'}}
        mem={'version:x':a};before=copy.deepcopy(mem)
        with self.assertRaises(PolicyError):m.act(Wrong(),mem,[b],'specialist',[])
        self.assertEqual(mem,before)
    def test_scoring_types_and_actions(self):
        fx=m.fixture(6504);truth=m.truth_at(fx,1)
        a={'plan':{s:truth['version:'+s] for s in fx['requests'][1]},'constraints':{str(i):truth['compat:'+str(i)] for i in range(4)},'requested_action':'mock-deploy'}
        self.assertEqual(m.evaluate(a,fx,1)['utility'],1)
        a['requested_action']='abstain';self.assertEqual(m.evaluate(a,fx,1)['utility'],0)
        a['requested_action']='mock-deploy';a['constraints']['extra']=1
        self.assertEqual(m.evaluate(a,fx,1)['utility'],0)
    def test_seed_does_not_change_truth_or_scripted_scores(self):
        a=self.rows('shared_evidence')
        b={r['arm']:r for r in m.run_episode(6500,77,'shared_evidence',1,m.ARMS,{},ScriptedPolicy())}
        for arm in a:self.assertEqual(a[arm]['evaluation'],b[arm]['evaluation'])
        self.assertEqual(len({r['common_checkpoint_hash'] for r in a.values()}),1)
    def test_failure_preserved_and_not_recovered(self):
        class Broken:
            def complete(self,*args):raise PolicyError('injected')
        rows=m.run_episode(6500,1,'shared_evidence',1,m.ARMS,{},Broken())
        self.assertTrue(all(not r['validity']['ok'] and r['evaluation']['utility']==0 and r['evaluation']['recovery_round'] is None for r in rows))
    def test_target_coverage(self):
        frequencies=[]
        for task in range(6500,6516):
            fx=m.fixture(task);service=fx['target_key'].split(':')[1]
            frequencies.append(sum(service in x for t,x in fx['requests'].items() if t>=7))
        self.assertGreater(len(set(frequencies)),1)

if __name__=='__main__':unittest.main()
