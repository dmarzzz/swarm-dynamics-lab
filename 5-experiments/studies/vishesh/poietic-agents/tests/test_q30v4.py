import contextlib,copy,io,json,sqlite3,sys,tempfile,threading,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import q30v4,q30v4_launch as worker,q30v4_admission as admission
from q30v4_relay import validate_payload
from common import canonical,digest
from budget import Budget
from world import World,overlap

from q30v4_pacing import Pacer
from q30v4_renewal import apply_approved_window
import q30v3

class Q30V4Tests(unittest.TestCase):
    def rehearse(self,bad=False):
        models=q30v4.models();expected={}
        for role in q30v4.ROLES:
            for case in range(12):
                state=q30v4.make_case(case,development=True);state['engine'].actors['agent-0'].model=role
                for step in range(4):
                    p=q30v4.probe(state,step,role);expected[f'Q30-04:{role}:{case}:{step}:physical-0']=(q30v4.wire(models[role],p['sections']),p['expected']);q30v4.apply(state,step,p['expected'],p['expected'])
        dispatches=[];uploads=[]
        class Provider:
            def open(self,wire,**kwargs):
                body=json.loads(wire.data);dispatches.append(body);req,action=expected[body['id']];assert req==body['request'];m=models[body['role']]
                if bad and len(dispatches)==1:action={'type':'propose','operation':'install','payload':{'steps':[]}}
                return io.BytesIO(canonical(dict(model=m['accepted_response_model_ids'][0],provider=m['provider_name'],choices=[dict(finish_reason='stop',message={'content':canonical(action)})],usage=dict(prompt_tokens=100,completion_tokens=20,cost=.00001))).encode())
        class Run:
            def __init__(self,*args):self._alive=threading.Event()
            def progress(self,*args,**kwargs):pass
            def artifact(self,path,name):uploads.append(name);return {'spooled':False}
            def done(self,**kwargs):pass
            def fail(self,**kwargs):pass
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);auth={'deadline':time.time()+3500};(root/'authority').mkdir()
            ledger=Budget(root/'authority/budget.sqlite',digest(auth),'fixture',1_500_000_000,288,auth['deadline'])
            for i in range(144):ledger.reserve('history-'+str(i),'fixture',503255302 if i==0 else 1);ledger.settle('history-'+str(i))
            ledger.close();c=root/'config.json';c.write_text(json.dumps(dict(attempt='Q30-04',prior_budget=admission.PRIOR,authorization=auth,source_commit='fixture',file_hashes={},allocation={'host':'fixture','allocated_usd_per_hour':.07143},credential={'relay_url':'http://127.0.0.1:1/invoke'},condition_tldrs={r:'OFFLINE' for r in q30v4.ROLES})))
            path=lambda p:root/'authority' if p=='/srv/swarm/poietic-agents-authority' else Path(p)
            with patch.object(worker,'verify'),patch.object(worker,'source_check'),patch.object(worker,'verify_public',return_value={}),patch.object(worker,'verify_catalog',return_value={}),patch.object(worker,'verify_relay_health'),patch.object(worker,'read_json',return_value={}),patch.object(worker.urllib.request,'build_opener',return_value=Provider()),patch.object(worker,'Path',side_effect=path),patch.object(worker,'make_case',side_effect=lambda case:q30v4.make_case(case,development=True)),patch.dict(sys.modules,{'swarm_report':SimpleNamespace(Run=Run,report=lambda *a,**k:True)}),contextlib.redirect_stdout(io.StringIO()):worker.run(c,root/'out')
            result=json.loads((root/'out/summary.json').read_text());self.assertEqual(result['terminal'],48);self.assertNotIn('records.json',uploads)
            self.assertEqual(result['budget']['physical_calls'],144+len(dispatches));return result

    def test_complete_native_loop_scripted_offline_preserves_original_history(self):
        r=self.rehearse();self.assertTrue(r['qualification_passed']);self.assertEqual(r['started'],48);self.assertFalse(r['scientific_result'])

    def test_bad_nested_payload_stops_role_and_reconciles_every_assignment(self):
        r=self.rehearse(True);self.assertFalse(r['qualification_passed']);self.assertEqual(r['started'],1);self.assertEqual(r['contracts']['cheap_generative']['schema_valid'],0)


    def test_exact_contract_fresh_manifest_and_scope(self):
        self.assertEqual(len(q30v4.assignments()),48)
        self.assertEqual(set(x['role'] for x in q30v4.assignments()),{'cheap_generative'})
        self.assertFalse({x['root'] for x in q30v4.assignments()} & {x['root'] for x in q30v3.assignments()})
        self.assertIs(q30v4.probe,q30v3.probe)
        self.assertIs(q30v4.Swarm,q30v3.Swarm)
        self.assertIs(q30v4.wire,q30v3.wire)
        self.assertIs(q30v4.apply,q30v3.apply)
        self.assertEqual(q30v4.models(),q30v3.models())
        c=admission.candidate()
        self.assertEqual(c['pi_stage_allocation']['api_usd'],.01867776)
        self.assertEqual(c['maximum_new_calls'],48)
        with self.assertRaises(ValueError):admission.verify(c,actual_host='sim-vishesh')
        c['minimum_dispatch_interval_s']=0
        with self.assertRaisesRegex(ValueError,'pi_paced_stage_scope'):admission.verify(c,actual_host='sim-vishesh')
        req=q30v4.wire(q30v4.models()['generalist'],[{'development':True}])
        with self.assertRaises(ValueError):validate_payload(dict(id='Q30-04:generalist:0:0:physical-0',role='generalist',request=req),q30v4.models())

    def test_pacing_accounts_for_latency_early_wake_and_deadline(self):
        clock=[0.0];sleeps=[]
        def sleep(n):sleeps.append(n);clock[0]+=n/2 if n>.001 else n
        p=Pacer(clock=lambda:clock[0],wall=lambda:100+clock[0],sleep=sleep)
        p.wait(200);self.assertEqual(p.last,0)
        clock[0]=1;p.wait(200);self.assertGreaterEqual(p.last,5)
        clock[0]=11;p.wait(200);self.assertEqual(p.last,11)
        with self.assertRaisesRegex(ValueError,'paced_dispatch_deadline'):p.wait(115)
        self.assertEqual(p.last,11)

    def test_one_use_time_amendment_preserves_all_original_rows_and_caps(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/'budget.sqlite';now=time.time()
            auth=dict(study='poietic-agents',stage='S0',deadline=now-1,physical_call_cap=288,api_cap_usd=1.5)
            db=sqlite3.connect(path)
            db.executescript('CREATE TABLE authority(id INTEGER PRIMARY KEY,hash TEXT,host TEXT,cap INTEGER,calls INTEGER,deadline REAL); CREATE TABLE charges(id TEXT PRIMARY KEY,request_hash TEXT,reserve INTEGER,settled INTEGER,status TEXT,created REAL);')
            old=(digest(auth),'sim-vishesh',1500000000,288,now-1)
            db.execute('INSERT INTO authority VALUES(1,?,?,?,?,?)',old)
            rows=[(str(i),'fixture',503255302 if i==0 else 1,None,'uncertain',now-100) for i in range(144)]
            db.executemany('INSERT INTO charges VALUES(?,?,?,?,?,?)',rows);db.commit()
            history=db.execute('SELECT * FROM charges ORDER BY id').fetchall()
            receipt=dict(schema_version=1,study='poietic-agents',attempt='Q30-04',approved=True,duration_seconds=900,maximum_new_calls=48,receipt_id='OFFLINE',decision_reference='OFFLINE',approved_at=now,quiescence_checked_at=now,workers_and_relays_stopped=True,quiescence_reference='OFFLINE',old_authorization=auth,expected_authority=dict(zip(('hash','host','cap','calls','deadline'),old)),charges_sha256=digest(history),expected_charge_count=144,exclusive_approved_account_allocation=True,source_commit='0'*40,plan_sha256='0'*64,pi_decision='PI-FUND-20261004-01',allocation_started_at=now)
            for delta in ({'maximum_new_calls':49},{'pi_decision':'wrong'},{'allocation_started_at':now-600},{'charges_sha256':'0'*64}):
                with self.assertRaises(ValueError):apply_approved_window(path,dict(receipt,**delta),now=now)
            result=apply_approved_window(path,receipt,now=now)
            self.assertEqual(result['authorization'],dict(auth,deadline=now+900))
            self.assertEqual(db.execute('SELECT * FROM charges ORDER BY id').fetchall(),history)
            self.assertEqual(db.execute('SELECT cap,calls FROM authority').fetchone(),(1500000000,288))
            with self.assertRaises(ValueError):apply_approved_window(path,receipt,now=now)
            db.close()

if __name__=='__main__':unittest.main()
