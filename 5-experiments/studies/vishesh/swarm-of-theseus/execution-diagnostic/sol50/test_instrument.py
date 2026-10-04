import copy, unittest
import instrument as i
class InstrumentTests(unittest.TestCase):
 def test_fifty_connected_members(self):
  for seed in range(30):
   w=i.world(seed)
   for key in ['routes','changed_routes']:
    seen={w['members'][0]}
    while True:
     new=seen|{q for p in seen for q in w[key][p]}
     if new==seen:break
     seen=new
    self.assertEqual(len(seen),50)
    self.assertTrue(all(len(set(v))==2 and p not in v for p,v in w[key].items()))
 def test_all_truth_classes(self):
  w=i.world(41)
  for p in w['members']:
   for change in [False,True]:
    for kind,truth in [('allow','allow'),('veto','hold'),('missing','defer'),('stale','defer'),('conflict','defer'),('irrelevant_veto','allow')]:
     self.assertEqual(i.challenge(w,p,50,kind,change)['truth'],truth)
 def test_complete_turnover(self):
  w=i.world(17);g=i.Institution(w,'interactive')
  for p in w['members']:g.notes[p]=i.note(p,w['routes'][p])
  for p in w['replacement_order']:g.replace(p,{'owner':p,'marker':'successor'})
  self.assertEqual(sum(g.generation.values()),50);self.assertEqual(len(g.events),50)
  self.assertTrue(all('/g1' in g.identity(p) for p in w['members']))
  self.assertTrue(all(x['marker']=='successor' for x in g.notes.values()))
 def test_actor_cannot_see_evaluator_or_peers(self):
  w=i.world(1);g=i.Institution(w,'interactive');a,b=w['members'][:2];g.notes[b]={'secret':'peer-only'}
  p=g.actor(a);self.assertNotIn('routes',p);self.assertNotIn('seed',p);self.assertNotIn('peer-only',str(p))
  p['current_observations'].append('mutation');self.assertEqual(g.actor(a)['current_observations'],[])
 def test_broken_and_retained_constraints(self):
  w=i.world(1)
  with self.assertRaises(ValueError):i.Institution(w,'broken').actor(w['members'][0],inherited={'note':'forbidden'})
  with self.assertRaises(ValueError):i.Institution(w,'retained').replace(w['members'][0],{})
 def test_typed_teacher_semantics(self):
  w=i.world(2);p=w['members'][0];n=i.note(p,w['routes'][p]);self.assertTrue(i.valid_note(n,p,w['routes'][p]));n['practice']='accept_any';self.assertFalse(i.valid_note(n,p,w['routes'][p]))
 def test_cross_owner_case_and_epoch_receipts(self):
  w=i.world(3);p=w['members'][0];c=i.challenge(w,p,0,'allow');required=w['routes'][p]
  for field,bad in [('owner','other'),('case','other'),('epoch',-1)]:
   rows=copy.deepcopy(c['receipts']);rows[0][field]=bad;self.assertEqual(i.reference(required,rows,p,c['case'],c['epoch']),'defer')
 def test_selective_revision_preserves_unaffected(self):
  w=i.world(4);notes={p:i.note(p,w['routes'][p]) for p in w['members']}
  for p in w['members']:
   new=i.selective_update(notes,p,i.examples(w,p,True));self.assertEqual(new[p],i.note(p,w['changed_routes'][p]));self.assertTrue(all(new[q]==notes[q] for q in notes if q!=p))
 def test_budget_retains_history(self):
  b=i.budget();self.assertLess(b['cumulative_worst_case_usd'],60);self.assertAlmostEqual(b['model_reserved_usd'],53.1456)
 def test_exact_model_and_size(self):
  body={'model':'openai/gpt-6-sol','max_tokens':512,'provider':{'allow_fallbacks':False}};self.assertTrue(i.check_wire(body))
  for patch in [{'model':'openai/gpt-6-sol-pro'},{'max_tokens':1024},{'provider':{'allow_fallbacks':True}},{'text':'a'*8001}]:
   with self.assertRaises(ValueError):i.check_wire(dict(body,**patch))
if __name__=='__main__':unittest.main()

class SemanticOrderRepair(unittest.TestCase):
 def test_reversed_pair_is_same_note(self):
  w=i.world(19);p=w["members"][0];n=i.note(p,w["routes"][p]);n["witnesses"].reverse();self.assertTrue(i.valid_note(n,p,w["routes"][p]));n["witnesses"]=[n["witnesses"][0]]*2;self.assertFalse(i.valid_note(n,p,w["routes"][p]))
 def test_reordered_reports_preserve_conflicting_duplicates(self):
  rows=[{"owner":"p","observations":[{"case":"c","epoch":1,"allow":True},{"case":"c","epoch":1,"allow":False}]}];other=copy.deepcopy(rows);other[0]["observations"].reverse();self.assertTrue(i.same_reports(rows,other));other[0]["observations"].pop();self.assertFalse(i.same_reports(rows,other))
 def test_cache_write_reservation(self):
  body={"text":"x"*1000};self.assertAlmostEqual(i.reservation_usd(body),(i.packet_bytes(body)+512)*2.5/1e6+.00512)
