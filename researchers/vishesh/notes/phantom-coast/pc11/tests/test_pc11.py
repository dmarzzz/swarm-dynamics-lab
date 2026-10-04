import copy,json,sys,unittest,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from contract import ACTORS,canonical,digest,validate_decision
from cases import cases,grade,summarize
from engine import run,audit,StopDispatch
from runner import world,arms
from policies import exact,posterior,action_risk
from reference import enumerate_action
from analysis import contrast
from native import request,decode,RESERVE
class Tests(unittest.TestCase):
 def test_reference(self):
  for c in cases():
   p=c['packet'];self.assertEqual(grade(c,exact(p))['map_correct'],4)
   if p['remaining_inspections']:
    probs=posterior(p);qs=tuple(probs[s] for s in p['tie_order']);h=p['remaining_inspections']
    vs=[enumerate_action(qs,h,i) for i in range(4)]
    for i,v in enumerate(vs):self.assertAlmostEqual(v,action_risk(qs,h,i))
    self.assertEqual(c['accepted_inspections'],[s for s,v in zip(p['tie_order'],vs) if abs(v-min(vs))<1e-12])
 def test_gate_missing(self):
  rs=[dict(id=c['id'],status='valid',grade=grade(c,exact(c['packet']))) for c in cases()]
  self.assertTrue(summarize(rs)['qualification_passed']);rs[0]['status']='failed';self.assertFalse(summarize(rs)['qualification_passed'])
 def test_gate_private_miss(self):
  rs=[]
  for c in cases():
   d=exact(c['packet'])
   if c['kind']=='private-positive':d['inspect']=c['packet']['private_reports'][0]['site']
   rs.append(dict(id=c['id'],status='valid',grade=grade(c,d)))
  self.assertFalse(summarize(rs)['qualification_passed'])
 def test_reserved(self):
  with self.assertRaises(ValueError):cases('Q0')
 def test_barrier_and_ten(self):
  w=world();seen=[]
  def actor(p):
   self.assertEqual(len(p['peer_slots']),9)
   self.assertFalse({'truth','target','poison','condition'}&set(p))
   self.assertTrue(all(x['time']==p['time']-1 for x in p['peer_slots']))
   seen.append(p);return exact(p)
  e=run(w,False,True,actor);self.assertEqual(len(seen),30);self.assertEqual(e['summary']['assigned'],30);self.assertTrue(audit(e)['verified'])
 def test_missing_denominator(self):
  e=run(world(),True,False,lambda p:None)
  self.assertEqual(e['summary']['timeline'][-1]['mean_loss_bounds'],[0,1])
  self.assertEqual(e['summary']['timeline'][-1]['target_wrong_bounds'],[0,1]);self.assertEqual(e['summary']['failed_slots'],2)
 def test_quorum(self):
  w=world();e=run(w,False,False,lambda p:exact(p) if p['agent'] in ACTORS[:5] else None)
  self.assertEqual(e['summary']['failed_slots'],2)
  e=run(w,False,False,lambda p:exact(p) if p['agent'] in ACTORS[:6] else None);self.assertEqual(e['summary']['failed_slots'],0)
 def test_fatal_propagates(self):
  def bad(p):raise StopDispatch('stop')
  with self.assertRaises(StopDispatch):run(world(),False,False,bad)
 def test_native_replay(self):
  e=run(world(),True,True,exact,'mock',native=True);self.assertTrue(audit(e)['verified']);e['turns'][0]['selected']='bad'
  with self.assertRaises(ValueError):audit(e)
 def test_pairing(self):
  es=[run(world(),p,s,exact) for p,s in arms()];self.assertEqual(contrast(es)['collective_interaction_bounds'],[0,0]);es[0]['world']['id']='bad'
  with self.assertRaises(ValueError):contrast(es)
 def test_request_bound_and_route(self):
  for e in [run(world(),p,s,exact) for p,s in arms()]:
   for t in e['turns']:
    for a in t['entries']:
     b=request(a['packet']);self.assertLessEqual(len(canonical(b).encode()),6400);self.assertFalse(b['provider']['allow_fallbacks']);self.assertEqual(b['model'],'openai/gpt-6-sol')
 def test_response_identity_cost(self):
  p=cases()[0]['packet'];r=dict(model='openai/gpt-6-sol',provider='OpenAI',usage=dict(prompt_tokens=1000,completion_tokens=100,cost=.003),choices=[dict(finish_reason='stop',message=dict(content=canonical(exact(p))))])
  d,c,s=decode(r,p);self.assertEqual(c,3000000)
  for key,v in [('provider','Other'),('model','openai/gpt-6-luna')]:
   q=copy.deepcopy(r);q[key]=v
   with self.assertRaises(ValueError):decode(q,p)
  q=copy.deepcopy(r);q['usage']['cost']=1
  with self.assertRaises(ValueError):decode(q,p)
 def test_public_sections(self):
  text=(Path(__file__).resolve().parents[1]/'PLAN.md').read_text()
  for h in ('TLDR','Question and prediction','Setup','Protocol','Metrics'):self.assertIn('## '+h+'\n',text)
 def test_budget_limits(self):
  import ledger,unittest.mock,hashlib
  with tempfile.TemporaryDirectory() as td:
   p=Path(td);(p/'prior').write_bytes(b'test')
   with unittest.mock.patch.object(ledger,'PREDECESSOR',hashlib.sha256(b'test').hexdigest()):
    l=ledger.Ledger(p/'ledger',p/'prior');l.claim()
    for i in range(128):l.reserve(str(i),RESERVE);l.finish(str(i),None)
    with self.assertRaises(ValueError):l.reserve('129',RESERVE)
    self.assertLess(l.summary()['cumulative_exposure_nano'],4000000000)
    with self.assertRaises(Exception):l.claim()
    l.db.close()
if __name__=='__main__':unittest.main()
