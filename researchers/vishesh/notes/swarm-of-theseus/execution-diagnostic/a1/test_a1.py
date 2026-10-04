import copy,json,sqlite3,tempfile,time,unittest
from pathlib import Path
from design import *
from scoring import policy_score,policy_reference,action_score
from admission import validate,public_check,GateError
from runner import reserve,write_new
from analyze import summarize

def correct_policy(a):
    v={'mapping':a['rule'],'support':{cls:[h['case']['id'] for h in a['history'] if h['case']['class']==cls] for cls in 'AB'}}
    return {'value':v,'raw_text':json.dumps(v),'error':None,'actual_usd':0.,'response_received':True}

def receipt():
    import hashlib
    now=time.time();rev='a'*40;sha=hashlib.sha256((ROOT/'A1-PLAN.md').read_bytes()).hexdigest()
    r={'experiment':EXPERIMENT,'source_commit':rev,'instrument_sha256':source_hash(),'assignments_sha256':digest(assignments()),'model':MODEL,'max_calls':204,'cap_usd':2.5,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'exclusive_claim_verified':True,'public_page_verified':True,'dependencies_verified':True,'research_review_status':'not-required-owner-direction','verified_epoch':now,'public_page_verified_epoch':now,'pricing_verified_epoch':now,'claim_until_epoch':now+8000,'plan_url':'https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/A1-PLAN.md','plan_sha256':sha,'assessment_url':'https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/A1-PRE.md','assessment_sha256':hashlib.sha256(b'Status: diagnostic-only\n').hexdigest(),'prior_spend_usd':.8122310437,'total_authority_usd':5,'infrastructure_hold_usd':.1,'update_approval_sha256':sha,'dispatch_origin':'orbital-one','allocation_reserved_usd':2.6}
    for k in ('authority_allocation_id','owner_authorization_ref','claim_id','host','review_policy_ref','operator','allocation_verification_ref','queue_issue','original_ledger_ref','budget_retirement_ref','credential_policy_ref','runtime_sha256'):r[k]='SCRIPTED'
    for k in ('approved_account_verified','original_ledger_reconciled','exclusive_workload_verified','queue_dispatch_authorized','credential_policy_verified','host_key_verified'):r[k]=True
    r['authority_allocation_id']='theseus-a1-7300-7305-v1'
    return r

