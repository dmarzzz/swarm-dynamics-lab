import unittest,copy
from itertools import product
import typed_interface as t
class TypedTests(unittest.TestCase):
    def test_all_signal_patterns_and_labels_roundtrip(self):
        for bits in product((0,1),repeat=6):
            values=[list(bits[k:k+2]) for k in (0,2,4)]
            for label in (None,True,False):
                r={'id':'opaque','readings':values}
                if label is not None:r.update(outcome=label,epoch=0)
                self.assertEqual(t.decode(t.encode(r)),r)
    def test_named_fields_remove_position_dependency(self):
        r=t.encode({'id':'x','readings':[[1,0],[0,1],[1,1]]});self.assertEqual(r['sources']['source_0'],{'signal':1,'fresh':0});self.assertNotIn('readings',r)
    def test_teacher_rule_and_support_not_just_copying(self):
        for seed in range(31000,31020):
            w=t.development_world(seed,'stable_exception')
            for role,d in w['roles'].items():
                r={'governing_source':t.SOURCES[d['source']],'predicate':t.PREDICATES[role],'evidence':[t.encode(x) for x in t.i.minimal_support(role,d['history'])]}
                self.assertTrue(t.teacher_gate(role,r,d['history']))
                self.assertFalse(t.teacher_gate(role,dict(r,predicate='split_source_signal_fresh'),d['history']))
                self.assertFalse(t.teacher_gate(role,dict(r,governing_source=t.SOURCES[(d['source']+1)%3]),d['history']))
    def test_evaluation_self_labels_not_provenance(self):
        w=t.development_world(31001,'stable_exception');d=w['roles']['release'];case=dict(d['tests'][0],outcome=True,epoch=0)
        self.assertFalse(t.teacher_gate('release',{'governing_source':t.SOURCES[d['source']],'predicate':'signal_and_fresh','evidence':[t.encode(case)]},d['history']))
    def test_ordinary_training_contains_both_outcomes(self):
        for seed in range(31000,31100):
            for d in t.development_world(seed,'stable_exception')['roles'].values():self.assertEqual({h['outcome'] for h in d['history']},{True,False})
    def test_invalid_fields_fail(self):
        with self.assertRaises(ValueError):t.decode({'id':'x','sources':{'source_0':{'signal':1,'fresh':0}}})
if __name__=='__main__':unittest.main()
