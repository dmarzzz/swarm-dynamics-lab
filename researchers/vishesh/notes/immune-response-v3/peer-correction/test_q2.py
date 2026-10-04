import copy,datetime,sqlite3,tempfile,time,unittest
from pathlib import Path
from contextlib import closing
import q2_native as n,q2_admission as a,q2_qualification as q,q2_relay as relay
import test_native as original
import test_instrument as original_instrument
class Q2Tests(unittest.TestCase):
 def test_complete_rule_collection_has_same_semantics_and_visible_contract(self):
  events=[];r=q.collect(original_instrument.CollectionTests.Rule(),events.append)
  self.assertTrue(r['automated_pass']);self.assertEqual(48,r['calls_attempted'])
  for e in events:
   if e['kind']=='request' and e['phase']=='action':self.assertIn('reason: at most 240 characters',e['body']['messages'][0]['content'])
 def test_48_limit_preserves_q1_and_history(self):
  with tempfile.TemporaryDirectory() as d:
   root=Path(d);db=root/'ledger';original.ledger(db)
   with closing(sqlite3.connect(db)) as c,c:
    c.execute('update budget set calls=711,reserved=15.606955')
    for j in range(2):c.execute('insert into immune_requests values(?,?,?,?,?,?,?,?,?,?)',(str(j),'peer-correction-q1','old','response_received',.04113,1,1,.01,1,2))
   p=n.Policy(db,root/'usage','peer-contract-q2','newpacket',time.time()+900)
   with self.assertRaisesRegex(ValueError,'already_claimed'):n.Policy(db,root/'other','peer-contract-q2','newpacket',time.time()+900)
   for _ in range(48):p.reserve(b'x'*8000)
   with self.assertRaisesRegex(ValueError,'persistent_budget'):p.reserve(b'x')
   with closing(sqlite3.connect(db)) as c:
    used,calls=c.execute('select reserved,calls from budget').fetchone();self.assertAlmostEqual(18.264235,used);self.assertEqual(759,calls)
    self.assertEqual(2,c.execute("select count(*) from immune_requests where run_id='peer-correction-q1'").fetchone()[0])
    self.assertEqual(48,c.execute("select count(*) from immune_requests where run_id='peer-contract-q2'").fetchone()[0])
   for stage in ('peer-correction-q1','peer-correction-p1'):
    with self.assertRaisesRegex(ValueError,'unfunded'):n.Policy(db,root/'other',stage,'x',time.time()+900)
 def test_q2_admission_scope_and_time(self):
  r,now=original.AdmissionTests().receipt();r.update(stage='peer-contract-q2',campaign_max_calls=48,campaign_model_max_usd=2.657280,infrastructure_reserved_usd=.03)
  r['allocation']['expires']=(now+datetime.timedelta(minutes=20)).isoformat();p={'contract_sha256':'offline'}
  self.assertTrue(a.validate_contract(r,p,now,'offline'))
  for k,v in [('stage','peer-correction-p1'),('campaign_max_calls',232),('funded',False),('infrastructure_reserved_usd',.031)]:
   bad=copy.deepcopy(r);bad[k]=v
   with self.assertRaises(ValueError):a.validate_contract(bad,p,now,'offline')
  for minutes in (11,21):
   bad=copy.deepcopy(r);bad['allocation']['expires']=(now+datetime.timedelta(minutes=minutes)).isoformat()
   with self.assertRaises(ValueError):a.validate_contract(bad,p,now,'offline')
  self.assertEqual((48,2.657280,900),relay.limits('peer-contract-q2'))
  with self.assertRaises(ValueError):relay.limits('peer-correction-p1')
class PublicPlanTest(unittest.TestCase):
 def test_actual_plan_shape(self):
  import importlib.util
  path=Path(__file__).resolve().parent
  spec=importlib.util.spec_from_file_location('q2_public_test',path.parent.parent/'experiment-documentation/public_plan.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
  module.validate({'id':'immune-response-v3','url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/Q2-PLAN.md','description':'TLDR: qualification'},(path/'Q2-PLAN.md').read_text(),'Q2 explicit existing limits: fixed outcomes and all assigned development worlds.')
if __name__=='__main__':unittest.main()
