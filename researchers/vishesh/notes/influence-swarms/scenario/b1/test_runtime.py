import copy,datetime as dt,json,sqlite3,tempfile,unittest
from pathlib import Path
import cases as c,instrument as i,runtime as r
from test_b1 import fixture,cell
class RuntimeTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.dir=Path(self.tmp.name);self.ledger=self.dir/'budget.sqlite'
  with r.database(self.ledger) as db:db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,20,7.961696,530)');db.execute('CREATE TABLE b1_scope(packet_sha256 TEXT PRIMARY KEY,maximum_model REAL,model_debited REAL,hosting_reserved REAL,status TEXT)');db.execute('INSERT INTO b1_scope VALUES(?,10.50624,0,0.5,"funded")',(r.FROZEN_PACKET,))
  self.cases=[c.make(f,s) for f in c.FAMILIES for s in range(5)]
 def body(self,wire):
  obs=json.loads(wire['messages'][1]['content']);case=next(x for x in self.cases if x['brief']==obs['brief']);a=fixture(case,obs['output_kind']=='final_decision')
  return c.encoded({'provider':'OpenAI','model':i.MODEL,'usage':{'prompt_tokens':100,'completion_tokens':100,'cost':.00006},'choices':[{'finish_reason':'stop','message':{'content':json.dumps(a)}}]})
 def transport(self,raw):return self.body(json.loads(raw))
 def collect(self,transport=None,out='attempt'):
  return r.collect('B1-D0',self.cases,self.dir/out,self.ledger,out,transport or self.transport,(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=2)).isoformat(),{'reserved':7.961696,'calls':530})
 def budget(self):
  with r.database(self.ledger) as db:return db.execute('SELECT cap,reserved,calls FROM budget').fetchone()
 def test_complete_preserves_ledger_and_gate(self):
  s=self.collect();self.assertEqual(s['calls'],240);self.assertEqual(s['valid_calls'],240);self.assertTrue(s['complete']);self.assertEqual(self.budget()[2],770);self.assertAlmostEqual(self.budget()[1],9.129056)
  self.assertTrue(json.loads((self.dir/'attempt/assessment.json').read_text())['qualified'])
  with self.assertRaises(FileExistsError):self.collect()
 def test_full_evaluation_and_unchanged_science(self):
  d=[cell(x,cond,arm)[0] for x in self.cases if x['split']=='development' for cond in i.CONDITIONS for arm in i.ARMS]
  with r.database(self.ledger) as db:db.execute('UPDATE budget SET reserved=9.129056,calls=770');db.execute('UPDATE b1_scope SET model_debited=1.16736')
  s=r.collect('B1-E0',self.cases,self.dir/'e0',self.ledger,'e0',self.transport,(dt.datetime.now(dt.timezone.utc)+dt.timedelta(hours=2)).isoformat(),{'reserved':9.129056,'calls':770},d)
  self.assertTrue(s['complete']);self.assertEqual(s['valid_calls'],1920);self.assertAlmostEqual(self.budget()[1],r.MODEL_CEILING);self.assertEqual(self.budget()[2],2690)
  self.assertEqual(json.loads((self.dir/'e0/assessment.json').read_text())['overall_mean'],0)
 def test_reservation_precedes_transport(self):
  def fail(raw):self.assertEqual(self.budget()[2],531);raise TimeoutError('secret-like text must not be logged')
  s=self.collect(fail);self.assertEqual(s['calls'],1);self.assertEqual(s['unstarted_calls'],239);self.assertEqual(s['usage_missing'],1);self.assertIsNone(s['actual_usd']);self.assertNotIn('secret-like',(self.dir/'attempt/events.jsonl').read_text())
 def test_invalid_answer_cost_retained(self):
  def bad(raw):b=json.loads(self.transport(raw));b['choices'][0]['message']['content']='not json';return c.encoded(b)
  s=self.collect(bad);self.assertEqual(s['calls'],1);self.assertEqual(s['valid_calls'],0);self.assertEqual(s['usage_missing'],0);self.assertAlmostEqual(s['actual_usd'],.00006)
 def test_route_cost_and_usage_fail_closed(self):
  for idx,key in enumerate(('route','cost','usage')):
   def bad(raw):
    b=json.loads(self.transport(raw))
    if key=='route':b['provider']='Other'
    if key=='cost':b['usage']['cost']=1
    if key=='usage':del b['usage']
    return c.encoded(b)
   # Each test journal uses a fresh fixture ledger, not a real budget reset.
   with r.database(self.ledger) as db:db.execute('UPDATE budget SET reserved=7.961696,calls=530')
   s=self.collect(bad,'bad'+str(idx));self.assertEqual(s['calls'],1);self.assertFalse(s['complete'])
 def test_unamended_cap_rejected_without_call(self):
  with r.database(self.ledger) as db:db.execute('UPDATE budget SET cap=8')
  with self.assertRaises(r.Stop):self.collect()
  self.assertEqual(self.budget()[2],530)
 def test_evaluation_requires_real_complete_d0_recordset(self):
  with self.assertRaises(r.Stop):r.Sequence('B1-E0',self.cases,[])
  d=[cell(x,cond,arm)[0] for x in self.cases if x['split']=='development' for cond in i.CONDITIONS for arm in i.ARMS]
  s=r.Sequence('B1-E0',self.cases,d);self.assertEqual(len(s.assignments),288)
  d[0]['execution']='partial'
  with self.assertRaises(r.Stop):r.Sequence('B1-E0',self.cases,d)
 def test_relay_returns_malformed_evidence_then_closes(self):
  relay=r.Relay('B1-D0',self.cases,self.dir/'relay');raw=c.encoded(relay.seq.next()['wire'])
  def malformed(raw):b=json.loads(self.transport(raw));b['choices'][0]['message']['content']='malformed';return c.encoded(b)
  response=relay.send(raw,malformed);self.assertEqual(json.loads(response)['usage']['cost'],.00006);self.assertTrue(relay.stopped)
  with self.assertRaises(r.Stop):relay.send(raw,self.transport)
 def test_admission_funding_and_runtime_fail_closed(self):
  now=dt.datetime.now(dt.timezone.utc);fund={'decision':'approved','stages':['B1-D0','B1-E0'],'packet_sha256':r.FROZEN_PACKET,'maximum_incremental_usd':11.01,'authority_reference':'OFFLINE TEST FIXTURE ONLY','study_cap_usd':20}
  plan='https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/plan.md';tldrs={x:('OFFLINE fixture question treatment comparator metrics and limitations; '+x)*2 for x in i.CONDITIONS}
  obs={'host':'fixture','approved_account_match':True,'exclusive_claim_current':True,'workload_idle':True,'clean_runtime':True,'public_page_verified':True,'route_available':True,'source_commit':'a'*40,'runtime_manifest_sha256':'b'*64,'ledger_identity_sha256':'c'*64,'public_plan':plan,'condition_tldrs':tldrs,'model':i.MODEL,'provider':'OpenAI','input_rate':.1,'output_rate':.5,'historical_hosting_usd':0,'historical_hosting_status':'reconciled','older_lineage_reservations_preserved':True,'all_in_hosting_hourly_usd':.05,'hosting_hours_reserved':6,'hosting_max_usd':.3,'allocation_billing_start':now.isoformat(),'budget':[20,7.961696,530]}
  a={'stage':'B1-D0','funding_sha256':c.digest(fund),'packet_sha256':r.FROZEN_PACKET,'checked_utc':now.isoformat(),'until':(now+dt.timedelta(hours=2)).isoformat(),'host':'fixture','source_commit':'a'*40,'runtime_manifest_sha256':'b'*64,'ledger_identity_sha256':'c'*64,'public_plan':plan,'condition_tldrs':tldrs,'budget_before':{'reserved':7.961696,'calls':530}}
  self.assertTrue(r.admission(a,fund,obs,now)['admitted'])
  for field,value in [('exclusive_claim_current',False),('approved_account_match',False),('historical_hosting_usd',None),('route_available',False),('input_rate',1)]:
   bad=copy.deepcopy(obs);bad[field]=value
   with self.assertRaises(r.Stop):r.admission(a,fund,bad,now)
  bad=copy.deepcopy(fund);bad['decision']='pending'
  with self.assertRaises(r.Stop):r.admission(a,bad,obs,now)
if __name__=='__main__':unittest.main()
