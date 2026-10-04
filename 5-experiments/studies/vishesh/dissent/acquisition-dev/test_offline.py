from copy import deepcopy
import json
import unittest
from episodes import build, digest
from engine import (Episode, actor_projection, selection_request, final_request, resolve,
                    neutral_reference, routine, replay, validate_world, eligibility_receipt)


class AcquisitionTests(unittest.TestCase):
    def setUp(self):self.worlds=build()

    def test_all_hand_authored_counterfactual_labels(self):
        self.assertEqual(sum(len(validate_world(w)) for w in self.worlds),18)

    def test_neutral_uses_unresolved_coverage(self):
        choices=[neutral_reference(actor_projection(w)) for w in self.worlds]
        self.assertEqual(choices,['B','B','A','A','NONE','A'])

    def test_routine_is_authority_aware_and_preserves_its_coverage_miss(self):
        choices=[routine(actor_projection(w)) for w in self.worlds]
        self.assertEqual(choices,['B','A','A','A','NONE','A'])
        self.assertEqual(replay(self.worlds[1],choices[1])['event']['resolution']['action'],'DEFER')

    def test_no_private_evaluator_or_counterfactual_fields_in_selection(self):
        for w in self.worlds:
            w=deepcopy(w);w['rationale']='PRIVATE_SENTINEL';w['gold_by_choice']['NONE']='PRIVATE_SENTINEL'
            for s in w['sources']:s['response'][0]['text']='FUTURE_SENTINEL'
            request=json.dumps(selection_request(actor_projection(w),'neutral'))
            for value in ['PRIVATE_SENTINEL','FUTURE_SENTINEL','gold_by_choice','structural_family','mechanism',w['id']]:
                self.assertNotIn(value,request)

    def test_roles_differ_only_in_selection_instruction(self):
        for w in self.worlds:
            actor=actor_projection(w);a=selection_request(actor,'neutral');b=selection_request(actor,'challenge')
            self.assertNotEqual(a.pop('instructions'),b.pop('instructions'));self.assertEqual(a,b)

    def test_selector_cannot_observe_counterfactual_mutation(self):
        for w in self.worlds:
            other=deepcopy(w)
            for s in other['sources']:
                s['response'][0]['facts']={p:not v for p,v in s['response'][0]['facts'].items()}
            a=actor_projection(w);b=actor_projection(other)
            self.assertEqual(a,b);self.assertEqual(routine(a),routine(b));self.assertEqual(neutral_reference(a),neutral_reference(b))

    def test_only_selected_source_is_delivered(self):
        for w in self.worlds:
            for source in w['sources']:
                ep=Episode(w);ep.select(source['id'])
                self.assertEqual(ep.actor['observations'][len(w['initial']):],source['response'])

    def test_second_check_and_none_then_check_rejected(self):
        for first in ['NONE','A']:
            ep=Episode(self.worlds[0]);ep.select(first)
            with self.assertRaisesRegex(ValueError,'already_selected'):ep.select('B')

    def test_deadline_and_credit_limit(self):
        for field,value in [('deadline',100)]:
            w=deepcopy(self.worlds[0]);w['task'][field]=value
            with self.assertRaisesRegex(ValueError,'unavailable_choice'):Episode(w).select('B')
        w=deepcopy(self.worlds[0]);w['budget']['credits']=0
        with self.assertRaisesRegex(ValueError,'unavailable_choice'):Episode(w).select('B')

    def test_negative_cost_and_latency_rejected(self):
        for field in ['cost','latency']:
            w=deepcopy(self.worlds[0]);w['sources'][0][field]=-1
            with self.assertRaises(ValueError):actor_projection(w)

    def test_source_spoof_or_undeclared_fact_rejected_without_spending(self):
        for kind in ['origin','coverage','authority']:
            w=deepcopy(self.worlds[0]);s=w['sources'][1]
            if kind=='origin':s['response'][0]['origin']='A'
            elif kind=='coverage':s['response'][0]['facts']['unknown']=True
            else:s['authority']=9
            ep=Episode(w);before=deepcopy(ep.actor)
            with self.assertRaises(ValueError):ep.select('B')
            self.assertEqual(ep.actor,before);self.assertFalse(ep.terminal)

    def test_ttl_inclusive_future_scope_revision(self):
        a=actor_projection(self.worlds[4]);a['observations']=a['observations'][:1]
        a['observations'][0]['observed_at']=93
        self.assertEqual(resolve(a)['action'],'PROCEED')
        for field,value in [('observed_at',92),('observed_at',101),('scope','other'),('revision','r0')]:
            b=deepcopy(a);b['observations'][0][field]=value
            self.assertEqual(resolve(b)['action'],'DEFER')

    def test_authority_and_conflict_controls(self):
        self.assertEqual(resolve(actor_projection(self.worlds[2]))['action'],'DEFER')
        conflict=actor_projection(self.worlds[3]);self.assertEqual(resolve(conflict)['predicate_states']['inspection_clear'],'conflict')
        self.assertEqual(replay(self.worlds[3],'A')['event']['resolution']['action'],'PROCEED')
        self.assertEqual(replay(self.worlds[3],'B')['event']['resolution']['action'],'DEFER')

    def test_optional_expiry_does_not_stop_legitimate_service(self):
        self.assertEqual(resolve(actor_projection(self.worlds[4]))['action'],'PROCEED')
        self.assertEqual(neutral_reference(actor_projection(self.worlds[4])),'NONE')

    def test_one_check_unresolved_but_illegal_two_checks_would_change_answer(self):
        w=self.worlds[5]
        self.assertTrue(all(replay(w,c)['event']['resolution']['action']=='DEFER' for c in ['NONE','A','B']))
        hypothetical=actor_projection(w)
        hypothetical['observations']=[d for s in w['sources'] for d in s['response']]
        self.assertEqual(resolve(hypothetical)['action'],'PROCEED')

    def test_final_gate_receipt_and_common_resolver(self):
        a=actor_projection(self.worlds[0]);req=final_request(a)
        self.assertEqual(req['state']['observations'],[])
        self.assertEqual(req['state']['eligibility']['eligible_count'],0)
        self.assertNotIn('action',req['state'])

    def test_recorder_deterministic_replay(self):
        for w in self.worlds:
            choice=neutral_reference(actor_projection(w))
            self.assertEqual(digest(replay(w,choice)),digest(replay(w,choice)))

    def test_fault_actions_do_not_pass_all_cases(self):
        gold=[v for w in self.worlds for v in w['gold_by_choice'].values()]
        for action in ['PROCEED','HOLD','DEFER']:self.assertLess(sum(v==action for v in gold),len(gold))
        a=actor_projection(self.worlds[0]);a['task']['ttl']=999
        self.assertNotEqual(resolve(a)['action'],self.worlds[0]['gold_by_choice']['NONE'])

    def test_catalog_order_invariance(self):
        for w in self.worlds:
            a=actor_projection(w);b=deepcopy(a);b['catalog'].reverse()
            self.assertEqual(routine(a),routine(b));self.assertEqual(neutral_reference(a),neutral_reference(b))

    def test_identifier_renaming_not_family_diversity(self):
        for w in self.worlds:
            a=actor_projection(w);b=deepcopy(a);rename={s['id']:'renamed-'+s['id'] for s in b['catalog']}
            for s in b['catalog']:s['id']=rename[s['id']]
            b['task']['source_authorities']={rename.get(k,k):v for k,v in b['task']['source_authorities'].items()}
            for d in b['observations']:d['origin']=rename.get(d['origin'],d['origin'])
            for policy in [routine,neutral_reference]:self.assertEqual(policy(b),rename.get(policy(a),policy(a)))
        self.assertEqual(len({w['structural_family'] for w in self.worlds}),3)


if __name__=='__main__':unittest.main()
