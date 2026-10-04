import copy,json,sqlite3,sys,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'src'))
from budget import Budget
from common import digest,canonical
from provider_diagnostics import safe_error,retry_after
from route_retry import Adapter,TransportStopped,wire,contract,retry_delay,validate_catalog,_reserve_scoped

class RouteRepairTests(unittest.TestCase):
    def test_nested_hints_alias_and_provenance_without_secret(self):
        secret='TEST_SECRET_DO_NOT_RETURN'
        raw={'error':{'code':429,'metadata':{'headers':{'retry-after':'11','authorization':secret}},'provider_error_code':'rate_limited','message':secret,'provider_name':'DekaLLM'}}
        body={'error':{'code':429,'message':secret,'metadata':{'limit_source':'upstream_provider_shared_pool','raw':json.dumps(raw),'headers':{'Retry-After':'9','x-ratelimit-remaining':'0','Cookie':secret}}}}
        r=safe_error(429,body,{'retry-after':'4','Authorization':secret},'DekaLLM',1700000000)
        self.assertNotIn(secret,canonical(r));self.assertEqual(r['provider_code'],'rate_limited')
        self.assertEqual(r['retry_after_seconds'],11);self.assertEqual(r['limit_source'],'upstream_provider_shared_pool')
        self.assertEqual(r['provider_name'],'DekaLLM');self.assertIn('raw.error',r['provider_name_source'])
        self.assertEqual(len(r['quota_hints']),3);self.assertTrue(r['retry_eligible_envelope'])
        r=safe_error(429,{'error':{'code':429}},expected_provider='DekaLLM')
        self.assertEqual(r['expected_provider'],'DekaLLM');self.assertNotIn('provider_name',r);self.assertNotIn('limit_source',r)

    def test_untrusted_shapes_and_partial_outputs_never_retry(self):
        for body in [b'raw secret',{'error':{'code':429},'choices':[{'message':{'content':'partial'}}]}, {'error':{'code':429},'usage':{'cost':.001}}, {'error':{'code':429},'usage':{'cost':'0'}}, {'error':{'code':429},'id':'generation-started'}]:
            self.assertFalse(safe_error(429,body)['retry_eligible_envelope'])
        self.assertFalse(safe_error(200,{'error':{'code':429}})['retry_eligible_envelope'])
        r=safe_error(429,{'error':{'code':429,'metadata':{'raw':'{"error":{"provider_error_code":"API_KEY_SECRET"}}'}}})
        self.assertNotIn('API_KEY_SECRET',canonical(r))
        for raw in ['['*2000, 'x'*32001, [],False]:safe_error(429,{'error':{'code':429,'metadata':{'raw':raw}}})

    def test_retry_after_is_not_shortened_and_nontransient_stops(self):
        r={'retry_eligible_envelope':True,'retry_after_seconds':17}
        self.assertEqual(retry_delay(r,1,100,.5),17.5)
        self.assertEqual(retry_delay({'retry_eligible_envelope':True},2,100,1),11)
        for delta in [{'retry_after_seconds':61},{'provider_name_mismatch':True},{'diagnostic_conflicts':['limit_source']},{'limit_source':'openrouter_credits'},{'provider_code':'insufficient_quota'},{'retry_eligible_envelope':False}]:
            self.assertIsNone(retry_delay(dict(r,**delta),1,100,0))
        self.assertIsNone(retry_delay(r,1,60,0));self.assertIsNone(retry_delay(r,3,100,0))
        self.assertEqual(retry_after('Tue, 14 Nov 2023 22:13:21 GMT',1700000000.1),1)

    def fixture(self,replies):
        directory=tempfile.TemporaryDirectory();self.addCleanup(directory.cleanup)
        path=Path(directory.name)/'original.sqlite';deadline=time.time()+1000
        b=Budget(path,'OFFLINE','fixture',1_500_000_000,288,deadline);self.addCleanup(b.close)
        for i in range(148):b.reserve('history:'+str(i),'OFFLINE',503782838 if i==0 else 1);b.settle('history:'+str(i))
        clock=[0.];events=[];requests=[];queue=list(replies)
        def transport(req):
            requests.append(copy.deepcopy(req));result=queue.pop(0)
            if isinstance(result,Exception):raise result
            return result
        adapter=Adapter(b,transport,deadline,clock=lambda:clock[0],wall=lambda:deadline-900+clock[0],sleep=lambda n:clock.__setitem__(0,clock[0]+n),jitter=lambda:.5,emit=events.append)
        return adapter,b,events,requests,clock

    def success(self,content='invalid action'):
        return (200,dict(model=contract()['requested_model_id'],provider='DekaLLM',choices=[{'finish_reason':'stop','message':{'content':content}}],usage={'prompt_tokens':10,'completion_tokens':5,'cost':.000004}),{})
    def refusal(self):return (429,{'error':{'code':429,'metadata':{'provider_name':'DekaLLM','provider_error_code':'rate_limited'}}},{'Retry-After':'7'})

    def test_recovered429_same_request_two_rows_and_prior_history(self):
        a,b,events,reqs,clock=self.fixture([self.refusal(),self.success()]);req=wire([{'development':'fixture'}]);result=a.invoke('Q30-05:cheap_generative:0:0',req)
        self.assertEqual(reqs,[req,req]);self.assertGreaterEqual(events[1]['started_monotonic']-events[0]['started_monotonic'],7)
        rows=b.db.execute("SELECT reserve,settled,status FROM charges WHERE id LIKE 'Q30-05:%' ORDER BY id").fetchall()
        self.assertEqual(rows,[(380928,None,'uncertain'),(380928,4000,'known')]);self.assertEqual(b.summary()['physical_calls'],150)
        self.assertEqual(b.db.execute("SELECT SUM(COALESCE(settled,reserve)) FROM charges WHERE id LIKE 'history:%'").fetchone()[0],503782985)
        self.assertEqual(result['choices'][0]['message']['content'],'invalid action')
        with self.assertRaises(ValueError):a.invoke('Q30-05:cheap_generative:0:0',req)

    def test_third429_and_timeout_stop_without_semantic_retry(self):
        a,b,events,reqs,_=self.fixture([self.refusal()]*3)
        with self.assertRaises(TransportStopped):a.invoke('Q30-05:cheap_generative:0:0',wire([{}]))
        self.assertEqual(len(reqs),3);self.assertTrue(a.stopped);self.assertEqual(b.summary()['physical_calls'],151)
        for result in [TimeoutError('SECRET'),(200,{'error':{'code':429}},{}), (429,{'error':{'code':429},'choices':[{'delta':{'content':'part'}}]}, {})]:
            a,b,events,reqs,_=self.fixture([result])
            with self.assertRaises(TransportStopped):a.invoke('Q30-05:cheap_generative:0:0',wire([{}]))
            self.assertEqual(len(reqs),1);self.assertNotIn('SECRET',canonical(events))

    def test_global_retry_and_physical_limits_are_atomic_in_original_ledger(self):
        a,b,events,reqs,_=self.fixture([])
        # All48 initial slots plus6 retries. A fresh object cannot reset this stage cap.
        for i in range(48):
            ident=f'Q30-05:cheap_generative:{i//4}:{i%4}:physical-0';_reserve_scoped(b,ident,'OFFLINE',380928);b.settle(ident)
        for i in range(6):
            ident=f'Q30-05:cheap_generative:{i//4}:{i%4}:physical-1';_reserve_scoped(b,ident,'OFFLINE',380928);b.settle(ident)
        with self.assertRaises(ValueError):_reserve_scoped(b,'Q30-05:cheap_generative:3:3:physical-1','OFFLINE',380928)
        self.assertEqual(b.summary()['physical_calls'],202)
        self.assertEqual(b.db.execute('SELECT cap,calls FROM authority').fetchone(),(1500000000,288))

    def test_nested_partial_output_and_nonrate_status_never_retry(self):
        for raw in [{'choices':[{'text':'partial'}]}, {'error':{'code':401}}, {'error':{'code':403}}]:
            receipt=safe_error(429,{'error':{'code':429,'metadata':{'raw':json.dumps(raw)}}},None,'DekaLLM')
            self.assertIsNone(retry_delay(receipt,1,200,.1))
        receipt=safe_error(429,{'error':{'code':429,'metadata':{'provider_error_code':429,'raw':json.dumps({'error':{'code':401}})}}})
        self.assertIn('provider_status',receipt['diagnostic_conflicts'])
        self.assertIsNone(retry_delay(receipt,1,200,.1))

    def test_provider_pin_parameters_and_served_route_are_enforced(self):
        request=wire([{}]);self.assertEqual(request['provider'],{'only':['dekallm/bf16'],'allow_fallbacks':False,'require_parameters':True,'data_collection':'deny'})
        c=json.loads((BASE/'route-repair/catalog.json').read_text())['endpoint'];self.assertTrue(validate_catalog({'data':{'endpoints':[c]}})['parameter_support'])
        c['supported_parameters'].remove('reasoning_effort')
        with self.assertRaises(ValueError):validate_catalog({'data':{'endpoints':[c]}})
        good=self.success();bad=(good[0],dict(good[1],provider='DeepInfra'),{})
        a,b,events,reqs,_=self.fixture([bad])
        with self.assertRaisesRegex(TransportStopped,'route_mismatch'):a.invoke('Q30-05:cheap_generative:0:0',request)
        self.assertEqual(len(reqs),1);self.assertEqual(events[-1]['status'],'route_mismatch')
        self.assertEqual(b.db.execute("SELECT status FROM charges WHERE id LIKE 'Q30-05:%'").fetchone()[0],'known')


