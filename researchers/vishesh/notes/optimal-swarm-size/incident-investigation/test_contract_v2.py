import copy,json,unittest
from prototype import ActorTools,build_case,reference
from contract_v2 import ContractWorld,canonical_answer,PUBLIC_CONTRACT,CAUSE_ALIASES


def investigate(w):
    while w.coverage()['pending']:
        w.query(w.coverage()['pending'][:w.slots])


class ContractTests(unittest.TestCase):
    def test_all_reference_case_types_and_slots(self):
        for structure in ('independent','serial','mixed'):
            for condition in ('fault','clean','insufficient'):
                for slots in (1,3):
                    w=ContractWorld(build_case(structure,condition,31),slots)
                    a=reference(ActorTools(w));r=w.evaluate(a)
                    self.assertTrue(r['joint_correct'],(structure,condition,slots))
                    if condition=='insufficient':
                        self.assertIsNone(r['identified_fault']);self.assertEqual(r['actions_attempted'],0)
                    if condition=='fault':self.assertGreater(r['actions_applied'],0)
    def test_unknown_rejected_repeated_handles_do_not_poison_coverage(self):
        w=ContractWorld(build_case('independent','fault',31),3)
        w.query(['unknown']);self.assertFalse(w.coverage()['complete'])
        investigate(w);before=w.coverage();w.query(['unknown']);w.query([before['issued'][0]])
        self.assertEqual(w.coverage(),before)
        a=reference(ActorTools(w));self.assertTrue(w.evaluate(a)['joint_correct'])
    def test_rejected_same_batch_new_handle_does_not_satisfy_coverage(self):
        c=build_case('serial','fault',31);w=ContractWorld(c,3);first=c['initial'][0];second=c['records'][first]['next']
        result=w.query([first,second]);self.assertEqual(result[1]['evidence']['kind'],'rejected')
        self.assertIn(second,w.coverage()['pending']);self.assertNotIn(second,w.coverage()['investigated'])
        self.assertTrue(w.evaluate(reference(ActorTools(w)))['joint_correct'])
    def test_repeated_handles_cannot_fake_progress(self):
        w=ContractWorld(build_case('independent','fault'),3);h=w.start()['handles'][0]
        w.query([h]);w.query([h]);self.assertEqual(len(w.coverage()['investigated']),1)
        with self.assertRaises(ValueError):w.query([h,h])
    def test_mutation_before_investigation_is_rejected(self):
        w=ContractWorld(build_case('serial','fault'),3);old=copy.deepcopy(w._state)
        self.assertEqual(w.act({'op':'patch_service','service':next(iter(old)),'set':{'protocol':2}}),'contract_rejected')
        self.assertEqual(old,w._state)
    def test_missing_blocks_mutations_and_unobserved_escalation_fails(self):
        w=ContractWorld(build_case('mixed','insufficient'),3);a={'decision':'escalate','diagnoses':[]}
        self.assertFalse(w.evaluate(a)['joint_correct']);investigate(w);self.assertTrue(w.evaluate(a)['joint_correct'])
        old=copy.deepcopy(w._state);w.act({'op':'rebalance','allocations':{s:3 for s in old}})
        self.assertEqual(old,w._state);self.assertFalse(w.evaluate(a)['joint_correct'])
    def test_all_declared_lexical_aliases(self):
        for alias,canonical in CAUSE_ALIASES.items():
            a={'decision':'resolve','diagnoses':[{'service':'shared_pool' if canonical=='allocation' else 'service-x','cause':alias,'evidence':['trace-x']}]}
            r=canonical_answer(a);self.assertEqual(r['diagnoses'][0]['cause'],canonical)
            if canonical=='allocation':self.assertEqual(r['diagnoses'][0]['service'],'shared-pool')
            self.assertEqual(a['diagnoses'][0]['cause'],alias)
    def test_no_fuzzy_alias_or_extra_fields(self):
        for d in ({'service':'s','cause':'network issue','evidence':['h']}, {'service':'s','cause':'protocol','evidence':['h'],'rationale':'guess'}, {'service':'s','cause':'protocol','evidence':[]}):
            with self.assertRaises(ValueError):canonical_answer({'decision':'resolve','diagnoses':[d]})
    def test_same_service_label_is_not_silently_pool_equivalence(self):
        w=ContractWorld(build_case('mixed','fault'),3);a=reference(ActorTools(w));bad=copy.deepcopy(a)
        bad['diagnoses'][0]['service']=next(iter(w._state));self.assertFalse(w.evaluate(bad)['joint_correct'])
        a['diagnoses'][0].update(service='shared_pool',cause='shared_allocation');self.assertTrue(w.evaluate(a)['joint_correct'])
    def test_fabricated_or_incomplete_citations_fail(self):
        w=ContractWorld(build_case('mixed','fault'),3);a=reference(ActorTools(w))
        for evidence in (['invented'],a['diagnoses'][0]['evidence'][:2]):
            bad=copy.deepcopy(a);bad['diagnoses'][0]['evidence']=evidence
            r=w.evaluate(bad);self.assertTrue(r['actual_recovery']);self.assertFalse(r['cited_evidence_supported']);self.assertFalse(r['joint_correct'])
    def test_identification_is_not_repair(self):
        c=build_case('serial','fault');w=ContractWorld(c,3);investigate(w)
        h=next(h for h,r in c['records'].items() if r['kind']=='handshake')
        a={'decision':'resolve','diagnoses':[{'service':c['records'][h]['service'],'cause':'protocol','evidence':[h]}]}
        r=w.evaluate(a);self.assertTrue(r['identified_fault']);self.assertTrue(r['cited_evidence_supported']);self.assertEqual(r['actions_applied'],0);self.assertFalse(r['actual_recovery']);self.assertFalse(r['joint_correct'])
    def test_safe_shared_capacity_still_enforced(self):
        c=build_case('mixed','fault');w=ContractWorld(c,3);investigate(w)
        self.assertEqual(w.act({'op':'rebalance','allocations':{s:4 for s in w._state}}),'unsafe_rejected')
        self.assertEqual(w._state,c['states'])
    def test_duplicate_diagnoses_fail(self):
        w=ContractWorld(build_case('serial','fault'),3);a=reference(ActorTools(w));a['diagnoses']*=2
        self.assertFalse(w.evaluate(a)['joint_correct'])
    def test_actor_conventions_are_explicit_without_gold(self):
        for structure in ('independent','serial','mixed'):
            w=ContractWorld(build_case(structure,'fault'),3);packet=w.start()
            self.assertEqual(packet['contract'],PUBLIC_CONTRACT);self.assertIn('patch_service',packet['tools']);self.assertNotIn('patch',packet['tools'])
            self.assertNotIn('gold',packet);self.assertNotIn('condition',packet);self.assertNotIn('structure',packet)
            self.assertIn('all service metrics',packet['contract']['diagnosis_rules']['allocation'])

if __name__=='__main__':unittest.main()
