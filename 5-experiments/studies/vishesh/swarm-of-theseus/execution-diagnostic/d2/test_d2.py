import unittest,tempfile,json,sqlite3,time,copy,hashlib
from pathlib import Path
from unittest.mock import patch
from design import *
from scoring import reference
from admission import validate,public_check,GateError
import runner
from analyze import summarize

def oracle(a):
 return {'value':{'decisions':[{'id':c['id'],'command':d1.commands(a['context'])[d1.truth(c,a['context'],a['rule'])]} for c in a['cases']]},'error':None,'usage':{'input_tokens':10,'output_tokens':10},'actual_usd':.00006,'response_received':True}
class Tests(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.design=assignments();cls.a=next(a for a in cls.design if a['arm']=='D')
 def test_manifest(self):self.assertEqual(check(self.design)['calls'],432)
 def test_pairs(self):
  for seed in range(7100,7106):
   for family in ('release','incident'):
    d=[a for a in self.design if a['seed']==seed and a['context']==family and a['arm']=='D' and a['repeat']==0];self.assertEqual(d[0]['cases'],list(reversed(d[1]['cases'])))
    for a in d:
     es=[e for e in self.design if e['seed']==seed and e['context']==family and e['arm']=='E' and e['order']==a['order'] and e['repeat']==0]
     self.assertEqual({c['id'] for c in a['cases']},{e['cases'][0]['id'] for e in es})
 def test_all_oracles(self):
  for a in self.design:
   result=oracle(a);self.assertTrue(all(r['correct'] for r in reference(a,result)));self.assertTrue(all(r['correct'] for r in d1.score(a,result)['rows']))
 def test_malformed_contracts(self):
  a=self.a;good=oracle(a)
  bads=[]
  for kind in ('duplicate','missing','unknown','command','extra','type','notebook'):
   b=copy.deepcopy(good);ds=b['value']['decisions']
   if kind=='duplicate':ds.append(ds[0])
   if kind=='missing':ds.pop()
   if kind=='unknown':ds[0]['id']='unknown'
   if kind=='command':ds[0]['command']='console2/wrong'
   if kind=='extra':ds[0]['extra']=True
   if kind=='type':ds[0]['command']=123
   if kind=='notebook':b['value']['notebook']='unexpected'
   bads.append(b)
  for b in bads:
   self.assertFalse(any(r['correct'] for r in reference(a,b)));self.assertEqual([r['correct'] for r in reference(a,b)],[r['correct'] for r in d1.score(a,b)['rows']])
 def test_alias_diagnostic_only(self):
  a=self.a;b=oracle(a)
  for d in b['value']['decisions']:d['command']=d['command'].split('/')[-1]
  rs=reference(a,b);self.assertTrue(all(r['semantic_correct'] for r in rs));self.assertFalse(any(r['correct'] for r in rs))
 def test_raw_reparse(self):
  b=oracle(self.a);b['raw_text']='invalid json';self.assertFalse(any(r['correct'] for r in reference(self.a,b)))
 def test_budget(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'quota'
   with sqlite3.connect(p) as db:db.execute('CREATE TABLE budget(id,cap,used,calls,deadline)');db.execute('INSERT INTO budget VALUES(1,4,3.99,431,?)',(time.time()+5,))
   self.assertEqual(runner.reserve(p,.001,time.time()),432)
   with self.assertRaises(GateError):runner.reserve(p,.001,time.time())
 def receipt(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'prep';runner.prepare(p);r=json.loads((p/'admission-template.json').read_text())
  now=time.time();r.update(status='diagnostic-only',authority_allocation_id='fixture',owner_authorization_ref='fixture',claim_id='fixture',host='fixture',operator='fixture',review_policy_ref='fixture',allocation_verification_ref='fixture',exclusive_claim_verified=True,dependencies_verified=True,public_page_verified=True,verified_epoch=now,public_page_verified_epoch=now,pricing_verified_epoch=now,claim_until_epoch=now+8000,assessment_url=r['plan_url'].replace('D2-PLAN','D2-PRE'),assessment_sha256='a'*64)
  return r
 def test_admission(self):
  r=self.receipt();validate(r,r['source_commit'],self.design)
  for key,val in [('source_commit','bad'),('cap_usd',5),('prior_spend_usd',0),('verified_epoch',0),('claim_until_epoch',0),('public_page_verified',False),('assignments_sha256','bad'),('update_approval_sha256','bad')]:
   bad=dict(r);bad[key]=val
   with self.assertRaises(GateError):validate(bad,r['source_commit'],self.design)
 def test_public_hash(self):
  r=self.receipt()
  with self.assertRaises(GateError):public_check(r,lambda u:json.dumps({'experiments':[]}))
 def test_fixture_and_missing_denominators(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'calls').mkdir();(p/'manifest.json').write_text(json.dumps({'evidence_type':'SCRIPTED — NOT MODEL EVIDENCE','assignments':self.design}))
   for a in self.design[:3]:
    (p/'calls'/(a['id']+'-finished.json')).write_text(json.dumps(oracle(a)))
   s=summarize(p);self.assertEqual(s['assigned_decisions'],768);self.assertEqual(s['terminal_calls'],3);self.assertFalse(s['audit_disagreements']);self.assertIsNone(s['candidate_executor']);self.assertIn('SCRIPTED', (p/'replay.html').read_text())
 def test_served_model_mismatch_stops(self):
  class Response:
   def __enter__(self):return self
   def __exit__(self,*a):pass
   def read(self,n):return json.dumps({'model':'wrong','stop_reason':'end_turn','usage':{'input_tokens':10,'output_tokens':10},'content':[{'type':'text','text':'{"decisions":[]}'}]}).encode()
  with patch.object(runner.urllib.request,'urlopen',return_value=Response()):r=runner.invoke(self.a['request'],'TEST-NOT-A-SECRET')
  self.assertEqual(r['error'],'served_model_mismatch')
if __name__=='__main__':unittest.main()
