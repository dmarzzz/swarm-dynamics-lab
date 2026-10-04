import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from contract import CELLS,development_world,reconstruct
from design import schedule,clean_packet,qualified
from wire import request,validate,SNAPSHOT,reservation
from ledger import Ledger,HISTORICAL_NANO
from engine import Engine
from admission import Admission

def response(req,choices=None):
    choices=choices or {}
    answers={}
    for k,q in req['questions'].items():
        c=choices.get(k,next(iter(q['criteria'])))
        answers[k]=dict(type='choice',choice=c,confidence=1,probabilities={v:float(v==c) for v in q['criteria']})
    return dict(model=SNAPSHOT,provider='TypeSafe',answers=answers,usage=dict(cost=.000001,input_tokens=100,output_tokens=0))

def fixture(req):
    p=req['state']
    if 'target' in req['questions']:
        seen={r['cell'] for r in p['evidence']['observations'] if r['source']=='sensor'}
        return response(req,{'target':next(c for c in CELLS if c not in seen)})
    m=reconstruct(p);return response(req,{f'cell_{c.replace(",","_")}':v for c,v in m.items()})

class Native(unittest.TestCase):
    def setUp(self):self.w=development_world(300);self.p=clean_packet(self.w,0,'choice')[0]
    def test_counts_no_reserved_construction(self):
        self.assertEqual(len(schedule('Q0')),24);self.assertEqual(len(schedule('S1')),1792)
        self.assertEqual(len({r['id'] for r in schedule('S1')}),1792)
        self.assertEqual(sum(r['kind']=='yoked' for r in schedule('S1')),32)
    def test_choice_has_all_cells_and_one_question(self):
        req=request(self.p,'choice');self.assertEqual(set(req['questions']['target']['criteria']),set(CELLS));self.assertEqual(reservation(req),1344000)
        self.assertEqual(validate(response(req),req)['result']['choice'],'0,0')
    def test_model_fallback_and_schema_rejected(self):
        req=request(self.p,'choice')
        for field,value in [('model','wrong'),('provider','other'),('answers',{})]:
            raw=response(req);raw[field]=value
            with self.assertRaises(ValueError):validate(raw,req)
    def test_probabilities_and_usage_rejected(self):
        req=request(self.p,'choice');raw=response(req);raw['answers']['target']['probabilities']['0,0']=float('nan')
        with self.assertRaises(ValueError):validate(raw,req)
        raw=response(req);raw['usage']['cost']=1
        with self.assertRaises(ValueError):validate(raw,req)
    def test_current_missing_cell_without_hidden_truth(self):
        p,missing=clean_packet(self.w,0,'choice');self.assertEqual(len(p['evidence']['observations']),35);self.assertNotIn(missing,{r['cell'] for r in p['evidence']['observations']});self.assertNotIn('truth',p)
    def test_map_requests_name_the_cells(self):
        req=request(self.p,'map');self.assertEqual(len(req['questions']),36)
        self.assertEqual(len(validate(response(req),req)['result']['map']),36)

class Persistence(unittest.TestCase):
    def setUp(self):self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name);self.l=Ledger(self.base/'budget.sqlite','a'*64)
    def tearDown(self):self.l.db.close();self.tmp.cleanup()
    def test_carry_forward_uncertainty_duplicate_and_no_reset(self):
        self.l.reserve('x',48384000);self.l.finish('x')
        self.assertAlmostEqual(self.l.summary()['cumulative_exposure_usd'],(HISTORICAL_NANO+48384000)/1e9)
        with self.assertRaises(Exception):self.l.reserve('x',48384000)
        with self.assertRaises(ValueError):Ledger(self.base/'budget.sqlite','b'*64)
    def test_stage_cannot_repeat(self):
        self.l.claim('Q0','q0-a1')
        with self.assertRaises(Exception):self.l.claim('Q0','q0-a2')
    def test_unknown_reservations_exhaust_budget(self):
        count=0
        while True:
            try:self.l.reserve(str(count),48384000);count+=1
            except ValueError:break
        self.assertEqual(count,79);self.assertLessEqual(self.l.summary()['cumulative_exposure_usd'],4)
    def test_record_written_before_wire(self):
        def transport(req):
            rows=json.loads((self.base/'run'/'records.json').read_text());self.assertEqual(sum(r['status']=='started' for r in rows),1);return fixture(req)
        engine=Engine('Q0','fixture',self.base/'run',self.l,transport,{s:development_world(s) for s in range(300,304)})
        result=engine.run();self.assertTrue(result['qualification_passed']);self.assertEqual(result['valid'],24)
    def test_failure_stop_retains_unstarted_and_cost(self):
        calls=[]
        def fail(req):calls.append(1);raise TimeoutError('sensitive error intentionally never persisted')
        result=Engine('Q0','fixture',self.base/'run',self.l,fail,{s:development_world(s) for s in range(300,304)}).run()
        self.assertEqual(len(calls),5);self.assertEqual(result['assigned'],24);self.assertEqual(result['started'],5);self.assertFalse(result['qualification_passed'])
        self.assertNotIn('sensitive',(self.base/'run'/'records.json').read_text());self.assertGreater(result['budget']['cumulative_exposure_usd'],.16)
    def test_sensing_round_barrier_and_fixed_denominators(self):
        engine=Engine('S1','fixture',self.base/'run',self.l,fixture,{300:development_world(300)})
        result=engine.run();self.assertEqual(result['valid'],224)
        episodes=json.loads((self.base/'run'/'episodes.json').read_text());self.assertEqual(len(episodes),12)
        for e in episodes:self.assertEqual(len(e['events']),12)
        team=[r for r in engine.rows if r.get('policy')=='team' and r.get('slot')==1 and r['kind']=='choice']
        self.assertTrue(all(r['request']['state']['previous_proposals']==[] for r in team))
        for r in engine.rows:
            if r['kind']=='yoked':self.assertEqual(r['request']['state']['previous_proposals'],[])
    def test_all_missing_contrast_not_zero_interval(self):
        def fail(req):raise ValueError('invalid')
        engine=Engine('S1','fixture',self.base/'run',self.l,fail,{300:development_world(300)})
        result=engine.run();self.assertEqual(result['overall']['primary_bounds'],{'lower':-2,'upper':2});self.assertEqual(result['assigned'],224)
    def test_unadmitted_config_never_calls_public_or_world(self):
        with patch('contract._world',side_effect=AssertionError('opened')),patch('admission.subprocess.check_output',return_value='x'):
            with self.assertRaises(ValueError):Admission({},'Q0',lambda *a:self.fail('network'))

