"""Zero-key engineering checks for matching, blindness, temporal semantics and failures."""
import copy,io,json,os,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import sim,study,provider,render,analyze
class Checks(unittest.TestCase):
 def setUp(self):self.cfg=study.design()['cfg']
 def test_deterministic_resources(self):
  for n in (1,4,16):
   w=sim.make_world(6900,n,'sleeper',self.cfg);self.assertEqual(w,sim.make_world(6900,n,'sleeper',self.cfg))
   for raw in w['rounds']:
    self.assertEqual(sum(w['roles'][r['node']]=='attacker' for r in raw['reports']),16)
    self.assertEqual(sum(w['roles'][r['node']]!='attacker' for r in raw['reports']),18 if raw['round']<4 else 24)
   for arm in study.design()['arms']:
    ts=sim.simulate(w,arm,self.cfg);self.assertEqual(ts,sim.simulate(w,arm,self.cfg))
    for st in ts:self.assertEqual((len(st['audits']),len({a['node'] for a in st['audits']}),len(st['packet']['reports'])),(4,4,12))
 def test_policy_blindness(self):
  w=sim.make_world(6900,16,'sleeper',self.cfg);ts=sim.simulate(w,'renewal',self.cfg)
  for st in ts:
   self.assertEqual(set(st['packet']),{'skills','round','reports','audit_pass_probability'})
   for r in st['packet']['reports']:self.assertEqual(set(r),{'node','skill','claim','message','join_round','audit_now','history'})
  before=ts[2]['history_after'];raw=w['rounds'][3];a=sim.select_audits(raw['reports'],before,'renewal',4,(6900,16,4));w['truths']={};w['roles']={}
  self.assertEqual(a,sim.select_audits(w['rounds'][3]['reports'],before,'renewal',4,(6900,16,4)))
 def test_controls_and_scarcity(self):
  a=sim.make_world(6900,16,'sleeper',self.cfg);b=sim.make_world(6900,16,'clean',self.cfg);c=sim.make_world(6900,16,'relapse',self.cfg)
  self.assertEqual(a['truths'],b['truths']);self.assertEqual(a['rounds'][:3],b['rounds'][:3]);self.assertEqual([r['round'] for r in c['rounds'] if r['attack_active']],[4,7,8])
  for raw in a['rounds'][3:]:
   rare=[r for r in raw['reports'] if a['roles'][r['node']]!='attacker' and r['skill']>=3]
   self.assertEqual(len(rare),3);self.assertEqual({r['skill'] for r in rare},{3,4,5});self.assertTrue(any(a['roles'][r['node']]=='attacker' and r['join_round']==4 for r in raw['reports']))
 def test_observed_state_updates(self):
  w=sim.make_world(6900,16,'sleeper',self.cfg)
  for arm in study.design()['arms']:
   last={}
   for st in sim.simulate(w,arm,self.cfg):
    self.assertEqual(st['history_before'],last);expected=copy.deepcopy(last)
    for a in st['audits']:
     h=expected.setdefault(a['node'],{'pass':0,'fail':0});h['pass' if a['passed'] else 'fail']+=1
    self.assertEqual(expected,st['history_after']);last=expected
    self.assertFalse({a['message'] for a in st['audits'] if not a['passed']} & {r['message'] for r in st['packet']['reports']})
 def test_assignments_and_competence(self):
  q=study.assignments('Q0');s=study.assignments('S1');z=study.assignments('S0')
  self.assertEqual((len(q),len(s),len(z)),(36,1944,198));self.assertEqual(len({r['id'] for r in s}),1944);self.assertFalse({r['task'] for r in q}&{r['task'] for r in s})
  for r in q:self.assertTrue(study.evaluate(r,study.scripted(r['packet']))['exact_packet'])
  self.assertTrue(all(r['task']<12000 for r in s))
 def test_malformed_billed_once(self):
  with self.assertRaises(ValueError):study.validate({'values':{str(i):True for i in range(6)}})
  b={'usage':{'input_tokens':100,'output_tokens':10},'model':study.design()['model'],'stop_reason':'end_turn','content':[{'type':'text','text':'{}'}]}
  with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'SWARM_MODEL_API_KEY':'test-only','SWARM_MODEL_WORKSPACE_ID':'test-only'}):
   ledger=provider.Ledger(Path(td)/'ledger.jsonl');client=provider.Anthropic(ledger,opener=lambda *a,**k:io.BytesIO(json.dumps(b).encode()))
   with self.assertRaises(provider.CallFailure) as err:client.call(study.qualification_assignments()[0]['packet'],'once')
   self.assertEqual(err.exception.category,'invalid_structured_answer');self.assertTrue(err.exception.accounting['attempted']);self.assertEqual(ledger.transact()['usage_reported_calls'],1)
   with self.assertRaises(provider.CallFailure) as err:client.call(study.qualification_assignments()[0]['packet'],'once')
   self.assertEqual(err.exception.category,'duplicate_call_refused');self.assertEqual(ledger.transact()['attempted_calls'],1)
 def test_analysis_identity_interaction_and_missing(self):
  rows=[]
  for n,arm,value in ((1,'renewal',.5),(1,'reputation',.5),(16,'renewal',1),(16,'reputation',.25)):
   ev={m:value for m in analyze.METRICS}
   rows.append(dict(id=f'{n}-{arm}',task=7100,identities=n,strategy='sleeper',arm=arm,round=8,kind='pilot',status='completed',evaluation=ev,scripted_evaluation=ev))
  result=analyze.analyze(rows)
  self.assertEqual(result['primary']['mean'],.75)
  interaction=next(x for x in result['identity_interactions'] if x['strategy']=='sleeper' and x['round']==8 and x['metric']=='rare_accuracy')
  self.assertEqual(interaction['mean'],.75)
  with self.assertRaises(ValueError):analyze.analyze(rows+[rows[0]])
  rows[0]['status']='failed';result=analyze.analyze(rows)
  c=next(x for x in result['cells'] if x['identities']==1 and x['arm']=='renewal')
  self.assertEqual(c['assigned_accuracy_bounds'],[0,1]);self.assertEqual(c['valid'],0)
 def test_render_transition_failure(self):
  w=sim.make_world(6900,16,'sleeper',self.cfg);hs=[]
  for arm in study.design()['arms']:hs += [dict(task=6900,identities=16,strategy='sleeper',arm=arm,**s) for s in sim.simulate(w,arm,self.cfg)]
  self.assertEqual(render.frame([{'status':'failed','kind':'pilot'}],1,'S0',history=hs,round_cursor=4).size,(1800,1200))
  self.assertNotEqual(render.frame([],1,'S0',history=hs,round_cursor=3).tobytes(),render.frame([],1,'S0',history=hs,round_cursor=4).tobytes())
 def test_opus_request_contract(self):
  d=study.design();b=provider.request_body(d,{'x':1})
  for k in ('temperature','top_p','top_k','thinking','tool_choice','fallbacks'):self.assertNotIn(k,b)
  self.assertEqual(b['model'],'claude-opus-5-5');self.assertEqual(b['output_config']['effort'],'low');self.assertIn('format',b['output_config'])
  self.assertEqual(b['messages'][-1]['role'],'user')
 def test_opus_response_handling(self):
  good='{"values":{"0":1,"1":null,"2":3,"3":null,"4":null,"5":null}}'
  base={'usage':{'input_tokens':100,'output_tokens':10},'model':study.design()['model']}
  cases=[({'stop_reason':'end_turn','content':[{'type':'thinking','thinking':''},{'type':'text','text':good}]},None),
         ({'stop_reason':'refusal','content':[]},'refusal'),
         ({'stop_reason':'max_tokens','content':[{'type':'thinking','thinking':''}]},'output_cap'),
         ({'stop_reason':'end_turn','content':[{'type':'thinking','thinking':''}]},'invalid_structured_answer'),
         ({'stop_reason':'end_turn','content':[{'type':'text','text':good},{'type':'text','text':good}]},'invalid_structured_answer')]
  for i,(resp,want) in enumerate(cases):
   with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'SWARM_MODEL_API_KEY':'test-only','SWARM_MODEL_WORKSPACE_ID':'test-only'}):
    body=dict(base,**resp);client=provider.Anthropic(provider.Ledger(Path(td)/'l.jsonl'),opener=lambda *a,**k:io.BytesIO(json.dumps(body).encode()))
    if want is None:
     ans,acct=client.call({'skills':[0]},f'c{i}');self.assertEqual(ans['values']['0'],1)
    else:
     with self.assertRaises(provider.CallFailure) as err:client.call({'skills':[0]},f'c{i}')
     self.assertEqual(err.exception.category,want)
if __name__=='__main__':unittest.main(verbosity=2)
