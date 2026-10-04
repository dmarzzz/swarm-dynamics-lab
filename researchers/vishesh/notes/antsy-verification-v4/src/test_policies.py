import copy,unittest
import policies as p


def fixture():
    return {'id':1,'modes':{m:{'observations':[{'confidence':.8,'words':10} for _ in range(3)],'evaluation':{'recall':q,'regions':[q,q,q],'total_field_exact':q>.8}} for m,q in zip(p.MODES,(.4,.9,.6))}}
CAL={'bias':dict.fromkeys(p.MODES,0),'best_fixed':'B'}

class Tests(unittest.TestCase):
    def test_blindness(self):
        a=fixture();b=copy.deepcopy(a);b['modes']['A']['evaluation']['recall']=0
        self.assertEqual(p.initial(a,CAL),p.initial(b,CAL));self.assertNotIn('evaluation',p.actor_input(p.initial(a,CAL),0,False))
    def test_budget_and_duplicate(self):
        r=fixture();b=p.initial(r,CAL);p.purchase(b,r,'A',0)
        with self.assertRaises(ValueError):p.purchase(b,r,'A',0)
        p.purchase(b,r,'B',0)
        with self.assertRaises(ValueError):p.purchase(b,r,'C',0)
    def test_stopping_prefix(self):
        r=fixture();tape=[['STOP']*4+['A'],['B']*5]
        fixed=p.policy(r,CAL,'swarm-fixed',tape=tape);adaptive=p.policy(r,CAL,'swarm-adaptive',tape=tape)
        self.assertEqual(len(fixed['checks']),2);self.assertEqual(len(adaptive['checks']),0)
    def test_random_pairing_and_no_truth_mutation(self):
        r=fixture();old=copy.deepcopy(r);self.assertEqual(p.policy(r,CAL,'random-checks'),p.policy(r,CAL,'random-checks'));self.assertEqual(r,old)
    def test_counterfactual_grade(self):
        r=fixture();result=p.policy(r,CAL,'best-fixed');self.assertEqual(p.evaluate(r,result)['regret'],0)
        self.assertGreaterEqual(p.budget_oracle(r,CAL),.4)
    def test_tool_failure_is_retained(self):
        class Broken:
            def choose(self,*args):raise RuntimeError('injected')
        r=p.policy(fixture(),CAL,'single-agent',Broken());self.assertFalse(r['valid']);self.assertEqual(r['error'],'RuntimeError')

if __name__=='__main__':unittest.main()
