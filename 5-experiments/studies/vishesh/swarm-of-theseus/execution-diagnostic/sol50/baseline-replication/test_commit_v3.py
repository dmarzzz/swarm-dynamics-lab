import unittest
import commit_v3,selection_v2
class CommitCandidateTests(unittest.TestCase):
 def test_only_commit_instruction_changes(self):
  for family in ('release','failover','delegation'):
   for phase in ('learn','select','attest','decide','question','teach','commit'):
    old=selection_v2.wire(phase,family,{});new=commit_v3.wire(phase,family,{})
    if phase=='commit':
     self.assertNotEqual(old['messages'][0],new['messages'][0]);self.assertEqual(old['messages'][1:],new['messages'][1:]);self.assertEqual({k:v for k,v in old.items() if k!='messages'},{k:v for k,v in new.items() if k!='messages'})
    else:self.assertEqual(old,new)
 def test_existing_engine_keeps_schema_and_semantics_separate(self):
  import copy,engine,turnover
  from development import dev_world
  w=dev_world(77331);owner=w['members'][0];gold=w['routes'][owner];peers=[p for p in w['members'] if p!=owner];wrong=next([a,b] for a in peers for b in peers if a!=b and set([a,b])!=set(gold))
  for pair,extra in ((gold,False),(wrong,False),(gold,True)):
   state=engine.Institution(w,'release',{p:{'witnesses':w['routes'][p]} for p in w['members']})
   def call(family,phase,packet,condition):
    commit_v3.wire(phase,family,packet)
    if phase=='question':return {'question':'Which peers?'}
    if phase=='teach':return {'note':{'witnesses':gold},'explanation':'Recorded pair.'}
    value={'note':{'witnesses':pair}}
    if extra:value['decision']='defer'
    return value
   if extra:
    with self.assertRaisesRegex(ValueError,'commit_schema'):turnover.replace(state,owner,'interactive',call)
   else:self.assertEqual(turnover.replace(state,owner,'interactive',call)['note_correct'],pair==gold)
if __name__=='__main__':unittest.main()
