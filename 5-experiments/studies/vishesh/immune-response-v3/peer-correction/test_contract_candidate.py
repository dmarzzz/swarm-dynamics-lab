import copy
import json
import unittest
import jsonschema
import peer_instrument as frozen
import contract_candidate as candidate


class ExplicitContract(unittest.TestCase):
    def setUp(self):
        self.case = frozen.roots()[0]
        self.o = frozen.observation(self.case, self.case['initial'], 1, [], source=False)
        self.d = frozen.world.reference.labels(self.o)

    def test_only_instruction_changes_and_schema_boundaries_stay_fixed(self):
        old, old_body = frozen.request(self.case, self.o, 'action', self.d)
        new, body = candidate.request(self.case, self.o, 'action', self.d)
        self.assertIn('reason: at most 240 characters', body['messages'][0]['content'])
        self.assertEqual({k:v for k,v in old.items() if k!='instructions'},
                         {k:v for k,v in new.items() if k!='instructions'})
        a=copy.deepcopy(old_body); b=copy.deepcopy(body)
        a['messages'][0]['content']=b['messages'][0]['content']='instruction'
        self.assertEqual(a,b)
        for length, valid in [(240,True),(241,False),(325,False)]:
            errors=list(jsonschema.Draft202012Validator(new['response_schema']).iter_errors(
                {'reason':'x'*length,'action_id':'wait'}))
            self.assertEqual(not errors,valid)
        self.assertEqual(frozen.request(self.case,self.o,'diagnosis'),
                         candidate.request(self.case,self.o,'diagnosis'))

    def test_all_note_limits_are_visible_and_enforced(self):
        initial={'diagnosis':self.d,'proposal':{'reason':'Healthy.','action_id':'wait'}}
        for arm in frozen.ARMS:
            old,_=frozen.note_request(self.o,initial,arm)
            q,body=candidate.note_request(self.o,initial,arm)
            self.assertEqual(old['response_schema'],q['response_schema'])
            for name,spec in q['response_schema']['properties'].items():
                if 'maxLength' not in spec:continue
                self.assertIn(f'{name}: at most {spec["maxLength"]} characters',body['messages'][0]['content'])
                self.assertFalse(list(jsonschema.Draft202012Validator(spec).iter_errors('x'*spec['maxLength'])))
                self.assertTrue(list(jsonschema.Draft202012Validator(spec).iter_errors('x'*(spec['maxLength']+1))))

    def test_existing_worst_case_wire_test_with_candidate(self):
        # Exercise the established maximal intermediary-message construction unchanged.
        from unittest.mock import patch
        from test_instrument import PeerPreparation
        class Shim:
            def __getattr__(self,name):return getattr(frozen,name)
            request=staticmethod(candidate.request)
            note_request=staticmethod(candidate.note_request)
        with patch('test_instrument.i',Shim()):
            PeerPreparation('test_maximum_note_and_action_payloads_fit').test_maximum_note_and_action_payloads_fit()


if __name__=='__main__':unittest.main()
