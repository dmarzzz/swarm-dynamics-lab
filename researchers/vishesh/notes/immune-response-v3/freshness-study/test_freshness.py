import copy,unittest
import freshness as s
class Semantics(unittest.TestCase):
 def test_restart_semantics(self):
  for case,useful,redundant in [('healthy_fresh',0,1),('fresh_crash',1,0)]:
   f,w=s.fixture(case,9401);r=s.step(f,w,s.action('deploy',f['alias']['worker'],w['deployed']['worker']));self.assertEqual((r['useful_restart'],r['redundant']),(useful,redundant));self.assertEqual(r['healthy'],1)
 def test_stale_states_hidden(self):
  for case in ['stale_false_alarm','masked_crash']:
   f,w=s.fixture(case,9401);o=s.observe(f,w,1,[],[],False);self.assertNotEqual(all(o['cached_probe']['checks'].values()),all(s.health(f,w).values()));self.assertNotIn('case',o);self.assertNotIn('live',o)
 def test_receipt_uses_only_metadata(self):
  self.assertEqual(s.receipt({'epoch':6},7)['status'],'stale');self.assertEqual(s.receipt({'epoch':7},7)['status'],'current')
 def test_inspection_and_cache(self):
  f,w=s.fixture('masked_crash',9401);s.step(f,w,s.action('inspect'));self.assertFalse(w['probe']['live']['worker']);epoch=w['probe']['epoch'];s.step(f,w,s.action('deploy',f['alias']['worker'],2));self.assertEqual(w['probe']['epoch'],epoch);self.assertNotEqual(w['epoch'],epoch)
 def test_baseline_all_cases(self):
  for c in s.CASES:
   f,w=s.fixture(c,9401);tr=[]
   for t in range(1,5):tr.append(s.step(f,w,s.reference(s.observe(f,w,t,[],[],False))))
   self.assertTrue(tr[-1]['healthy'],c);self.assertGreaterEqual(sum(x['healthy'] for x in tr),2,c);self.assertEqual(sum(x['redundant']+x['rejected']+x['lost_health'] for x in tr),0,c)
   if c.startswith('healthy') or c=='stale_false_alarm':self.assertFalse(any(x['action']['action']=='deploy' for x in tr),c)
 def test_stale_trusting_fails_masked_crash(self):
  f,w=s.fixture('masked_crash',9401)
  for t in range(1,5):
   o=s.observe(f,w,t,[],[],False);o['cached_probe']['epoch']=o['current_epoch'];s.step(f,w,s.reference(o))
  self.assertFalse(all(s.health(f,w).values()))
 def test_destructive_store_rejected(self):
  f,w=s.fixture('schema_transition',9401);before=copy.deepcopy(w);r=s.step(f,w,s.action('deploy',f['alias']['store'],1));self.assertEqual(r['rejected'],1);self.assertEqual(w,before)
 def test_same_arm_source_records(self):
  f,w=s.fixture('masked_crash',9401);a=[{'observed_epoch':6,'recommendation':'inspect','role':'test'}];raw=s.observe(f,w,1,[],a,False);checked=s.observe(f,w,1,[],a,True);checked.pop('probe_receipt');checked['team_advice'][0].pop('freshness_receipt');self.assertEqual(raw,checked)
if __name__=='__main__':unittest.main()

class Admission(unittest.TestCase):
 def test_credential_payload_fails_closed(self):
  from launch import validate
  for p in [{},{'key':'invalid','workspace':'invalid'},{'key':'invalid','workspace':'invalid','extra':True}]:
   with self.assertRaises(ValueError):validate(p)

class ActionContract(unittest.TestCase):
 def allowed(self,schema,a):
  return any(all(a[k] in rule['enum'] for k,rule in branch['properties'].items()) for branch in schema['anyOf'])
 def test_every_schema_combination_has_defined_engine_result(self):
  import itertools
  for case in s.CASES:
   f,w=s.fixture(case,9401);sc=s.legacy_schema(f)
   for kind,service,version in itertools.product(['deploy','inspect','refresh','wait'],list(f['alias'].values())+['none'],range(4)):
    a=s.action(kind,service,version)
    if self.allowed(sc,a):s.step(f,copy.deepcopy(w),a)
 def test_retained_a5_invalid_inspect_is_rejected_by_visible_schema(self):
  f,w=s.fixture('stale_false_alarm',9401)
  self.assertFalse(self.allowed(s.legacy_schema(f),s.action('inspect',f['alias']['worker'],0)))
  self.assertTrue(self.allowed(s.legacy_schema(f),s.action('inspect')))
 def test_no_nonexistent_service_version_in_schema(self):
  f,w=s.fixture('healthy_fresh',9401)
  self.assertFalse(self.allowed(s.legacy_schema(f),s.action('deploy',f['alias']['gateway'],3)))
