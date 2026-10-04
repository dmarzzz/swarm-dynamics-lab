import copy,json,sys,unittest
from pathlib import Path
S=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(S/'src'),str(S/'analysis')]
from dossier import build,evaluate
from study import run,reference_decision,cost_worksheet
from run import Scripted
from paired import analyze

class IterationTests(unittest.TestCase):
    def cases(self):
        return [build(c['family'],i,c['world'],seed=37,dossier_spec=c) for i,c in enumerate(json.loads((S/'qualification-v2.json').read_text())['cases'])]
    def test_new_dossiers_choose_or_defer_for_named_reasons(self):
        cases=self.cases()
        for i,c in enumerate(cases):
            a=reference_decision({'brief':c['brief'],'documents':c['documents'],'candidates':c['candidates']})
            expected=list(c['evaluator']['products'])[[1,0,0,1][i]] if i!=2 else 'DEFER'
            self.assertEqual(a['choice'],expected)
            self.assertEqual(evaluate(c,a)['acceptable_decision'],1)
        c=cases[3];target=c['evaluator']['target'];r=evaluate(c,{'choice':target,'annual_total_usd':None})
        self.assertEqual(set(r['constraint_violations']),{'deployment_scope','rollout_deadline'})
        self.assertEqual(evaluate(c,{'choice':'DEFER','annual_total_usd':None})['avoidable_deferral'],1)
    def test_qualifier_is_not_just_a_profile_change(self):
        for c in self.cases():
            old=build(c['family'],c['profile'],c['world'],seed=37)
            self.assertNotEqual(c['evaluator']['products'],old['evaluator']['products'])
            obs={'brief':c['brief'],'documents':c['documents'],'candidates':c['candidates']}
            for r in cost_worksheet(obs):
                e=evaluate(c,{'choice':r['candidate'],'annual_total_usd':r['total_usd']})
                self.assertEqual(e['cost_claim_error_usd'],0)
            self.assertIn('$'+str(c['brief']['human_cost_per_unresolved_ticket']),next(d['text'] for d in c['documents'] if d['id']=='workload'))
    def test_missing_pair_is_unidentified_not_zero(self):
        rows=run(build('usage_cliff'),Scripted())['outcomes']
        p=analyze(rows)['pairs'][0]
        self.assertFalse(p['identified']);self.assertEqual(p['contrast_bounds'],[-1,1])
    def test_valid_zero_and_invalid_bounds_are_distinct(self):
        rows=[]
        for w in ('clean','omission'):rows+=run(build('usage_cliff',world=w),Scripted())['outcomes']
        self.assertEqual(analyze(rows)['pairs'][0]['contrast_bounds'],[0,0])
        broken=copy.deepcopy(rows);broken[0]['valid']=False;broken[0]['evaluation']=None
        self.assertFalse(analyze(broken)['pairs'][0]['identified'])
        with self.assertRaises(ValueError):analyze(rows+rows[:1])
    def test_gate_rejects_targeted_or_incomplete_qualification(self):
        from native import qualification_gate
        q=dict(stage='Q4',qualified=True,source_signature='frozen',planned=12,terminal=12,valid=12,acceptable=12,invalid=0)
        qualification_gate(q,'frozen')
        for key,value in [('stage','Q3'),('acceptable',11),('source_signature','old'),('qualified',False),('invalid',1)]:
            bad={**q,key:value}
            with self.assertRaises(ValueError):qualification_gate(bad,'frozen')
    def test_case_file_is_part_of_source_signature(self):
        from native import signature
        self.assertEqual(len(signature({'model':'fixture'})),64)

if __name__=='__main__':unittest.main()
