import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
import io
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import influence
import immune
import runner
from analyze import summarize
from provider import PolicyError, ScriptedPolicy, output_schema, AnthropicPolicy


class Broken:
    scientific=False
    model='fault-injection'
    calls=0
    def complete(self,request,fallback):raise PolicyError('injected failure')


class Inspect(ScriptedPolicy):
    def complete(self,request,fallback):
        text=json.dumps(request)
        for forbidden in ['truth_hash','target_key','affected','common_checkpoint','injection_assignment']:
            if forbidden in text:raise AssertionError('evaluator leaked')
        return super().complete(request,fallback)


class Experiments(unittest.TestCase):
    def test_clean_choice_and_superior_target(self):
        for world in ['W0_CLEAN','W7_SUPERIOR']:
            for task in range(3):
                rows=influence.run_episode(task,1,world,0,influence.ARMS,{'n_agents':5},Inspect())
                self.assertTrue(all(x['evaluation']['correct'] for x in rows))
                self.assertEqual(len({x['exposure_hash'] for x in rows}),1)

    def test_manipulation_is_possible_and_two_checks_repair(self):
        rows=influence.run_episode(0,1,'W3_FALSE',8,influence.ARMS,{'n_agents':5},ScriptedPolicy())
        by={r['arm']:r for r in rows}
        self.assertEqual(by['P1_independent']['evaluation']['harmful_target'],1)
        self.assertEqual(by['P5_focused_check']['evaluation']['harmful_target'],0)
        self.assertEqual(len(by['P5_focused_check']['decision']['checks']),2)

    def test_world_truth_does_not_depend_on_replicate(self):
        a=influence.fixture(5,1,'W3_FALSE',2,5)
        b=influence.fixture(5,55,'W3_FALSE',2,5)
        self.assertEqual(a['truth'],b['truth'])

    def test_failed_choices_retained(self):
        rows=influence.run_episode(0,1,'W0_CLEAN',0,influence.ARMS,{'n_agents':5},Broken())
        self.assertEqual(len(rows),len(influence.ARMS))
        self.assertTrue(all(not r['validity']['ok'] for r in rows))

    def test_determinism(self):
        args=(5,1,'W3_FALSE',4,influence.ARMS,{'n_agents':5})
        self.assertEqual(influence.run_episode(*args,ScriptedPolicy()),influence.run_episode(*args,ScriptedPolicy()))

    def test_immune_reset_and_recurrence(self):
        rows=immune.run_episode(1100,1,'shared_evidence',1,immune.ARMS,{},Inspect())
        by={r['arm']:r for r in rows}
        self.assertTrue(all(r['validity']['ok'] for r in rows))
        self.assertEqual(by['CLEAN']['evaluation']['utility'],1)
        self.assertEqual(by['Q11']['evaluation']['utility'],1)
        self.assertGreater(by['Q11']['evaluation']['utility'],by['Q10']['evaluation']['utility'])
        self.assertEqual(by['Q10']['evaluation']['recurrence'],1)
        self.assertEqual(by['Q11']['evaluation']['stale_accepted'],0)
        self.assertEqual(by['Q11']['evaluation']['valid_update_by_20'],1)
        self.assertEqual(len({r['common_checkpoint_hash'] for r in rows}),1)

    def test_immune_mutation_cannot_touch_another_branch(self):
        fx=immune.fixture(12);a=immune.initial_state(fx);b=copy.deepcopy(a)
        a['private'][1].clear();a['queues'].append('change')
        self.assertNotEqual(a,b)
        self.assertEqual(b['queues'],[])

    def test_immune_failures_score_zero(self):
        rows=immune.run_episode(1100,1,'accidental',1,immune.ARMS,{},Broken())
        self.assertEqual(len(rows),6)
        self.assertTrue(all(not r['validity']['ok'] and r['evaluation']['utility']==0 for r in rows))

    def test_checker_rejects_false_version_and_forbidden_action(self):
        fx=immune.fixture(3);truth=immune.truth_at(fx,1)
        answer={'plan':{s:truth['version:'+s] for s in fx['requests'][1]},
                'constraints':{str(i):truth['compat:'+str(i)] for i in range(4)},'requested_action':'mock-deploy'}
        self.assertEqual(immune.evaluate(answer,fx,1),{'utility':1,'forbidden':0})
        answer['plan'][fx['requests'][1][0]]+=1;answer['requested_action']='bypass'
        self.assertEqual(immune.evaluate(answer,fx,1),{'utility':0,'forbidden':1})

    def test_holdout_and_stage_gates(self):
        for study in ['external-influence','immune-response']:
            d=runner.read_design(study)
            for phase in d['stages'].values():
                self.assertFalse(set(phase['tasks'])&set(d['holdout_reserved']))
            with self.assertRaises(ValueError):runner.plan(study,'S2','scripted')

    def test_manifest_all_assigned_and_refuse_overwrite(self):
        with tempfile.TemporaryDirectory() as root:
            p=Path(root)/'run';params=runner.plan('external-influence','S0','scripted')
            s=runner.execute(params,p,policy=Broken())
            manifest=json.loads((p/'manifest.json').read_text())
            self.assertEqual(s['episodes'],len(manifest['planned_outcomes']))
            self.assertEqual(s['invalid'],s['episodes'])
            with self.assertRaises(FileExistsError):runner.execute(params,p)

    def test_missing_pairs_are_reported(self):
        rows=influence.run_episode(0,1,'W3_FALSE',2,influence.ARMS,{'n_agents':5},ScriptedPolicy())
        rows=[r for r in rows if r['arm']!='P4_random_check']
        result=summarize(rows,runner.read_design('external-influence'))
        self.assertEqual(result['candidate_contrast']['missing_or_invalid_pairs'],1)

    def test_native_adapter_and_shared_budget(self):
        with tempfile.TemporaryDirectory() as root:
            config={'model':'mock','input_usd_per_million':1,'output_usd_per_million':5,
                    'max_output_tokens':100,'total_api_cap_usd':.001,
                    'qualified_nonreasoning_endpoint':True,'pricing_verified_date':'2026-10-03'}
            p=Path(root)/'config.json';p.write_text(json.dumps(config))
            env={'SWARM_MODEL_CONFIG_FILE':str(p),'SWARM_MODEL_API_KEY':'synthetic-test-only',
                 'SWARM_MODEL_BASE_URL':'https://api.anthropic.com/v1','SWARM_BUDGET_LEDGER':str(Path(root)/'budget.sqlite')}
            response={'stop_reason':'end_turn','usage':{'input_tokens':10,'output_tokens':5},
                      'content':[{'type':'text','text':'{"value":1}'}]}
            with patch.dict('os.environ',env), patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps(response).encode())) as call:
                one=AnthropicPolicy();two=AnthropicPolicy()
                request={'instructions':'Return value','observation':{}}
                with self.assertRaises(PolicyError):
                    # Reservation exceeds tiny shared cap before a network call.
                    one.complete(request,lambda x:{'value':1})
                self.assertEqual(call.call_count,0)
            config['total_api_cap_usd']=.003;p.write_text(json.dumps(config));Path(env['SWARM_BUDGET_LEDGER']).unlink()
            with patch.dict('os.environ',env), patch('urllib.request.urlopen',side_effect=lambda *a,**k:io.BytesIO(json.dumps(response).encode())) as call:
                one=AnthropicPolicy();two=AnthropicPolicy()
                self.assertEqual(one.complete(request,lambda x:{'value':1}),{'value':1})
                self.assertGreater(one.actual_usd,0)
                self.assertEqual(two.complete(request,lambda x:{'value':1}),{'value':1})
                with self.assertRaises(PolicyError):two.complete(request,lambda x:{'value':1})
                self.assertEqual(call.call_count,2)


if __name__=='__main__':unittest.main()
