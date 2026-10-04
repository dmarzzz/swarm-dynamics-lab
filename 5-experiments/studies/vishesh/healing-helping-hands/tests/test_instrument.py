import json,sys,tempfile,time,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from corpus import *
from sim import *
from providers import Budget,validate_laya
from run import Journal
class Tests(unittest.TestCase):
 def setUp(self):self.c=make(8101);self.tape=[d['label'] for d in self.c['docs']]
 def test_fixture_balance_and_blindness(self):
  self.assertEqual(len(self.c['docs']),200);self.assertEqual(len(self.c['heads']),20);self.assertEqual(len(set(i%20 for i in self.c['heads'])),20)
  self.assertEqual(set(observation(self.c,self.c['docs'][0])),{'claim','report'})
  self.assertEqual(collections.Counter(x['expected'] for x in qualification()),dict.fromkeys(LABELS,20))
 def test_deduplicate_and_no_cross_claim(self):
  d=self.c['docs'];root=d[0]['root'];copy=next(x['id'] for x in d if x['root']==root and x['id']!=0)
  self.assertEqual(ledger({0,copy,1},set(),0,d,self.tape),ledger({0},set(),0,d,self.tape))
 def test_synchronous_one_hop(self):
  mem=[set() for _ in range(N)];mem[0]={0};n=[set() for _ in range(N)]
  after,_=step(mem,n,'evidence-only');self.assertIn(0,after[1]);self.assertNotIn(0,after[2]);self.assertEqual(mem[1],set())
 def test_notice_idempotence(self):
  d=self.c['docs'];r=d[0]['root'];self.assertEqual(ledger({0},{r},0,d,self.tape),{})
  mem=[{i} for i in range(N)];n=[set() for _ in range(N)];n[0]={r};_,first=step(mem,n,'evidence+withdrawals');_,second=step(mem,first,'evidence+withdrawals');self.assertEqual(first[0],second[0])
 def test_exact_recovery_and_stale_citations(self):
  healed=rollout(self.c,self.tape,'evidence+withdrawals','combined');local=rollout(self.c,self.tape,'evidence-only','combined')
  self.assertEqual(healed['metrics']['final_accuracy'],1);self.assertEqual(healed['metrics']['final_stale'],0);self.assertGreater(local['metrics']['final_stale'],0)
 def test_erasure_recoverable(self):
  result=rollout(self.c,self.tape,'evidence-only','erasure');self.assertEqual(result['metrics']['final_accuracy'],1);self.assertEqual(result['metrics']['final_coverage'],1)
 def test_no_event_negative_control(self):
  a=rollout(self.c,self.tape,'evidence-only','none');b=rollout(self.c,self.tape,'evidence+withdrawals','none');self.assertEqual(a,b)
 def test_paired_prefix_and_reproducibility(self):
  a=rollout(self.c,self.tape,'evidence+withdrawals','none');b=rollout(self.c,self.tape,'evidence+withdrawals','withdrawal');self.assertEqual(a['frames'][:10],b['frames'][:10]);self.assertEqual(a,rollout(make(8101),self.tape,'evidence+withdrawals','none'))
 def test_budget_exact_bound(self):
  b=Budget(time.monotonic()+5,{'qwen':1,'laya':0});b.reserve('qwen')
  with self.assertRaises(RuntimeError):b.reserve('qwen')
  self.assertEqual(b.attempts['qwen'],1)
 def test_deadline_before_dispatch(self):
  b=Budget(time.monotonic()-1)
  with self.assertRaises(TimeoutError):b.reserve('qwen')
  self.assertEqual(b.attempts['qwen'],0)
 def test_fault_journal_and_failed_call_count(self):
  for error in (TimeoutError,ValueError):
   class Bad:
    def predict(self,*args):raise error('never print provider text')
   with tempfile.TemporaryDirectory() as tmp:
    b=Budget(time.monotonic()+5);j=Journal(Path(tmp)/'calls.jsonl',b)
    with self.assertRaises(error):j.call(Bad(),'qwen',{'claim':'c','report':'r'},0,{'stage':'fault-test'})
    lines=[json.loads(s) for s in j.path.read_text().splitlines()];self.assertEqual([r['type'] for r in lines],['call_started','call_failed']);self.assertEqual(b.attempts['qwen'],1);self.assertNotIn('never print',j.path.read_text())
 def test_laya_wrong_argmax_rejected(self):
  with self.assertRaises(ValueError):validate_laya({'choice':'SUPPORT','probabilities':{'SUPPORT':.1,'REFUTE':.8,'UNCERTAIN':.1}},LABELS)
 def test_missing_route_tape_label_rejected(self):
  with self.assertRaises(ValueError):rollout(self.c,['bad']*200,'none','none')
if __name__=='__main__':unittest.main()

class TerminalAccountingTests(unittest.TestCase):
 def test_provider_failure_terminates_every_assignment(self):
  from unittest.mock import patch
  import run
  class Broken:
   metadata={'fixture':'offline fault injection'}
   def predict(self,*args):raise TimeoutError('sensitive provider diagnostic must be suppressed')
   def close(self):pass
  with tempfile.TemporaryDirectory() as tmp:
   out=Path(tmp)/'attempt'
   with patch.object(run,'source_check',return_value={}),patch.object(run,'Qwen',Broken),patch.object(run,'Laya',Broken),patch.object(run,'qualify',return_value={'status':'passed'}),patch('builtins.print'):
    m=run.execute(out,{'commit':'offline-fault-test'})
   self.assertEqual(len(m['assignments']),144)
   self.assertEqual(collections.Counter(a['status'] for a in m['assignments']),{'completed':36,'not_run':108})
   self.assertEqual(m['calls'],{'qwen':1,'laya':0})
   self.assertTrue(all((out/(a['id']+'.json')).exists() for a in m['assignments']))
   self.assertNotIn('sensitive provider', (out/'calls.jsonl').read_text())
 def test_unreachable_recovery_is_null(self):
  c=make(8201);r=rollout(c,['SUPPORT']*200,'none','combined')
  self.assertIsNone(r['metrics']['recovery_rounds'])
