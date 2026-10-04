import copy
import json
from pathlib import Path
import sys
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from scoring import digest,text_hash,score,paired_summary,reconcile_chain
from fixtures import cases,validate,copy_source,reference_lookup

class ScoringTests(unittest.TestCase):
    def setUp(self):
        self.case=cases()[0];self.hop=self.case['trajectories']['faithful'][0]
        self.gold=self.case['gold'];self.visible={r['id'] for r in self.case['records']}
    def result(self,review=None):
        return score(self.hop['text'],review or self.hop['review'],self.gold,self.visible)
    def test_full_fixture_matrix(self):
        r=validate();self.assertEqual((r['roots'],r['trajectories'],r['hop_outputs']),(8,24,72))
    def test_output_hash_tampering_refused(self):
        with self.assertRaises(ValueError):score(self.hop['text']+' changed',self.hop['review'],self.gold,self.visible)
    def test_gold_hash_tampering_refused(self):
        gold=copy.deepcopy(self.gold);gold['obligations'][0]['acceptable'][0]['fact']['time']='future'
        with self.assertRaises(ValueError):score(self.hop['text'],self.hop['review'],gold,self.visible)
    def test_duplicate_assertions_do_not_raise_retention(self):
        r=copy.deepcopy(self.hop['review']);r['claims']+=copy.deepcopy(r['claims'])
        self.assertEqual(self.result(r),self.result())
    def test_correct_and_wrong_same_obligation_fails(self):
        r=copy.deepcopy(self.hop['review']);bad=copy.deepcopy(r['claims'][0]);bad['fact']['modality']='verified';bad['support']='contradicted';r['claims'].append(bad)
        self.assertEqual(self.result(r)['retained'],2)
    def test_inconsistent_duplicate_judgment_refused(self):
        r=copy.deepcopy(self.hop['review']);bad=copy.deepcopy(r['claims'][0]);bad['support']='unknown';r['claims'].append(bad)
        with self.assertRaises(ValueError):self.result(r)
    def test_missing_and_unreviewed_are_not_zero(self):
        self.assertEqual(score(None,None,self.gold,self.visible)['status'],'missing')
        self.assertIsNone(score(self.hop['text'],None,self.gold,self.visible)['retention'])
    def test_empty_scored_output_is_zero(self):
        r=copy.deepcopy(self.hop['review']);r.update(output_sha256=text_hash(''),claims=[])
        self.assertEqual(score('',r,self.gold,self.visible)['retention'],0)
    def test_unreviewed_assertions_refused(self):
        r=copy.deepcopy(self.hop['review']);r['all_assertions_reviewed']=False
        with self.assertRaises(ValueError):self.result(r)
    def test_citation_id_not_primary_advantage(self):
        r=copy.deepcopy(self.hop['review']);r['claims'][0]['citations']=['invented']
        result=self.result(r);self.assertEqual(result['retention'],1);self.assertEqual(result['invalid_citation_ids'],1)
        # Deliberately separate field: wrong citation invalidates a source-link claim, not semantic content.
    def test_unmapped_addition_reported_without_retention_gain(self):
        r=copy.deepcopy(self.hop['review']);extra=copy.deepcopy(r['claims'][0]);extra.update(obligation_id=None,support='unknown',critical_addition=True);extra['fact']['entity']='new entity';r['claims'].append(extra)
        self.assertEqual(self.result(r)['unsupported_critical_additions'],1);self.assertEqual(self.result(r)['retained'],3)
    def test_unknown_obligation_mapping_refused(self):
        r=copy.deepcopy(self.hop['review']);r['claims'][0]['obligation_id']='foreign'
        with self.assertRaises(ValueError):self.result(r)
    def test_order_and_evaluator_id_invariance(self):
        r=copy.deepcopy(self.hop['review']);r['claims'].reverse()
        self.assertEqual(self.result(r),self.result())
        self.assertNotIn('obligations',copy_source(self.case['records']))
        gold=copy.deepcopy(self.gold);gold['obligations'][0]['id']='renamed';r=copy.deepcopy(self.hop['review']);r['claims'][0]['obligation_id']='renamed';r['gold_sha256']=digest(gold)
        self.assertEqual(score(self.hop['text'],r,gold,self.visible)['retention'],1)
    def test_failed_parent_cannot_have_scored_descendant(self):
        missing={'status':'missing','retention':None}
        with self.assertRaises(ValueError):reconcile_chain([self.result(),missing,self.result()])
        self.assertIsNone(reconcile_chain([self.result(),missing,missing])['terminal_retention'])
    def test_paired_bounds_use_all_assignments(self):
        result=paired_summary(['a','b','c'],{'a':.5,'b':1},{'a':1,'b':0})
        self.assertEqual(result['complete_pair_mean'],-.25)
        self.assertEqual(result['all_assigned_bounds'],[-.5,1/6])
    def test_no_complete_pairs_stay_unknown(self):
        result=paired_summary(['a'],{},{});self.assertIsNone(result['complete_pair_mean']);self.assertEqual(result['all_assigned_bounds'],[-1,1])
    def test_invalid_pair_assignments_refused(self):
        for args in [(['a','a'],{},{}),(['a'],{'b':1},{}),(['a'],{'a':float('nan')},{})]:
            with self.assertRaises(ValueError):paired_summary(*args)
    def test_actor_projection_ignores_evaluator_metadata(self):
        records=copy.deepcopy(self.case['records']);original=copy_source(records)
        for record in records:record.update(gold='contradicted',family='changed',arm='structured')
        self.assertEqual(copy_source(records),original)
    def test_chain_rejects_numeric_missing_or_invalid_score(self):
        for bad in ({'status':'missing','retention':0},{'status':'scored','retention':2}):
            with self.assertRaises(ValueError):reconcile_chain([bad]*3)
    def test_critical_addition_requires_boolean(self):
        r=copy.deepcopy(self.hop['review']);r['claims'][0]['critical_addition']=1
        with self.assertRaises(ValueError):self.result(r)
    def test_reference_lookup_requires_unique_resolvable_ids(self):
        with self.assertRaises(ValueError):reference_lookup(self.case['records'],['absent'])
        with self.assertRaises(ValueError):reference_lookup(self.case['records']*2,[])

if __name__=='__main__':unittest.main()
