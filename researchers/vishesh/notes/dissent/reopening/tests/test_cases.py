"""Known-answer, context-invariant and scorer fault fixtures; no provider access."""
from copy import deepcopy
import importlib.util
import json
from pathlib import Path
import sys
import unittest

BASE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(BASE))
from cases import ACTIONS, CONDITIONS, build, definition, digest, make_case, reference, request_for, score


def diff(a, b, prefix=''):
    if type(a) != type(b):
        return {prefix}
    if isinstance(a, dict):
        out = set()
        for key in a.keys() | b.keys():
            if key not in a or key not in b:
                out.add(prefix+'/'+key)
            else:
                out |= diff(a[key], b[key], prefix+'/'+key)
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return {prefix}
        return set().union(*(diff(x, y, prefix+'/'+str(i)) for i, (x, y) in enumerate(zip(a, b)))) if a else set()
    return {prefix} if a != b else set()


def rows(manifest, stage='D0', choose=reference):
    return [{'id': a['id'], 'request_sha256': a['request_sha256'], 'ordered_request_sha256': a['ordered_request_sha256'],
             'status': 'completed', 'action': choose(a['request'])}
            for a in manifest['assignments'] if a['stage'] == stage]


class CaseChecks(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = build()
        cls.main = [x for x in cls.manifest['cases'] if not x['qualification']]

    def test_exact_allocation_and_nested_units(self):
        m = self.manifest
        self.assertEqual(len(self.main), 12)
        self.assertEqual(len({x['family'] for x in self.main}), 6)
        self.assertEqual(len(m['assignments']), 162)
        self.assertEqual(sum(a['stage']=='Q0' for a in m['assignments']), 18)
        self.assertEqual(len({a['id'] for a in m['assignments']}), 162)
        for condition in CONDITIONS:
            self.assertEqual(sum(a['stage']=='D0' and a['condition']==condition for a in m['assignments']), 24)

    def test_manifest_reproduces_and_has_no_dispatch(self):
        self.assertEqual(self.manifest, build())
        self.assertFalse(self.manifest['native_dispatch'])

    def test_hand_authored_targets_match_literal_public_reference(self):
        for a in self.manifest['assignments']:
            with self.subTest(a=a['id']):
                self.assertEqual(reference(a['request']), a['expected'])

    def test_only_declared_history_and_ballot_fields_change(self):
        for case in self.main:
            baseline = request_for(case, 'C00')
            self.assertEqual(diff(baseline, request_for(case, 'C10')), {'/state/historical_last_verified'})
            self.assertEqual(diff(baseline, request_for(case, 'C01')), {'/state/supplied_ballots'})
            self.assertEqual(diff(baseline, request_for(case, 'C11')), {'/state/historical_last_verified', '/state/supplied_ballots'})

    def test_absolute_clock_translation_preserves_every_duration(self):
        for case in self.main:
            old, new = request_for(case, 'C11'), request_for(case, 'CT')
            expected = {'/state/task/'+x for x in ('now', 'deadline', 'horizon')}
            expected |= {'/state/historical_last_verified/'+x for x in ('observed_at', 'expires_at')}
            expected |= {'/state/'+x+'/0/observed_at' for x in ('observations', 'evidence_cards')}
            self.assertEqual(diff(old, new), expected)
            os, ns = old['state'], new['state']
            for field in ('deadline', 'horizon'):
                self.assertEqual(os['task'][field]-os['task']['now'], ns['task'][field]-ns['task']['now'])
            self.assertEqual(os['task']['now']-os['observations'][0]['observed_at'], ns['task']['now']-ns['observations'][0]['observed_at'])
            self.assertEqual(ns['historical_last_verified']['expires_at']-os['historical_last_verified']['expires_at'], 100)

    def test_age_changes_only_applicable_current_observation_times(self):
        for case in self.main:
            original, aged = request_for(case, 'C11'), request_for(case, 'CA')
            self.assertEqual(diff(original, aged), {'/state/observations/0/observed_at', '/state/evidence_cards/0/observed_at'})
            s = aged['state']
            self.assertLess(s['historical_last_verified']['observed_at'], s['observations'][0]['observed_at'])
            self.assertLessEqual(s['task']['now']-s['observations'][0]['observed_at'], s['task']['ttl'])

    def test_exact_repeated_request_bytes_and_order(self):
        for case in self.main:
            for condition in CONDITIONS:
                a, b = [x for x in self.manifest['assignments'] if x['case']==case['id'] and x['condition']==condition]
                self.assertNotEqual(a['id'], b['id'])
                self.assertEqual(json.dumps(a['request']), json.dumps(b['request']))
                self.assertEqual(a['ordered_request_sha256'], b['ordered_request_sha256'])
            orders = [list(request_for(case, c)['questions']['action']['criteria']) for c in CONDITIONS]
            self.assertTrue(all(x==orders[0] for x in orders))

    def test_every_condition_occurs_in_each_repeat_block(self):
        assignments = self.manifest['assignments']
        self.assertTrue(all(a['stage']=='Q0' for a in assignments[:18]))
        for repeat in (0, 1):
            block=assignments[18+72*repeat:18+72*(repeat+1)]
            self.assertEqual({a['repeat'] for a in block}, {repeat})
            self.assertEqual(len({(a['case'],a['condition']) for a in block}), 72)

    def test_actor_payload_has_no_evaluator_or_treatment_metadata(self):
        for a in self.manifest['assignments']:
            req = a['request']
            self.assertEqual(set(req), {'model','provider','state','questions'})
            self.assertEqual(set(req['state']), {'task','observations','evidence_cards','historical_last_verified','supplied_ballots','current_authorized_action'})
            payload=json.dumps(req)
            for forbidden in ('"expected"', '"condition"', '"direction"', '"repeat"', '"family"', 'Qualification task'):
                self.assertNotIn(forbidden, payload)
            self.assertEqual(req['state']['current_authorized_action'], 'DEFER')

    def test_extracted_spans_and_source_preservation(self):
        for a in self.manifest['assignments']:
            state=a['request']['state']
            for source,card in zip(state['observations'],state['evidence_cards']):
                self.assertEqual(source['text'],card['text'])
                self.assertEqual(source['observed_at'],card['observed_at'])
                self.assertEqual(len(card['explicit_facts']),1)
                for fact in card['explicit_facts']:
                    start,end=fact['span']
                    self.assertEqual(source['text'][start:end],fact['source_text'])

    def test_qualification_and_main_full_requests_are_disjoint(self):
        q={a['request_sha256'] for a in self.manifest['assignments'] if a['stage']=='Q0'}
        d={a['request_sha256'] for a in self.manifest['assignments'] if a['stage']=='D0'}
        self.assertFalse(q & d)  # Same finite grammars; this is not a semantic holdout claim.

    def test_freshness_scope_revision_and_conflicts_are_not_votes(self):
        req=request_for(self.main[0],'C11')
        for key,value in [('scope','wrong'),('revision','wrong'),('observed_at',92),('observed_at',101)]:
            altered=deepcopy(req);altered['state']['observations'][0][key]=value
            self.assertEqual(reference(altered),'DEFER')
        for case in self.manifest['cases']:
            if case['uncertainty']:
                self.assertEqual(reference(request_for(case,'C11')),'DEFER')

    def test_boundary_and_optional_information_targets(self):
        self.assertEqual(reference(request_for(make_case('alarm',1,'resume'),'C11')),'PROCEED')
        self.assertEqual(reference(request_for(make_case('bridge',0,'resume'),'C11')),'PROCEED')
        self.assertEqual(reference(request_for(make_case('build',0,'resume'),'C11')),'PROCEED')
        self.assertEqual(reference(request_for(make_case('build',0,'stop'),'C11')),'HOLD')

    def test_action_orders_are_balanced_within_direction(self):
        for direction in ('stop', 'resume'):
            counts = [sum(c['direction']==direction and c['action_order_index']==i for c in self.main) for i in range(3)]
            self.assertEqual(counts,[2,2,2])

    def test_unknown_condition_is_rejected(self):
        with self.assertRaises(ValueError):request_for(self.main[0],'AUTO')


class ScoringChecks(unittest.TestCase):
    def setUp(self):
        self.m=build();self.rows=rows(self.m)

    def test_reference_has_zero_paired_effect(self):
        result=score(self.m,self.rows)
        self.assertEqual(result['primary_bounds'],[0,0])
        self.assertEqual(result['repeat_cells_complete'],72)
        self.assertEqual(result['repeat_cells_disagree'],0)
        self.assertTrue(all(x['correct']==24 for x in result['by_condition'].values()))

    def test_qualification_counts_all_controls(self):
        self.assertTrue(score(self.m,rows(self.m,'Q0'),'Q0')['qualification_passed'])
        q=rows(self.m,'Q0');q.pop()
        self.assertFalse(score(self.m,q,'Q0')['qualification_passed'])

    def test_wrong_simple_policies_are_detectable(self):
        self.assertEqual(sum(x['correct'] for x in score(self.m,rows(self.m,choose=lambda r:'DEFER'))['by_condition'].values()),0)
        for field in ('history','ballots'):
            def choose(req):
                state=req['state']
                if field=='history':return (state['historical_last_verified'] or {}).get('action','DEFER')
                return state['supplied_ballots'][0] if state['supplied_ballots'] else 'DEFER'
            result=score(self.m,rows(self.m,choose=choose))
            self.assertEqual(result['by_condition']['C11']['correct'],0)
            self.assertEqual(result['by_condition']['C11']['wrong_PROCEED'],12)
            self.assertEqual(result['by_condition']['C11']['needless_HOLD'],12)

    def test_missing_is_unknown_not_agreement_or_native_defer(self):
        a=next(x for x in self.m['assignments'] if x['stage']=='D0' and x['condition']=='C11')
        kept=[r for r in self.rows if r['id']!=a['id']]
        out=score(self.m,kept)
        self.assertEqual(out['statuses']['unstarted'],1)
        self.assertAlmostEqual(out['primary_bounds'][0],-1/24)
        self.assertEqual(out['primary_bounds'][1],0)
        self.assertEqual(out['repeat_cells_complete'],71)
        self.assertEqual(out['by_condition']['C11']['unexpected_DEFER'],0)

    def test_one_missed_repeat_is_one_error_not_four_epochs(self):
        target=next(a for a in self.m['assignments'] if a['stage']=='D0' and a['condition']=='C11')
        next(r for r in self.rows if r['id']==target['id'])['action']='DEFER'
        out=score(self.m,self.rows)
        self.assertEqual(out['by_condition']['C11']['correct'],23)
        self.assertAlmostEqual(out['primary_bounds'][0],-1/24)
        self.assertEqual(out['repeat_cells_disagree'],1)

    def test_invalid_and_failed_outcomes_remain_assigned(self):
        for status in ('invalid','failed'):
            rows_=deepcopy(self.rows);rows_[0].update(status=status,action=None)
            out=score(self.m,rows_)
            self.assertEqual(out['assigned'],144)
            self.assertEqual(out['statuses'][status],1)
            self.assertEqual(sum(x['valid'] for x in out['by_condition'].values()),143)

    def test_bad_or_duplicate_ids_and_changed_bindings_fail(self):
        for mutate in ('duplicate','unknown','hash','ordered','status','action','failed_action'):
            rs=deepcopy(self.rows)
            if mutate=='duplicate':rs.append(rs[0])
            elif mutate=='unknown':rs[0]['id']='not-assigned'
            elif mutate=='hash':rs[0]['request_sha256']='wrong'
            elif mutate=='ordered':rs[0]['ordered_request_sha256']='wrong'
            elif mutate=='status':rs[0]['status']='retrying'
            elif mutate=='action':rs[0]['action']='KEEP'
            else:rs[0]['status']='failed'
            with self.subTest(mutate=mutate),self.assertRaises(ValueError):score(self.m,rs)

    def test_all_missing_has_full_uncertainty(self):
        result=score(self.m,[])
        self.assertEqual(result['primary_bounds'],[-1,1])
        self.assertEqual(result['repeat_cells_complete'],0)
        self.assertEqual(result['statuses']['unstarted'],144)


if __name__=='__main__':unittest.main()
