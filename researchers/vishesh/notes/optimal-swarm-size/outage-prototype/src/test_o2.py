import copy,json,unittest
from engine import execute
from world import make_case,World
from policies import reference_actions
from native import payload
from run_outage_o2 import assignments,admission_errors,FLAGS
from local_relay import contracts

def owned_reference(messages,actor,tick):
    packet=json.loads(messages[-1]['content']);obs=copy.deepcopy(packet['observation'])
    if 'ownership' in packet:obs['service_ids']=packet['ownership']['owned_services']
    return json.dumps({'actions':reference_actions(obs,packet['max_actions'])})

class O2Tests(unittest.TestCase):
    def test_ownership_partitions_and_equal_slots(self):
        for n in (1,4,8):
            packets=[]
            def call(messages,actor,tick):
                packets.append(json.loads(messages[-1]['content']));return owned_reference(messages,actor,tick)
            r=execute(make_case(0,True,21,8),'single' if n==1 else 'fixed',call,team_size=n,ownership=n>1)
            self.assertTrue(r['evaluation']['success']);self.assertEqual(r['duplicate_patch_targets'],0)
            self.assertEqual(r['ownership_violations'],0)
            for tick in range(8):
                rows=[p for p in packets if p['observation']['tick']==tick]
                self.assertEqual(sum(p['max_actions'] for p in rows),8)
                if n>1:
                    owners=[s for p in rows for s in p['ownership']['owned_services']]
                    self.assertEqual(len(owners),8);self.assertEqual(len(set(owners)),8)
    def test_wrong_owner_is_rejected_and_retained(self):
        def wrong(messages,actor,tick):
            p=json.loads(messages[-1]['content']);return json.dumps({'actions':[{'op':'inspect','service':p['observation']['service_ids'][(actor+1)%4]}]})
        r=execute(make_case(0),'fixed',wrong,team_size=4,ownership=True)
        self.assertEqual(r['ownership_violations'],32);self.assertFalse(r['evaluation']['success']);self.assertEqual(r['actions'],0)
    def test_reference_recovery_and_payload_sizes(self):
        sizes=[]
        def call(messages,actor,tick):
            sizes.append(len(json.dumps(payload(messages,1024)).encode()));return owned_reference(messages,actor,tick)
        for changing in (False,True):
            for n in (1,4,8):
                r=execute(make_case(0,changing,21,8),'single' if n==1 else 'fixed',call,team_size=n,ownership=n>1)
                self.assertTrue(r['evaluation']['success'])
            self.assertTrue(execute(make_case(0,changing,21,8),'scheduled')['evaluation']['success'])
        self.assertLess(max(sizes),24000)
    def test_manifest_relay_and_budget_envelope(self):
        rows=assignments();self.assertEqual(len(rows),10);self.assertEqual(len({r['id'] for r in rows}),10)
        allowed,tokens,size=contracts('outage-o2');self.assertEqual(len(allowed),272)
        self.assertEqual((tokens,size),(1024,24000));self.assertLessEqual(len(allowed)*38632,11000000)
        for r in rows:
            if r['arm']!='scheduled':self.assertIn(r['id']+'/7/'+str(r['n']-1),allowed)
        self.assertFalse(any('scheduled' in k for k in allowed))
    def test_explicit_new_admission_scope(self):
        a={k:True for k in FLAGS}|dict(source_commit='a',attempt_id='outage-o2',credential_alias='local-openrouter-relay',claim_id='x',verified_epoch=100,claim_expiry_epoch=8000,dispatch_origin='owner-directed-ownership-size-diagnostic')
        self.assertEqual(admission_errors(a,'a',100),[])
        self.assertIn('attempt_mismatch',admission_errors(a|{'attempt_id':'outage-o1'},'a',100))
    def test_tool_cap_enforced_at_eight(self):
        w=World(make_case(0,False,21,8));w.step([(0,{'op':'wait'})]*8)
        with self.assertRaises(ValueError):w.step([(0,{'op':'wait'})]*9)

if __name__=='__main__':unittest.main()
