import unittest,sys,itertools,math
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from scenario import *
from trace_contract import *

def brute(q,c):
    best=math.inf
    for first,a,b in itertools.product(('trust','check'),repeat=3):
        loss=0
        for good,y,z in itertools.product((False,True),repeat=3):
            p=.9 if good else .3;weight=(q if good else 1-q)*(p if y else 1-p)*(p if z else 1-p)
            second=(a if y else b) if first=='check' else a
            loss+=weight*((c if first=='check' else not y)+(c if second=='check' else not z))
        best=min(best,loss)
    return best
class Tests(unittest.TestCase):
 def test_posterior_direct_likelihood(self):
  for h in itertools.product((False,True),repeat=3):
   for noise in (.1,.3):
    ps=[noise+(1-2*noise)*p for p in (.9,.3)];weights=[math.prod(p if x else 1-p for x in h) for p in ps];q=weights[0]/sum(weights)
    self.assertAlmostEqual(posterior(h,noise,0),q);self.assertAlmostEqual(posterior(h,noise,.4),.6*q+.4*(1-q))
 def test_bellman_against_policy_enumeration(self):
  for q,c in itertools.product((0,.1,.5,.5226708829968377,.9,1),(.1,.4)):
   self.assertAlmostEqual(min(values(q,c,2).values()),brute(q,c));self.assertGreaterEqual(min(values(q,c,2).values())+1e-12,q*oracle_cost(True,c)+(1-q)*oracle_cost(False,c))
 def test_information_changes_action(self):
  q=posterior((True,True,False),.1,.4);self.assertEqual(choose(q,.4,1),'trust');self.assertEqual(choose(q,.4,2),'check');self.assertAlmostEqual(values(q,.4,2)['trust']-values(q,.4,2)['check'],.07095645828265629)
 def test_feedback_and_hidden_projection(self):
  self.assertIsNone(step('trust',False,.4)['feedback']);self.assertEqual(step('trust',False,.4)['loss'],1)
  self.assertIs(step('check',False,.4)['feedback'],False);self.assertEqual(step('check',False,.4)['loss'],.4)
  p=observable((True,True,False),.1,.4,.4);self.assertEqual(set(p),{'calibration','noise','shift_probability','check_cost','feedback','remaining','legal_actions'});self.assertNotIn('posterior',p)
  self.assertEqual(controller(p,'bayes'),'check');self.assertEqual(controller(p,'posterior_greedy'),'trust')
  self.assertEqual(controller(p,'always_trust'),'trust');self.assertEqual(controller(p,'always_check'),'check')
  copied=dict(p,feedback=[False],remaining=1);self.assertEqual(controller(copied),choose(update(posterior((True,True,False),.1,.4),False),.4,1));self.assertEqual(p['feedback'],[])
 def test_development_partition(self):
  xs=development_cases();self.assertEqual(len(xs),24);self.assertEqual([x['id'] for x in xs],list(range(3000,3024)));self.assertTrue(all(len(x['visible']['calibration'])==3 for x in xs))
 def test_sanitized_response_preserves_diagnostics(self):
  raw=dict(type='choice',choice='check',probabilities={'trust':.3,'check':.7},confidence=.8,headers={'Authorization':'SYNTHETIC_SECRET'},debug='SYNTHETIC_SECRET');p=project_answer(raw,('trust','check'));self.assertEqual(p['confidence'],.8);self.assertNotIn('SYNTHETIC_SECRET',str(p))
  raw['probabilities']['debug']='SYNTHETIC_SECRET'
  with self.assertRaises(ValueError):project_answer(raw,('trust','check'))
 def test_full_denominator_and_failures(self):
  events=[dict(id='a',kind='start'),dict(id='a',kind='terminal',status='failed'),dict(id='b',kind='start')];self.assertEqual(reconcile(['a','b','c'],events),{'a':'failed','b':'started','c':'not-started'})
  with self.assertRaises(ValueError):reconcile(['a','b','c'],events+[dict(id='a',kind='start')])
 def test_invalid_inputs(self):
  for p in (True,float('nan'),float('inf'),-1,2):
   with self.assertRaises(ValueError):probability(p)
  with self.assertRaises(ValueError):values(.5,.4,3)
  with self.assertRaises(ValueError):step('invented',True,.1)
  with self.assertRaises(ValueError):observable((True,False,True),.1,0,.4,(0,))
  with self.assertRaises(ValueError):observable((True,False,True),.1,0,.4,(True,True,True))
if __name__=='__main__':unittest.main()
