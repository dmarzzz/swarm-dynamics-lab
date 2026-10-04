import copy,json,unittest
from tasks import generate,reference_answer
from stage_audit import evidence_stage_audit
from engine import execute
from run_qualification import assignments_for
class StageAudit(unittest.TestCase):
    def test_regressions_rescues_and_duplicate_proofs(self):
        t=generate('evidence','chain',0,width=3);correct=reference_answer(t)['answers'];worker=copy.deepcopy(correct);final=copy.deepcopy(correct)
        worker['item_00']['value']+=1
        final['item_01']['value']+=1
        final['item_02']['source_ids']+=final['item_02']['source_ids'][:1]
        r=evidence_stage_audit(t,{'work_artifacts':worker,'artifact':json.dumps({'answers':final}),'plan_dependencies':t.public['dependencies']})
        self.assertEqual((r['correct_to_wrong'],r['wrong_to_correct']),(2,1))
        self.assertEqual(r['worker_wrong_values'],1);self.assertEqual(r['final_wrong_proofs'],1)
        self.assertEqual(r['missing_required_edges'],0)
    def test_worker_capture_adds_no_calls_or_truth_to_context(self):
        t=generate('evidence','parallel',0,width=2);answer=reference_answer(t);phases=[]
        def call(messages,deadline,actor,phase,item):
            phases.append(phase);self.assertNotIn('stage_diagnostics',json.dumps(messages))
            if phase=='plan':return json.dumps({'dependencies':t.public['dependencies']})
            if phase=='work':return json.dumps({'artifact':answer['answers'][item]})
            return json.dumps(answer)
        r=execute(t.public,1,1,10,2,call,strict_contract=True)
        self.assertEqual(phases,['plan','work','work','integrate']);self.assertEqual(r['work_artifacts'],answer['answers'])
        audit=evidence_stage_audit(t,r);self.assertTrue(audit['assembled_worker_evaluation']['substantive_success'])
    def test_missing_answers_are_not_success(self):
        t=generate('evidence','chain',0,width=2);r=evidence_stage_audit(t,{'artifact':None})
        self.assertEqual(r['worker_wrong_values'],2);self.assertEqual(r['missing_required_edges'],1)
    def test_eight_evidence_cases_with_separate_identity(self):
        rows=assignments_for({'stage':'evidence-audit','attempt_id':'q-a5','attempt_cap_microdollars':4000000,'episode_cap_microdollars':2000000,'response_contract':'anthropic-json-schema-v1'})
        self.assertEqual(len(rows),8);self.assertTrue(all(r['family']=='evidence' and r['width']==16 for r in rows));self.assertEqual([r['root'] for r in rows],[0,0,1,1,2,2,3,3])
