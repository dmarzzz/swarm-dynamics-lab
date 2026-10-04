import unittest,json,copy,tempfile,sqlite3,time
from pathlib import Path
from design import *
from scoring import reference
import runner
from admission import validate,GateError,public_check
from analyze import summarize

def oracle(a):return {'value':{'decisions':[{'id':a['cases'][0]['id'],'command':d1.commands(a['context'])[d1.truth(a['cases'][0],a['context'],a['rule'])]}]},'error':None,'actual_usd':.0001,'usage':{'input_tokens':20,'output_tokens':16},'response_received':True}
class Test(unittest.TestCase):
 @classmethod
 def setUpClass(cls):cls.aa=assignments()
 def test_manifest(self):self.assertEqual(check(self.aa)['calls'],384)
 def test_pair_information(self):
  for a in self.aa:
   p=next(x for x in self.aa if x['cases']==a['cases'] and x['context']==a['context'] and x['repeat']==a['repeat'] and x['arm']!=a['arm']);self.assertEqual(a['request']['messages'],p['request']['messages'])
 def test_schema(self):
  for a in self.aa:
   if a['arm']=='F':
    s=a['request']['output_config']['format']['schema']['properties']['decisions'];self.assertEqual(s['minItems'],1);self.assertEqual(s['maxItems'],1);self.assertEqual(s['items']['properties']['id']['enum'],[a['cases'][0]['id']])
 def test_oracles_and_failures(self):
  for a in self.aa:
   r=oracle(a);self.assertTrue(reference(a,r)[0]['correct']);self.assertTrue(d1.score(dict(a,arm='E'),r)['rows'][0]['correct'])
  for kind in ('id','command','duplicate','missing','extra'):
   a=self.aa[0];r=oracle(a);d=r['value']['decisions']
   if kind=='id':d[0]['id']='bad'
   if kind=='command':d[0]['command']='bad'
   if kind=='duplicate':d.append(copy.deepcopy(d[0]))
   if kind=='missing':d.clear()
   if kind=='extra':r['value']['notebook']='bad'
   self.assertFalse(reference(a,r)[0]['correct']);self.assertFalse(d1.score(dict(a,arm='E'),r)['rows'][0]['correct'])
 def test_d2_regression_cases(self):
  # Saved failures are software regressions only, not fresh empirical samples.
  import tarfile
  with tarfile.open(ROOT/'results/D2/evidence.tar.gz') as t:
   m=json.load(t.extractfile('manifest.json'));target=0
   for a in m['assignments']:
    if a['arm']!='E':continue
    r=json.load(t.extractfile('calls/'+a['id']+'-finished.json'))
    if not reference(a,r)[0]['correct']:
     target+=1;new=request(a['cases'][0],a['rule'],a['context'],'F');self.assertEqual(new['output_config']['format']['schema']['properties']['decisions']['items']['properties']['id']['enum'],[a['cases'][0]['id']]);self.assertTrue(reference(a,oracle(a))[0]['correct'])
   self.assertEqual(target,11)
 def test_budget(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'db'
   with sqlite3.connect(p) as db:db.execute('CREATE TABLE budget(id,cap,used,calls,deadline)');db.execute('INSERT INTO budget VALUES(1,3.7,3.69,383,?)',(time.time()+10,))
   self.assertEqual(runner.reserve(p,.001,time.time()),384)
   with self.assertRaises(GateError):runner.reserve(p,.001,time.time())
 def test_admission(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t)/'prep';runner.prepare(p);r=json.loads((p/'admission-template.json').read_text())
  now=time.time();r.update(status='diagnostic-only',authority_allocation_id='fixture',owner_authorization_ref='fixture',claim_id='fixture',host='fixture',operator='fixture',review_policy_ref='fixture',allocation_verification_ref='fixture',exclusive_claim_verified=True,dependencies_verified=True,public_page_verified=True,verified_epoch=now,public_page_verified_epoch=now,pricing_verified_epoch=now,claim_until_epoch=now+8000,assessment_url=r['plan_url'].replace('R1-PLAN','R1-PRE'),assessment_sha256='a'*64);validate(r,r['source_commit'],self.aa)
  for k,v in [('prior_spend_usd',0),('cap_usd',5),('verified_epoch',0),('claim_until_epoch',0),('assignments_sha256','bad'),('public_page_verified',False)]:
   bad=dict(r);bad[k]=v
   with self.assertRaises(GateError):validate(bad,r['source_commit'],self.aa)
  with self.assertRaises(GateError):public_check(r,lambda u:json.dumps({'experiments':[]}))
 def test_full_oracle_and_missing(self):
  with tempfile.TemporaryDirectory() as t:
   p=Path(t);(p/'calls').mkdir();(p/'manifest.json').write_text(json.dumps({'assignments':self.aa,'evidence_type':'SCRIPTED — NOT MODEL EVIDENCE'}))
   s=summarize(p);self.assertEqual(s['assigned_decisions'],384);self.assertIsNone(s['candidate_executor'])
   for a in self.aa:(p/'calls'/(a['id']+'-finished.json')).write_text(json.dumps(oracle(a)))
   s=summarize(p);self.assertTrue(s['arms']['E']['qualified']);self.assertTrue(s['arms']['F']['qualified']);self.assertFalse(s['audit_disagreements']);self.assertEqual(s['mean_F_minus_E'],0)
if __name__=='__main__':unittest.main()
