"""Offline contract/fault checks, not model evidence."""
import unittest,copy,sqlite3
from contextlib import closing
from definition import cases,request,assess,ARMS,LABELS,digest
from worker import admission
from relay import payloads
from jev_relay import reserve

class Contract(unittest.TestCase):
 def rows(self):return [{**c,'labels':{a:c['expected'] for a in ARMS}} for c in cases()]
 def test_balanced_unique(self):
  c=cases();self.assertEqual(len({x['id'] for x in c}),60)
  for k in LABELS:self.assertEqual(sum(x['expected']==k for x in c),20)
 def test_truth_cannot_enter_actor(self):
  c=cases()[0];p=request(c,0,'x','SUPPORT');c['expected']='FORGED';c['secret_truth']='FORGED';self.assertEqual(p,request(c,0,'x','SUPPORT'));self.assertNotIn('FORGED',str(p))
 def test_treatment_is_proposal_only(self):
  c=cases()[0];b=request(c,0,'x');p=request(c,0,'x','REFUTE');self.assertEqual(b['state']['report'],p['state']['report']);self.assertEqual(b['questions']['label']['criteria'],p['questions']['label']['criteria']);self.assertEqual(set(p['state'])-set(b['state']),{'qwen_proposal'})
 def test_rotation_survives_wire(self):
  self.assertEqual([next(iter(request(cases()[0],i,'x')['questions']['label']['criteria'])) for i in range(3)],list(LABELS))
 def test_qwen_failure_does_not_block_composite(self):
  r=self.rows()
  for x in r:x['labels']['qwen']='UNCERTAIN'
  a=assess(r);self.assertFalse(a['qwen']['passed']);self.assertTrue(a['admit_s1'])
 def test_class_floor_not_overall_only(self):
  r=self.rows();subset=[x for x in r if x['expected']=='REFUTE']
  for x in subset[:7]:x['labels']['qwen+jev']='SUPPORT'
  a=assess(r);self.assertGreater(a['qwen+jev']['accuracy'],.85);self.assertFalse(a['admit_s1'])
 def test_missing_fails(self):
  r=self.rows();del r[0]['labels']['qwen+jev'];a=assess(r);self.assertFalse(a['admit_s1']);self.assertEqual(a['qwen+jev']['valid'],59)
 def test_anchoring(self):
  r=self.rows();x=r[0];wrong=next(k for k in LABELS if k!=x['expected']);x['labels']['qwen']=x['labels']['qwen+jev']=wrong;self.assertEqual(assess(r)['paired']['anchoring'],1)
 def test_allowed_payloads_cover_all_proposals(self):
  a=payloads('S0');self.assertEqual(len(a),240)
  for i,c in enumerate(cases()):
   for proposal in (None,*LABELS):self.assertIn(digest(request(c,i,'C1-S0',proposal)),a)
 def good_admission(self):return dict(stage='S0',decision='diagnostic-only',checked_epoch=1000,exclusive_claim_verified=True,workload_verified=True,budget_verified=True,page_verified=True,claim_expires_epoch=3000,cumulative_usd_cap=.1,remaining_usd=.08,host='fixture',claim_id='fixture')
 def test_admission_pass(self):self.assertTrue(admission(self.good_admission(),'S0',1000))
 def test_expired_and_missing_admission(self):
  for key,value in [('checked_epoch',1),('exclusive_claim_verified',False),('workload_verified',False),('budget_verified',False),('page_verified',False),('claim_expires_epoch',1100),('cumulative_usd_cap',1),('remaining_usd',0),('stage','S1'),('decision','ready')]:
   a=self.good_admission();a[key]=value
   with self.subTest(key=key),self.assertRaises(ValueError):admission(a,'S0',1000)
 def test_s1_requires_ready(self):
  a=self.good_admission();a.update(stage='S1',claim_expires_epoch=10000)
  with self.assertRaises(ValueError):admission(a,'S1',1000)
  a['decision']='ready';self.assertTrue(admission(a,'S1',1000))
 def test_shared_budget_no_reset(self):
  with closing(sqlite3.connect(':memory:')) as db:
   db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');db.execute('INSERT INTO calls VALUES(?,?,?,?)',('historic',1344000,'completed',.099));db.commit()
   with self.assertRaises(RuntimeError):reserve(db,'new',2160,True)
   self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],1)
 def test_duplicate_rejected(self):
  with closing(sqlite3.connect(':memory:')) as db:
   db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');reserve(db,'a',2160,True)
   with self.assertRaises(sqlite3.IntegrityError):reserve(db,'a',2160,True)
 def test_uncertain_spend_reserved(self):
  with closing(sqlite3.connect(':memory:')) as db:
   db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)')
   for i in range(74):reserve(db,str(i),2160,True)
   with self.assertRaises(RuntimeError):reserve(db,'over',2160,True)
 def test_qwen_wire_unchanged(self):
  from unittest.mock import patch
  from providers import Qwen as Old
  from qwen_trace import Qwen as New
  import io,json
  obs={'claim':'dev claim','report':'dev accuracy improved'};captured=[]
  def respond(req,timeout):
   captured.append(json.loads(req.data));return io.BytesIO(json.dumps({'message':{'content':'{"label":"IMPROVED"}'},'prompt_eval_count':5,'eval_count':4}).encode())
  with patch('urllib.request.urlopen',side_effect=respond):
   old=Old.__new__(Old).predict(obs,4,2);new=New.__new__(New).predict(obs,4,2)
  self.assertEqual(captured[0],captured[1]);self.assertEqual(old,{k:new[k] for k in old});self.assertEqual(new['request_payload'],captured[1])
if __name__=='__main__':unittest.main()
