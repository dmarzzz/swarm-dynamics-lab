import copy, itertools, unittest
import study_receipts as s
class Tests(unittest.TestCase):
 def test_public_plan_contract(self):
  import sys
  sys.path.insert(0,str(s.ROOT.parent.parent/'experiment-documentation'))
  from public_plan import validate
  p=validate({'id':'immune-response-v3','description':'TLDR: Paired evidence diagnostic','url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/researchers/vishesh/notes/immune-response-v3/evidence-study/README.md'},(s.ROOT/'README.md').read_text(),'Paired evidence receipts with clean and stale memory and exact shared reviewer outputs')
  self.assertEqual(p['experiment'],'immune-response-v3')
 def test_receipt_all_boolean_patterns(self):
  for a in itertools.product([False,True],repeat=4):
   obs=dict(zip(s.CHECKS,a))
   for b in itertools.product([False,True],repeat=4):
    claim=dict(zip(s.CHECKS,b));p={'observed_checks':claim};r=s.receipt(p,obs,True)
    self.assertEqual(r['status']=='match',a==b)
    self.assertEqual(len(r['mismatches']),sum(x!=y for x,y in zip(a,b)))
    self.assertEqual(s.receipt(p,obs,False)['mismatches'],[])
 def test_strict_claim_types(self):
  self.assertFalse(s.valid_checks(dict.fromkeys(s.CHECKS,1)))
  self.assertEqual(s.receipt({},dict.fromkeys(s.CHECKS,True),True)['status'],'missing_claims')
 def test_reference_and_clean_control(self):
  for c,m,checked in itertools.product(s.CASES,['clean','stale'],[False,True]):
   f=s.fixture(c,9290);proposals=s.get_advice(f,m,None,lambda e:None)
   r=s.execute_episode(f,m,checked,proposals,None,lambda e:None)
   self.assertEqual(r['invalid'],0);self.assertTrue(r['final_healthy']);self.assertGreaterEqual(r['healthy_ticks'],5)
   self.assertEqual(r['damage_events'],0);self.assertEqual(r['claim_errors'],0)
   if c=='false_alarm':self.assertEqual(r['deployments'],0)
   if c=='migrated_data':self.assertEqual(r['probe_regressions'],1)
   if m=='clean':self.assertTrue(all(not x['visible_memory_ids'] for x in r['trace']))
   else:self.assertIn('delayed-handoff-17',r['trace'][3]['visible_memory_ids'])
 def test_paired_advice_no_mutation(self):
  f=s.fixture('stale_advice',9290);p=s.get_advice(f,'stale',None,lambda e:None);p[0]['observed_checks']['data_readable']=True;before=copy.deepcopy(p)
  a=s.execute_episode(f,'stale',False,p,None,lambda e:None);b=s.execute_episode(f,'stale',True,p,None,lambda e:None)
  self.assertEqual(p,before);self.assertEqual(a['proposal_hash'],b['proposal_hash']);self.assertEqual(a['healthy_ticks'],b['healthy_ticks']);self.assertEqual(b['advice'][0]['receipt']['status'],'mismatch')
 def test_faithful_claim_is_not_good_action(self):
  class Bad:
   def complete(self,request,fallback):
    o=request['observation'];return dict(action='deploy',service=o['roles_to_services']['gateway'],version=1,reason='test',observed_checks=o['health_probe'])
  f=s.fixture('false_alarm',9290);r=s.execute_episode(f,'clean',True,[],Bad(),lambda e:None)
  self.assertEqual(r['claim_errors'],0);self.assertGreater(r['damage_events'],0);self.assertEqual(r['healthy_ticks'],0)
 def test_rejected_vs_applied_damage(self):
  class Unsafe:
   def complete(self,request,fallback):
    o=request['observation'];return dict(action='deploy',service=o['roles_to_services']['store'],version=1,reason='test',observed_checks=o['health_probe'])
  r=s.execute_episode(s.fixture('migrated_data',9290),'clean',True,[],Unsafe(),lambda e:None)
  self.assertEqual(r['rejected_actions'],6);self.assertEqual(r['damage_events'],0)
 def test_missing_response_keeps_denominator(self):
  class Broken:
   def complete(self,request,fallback):raise ValueError('do not expose arbitrary error text')
  f=s.fixture('stale_advice',9290);r=s.execute_episode(f,'clean',True,[],Broken(),lambda e:None)
  self.assertEqual(len(r['trace']),6);self.assertEqual(r['invalid'],6);self.assertEqual(r['healthy_ticks'],0)
 def test_equal_count_tradeoff_means_damage(self):
  # Losing one passed check counts even if a different failed check is repaired.
  before=dict(rpc_compatible=True,data_readable=False,storage_format=True,requested_feature=True)
  after=dict(rpc_compatible=False,data_readable=True,storage_format=True,requested_feature=True)
  self.assertEqual(sum(before.values()),sum(after.values()));self.assertEqual([k for k in s.CHECKS if before[k] and not after[k]],['rpc_compatible'])
if __name__=='__main__':unittest.main()