class A1Tests(unittest.TestCase):
    def test_panel_counts_and_disjointness(self):
        self.assertEqual(check()['assigned_calls'],204);self.assertEqual(check(8300)['independent_designed_roots'],6)
        self.assertFalse({c['id'] for w in worlds() for c in w['train']+w['test']} & {c['id'] for w in worlds(8300) for c in w['train']+w['test']})
    def test_identifiability_and_exact_baseline(self):
        for a in assignments()[:12]:
            self.assertEqual({c:candidates(a['history'],c,a['context'])[0] for c in 'AB'},a['rule'])
            r=correct_policy(a);self.assertTrue(policy_score(a,r)['qualified']);self.assertTrue(policy_reference(a,r)['qualified'])
    def test_no_truth_or_test_in_learning_input(self):
        for a in assignments()[:12]:
            visible=json.loads(a['request']['messages'][0]['content'])
            self.assertEqual(set(visible),{'task_family','history'})
            if a['context']=='incident':self.assertEqual({h['outcome'] for h in visible['history']},{'activated','quiet'})
            self.assertNotIn('mapping',visible)
    def test_f_executor_unchanged(self):
        for a in assignments()[12:]:
            self.assertEqual(execution_request(a,a['rule']),r1.request(a['cases'][0],a['rule'],a['context'],'F'))
    def test_false_policy_and_citations_fail(self):
        for a in assignments()[:12]:
            r=correct_policy(a);r['value']['mapping']=dict(zip('AB',reversed(tuple(a['rule'].values()))));r['raw_text']=json.dumps(r['value'])
            self.assertFalse(policy_score(a,r)['qualified']);self.assertFalse(policy_reference(a,r)['qualified'])
    def test_valid_id_without_semantic_support_fails(self):
        a=next(a for a in assignments()[:12] if a['context']=='release');r=correct_policy(a)
        cls='A';h=next(h for h in a['history'] if h['case']['class']==cls and h['outcome']=='hold')
        r['value']['support'][cls]=[h['case']['id']];r['raw_text']=json.dumps(r['value'])
        self.assertFalse(policy_score(a,r)['support_valid']);self.assertFalse(policy_reference(a,r)['qualified'])
    def test_wrong_class_duplicate_unknown_support_fail(self):
        a=assignments()[0]
        for ids in (['missing'],[],[a['history'][0]['case']['id']]*2):
            r=correct_policy(a);r['value']['support']['A']=ids;r['raw_text']=json.dumps(r['value']);self.assertFalse(policy_score(a,r)['qualified'])
    def test_missing_bad_mapping_cannot_fallback(self):
        a=assignments()[0]
        for value in (None,{}, {'mapping':{'A':'probe','B':'probe'},'support':{}}, {'mapping':{'A':[],'B':'ledger'},'support':{}}):
            r={'value':value,'raw_text':json.dumps(value)};self.assertIsNone(policy_score(a,r)['mapping']);self.assertFalse(policy_reference(a,r)['qualified'])
    def test_schema_and_false_activations(self):
        a=next(a for a in assignments()[12:] if a['context']=='incident' and not a['cases'][0]['evidence'][a['rule'][a['cases'][0]['class']]]['signal'])
        v={'decisions':[{'id':a['cases'][0]['id'],'command':'console1/probe'}]};r={'value':v,'raw_text':json.dumps(v)}
        self.assertFalse(action_score(a,r)['correct']);self.assertTrue(action_score(a,r)['valid_response'])
        v['decisions'].append(v['decisions'][0]);r['raw_text']=json.dumps(v);self.assertFalse(action_score(a,r)['valid_response'])
    def test_all_gate_fields_fail_closed(self):
        r=receipt();validate(r,r['source_commit'],assignments())
        for k in r:
            if k=='status':continue
            broken=copy.deepcopy(r);broken.pop(k)
            with self.subTest(k=k),self.assertRaises(GateError):validate(broken,r['source_commit'],assignments())
    def test_expired_changed_scope_and_wrong_origin_block(self):
        r=receipt()
        for k,v in [('verified_epoch',0),('claim_until_epoch',0),('dispatch_origin','laptop'),('update_approval_sha256','0'*64),('prior_spend_usd',0),('max_calls',205)]:
            b=dict(r,**{k:v})
            with self.assertRaises(GateError):validate(b,r['source_commit'],assignments())
    def test_public_registration_and_hash(self):
        r=receipt()
        def read(url):
            if url.endswith('/api/state'):return json.dumps({'experiments':[{'id':EXPERIMENT,'url':r['plan_url'],'description':'TLDR: scripted fixture'}]})
            if url.endswith('A1-PLAN.md'):return (ROOT/'A1-PLAN.md').read_text()
            return 'Status: diagnostic-only\n'
        self.assertIn('checked_epoch',public_check(r,read))
        with self.assertRaises(GateError):public_check(r,lambda url:'{}' if url.endswith('/api/state') else read(url))
    def test_budget_and_duplicate_write(self):
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'quota.sqlite'
            with sqlite3.connect(p) as db:db.execute('CREATE TABLE budget (id,cap,used,calls,deadline)');db.execute('INSERT INTO budget VALUES (1,2.5,2.499,203,?)',(time.time()+10,))
            with self.assertRaises(GateError):reserve(p,.01,time.time())
            write_new(Path(tmp)/'once',{})
            with self.assertRaises(FileExistsError):write_new(Path(tmp)/'once',{})
    def test_full_saved_fixture_reconciliation_and_missingness(self):
        # Software integration fixture only: no actor/provider call, no empirical sample.
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp);(p/'calls').mkdir();design=assignments();write_new(p/'manifest.json',{'evidence_type':'SCRIPTED SOFTWARE FIXTURE — NOT MODEL EVIDENCE','assignments':design})
            for a in design:
                if a['kind']=='learn':result=correct_policy(a);body=a['request']
                else:
                    body=execution_request(a,a['rule']);c=a['cases'][0];command=d1.commands(a['context'])[d1.truth(c,a['context'],a['rule'])];v={'decisions':[{'id':c['id'],'command':command}]};result={'value':v,'raw_text':json.dumps(v),'error':None,'actual_usd':0.,'response_received':True}
                write_new(p/'calls'/(a['id']+'-started.json'),{'request':body,'request_sha256':digest(body),'reserved_usd':.01})
                write_new(p/'calls'/(a['id']+'-finished.json'),result)
            s=summarize(p);self.assertTrue(s['qualification_passed']);self.assertEqual(s['arms']['learned']['correct'],96)
            (p/'calls'/(design[-1]['id']+'-finished.json')).unlink();s=summarize(p);self.assertFalse(s['qualification_passed']);self.assertEqual(s['unknown_usage_calls'],1);self.assertEqual(s['unresolved_exposure_usd'],.01)
    def test_actual_dispatch_loop_invalid_parent_and_duplicate_fence(self):
        import runner,types,sys
        from unittest.mock import patch
        design=assignments();lookup={json.dumps(a['request'],sort_keys=True):a for a in design[:12]}
        for a in design[12:]:lookup[json.dumps(execution_request(a,a['rule']),sort_keys=True)]=a
        calls=[]
        def fake_invoke(body,key,timeout):
            a=lookup[json.dumps(body,sort_keys=True)];calls.append(a['id'])
            if a['kind']=='learn':
                if a['id']==design[0]['id']:return {'value':{},'raw_text':'{}','error':None,'actual_usd':0.,'response_received':True}
                return correct_policy(a)
            c=a['cases'][0];v={'decisions':[{'id':c['id'],'command':d1.commands(a['context'])[d1.truth(c,a['context'],a['rule'])]}]}
            return {'value':v,'raw_text':json.dumps(v),'error':None,'actual_usd':0.,'response_received':True}
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);ledger=root/'original.sqlite'
            with sqlite3.connect(ledger) as db:db.execute('CREATE TABLE allocations (id TEXT PRIMARY KEY, output TEXT, assigned_sha TEXT)')
            r=receipt();r['status']='diagnostic-only';rp=root/'receipt.json';rp.write_text(json.dumps(r))
            def git(cmd,**kw):
                return '/private/tmp/swarm-theseus' if '--show-toplevel' in cmd else '' if 'status' in cmd else 'a'*40
            with patch.object(runner,'ALLOCATION_LEDGER',ledger),patch.object(runner,'invoke',fake_invoke),patch.object(runner,'public_check',return_value={'fixture':True}),patch.object(runner.socket,'gethostname',return_value='SCRIPTED'),patch.object(runner.subprocess,'check_output',side_effect=git),patch.object(runner.resource,'setrlimit'),patch.dict(sys.modules,{'swarm_report':types.SimpleNamespace(report=lambda *a,**k:True)}),patch.dict(runner.os.environ,{'SWARM_MODEL_API_KEY':'SCRIPTED-NOT-A-KEY','SWARM_MODEL_WORKSPACE_ID':'SCRIPTED-NOT-A-ROUTE'}):
                runner.run(rp,root/'run')
                summary=json.loads((root/'run/summary.json').read_text());self.assertEqual(summary['started_calls'],196);self.assertEqual(summary['observed_decisions'],184);self.assertFalse(summary['qualification_passed']);self.assertEqual(summary['arms']['learned']['correct'],88)
                with self.assertRaises(sqlite3.IntegrityError):runner.run(rp,root/'duplicate')
                self.assertEqual(len(calls),196)
if __name__=='__main__':unittest.main()
