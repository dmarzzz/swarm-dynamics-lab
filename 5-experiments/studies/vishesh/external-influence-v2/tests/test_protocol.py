import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from environment import fixture, choose, parse_document, utility
from protocol import run_arm, ARMS, scripted, validate_report
from provider import ScriptedPolicy, PolicyError, output_schema
from runner import plan
from analyze import summarize

def condition(**kw):
    return dict(domain='procurement',task_id=0,seed=17,world='clean',dose=0,n_agents=9,verification='fresh',**kw)

def draw(**kw):
    c=condition();c.update(kw);return c

class Tests(unittest.TestCase):
    def test_live_request_envelopes(self):
        class Bounded:
            def complete(self,request,fallback):
                answer=fallback(request['observation'])
                body={'model':'claude-haiku-4-5-20251001','system':request['instructions'],'temperature':0,
                      'max_tokens':1024,'messages':[{'role':'user','content':json.dumps(request['observation'],sort_keys=True)}],
                      'output_config':{'format':{'type':'json_schema','schema':output_schema(answer)}}}
                if len(json.dumps(body).encode())>12000:raise AssertionError('request bound exceeded')
                return answer
        for a in plan('S0','anthropic')['assignments']+plan('S1','anthropic')['assignments']:
            r=run_arm({k:v for k,v in a.items() if k!='arm'},a['arm'],Bounded())
            self.assertTrue(r['validity']['ok'],a)

    def test_pairing_and_variation(self):
        for domain in ('procurement','dependency','travel'):
            a=fixture(domain,0,17,'clean',0);b=fixture(domain,0,18,'misleading',8)
            self.assertEqual(a['truth_hash'],b['truth_hash']);self.assertNotEqual(a['corpus_hash'],b['corpus_hash'])
            self.assertNotEqual(a['truth_hash'],fixture(domain,1,17,'clean',0)['truth_hash'])
            for d in a['documents']:
                for n,v in parse_document(d,a['brief']).items():
                    for k in ['cost','quality','latency']:self.assertAlmostEqual(v[k],a['truth'][n][k],places=2)
    def test_clean_and_superior(self):
        for domain in ('procurement','dependency','travel'):
            for world in ('clean','superior'):
                for arm in ARMS:
                    r=run_arm(draw(domain=domain,world=world,dose=8),arm,ScriptedPolicy())
                    self.assertTrue(r['validity']['ok']);self.assertEqual(r['evaluation']['correct'],1)
                    self.assertEqual(r['call_slots'],15)
    def test_blindness_and_no_cross_arm_mutation(self):
        events=[];a=run_arm(draw(world='misleading',dose=8),'targeted_check',ScriptedPolicy(),events.append)
        b=run_arm(draw(world='misleading',dose=8),'targeted_check',ScriptedPolicy())
        self.assertEqual(a['choice'],b['choice']);self.assertEqual(a['exposure_hash'],b['exposure_hash'])
        for event in events:
            if event['kind']=='request':
                serialized=json.dumps(event)
                for key in ('truth_hash','best','target','modified_documents'):
                    self.assertNotIn('"'+key+'":',serialized)
    def test_manipulation_and_checks(self):
        failures=0;repairs=0
        for task in range(8):
            c=draw(task_id=task,world='misleading',dose=12)
            a=run_arm(c,'discussion',ScriptedPolicy());b=run_arm(c,'targeted_check',ScriptedPolicy())
            failures+=a['evaluation']['harmful_target'];repairs+=a['evaluation']['harmful_target'] and not b['evaluation']['harmful_target']
        self.assertGreater(failures,0);self.assertGreater(repairs,0)
    def test_unavailable_and_stale_do_not_oracle_repair(self):
        for mode in ('stale','unavailable'):
            r=run_arm(draw(world='misleading',dose=12,verification=mode),'targeted_check',ScriptedPolicy())
            self.assertTrue(r['validity']['ok']);self.assertEqual(r['evaluation']['available_checks'],0)
            self.assertEqual(r['evaluation']['harmful_target'],1)
    def test_call_matching(self):
        for n in (5,9):
            for arm in ARMS:self.assertEqual(run_arm(draw(n_agents=n),arm,ScriptedPolicy())['call_slots'],2*(n-3)+3)
    def test_failures_remain_assigned(self):
        class Broken:
            def complete(self,*a):raise PolicyError('test')
        r=run_arm(draw(),'random_check',Broken());s=summarize([r])
        self.assertEqual(s['invalid'],1);self.assertEqual(s['cells'][0]['harmful_target_all_assigned_bounds'],[0,1])
    def test_forged_citation_and_nonfinite_rejected(self):
        data=fixture('procurement',0,17,'clean',0)
        o={'brief':data['brief'],'documents':data['allocations'][0]};a=scripted(o)
        a['estimates'][0]['citations']=['forged']
        with self.assertRaises(PolicyError):validate_report(a,data['brief'],{'doc-00'})
        a=scripted(o);a['estimates'][0]['cost']=float('nan')
        with self.assertRaises(PolicyError):validate_report(a,data['brief'],{d['id'] for d in o['documents']})
    def test_splits_and_bounded_live_plan(self):
        assignments=plan('S0','anthropic')['assignments']+plan('S1','anthropic')['assignments']
        self.assertTrue(all(a['task_id']<9000 for a in assignments));self.assertEqual(len(assignments),54)
        self.assertEqual(sum(2*(a['n_agents']-3)+3 for a in assignments),810)
        self.assertLess(810*.017632+30.432064,45)
        with self.assertRaises(ValueError):plan('S2','anthropic')
        with self.assertRaises(ValueError):plan('engineering','anthropic')
    def test_analysis_never_pools_domains_or_invents_ci(self):
        rows=[run_arm(draw(domain=d,world='misleading',dose=8),a,ScriptedPolicy()) for d in ('procurement','dependency','travel') for a in ('random_check','targeted_check')]
        s=summarize(rows)
        self.assertEqual(len(s['contrasts']),3)
        self.assertTrue(all(c['tasks']==1 and c['ci95'] is None for c in s['contrasts']))

if __name__=='__main__':unittest.main()