if __name__=='__main__':unittest.main()

class Gate(unittest.TestCase):
    def setUp(self):
        import datetime
        from admission import fingerprint
        from wire import digest
        import hashlib
        self.t=tempfile.TemporaryDirectory();self.p=Path(self.t.name);self.now=datetime.datetime.now(datetime.timezone.utc)
        proof=self.p/'proof';proof.write_text('Fixture attestation only. Never live admission.')
        ref={'path':str(proof),'sha256':hashlib.sha256(proof.read_bytes()).hexdigest()}
        ledger=self.p/'ledger';ledger.write_bytes(b'fixture')
        self.c=dict(design='PC-2',stage='Q0',attempt='q0-a1',source_commit='head',instrument=fingerprint(),assignment_sha256=digest(schedule('Q0')),research_scope_admitted=True,authorization='phantom-coast-usd5-20261004',prior_spend_nano=162723246,api_cap_nano=4000000000,max_calls=1816,checked_utc=self.now.isoformat(),claim_until=(self.now+datetime.timedelta(hours=2)).isoformat(),deadline=(self.now+datetime.timedelta(hours=2)).isoformat(),model=SNAPSHOT,ledger_path=str(ledger),ledger_sha256=hashlib.sha256(ledger.read_bytes()).hexdigest())
        for name in ('research_scope','pre_assessment','page_verification','allocation','budget_lineage','runtime'):self.c[name]=ref
        for flag in ('predecessor_fenced','predecessor_reconciled','single_ledger_authority','exclusive_allocation','approved_mars_fleet','rendered_page_verified'):self.c[flag]=True
        from admission import BASE
        self.c.update(plan_url='fixture-plan',plan_sha256=hashlib.sha256((BASE/'PLAN.md').read_bytes()).hexdigest(),run_tldr='fixture only')
    def tearDown(self):self.t.cleanup()
    def admit(self,c=None,public=None):
        c=c or self.c
        with patch('admission.subprocess.check_output',return_value='head'):
            return Admission(c,'Q0',public or (lambda *a:dict(url=c['plan_url'],plan_sha256=c['plan_sha256'])),self.now)
    def test_source_budget_scope_allocation_are_enforced(self):
        for key,value in [('instrument',{}),('source_commit','wrong'),('assignment_sha256','wrong'),('research_scope_admitted',False),('exclusive_allocation',False),('prior_spend_nano',0),('max_calls',2000),('single_ledger_authority',False),('approved_mars_fleet',False),('rendered_page_verified',False)]:
            c=copy.deepcopy(self.c);c[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.admit(c)
    def test_expired_short_stale_and_tampered_evidence(self):
        import datetime
        for key,value in [('checked_utc',(self.now-datetime.timedelta(minutes=6)).isoformat()),('claim_until',self.now.isoformat()),('ledger_sha256','wrong'),('research_scope',{'path':str(self.p/'proof'),'sha256':'wrong'})]:
            c=copy.deepcopy(self.c);c[key]=value
            with self.subTest(key=key),self.assertRaises(ValueError):self.admit(c)
    def test_public_mismatch_and_network_failure_block(self):
        with self.assertRaises(ValueError):self.admit(public=lambda *a:dict(url='wrong',plan_sha256=self.c['plan_sha256']))
        def failed(*a):raise OSError('offline')
        with self.assertRaises(OSError):self.admit(public=failed)
    def test_admission_does_not_generate_worlds(self):
        with patch('contract._world',side_effect=AssertionError('opened')):
            a=self.admit();self.assertTrue(a.allows(400));self.assertFalse(a.allows(500));self.assertFalse(a.allows(1000))

class Launch(unittest.TestCase):
    def test_start_ack_failure_prevents_reserved_world_and_transport(self):
        import types
        import run as runner
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);key=p/'fixture-key';key.write_text('NON_SECRET_TEST_FIXTURE');key.chmod(0o600)
            c={'stage':'Q0','attempt':'fixture-q0','ledger_path':str(p/'budget'),'predecessor_sha256':'a'*64,'host':'fixture','source_commit':'fixture','run_tldr':'fixture only'}
            config=p/'config.json';config.write_text(json.dumps(c))
            hub=types.SimpleNamespace(params={})
            sr=types.SimpleNamespace(Run=lambda *a:hub,report=lambda *a,**kw:False)
            admission=types.SimpleNamespace(public={})
            with patch.object(runner,'Admission',return_value=admission),patch.object(runner,'check_route',return_value={}),patch.object(runner,'_world',side_effect=AssertionError('reserved world opened')),patch.dict(sys.modules,{'swarm_report':sr}):
                with self.assertRaisesRegex(ValueError,'start_unacknowledged'):runner.run(config,p/'out',key)
            self.assertFalse((p/'out').exists())
    def test_route_price_and_provider_changes_block(self):
        import run as runner
        import io
        def opener(row):return type('Opener',(),{'open':lambda self,*a,**kw:io.StringIO(json.dumps({'data':{'endpoints':[row]}}))})()
        route=dict(provider_name='TypeSafe',tag='typesafe',status=0,name=SNAPSHOT,pricing={'prompt':.000000042,'completion':0},context_length=32000)
        self.assertEqual(runner.check_route(opener(route))['snapshot'],SNAPSHOT)
        for key,value in [('provider_name','other'),('pricing',{'prompt':1,'completion':0}),('context_length',64000)]:
            r=copy.deepcopy(route);r[key]=value
            with self.assertRaises(ValueError):runner.check_route(opener(r))

