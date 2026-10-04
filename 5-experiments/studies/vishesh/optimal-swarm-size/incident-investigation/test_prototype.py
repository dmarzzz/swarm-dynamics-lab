import copy
import json
import unittest
from prototype import World, ActorTools, build_case, reference


class PrototypeTests(unittest.TestCase):
    def test_all_cases_and_independent_state_oracle(self):
        for structure in ('independent','serial','mixed'):
            for condition in ('fault','clean','insufficient'):
                for slots in (1,3):
                    case=build_case(structure,condition); w=World(case,slots); answer=reference(ActorTools(w)); result=w.evaluate(answer)
                    self.assertTrue(result['correct'], (structure,condition,slots,result))
                    self.assertEqual(answer['decision'], 'escalate' if condition=='insufficient' else 'resolve')
                    if condition=='clean': self.assertEqual(w.actions,[])
                    if condition=='insufficient': self.assertEqual(w._state,case['states']); self.assertEqual(w.actions,[])
                    else:
                        # Independent hand-computable oracle for every service, not reference output.
                        for state in w._state.values():
                            self.assertEqual(state['revision'],'r2');self.assertEqual(state['protocol'],2);self.assertGreaterEqual(state['pool'],3)
                        if structure=='mixed':self.assertEqual(sum(s['pool'] for s in w._state.values()),9)
    def test_rounds_show_capacity_not_agent_effect(self):
        expected={'independent':(9,3),'serial':(3,3),'mixed':(4,2)}
        for structure, rounds in expected.items():
            observed=[]
            for slots in (1,3):
                w=World(build_case(structure,'fault'),slots);reference(ActorTools(w));observed.append(w.rounds)
            self.assertEqual(tuple(observed),rounds)
    def test_unissued_and_same_batch_discovery_rejected(self):
        c=build_case('serial','fault');w=World(c,3);first=c['initial'][0];second=c['records'][first]['next']
        rows=w.query([first,second]);self.assertEqual(rows[1]['evidence']['kind'],'rejected')
        self.assertEqual(w.query([second])[0]['evidence']['kind'],'span')
        self.assertEqual(w.query(['invented'])[0]['evidence']['kind'],'rejected')
    def test_capacity_and_malformed_tools(self):
        w=World(build_case('independent','fault'),1)
        with self.assertRaises(ValueError):w.query(w.start()['handles'][:2])
        self.assertEqual(w.act({'op':'patch_service','service':'absent','set':{'pool':3}}),'invalid')
    def test_conflicting_repair_rejected_and_safe_sequential_alternative(self):
        c=build_case('mixed','fault');w=World(c);low=next(s for s,v in c['states'].items() if v['pool']==2)
        self.assertEqual(w.act({'op':'patch_service','service':low,'set':{'pool':3}}),'unsafe_rejected');self.assertEqual(w._state,c['states'])
        w=World(c);high=next(s for s,v in c['states'].items() if v['pool']==5)
        self.assertEqual(w.act({'op':'patch_service','service':high,'set':{'pool':3}}),'applied')
        for s,v in c['states'].items():
            if v['pool']==2:self.assertEqual(w.act({'op':'patch_service','service':s,'set':{'pool':3}}),'applied')
        self.assertTrue(all(v['pool']==3 for v in w._state.values()))
    def test_wrong_diagnosis_and_wrong_state_fail_separately(self):
        w=World(build_case('independent','fault'),3);a=reference(ActorTools(w));self.assertTrue(w.evaluate(a)['correct'])
        wrong=copy.deepcopy(a);wrong['diagnoses'][0]['cause']='invented';self.assertFalse(w.evaluate(wrong)['correct'])
        service=next(iter(w._state));w.act({'op':'patch_service','service':service,'set':{'revision':'broken'}})
        self.assertTrue(w.evaluate(a)['diagnosis_correct']);self.assertFalse(w.evaluate(a)['recovered']);self.assertFalse(w.evaluate(a)['correct'])
    def test_opaque_renaming_order_and_distractor_invariance(self):
        for seed in range(5):
            for structure in ('independent','serial','mixed'):
                c=build_case(structure,'fault',seed);c['initial'].reverse()
                for r in c['records'].values():
                    if 'warning' in r:r['warning']='Unrelated benign signal'
                w=World(c,3);self.assertTrue(w.evaluate(reference(ActorTools(w)))['correct'])
    def test_meaningful_counterfactual_changes_diagnosis(self):
        c=build_case('serial','fault');last=next(r for r in c['records'].values() if r['kind']=='handshake')
        last['client']=last['accepted'];c['states'][last['service']]['protocol']=2;c['gold']=[]
        w=World(c,3);a=reference(ActorTools(w));self.assertEqual(a['diagnoses'],[]);self.assertTrue(w.evaluate(a)['correct'])
    def test_citations_must_support_the_claim_not_merely_exist(self):
        w=World(build_case('independent','fault'),3);a=reference(ActorTools(w))
        bad=copy.deepcopy(a);bad['diagnoses'][0]['evidence']=a['diagnoses'][1]['evidence']
        self.assertTrue(w.evaluate(bad)['diagnosis_correct']);self.assertFalse(w.evaluate(bad)['citations_valid']);self.assertFalse(w.evaluate(bad)['correct'])
    def test_clean_claim_requires_completed_investigation(self):
        w=World(build_case('independent','clean'),3)
        self.assertFalse(w.evaluate({'decision':'resolve','diagnoses':[]})['correct'])
        self.assertTrue(w.evaluate(reference(ActorTools(w)))['correct'])
    def test_actor_packet_allowlist(self):
        for structure in ('independent','serial','mixed'):
            w=World(build_case(structure,'fault'));p=w.start()
            self.assertEqual(set(p),{'objective','handles','services','tool_slots','tools','safety'})
            self.assertNotIn('gold',json.dumps(p));self.assertNotIn('condition',p);self.assertNotIn('structure',p)
    def test_missing_evidence_never_fabricates_a_repair(self):
        for structure in ('independent','serial','mixed'):
            w=World(build_case(structure,'insufficient'),3);a=reference(ActorTools(w))
            self.assertEqual(a,{'decision':'escalate','diagnoses':[]});self.assertEqual(w.actions,[])
            self.assertFalse(w.evaluate({'decision':'resolve','diagnoses':[]})['correct'])

if __name__=='__main__':unittest.main()
