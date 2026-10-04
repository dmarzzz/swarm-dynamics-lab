import copy,unittest
import instrument as i
import coordinator as c
import native as n
class SchedulingTests(unittest.TestCase):
 def oracle(self,w):
  def call(phase,p):
   # Test double only. Native actors never receive w or this closure.
   if phase=='learn':
    owner=p['position'];required=w['routes'][owner];cases=p['tests'];return {'note':i.note(owner,required),'actions':[{'case':x['case'],'action':i.reference(required,x['receipts'],owner,x['case'],x['epoch'])} for x in cases]}
   if phase=='commit':return {'note':i.note(p['position'],w['routes'][p['position']])}
   if phase=='select':
    owner=p['position'];required=(p['current_observations'][0]['authorized_witnesses'] if p['current_observations'] else w['routes'][owner]);return {'witnesses':required,'note':i.note(owner,required)}
   if phase=='attest':return {'reports':copy.deepcopy(p['private_inbox'])}
   if phase=='decide':
    owner=p['position'];return {'actions':[{'case':x['case'],'action':i.reference(p['private_note']['witnesses'],p['received_receipts'],owner,x['case'],x['epoch'])} for x in p['cases']]}
   if phase=='question':return {'question':'Which witnesses and current-evidence rule should I preserve?'}
   if phase=='teach':return {'note':p['private_note'],'explanation':'Use both current witnesses; defer on missing evidence.'}
  return call
 def test_native_calls_receive_only_local_data(self):
  w=i.world(902);g=i.Institution(w,'interactive',{p:i.note(p,w['routes'][p]) for p in w['members']});count=[];oracle=self.oracle(w)
  def spy(phase,p):
   self.assertNotIn('routes',p);self.assertNotIn('truth',p);n.request(phase,p);count.append(phase);return oracle(phase,p)
  r=c.checkpoint(g,0,spy);self.assertEqual(len(count),150);self.assertEqual(sum(x['correct'] for x in r['decisions']),300);self.assertTrue(all(x['copied_exactly'] for x in r['witnesses']))
 def test_changed_roles_native_reference(self):
  w=i.world(903);g=i.Institution(w,'interactive',{p:i.note(p,w['routes'][p]) for p in w['members']});r=c.checkpoint(g,50,self.oracle(w),changed=True);self.assertEqual(sum(x['correct'] for x in r['decisions']),300)
 def test_broken_commit_has_no_answer_bearing_test_panel(self):
  w=i.world(905);p=w['members'][0];g=i.Institution(w,'broken',{p:i.note(p,w['routes'][p])});seen=[]
  def spy(phase,packet):
   seen.append(packet);self.assertEqual(phase,'commit');return {'note':i.note(p,w['members'][1:3])}
  c.replace(g,p,spy);self.assertEqual(len(seen),1);self.assertNotIn('tests',seen[0]);self.assertNotIn('inherited_note',seen[0]);self.assertIsNone(seen[0]['private_note'])
 def test_simple_controller_uses_learned_not_gold_routes(self):
  w=i.world(907);notes={p:i.note(p,w['routes'][p]) for p in w['members']};good=c.controller_reference(w,notes,0);self.assertEqual(sum(x['correct'] for x in good['decisions']),300)
  for p in notes:notes[p]['witnesses']=[]
  bad=c.controller_reference(w,notes,0);self.assertLess(sum(x['correct'] for x in bad['decisions']),300)
 def test_complete_replacement_reference(self):
  w=i.world(904);g=i.Institution(w,'interactive',{p:i.note(p,w['routes'][p]) for p in w['members']})
  for p in w['replacement_order']:
   r=c.replace(g,p,self.oracle(w));self.assertTrue(r['teacher_semantics_correct']);self.assertTrue(r['note_correct'])
  self.assertTrue(all(v==1 for v in g.generation.values()))
if __name__=='__main__':unittest.main()

class FullScheduleFixture(unittest.TestCase):
 def test_full_50_member_scheduler_fixture_and_envelopes(self):
  w=i.world(10001);oracle=SchedulingTests().oracle(w);counts=[]
  def checked(phase,p):
   wire=n.request(phase,p);counts.append(i.packet_bytes(wire));return oracle(phase,p)
  result=c.evaluate_world(w,checked)
  self.assertTrue(result['qualification_passed']);self.assertEqual(len(result['arms']),4)
  self.assertLessEqual(len(counts)+30,2400);self.assertLessEqual(max(counts),8000)
  for arm in ('interactive','static','broken'):
   self.assertEqual(result['arms'][arm]['checkpoints'][-1]['founders_remaining'],0)
  self.assertEqual(result['arms']['retained']['checkpoints'][-1]['founders_remaining'],50)
 def test_attention_capacity_congestion_is_recorded(self):
  w=i.world(11111);g=i.Institution(w,'broken');oracle=SchedulingTests().oracle(w)
  def overloaded(phase,p):
   if phase=='select':
    peers=[x for x in w['members'] if x!=p['position']][:2]
    return {'witnesses':peers,'note':i.note(p['position'],peers)}
   if phase=='attest':self.assertLessEqual(len(p['private_inbox']),2)
   return oracle(phase,p)
  result=c.checkpoint(g,50,overloaded);self.assertGreater(len(result['attention_overflow']),0)
