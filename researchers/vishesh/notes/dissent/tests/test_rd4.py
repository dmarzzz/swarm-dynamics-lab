import copy,itertools,json,sys,unittest
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from cases import make_case,digest
from protocol import actor_packet,validate_challenge,step,Ledger
from policies import ExactReference
import rd4_design as design

class RepairTests(unittest.TestCase):
    def test_duplicate_aliases_cannot_buy_checks_or_change_resolution(self):
        for truth in ('PROCEED','HOLD'):
            c=make_case(truth=truth);ledger=Ledger(max_checks=2)
            first=step(c,'always-check',ExactReference(),ledger)
            identity=next(iter(ledger.closed))
            for count in (1,2,8):
                other=copy.deepcopy(c);other['task'].update(now=1,deadline=3)
                original=next(e for e in other['evidence'] if e['id']=='e4')
                aliases=[]
                for i in range(count):
                    e=copy.deepcopy(original);e['id']='alias'+str(i);aliases.append(e)
                other['evidence']+=aliases
                other['challenge']['evidence_ids']=['e4']+[e['id'] for e in reversed(aliases)]
                self.assertEqual(validate_challenge(actor_packet(other),ledger.closed)[2],identity)
                result=step(other,'always-check',ExactReference(),ledger)
                self.assertEqual(result['final'],first['final']);self.assertEqual(result['checks'],0)
            self.assertEqual(ledger.checks,1)
    def test_switching_requested_action_does_not_create_observation(self):
        c=make_case();p=actor_packet(c);key=validate_challenge(p,set())[2]
        p['challenge']['alternative'],p['challenge']['withdraw_if']=p['challenge']['withdraw_if'],p['challenge']['alternative']
        self.assertEqual(validate_challenge(p,set())[2],key)
    def test_version_change_invalidates_old_closure(self):
        c=make_case();ledger=Ledger(max_checks=2);step(c,'always-check',ExactReference(),ledger)
        c=copy.deepcopy(c);c['task'].update(revision='v2',now=1)
        for e in c['evidence']:e['revision']='v2'
        c['verification']['record']['revision']='v2'
        r=step(c,'always-check',ExactReference(),ledger)
        self.assertEqual(r['checks'],1);self.assertEqual(ledger.checks,2)
    def test_expired_closure_does_not_authorize_old_action(self):
        c=make_case();ledger=Ledger(max_checks=2);step(c,'always-check',ExactReference(),ledger)
        c=copy.deepcopy(c);c['task'].update(now=8,deadline=10)
        self.assertEqual(step(c,'always-check',ExactReference(),ledger)['final'],'DEFER')
    def test_new_observation_reopens_with_same_speaker(self):
        c=make_case();ledger=Ledger(max_checks=2);step(c,'always-check',ExactReference(),ledger)
        c=copy.deepcopy(c);c['task'].update(now=1,deadline=3)
        next(e for e in c['evidence'] if e['id']=='e4')['observed_at']=1
        self.assertEqual(step(c,'always-check',ExactReference(),ledger)['checks'],1)
    def test_same_source_conflicting_reports_not_merged_or_independent(self):
        c=make_case();p=actor_packet(c);e=copy.deepcopy(p['records'][-1]);e['id']='conflict';e['text']='Conflicting report.'
        # Select the actual cited source, not shuffled position.
        e=copy.deepcopy(next(e for e in p['records'] if e['id']=='e4'));e.update(id='conflict',text='Conflicting report.')
        old=validate_challenge(p,set())[2];p['records'].append(e);p['challenge']['evidence_ids'].append('conflict')
        self.assertNotEqual(old,validate_challenge(p,set())[2]);self.assertEqual(len({x['root'] for x in p['records']}),2)
    def test_qualification_refuses_implicit_construction(self):
        with self.assertRaisesRegex(ValueError,'explicit_prepare'):design.qualification()
    def test_development_path_cannot_touch_native_qualification(self):
        with patch.object(design,'qualification',side_effect=AssertionError('reserved touched')):
            self.assertEqual(len(design.assignments('S4')),144)
    def test_matrix_and_temporal_oracle(self):
        for c in design.trajectories():
            rows=design.execute(c,'always-check',design.GrammarReference())
            self.assertTrue(all(x['correct_completion'] for x in rows),(c['scenario'],c['condition'],rows))
            self.assertEqual([r['checks'] for r in rows],([1,0,0,1] if c['condition'] in ('supported','withdrawn') else [0,0,0,1]))
    def test_policy_wording_diff_only(self):
        p=actor_packet(design.trajectories()[0]);a=design.wire('admission',p);b=design.wire('symmetric',p)
        self.assertEqual(list(a['questions']['action']['criteria']),list(b['questions']['action']['criteria']))
        a['questions']['action'].pop('criteria');b['questions']['action'].pop('criteria');self.assertEqual(a,b)
    def test_no_evaluator_leak(self):
        c=design.trajectories()[0]['frames'][0];a=actor_packet(c);c['gold']['action']='CANARY';c['condition']='CANARY';c['future']='CANARY';self.assertEqual(a,actor_packet(c))
    def test_frozen_requests_cover_divergent_policy_actions(self):
        with patch.object(design,'qualification',side_effect=AssertionError('reserved touched')):allowed=design.frozen_requests('S4')
        for gate,action in itertools.product(('CHECK','KEEP','DEFER'),('PROCEED','HOLD','DEFER')):
            def policy(phase,p):
                req=design.wire(phase,p);self.assertIn(digest(req),allowed)
                return gate if phase in ('admission','symmetric') else action
            for c in design.trajectories():
                for arm in design.ARMS:design.execute(c,arm,policy)
    def test_template_reference_negation_and_optional_checks(self):
        for domain in design.DOMAINS:
            for action in ('PROCEED','HOLD'):
                for form in range(3):
                    p={'task':design.task(domain,'fixture'),'records':[design.record(domain,action,'fixture',0,form=form)]}
                    self.assertEqual(design.GrammarReference()('resolve',p),action)

if __name__=='__main__':unittest.main()
