"""Offline invariant and fault tests. No credentials, network or model downloads."""
import copy
import itertools
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from http.server import BaseHTTPRequestHandler,HTTPServer
from threading import Thread
from tasks import make_world,validate_world,task_view,document,digest,allocation,feasible,independent_answer
from sim import Runner,DEFAULT_CFG,arms_for,run_episode,majority,merge_memory,evaluate,validate_response
from providers import Scripted,HTTP,Anthropic,ProviderFailure,phase_schema
from analyze import summarize,contrast
from worker import execute_bundle
from artifacts import prepare_artifacts

class Tests(unittest.TestCase):
    def test_worlds(self):
        answers=set();keys=set();families=set()
        for i in range(300):
            w=make_world(i);answers.add(validate_world(w));keys.add(w['target_key']);families.add(w['family'])
            self.assertEqual(w,make_world(i))
            self.assertNotIn('false_value',json.dumps(task_view(w)))
            for n in (3,5,9):
                groups,exposed=allocation(w,n,1)
                self.assertEqual(sorted(sum(groups,[])),sorted(d['id'] for d in w['docs']))
                self.assertIn('digest',groups[exposed])
        self.assertEqual(answers,{'A','B','C'});self.assertEqual(len(families),3)
    def test_boundary_truth_tables(self):
        self.assertTrue(feasible('capacity',{'power':10,'access':5},{'power_min':10,'access_max':5}))
        self.assertFalse(feasible('capacity',{'power':9,'access':5},{'power_min':10,'access_max':5}))
        self.assertTrue(feasible('total_cost',{'base':20,'freight':30,'days':5},{'budget':50,'deadline':5}))
        self.assertFalse(feasible('total_cost',{'base':20,'freight':31,'days':5},{'budget':50,'deadline':5}))
        for direct,backup,fast in itertools.product([False,True],repeat=3):
            self.assertEqual(feasible('dependency',{'direct':10 if direct else 9,'backup':int(backup),'transfer':2 if fast else 3},
                                     {'required':10,'transfer_max':2}),direct or (backup and fast))
    def test_tally(self):
        self.assertEqual(majority(['A','B','C'],3),'ABSTAIN')
        self.assertEqual(majority(['A','A','ABSTAIN'],3),'A')
        self.assertEqual(majority(['A','A','B','C','ABSTAIN'],5),'ABSTAIN')
        self.assertEqual(majority(['ABSTAIN']*3,3),'ABSTAIN')
    def test_merge(self):
        c={'key':'A.power','value':4,'sources':['digest']}
        self.assertEqual(merge_memory([{'claims':[c]}],3),[])
        m=merge_memory([{'claims':[c]},{'claims':[c]},{'claims':[]}],3)
        self.assertEqual(len(m),1);self.assertEqual(m[0]['sources'],['digest'])
        self.assertEqual(m[0]['agents'],[0,1])
    def test_validation(self):
        cfg=DEFAULT_CFG;ctx={'task':task_view(make_world(0))}
        for response in [{'vote':'D','claims':[]},{'vote':'A','claims':[{'key':'hidden','value':1,'sources':['digest']}]},
                         {'vote':'A','claims':[{'key':ctx['task']['fact_keys'][0],'value':True,'sources':['digest']}]},
                         {'vote':'A','claims':[],'override':True}]:
            with self.assertRaises(ValueError):validate_response(response,'ballot',ctx,cfg)
        with self.assertRaises(ValueError):validate_response({'read':['audit']*4},'verify',ctx,cfg)
    def test_barriers_and_probe_isolation(self):
        w=make_world(0);r=Runner(Scripted(),DEFAULT_CFG);snapshot=r.acquire(w,1,True);before=copy.deepcopy(snapshot)
        result=r.continue_arm(w,snapshot,3,'board');self.assertEqual(snapshot,before)
        calls=[e for e in r.events if e['kind']=='call_start' and e['phase']=='discuss']
        for turn in (1,2,3):
            group=[e for e in calls if e['round']==turn]
            boards=[e['request']['context']['board'] for e in group]
            self.assertTrue(all(b==boards[0] for b in boards))
            self.assertEqual(len(boards[0]),(turn-1)*3)
            self.assertTrue(all(p['round']<turn for p in boards[0]))
            self.assertTrue(all('vote' not in p for e in group for p in e['request']['context']['private_history']))
        parent=next(e for e in r.events if e['kind']=='call_start' and e['phase']=='parent')
        self.assertEqual(set(parent['request']['context']),{'memory','key','delta','question'})
        self.assertEqual(len(result['trajectory']),4)
    def test_clean_scripted_and_pairing(self):
        for task in range(6):
            rows=run_episode(task,1,'',1,arms_for(),{},Scripted())
            self.assertEqual(len(rows),8)
            self.assertTrue(all(r['evaluation']['correct']==1 for r in rows))
            self.assertTrue(all(r['evaluation']['followup_correct']==1 for r in rows))
            for attack in (False,True):
                hashes={r['snapshot_hash'] for r in rows if r['arm']['attack']==attack}
                self.assertEqual(len(hashes),1)
            for row in rows:
                for events in (row['events'],row['acquisition_events']):
                    previous='0'*64
                    for e in events:
                        self.assertEqual(e['previous'],previous)
                        self.assertEqual(digest({k:v for k,v in e.items() if k!='hash'}),e['hash']);previous=e['hash']
    def test_attack_locality(self):
        w=make_world(0);a=Runner(Scripted(),DEFAULT_CFG);b=Runner(Scripted(),DEFAULT_CFG)
        a.acquire(w,1,False);b.acquire(w,1,True)
        ad=[e for e in a.events if e['kind']=='tool_result' and e['initial']]
        bd=[e for e in b.events if e['kind']=='tool_result' and e['initial']]
        self.assertEqual(sum(x['document']!=y['document'] for x,y in zip(ad,bd)),1)
        self.assertTrue(all(e['document']==document(w,e['document']['id']) for e in b.events if e['kind']=='tool_result' and not e['initial']))
    def test_errors_count(self):
        class Broken(Scripted):
            def complete(self,request):raise TimeoutError('sensitive-value-never-copy')
        rows=run_episode(0,1,'',1,arms_for(),{},Broken())
        self.assertEqual(len(rows),8);self.assertTrue(all(r['evaluation']['invalid']==1 for r in rows))
        self.assertNotIn('sensitive-value',json.dumps(rows))
        self.assertTrue(all(c['assigned']==1 and c['invalid']==1 for c in summarize(rows).values()))
        self.assertEqual(contrast(rows)['invalid_outcome_bounds'],[-2,2])
    def test_harmful_scorer(self):
        w=make_world(2);key=w['target_key'];false={'key':key,'value':w['false_value'],'sources':['digest']}
        b={'vote':w['target'],'claims':[false]};ballots=[copy.deepcopy(b) for _ in range(3)]
        result={'decision':w['target'],'ballots':ballots,'memory':merge_memory(ballots,3),
                'trajectory':[{'round':0,'ballots':ballots,'decision':w['target']}],
                'followup':{'value':w['false_value']+w['followup_delta']},'initial':ballots,'reports':[{'claims':[false]}]*3}
        ev=evaluate(w,result,0)
        self.assertEqual([ev[k] for k in ('target_win','wrong','false_memory_admitted','followup_target_error')],[1,1,1,1])
        self.assertEqual(ev['correct'],0)
    def test_private_control(self):
        w=make_world(1);r=Runner(Scripted(),DEFAULT_CFG);snapshot=r.acquire(w,1,False);r.continue_arm(w,snapshot,3,'private')
        calls=[e for e in r.events if e['kind']=='call_start' and e['phase']=='discuss']
        self.assertTrue(all(not e['request']['context']['board'] for e in calls))
    def test_cluster_and_missing(self):
        rows=run_episode(0,1,'',1,arms_for(),{})
        self.assertEqual(contrast(rows)['task_clusters'],1)
        with self.assertRaises(ValueError):contrast(rows+rows)
        with self.assertRaises(ValueError):contrast([r for r in rows if not (r['arm']['attack'] and r['arm']['rounds']==6)])
    def test_no_truth_in_requests(self):
        for row in run_episode(1,1,'',1,arms_for((0,1)),{}):
            for e in row['events']+row['acquisition_events']:
                if e['kind']=='call_start':
                    text=json.dumps(e['request'])
                    for forbidden in ('false_value','target_key','independent_answer','world_hash'):
                        self.assertNotIn(forbidden,text)
    def test_bundle_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'run';p={'tasks':[0],'seeds':[1],'rounds':[0,1],'n_agents':3,'stage':'S0'}
            result=execute_bundle(p,path,Scripted());self.assertEqual(result['episodes'],4)
            self.assertEqual(len(json.loads((path/'manifest.json').read_text())['planned_episodes']),4)
            with self.assertRaises(FileExistsError):execute_bundle(p,path,Scripted())
    def test_compressed_chunked_artifacts(self):
        import gzip,hashlib
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);payload=json.dumps({'data':list(range(2000))}).encode()
            (p/'episodes.jsonl').write_bytes(payload)
            parts=prepare_artifacts(p,limit=300)
            index=json.loads(parts[-1].read_text())['files'][0]
            self.assertGreater(len(index['parts']),1)
            self.assertTrue(all(x.stat().st_size<=300 for x in parts[:-1]))
            compressed=b''.join((p/'upload'/name).read_bytes() for name in index['parts'])
            self.assertEqual(gzip.decompress(compressed),payload)
            self.assertEqual(hashlib.sha256(payload).hexdigest(),index['raw_sha256'])
            first=[x.read_bytes() for x in parts];second=[x.read_bytes() for x in prepare_artifacts(p,limit=300)]
            self.assertEqual(first,second)
    def test_anthropic_contract_usage_and_no_retry(self):
        from io import BytesIO
        import urllib.error
        response={'stop_reason':'end_turn','content':[{'type':'text','text':'{"value":4}'}],
                  'usage':{'input_tokens':20,'output_tokens':4}}
        with patch.dict('os.environ',{'SWARM_MODEL_API_KEY':'test-secret','SWARM_MODEL_WORKSPACE_ID':'wrkspc_test'}):
            model=Anthropic(model='mock',max_calls=3,max_cost_usd=1,input_usd_per_million=1,output_usd_per_million=5)
            with patch('urllib.request.urlopen',return_value=BytesIO(json.dumps(response).encode())) as call:
                self.assertEqual(model.complete({'phase':'parent','context':{}}),{'value':4})
                req=call.call_args.args[0]; body=json.loads(req.data)
                self.assertEqual(req.full_url,'https://api.anthropic.com/v1/messages')
                self.assertEqual(req.get_header('Anthropic-workspace-id'),'wrkspc_test')
                self.assertNotIn('test-secret',req.data.decode())
                self.assertEqual(body['output_config']['format']['schema'],phase_schema('parent'))
                self.assertAlmostEqual(model.actual_cost_usd,.00004)
                self.assertEqual(model.usage_missing_calls,0)
            response['stop_reason']='max_tokens'
            with patch('urllib.request.urlopen',return_value=BytesIO(json.dumps(response).encode())):
                with self.assertRaisesRegex(ProviderFailure,'incomplete'): model.complete({'phase':'parent','context':{}})
            self.assertAlmostEqual(model.actual_cost_usd,.00008)
            error=urllib.error.HTTPError('https://api.anthropic.com',429,'test-secret',{},None)
            with patch('urllib.request.urlopen',side_effect=error) as call:
                with self.assertRaisesRegex(ProviderFailure,'provider HTTP 429'): model.complete({'phase':'parent','context':{}})
                self.assertEqual(call.call_count,1)
            self.assertEqual(model.usage_missing_calls,1)
            self.assertEqual(model.calls,3)
            with self.assertRaisesRegex(ProviderFailure,'call budget'): model.complete({'phase':'parent','context':{}})

    def test_anthropic_billing_error_is_safe(self):
        from io import BytesIO
        import urllib.error
        with patch.dict('os.environ',{'SWARM_MODEL_API_KEY':'test-secret'}):
            model=Anthropic(model='mock',max_cost_usd=1,input_usd_per_million=1,output_usd_per_million=5)
            body=json.dumps({'error':{'message':'Your credit balance is too low test-secret'}}).encode()
            error=urllib.error.HTTPError('https://api.anthropic.com',400,'test-secret',{},BytesIO(body))
            with patch('urllib.request.urlopen',side_effect=error):
                with self.assertRaises(ProviderFailure) as raised: model.complete({'phase':'parent','context':{}})
            self.assertEqual(raised.exception.public_reason,'provider_credit_balance_low')
            self.assertNotIn('test-secret',str(raised.exception))

    def test_pilot_budget_covers_complete_plan(self):
        from pilot import plan
        for smoke,worlds in ((True,1),(False,6)):
            p=plan(smoke);c=p['model_config']
            self.assertEqual(c['max_calls'],170*worlds)
            per_call=((c['max_input_bytes']+16384)*c['input_usd_per_million']+c['max_output_tokens']*c['output_usd_per_million'])/1e6
            self.assertGreater(c['max_cost_usd'],c['max_calls']*per_call)
            for phase in ('verify','report','discuss','ballot','parent'):
                self.assertLess(len(json.dumps(phase_schema(phase)).encode()),4096)

    def test_http_adapter_and_caps(self):
        requests=[]
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def do_POST(self):
                requests.append(json.loads(self.rfile.read(int(self.headers['Content-Length']))))
                body=json.dumps({'choices':[{'finish_reason':'stop','message':{'content':'{"value": 4}'}}],
                                 'usage':{'prompt_tokens':20,'completion_tokens':4,'total_tokens':24}}).encode()
                self.send_response(200);self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
        server=HTTPServer(('127.0.0.1',0),Handler);thread=Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            with patch.dict('os.environ',{'SWARM_MODEL_BASE_URL':f'http://127.0.0.1:{server.server_port}/v1','SWARM_MODEL_API_KEY':''}):
                model=HTTP('mock-v1',max_calls=1,max_cost_usd=.1,input_usd_per_million=1,output_usd_per_million=1)
                self.assertEqual(model.complete({'phase':'parent','context':{}}),{'value':4})
                with self.assertRaises(ProviderFailure): model.complete({'phase':'parent','context':{}})
                self.assertEqual(len(requests),1)
                with self.assertRaises(ProviderFailure):HTTP('mock-v1')
        finally: server.shutdown();server.server_close();thread.join()

if __name__=='__main__':unittest.main(verbosity=2)
