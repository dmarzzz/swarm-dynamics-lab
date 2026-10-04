import unittest,copy,json
from collections import Counter
import turnover,contract,test_q3
from development import dev_world
class TurnoverTests(unittest.TestCase):
 def test_four_arms_share_checkpoint_and_full_replacement(self):
  for family in ('release','failover','delegation'):
   seen=[]
   def call(fam,phase,p,condition):
    contract.wire(phase,fam,p);seen.append((phase,condition,copy.deepcopy(p)))
    self.assertNotIn('routes',p);self.assertNotIn('gold',p)
    if 'static' in condition and phase=='teach':self.assertNotIn('question',p)
    if phase=='commit' and 'broken' in condition:
     self.assertNotIn('inherited_note',p);self.assertNotIn('predecessor_message',p);self.assertEqual(p['current_observations'],[]);self.assertIsNone(p['private_note'])
     return {'note':{'witnesses':[x['position'] for x in p['roster'] if x['position']!=p['position']][:2]}}
    return test_q3.oracle(fam,phase,p,condition)
   result=turnover.trajectory(dev_world(8800),family,call);self.assertTrue(result['complete']);self.assertLessEqual(len(seen),138)
   for arm,r in result['arms'].items():
    self.assertEqual(r['initial_notes'],result['common_notes']);self.assertEqual(len(r['replacements']),0 if arm=='retained' else 6)
    self.assertEqual(set(r['terminal_generations'].values()),{0} if arm=='retained' else {1});self.assertEqual(len(r['terminal']['decisions']),6)
   self.assertEqual(sum(phase=='learn' for phase,_,_ in seen),6)
   for arm in ('interactive','static','retained'):self.assertTrue(result['arms'][arm]['terminal']['passed'])
 def test_acquisition_failure_cannot_be_scored_as_culture_loss(self):
  def fail(*args):return {'note':{'witnesses':[]}}
  r=turnover.trajectory(dev_world(8801),'release',fail);self.assertFalse(r['complete']);self.assertEqual(r['arms'],{});self.assertEqual(r['stop'],'founder_gate')
if __name__=='__main__':unittest.main()
