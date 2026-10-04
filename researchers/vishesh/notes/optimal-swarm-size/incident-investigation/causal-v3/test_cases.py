import copy,json,unittest
from worlds import World,ROOTS,CLEAN,probes,infer,CAUSE
from broker import Broker,scripted_run

class CausalTests(unittest.TestCase):
    def test_all_cases_both_brokers_references(self):
        for root in ROOTS:
            for condition in ('fault','clean','missing'):
                for n in (1,3):
                    w=World(root,condition);b,r=scripted_run(w,n)
                    self.assertTrue(r['joint_correct'],(root,condition,n,r))
                    self.assertTrue(all(e['tool_units']<=3 for e in b.events))
                    if condition!='fault':self.assertLessEqual(b.rounds,4);self.assertEqual(w.actions,[])
    def test_fault_truth_and_clean_truth(self):
        for root in ROOTS:
            self.assertFalse(all(probes(root,World(root,'fault').state).values()))
            self.assertTrue(all(probes(root,World(root,'clean').state).values()))
    def test_causal_repair_counterfactuals(self):
        for root in ROOTS:
            b,r=scripted_run(World(root,'fault'),1);self.assertTrue(r['recovered'])
            actions=[a for e in b.events for batch in e['proposals'] for a in batch if a['op']=='patch']
            for skipped in range(len(actions)):
                w=World(root,'fault')
                while w.coverage()['pending']:w.query(w.coverage()['pending'][:3])
                for i,a in enumerate(actions):
                    if i!=skipped:w.act(a)
                self.assertFalse(all(probes(root,w.state).values()),(root,skipped))
    def test_schema_order_is_causal_and_unsafe_rejected(self):
        w=World('schema_rollout','fault');w.query(w.coverage()['pending']);before=copy.deepcopy(w.state)
        r=w.act({'op':'patch','field':'producer_schema','value':2});self.assertEqual(r['status'],'unsafe_rejected');self.assertEqual(before,w.state)
    def test_wrong_or_unqueried_citation_and_label_fail(self):
        for root in ROOTS:
            w=World(root,'fault');b,_=scripted_run(w,1);a=copy.deepcopy(b.answer);a['diagnoses'][0]['evidence']=['fake'];self.assertFalse(w.evaluate(a)['joint_correct'])
            a=copy.deepcopy(b.answer);a['diagnoses'][0]['cause']=next(c for r,c in CAUSE.items() if r!=root);self.assertFalse(w.evaluate(a)['joint_correct'])
    def test_diagnosis_without_action_does_not_recover(self):
        w=World('auth_chain','fault')
        while w.coverage()['pending']:w.query(w.coverage()['pending'])
        _,a=infer(w.receipts);r=w.evaluate(a);self.assertTrue(r['identified_fault']);self.assertFalse(r['recovered']);self.assertFalse(r['joint_correct'])
    def test_unknown_and_repeated_handles_do_not_poison(self):
        w=World('route_config','fault');w.query(['unknown']);w.query(['e0']);w.query(['e0']);self.assertEqual(w.coverage()['pending'],['e1','e2'])
        b,r=scripted_run(w,1);self.assertTrue(r['joint_correct'])
    def test_discovered_handle_cannot_be_used_in_same_batch(self):
        w=World('auth_chain','fault');r=w.query(['e0','e1']);self.assertEqual(r[1]['evidence']['kind'],'rejected');self.assertIn('e1',w.coverage()['pending'])
    def test_equal_capacity_and_ownership(self):
        w=World('route_config','fault');b=Broker(w,3)
        with self.assertRaises(ValueError):b.step([[{'op':'query','handle':'e0'},{'op':'query','handle':'e1'}],[],[]])
        with self.assertRaises(ValueError):b.step([[{'op':'query','handle':'e1'}],[],[]])
        b.step([[{'op':'query','handle':'e0'}],[{'op':'query','handle':'e1'}],[{'op':'query','handle':'e2'}]])
        self.assertEqual(b.events[-1]['tool_units'],3)
    def test_no_same_round_evidence_to_repair(self):
        b=Broker(World('auth_chain','fault'),1)
        with self.assertRaises(ValueError):b.step([[{'op':'query','handle':'e0'},{'op':'patch','field':'billing_audience','value':'billing'}]])
        self.assertEqual(b.rounds,0)
    def test_no_silent_deduplication(self):
        b=Broker(World('route_config','fault'),1)
        with self.assertRaises(ValueError):b.step([[{'op':'query','handle':'e0'},{'op':'query','handle':'e0'}]])
        self.assertEqual(b.world.receipts,[])
    def test_finish_consensus_and_no_free_peer_diagnosis(self):
        b=Broker(World('route_config','clean'),3);b.step([[{'op':'query','handle':'e0'}],[{'op':'query','handle':'e1'}],[{'op':'query','handle':'e2'}]])
        f={'op':'finish','decision':'resolve','diagnoses':[]}
        b.step([[f],[f],[]]);self.assertIsNone(b.answer)
        b.step([[f],[f],[f|{'decision':'escalate'}]]);self.assertIsNone(b.answer)
        b.step([[f],[f],[f]]);self.assertIsNotNone(b.answer)
    def test_shared_action_uses_three_units(self):
        w=World('route_config','clean');w.query(['e0','e1','e2']);b=Broker(w,3)
        with self.assertRaises(ValueError):b.step([[{'op':'rebalance'}],[{'op':'patch','field':'west_target','value':'west'}],[]])
        self.assertEqual(b.rounds,0)
    def test_history_public_no_private_case_truth(self):
        w=World('cursor_chain','fault');b=Broker(w,3);p=b.packet(0)
        self.assertNotIn('condition',p['start']);self.assertNotIn('state',p['start']);self.assertNotIn('gold',json.dumps(p));self.assertNotIn('grade',json.dumps(p))
    def test_reference_decoupled_from_hidden_world(self):
        for root in ROOTS:
            w=World(root,'fault')
            while w.coverage()['pending']:w.query(w.coverage()['pending'])
            serialized=json.loads(json.dumps(w.receipts));actions,answer=infer(serialized)
            self.assertTrue(actions);self.assertEqual(answer['diagnoses'][0]['cause'],CAUSE[root])
    def test_clean_mutation_not_counted_as_restraint(self):
        w=World('route_config','clean');w.query(['e0','e1','e2']);w.act({'op':'patch','field':'west_target','value':'west'})
        self.assertFalse(w.evaluate({'decision':'resolve','diagnoses':[]})['joint_correct'])
    def test_fresh_worlds_no_state_leak(self):
        for root in ROOTS:
            a=World(root,'fault');before=copy.deepcopy(a.state);scripted_run(a,3);self.assertEqual(World(root,'fault').state,before)

if __name__=='__main__':unittest.main()
