import copy, json, unittest
from itertools import product
from instrument import *

class TransmissionTests(unittest.TestCase):
    def setUp(self):
        self.world=make_world(11000,'stable_exception');self.inst=Institution(self.world)
    def test_separate_exhaustive_truth_reference(self):
        for role in ROLES:
            for bits in product((0,1),repeat=6):
                values=[list(bits[i:i+2]) for i in (0,2,4)]
                for source in range(3):
                    expected=truth(role,values,source)
                    self.assertIn(source,compatible(role,[{'readings':values,'outcome':expected}]))
                    self.assertNotIn(source,compatible(role,[{'readings':values,'outcome':not expected}]))
    def test_founder_identifiability_all_permutations(self):
        for seed in range(11000,11030):
            w=make_world(seed,'stable_exception')
            for role,d in w['roles'].items():self.assertEqual(compatible(role,d['history']),[d['source']])
    def test_disjoint_train_and_test_patterns(self):
        for d in self.world['roles'].values():
            self.assertFalse({digest(h['readings']) for h in d['history']} & {digest(h['readings']) for h in d['tests']})
    def test_novice_has_no_ancestor_history_or_truth(self):
        for phase in ('question','commit'):
            p=self.inst.packet('release',phase)
            self.assertEqual(set(p),{'role','phase','rules','note','current_evidence','question','answer','cases'})
    def test_case_payload_is_actor_only(self):
        for d in self.world['roles'].values():
            for c in d['tests']:self.assertEqual(set(c),{'id','readings'})
    def test_private_history_not_mutable_through_packet(self):
        p=self.inst.packet('release','answer');p['private_history'].clear()
        self.assertTrue(self.inst.active('founder-release').private_history)
    def test_retired_member_cannot_answer(self):
        old=self.inst.current['release'];self.inst.replace('release',self.inst.active(old).note)
        with self.assertRaises(ValueError):self.inst.active(old)
    def test_two_complete_replacement_cycles(self):
        reference_round(self.inst);one=set(self.inst.current.values());reference_round(self.inst)
        self.assertFalse(one & set(self.inst.current.values()))
        self.assertEqual(sum(m.active for m in self.inst.members.values()),3)
        self.assertEqual(len(self.inst.events),6)
    def test_successors_inherit_only_transmitted_evidence(self):
        old=self.inst.active('founder-release');new=self.inst.replace('release',old.note)
        self.assertEqual(self.inst.active(new).private_history,read_note('release',old.note)['evidence'])
        self.assertLess(len(self.inst.active(new).private_history),len(old.private_history))
    def test_source_change_is_selective(self):
        w=make_world(11001,'changed_practice');i=Institution(w);reference_round(i)
        rows=reference_round(i,w['events']);self.assertEqual([r['state'] for r in rows],['revise','retain','retain'])
    def test_contradiction_and_ambiguity(self):
        w=make_world(11002,'unreliable_evidence');i=Institution(w);reference_round(i)
        rows=reference_round(i,w['events']);self.assertEqual([r['state'] for r in rows],['retain','quarantine','provisional'])
        self.assertEqual(rows[1]['actions'],['defer']*8)
    def test_ambiguous_unanimous_case_keeps_service(self):
        c={'readings':[[0,0]]*3};self.assertEqual(robust_action('release',c,[0,1,2]),'hold')
        self.assertEqual(robust_action('release',{'readings':[[1,1],[0,0],[0,0]]},[0,1,2]),'defer')
    def test_no_evidence_cannot_promote(self):
        self.assertEqual(evidence_decision('release',0,[])['state'],'provisional')
    def test_nuisance_reordering_renaming(self):
        for role,d in self.world['roles'].items():
            hist=copy.deepcopy(d['history']);hist.reverse()
            for h in hist:h['id']='opaque-renamed';h['irrelevant']='memo'
            self.assertEqual(compatible(role,hist),[d['source']])
    def test_wrong_source_has_visible_counterexample(self):
        for role,d in self.world['roles'].items():
            for other in set(range(3))-{d['source']}:
                self.assertTrue(any(truth(role,h['readings'],other)!=h['outcome'] for h in d['history']))
    def test_message_note_limits_fail_not_truncate(self):
        with self.assertRaises(ValueError):self.inst.packet('release','question',question='x'*401)
        with self.assertRaises(ValueError):self.inst.replace('release','x'*1201)
    def test_wrong_role_note_rejected(self):
        with self.assertRaises(ValueError):self.inst.replace('release',self.inst.active('founder-incident').note)
    def test_static_and_broken_contrast(self):
        p=self.inst.packet('release','commit',arm='static',answer='teacher-secret')
        self.assertTrue(p['note']);self.assertEqual(p['answer'],'')
        p=self.inst.packet('release','commit',arm='broken',answer='teacher-secret');self.assertEqual(p['note'],'');self.assertEqual(p['answer'],'')
    def test_manifest_no_native_permission_and_envelope(self):
        m=qualification_manifest();self.assertEqual(len(m['assignments']),72);self.assertFalse(m['native_dispatch_enabled'])
        self.assertEqual(len({a['id'] for a in m['assignments']}),72)
        self.assertLessEqual(72*(16000+1024*5)/1e6*1.1,1.70)
        self.assertLess(m['prior_exposure_usd']+m['total_cap_usd'],m['original_cap_usd'])
    def test_missing_prerequisites_preserved(self):
        m=qualification_manifest();r=reconcile(m,{m['assignments'][0]['id']:'failed'})
        self.assertEqual(len(r),72);self.assertEqual(list(r.values()).count('unstarted'),71)
        with self.assertRaises(ValueError):reconcile(m,{'fake':'complete'})
    def test_founder_packet_never_receives_scripted_gold_note(self):
        self.assertEqual(self.inst.packet('release','founder')['note'],'')
    def test_unknown_policy_stays_provisional(self):
        self.assertEqual(evidence_decision('release',None,[])['state'],'provisional')
    def test_case_and_current_evidence_reject_extra_fields(self):
        with self.assertRaises(ValueError): self.inst.packet('release','commit',cases=[{'id':'x','readings':[], 'gold':1}])
        with self.assertRaises(ValueError): self.inst.packet('release','commit',current_evidence=[{'id':'x','private_truth':1}])
    def test_heldout_cases_have_service_and_harm_opportunities(self):
        for seed in range(11000,11030):
            for role,d in make_world(seed,'stable_exception')['roles'].items():
                positives=sum(truth(role,c['readings'],d['source']) for c in d['tests'])
                self.assertGreaterEqual(positives,2);self.assertLessEqual(positives,6)
                for wrong in set(range(3))-{d['source']}:
                    self.assertTrue(any(truth(role,c['readings'],wrong)!=truth(role,c['readings'],d['source']) for c in d['tests']))
    def test_founder_and_successor_panels_are_disjoint(self):
        for d in self.world['roles'].values():
            groups=[{digest(r['readings']) for r in d[k]} for k in ('history','founder_tests','tests')]
            for i,j in ((0,1),(0,2),(1,2)):self.assertFalse(groups[i]&groups[j])
    def example_response(self):
        d=self.world['roles']['release']; note=self.inst.active('founder-release').note
        return d,{'note':note,'actions':[{'id':c['id'],'action':robust_action('release',c,[d['source']])} for c in d['tests']]}
    def test_semantic_score_exact_reference(self):
        d,r=self.example_response();self.assertTrue(score_response('release',d['tests'],d['history'],d['source'],r,d['history'])['qualified'])
    def test_hidden_evidence_cannot_validate_a_note(self):
        d,r=self.example_response();s=score_response('release',d['tests'],d['history'],d['source'],r,[])
        self.assertTrue(s['policy_correct']);self.assertFalse(s['qualified'])
    def test_duplicate_action_ids_do_not_pass(self):
        d,r=self.example_response();r['actions'][1]=r['actions'][0]
        self.assertFalse(score_response('release',d['tests'],d['history'],d['source'],r,d['history'])['valid'])
    def test_wrong_but_valid_policy_is_not_repaired(self):
        d,r=self.example_response();note=json.loads(r['note']);note['source']=(d['source']+1)%3;r['note']=json.dumps(note)
        original=copy.deepcopy(r);s=score_response('release',d['tests'],d['history'],d['source'],r,d['history'])
        self.assertTrue(s['valid']);self.assertFalse(s['policy_correct']);self.assertEqual(r,original)
    def test_actor_note_rejects_extra_gold_fields(self):
        d,r=self.example_response();note=json.loads(r['note']);note['hidden_truth']='leak'
        with self.assertRaises(ValueError):read_note('release',json.dumps(note))
    def test_fixture_only_validation(self):
        r=validate();self.assertEqual(r['native_calls'],0);self.assertEqual(r['exact_founder_policies'],54)
        self.assertEqual(r['two_cycle_rosters_verified'],18)

if __name__=='__main__':unittest.main()
