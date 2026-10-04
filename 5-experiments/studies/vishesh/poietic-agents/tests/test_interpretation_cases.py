import copy,json,sys,unittest
from pathlib import Path
B=Path(__file__).resolve().parents[1]/'interpretation-dev';sys.path.insert(0,str(B))
from fixed_baseline import public_context,decide,valid_output

class InterpretationCasesTests(unittest.TestCase):
    def setUp(self):
        self.cases=json.loads((B/'cases.json').read_text());self.labels=json.loads((B/'labels.json').read_text())
    def test_every_hand_label_has_public_fixed_controller_witness(self):
        self.assertEqual(len(self.cases),16);self.assertEqual(len({x['root'] for x in self.cases}),4)
        for case in self.cases:
            answer=decide(public_context(case));self.assertTrue(valid_output(answer,case['public']['task']['kind']))
            self.assertEqual(answer,self.labels[case['id']],case['id'])
    def test_meaning_pairs_change_invariants_preserve_missing_abstains(self):
        for root in {x['root'] for x in self.cases}:
            self.assertNotEqual(self.labels[root+'-base']['value'],self.labels[root+'-changed']['value'])
            self.assertEqual(self.labels[root+'-base'],self.labels[root+'-invariant'])
            self.assertEqual(self.labels[root+'-missing']['status'],'insufficient_evidence')
    def test_reordering_duplication_and_opaque_ids_do_not_change_decision(self):
        for case in self.cases:
            packet=public_context(case);expected=decide(packet)
            packet['documents']=list(reversed(packet['documents']))+[copy.deepcopy(packet['documents'][0])]
            self.assertEqual(decide(packet),expected)
            case=copy.deepcopy(case);case['id']='opaque-random';case['root']='opaque';case['gold']='PROTECTED_SENTINEL'
            self.assertNotIn('PROTECTED_SENTINEL',json.dumps(public_context(case)))
            self.assertEqual(decide(public_context(case)),expected)
    def test_unrecognized_semantics_and_output_shape_fail_closed(self):
        for case in self.cases:
            packet=public_context(case)
            next(x for x in packet['documents'] if x['kind']=='policy')['body']='A different policy with unspecified precedence.'
            self.assertEqual(decide(packet)['status'],'insufficient_evidence')
        self.assertFalse(valid_output(dict(status='answer',value=1,citations=[]),'returns'))
        self.assertFalse(valid_output(dict(status='answer',value=False,citations=[],extra=1),'returns'))
    def test_complete_public_packet_fits_context_budget_without_labels(self):
        for case in self.cases:
            s=json.dumps(public_context(case),sort_keys=True,ensure_ascii=True)
            self.assertLess(len(s),4500)
            for field in ['"expected"','"gold"','"variant"','"root"']:self.assertNotIn(field,s)

if __name__=='__main__':unittest.main()