class QualificationLifecycleTests(unittest.TestCase):
    def test_complete_fresh_lifecycle_with_one_recovered_refusal_is_scored_once(self):
        import route_qualification as q
        expected=[]
        for case in range(12):
            state=q.make_case(case,development=True)
            for step in range(4):
                p=q.probe(state,step,'cheap_generative');expected.append((wire(p['sections']),p['expected']));q.apply(state,step,p['expected'],p['expected'])
        with tempfile.TemporaryDirectory() as directory:
            deadline=time.time()+2000;b=Budget(Path(directory)/'fixture.sqlite','OFFLINE','fixture',1500000000,288,deadline)
            calls=[];clock=[0.];cursor=[0]
            def transport(req):
                calls.append(req)
                if len(calls)==1:return (429,{'error':{'code':429}},{'Retry-After':'6'})
                want,action=expected[cursor[0]];cursor[0]+=1;self.assertEqual(req,want)
                return 200,dict(model=contract()['requested_model_id'],provider='DekaLLM',choices=[dict(finish_reason='stop',message={'content':canonical(action)})],usage=dict(prompt_tokens=100,completion_tokens=20,cost=.00001)),{}
            a=Adapter(b,transport,deadline,clock=lambda:clock[0],wall=lambda:deadline-1800+clock[0],sleep=lambda n:clock.__setitem__(0,clock[0]+n),jitter=lambda:.25)
            r=q.run(a,development=True);self.assertTrue(r['summary']['passed']);self.assertEqual(r['summary']['physical_attempts'],49);self.assertEqual(r['summary']['correct'],48)
            self.assertEqual(b.summary()['uncertain_requests'],1);b.close()

if __name__=='__main__':unittest.main()
