import unittest,copy,json
from pathlib import Path
from cases import build
from contract import compare,score,summarize,request,bound,core
from baseline import solve,parse
class Tests(unittest.TestCase):
 def test_development_oracle_and_strong_parser(self):
  rows=build('development-v2');records=[]
  for row in rows:
   s=score(row,solve(row['actor']));self.assertTrue(s['labels_correct']);self.assertTrue(s['quotes_valid']);self.assertEqual(s['source_facts_correct'],3);self.assertEqual(s['report_facts_correct'],len(row['actor']['reports']));self.assertTrue(s['decision_correct']);self.assertLessEqual(bound(request(row['actor'])),10000);records.append({'valid':True,'score':s})
  self.assertTrue(summarize(rows,records)['qualified'])
 def test_same_threshold_different_value(self):
  f=dict(entity='e',time='12:00',property='mass_g',value=6000,status='observed');self.assertEqual(compare(f,f|{'value':7000}),'CONTRADICTED');self.assertEqual(compare(f,f|{'value':None,'status':'unknown'}),'NOT_ESTABLISHED')
 def test_unknown_and_identity(self):
  f=dict(entity='e',time='12:00',property='running',value=1,status='observed')
  for delta in [{'entity':'other'},{'time':'13:00'},{'status':'unknown','value':None}]:self.assertEqual(compare(f,f|delta),'NOT_ESTABLISHED')
 def test_faults_exposed(self):
  row=build('development-v2')[0];a=solve(row['actor']);a['sources']['s0']['value']=99;s=score(row,a);self.assertLess(s['source_facts_correct'],3);self.assertFalse(s['labels_correct'])
  a=solve(row['actor']);a['sources']['s0']['quote']='At';self.assertFalse(score(row,a)['quotes_valid'])
  a=solve(row['actor']);a['sources']['s0']['value']=True
  with self.assertRaises(ValueError):score(row,a)
 def test_pairing(self):
  rows=build('development-v2')
  for root in {r['root'] for r in rows}:
   pair=sorted([r for r in rows if r['root']==root],key=lambda r:r['condition']['copies']);a,b=pair
   self.assertEqual(a['actor']['sources'],b['actor']['sources']);self.assertEqual(a['gold']['decision'],b['gold']['decision']);self.assertEqual(len(b['actor']['reports'])-len(a['actor']['reports']),2)
 def test_all_previous_false_flags(self):
  path=Path(__file__).resolve().parents[2]/'results/QM-PQ-01/fidelity-analysis.json';rows=json.loads(path.read_text())['mismatches'];self.assertEqual(len(rows),18)
  for r in rows:
   f=parse(r['report']);s=parse(r['source'],f);self.assertEqual(compare(s,f),'SUPPORTED')
 def test_absent_and_failed_rows_never_qualify(self):
  self.assertFalse(summarize(build('development-v2'),[])['qualified'])
if __name__=='__main__':unittest.main()

class AdmissionTests(unittest.TestCase):
 def test_fail_closed_admission(self):
  import runtime,time,socket
  from unittest.mock import patch
  here=Path(__file__).resolve().parent
  # Qualification actor rows are not opened in this test; synthesize a development manifest.
  rows=build('admission-fixture');manifest={'attempt':'QM-PQ-02','assignments':[{'request_sha256':__import__('contract').digest(request(r['actor']))} for r in rows]};packet={'manifest':manifest,'rows':rows}
  c={'source_sha256':runtime.hashes(),'owner_directed_qualification':True,'max_calls':24,'max_reserved_usd':1.44,'allocation':{'host':socket.gethostname().split('.')[0],'exclusive':True,'approved_account_verified':True,'merged_claim_verified':True,'workload_verified_clear':True,'checked_at':time.time(),'expires_at':time.time()+60,'claim_id':'fixture'},'deadline':time.time()+60,'infrastructure_total_bound_usd':.2,'cumulative_hours_bound':2,'ledger':'fixture','budget_extension_sha256':runtime.hashes()['AUTHORIZATION.json'],'run_tldr':'fixture','plan_url':'fixture'}
  real_read=Path.read_text
  def read(p,*args,**kwargs):return json.dumps(manifest) if p==here/'manifest.json' else real_read(p,*args,**kwargs)
  with patch.object(Path,'read_text',read),patch.object(runtime.legacy,'Ledger') as ledger,patch.object(runtime.public_plan,'check',return_value={'url':'fixture','plan_sha256':runtime.hashes()['PLAN.md']}),patch.object(runtime,'route_check',return_value={}):
   ledger.return_value.audit.return_value={'calls':73,'uncertain':0,'reserved_usd':.785856};runtime.preflight(c,packet)
   for key,val in [('source_sha256',{}),('owner_directed_qualification',False),('max_calls',25),('max_reserved_usd',2),('deadline',0),('budget_extension_sha256','bad')]:
    d=copy.deepcopy(c);d[key]=val
    with self.assertRaises(AssertionError):runtime.preflight(d,packet)
   for key,val in [('exclusive',False),('approved_account_verified',False),('merged_claim_verified',False),('workload_verified_clear',False),('expires_at',0),('checked_at',0),('host','wrong')]:
    d=copy.deepcopy(c);d['allocation'][key]=val
    with self.assertRaises(AssertionError):runtime.preflight(d,packet)
   ledger.return_value.audit.return_value={'calls':73,'uncertain':1,'reserved_usd':.785856}
   with self.assertRaises(AssertionError):runtime.preflight(c,packet)
