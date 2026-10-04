"""Scripted offline acceptance checks; no native performance claims."""
import contextlib,io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from input_binding import binding,futile,receipt
from tasks import generate,reference_answer
from engine import execute
from run_qualification import assignments_for,run_batch,launch_errors
class InputBinding(unittest.TestCase):
    def test_queue_admission_fails_closed(self):
        from admit_input_binding import admission_errors
        a=dict(exclusive_claim_verified=True,approved_account_verified=True,sole_ledger_writer_verified=True,prior_worker_stopped=True,prior_artifacts_verified=True,dedicated_credential_provenance_verified=True,source_commit='rev',attempt_id='q-a7',dispatch_origin='orbital-one',credential_alias='swarm-lab-anthropic/vishesh',queue_issue=1,claim_id='claim',verified_epoch=1000,claim_expiry_epoch=9000)
        self.assertEqual(admission_errors(a,'rev',1000),[])
        for key,value in [('source_commit','wrong'),('dispatch_origin','laptop'),('credential_alias','general'),('exclusive_claim_verified',False),('sole_ledger_writer_verified',False),('verified_epoch',0),('claim_expiry_epoch',1500)]:
            self.assertIn(key if key not in ('verified_epoch','claim_expiry_epoch') else ('stale_admission' if key=='verified_epoch' else 'claim_expiry'),admission_errors(a|{key:value},'rev',1000))
    def config(self):return json.loads((Path(__file__).parent.parent/'input-binding-config.json').read_text())
    def test_public_only_binding_and_wrong_upstream_retained(self):
        t=generate('evidence','chain',6,width=3);b=binding(t.public,'item_00',{})
        self.assertEqual(set(b['public_records']),{'opening','a_0','b_0'})
        wrong={'item_00':{'value':-123,'source_ids':[]}}
        b=binding(t.public,'item_01',wrong)
        self.assertEqual(b['prerequisite_artifacts'],wrong);self.assertEqual(set(b['public_records']),{'a_1','b_1'})
        self.assertNotIn('value',b);self.assertNotIn('truth',json.dumps(b));self.assertEqual(len(receipt(b)['sha256']),64)
    def test_assignment_pairs_resource_contract_and_review_waiver(self):
        c=self.config();rows=assignments_for(c);self.assertEqual(len(rows),8)
        self.assertEqual([r['arm'] for r in rows],['full','bound','bound','full','bound','full','full','bound'])
        self.assertEqual({r['root'] for r in rows},{6,7});self.assertTrue(all(r['n']==1 for r in rows))
        for a,b in zip(rows[::2],rows[1::2]):self.assertEqual(a['public_task_sha256'],b['public_task_sha256']);self.assertNotEqual(a['id'],b['id'])
        self.assertNotIn('missing:independent_review_commit',launch_errors(c))
        c['slots']=2
        with self.assertRaises(ValueError):assignments_for(c)
    def test_bound_changes_only_work_prompt_preserves_history(self):
        t=generate('evidence','chain',6,width=3);answer=reference_answer(t);arms={}
        for bound in (False,True):
            contexts=[];events=[]
            def call(messages,deadline,actor,phase,item):
                contexts.append((phase,messages))
                if phase=='plan':return json.dumps({'dependencies':t.public['dependencies']})
                if phase=='work':return json.dumps({'artifact':answer['answers'][item]})
                return json.dumps(answer)
            r=execute(t.public,1,1,10,2,call,events.append,strict_contract=True,enforce_dependencies=True,bind_inputs=bound)
            self.assertIsNone(r['failure']);self.assertEqual(len(contexts),5)
            self.assertEqual(sum(e['kind']=='input_binding' for e in events),3 if bound else 0)
            self.assertEqual(contexts[1][1][1]['content'],json.dumps(t.public,sort_keys=True))
            arms[bound]=contexts
        self.assertEqual(arms[False][0],arms[True][0]);self.assertEqual(arms[False][-1][1][-1],arms[True][-1][1][-1])
        self.assertNotIn('Explicit public input binding',arms[False][1][1][-1]['content'])
        self.assertIn('Explicit public input binding',arms[True][1][1][-1]['content'])
    def test_futility_not_partial_or_one_structure(self):
        rows=assignments_for(self.config());records=[{'assignment':r,'evaluation':{'quality':.5}} for r in rows[:4]]
        self.assertFalse(futile(records[:3]));self.assertTrue(futile(records))
        records[1]['evaluation']['quality']=.6;self.assertFalse(futile(records))
    def test_runner_retains_unstarted_denominator_at_futility(self):
        c=self.config()
        class FakeProvider:
            def __init__(self,c,b,e,j,p):self.task=generate('evidence','chain' if p['dependencies'][p['items'][1]] else 'parallel',int(p['id'].split('/')[-1]));self.answer=reference_answer(self.task)
            def __call__(self,m,d,a,phase,item):
                if phase=='plan':return json.dumps({'dependencies':self.task.public['dependencies']})
                if phase=='work':return json.dumps({'artifact':self.answer['answers'][item]})
                return json.dumps(self.answer)
        class FakeReporter:
            def __init__(self,*a):pass
            def progress(self,*a):return {'acknowledged':True}
            def finish(self,*a):return {'complete':True}
        with tempfile.TemporaryDirectory() as temp:
            out=Path(temp)/'out';out.mkdir()
            with patch('run_qualification.Provider',FakeProvider),patch('run_qualification.Reporter',FakeReporter),contextlib.redirect_stdout(io.StringIO()):run_batch(c,'SCRIPTED-NOT-MODEL',out,Path(temp)/'ledger.sqlite',assignments_for(c))
            rec=json.loads((out/'reconciliation.json').read_text())
            self.assertEqual((rec['assigned'],rec['terminal'],rec['unstarted']),(8,4,4));self.assertEqual(rec['stop_reason'],'input_binding_futility')
            self.assertTrue(rec['executed_publication_complete']);self.assertFalse(rec['execution_complete'])