class Visual(unittest.TestCase):
    def test_initial_audit_failure_and_final_frames(self):
        from contract import Episode
        from design import endpoint
        from replay import frame
        from PIL import Image
        out=Path(tempfile.gettempdir())/'phantom-pc2-visual-check';out.mkdir(exist_ok=True)
        es=[]
        for report in ('misleading','benign'):
            e=Episode(development_world(300),report=report,audit=True)
            for slot in range(12):e.step([None]*3 if slot==5 else [CELLS[slot]]*3)
            records=[{'kind':'map','status':'not-started'} for _ in range(3)]+[{'kind':'yoked','status':'not-started'}]
            es.append(dict(seed=300,policy='team',report=report,audit=True,events=e.events,truth=e.world['truth'],report_cells=e.world['region'],endpoint=endpoint(e,records),status='fixture-missing-endpoints'))
        for slot in (0,6,12):
            im=frame(es,300,'team',True,slot,fixture=True);im.save(out/f'frame-{slot}.png');self.assertEqual(im.size,(1600,920))
        frames=[frame(es,300,'team',True,s,fixture=True).resize((800,460)) for s in (0,6,12)]
        frames[0].save(out/'fixture.gif',save_all=True,append_images=frames[1:],duration=200)
        with Image.open(out/'fixture.gif') as im:self.assertEqual(im.n_frames,3)

class Qualification(unittest.TestCase):
    def test_thresholds_and_missingness_cannot_promote(self):
        worlds={s:development_world(s,'block' if s%2==0 else 'scattered') for s in range(300,304)}
        rows=[]
        for a in schedule('Q0',worlds):
            req=request(clean_packet(worlds[a['seed']],a['actor'],a['kind'])[0],a['kind'])
            rows.append(dict(a,status='valid',checked=validate(fixture(req),req)))
        self.assertTrue(qualified(rows,worlds)['qualification_passed'])
        choices=[r for r in rows if r['kind']=='choice']
        for i in range(2):
            actual=choices[i]['checked']['result']['choice'];choices[i]['checked']['result']['choice']=next(c for c in CELLS if c!=actual)
            self.assertEqual(qualified(rows,worlds)['qualification_passed'],i==0)
        rows[0]['status']='failed';self.assertFalse(qualified(rows,worlds)['qualification_passed'])
        with self.assertRaises(ValueError):qualified(rows[:-1],worlds)

class OptionalReview(unittest.TestCase):
    setUp=Gate.setUp
    tearDown=Gate.tearDown
    admit=Gate.admit
    def test_researcher_review_fields_not_required(self):
        self.assertNotIn('researcher_review',self.c)
        self.assertNotIn('researcher_review_passed',self.c)
        self.assertNotIn('reviewer_researcher',self.c)
        self.assertTrue(self.admit().allows(400))
    def test_old_negative_review_flags_do_not_reintroduce_gate(self):
        c=copy.deepcopy(self.c)
        c.update(researcher_review_passed=False,reviewer_researcher='vishesh')
        self.assertTrue(self.admit(c).allows(400))
