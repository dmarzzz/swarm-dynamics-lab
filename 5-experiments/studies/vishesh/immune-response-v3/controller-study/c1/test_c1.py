import copy,importlib.util,json,os,sqlite3,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('tested_c1_run',BASE/'run.py');run=importlib.util.module_from_spec(spec);spec.loader.exec_module(run)
import cases,panel,public_reference
from native_provider import wire,validate_wire
class C1(unittest.TestCase):
    def test_panel_labels_feasibility_and_nontrivial_controls(self):
        roots=panel.build();self.assertEqual(len(roots),12);self.assertEqual(len({x['family'] for x in roots}),4)
        no_op_fails=0;always_deploy_fails=0
        for c in roots:
            state=copy.deepcopy(c['initial']);trace=[];history=[]
            for tick in (1,2):
                o=cases.observe(c,state,tick,history,[]);d=public_reference.labels(o);self.assertEqual(d,cases.diagnosis(o))
                for req in [run.candidate.diagnosis_request(o),run.candidate.action_request(c,o,d,'justification_first')]:validate_wire(wire(req,'anthropic/claude-opus-4.6'))
                a=cases.f.controller.decode(c['fixture'],public_reference.choose(o));x=cases.f.step(c['fixture'],state,a);trace.append(x);history.append({'action':a,'result':x['result']})
            self.assertTrue(cases.gate(c,trace),c['variant'])
            for constant in ('wait','deploy'):
                state=copy.deepcopy(c['initial']);o=cases.observe(c,state,1,[],[]);action=cases.f.action('wait') if constant=='wait' else cases.f.action('deploy',o['roles_to_services']['worker'],o['deployed'][o['roles_to_services']['worker']])
                t=[cases.f.step(c['fixture'],state,action) for _ in range(2)];failed=not cases.gate(c,t)
                if constant=='wait':no_op_fails+=failed
                else:always_deploy_fails+=failed
        self.assertGreater(no_op_fails,0);self.assertGreater(always_deploy_fails,0)
    def test_reference_no_hidden_or_gold_inputs(self):
        c=cases.make('worker_crash',777);o=cases.observe(c,c['initial'],1,[],[]);a=public_reference.choose(o)
        self.assertEqual(a['action_id'],'deploy:'+o['roles_to_services']['worker']+':'+str(o['deployed'][o['roles_to_services']['worker']]))
        # Hidden runtime changes cannot affect a function receiving the unchanged public view.
        c['initial']['live']['worker']=True;self.assertEqual(a,public_reference.choose(o))
        o['catalog'][o['roles_to_services']['gateway']][str(o['deployed'][o['roles_to_services']['gateway']])]['requires_rpc']='impossible'
        self.assertFalse(public_reference.labels(o)['rpc_compatible'])
    def test_exact_arm_difference_and_diagnosis_shared(self):
        c=cases.development()[0];o=cases.observe(c,c['initial'],1,[],[]);d=public_reference.labels(o);a=run.candidate.action_request(c,o,d,'action_first');b=run.candidate.action_request(c,o,d,'justification_first')
        self.assertEqual(a['observation'],b['observation']);self.assertEqual(a['response_schema']['properties'],b['response_schema']['properties']);self.assertEqual(a['instructions'].split('Serialize fields')[0],b['instructions'].split('Serialize fields')[0]);self.assertEqual(run.candidate.diagnosis_request(o),run.candidate.diagnosis_request(o))
    def test_full_scripted_packet(self):
        with tempfile.TemporaryDirectory() as td:
            s=run.execute(Path(td)/'out');self.assertEqual(s['recorded'],8);self.assertEqual(s['api_calls'],0);self.assertTrue(all(x['qualified'] for x in s['cells']));self.assertFalse(s['successor_authorized'])
    def test_wrong_order_is_manipulation_failure_before_action(self):
        class Fake:
            calls=0;actual_usd=0
            def complete(self,q,_):
                self.calls+=1;o=q['observation']
                if 'fault' in q['response_schema']['properties']:return public_reference.labels(o)
                a=public_reference.choose(o);return {k:a[k] for k in reversed(q['response_schema']['required'])}
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'out'
            with self.assertRaisesRegex(ValueError,'ordering_manipulation_failed'):run.execute(out,policy=Fake())
            s=json.loads((out/'summary.json').read_text());self.assertEqual((s['api_calls'],s['recorded'],s['incomplete'],s['unstarted']),(2,0,1,7));self.assertNotIn('"kind": "frame"',(out/'events.jsonl').read_text())
    def test_missing_native_admission_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'out'
            with self.assertRaises((TypeError,FileNotFoundError)):run.execute(out,'openrouter',None)
            self.assertFalse(out.exists())
    def test_budget_reservation_and_native_limit(self):
        ns=importlib.util.spec_from_file_location('tested_c1_native',BASE/'native.py');n=importlib.util.module_from_spec(ns);ns.loader.exec_module(n)
        with tempfile.TemporaryDirectory() as td:
            ledger=Path(td)/'budget.sqlite'
            with sqlite3.connect(ledger) as db:
                db.execute('create table budget(id integer primary key,cap real,reserved real,calls integer)');db.execute('insert into budget values(1,8,4.812055,485)')
                db.execute('create table immune_requests(request_id text primary key,run_id text,request_hash text,state text,reserved_usd real,input_tokens integer,output_tokens integer,actual_usd real,started real,ended real)')
            env={'SWARM_BUDGET_LEDGER':str(ledger),'SWARM_USAGE_LOG':str(Path(td)/'usage.jsonl'),'SWARM_MODEL_CONFIG_FILE':str(BASE.parent/'opus-config.json'),'SWARM_MODEL_BASE_URL':'http://127.0.0.1:18765','SWARM_MODEL_API_KEY':''}
            with patch.dict(os.environ,env):
                p=n.Policy()
                for _ in range(32):p.reserve(b'x'*8000)
                with self.assertRaisesRegex(ValueError,'attempt_limit'):p.reserve(b'x')
                with self.assertRaises(AssertionError):n.Policy()
            with sqlite3.connect(ledger) as db:
                cap,reserved,calls=db.execute('select cap,reserved,calls from budget').fetchone();self.assertAlmostEqual(reserved,6.583575);self.assertEqual(calls,517)
if __name__=='__main__':unittest.main()
