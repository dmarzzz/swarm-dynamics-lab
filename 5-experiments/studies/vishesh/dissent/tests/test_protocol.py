import copy,json,math,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cases import make_case,development_examples,digest
from protocol import actor_packet,validate_challenge,step,episode,summarize,Ledger,majority
from policies import ExactReference,TapePolicy
from jev import request,validate
from launch import readiness

class ProtocolTests(unittest.TestCase):
    def test_correct_dissent_repairs_wrong_majority(self):
        r=step(make_case(), 'evidence-gate', ExactReference())
        self.assertTrue(r['correction']);self.assertEqual(r['checks'],1);self.assertEqual(r['final'],'HOLD')
    def test_wrong_dissent_withdraws(self):
        r=step(make_case(truth='PROCEED'), 'evidence-gate', ExactReference())
        self.assertTrue(r['correct_completion']);self.assertEqual(r['closure'],'withdrawn');self.assertFalse(r['corruption'])
    def test_blind_veto_causes_harm(self):
        r=step(make_case(truth='PROCEED'), 'blind-veto', ExactReference())
        self.assertTrue(r['corruption']);self.assertEqual(r['checks'],0)
    def test_reverse_direction_is_not_special(self):
        r=step(make_case(truth='PROCEED',majority='HOLD'), 'evidence-gate', ExactReference())
        self.assertTrue(r['correction']);self.assertEqual(r['final'],'PROCEED')
    def test_scope_and_stale_rejected(self):
        for variant in ('wrong_scope','stale'):
            r=step(make_case(variant=variant), 'evidence-gate', ExactReference())
            self.assertEqual(r['checks'],0);self.assertEqual(r['final'],'PROCEED')
    def test_missing_check_remains_in_denominator(self):
        r=step(make_case(variant='no_check'), 'always-check', ExactReference())
        self.assertEqual(r['status'],'unavailable');self.assertEqual(summarize([r])['assigned_decisions'],1)
        self.assertEqual(summarize([r])['correct_on_time_rate'],0)
    def test_late_correct_observation_not_success(self):
        r=step(make_case(variant='late'), 'always-check', ExactReference())
        self.assertEqual(r['status'],'late');self.assertFalse(r['correct_completion'])
    def test_check_budget_enforced(self):
        r=step(make_case(), 'always-check', ExactReference(),Ledger(max_checks=0))
        self.assertEqual(r['final'],'DEFER');self.assertEqual(r['checks'],0)
    def test_absent_challenge_no_tool(self):
        r=step(make_case(variant='absent'), 'always-check', ExactReference())
        self.assertEqual(r['reason'],'absent');self.assertEqual(r['checks'],0)
    def test_noisy_verifier_can_cause_false_reversal(self):
        r=step(make_case(variant='noisy_check',truth='PROCEED'), 'always-check', ExactReference())
        self.assertTrue(r['corruption'])
    def test_temporal_withdraw_repeat_and_reopen(self):
        rows=episode(make_case('alarm'), 'evidence-gate', ExactReference())
        self.assertEqual([r['closure'] for r in rows],['withdrawn','suppressed_repeat','supported'])
        self.assertEqual(sum(r['checks'] for r in rows),2)
        self.assertTrue(all(r['correct_completion'] for r in rows))
    def test_same_ancestry_new_id_is_not_new_evidence(self):
        c=make_case();ledger=Ledger(max_checks=2)
        step(c,'always-check',ExactReference(),ledger)
        d=copy.deepcopy(c)
        next(e for e in d['evidence'] if e['id']=='e4')['id']='new-alias'
        d['challenge']['evidence_ids']=['new-alias']
        r=step(d,'always-check',ExactReference(),ledger)
        self.assertEqual(r['closure'],'suppressed_repeat');self.assertEqual(r['checks'],0)
    def test_unknown_or_duplicate_citation_rejected(self):
        for ids in (['hidden'],['e4','e4'],[]):
            c=make_case();c['challenge']['evidence_ids']=ids
            self.assertFalse(validate_challenge(actor_packet(c),set())[0])
    def test_expired_or_future_evidence(self):
        c=make_case();c['challenge']['expires_at']=-1
        self.assertEqual(validate_challenge(actor_packet(c),set())[1],'expired')
        c=make_case();next(e for e in c['evidence'] if e['id']=='e4')['observed_at']=9
        self.assertEqual(validate_challenge(actor_packet(c),set())[1],'stale_or_future')
    def test_no_gold_or_condition_leak_and_mutation(self):
        c=make_case();before=actor_packet(c)
        c['gold']['action']='PROCEED';c['condition']='EVALUATOR_SECRET';c['seed']=6188
        c['evidence'][0]['gold_correct']=True
        c['task']['future_truth']='HOLD'
        self.assertEqual(before,actor_packet(c))
        self.assertNotIn('gold',json.dumps(actor_packet(c)))
    def test_policy_cannot_mutate_world(self):
        c=make_case();before=copy.deepcopy(c)
        def p(phase,packet):
            packet['records'].clear()
            return 'CHECK' if phase=='admission' else 'HOLD'
        step(c,'evidence-gate',p);self.assertEqual(c,before)
    def test_failure_is_not_silent_majority(self):
        def broken(*args):raise RuntimeError('secret-value-that-must-not-appear')
        r=step(make_case(),'evidence-gate',broken)
        self.assertEqual(r['status'],'failed');self.assertEqual(r['final'],'DEFER')
        self.assertNotIn('secret-value',json.dumps(r))
    def test_invalid_policy_output(self):
        r=step(make_case(),'evidence-gate',lambda *args:'invented')
        self.assertEqual(r['status'],'failed')
    def test_tie_and_invalid_votes(self):
        self.assertEqual(majority(['HOLD','PROCEED']),'DEFER')
        with self.assertRaises(ValueError):majority(['yes'])
    def test_zero_denominators_are_null(self):
        self.assertIsNone(summarize([])['correct_on_time_rate'])
        r=step(make_case(),'majority',ExactReference())
        self.assertIsNone(summarize([r])['harmful_reversal_rate'])
    def test_matched_random_false_spends_nothing(self):
        r=step(make_case(),'matched-random',ExactReference(),random_check=False)
        self.assertEqual(r['checks'],0)
    def test_reproducible_case_and_reserved_seed_guard(self):
        self.assertEqual(make_case(),make_case())
        with self.assertRaises(ValueError):make_case(seed=6100)
    def test_report_order_does_not_change_exact_check(self):
        a=make_case();b=copy.deepcopy(a);b['evidence'].reverse()
        self.assertEqual(step(a,'always-check',ExactReference())['final'],step(b,'always-check',ExactReference())['final'])
    def test_public_packet_contains_no_check_before_acquisition(self):
        self.assertNotIn('check_record',actor_packet(make_case()))
    def test_all_three_scenario_contracts(self):
        for c in development_examples():
            r=episode(c,'always-check',ExactReference())
            self.assertTrue(all(x['events'][-1]['phase']=='resolution' for x in r))

