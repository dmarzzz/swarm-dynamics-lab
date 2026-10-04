import copy,json,sys,tempfile,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import MODEL,sha
from ledger import Ledger
from worker import execute
PACKET=Path(__file__).resolve().parents[1]/'a0/packet.json'
class WorkerTests(unittest.TestCase):
 def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.l=Ledger(self.base/'budget.sqlite',2000000000,'owner-default');self.packet=json.loads(PACKET.read_text())
 def tearDown(self):self.l.db.close();self.tmp.cleanup()
 def raw(self,req):
  payload=json.loads(req['messages'][0]['content']);text='Faithful scripted test only.'
  if 'JSON object' in payload['task']:text=json.dumps({'claims':[{'claim':'Fixture','status':'reported','uncertainty':'unknown','source_ids':[]}]})
  return {'role':'assistant','model':MODEL,'stop_reason':'end_turn','content':[{'type':'text','text':text}],'usage':{'input_tokens':500,'output_tokens':40}}
 def test_complete_reconciles_but_does_not_claim_semantic_pass(self):
  s=execute(self.packet,self.base/'out',self.l,lambda r:500,self.raw,time.time()+300)
  self.assertEqual((s['assigned'],s['valid'],s['scored']),(72,72,0));self.assertEqual(s['budget']['model_calls'],72)
 def test_v0_uses_same_cumulative_ledger_and_distinct_stage(self):
  self.l.reserve('prior','A0','model',1000000,'old');self.l.settle('prior',1000000)
  self.packet['stage']='V0';self.packet['scope']='real-source test fixture only'
  s=execute(self.packet,self.base/'v0',self.l,lambda r:500,self.raw,time.time()+300)
  self.assertEqual(s['stage'],'V0');self.assertEqual(s['budget']['model_calls'],73)
 def test_unknown_failure_keeps_reserve_stops_without_retry(self):
  def fail(req):raise TimeoutError('suppressed')
  s=execute(self.packet,self.base/'out',self.l,lambda r:500,fail,time.time()+300)
  self.assertEqual((s['failed'],s['unstarted']),(1,71));self.assertEqual(s['budget']['unresolved_model_calls'],1)
  self.assertEqual(s['budget']['model_upper_nano'],10752000)
 def test_count_refusal_makes_no_paid_call(self):
  def fail(req):self.fail('generation must not run')
  s=execute(self.packet,self.base/'out',self.l,lambda r:8193,fail,time.time()+300)
  self.assertEqual(s['budget']['model_calls'],0)
 def test_no_duplicate_attempt(self):
  (self.base/'out').mkdir()
  with self.assertRaises(ValueError):execute(self.packet,self.base/'out',self.l,lambda r:500,self.raw,time.time()+300)
 def test_ledger_cannot_reset(self):
  with self.assertRaises(ValueError):Ledger(self.base/'budget.sqlite',10000000000,'invented')
 def test_reservations_include_infrastructure(self):
  self.l.reserve('host','A0','infrastructure',1999999999,'ref')
  with self.assertRaises(ValueError):self.l.reserve('call','A0','model',100,'req')
 def test_duplicate_call_and_stage_limit(self):
  self.l.reserve('call','A0','model',100,'req',1)
  with self.assertRaises(Exception):self.l.reserve('call','A0','model',100,'req',1)
  with self.assertRaises(ValueError):self.l.reserve('next','A0','model',100,'req',1)
 def test_invalid_response_is_retained_and_bounded(self):
  def bad(req):return {**self.raw(req),'model':'wrong'}
  s=execute(self.packet,self.base/'out',self.l,lambda r:500,bad,time.time()+300)
  self.assertEqual(s['valid'],0);self.assertEqual(s['budget']['unresolved_model_calls'],1)
if __name__=='__main__':unittest.main()
