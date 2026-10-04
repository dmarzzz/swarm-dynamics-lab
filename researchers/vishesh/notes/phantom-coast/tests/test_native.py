import copy,sys,tempfile,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import native as n
from budget import Budget
from instrument import world,request_for_assignment,digest
class Native(unittest.TestCase):
    def setUp(self):
        w=world(100);self.req=n.request(request_for_assignment(w,dict(kind='clean',actor=0)))
        self.raw={'model':n.SNAPSHOT,'provider':'TypeSafe','usage':{'cost':.001,'input_tokens':2000,'output_tokens':300},
                  'answers':{k:{'type':'choice','choice':'LAND','confidence':1,'probabilities':{'LAND':1,'WATER':0,'UNKNOWN':0}} for k in self.req['questions']}}
    def test_targets_explicit(self):
        self.assertEqual(len(self.req['questions']),36)
        for c in n.CELLS:self.assertIn(c,self.req['questions']['cell_'+c.replace(',','_')]['instructions'])
    def test_native_shape(self):
        result=n.validate(self.raw,self.req);self.assertEqual(len(result['response']['map']),36);self.assertEqual(result['response']['evidence_ids'],[])
    def test_missing_answer_rejected(self):
        self.raw['answers'].pop('cell_0_0')
        with self.assertRaises(ValueError):n.validate(self.raw,self.req)
    def test_route_rejected(self):
        self.raw['model']='different'
        with self.assertRaises(ValueError):n.validate(self.raw,self.req)
    def test_nan_rejected(self):
        self.raw['answers']['cell_0_0']['probabilities']['LAND']=float('nan')
        with self.assertRaises(ValueError):n.validate(self.raw,self.req)
    def test_rounding_tolerance(self):
        self.raw['answers']['cell_0_0']['probabilities']={'LAND':.34,'WATER':.33,'UNKNOWN':.34}
        n.validate(self.raw,self.req)
    def test_wrong_mass_rejected(self):
        self.raw['answers']['cell_0_0']['probabilities']={'LAND':.9,'WATER':.9,'UNKNOWN':.9}
        with self.assertRaises(ValueError):n.validate(self.raw,self.req)
    def test_cost_bound(self):
        self.raw['usage']['cost']=1
        with self.assertRaises(ValueError):n.validate(self.raw,self.req)
    def test_missing_qualification_is_failure(self):
        x=n.qualification([]);self.assertFalse(x['qualification_passed']);self.assertEqual(x['upper'],1)
        self.assertEqual(x['by_label']['LAND']['denominator'],216)
    def test_atomic_budget_and_duplicates(self):
        with tempfile.TemporaryDirectory() as d:
            b=Budget(Path(d)/'ledger',2*n.RESERVE_NANO);b.reserve('a');b.finish('a');b.reserve('b')
            with self.assertRaises(ValueError):b.reserve('c')
            b.finish('b',0)
            with self.assertRaises(Exception):b.reserve('a')
            self.assertEqual(b.summary()['cost_with_unresolved_reservations_usd'],n.RESERVE_NANO/1e9)
            with self.assertRaises(ValueError):Budget(Path(d)/'ledger',3*n.RESERVE_NANO)
            b.close()
    def test_missing_history_not_null(self):
        x=n.analyze_history([])
        self.assertEqual(x['assigned'],522)
        self.assertEqual(x['mean_interaction'],{'lower':-2,'upper':2})
        self.assertTrue(all(t['error']['upper']==1 for w in x['worlds'] for t in w['trajectories']))
    def test_unauthorized_launch_fails_before_git_or_network(self):
        from live_worker import verify_config
        with self.assertRaisesRegex(ValueError,'spending_authorization_required'):
            verify_config({'experiment':'phantom-coast','stage':'Q0','design':'PC-1L'},'Q0',Path('/nonexistent'))
    def test_all_correct_qualification(self):
        records=[]
        for a in n.schedule('Q0'):
            records.append({'id':a['id'],'status':'valid','checked':{'response':{'map':world(a['seed'],stage='Q0')['truth'],'evidence_ids':[]}}})
        result=n.qualification(records)
        self.assertTrue(result['qualification_passed']);self.assertEqual(result['upper'],0)
        records[0]['status']='failed'
        self.assertFalse(n.qualification(records)['qualification_passed'])
if __name__=='__main__':unittest.main()
