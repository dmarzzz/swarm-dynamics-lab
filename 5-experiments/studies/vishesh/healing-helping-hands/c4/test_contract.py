import copy,itertools,unittest
from contract import actor_input,admit,qwen_payload,score,qualify
from scenarios import fixture
class PolicyTests(unittest.TestCase):
    def row(self,i,a='SUPPORT',b='SUPPORT',j='SUPPORT',gold='SUPPORT'):
        return {'id':str(i),'family':'dev','expected':gold,'status':'completed','labels':{'a':a,'b':b,'jev':j}}
    def test_agreement_can_be_wrong(self):
        s=score([self.row(0,gold='REFUTE',j='REFUTE')]);self.assertEqual(s['families']['dev']['accepted_wrong'],1);self.assertEqual(s['macro_safety_delta'],1);self.assertFalse(s['useful_descriptive_result'])
    def test_disagreement_uses_jev(self):
        s=score([self.row(0,b='REFUTE',j='REFUTE',gold='REFUTE')]);self.assertEqual(s['details'][0]['predictions']['cascade'],'REFUTE');self.assertEqual(s['counterfactual_cascade_jev_calls'],1)
    def test_matched_count(self):
        rows=[self.row(i,b='REFUTE' if i%3==0 else 'SUPPORT') for i in range(11)]
        s=score(rows);self.assertEqual(sum(x['matched_referred'] for x in s['details']),sum(x['referred'] for x in s['details']))
    def test_routing_never_uses_truth(self):
        rows=[self.row(i,b='REFUTE' if i%3==0 else 'SUPPORT') for i in range(11)];other=copy.deepcopy(rows)
        for r in other:r['expected']='UNCERTAIN'
        self.assertEqual([(r['referred'],r['matched_referred']) for r in score(rows)['details']],[(r['referred'],r['matched_referred']) for r in score(other)['details']])
    def test_random_expected_reference(self):
        rows=[self.row(0,b='REFUTE',gold='REFUTE',j='REFUTE'),self.row(1),self.row(2,gold='REFUTE',j='REFUTE')]
        actual=[]
        for chosen in itertools.combinations(range(3),1):actual.append(sum((r['labels']['jev'] if i in chosen else r['labels']['a'])!=r['expected'] for i,r in enumerate(rows))/3)
        self.assertAlmostEqual(score(rows)['families']['dev']['uniform_random_expected_error'],sum(actual)/len(actual))
    def test_missing_is_not_silent_null(self):
        r=self.row(1);r.update(status='not_run',labels={});s=score([self.row(0),r]);self.assertEqual(s['missing'],1);self.assertFalse(s['complete_evidence']);self.assertEqual(s['paired_delta_missing_bounds'],{'lower':-.5,'upper':.5});self.assertFalse(s['useful_descriptive_result'])
    def test_duplicate_refused(self):
        with self.assertRaises(ValueError):score([self.row(0),self.row(0)])
    def test_actor_projection_and_variant_fidelity(self):
        c=fixture('target_distractor','REFUTE',0,'DEV');c['secret_evaluator']='never_send';p=qwen_payload(c,0);q=qwen_payload(c,1)
        self.assertEqual(set(actor_input(c)),{'claim','report'});self.assertIn(c['claim'],p['messages'][0]['content']);self.assertNotIn('never_send',str(p));self.assertNotEqual(p['format'],q['format']);p.pop('format');q.pop('format');self.assertEqual(p,q)
class QualificationTests(unittest.TestCase):
    def test_each_class_floor_and_missingness(self):
        rows=[{'id':str(i), 'expected':label,'status':'completed','labels':{'a':label,'b':label,'jev':label}} for i,label in enumerate(['SUPPORT']*20+['REFUTE']*20+['UNCERTAIN']*20)]
        self.assertTrue(qualify(rows)['qualified'])
        for r in rows[:7]:r['labels']['jev']='REFUTE'
        self.assertFalse(qualify(rows)['qualified'])
        for r in rows[:7]:r['labels']['jev']='SUPPORT'
        rows[0]['status']='failed'
        self.assertFalse(qualify(rows)['qualified'])

class AdmissionTests(unittest.TestCase):
    def receipt(self):
        d={k:True for k in ('owner_plan_approved','public_plan_verified','exclusive_claim_verified','workload_verified','account_verified','source_verified','model_verified','original_ledger_verified')}
        d.update(stage='S0',plan_sha256='p',approval_plan_sha256='p',checked_epoch=1000,cumulative_call_cap=2671,cumulative_usd_cap=.10,incremental_usd_cap=.03,spent_usd=.040890822,uncertain_usd=.001344,projected_stage_usd=.002,incremental_spent_usd=0,ledger_entries=2179,claim_expires_epoch=6000)
        return d
    def test_valid_fixture(self):self.assertTrue(admit(self.receipt(),'S0','p',1000))
    def test_gates_fail_closed(self):
        for key,value in [('owner_plan_approved',False),('public_plan_verified',False),('exclusive_claim_verified',False),('account_verified',False),('approval_plan_sha256','old'),('ledger_entries',2670),('spent_usd',.099),('incremental_spent_usd',.029),('claim_expires_epoch',1100),('checked_epoch',0),('projected_stage_usd',float('nan'))]:
            with self.subTest(key=key):
                d=self.receipt();d[key]=value
                with self.assertRaises(ValueError):admit(d,'S0','p',1000)
    def test_s1_requires_matching_qualification(self):
        d=self.receipt();d['stage']='S1'
        with self.assertRaises(ValueError):admit(d,'S1','p',1000)
        d.update(s0_qualified=True,scientific_hash='new',s0_scientific_hash='old')
        with self.assertRaises(ValueError):admit(d,'S1','p',1000)
if __name__=='__main__':unittest.main()
