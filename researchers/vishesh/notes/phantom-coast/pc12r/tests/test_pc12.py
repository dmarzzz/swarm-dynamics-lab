import sys,json,copy,unittest,tempfile,hashlib
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from instrument import *
from native import request,decode,RESERVE
from validate_offline import validate_all
from runner import Actor
class Tests(unittest.TestCase):
 def test_breadth(self):self.assertEqual(validate_all()['parameter_combinations'],1728)
 def test_source_copy_invariance(self):
  w=worlds()[0]
  for f in (False,True):self.assertEqual(posterior(main_packet(w,f,1,0,'before')),posterior(main_packet(w,f,3,0,'before')))
 def test_independent_strength(self):
  q=qualification();rs=[dict(assignment=c['id'],status='valid',decision=dict(p=c['gold']['p'],label=c['gold']['label'],inspect=c['gold']['inspections'][0])) for c in q];self.assertTrue(qscore(q,rs)['qualification_passed']);rs[0]['status']='failed';self.assertFalse(qscore(q,rs)['qualification_passed'])
 def test_qualified_does_not_select_on_copies(self):self.assertTrue(all(len({r[0] for r in c['packet']['reports']})==len(c['packet']['reports']) for c in qualification()))
 def test_no_truth_leak(self):
  for w in worlds():
   for f,c in arms(w):
    p=main_packet(w,f,c,0,'before');self.assertEqual(set(p),{'actor','sites','target','reports','direct','previous'});self.assertFalse(any(r[0]==w['target'] for r in p['direct']))
 def test_world_breadth(self):
  ws=worlds();self.assertEqual(len(ws),8);self.assertEqual(len({w['id'] for w in ws}),8)
  for w in ws:self.assertEqual(set(w['truth'].values()),{'LAND','WATER'})
 def test_label_probability_schema(self):
  p=qualification()[0]['packet']
  for q in (-.1,1.1,float('nan'),True):
   with self.assertRaises(ValueError):validate(dict(p=q,label='LAND',inspect='A'),p)
 def test_missing_bounds(self):
  s=analyze(worlds(),[]);self.assertEqual(s['primary_bounds'],[-1,1]);self.assertIsNone(s['primary']);self.assertEqual(s['missing'],640)
 def test_exact_main_and_correction(self):
  rs=[]
  for w in worlds():
   for f,c in arms(w):
    for a in range(10):
     for phase in ('before','after'):
      p=main_packet(w,f,c,a,phase);g=gold(p);rs.append(dict(assignment=f"{w['id']}/{'false' if f else 'true'}/{c}/{a}/{phase}",status='valid',packet=p,decision=dict(p=g['p'],label=g['label'],inspect=g['inspections'][0])))
  s=analyze(worlds(),rs);self.assertEqual(s['primary'],0);self.assertEqual(s['after_correct_labels'],320);self.assertEqual(s['before_mean_regret'],0)
 def test_native_decode(self):
  p=qualification()[0]['packet'];g=gold(p);r=dict(model='openai/gpt-6-sol',provider='OpenAI',usage=dict(cost=.001,prompt_tokens=200,completion_tokens=25),choices=[dict(finish_reason='stop',message=dict(content=canonical(dict(p=g['p'],label=g['label'],inspect=g['inspections'][0]))))]);self.assertEqual(decode(r,p)[1],1000000);r['model']='different'
  with self.assertRaises(ValueError):decode(r,p)
 def test_budget_656(self):
  import ledger
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'prior').write_bytes(b'test')
   with patch.object(ledger,'PREDECESSOR',hashlib.sha256(b'test').hexdigest()):
    l=ledger.Ledger(p/'budget',p/'prior');l.claim()
    for i in range(656):l.reserve(str(i),RESERVE);l.finish(str(i),None)
    with self.assertRaises(ValueError):l.reserve('extra',RESERVE)
    self.assertLess(l.summary()['cumulative_exposure_nano'],4000000000);l.db.close()
 def test_batch_failure_accounts_all_stops_later(self):
  import ledger
  class A:
   def current(self):return True
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'prior').write_bytes(b'test')
   with patch.object(ledger,'PREDECESSOR',hashlib.sha256(b'test').hexdigest()):
    l=ledger.Ledger(p/'budget',p/'prior');l.claim();calls=[]
    def bad(b):calls.append(b);return [{} for _ in b]
    a=Actor(l,bad,p,A());jobs=[(c['id'],c['packet']) for c in qualification()];rs=a.collect(jobs);self.assertEqual(len(calls),1);self.assertEqual(l.summary()['calls'],4);self.assertEqual(sum(r['status']=='unstarted' for r in rs),12);l.db.close()
 def test_public_sections(self):
  s=(Path(__file__).resolve().parents[1]/'PLAN.md').read_text()
  for h in ['TLDR','Question and prediction','Setup','Protocol','Metrics']:self.assertIn('## '+h+'\n',s)
if __name__=='__main__':unittest.main()
