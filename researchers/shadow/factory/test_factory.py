import copy
import json
from pathlib import Path
import tempfile
import unittest
import factory as f

class FactoryTests(unittest.TestCase):
    def test_schema(self):
        good={'values':{str(i):i for i in range(6)}}
        self.assertEqual(f.parse_answer(json.dumps(good)),good)
        good['values']['0']=0.0
        self.assertEqual(f.parse_answer(json.dumps(good))['values']['0'],0)
        for bad in [True,'1',1.2,float('nan'),float('inf')]:
            obj=copy.deepcopy(good); obj['values']['0']=bad
            with self.assertRaises((AssertionError,ValueError,OverflowError)): f.parse_answer(json.dumps(obj))
        with self.assertRaises(Exception): f.parse_answer('```'+json.dumps(good)+'```')
    def test_bootstrap(self):
        self.assertEqual(f.bootstrap({'ring':[.5]*3,'community':[.5]*3},100),[.5,.5])
    def test_assignments_and_scoring(self):
        s=f.read_spec('split-sonnet-linked-strong',frozen=False)
        aa=f.assignments(s)
        self.assertEqual(len(aa),204)
        study,sim,_=f.load_parent()
        rows=[]
        for a in aa:
            ans=study.scripted(a['packet'])
            r={k:v for k,v in a.items() if k!='packet'}
            r.update(status='completed',metrics=sim.grade(ans['values'],a['answers'],a['fabricated']))
            if a['stage']=='Q': r['exact']=ans['values']==a['expected']
            rows.append(r)
        small=copy.deepcopy(s); small['bootstrap_draws']=100
        with tempfile.TemporaryDirectory() as d:
            out=Path(d)
            result=f.analyze(small,aa,rows,out)
            self.assertTrue(result['qualification_passed'])
            self.assertEqual(result['paired_roots'],48)
            self.assertAlmostEqual(result['primary'],4/9)
            # Failed rows stay assigned; complete pairs decline and worst-case bounds widen.
            rows[-1]['status']='failed'
            result=f.analyze(small,aa,rows,out)
            self.assertEqual(result['status'],'lead')
            self.assertEqual(result['paired_roots'],47)
            self.assertLess(result['all_assigned_bounds'][0],result['all_assigned_bounds'][1])
            # Duplicate terminal records fail closed.
            with self.assertRaises(AssertionError): f.analyze(small,aa,rows+[rows[0]],out)
    def test_no_paid_route(self):
        self.assertEqual(f.TOTAL_PAID_CAP_USD,20)
        for p in (f.ROOT/'specs').glob('*.json'):
            s=f.read_spec(p.name,False)
            self.assertEqual(s['max_paid_usd'],0)
            self.assertEqual(s['route'],'anthropic-pool')

if __name__=='__main__': unittest.main()
