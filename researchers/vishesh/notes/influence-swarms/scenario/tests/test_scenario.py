import copy
import json
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from dossier import FAMILIES,WORLDS,build,costs,evaluate,verification
from study import reference_decision,run,validate
from run import Scripted

class ScenarioTests(unittest.TestCase):
    def test_worksheet_uses_visible_sources_without_recommendation(self):
        from study import cost_worksheet
        c=build('usage_cliff',5)
        obs={'brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']}
        rows=cost_worksheet(obs)
        self.assertEqual(len(rows),3)
        for r in rows:
            self.assertFalse(set(r)&{'choice','eligible','acceptable','target'})
            self.assertEqual(r['total_usd'],costs(c['brief'],c['evaluator']['products'][r['candidate']])['total'])
        obs['documents']=c['allocations'][0];self.assertEqual(cost_worksheet(obs),[])
    def test_native_schema_matches_confidence_and_citation_contract(self):
        from native import ScenarioPolicy
        from study import scripted
        policy=ScenarioPolicy.__new__(ScenarioPolicy)
        c=build('usage_cliff',6)
        for phase in ('initial','chair'):
            obs={'phase':phase,'brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']}
            s=policy.schema({'observation':obs},scripted)['properties']
            self.assertEqual(s['confidence']['type'],'number')
            self.assertEqual(s['choice']['enum'],c['candidates']+['DEFER'])
            ids=s['findings']['items']['properties']['citations']['items']['enum'] if phase=='initial' else s['citations']['items']['enum']
            self.assertEqual(ids,[d['id'] for d in c['documents']])
    def test_sensitivity_is_visible(self):
        from sensitivity import audit
        a=audit();self.assertEqual(a['cases'],24);self.assertGreater(a['sensitivity_dependent'],0)
    def test_worlds_change_only_comparison_text(self):
        for family in FAMILIES:
            for profile in range(4):
                clean=build(family,profile)
                for world in WORLDS:
                    other=build(family,profile,world)
                    self.assertEqual(clean['evaluator'],other['evaluator'])
                    self.assertEqual(clean['brief'],other['brief'])
                    self.assertEqual([d for d in clean['documents'] if d['kind']!='comparison'],[d for d in other['documents'] if d['kind']!='comparison'])
                    self.assertEqual(len(other['documents']),16)
    def test_reference_uses_documents_and_matches_evaluator(self):
        labels=set()
        for family in FAMILIES:
            for profile in range(4):
                c=build(family,profile,'syndication');obs={'brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']}
                answer=reference_decision(obs);self.assertEqual(evaluate(c,answer)['acceptable_decision'],1)
                labels.add(answer['choice'])
        self.assertGreaterEqual(len(labels-{'DEFER'}),2)
    def test_manual_cost_example(self):
        b={'complex_share':.5,'monthly_tickets':100,'seats':2,'human_cost_per_unresolved_ticket':8}
        p={'simple':.8,'complex':.4,'seat':10,'outcome':1,'setup':100}
        v=costs(b,p);self.assertAlmostEqual(v['automation'],.6);self.assertEqual(v['software'],1060);self.assertEqual(v['human'],3840);self.assertEqual(v['total'],4900)
    def test_missing_scope_is_not_false_certainty(self):
        c=build('evidence_gap');a=reference_decision({'brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']})
        self.assertEqual(a['choice'],'DEFER');self.assertEqual(evaluate(c,a)['avoidable_deferral'],0)
    def test_genuine_value_does_not_reward_blanket_rejection(self):
        for i in range(4):
            c=build('genuine_value',i);a=reference_decision({'brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']})
            self.assertEqual(a['choice'],c['evaluator']['target']);self.assertEqual(evaluate(c,a)['harmful_target'],0)
    def test_named_constraints(self):
        for family,reason in [('residency_scope','deployment_scope'),('migration_deadline','rollout_deadline')]:
            c=build(family);e=evaluate(c,{'choice':c['evaluator']['target'],'annual_total_usd':None})
            self.assertIn(reason,e['constraint_violations']);self.assertIsNone(e['cost_regret_usd'])
    def test_partial_dossier_does_not_get_hidden_facts(self):
        c=build('usage_cliff');self.assertEqual(reference_decision({'brief':c['brief'],'candidates':c['candidates'],'documents':c['allocations'][0]})['choice'],'DEFER')
    def test_checks_retrieve_actual_records(self):
        c=build('usage_cliff');d=verification(c,{'candidate':c['candidates'][0],'kind':'scope'});self.assertIn(d,c['documents'])
        with self.assertRaises(ValueError):verification(c,{'candidate':c['candidates'][0],'kind':'truth'})
    def test_forks_share_facts_but_not_votes(self):
        r=run(build('usage_cliff'),Scripted());self.assertEqual(r['calls'],14);self.assertEqual(len(r['outcomes']),3)
        chairs=[e['request']['observation'] for e in r['events'] if e['kind']=='request' and e['request']['observation']['phase']=='chair']
        a,b=chairs[:2];self.assertEqual(a['documents'],b['documents']);self.assertEqual(a['checks'],b['checks'])
        for p,q in zip(a['reports'],b['reports']):self.assertEqual({k:v for k,v in p.items() if k not in ('choice','confidence')},q)
        for e in r['events']:
            if e['kind']=='request':
                obs=e['request']['observation'];self.assertFalse(set(obs)&{'evaluator','target','family','world','acceptable','scorecard'})
    def test_outcome_is_not_overwritten(self):
        c=build('migration_deadline');target=c['evaluator']['target']
        class Wrong(Scripted):
            def complete(self,request,fallback):
                a=super().complete(request,fallback)
                if request['observation']['phase']=='chair':a['choice']=target
                return a
        r=run(c,Wrong());self.assertTrue(all(x['decision']['choice']==target for x in r['outcomes']));self.assertTrue(all(not x['evaluation']['acceptable_decision'] for x in r['outcomes']))
    def test_prefix_failure_keeps_denominator(self):
        class Broken:
            def complete(self,*a):raise RuntimeError('fixture failure')
        r=run(build('usage_cliff'),Broken());self.assertEqual(len(r['outcomes']),3);self.assertTrue(all(not x['valid'] for x in r['outcomes']))
    def test_forged_and_nonfinite_output_rejected(self):
        c=build('usage_cliff');o={'phase':'chair','brief':c['brief'],'candidates':c['candidates'],'documents':c['documents']};a=reference_decision(o)
        for key,value in [('confidence',float('nan')),('annual_total_usd',float('inf')),('citations',['invented'])]:
            bad=copy.deepcopy(a);bad[key]=value
            with self.assertRaises(ValueError):validate(bad,o)
    def test_all_reports_fit_initial_envelope(self):
        r=run(build('genuine_value',3,'syndication'),Scripted())
        self.assertLess(max(len(json.dumps(e['request']).encode()) for e in r['events'] if e['kind']=='request'),24576)

if __name__=='__main__':unittest.main()
