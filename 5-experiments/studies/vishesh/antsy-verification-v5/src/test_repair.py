import unittest
from repair import Board,Observation,decide

def board():return Board({m:[{'confidence':q}]*3 for m,q in [('A',.6),('B',.5),('C',.1)]},{m:0 for m in 'ABC'})
def scenario():
 return {'modes':{m:{'evaluation':{'regions':[v]*3,'recall':v}} for m,v in [('A',0.),('B',1.),('C',0.)]}}
class Contracts(unittest.TestCase):
 def test_null_preserves_all_scores(self):
  for m in 'ABC':
   for j in range(3):
    b=board();before=b.scores();b.buy(Observation(m,j,None));self.assertEqual(b.scores(),before);self.assertEqual(b.choose(),'A')
 def test_zero_is_evidence(self):
  b=board();b.buy(Observation('A',0,0.));self.assertAlmostEqual(b.scores()['A'],.4);self.assertEqual(b.choose(),'B')
 def test_global_empty_is_symmetric(self):
  b=board();b.buy(Observation('A',0,None));self.assertEqual(b.scores('global-empty'),{'A':.6,'B':.5,'C':.1})
 def test_original_failure_reproduced(self):
  b=Board({m:[{'confidence':q} for q in qs] for m,qs in [('A',[0,.8,.8]),('B',[.7,.7,.7]),('C',[0,0,0])]},{m:0 for m in 'ABC'})
  self.assertEqual(b.choose(),'B');b.buy(Observation('A',0,None));self.assertEqual(b.choose('original'),'A');self.assertEqual(b.choose(),'B')
 def test_duplicate_and_budget(self):
  b=board();b.buy(Observation('A',0,None))
  with self.assertRaises(ValueError):b.buy(Observation('A',0,0))
  b.buy(Observation('B',1,0))
  with self.assertRaises(ValueError):b.buy(Observation('C',2,0))
 def test_continue_for_useful_check(self):
  action,values=decide(board(),[scenario()],.1);self.assertIsNotNone(action);self.assertGreater(values[action],.1)
 def test_stop_when_expensive(self):self.assertIsNone(decide(board(),[scenario()],1.)[0])
 def test_stop_when_no_value(self):
  r=scenario()
  for m in 'ABC':r['modes'][m]['evaluation']['recall']=.5
  self.assertIsNone(decide(board(),[r],0.)[0])
 def test_zero_budget(self):
  b=board();b.buy(Observation('A',0,0));b.buy(Observation('A',1,0));self.assertIsNone(decide(b,[scenario()],0.)[0])
 def test_invalid_observation(self):
  for q in [-1,2,float('nan')]:
   with self.assertRaises(ValueError):Observation('A',0,q)
 def test_no_current_truth_in_board(self):self.assertEqual(set(vars(board())),{'prior','checks'})
if __name__=='__main__':unittest.main()
