"""Offline invariant checks; no credentials, network or provider SDK required."""
import copy,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from PIL import Image
import sim,render,worker
D=worker.load(); CFG=D['cfg']
def world(**kw): return sim.make_world(100,kw.get('bridges',1),kw.get('attacker_pass',.1),kw.get('clean',False),CFG)
class Qualification(unittest.TestCase):
 def test_determinism(self):
  self.assertEqual(world(),world()); self.assertEqual(sim.run_episode(world(),4,sim.ARMS,CFG),sim.run_episode(world(),4,sim.ARMS,CFG))
 def test_degree_preserved(self):
  a=world(bridges=1); b=world(bridges=3)
  self.assertEqual({x:len(v) for x,v in a['public']['adj'].items()},{x:len(v) for x,v in b['public']['adj'].items()})
  self.assertNotEqual(a['public']['adj'],b['public']['adj'])
 def test_matching_profiles(self):
  w=world(); n=w['public']['nodes']; g=w['groups']
  def profile(group): return sorted((len(w['public']['adj'][x]),n[x]['age'],n[x]['activity'],n[x]['skill']) for x in g if g[x]==group)
  self.assertEqual(profile(1),profile(2))
 def test_observation_boundary(self):
  w=world(); p=w['public']; self.assertEqual(set(p),{'nodes','adj','trusted'})
  self.assertTrue(all(set(n)=={'skill','claim','age','activity'} for n in p['nodes'].values()))
  other=copy.deepcopy(w); other['truth']={x:None for x in other['truth']}
  for arm in sim.ARMS[1:]: self.assertEqual(sim.select_check(p,arm,set(),set(),[],100,1),sim.select_check(other['public'],arm,set(),set(),[],100,1))
  packet=sim.public_packet(w,sim.run_episode(w,4,sim.ARMS,CFG)[-1]); self.assertEqual(set(packet),{'reports','skills'})
  self.assertTrue(all(set(n)=={'node','skill','claim','age','activity','check_passed'} for n in packet['reports']))
 def test_zero_budget(self):
  r=sim.run_episode(world(),0,sim.ARMS,CFG)
  self.assertTrue(all(x['evaluation']==r[0]['evaluation'] and x['trace'][0]['admitted']==r[0]['trace'][0]['admitted'] for x in r))
 def test_unique_checks_and_seats(self):
  for r in sim.run_episode(world(),8,sim.ARMS,CFG):
   ev=[s['event'] for s in r['trace'] if s['event']]
   self.assertEqual(len(ev),0 if r['arm']=='no_verification' else 8); self.assertEqual(len(ev),len({e['node'] for e in ev}))
   self.assertTrue(all(s['metrics']['admitted_count']==18 for s in r['trace']))
 def test_clean_ceiling(self):
  w=world(clean=True); ids=list(w['public']['nodes']); m=sim.evaluate(w,ids,sim.decide(w['public'],ids),[])
  self.assertEqual(m['task_accuracy'],1); self.assertIsNone(m['malicious_admission'])
 def test_tie_abstains(self):
  self.assertIsNone(sim.decide({'nodes':{'a':{'skill':0,'claim':1},'b':{'skill':0,'claim':2}}},['a','b'])['0'])
 def test_no_check_stable(self):
  r=sim.run_episode(world(),4,sim.ARMS,CFG)[0]; self.assertTrue(all(s['metrics']==r['trace'][0]['metrics'] for s in r['trace']))
 def test_failed_checks_remove_nodes(self):
  w=world(); w['checks']={x:False for x in w['checks']}; r=sim.run_episode(w,4,['coverage'],CFG)[0]
  self.assertEqual(len(r['trace'][-1]['failed']),4)
  self.assertTrue(all(not(set(s['failed']) & set(s['admitted'])) for s in r['trace']))
 def test_uninformative_verifier(self):
  a=world(attacker_pass=.9); b=world(attacker_pass=.9,clean=True); self.assertEqual(a['checks'],b['checks'])
  for x,y in zip(sim.run_episode(a,4,sim.ARMS,CFG),sim.run_episode(b,4,sim.ARMS,CFG)):
   self.assertEqual([s['admitted'] for s in x['trace']],[s['admitted'] for s in y['trace']])
 def test_render_history(self):
  w=world(); r=sim.run_episode(w,4,sim.ARMS,CFG); before=json.dumps(r,sort_keys=True)
  with tempfile.TemporaryDirectory() as path:
   self.assertEqual(render.replay(w,r,path,'test'),5)
   with Image.open(Path(path)/'replay.gif') as im: self.assertEqual(im.n_frames,5); self.assertEqual(im.size,(1800,1180))
   with Image.open(Path(path)/'final_frame.png') as im: self.assertEqual(im.size,(1800,1180))
  self.assertEqual(json.dumps(r,sort_keys=True),before)
 def test_failures_retained_no_network(self):
  p=worker.params('S0')[0]; p['tasks']=[100]
  with tempfile.TemporaryDirectory() as path,patch('urllib.request.urlopen',side_effect=AssertionError('Network forbidden')),patch('sim.run_episode',side_effect=ValueError('injected')):
   out=Path(path)/'fault'
   with self.assertRaises(RuntimeError): worker.execute(p,out)
   s=json.loads((out/'summary.json').read_text()); self.assertEqual(s['invalid'],4); self.assertEqual(s['graded'],0); self.assertEqual(s['model_calls'],0)
   self.assertEqual(len((out/'episodes.jsonl').read_text().splitlines()),4)
 def test_holdout_blocked(self):
  with self.assertRaises(ValueError): worker.params('S2')
  self.assertFalse(set(D['stages']['S0']['tasks'])&set(D['stages']['S1']['tasks']))
 def test_hub_stops_after_failed_cell(self):
  from unittest.mock import MagicMock
  sr=MagicMock(); run=MagicMock(); run.id='sybil-specialists/fault'; run.attempt=1
  run.__exit__.return_value=False; sr.next_run.return_value=run
  with patch('worker.execute',side_effect=RuntimeError('injected cell failure')):
   with self.assertRaises(RuntimeError): worker.run_hub(sr)
  sr.next_run.assert_called_once_with('sybil-specialists')
  self.assertIs(run.__exit__.call_args.args[0],RuntimeError)
if __name__=='__main__': unittest.main(verbosity=2)
