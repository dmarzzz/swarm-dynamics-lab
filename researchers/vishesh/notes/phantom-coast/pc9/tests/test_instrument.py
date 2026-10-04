import copy,itertools,json,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import ACTORS,packet,digest,request,decode_answers,validate_decision
from engine import run,audit
from policies import evidence,exact,posterior,risk,exhaustive_risk
from analysis import contrast,summarize
from fixtures import WORLD,copy_peer_fault,make_replay

class Instrument(unittest.TestCase):
 def setUp(self):self.w=copy.deepcopy(WORLD)
 def p(self):return packet(self.w,False,False,'agent-2',0,[],[])
 def test_treatment_is_only_report_value(self):
  for a in ACTORS:
   clean=packet(self.w,False,True,a,0,[],[]);bad=packet(self.w,True,True,a,0,[],[])
   if a==self.w['seed_actor']:
    self.assertNotEqual(clean,bad);bad['private_reports'][0]['label']=clean['private_reports'][0]['label']
   self.assertEqual(clean,bad)
 def test_hidden_truth_and_target_do_not_leak_to_unexposed(self):
  before=packet(self.w,True,False,'agent-0',0,[],[])
  for site in self.w['truth']:self.w['truth'][site]='LAND'
  self.w['target']='Spur'
  self.assertEqual(before,packet(self.w,True,False,'agent-0',0,[],[]))
 def test_round_barrier_and_receipt_time(self):
  seen=[]
  def spy(p):
   seen.append(copy.deepcopy(p));return evidence(p)
  run(self.w,False,True,spy)
  for p in seen:
   self.assertTrue(all(m['time']<p['time'] for m in p['peer_slots']))
   self.assertTrue(all(r['time']<=p['time'] for r in p['observations']))
   self.assertEqual(len(p['observations']),p['time'])
   self.assertEqual(len(p['peer_slots']),4)
 def test_peer_mask_only_removes_interpretations(self):
  off=run(self.w,True,False,evidence);on=run(self.w,True,True,evidence)
  for ta,tb in zip(off['turns'],on['turns']):
   for a,b in zip(ta['entries'],tb['entries']):
    pa=copy.deepcopy(a['packet']);pb=copy.deepcopy(b['packet']);pa.pop('peer_slots');pb.pop('peer_slots');self.assertEqual(pa,pb)
 def test_actor_mutation_cannot_change_engine_or_others(self):
  def malicious(p):
   answer=evidence(p);p['sites'].clear();p['observations'].append({'bad':True});p['peer_slots'].clear();return answer
  x=run(self.w,False,True,malicious);y=run(self.w,False,True,evidence)
  self.assertEqual(x,y);self.assertEqual(self.w,WORLD)
 def test_private_reports_only_seed(self):
  e=run(self.w,True,True,evidence)
  for t in e['turns']:
   for a in t['entries']:self.assertEqual(bool(a['packet']['private_reports']),a['agent']==self.w['seed_actor'])
 def test_no_current_round_peer_leak_via_callback(self):
  def actor(p):
   self.assertFalse(any(m.get('id')==f"t{p['time']}/agent-0" for m in p['peer_slots']));return evidence(p)
  e=run(self.w,False,True,actor);self.assertEqual(e['summary']['valid'],15)
 def test_evidence_unknown_and_corrected(self):
  p=self.p();self.assertEqual(evidence(p)['map']['Moor'],'UNKNOWN')
  p['private_reports'][0]['label']='WATER';p['observations']=[dict(site='Moor',label='LAND')]
  self.assertEqual(exact(p)['map']['Moor'],'LAND');self.assertEqual(evidence(p)['map']['Moor'],'LAND')
 def test_no_duplicate_source_strengthening(self):
  p=self.p();base=posterior(p);p['private_reports']*=4;self.assertEqual(posterior(p),base)
 def test_contradictory_direct_data_fails_closed(self):
  p=self.p();p['observations']=[dict(site='Moor',label=v) for v in ('LAND','WATER')]
  with self.assertRaises(ValueError):posterior(p)
 def test_exact_reference_matches_independent_world_tree(self):
  for q in [(.5,.5,.5,.5),(.8,.5,.5,.5),(.2,0.,1.,.5),(.8,.2,1.,0.)]:
   for h in range(3):self.assertAlmostEqual(risk(q,h),exhaustive_risk(q,h),places=12)
  self.assertAlmostEqual(risk((.8,.5,.5,.5),0),.95)
  self.assertAlmostEqual(risk((.8,.5,.5,.5),2),.45)
 def test_unique_useful_inspection(self):
  p=self.p();p['remaining_inspections']=1;p['observations']=[dict(site=s,label='WATER') for s in p['sites'] if s!='Moor']
  self.assertEqual(exact(p)['inspect'],'Moor')
 def test_repeat_inspection_consumes_capacity(self):
  def repeat(p):
   r=evidence(p)
   if p['remaining_inspections']:r['inspect']='Kite'
   return r
  e=run(self.w,True,True,repeat);self.assertEqual(e['summary']['repeat_slots'],1);self.assertEqual(e['summary']['unique_coverage'],1)
 def test_failed_vote_slot_no_oracle_rescue(self):
  def fails(p):return evidence(p) if p['agent'] in ACTORS[:2] else None
  e=run(self.w,False,True,fails);self.assertEqual(e['summary']['failed_slots'],2);self.assertEqual(e['summary']['unique_coverage'],0);self.assertEqual(e['summary']['valid'],6)
 def test_errors_and_missing_are_distinct(self):
  def fail(p):
   if p['agent']==ACTORS[0]:return None
   if p['agent']==ACTORS[1]:return {'bad':'ignored'}
   if p['agent']==ACTORS[2]:raise RuntimeError('must not log arbitrary exception detail')
   return evidence(p)
  e=run(self.w,False,True,fail);s=e['summary']['timeline'][-1]['unexposed_target'];self.assertEqual(s['missing'],1);self.assertEqual(s['invalid'],1);self.assertEqual(s['unknown'],2);self.assertEqual(e['summary']['failed_slots'],2);self.assertNotIn('must not log',json.dumps(e));self.assertTrue(audit(e)['verified'])
 def test_strict_output_and_wire_roundtrip(self):
  p=self.p();a=evidence(p);q=request(p)['questions'];answers={k:dict(type='choice',choice=a['inspect'] if k=='inspect' else a['map'][k[4:]]) for k in q}
  self.assertEqual(a,decode_answers(answers,p))
  for bad in [dict(a,extra=1),dict(map={},inspect='Kite'),dict(map=a['map'],inspect='outside')]:
   with self.assertRaises(ValueError):validate_decision(bad,p)
 def test_total_budget_and_question_count(self):
  e=run(self.w,False,True,evidence);self.assertEqual(sum(len(request(x['packet'])['questions']) for t in e['turns'] for x in t['entries']),70)
  self.assertEqual(8*4*70+8*5,2280);self.assertAlmostEqual(2280*.001344+.858328842,3.922648842)
 def test_final_action_is_forbidden(self):
  e=run(self.w,False,True,evidence);p=e['turns'][-1]['entries'][0]['packet'];self.assertEqual(p['remaining_inspections'],0)
  with self.assertRaises(ValueError):validate_decision(dict(map=evidence(p)['map'],inspect='Kite'),p)
 def test_replay_detects_tampering_even_if_rehashed(self):
  e=run(self.w,True,True,exact);self.assertTrue(audit(e)['verified']);e['turns'][0]['entries'][0]['packet']['observations'].append(dict(id='future',site='Moor',label='LAND',time=2));e['sha256']=digest({k:v for k,v in e.items() if k!='sha256'})
  with self.assertRaises(ValueError):audit(e)
 def test_missing_bounds_and_denominators(self):
  e=run(self.w,True,False,lambda p:None)
  s=e['summary']['timeline'][-1];self.assertEqual(s['target_wrong_bounds'],[0,1]);self.assertEqual(s['mean_loss_bounds'],[0,1]);self.assertEqual(sum(s['unexposed_target'].values()),4);self.assertEqual(sum(s['all_locations'].values()),20)
 def test_zero_wrong_is_not_zero_uncertainty(self):
  e=run(self.w,True,False,evidence);s=e['summary']['timeline'][0];self.assertEqual(s['target_wrong_bounds'],[0,0]);self.assertEqual(s['unexposed_target']['unknown'],4);self.assertEqual(s['mean_loss_bounds'],[.25,.25])
 def test_controlled_fault_spreads_and_is_correctable(self):
  data=make_replay();c=data['contrast'];self.assertEqual(c['collective_interaction_bounds'],[1,1])
  arms={(e['condition']['poison'],e['condition']['peers']):e for e in data['episodes']}
  self.assertIsNone(arms[(True,True)]['summary']['first_target_inspection'])
  self.assertEqual(arms[(False,True)]['summary']['first_target_inspection'],2)
  for e in data['episodes']:
   for t in e['summary']['timeline']:
    if t['after_target_receipt']['denominator']:self.assertEqual(t['after_target_receipt']['wrong'],0)
 def test_null_reference_not_forced_to_poison(self):
  es=[run(self.w,p,s,evidence) for p in (False,True) for s in (False,True)]
  self.assertEqual(contrast(es)['collective_interaction_bounds'],[0,0])
 def test_renaming_preserves_policy_and_metric(self):
  names=dict(zip(self.w['truth'],['q9','c2','n7','h4']));changed=copy.deepcopy(self.w);changed['truth']={names[s]:v for s,v in self.w['truth'].items()};changed['target']=names[changed['target']];changed['tie_order']=[names[s] for s in changed['tie_order']]
  a=run(self.w,True,True,exact);b=run(changed,True,True,exact)
  self.assertEqual(a['summary']['timeline'][-1]['mean_loss_bounds'],b['summary']['timeline'][-1]['mean_loss_bounds']);self.assertEqual([names[t['selected']] if t['selected'] else None for t in a['turns']],[t['selected'] for t in b['turns']])
 def test_world_site_order_irrelevant_with_fixed_ties(self):
  w=copy.deepcopy(self.w);w['truth']=dict(reversed(list(w['truth'].items())))
  a=run(self.w,False,True,exact);b=run(w,False,True,exact)
  self.assertEqual(a['summary'],b['summary'])
 def test_incomplete_or_crossworld_contrast_rejected(self):
  es=make_replay()['episodes']
  with self.assertRaises(ValueError):contrast(es[:3])
  es[0]['world']['id']='another'
  with self.assertRaises(ValueError):contrast(es)

 def test_mirrored_land_water_reference_has_same_loss(self):
  mirror=copy.deepcopy(self.w);mirror['truth']={s:('WATER' if v=='LAND' else 'LAND') for s,v in self.w['truth'].items()}
  for poisoned in (False,True):
   a=run(self.w,poisoned,True,exact);b=run(mirror,poisoned,True,exact)
   self.assertEqual(a['summary']['timeline'][-1]['mean_loss_bounds'],b['summary']['timeline'][-1]['mean_loss_bounds'])
 def test_majority_and_tie_are_not_selected_by_truth(self):
  def tied(p):
   d=evidence(p)
   if p['remaining_inspections']:d['inspect']='Spur' if p['agent'] in ACTORS[:2] else 'Reef' if p['agent'] in ACTORS[2:4] else 'Kite'
   return d
  e=run(self.w,False,False,tied);self.assertEqual(e['turns'][0]['selected'],'Reef')
 def test_correction_metrics_use_visible_time_not_future(self):
  e=run(self.w,False,True,evidence)
  self.assertEqual(e['summary']['timeline'][1]['after_target_receipt']['denominator'],0)
  self.assertEqual(e['summary']['timeline'][2]['after_target_receipt']['denominator'],4)
 def test_pooled_reference_uses_reports_not_world(self):
  from policies import pooled_endpoint
  e=run(self.w,True,False,copy_peer_fault);p=pooled_endpoint(e)
  e['world']['truth']={s:'WATER' for s in e['world']['truth']}
  self.assertEqual(pooled_endpoint(e),p)

if __name__=='__main__':unittest.main()
