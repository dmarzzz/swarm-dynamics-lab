import unittest
import instrument as i
import coordinator as c
from addressing import resolve_pair
import test_coordinator
class AddressTests(unittest.TestCase):
 def setUp(self):
  self.w=i.world(61616);self.g=i.Institution(self.w,'interactive');self.p=self.w['members'][0]
 def test_positions_current_identities_and_mixed(self):
  peers=self.w['routes'][self.p];roster=self.g.actor(self.p)['roster']
  for values in [peers,[self.g.identity(x) for x in peers],[peers[0],self.g.identity(peers[1])]]:self.assertEqual(resolve_pair(values,roster,self.p),peers)
 def test_retired_generation_never_maps_to_replacement(self):
  a,b=self.w['routes'][self.p];old=self.g.identity(a);self.g.replace(a,None)
  with self.assertRaises(ValueError):resolve_pair([old,b],self.g.actor(self.p)['roster'],self.p)
  self.assertEqual(resolve_pair([self.g.identity(a),b],self.g.actor(self.p)['roster'],self.p),[a,b])
 def test_duplicate_unknown_and_self(self):
  a,b=self.w['routes'][self.p];roster=self.g.actor(self.p)['roster']
  for values in [[a,self.g.identity(a)],[a,'unknown'],[a,self.p]]:
   with self.assertRaises(ValueError):resolve_pair(values,roster,self.p)
 def test_wrong_current_peer_is_not_repaired(self):
  wrong=[x for x in self.w['members'] if x!=self.p and x not in self.w['routes'][self.p]][:2]
  self.assertEqual(resolve_pair(wrong,self.g.actor(self.p)['roster'],self.p),wrong)
 def test_ambiguous_roster_rejected(self):
  roster=self.g.actor(self.p)['roster'];roster[1]['identity']=roster[2]['identity']
  with self.assertRaises(ValueError):resolve_pair(self.w['routes'][self.p],roster,self.p)
 def test_full_native_schedule_fixture_using_identity_aliases(self):
  self.g.notes={p:i.note(p,self.w['routes'][p]) for p in self.w['members']};oracle=test_coordinator.SchedulingTests().oracle(self.w)
  def aliases(phase,packet):
   result=oracle(phase,packet)
   if phase=='select':result['witnesses']=[self.g.identity(x) for x in result['witnesses']]
   return result
  out=c.checkpoint(self.g,0,aliases);self.assertEqual(sum(x['correct'] for x in out['decisions']),300);self.assertEqual(len(out['witnesses']),50);self.assertTrue(all(x['route_correct'] for x in out['selections']));self.assertFalse(out['attention_overflow'])
if __name__=='__main__':unittest.main()
