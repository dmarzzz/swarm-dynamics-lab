import unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent));sys.path.insert(0,str(Path(__file__).parent.parent/'src'))
from engine import *
from corpus import make
class Checks(unittest.TestCase):
 def setUp(self):
  self.r={'d0':{'kind':'document','claim':0,'root':'a','publisher':'p','label':'SUPPORT'},'d1':{'kind':'document','claim':0,'root':'a','publisher':'p','label':'SUPPORT'},'n':{'kind':'notice','claim':0,'root':'a','issuer':'p','authenticated':True}}
 def test_dedup(self):self.assertEqual(len(query({'d0','d1'},self.r,0,'append')['kept']),1)
 def test_conflicting_copies_abstain(self):
  self.r['d1']['label']='REFUTE';self.assertEqual(query({'d0','d1'},self.r,0,'append')['answer'],'UNCERTAIN')
 def test_authenticated_withdrawal(self):self.assertTrue(query({'d0','n'},self.r,0,'verified')['missing'])
 def test_forged_is_rejected(self):
  self.r['n']['issuer']='wrong';self.assertFalse(query({'d0','n'},self.r,0,'verified')['missing']);self.assertTrue(query({'d0','n'},self.r,0,'blind')['missing'])
 def test_unauthenticated_is_rejected(self):
  self.r['n']['authenticated']=False;self.assertFalse(query({'d0','n'},self.r,0,'verified')['missing'])
 def test_missing_lineage(self):
  self.r['n']['root']=None;self.assertFalse(query({'d0','n'},self.r,0,'verified')['missing'])
 def test_pending_notice(self):
  self.assertFalse(query({'n'},self.r,0,'verified')['deleted']);self.assertEqual(query({'n','d0'},self.r,0,'verified')['deleted'],{'a'})
 def test_append_never_deletes(self):self.assertFalse(query({'n','d0'},self.r,0,'append')['deleted'])
 def test_claim_isolation(self):self.assertTrue(query({'d0'},self.r,1,'append')['missing'])
 def test_missing_not_correct_unknown(self):
  f=evaluate([set() for _ in range(200)],{}, {'roots':{}},set(),'append',0,0,set());self.assertEqual(f['incorrect_or_missing'],1);self.assertEqual(f['local_accuracy'],1)
 def test_sync_and_budget(self):
  m=[set() for _ in range(200)];m[0]={'d0'};out,t,mx=peer_step(m,self.r);self.assertIn('d0',out[1]);self.assertNotIn('d0',out[2]);self.assertEqual(mx,1)
  records={f'd{i}':{'kind':'document'} for i in range(10)};m[0]=set(records);out,t,mx=peer_step(m,records);self.assertEqual(len(out[1]),4);self.assertEqual(mx,4)
  out,t,mx=peer_step(m,records,cap=16);self.assertEqual(len(out[1]),10);self.assertEqual(mx,10)
 def test_central_outage_and_queue(self):
  own=[set() for _ in range(200)];cache=[set() for _ in range(200)];own[0]={'d0'}
  cache,b,t=central_step(cache,own,set(),self.r,{0});self.assertFalse(b)
  cache,b,t=central_step(cache,own,b,self.r,set());self.assertEqual(b,{'d0'});self.assertEqual(cache[20],{'d0'})
 def test_cache_preserved(self):
  own=[set() for _ in range(200)];cache=[set() for _ in range(200)];cache[0]={'d0'}
  out,b,t=central_step(cache,own,set(),self.r,{0});self.assertEqual(out[0],{'d0'})
 def test_actor_schema_no_gold(self):
  c=make(3);e,t=build(c,[d['label'] for d in c['docs']],17,'combined');self.assertEqual(sum(map(len,e['initial'])),160);self.assertEqual(sum(map(len,e['added'])),40)
  self.assertEqual(len(t['withdrawn']),20);self.assertTrue(all('text' not in r and 'expected' not in r for r in e['records'].values()))
 def test_event_targets_and_pairing(self):
  c=make(3);tape=[d['label'] for d in c['docs']];a,x=build(c,tape,17,'withdrawal');b,y=build(c,tape,17,'combined');self.assertEqual(a['placement'],b['placement']);self.assertEqual(x['withdrawn'],y['withdrawn'])
 def test_invalid_tape_and_condition(self):
  with self.assertRaises(ValueError):build(make(3),[],17,'benign')
  with self.assertRaises(ValueError):rollout({},[],1,'unlisted','benign')
if __name__=='__main__':unittest.main()

class RunnerChecks(unittest.TestCase):
 def test_failure_denominator_and_no_overwrite(self):
  import tempfile,json
  from unittest.mock import patch
  import execute
  c=make(3);loaded={f'corpus-{s}.json':c for s in (8701,8702,8703)}
  loaded.update({f'tapes-{s}.json':{'jev':[d['label'] for d in c['docs']]} for s in (8701,8702,8703)})
  with tempfile.TemporaryDirectory() as d,patch.object(execute,'check',return_value={'url':'https://example/practical/PLAN.md','commit':'x'}),patch.object(execute,'source_check',return_value={}),patch.object(execute,'inputs',return_value=(loaded,{})),patch.object(execute,'rollout',side_effect=RuntimeError('fault')):
   out=Path(d)/'attempt';m=execute.run(out,Path(d),'unit fixture');self.assertEqual(m['terminal_counts'],{'failed':1,'not_run':179});self.assertEqual(len(list(out.glob('*-peer-verified.json'))),36)
   with self.assertRaises(FileExistsError):execute.run(out,Path(d),'unit fixture')
 def test_input_tamper_fails(self):
  import tempfile,execute
  from unittest.mock import patch
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(FileNotFoundError):execute.inputs(Path(d))

class ReportingChecks(unittest.TestCase):
 def test_no_host_keyword_and_acknowledgement(self):
  import tempfile
  from reporting import Reporter
  class SDK:
   def report(self,kind,experiment,run,*,source,role,strict,metrics=None):return True
  with tempfile.TemporaryDirectory() as d:
   r=Reporter(SDK(),'e','r',Path(d)/'events');self.assertTrue(r.emit('metric',metrics={'completed':1}))
   with self.assertRaises(ValueError):r.emit('metric',host='x')
 def test_unacknowledged_fails_closed(self):
  import tempfile
  from reporting import Reporter,ReportingFailure
  class SDK:
   def report(self,*a,**k):return False
  with tempfile.TemporaryDirectory() as d:
   with self.assertRaises(ReportingFailure):Reporter(SDK(),'e','r',Path(d)/'events').emit('start')
 def test_raw_error_not_recorded(self):
  import tempfile
  from reporting import Reporter,ReportingFailure
  class SDK:
   def report(self,*a,**k):raise RuntimeError('sensitive-diagnostic-placeholder')
  with tempfile.TemporaryDirectory() as d:
   p=Path(d)/'events'
   with self.assertRaises(ReportingFailure):Reporter(SDK(),'e','r',p).emit('start')
   self.assertNotIn('sensitive-diagnostic-placeholder',p.read_text());self.assertIn('RuntimeError',p.read_text())
