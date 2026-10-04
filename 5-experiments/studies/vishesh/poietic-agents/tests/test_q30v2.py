import contextlib,copy,io,json,sqlite3,sys,tempfile,threading,time,unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
import q30v2,q30v2_launch as worker,q30v2_admission as admission
from q30v2_relay import validate_payload
from common import canonical,digest
from budget import Budget
from world import World,overlap

class Q30V2Tests(unittest.TestCase):
    def test_thirty_uniform_actors_balanced_overlap_and_separate_cohorts(self):
        e=q30v2.Swarm(World(0));self.assertEqual(len(e.actors),30)
        defs=[{k:v for k,v in a.definition().items() if k!='id'} for a in e.actors.values()]
        self.assertTrue(all(d==defs[0] for d in defs))
        for epoch,expected in [(1,24),(5,0)]:
            jobs=q30v2.workload(0,epoch,'overlap_shift');m=overlap(jobs,e.world)
            self.assertEqual(len(jobs),30);self.assertEqual(m['repeated_occurrences'],expected)
        self.assertEqual(len(q30v2.assignments()),96)
        self.assertFalse({x['root'] for x in q30v2.assignments()} & {300,400,404,408,500,504,508,700,701,702,703})

    def test_explicit_contract_reference_steps_and_route_parameter_boundary(self):
        models=q30v2.models()
        for role in q30v2.ROLES:
            for case in range(12):
                state=q30v2.make_case(case,development=True)
                for step in range(4):
                    p=q30v2.probe(state,step,role);req=q30v2.wire(models[role],p['sections'])
                    self.assertLessEqual(len(canonical(req)),7500)
                    envelope=dict(id=f'Q30-02:{role}:{case}:{step}:physical-0',role=role,request=req)
                    self.assertEqual(validate_payload(envelope,models),models[role])
                    with self.assertRaises(ValueError):validate_payload(envelope,models,'D0-02')
                    with self.assertRaises(ValueError):validate_payload(dict(envelope,id=envelope['id'][:-1]+'1'),models)
                    self.assertTrue(q30v2.apply(state,step,p['expected'],p['expected'])['correct'])
        req=q30v2.wire(models['generalist'],[{'test':'development'}]);self.assertEqual(req['temperature'],0);self.assertEqual(req['reasoning'],{'effort':'low'})

    def test_saved_failure_shapes_rejected_instead_of_counted_as_valid(self):
        s=q30v2.make_case(1,development=True)
        wrong=dict(type='propose',operation='register_service',payload={'provider':'self','name':'data','endpoint':'inventory','capacity':2})
        self.assertFalse(q30v2.apply(s,3,wrong,wrong)['schema_valid']);self.assertFalse(s['engine'].services)
        with self.assertRaises(ValueError):s['engine'].dispatch('agent-0',dict(type='answer',value={'entity_ids':[]},receipts=[]),s['job'])
        with self.assertRaises(ValueError):q30v2.validate_action(dict(type='propose',operation='install',payload={'procedure':'normalized','steps':[]}))

    def test_non_authorizing_candidate_and_faulted_admission(self):
        c=admission.candidate();now=time.time()
        with self.assertRaises(ValueError):admission.verify(c,actual_host='sim-vishesh')
        c['owner_update_approval'].update(approved=True,decision_reference='OFFLINE')
        c['authorization']=dict(study='poietic-agents',stage='S0',owner_approved=True,reference='OFFLINE',api_cap_usd=1.5,infrastructure_cap_usd=.5,total_cumulative_cap_usd=2,physical_call_cap=288,deadline=now+3500)
        c['allocation']=dict(host='sim-vishesh',experiment='poietic-agents',operator='vishesh/codex-heterogeneous',exclusive=True,registered_fleet_destination=True,workload_idle=True,approved_account_verified=True,claim_id='OFFLINE',merged_claim_revision='0'*40,host_key_provenance='OFFLINE',checked_at=now,expires_at=now+7200,allocated_usd_per_hour=.07143,charge_started_at=now)
        c['credential']=dict(alias='swarm-lab-openrouter',study_authorized=True)
        url='https://github.com/dmarzzz/swarm-lab/blob/'+'0'*40+'/P30-PLAN.md';c['public_plan']=dict(url=url,sha256=c['proposal_sha256']);c['page_verification']=dict(url=url,rendered=True,checked_at=now)
        self.assertTrue(admission.verify(c,now=now,actual_host='sim-vishesh')['ready'])
        for section,field,value in [('prior_budget','physical_calls',0),('allocation','host','other'),('allocation','checked_at',now-301),('allocation','exclusive',False),('authorization','api_cap_usd',9.25),('owner_update_approval','approved',False),('public_plan','sha256','0'*64)]:
            bad=copy.deepcopy(c);bad[section][field]=value
            with self.subTest(field=field),self.assertRaises(ValueError):admission.verify(bad,now=now,actual_host='sim-vishesh')

    def rehearse(self,bad=False):
        models=q30v2.models();expected={}
        for role in q30v2.ROLES:
            for case in range(12):
                state=q30v2.make_case(case,development=True);state['engine'].actors['agent-0'].model=role
                for step in range(4):
                    p=q30v2.probe(state,step,role);expected[f'Q30-02:{role}:{case}:{step}:physical-0']=(q30v2.wire(models[role],p['sections']),p['expected']);q30v2.apply(state,step,p['expected'],p['expected'])
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
            for i in range(79):ledger.reserve('history-'+str(i),'fixture',499330443 if i==0 else 1);ledger.settle('history-'+str(i))
            ledger.close();c=root/'config.json';c.write_text(json.dumps(dict(attempt='Q30-02',prior_budget=admission.PRIOR,authorization=auth,source_commit='fixture',file_hashes={},allocation={'host':'fixture','allocated_usd_per_hour':.07143},credential={'relay_url':'http://127.0.0.1:1/invoke'},condition_tldrs={r:'OFFLINE' for r in q30v2.ROLES})))
            path=lambda p:root/'authority' if p=='/srv/swarm/poietic-agents-authority' else Path(p)
            with patch.object(worker,'verify'),patch.object(worker,'source_check'),patch.object(worker,'verify_public',return_value={}),patch.object(worker,'verify_catalog',return_value={}),patch.object(worker,'verify_relay_health'),patch.object(worker,'read_json',return_value={}),patch.object(worker.urllib.request,'build_opener',return_value=Provider()),patch.object(worker,'Path',side_effect=path),patch.object(worker,'make_case',side_effect=lambda case:q30v2.make_case(case,development=True)),patch.dict(sys.modules,{'swarm_report':SimpleNamespace(Run=Run,report=lambda *a,**k:True)}),contextlib.redirect_stdout(io.StringIO()):worker.run(c,root/'out')
            result=json.loads((root/'out/summary.json').read_text());self.assertEqual(result['terminal'],96);self.assertNotIn('records.json',uploads)
            self.assertEqual(result['budget']['physical_calls'],79+len(dispatches));return result

    def test_complete_native_loop_scripted_offline_preserves_original_history(self):
        r=self.rehearse();self.assertTrue(r['qualification_passed']);self.assertEqual(r['started'],96);self.assertFalse(r['scientific_result'])

    def test_bad_nested_payload_stops_role_and_reconciles_every_assignment(self):
        r=self.rehearse(True);self.assertFalse(r['qualification_passed']);self.assertEqual(r['started'],49);self.assertEqual(r['contracts']['generalist']['schema_valid'],0)

if __name__=='__main__':unittest.main()
