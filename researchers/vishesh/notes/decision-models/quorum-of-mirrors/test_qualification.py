import copy
import unittest
from qualification import manifest, assignments, analyze, validate_manifest, validate_response, SNAPSHOT, PROVIDER


def response(choice):
    return {'model':SNAPSHOT,'provider':PROVIDER,'usage':{'cost':.0001,'input_tokens':100,'output_tokens':0},
            'answers':{'decision':{'choice':choice,'probabilities':{k:float(k==choice) for k in ('ZERO','ONE','DEFER')}}}}


def receipts():
    return [{'id':r['id'],'request_sha256':r['request_sha256'],'status':'complete','response':response(r['expected'])}
            for r in assignments()]


class QualificationContracts(unittest.TestCase):
    def test_exact_matrix_and_identical_repeats(self):
        rows=assignments()
        self.assertEqual(len(rows),32)
        self.assertEqual(len({r['id'] for r in rows}),32)
        for a,b in zip(rows[:16],rows[16:]):
            self.assertEqual(a['request'],b['request'])
            self.assertEqual(a['request_sha256'],b['request_sha256'])
            self.assertNotEqual(a['id'],b['id'])
        for q in (.65,.8):
            for label in ('ZERO','ONE'):
                self.assertEqual(sum(r['q']==q and r['expected']==label for r in rows),8)

    def test_no_evaluator_fields_in_requests(self):
        for r in assignments():
            self.assertEqual(set(r['request']['state']),{'reports'})
            for report in r['request']['state']['reports']:
                self.assertEqual(set(report),{'report_id','visible_root','bit','q'})
            self.assertNotIn('expected',r['request'])

    def test_manifest_target_or_payload_mutation_rejected(self):
        for field,value in [('expected','DEFER'),('request',{})]:
            m=manifest();m['assignments'][0][field]=value
            with self.assertRaises(ValueError):validate_manifest(m)

    def test_route_and_usage_rejection(self):
        for field,value in [('model','other'),('provider','other'),('usage',{'cost':0})]:
            r=response('ONE');r[field]=value
            with self.assertRaises(ValueError):validate_response(r)

    def test_choice_score_not_normalized(self):
        r=response('ONE');r['answers']['decision']['probabilities']={'ZERO':.33,'ONE':.34,'DEFER':.34}
        checked=validate_response(r)
        self.assertEqual(checked['probabilities'],r['answers']['decision']['probabilities'])
        r['answers']['decision']['probabilities']['ONE']=float('nan')
        with self.assertRaises(ValueError):validate_response(r)

    def test_perfect_scripted_fixture_qualifies_software_only(self):
        s=analyze(manifest(),receipts())
        self.assertTrue(s['qualified'])
        self.assertEqual((s['correct'],s['agreeing_pairs']),(32,16))

    def test_unstarted_and_failed_remain_in_denominator(self):
        rows=receipts()[:3];rows[-1]={'id':rows[-1]['id'],'request_sha256':rows[-1]['request_sha256'],'status':'failed'}
        s=analyze(manifest(),rows)
        self.assertEqual((s['correct'],s['failed'],s['unstarted']),(2,1,29))
        self.assertEqual(s['accuracy_all_assigned'],2/32)
        self.assertFalse(s['qualified'])

    def test_cell_floor_blocks_misleading_overall_pass(self):
        rows=receipts();target=[i for i,r in enumerate(assignments()) if r['q']==.65 and r['expected']=='ONE'][:3]
        for i in target:rows[i]['response']=response('ZERO')
        s=analyze(manifest(),rows)
        self.assertEqual(s['correct'],29)
        self.assertFalse(s['qualified'])

    def test_duplicate_and_request_mismatch_rejected(self):
        rows=receipts()
        with self.assertRaises(ValueError):analyze(manifest(),rows+[rows[0]])
        rows[0]['request_sha256']='different'
        with self.assertRaises(ValueError):analyze(manifest(),rows)


if __name__=='__main__':unittest.main()
