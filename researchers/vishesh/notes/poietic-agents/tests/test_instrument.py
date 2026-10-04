import copy
import json
import sys
import tempfile
import time
import unittest
from pathlib import Path

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from common import digest, stream_seed
from world import World, job, jobs, normalize, overlap
from engine import Engine, released_jobs, prefix_accounting
from evaluator import reference, grade, summarize
from operators import execute, used_parameters
from budget import Budget
from native import request, response, reserve_nano, verify_catalog
from qualification import ROLES, assignments, make_case, probe, apply, analyze
from admission import inventory, verify, verify_public
from render import qualification_frame, replay

class KnownWorld(World):
    def fetch(self,endpoint,entity,epoch):
        data={'inventory':[dict(entity_id=entity,available=9,reserved=2)],
              'supplier_terms':[dict(entity_id=entity,supplier='a',unit_cents=30,capacity=12,lead_days=2),dict(entity_id=entity,supplier='b',unit_cents=20,capacity=4,lead_days=3)],
              'delivery_status':[dict(entity_id=entity,expected=10,received=7,due_day=2),dict(entity_id=entity,expected=8,received=0,due_day=5)]}[endpoint]
        p=dict(endpoint=endpoint,entity_id=entity,schema_version=1,source_version=(epoch-1)//2+1,valid_from_epoch=((epoch-1)//2)*2+1,expires_after_epoch=((epoch-1)//2)*2+2,rows=data)
        p['receipt']=digest(p);return p

class InstrumentTests(unittest.TestCase):
    def setUp(self): self.w=KnownWorld(0);self.e=Engine(self.w);self.j=job(0,1,0,'sku-x');self.j['quantity']=5
    def test_hand_computed_answers(self):
        p=self.w.fetch('supplier_terms','sku-x',1)
        self.assertEqual(reference(self.j,[p]),{'supplier':'a','total_cents':150})
        self.j['quantity']=3
        self.assertEqual(reference(self.j,[p]),{'supplier':'b','total_cents':60})
        self.j['quantity']=99
        self.assertEqual(reference(self.j,[p]),{'supplier':None,'total_cents':0})
        self.j['kind']='exceptions';self.j['threshold']=8
        self.assertEqual(reference(self.j,[self.w.fetch('inventory','sku-x',1)]),['sku-x'])
        self.j['kind']='reconcile'
        self.assertEqual(reference(self.j,[self.w.fetch('delivery_status','sku-x',1)]),3)
    def test_stale_correct_fails(self):
        p=self.e.fetch('agent-0','supplier_terms',['sku-x'],1)[0]
        self.j['epoch']=3
        score=grade(self.j,{'value':{'supplier':'a','total_cents':150},'receipts':[p['receipt']]},self.w,self.e.actors['agent-0'].issued,10)
        self.assertTrue(score['correct']);self.assertFalse(score['fresh']);self.assertFalse(score['success'])
    def test_unissued_receipt_fails(self):
        p=self.w.fetch('supplier_terms','sku-x',1)
        self.assertFalse(grade(self.j,{'value':reference(self.j,[p]),'receipts':[p['receipt']]},self.w,{},10)['fresh'])
    def test_deadline(self):
        p=self.e.fetch('agent-0','supplier_terms',['sku-x'],1)[0]
        answer={'value':reference(self.j,[p]),'receipts':[p['receipt']]}
        self.assertTrue(grade(self.j,answer,self.w,self.e.actors['agent-0'].issued,120)['success'])
        self.assertFalse(grade(self.j,answer,self.w,self.e.actors['agent-0'].issued,120.01)['success'])
    def test_cache_and_version(self):
        e=Engine(self.w,'A1');e.fetch('agent-0','inventory',['sku-x'],1);e.fetch('agent-1','inventory',['sku-x'],1)
        self.assertEqual(e.usage['fetches'],1)
        e.fetch('agent-1','inventory',['sku-x'],3);self.assertEqual(e.usage['fetches'],2)
    def test_overlap_denominator(self):
        self.assertEqual(overlap(jobs(0,1),self.w)['repeated_occurrences'],4)
        self.assertEqual(overlap(jobs(0,5,'overlap_shift'),self.w)['repeated_occurrences'],0)
    def test_no_reuse_cache(self):
        e=Engine(self.w,'A1')
        for j in jobs(0,5,'overlap_shift'):e.fetch('agent-0',j['endpoints'][0],j['entities'],5)
        self.assertEqual(e.usage['fetches'],6);self.assertEqual(e.usage['cache_hits'],0)
    def test_unload_real_context_and_adapter(self):
        r=self.e.propose('agent-0',1,'x','unload_tool',{'name':'inventory'})
        self.assertTrue(r['accepted']);self.assertNotIn('inventory',self.e.context('agent-0',self.j)['loaded_tools'])
        with self.assertRaises(PermissionError):self.e.fetch('agent-0','inventory',['sku-x'],2)
        self.assertTrue(self.e.propose('agent-0',2,'y','load_tool',{'name':'inventory'})['accepted'])
        self.e.fetch('agent-0','inventory',['sku-x'],3)
    def test_protected_truth(self):
        with self.assertRaises(PermissionError): self.e.fetch('agent-0','private_truth',['sku-x'],1)
        self.assertFalse(self.e.propose('agent-0',1,'x','load_tool',{'name':'private_truth'})['accepted'])
    def test_mutation_idempotency(self):
        args=('agent-0',1,'x','unload_tool',{'name':'inventory'})
        self.assertEqual(self.e.propose(*args),self.e.propose(*args));self.assertEqual(self.e.usage['proposals'],1)
        with self.assertRaises(ValueError):self.e.propose('agent-0',1,'x','load_tool',{'name':'inventory'})
    def test_slot_and_failed_proposals_count(self):
        self.e.propose('agent-0',1,'x','unload_tool',{'name':'inventory'})
        self.assertFalse(self.e.propose('agent-0',1,'y','load_tool',{'name':'inventory'})['accepted'])
        self.assertEqual(self.e.usage['proposals'],2);self.assertEqual(self.e.usage['rejected'],1)
    def test_static_cannot_mutate(self):
        e=Engine(self.w,'A2');self.assertFalse(e.propose('agent-0',1,'x','unload_tool',{'name':'inventory'})['accepted'])
    def test_model_switch_requires_qualification(self):
        self.assertFalse(self.e.propose('agent-0',1,'x','switch_model',{'model':'typed_choice'})['accepted'])
        self.assertTrue(self.e.propose('agent-0',2,'y','switch_model',{'model':'typed_choice'},qualified=ROLES)['accepted'])
        self.assertEqual(self.e.actors['agent-0'].model,'typed_choice')
    def test_namespace_reset_private_memory(self):
        self.e.fetch('agent-0','inventory',['sku-x'],1)
        other=Engine(self.w,'A1');self.assertFalse(other.actors['agent-0'].issued);self.assertNotEqual(self.e.namespace,other.namespace)
        self.assertFalse(self.e.actors['agent-1'].issued)
    def test_pairing_call_count_independent(self):
        first=self.w.fetch('inventory','sku-x',3)
        for _ in range(10):self.w.fetch('delivery_status','sku-x',1)
        self.assertEqual(first,self.w.fetch('inventory','sku-x',3))
    def test_context_leakage(self):
        self.e.actors['agent-1'].memory.append({'secret_observation':'PRIVATE_MARKER'})
        text=json.dumps(self.e.context('agent-0',self.j))
        for forbidden in ('PRIVATE_MARKER','expected_answer','shock_schedule','future_jobs'):self.assertNotIn(forbidden,text)
    def test_generic_join_and_parameter_independence(self):
        e=Engine(self.w,'A1');packets=[]
        for ep in ('inventory','supplier_terms'):packets+=e.fetch('agent-0',ep,['sku-x'],1)
        ids=[p['receipt'] for p in packets]
        program=[{'op':'normalize','endpoint':'inventory'},{'op':'join','endpoint':'supplier_terms','key':'entity_id'}]
        a=e.program('agent-0',program,ids,self.j);self.j['quantity']=3;b=e.program('agent-0',program,ids,self.j)
        self.assertEqual(a,b);self.assertEqual(len(a),2);self.assertEqual(e.usage['program_ops'],2)
    def test_sandbox_program_and_undeclared_data(self):
        with self.assertRaises(ValueError): execute([{'op':'exec','cmd':'anything'}],[],self.j)
        with self.assertRaises(PermissionError):self.e.program('agent-0',[{'op':'normalize','endpoint':'inventory'}],['not-issued'],self.j)
    def test_service_real_reuse_and_invalidation(self):
        self.e.propose('agent-0',1,'r','register_service',{'name':'data','endpoint':'inventory','capacity':4})
        for i in (1,2):
            self.e.propose(f'agent-{i}',1,f'c{i}','connect',{'service':'agent-0/data'})
            result=self.e.service(f'agent-{i}','agent-0','data',['sku-x'],self.j)
            self.assertTrue(set(result['receipts'])<=set(self.e.actors[f'agent-{i}'].issued))
        self.assertEqual(self.e.usage['fetches'],1);self.assertEqual(self.e.usage['cache_hits'],1)
        self.j['epoch']=3;self.e.service('agent-1','agent-0','data',['sku-x'],self.j)
        self.assertEqual(self.e.usage['fetches'],2)
    def test_fork_accounting_and_isolation(self):
        self.e.fetch('agent-0','inventory',['sku-x'],1);child=self.e.fork_frozen()
        self.assertTrue(child.parent);self.assertEqual(child.actors,self.e.actors)
        child.actors['agent-0'].memory.clear();self.assertTrue(self.e.actors['agent-0'].memory)
        self.assertFalse(child.propose('agent-0',2,'x','unload_tool',{'name':'inventory'})['accepted'])
        self.assertEqual(prefix_accounting(10,3,2),{'physical_total':15,'adaptive_deployment':13,'frozen_deployment':12})
    def test_delayed_boundary_expires_fixed_arrivals(self):
        batch=[job(0,2,i) for i in range(6)]
        rows=released_jobs(batch,120+130)
        self.assertTrue(all(r['expired'] and not r['dispatchable'] for r in rows))
        self.assertEqual({r['release_s'] for r in rows},{120})
    def test_missing_assigned_and_infinity(self):
        summary=summarize([job(0,1,i) for i in range(6)],[],1)
        self.assertEqual(summary['quality'],0);self.assertEqual(summary['unstarted'],6)
        self.assertEqual(summary['cost_per_success_label'],'infinity')
    def test_duplicate_outcome_rejected(self):
        with self.assertRaises(ValueError):summarize([self.j],[{'id':self.j['id']},{'id':self.j['id']}],0)
    def test_named_random_streams(self):
        self.assertEqual(stream_seed('dev',1,'jobs'),stream_seed('dev',1,'jobs'))
        self.assertNotEqual(stream_seed('dev',1,'jobs'),stream_seed('dev',1,'policy'))
    def test_schema_migration(self):
        w=World(0);p=w.fetch('supplier_terms','sku-x',5)
        self.assertEqual(p['schema_version'],2)
        self.assertTrue(all('unit_cents' in r and 'body' not in r for r in normalize(p)))

class BudgetTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'ledger.sqlite';self.deadline=time.time()+1000
        self.b=Budget(self.path,'authority','host',100,2,self.deadline)
    def tearDown(self):self.b.close();self.tmp.cleanup()
    def test_reserve_before_uncertain_charge(self):
        self.b.reserve('1','request',60);self.b.settle('1')
        with self.assertRaises(ValueError):self.b.reserve('2','request2',60)
        self.assertEqual(self.b.summary()['charged_upper_usd'],60/1e9)
    def test_duplicate_and_spend_reconciliation(self):
        self.b.reserve('1','a',60);self.b.settle('1',10)
        with self.assertRaises(ValueError):self.b.reserve('1','a',60)
        self.b.reserve('2','b',60);self.b.settle('2',20)
        self.assertEqual(self.b.summary()['known_api_usd'],30/1e9)
        with self.assertRaises(ValueError):self.b.reserve('3','c',1)
    def test_authority_cannot_increase_or_copy_host(self):
        with self.assertRaises(ValueError):Budget(self.path,'authority','host',200,2,self.deadline)
        with self.assertRaises(ValueError):Budget(self.path,'authority','other-host',100,2,self.deadline)
    def test_rejected_settlement_preserves_reserve(self):
        self.b.reserve('1','a',60)
        with self.assertRaises(ValueError):self.b.settle('1',61)
        self.assertEqual(self.b.summary()['charged_upper_usd'],60/1e9)

class NativeAndQualificationTests(unittest.TestCase):
    def setUp(self):self.models=json.loads((BASE/'models.json').read_text())['models']
    def test_development_lifecycle_and_request_bound(self):
        # Hand-scripted unit fixtures on development roots, never reserved S0/S1 data.
        for role in ROLES:
            for case in range(3):
                state=make_case(case,development=True)
                for step in range(4):
                    p=probe(state,step,role);req=request(self.models[role],p['sections'],p['choices'])
                    self.assertEqual(req['provider']['allow_fallbacks'],False)
                    score=apply(state,step,p['expected'],p['expected'])
                    self.assertTrue(score['correct'],(role,case,step,score))
    def test_reserved_manifest_no_labels(self):
        rows=assignments();self.assertEqual(len(rows),144);self.assertEqual(len({r['id'] for r in rows}),144)
        self.assertFalse(any('expected' in r for r in rows))
    def test_qualification_all_assigned_failure(self):
        s=analyze([]);self.assertFalse(s['qualification_passed']);self.assertEqual(s['assigned'],144)
    def test_model_response_receipt_and_substitution(self):
        c=self.models['generalist'];raw={'model':c['accepted_response_model_ids'][0],'provider':c['provider_name'],
            'choices':[{'finish_reason':'stop','message':{'content':'{"type":"directory"}'}}],
            'usage':{'prompt_tokens':10,'completion_tokens':5,'cost':.00004}}
        self.assertEqual(response(raw,c)['actual_provider'],'Anthropic')
        raw['model']=self.models['cheap_generative']['requested_model_id']
        with self.assertRaises(ValueError):response(raw,c)
    def test_decision_finite_contract(self):
        c=self.models['typed_choice'];choices={'A':{'type':'directory'},'B':{'type':'answer','value':0,'receipts':[]}}
        raw={'model':c['accepted_response_model_ids'][0],'provider':c['provider_name'],
             'answers':{'action':{'type':'choice','choice':'A','probabilities':{'A':.7,'B':.3}}},
             'usage':{'input_tokens':10,'output_tokens':0,'cost':.00000042}}
        self.assertEqual(response(raw,c,choices)['action'],choices['A'])
        raw['answers']['action']['probabilities']['A']=float('nan')
        with self.assertRaises(ValueError):response(raw,c,choices)
    def test_maximum_wire_budget(self):
        self.assertLess(sum(reserve_nano(c)*96 for c in self.models.values())/1e9,5)
    def test_catalog_mismatch(self):
        c=self.models['typed_choice'];e=json.loads((BASE/'route-metadata.json').read_text())['routes']['typed_choice']
        self.assertTrue(verify_catalog({'data':{'endpoints':[e]}},c)['verified'])
        e['name']='different'
        with self.assertRaises(ValueError):verify_catalog({'data':{'endpoints':[e]}},c)

class AdmissionTests(unittest.TestCase):
    def setUp(self):
        self.now=time.time();self.c={'experiment':'poietic-agents','stage':'S0','attempt':'S0-01','file_hashes':inventory(),
          'assignment_sha256':digest(assignments()),'review_resolution':'P1-P3-v0.2-tested','source_commit':'a'*40,
          'authorization':{'study':'poietic-agents','stage':'S0','owner_approved':True,'reference':'unit-fixture-only','api_cap_usd':1.5,'infrastructure_cap_usd':0.5,'total_cumulative_cap_usd':2,'physical_call_cap':288,'deadline':self.now+3600},
          'allocation':{'experiment':'poietic-agents','operator':'vishesh/codex-heterogeneous','host':'fixture','claim_id':'fixture','merged_claim_revision':'a'*40,'exclusive':True,'registered_fleet_destination':True,'workload_idle':True,'approved_account_verified':True,'checked_at':self.now,'expires_at':self.now+4000,'allocated_usd_per_hour':.1,'charge_started_at':self.now},
          'credential':{'alias':'swarm-lab-openrouter','study_authorized':True},'worker_count':1,'concurrency':1,
          'public_plan':{'url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/README.md','sha256':'b'*64},
          'run_tldr':'TLDR: unit fixture','condition_tldrs':{r:'TLDR: unit fixture' for r in ROLES}}
        self.c['page_verification']={'url':self.c['public_plan']['url'],'rendered':True,'checked_at':self.now}
    def test_complete_fixture_and_missing_budget(self):
        self.assertTrue(verify(self.c,self.now,actual_host='fixture')['ready'])
        self.c['authorization']['owner_approved']=False
        with self.assertRaisesRegex(ValueError,'budget_not_authorized'):verify(self.c,self.now,actual_host='fixture')
    def test_fault_admission_matrix(self):
        for section,key,value in [('allocation','checked_at',self.now-301),('allocation','exclusive',False),('allocation','workload_idle',False),('allocation','approved_account_verified',False),('allocation','expires_at',self.now+100),('credential','study_authorized',False),('page_verification','rendered',False)]:
            c=copy.deepcopy(self.c);c[section][key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):verify(c,self.now,actual_host='fixture')
    def test_source_manifest_drift(self):
        self.c['file_hashes']['src/engine.py']='wrong'
        with self.assertRaisesRegex(ValueError,'source_mismatch'):verify(self.c,self.now,actual_host='fixture')
    def test_s1_cannot_bypass_qualification(self):
        self.c['stage']='S1'
        with self.assertRaisesRegex(ValueError,'unadmitted_stage'):verify(self.c,self.now,actual_host='fixture')
    def test_public_current_plan_binding(self):
        with self.assertRaisesRegex(ValueError,'plan_binding'):verify_public(self.c,lambda *a:{'url':'old','plan_sha256':'b'*64})
        with self.assertRaises(OSError):verify_public(self.c,lambda *a:(_ for _ in ()).throw(OSError()))
    def test_visual_fixture_labels_and_counts(self):
        with tempfile.TemporaryDirectory() as d:
            s=analyze([]);p=Path(d)/'frame.svg';qualification_frame(s,p,scripted=True)
            text=p.read_text();self.assertIn('SCRIPTED',text);self.assertEqual(text.count('Correct 0/48'),3)
            out=Path(d)/'replay.html';replay([{'epoch':0,'elapsed_s':0,'assigned':6,'successes':0,'cost_usd':0,'agents':[],'events':['</script>']}],out,True)
            self.assertNotIn('["</script>"]',out.read_text());self.assertIn('SCRIPTED',out.read_text())

if __name__=='__main__':unittest.main()

class MechanismRuntimeTests(unittest.TestCase):
    def test_capacity_failure_rolls_back_memory_but_charges_fetch(self):
        e=Engine(KnownWorld(0),capacity=800)
        before=digest({k:a.definition() for k,a in e.actors.items()})
        with self.assertRaises(ValueError):e.fetch('agent-0','inventory',['sku-x'],1)
        self.assertEqual(before,digest({k:a.definition() for k,a in e.actors.items()}))
        self.assertFalse(e.actors['agent-0'].issued);self.assertEqual(e.usage['fetches'],1)
    def test_live_route_dispatch_after_actual_model_change(self):
        from lineage import run_lineage
        e=Engine(KnownWorld(0));ticks=[0];seen=[]
        def backend(role,sections,choices,call_id):
            seen.append((role,call_id));ticks[0]+=1
            if 'boundary' in call_id:
                action={'type':'propose','operation':'switch_model','payload':{'model':'cheap_generative'}}
            else:
                current=sections[2]['job']
                action={'type':'fetch','endpoint':current['endpoints'][0],'entities':current['entities']}
            return {'action':action,'actual_model':role,'usage':{'cost_usd':.01}}
        assigned=[job(0,1,0,'sku-x'),job(0,2,0,'sku-x')]
        result=run_lineage(e,assigned,backend,ROLES,clock=lambda:ticks[0],sleep=lambda s:ticks.__setitem__(0,ticks[0]+s),deployment_started=0)
        self.assertTrue(any(role=='cheap_generative' and ':2:' in cid for role,cid in seen))
        self.assertEqual(result['summary']['assigned'],2)
        self.assertEqual(result['outcomes'][1]['release_s'],120)
        self.assertGreaterEqual(result['outcomes'][1]['finish_s'],126)
    def test_static_configuration_rejects_missing_construction(self):
        from lineage import static_configuration
        with self.assertRaises(ValueError):static_configuration(Engine(KnownWorld(0),'A2'),{})
    def test_finite_choices_contain_no_evaluator(self):
        from lineage import finite_actions
        e=Engine(KnownWorld(0));menu=finite_actions(e,'agent-0',job(0,1,0))
        self.assertTrue(2<=len(menu)<=12);self.assertNotIn('expected',json.dumps(menu))
    def test_png_record_counts(self):
        from render import qualification_png
        from PIL import Image
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'frame.png';qualification_png(analyze([]),p,True)
            with Image.open(p) as im:self.assertEqual(im.size,(1600,720))

class RelayTests(unittest.TestCase):
    def setUp(self):
        self.models=json.loads((BASE/'models.json').read_text())['models']
        state=make_case(0,development=True);packet=probe(state,0,'generalist')
        self.data={'id':'S0-01:generalist:0:0:physical-0','role':'generalist','request':request(self.models['generalist'],packet['sections'])}
    def test_assigned_native_envelope(self):
        from relay import validate_payload
        self.assertEqual(validate_payload(self.data,self.models)['provider_tag'],'anthropic')
    def test_unassigned_and_wrong_role(self):
        from relay import validate_payload
        for field,value in [('id','other-study:physical-0'),('role','cheap_generative')]:
            data=copy.deepcopy(self.data);data[field]=value
            with self.assertRaises(ValueError):validate_payload(data,self.models)
    def test_no_provider_fallback_or_oversized_generation(self):
        from relay import validate_payload
        for key,value in [('provider',{'allow_fallbacks':True}),('max_tokens',2000),('stream',True)]:
            data=copy.deepcopy(self.data);data['request'][key]=value
            with self.assertRaises(ValueError):validate_payload(data,self.models)
    def test_credential_remains_local_to_relay(self):
        import inspect,launch
        source=inspect.getsource(launch.run)
        self.assertNotIn('Bearer ',source);self.assertNotIn('POIETIC_OPENROUTER_KEY',source)
        self.assertIn('loopback_credential_relay_required',source)
    def test_review_resolution_evidence_is_required(self):
        case=AdmissionTests();case.setUp();case.c.pop('review_resolution',None)
        with self.assertRaisesRegex(ValueError,'review_resolution_missing'):verify(case.c,case.now,actual_host='fixture')
