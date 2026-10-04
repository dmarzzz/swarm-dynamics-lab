import copy,itertools,unittest
import study as s
class Test(unittest.TestCase):
 def test_feasible_all_cases_arms(self):
  for c,a in itertools.product(s.CASES,s.ARMS):
   row=s.execute_episode(s.fixture(c,8900),a,None,lambda _:None)
   self.assertEqual(row['invalid'],0);self.assertEqual(row['final_healthy'],1);self.assertEqual(row['unsafe_changes'],0)
 def test_multiple_feasible_bundles(self):
  f=s.fixture('stale_advice',8900)
  self.assertTrue(all(s.health(f,{'gateway':1,'worker':1,'store':1}).values()))
  self.assertTrue(all(s.health(f,{'gateway':2,'worker':2,'store':1}).values()))
 def test_old_snapshot_unsafe_after_migration(self):
  f=s.fixture('migrated_data',8901);self.assertFalse(all(s.health(f,dict(gateway=1,worker=1,store=1)).values()))
 def test_false_alarm_no_changes_needed(self):
  row=s.execute_episode(s.fixture('false_alarm',8902),'retain',None,lambda _:None);self.assertEqual(row['healthy_ticks'],6);self.assertEqual(row['deployments'],0)
 def test_revision_uses_observable_metadata(self):
  f=s.fixture('stale_advice',8900);notes=s.notes(f);self.assertEqual(s.memory_view(notes,'revision_check',f['revision']),[notes[1]])
 def test_reset_can_learn_again(self):
  f=s.fixture('stale_advice',8900);n=s.notes(f);self.assertEqual(s.memory_view(n,'reset',f['revision']),n)
 def test_no_case_or_arm_leak(self):
  f=s.fixture('stale_advice',8900);o=s.observe(f,f['deployed'],1,s.notes(f),'retain',[]);self.assertNotIn('case',o);self.assertNotIn('arm',o)
 def test_input_state_not_mutated(self):
  f=s.fixture('migrated_data',8901);before=copy.deepcopy(f);s.execute_episode(f,'retain',None,lambda _:None);self.assertEqual(before,f)
 def test_new_worker_can_drop_old_reader_compatibility(self):
  f=s.fixture('false_alarm',8903);d=dict(f['deployed']);d['worker']=3
  self.assertFalse(s.health(f,d)['data_readable'])
 def test_unsafe_attempt_preserved(self):
  class P:
   calls=0
   def complete(self,request,fallback):
    o=request['observation']
    if 'review_role' in o:return {'recommendation':'Check health before changing anything'}
    self.calls+=1
    if self.calls==1:return {'action':'deploy','service':o['roles_to_services']['store'],'version':2,'reason':'Deliberate unsafe test'}
    return {'action':'wait','service':'none','version':0,'reason':'No further changes'}
  row=s.execute_episode(s.fixture('false_alarm',8903),'retain',P(),lambda _:None)
  self.assertEqual(row['unsafe_changes'],1);self.assertEqual(row['invalid'],0);self.assertEqual(row['healthy_ticks'],6)
if __name__=='__main__':unittest.main()