class WireTests(unittest.TestCase):
    def setUp(self):
        self.req=request('resolve',actor_packet(make_case()))
        self.response={'model':'fixed-snapshot','provider':'TypeSafe','answers':{'action':{'choice':'HOLD','probabilities':{'PROCEED':0.1,'HOLD':0.8,'DEFER':0.1},'confidence':0.7}},'usage':{'input_tokens':100,'cost':0.00001}}
    def test_valid_wire(self):self.assertEqual(validate(self.response,self.req,'fixed-snapshot')['action'],'HOLD')
    def test_probability_mutations(self):
        for value in (True,float('nan'),1.5,-.1):
            d=copy.deepcopy(self.response);d['answers']['action']['probabilities']['HOLD']=value
            with self.assertRaises(ValueError):validate(d,self.req,'fixed-snapshot')
    def test_confidence_boolean_rejected(self):
        self.response['answers']['action']['confidence']=True
        with self.assertRaises(ValueError):validate(self.response,self.req,'fixed-snapshot')
    def test_provider_and_snapshot_checked(self):
        for key in ('model','provider'):
            d=copy.deepcopy(self.response);d[key]='other'
            with self.assertRaises(ValueError):validate(d,self.req,'fixed-snapshot')
    def test_choice_must_match_maximum(self):
        self.response['answers']['action']['choice']='PROCEED'
        with self.assertRaises(ValueError):validate(self.response,self.req,'fixed-snapshot')
    def test_missing_or_extra_labels_rejected(self):
        self.response['answers']['action']['probabilities']['EXTRA']=0
        with self.assertRaises(ValueError):validate(self.response,self.req,'fixed-snapshot')
    def test_tape_exact_binding_and_duplicates(self):
        row={'request':self.req,'request_sha256':digest(self.req),'response':self.response}
        p=TapePolicy([row],'fixed-snapshot')
        self.assertEqual(p('resolve',actor_packet(make_case())),'HOLD')
        with self.assertRaises(ValueError):TapePolicy([row,row],'fixed-snapshot')
        with self.assertRaises(ValueError):p('resolve',actor_packet(make_case(seed=1102)))
    def test_live_gate_closed_by_default(self):
        r=readiness({});self.assertFalse(r['ready_for_executor_review']);self.assertFalse(r['native_dispatch_available'])
    def test_request_does_not_contain_credential(self):
        self.assertNotIn('Authorization',json.dumps(self.req));self.assertEqual(self.req['provider']['allow_fallbacks'],False)

if __name__=='__main__':unittest.main()
