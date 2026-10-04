import copy,json,tempfile,unittest
from pathlib import Path
import fork_runner as r
ACTOR={'case_id':'scripted-unit-fixture','claim':'fixture','claim_date':None,'gold':'DO_NOT_DELIVER','evidence':[{'evidence_id':'e0','document_id':'d','source_host':'example.test','text':'First statement.','gold':'DO_NOT_DELIVER'},{'evidence_id':'e1','document_id':'d','source_host':'example.test','text':'Second statement.'}]}
ANSWER={'verdict':'Supported','confidence':.5,'citations':[{'evidence_id':'e0','quote':'First statement.'}],'justification':'fixture','unresolved':''}
class Admission:
 def __init__(self,ok=True):self.ok=ok;self.calls=0
 def check(self,**kw):self.calls+=1;return {'admitted':self.ok}
class Ledger:
 def __init__(self):self.rows={}
 def reserve(self,rid,amount,stage):
  if rid in self.rows:raise ValueError('duplicate')
  self.rows[rid]={'reserve':amount}
 def settle(self,rid,cost,evidence):self.rows[rid]['actual']=cost
 def uncertain(self,rid):self.rows[rid]['unknown']=True
class Tests(unittest.TestCase):
 def execute(self,transport=None,ok=True,count=lambda p:100):
  self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.out=Path(self.tmp.name)/'out';self.ledger=Ledger();self.admission=Admission(ok);self.payloads=[]
  def default(p):
   self.payloads.append(copy.deepcopy(p));return {'model':r.MODEL,'status':'completed','id':'unit-response','usage':{'cost':.001,'input_tokens':100,'output_tokens':100},'output':[{'type':'message','content':[{'type':'output_text','text':json.dumps(ANSWER)}]}]}
  return r.run_case('UNIT-NOT-NATIVE',ACTOR,self.out,transport or default,self.admission,self.ledger,count)
 def test_complete_forks_and_isolation(self):
  s=self.execute();self.assertEqual((s['assigned'],s['started'],s['valid']),(20,20,20));self.assertEqual(len(self.ledger.rows),20);self.assertEqual(self.admission.calls,20)
  self.assertNotIn('DO_NOT_DELIVER',json.dumps(self.payloads));reqs=[json.loads(x) for x in (self.out/'requests.jsonl').read_text().splitlines()]
  for seat in range(1,7):
   forks=[x for x in reqs if f'/{seat}/' in x['id'] and not x['id'].endswith('/initial')]
   self.assertEqual(forks[0]['parent_sha256'],forks[1]['parent_sha256']);self.assertEqual(forks[0]['request']['input'][:-1],forks[1]['request']['input'][:-1]);self.assertNotEqual(forks[0]['request']['input'][-1],forks[1]['request']['input'][-1])
  self.assertNotEqual(self.payloads[0]['input'][1],self.payloads[1]['input'][1])
 def test_no_approval_no_call(self):
  s=self.execute(ok=False);self.assertEqual(s['started'],0);self.assertEqual(self.ledger.rows,{})
 def test_oversize_no_reservation(self):
  s=self.execute(count=lambda p:4001);self.assertEqual(s['started'],0);self.assertEqual(self.ledger.rows,{})
 def test_transport_uncertainty_stops_no_retry(self):
  def fail(p):raise TimeoutError()
  s=self.execute(fail);self.assertEqual((s['started'],s['valid'],s['unstarted']),(1,0,19));self.assertTrue(next(iter(self.ledger.rows.values()))['unknown'])
 def test_missing_usage_retains_hold(self):
  s=self.execute(lambda p:{'usage':{}});self.assertEqual(s['started'],1);self.assertTrue(next(iter(self.ledger.rows.values()))['unknown'])
 def test_known_cost_missing_tokens_stops_but_settles(self):
  s=self.execute(lambda p:{'usage':{'cost':.001}});self.assertEqual(s['stop_reason'],'token_usage_missing');self.assertEqual(s['started'],1);self.assertEqual(next(iter(self.ledger.rows.values()))['actual'],.001);self.assertNotIn('unknown',next(iter(self.ledger.rows.values())))
 def test_billed_token_overflow_stops(self):
  s=self.execute(lambda p:{'usage':{'cost':.001,'input_tokens':4001,'output_tokens':1}});self.assertEqual(s['stop_reason'],'token_envelope');self.assertEqual(s['valid'],0)
 def test_safe_error_does_not_echo_exception_payload(self):
  self.assertEqual(r.safe_error(ValueError('private-provider-payload')), 'ValueError')
 def test_duplicate_attempt_directory(self):
  self.execute()
  with self.assertRaises(FileExistsError):r.run_case('UNIT-NOT-NATIVE',ACTOR,self.out,lambda p:None,self.admission,self.ledger,lambda p:100)
 def test_quotes_not_semantics(self):
  actor=r.project(ACTOR);self.assertTrue(r.validate(ANSWER,actor));bad=copy.deepcopy(ANSWER);bad['citations'][0]['quote']='Invented.'
  with self.assertRaises(ValueError):r.validate(bad,actor)
 def test_same_document_distinct_claim_retained(self):
  a=copy.deepcopy(ANSWER);b=copy.deepcopy(ANSWER);b['justification']='different claim';b['citations']=[{'evidence_id':'e1','quote':'Second statement.'}]
  board=r.peer_board({1:a,2:b},r.project(ACTOR));self.assertEqual(len(board['groups']),2);self.assertFalse(board['source_independence_verified'])
 def test_request_exact_model_reasoning_no_fallback(self):
  p=r.request(r.initial_input(r.project(ACTOR)));self.assertEqual(p['model'],'openai/gpt-6-sol');self.assertEqual(p['reasoning'],{'effort':'medium'});self.assertFalse(p['provider']['allow_fallbacks']);self.assertEqual(p['max_output_tokens'],2048)
 def test_rerun_fresh_initial_requests(self):
  self.execute();first=copy.deepcopy(self.payloads);s=self.execute();self.assertEqual(len(self.payloads),20);self.assertEqual(first,self.payloads);self.assertEqual(s['valid'],20)
if __name__=='__main__':unittest.main()
