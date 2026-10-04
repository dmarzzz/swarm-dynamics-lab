"""Offline development inputs only; neither C5 assignments nor model calls are generated."""
import unittest,sys,json,importlib.util
from pathlib import Path
HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('c5_scenarios',HERE/'scenarios.py');scenarios=importlib.util.module_from_spec(spec);spec.loader.exec_module(scenarios)
sys.path.insert(0,str(HERE.parent/'c4'))
from contract import qwen_payload
sys.path.insert(0,str(HERE.parent/'src'))
from jev import request
class ContextTests(unittest.TestCase):
    def test_name_independent_of_truth_and_family(self):
        for i in range(4):
            rows=[scenarios.fixture(label,900+i) for label in scenarios.LABELS]
            self.assertEqual(len({r['claim'] for r in rows}),1)
            for r in rows:
                text=r['claim']+' '+r['report']
                for forbidden in (*scenarios.LABELS,r['family'],'development','C5-'):
                    self.assertNotIn(forbidden,text)
    def test_exact_agent_visible_fields(self):
        for label in scenarios.LABELS:
            for i in range(4):
                r=scenarios.fixture(label,900+i)
                mutated={**r,'expected':'SECRET_TRUTH','family':'SECRET_FAMILY','id':'SECRET_ID','curator':'SECRET_CURATOR'}
                for variant in (0,1):
                    self.assertEqual(qwen_payload(r,variant),qwen_payload(mutated,variant))
                self.assertEqual(request(r,0,'development'),request(mutated,0,'development'))
                visible=request(r,0,'development')['state']
                self.assertEqual(set(visible),{'claim','report'})
                self.assertIn(r['claim'],qwen_payload(r,0)['messages'][0]['content'])
                self.assertIn(r['report'],qwen_payload(r,0)['messages'][0]['content'])
    def test_only_qwen_enum_order_changes(self):
        r=scenarios.fixture('SUPPORT',900);a=qwen_payload(r,0);b=qwen_payload(r,1)
        self.assertNotEqual(a['format'],b['format']);a.pop('format');b.pop('format');self.assertEqual(a,b)
    def test_explicit_comparison_and_unknown_measurement(self):
        for i in range(4):
            for label in ('SUPPORT','REFUTE'):
                self.assertIn('baseline',scenarios.fixture(label,900+i)['report'])
            self.assertTrue(any(x in scenarios.fixture('UNCERTAIN',900+i)['report'] for x in ('never tested','no accuracy result','without accuracy','planned')))
    def test_no_automatic_main_stage(self):
        with self.assertRaises(ValueError):scenarios.assignments('S1')
if __name__=='__main__':unittest.main()
