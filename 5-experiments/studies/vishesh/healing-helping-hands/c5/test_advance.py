"""Scripted transition faults: no held-out assignments, network or model calls."""
import unittest,copy
from advance import transition,consume_transition
class AdvanceTests(unittest.TestCase):
    def test_automatic_stage_cannot_dispatch_twice(self):
        import tempfile
        from pathlib import Path
        with tempfile.TemporaryDirectory() as t:
            p=Path(t)/'dispatch.json';consume_transition(p,{'advance':True})
            with self.assertRaises(FileExistsError):consume_transition(p,{'advance':True})
    def good(self):
        rows=[{'id':str(i),'expected':('SUPPORT','REFUTE','UNCERTAIN')[i%3],'status':'completed','labels':dict.fromkeys(('a','b','jev'),('SUPPORT','REFUTE','UNCERTAIN')[i%3])} for i in range(60)]
        m={'attempt':'C5-S0','status':'completed','source_hashes':{'file':'scripted'}}
        a={'attempt':'C5-S0','assigned':60,'completed':60,'starts':180,'terminal':180,'completed_calls':180,'all_payload_hashes_verified':True,'all_scores_reconstructed':True,'calls_sha256':'scripted','cost_usd':.0012}
        r={'scientific_qualification':'valid','scientific_review':'complete','assessor':'scripted-test','source_hashes':m['source_hashes'],'payload_sha256':'scripted','reviewed_miss_ids':[],'context_isolation_verified':True,'unresolved_instrument_defects':[]}
        admission={'stage':'S1','s0_scientific_hash':'scripted','scientific_hash':'scripted','projected_stage_usd':2*.0012/60*432+.001344,'spent_usd':.0433,'uncertain_usd':.001344,'incremental_spent_usd':.0024}
        return rows,m,a,r,admission
    def test_valid_chain_needs_no_new_owner_decision(self):self.assertFalse(transition(*self.good())['new_owner_approval_required'])
    def test_numeric_pass_does_not_override_contamination(self):
        x=self.good();x[3]['scientific_qualification']='invalid_label_leakage'
        with self.assertRaises(ValueError):transition(*x)
    def test_stops_on_integrity_budget_and_source_defects(self):
        for target,key,value in [(1,'status','failed'),(2,'completed_calls',179),(2,'all_payload_hashes_verified',False),(3,'context_isolation_verified',False),(3,'payload_sha256','other'),(3,'unresolved_instrument_defects',['leak']),(4,'scientific_hash','other'),(4,'spent_usd',.099),(4,'incremental_spent_usd',.029),(4,'projected_stage_usd',0)]:
            x=self.good();x[target][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):transition(*x)
    def test_misses_require_review_without_new_accuracy_gate(self):
        x=self.good();x[0][0]['labels']['a']='REFUTE';x[0][0]['labels']['b']='REFUTE'
        with self.assertRaises(ValueError):transition(*x)
        x[3]['reviewed_miss_ids']=['0'];self.assertTrue(transition(*x)['advance'])
    def test_incomplete_and_incompetent_qualification_stop(self):
        for mutate in ('missing','wrong'):
            x=self.good()
            for row in x[0][:11]:
                if mutate=='missing':row['status']='failed'
                else:row['labels']['jev']='UNCERTAIN' if row['expected']!='UNCERTAIN' else 'REFUTE'
            with self.assertRaises(ValueError):transition(*x)
if __name__=='__main__':unittest.main()
