import copy,json,unittest
import scale_families as f,scale_contract as c,scale_study as s,scale_engine as e,scale_turnover as t
import families as old
from instrument import world

class ScaleTests(unittest.TestCase):
 def test_sparse_history_equivalence_and_unique_inference(self):
  for seed in range(90600,90604):
   w=world(seed,50)
   for family in f.FAMILIES:
    for owner in w['members']:
     for changed in (False,True):
      h=f.history(w,family,owner,changed)
      self.assertEqual(f.expanded(w,family,owner,h,changed),old.history(w,family,owner,changed))
      self.assertEqual(set(f.infer(owner,[p for p in w['members'] if p!=owner],h)),set(w['changed_routes' if changed else 'routes'][owner]))
  with self.assertRaisesRegex(ValueError,'nonidentifiable'):f.infer('a',['b','c','d'],{'episodes':[]})

 def test_allocation_and_complete_lifecycle(self):
  for fn,cap in ((s.qualify,60),(s.main,1150)):
   calls=[]
   def call(family,phase,p,condition):
    body=c.wire(phase,family,p);calls.append((phase,len(json.dumps(body,separators=(',',':')).encode())))
    self.assertFalse({'routes','changed_routes','gold','replacement_order','seed'} & set(p))
    if phase=='commit' and 'inherited_note' not in p:
     self.assertIsNone(p['private_note']);self.assertNotIn('predecessor_message',p);self.assertEqual(p['current_observations'],[])
    return c.to_engine(phase,s.scripted(family,phase,p,condition))
   result=fn(call);self.assertTrue(result.get('passed',result.get('complete')));self.assertLessEqual(len(calls),cap)
   if fn==s.main:
    for arm,r in result['arms'].items():
     self.assertEqual(len(r['replacements']),0 if arm=='retained' else 50)
     self.assertEqual(set(r['terminal_generations'].values()),{0 if arm=='retained' else 1})
     self.assertEqual(sum(x['assigned'] for x in r['terminal']['decisions']),300)
     if arm!='broken':self.assertTrue(r['terminal']['passed'])

 def test_main_wrong_legal_decisions_remain_observed(self):
  def call(family,phase,p,condition):
   v=s.scripted(family,phase,p,condition)
   if phase=='decide':v['actions'][0]['action']='allow' if v['actions'][0]['action']!='allow' else 'hold'
   return c.to_engine(phase,v)
  result=s.main(call)
  self.assertTrue(result['complete']);self.assertFalse(result['initial']['passed'])

 def test_strict_commit_failure_preserved(self):
  w=world(90610,50);p=w['members'][0];g=e.Institution(w,'failover',{x:{'witnesses':w['routes'][x]} for x in w['members']})
  def call(fam,phase,packet,condition):
   v=s.scripted(fam,phase,packet,condition)
   if phase=='commit':v['decision']='defer'
   return c.to_engine(phase,v)
  with self.assertRaisesRegex(ValueError,'commit_schema'):t.replace(g,p,'interactive',call)

 def test_byte_limits_and_route_are_fail_closed(self):
  with self.assertRaisesRegex(ValueError,'oversized'):c.wire('commit','failover',{'text':'x'*12000})
  b=c.wire('commit','failover',{});b['provider']['allow_fallbacks']=True
  with self.assertRaisesRegex(ValueError,'route'):c.validate(b)
  self.assertEqual(c.PER_CALL*1210,c.PER_CALL*c.CAPS['Q50']+c.PER_CALL*c.CAPS['S50'])

 def test_maximum_nested_handoff_context(self):
  w=world(90611,50);owner=w['members'][0];note={'witnesses':w['routes'][owner]}
  teacher={'note':note,'explanation':'x'*1100};question={'question':'\U0001f642'*400}
  self.assertLessEqual(len(json.dumps(teacher,separators=(',',':'))),1200)
  g=e.Institution(w,'failover',{owner:note});p=t.c.successor(owner,g.actor(owner)['roster'],'static',note,teacher,question)
  self.assertLessEqual(len(json.dumps(c.wire('commit','failover',p),separators=(',',':')).encode()),12000)

 def test_future_stale_conflict_and_degree(self):
  for seed in range(90620,90624):
   w=world(seed,50)
   for key in ('routes','changed_routes'):
    self.assertEqual({sum(p in v for v in w[key].values()) for p in w['members']},{2})
   p=w['members'][0]
   for variant in ('future','old'):
    ex=f.example(w,'failover',p,'invalid',variant)
    self.assertEqual(f.decide(w['routes'][p],ex['private_records']+ex['public_records'],ex['target']),'defer')
   ex=f.example(w,'failover',p,'conflict');self.assertEqual(f.decide(w['routes'][p],ex['private_records'],ex['target']),'defer')

if __name__=='__main__':unittest.main()
