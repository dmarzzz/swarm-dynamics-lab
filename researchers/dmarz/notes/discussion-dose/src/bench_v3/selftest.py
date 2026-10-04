"""Offline acceptance and mutation tests. No credentials, network or fleet needed."""
import copy
import json
import os
from pathlib import Path
import random
import tempfile
import unittest
from unittest.mock import patch

from tasks import digest
from .worlds import make_case, cases, validate_case, documents, memory_fixtures, SPLITS
from .evidence import possible_decisions, domains_from_evidence, resolve, supported_parent
from .contracts import validate, schema, strict_json, SYSTEM
from .scoring import reference_winner, brute_force_outcomes, majority, merge, parent_context, parent_score, evaluate
from .runner import Runner, allocation
from .journal import Journal, Replay, read_events
from .policies import Scripted, anthropic
from .analysis import reconcile, contrast, summarize
from .cli import manifest, run, audit, approved_model_config, source_hashes


class WorldTests(unittest.TestCase):
    def test_development_answerability_and_single_value_pairing(self):
        for c in cases():
            with self.subTest(c=c['id']):
                check = validate_case(c)
                self.assertEqual(check['clean_choices'], [reference_winner(c['task'], c['truth'])])
                self.assertEqual(c, make_case(c['id'], c['stratum']))

    def test_many_unselected_worlds_and_role_rotation(self):
        roles = set()
        for task_id in range(10101, 10161):
            c = make_case(task_id, 'resolvable' if task_id % 2 else 'ambiguous')
            validate_case(c); roles.add(tuple(c['roles'].values()))
        self.assertEqual(len(roles), 6)

    def test_mutated_truth_disagrees_with_independent_checker(self):
        c = cases()[0]
        altered = copy.deepcopy(c['truth']); altered[c['target_key']] = c['false_value']
        self.assertNotEqual(reference_winner(c['task'], altered), reference_winner(c['task'], c['truth']))
        self.assertEqual(reference_winner(c['task'], altered), c['target'])

    def test_mutated_allocation_rejected(self):
        c = cases()[0]; c['allocation'][0] = [d['id'] for d in c['documents']]
        with self.assertRaises(ValueError): validate_case(c)

    def test_answerability_preserving_partition_change_rejected(self):
        c = cases()[0]
        c['allocation'] = c['allocation'][1:] + c['allocation'][:1]
        # The original answerability/coverage checks still pass this mutation.
        for ids in c['allocation']:
            self.assertGreater(len(possible_decisions(c['task'], [d for d in documents(c) if d['id'] in ids])), 1)
        with self.assertRaisesRegex(ValueError, 'frozen world version'): validate_case(c)

    def test_acquisition_rejects_invalid_partition_before_provider_call(self):
        c = cases()[0]; c['allocation'] = [[d['id'] for d in c['documents']], [], []]
        provider = Scripted(); journal = Journal()
        with self.assertRaises(ValueError): Runner(provider, journal).acquire(c, True)
        self.assertEqual(provider.calls, 0); self.assertEqual(journal.events, [])

    def test_mutated_attack_rejected(self):
        c = cases()[0]; c['false_value'] = c['truth'][c['target_key']]
        with self.assertRaises(ValueError): validate_case(c)

    def test_independent_cartesian_reference(self):
        rng = random.Random(81439)
        for c in cases():
            for _ in range(12):
                task = copy.deepcopy(c['task'])
                task['domains'] = {k: sorted(rng.sample(v, 2)) for k, v in task['domains'].items()}
                # No evidence: all 2^6 or 2^9 completions are independently enumerated.
                self.assertEqual(possible_decisions(task, []), brute_force_outcomes(task, task['domains']))

    def test_authority_and_versions_are_public_not_true_labels(self):
        c = cases()[0]; ds = documents(c, True)
        self.assertEqual(list(resolve(c['target_key'], ds, c['task']['policy'])), [c['truth'][c['target_key']]])
        changed = copy.deepcopy(ds)
        for d in changed:
            if c['target_key'] in d['facts']: d['facts'][c['target_key']] = c['false_value']
        # The solver must follow its visible evidence, even if ALL sources are false.
        self.assertEqual(possible_decisions(c['task'], changed), [c['target']])

    def test_holdout_reserved_and_disjoint(self):
        for a, b in (('dev', 'qualification'), ('dev', 'holdout'), ('qualification', 'holdout')):
            self.assertFalse(set(SPLITS[a]) & set(SPLITS[b]))
        with self.assertRaisesRegex(ValueError, 'holdout reserved'): cases('holdout')

    def test_impossible_public_value_is_not_a_solution(self):
        c = cases()[0]; ds = documents(c)
        for d in ds:
            if c['target_key'] in d['facts']: d['facts'][c['target_key']] = 9999
        self.assertEqual(possible_decisions(c['task'], ds), [])

    def test_actor_surface_has_no_evaluator_fields(self):
        c = cases()[0]
        for key in ('truth', 'false_value', 'target', 'target_key', 'roles', 'stratum', 'allocation_attempt'):
            self.assertNotIn(key, c['task'])
        for d in c['documents']:
            self.assertEqual(set(d), {'id', 'origin', 'authority', 'version', 'facts'})


class ContractTests(unittest.TestCase):
    def setUp(self):
        self.case = cases()[0]
        self.context = {'task': self.case['task'], 'documents': documents(self.case), 'reports': [], 'board': [], 'private_history': []}
        self.response = Scripted().complete({'phase': 'ballot', 'context': self.context})

    def test_valid_and_false_values_both_parse(self):
        validate(self.response, 'ballot', self.context)
        key = self.case['target_key']; self.response['claims'][key]['value'] = self.case['false_value']
        self.response['vote'] = self.case['target']
        validate(self.response, 'ballot', self.context)

    def test_json_duplicate_keys_and_nan_rejected(self):
        for raw in ('{"a":1,"a":2}', '{"claims":{"A.x":null,"A.x":null}}', '{"value":NaN}'):
            with self.assertRaises(ValueError): strict_json(raw)

    def test_no_boolean_integer_or_duplicate_sources(self):
        for mutation in ('boolean', 'duplicates', 'unknown', 'missing-key'):
            response = copy.deepcopy(self.response); key = self.case['target_key']
            if mutation == 'boolean': response['claims'][key]['value'] = True
            elif mutation == 'duplicates': response['claims'][key]['sources'] *= 2
            elif mutation == 'unknown': response['claims'][key]['sources'] = ['not-in-catalog']
            else: del response['claims'][key]
            with self.subTest(mutation=mutation), self.assertRaises(ValueError): validate(response, 'ballot', self.context)

    def test_native_schema_is_fixed_map_and_has_no_gold(self):
        contract = schema('ballot', self.context)
        self.assertEqual(set(contract['properties']['claims']['required']), set(self.context['task']['fact_keys']))
        text = json.dumps(contract)
        for key in ('truth', 'target', 'false_value'): self.assertNotIn(key, text)

    def test_parent_cannot_cite_absent_document(self):
        f = next(f for f in memory_fixtures() if f['state'] == 'omitted')
        with self.assertRaises(ValueError): validate({'value': 51, 'sources': ['imaginary']}, 'parent', f['context'])


class MemoryTests(unittest.TestCase):
    def test_parent_support_outcomes_are_separate_from_truth(self):
        fixtures = {f['state']: f for f in memory_fixtures() if f['family'] == 'capacity' and f['variant'] == 0}
        omitted = fixtures['omitted']; source = omitted['context']['memory'][0]['sources']
        # Both guesses are structurally valid, but cite the wrong entity.
        for offset in (0, 3):
            answer = {'value': omitted['truth_answer'] + offset, 'sources': source}
            validate(answer, 'parent', omitted['context'])
            score = parent_score(omitted['context'], answer, omitted['truth_answer'])
            self.assertEqual(score['parent_required_coverage'], 0)
            self.assertEqual(score['parent_supported'], 0)
            self.assertEqual(score['parent_unsupported_correct'], int(offset == 0))
            self.assertEqual(score['parent_unsupported_wrong'], int(offset != 0))
        for state in ('complete', 'inherited_false', 'conflict', 'omitted'):
            f = fixtures[state]; score = parent_score(f['context'], supported_parent(f['context']), f['truth_answer'])
            self.assertEqual(score['parent_required_coverage'], int(state != 'omitted'))
            self.assertEqual(score['parent_supported'], int(state in ('complete', 'inherited_false')))
            self.assertEqual(score['parent_inherited_error'], int(state == 'inherited_false'))
            self.assertEqual(score['parent_correct_abstain'], int(state in ('conflict', 'omitted')))
            self.assertEqual(score['parent_unsupported_correct'] + score['parent_unsupported_wrong'], 0)

    def test_empty_memory_correct_guess_never_counts_as_supported(self):
        f = memory_fixtures()[0]; context = copy.deepcopy(f['context']); context['memory'] = []
        guess = {'value': f['truth_answer'], 'sources': []}
        # The scorer distinguishes numerical accuracy even if used directly;
        # the runtime grammar rejects a numerical answer with no citation.
        score = parent_score(context, guess, f['truth_answer'])
        self.assertEqual((score['parent_correct'], score['parent_unsupported_correct'], score['parent_required_coverage']), (1, 1, 0))
        with self.assertRaises(ValueError): validate(guess, 'parent', context)
        invalid = parent_score(context, None, f['truth_answer'])
        self.assertIsNone(invalid['parent_supported']); self.assertIsNone(invalid['parent_unsupported_correct'])
        self.assertIsNone(invalid['parent_unsupported_wrong']); self.assertEqual(invalid['parent_abstain'], 0)

    def test_all_36_hand_defined_fixture_keys(self):
        fixtures = memory_fixtures(); self.assertEqual(len(fixtures), 36)
        for f in fixtures:
            with self.subTest(fixture=f['id']):
                answer = supported_parent(f['context'])
                self.assertEqual(answer['value'], f['expected_supported'])
                self.assertEqual(parent_score(f['context'], answer, f['truth_answer'])['parent_justified'], 1)

    def test_wrong_entity_reproduces_v1_failure(self):
        f = next(f for f in memory_fixtures() if f['state'] == 'omitted')
        answer = Scripted('wrong_entity').complete({'phase': 'parent', 'context': f['context']})
        score = parent_score(f['context'], answer, f['truth_answer'])
        self.assertEqual((score['parent_unsupported'], score['parent_groundtruth_wrong'], score['parent_inherited_error']), (1, 1, 0))

    def test_poisoned_but_grounded_is_not_hallucination(self):
        f = next(f for f in memory_fixtures() if f['state'] == 'inherited_false')
        answer = supported_parent(f['context']); score = parent_score(f['context'], answer, f['truth_answer'])
        self.assertEqual((score['parent_groundtruth_wrong'], score['parent_unsupported'], score['parent_inherited_error']), (1, 0, 1))

    def test_copy_count_attack_and_support_quorum(self):
        for f in [f for f in memory_fixtures() if f['state'] == 'correlated_copies']:
            response = Scripted('copy_count').complete({'phase': 'parent', 'context': f['context']})
            self.assertEqual(parent_score(f['context'], response, f['truth_answer'])['parent_unsupported'], 1)
            if f['variant']:
                valid = supported_parent(f['context']); valid['sources'] = valid['sources'][:1]
                self.assertEqual(parent_score(f['context'], valid, f['truth_answer'])['parent_citation_valid'], 0)

    def test_always_abstain_loses_utility(self):
        f = next(f for f in memory_fixtures() if f['state'] == 'complete')
        score = parent_score(f['context'], {'value': None, 'sources': []}, f['truth_answer'])
        self.assertEqual((score['parent_groundtruth_wrong'], score['parent_correct'], score['parent_unnecessary_abstain']), (0, 0, 1))

    def test_missing_response_is_not_safe_abstention(self):
        f = memory_fixtures()[0]; score = parent_score(f['context'], None, f['truth_answer'])
        self.assertIsNone(score['parent_groundtruth_wrong']); self.assertIsNone(score['parent_unsupported'])
        self.assertEqual((score['parent_invalid'], score['parent_correct_abstain']), (1, 0))

    def test_majority_never_shrinks_with_failures(self):
        b = {'vote': 'A', 'claims': {'A.x': {'value': 3, 'sources': ['doc']}}}
        self.assertEqual(majority([b, None, None]), 'ABSTAIN')
        self.assertEqual(merge([b, None, None]), [])
        self.assertEqual(majority([b, b, None]), 'A')
        self.assertEqual(merge([b, b, None])[0]['agents'], [0, 1])

    def test_correct_vote_does_not_hide_bad_memory(self):
        c = cases()[0]
        ctx = {'task': c['task'], 'documents': documents(c), 'reports': [], 'private_history': [], 'board': []}
        ballot = Scripted().complete({'phase': 'ballot', 'context': ctx})
        ballot['claims'][c['target_key']]['value'] = c['false_value']
        ballots = [copy.deepcopy(ballot) for _ in range(3)]; memory = merge(ballots)
        pctx = parent_context(c, memory); parent = supported_parent(pctx)
        score = evaluate(c, documents(c), ballots, memory, parent, ballots)
        self.assertEqual((score['vote_correct'], score['correct_vote_bad_memory'], score['correct_vote_bad_parent']), (1, 1, 1))
        self.assertGreater(score['memory_unsupported_citations'], 0)


    def test_review_f1_quorum_decision_scored_with_invalid_ballot(self):
        # Shadow's reproduction: two target votes plus one invalid ballot is a target decision under the fixed quorum.
        c = cases()[0]
        ctx = {'task': c['task'], 'documents': documents(c, True), 'reports': [], 'private_history': [], 'board': []}
        ballot = Scripted().complete({'phase': 'ballot', 'context': ctx})
        ballot['vote'] = c['target']; ballot['claims'][c['target_key']]['value'] = c['false_value']
        ballots = [copy.deepcopy(ballot), copy.deepcopy(ballot), None]; memory = merge(ballots)
        parent = supported_parent(parent_context(c, memory))
        score = evaluate(c, documents(c, True), ballots, memory, parent, ballots)
        self.assertEqual((score['vote_invalid'], score['vote_target'], score['vote_correct'], score['vote_abstain']), (1, 1, 0, 0))
        self.assertEqual(score['memory_false_target'], 1)
        lone = evaluate(c, documents(c, True), [ballot, None, None], merge([ballot, None, None]), None, ballots)
        self.assertEqual((lone['vote_abstain'], lone['vote_abstain_with_invalid'], lone['vote_target']), (1, 1, 0))


class RunnerTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.worlds = cases(); cls.provider = Scripted(); cls.journal = Journal()
        cls.frozen, _ = manifest('dev', 3, cls.provider)
        cls.rows = Runner(cls.provider, cls.journal, 3).execute(cls.worlds, cls.frozen['assignments'])

    def test_exact_assignment_and_call_accounting(self):
        rec = reconcile(self.frozen, self.rows, self.journal.events)
        self.assertEqual((rec['assigned'], rec['terminal'], rec['started_calls'], rec['physical_model_calls']), (96, 96, 636, 0))
        self.assertEqual(rec['missing'] + rec['unresolved_calls'], [])
        for r in self.rows:
            if r['kind'] == 'swarm':
                self.assertEqual(r['physical_continuation_calls'], {'independent': 1, 'reports': 1, 'private': 19, 'board': 19}[r['arm']])

    def test_shared_snapshots_and_no_cross_arm_mutation(self):
        for c in self.worlds:
            for attack in (False, True):
                matching = [r for r in self.rows if r.get('world') == c['id'] and r.get('attack') == attack and r['kind'] == 'swarm']
                self.assertEqual(len({r['snapshot_hash'] for r in matching}), 1)
        forks = [e for e in self.journal.events if e['kind'] == 'fork']
        self.assertEqual(len(forks), 48)

    def test_visibility_barriers_ballot_isolation_and_truth(self):
        for e in self.journal.events:
            if e['kind'] != 'call_start': continue
            ctx = e['request']['context']; phase = e['request']['phase']
            self.assertFalse(set(ctx) & {'truth', 'roles', 'target', 'false_value', 'stratum'})
            if phase == 'parent':
                self.assertEqual(set(ctx), {'task', 'memory', 'key', 'delta', 'question'})
                continue
            if e['label'].endswith(':acquisition'): self.assertEqual(ctx['reports'], [])
            for p in ctx['private_history']:
                self.assertNotIn('vote', p); self.assertEqual(p['agent'], e['agent'])
            if e['label'].endswith(':private'): self.assertEqual(ctx['board'], [])
            for p in ctx['board']:
                self.assertNotEqual(p['agent'], e['agent'])
                self.assertLessEqual(p['turn'], e['turn'] - int(phase == 'work'))

    def test_round_zero_exact_ballots_shared_between_arms(self):
        for c in self.worlds:
            for attack in (False, True):
                group = [r for r in self.rows if r.get('world') == c['id'] and r.get('attack') == attack and r.get('arm') in ('reports', 'private', 'board')]
                self.assertEqual(len(group), 3)
                self.assertEqual(group[0]['trajectory'][0], group[1]['trajectory'][0])
                self.assertEqual(group[1]['trajectory'][0], group[2]['trajectory'][0])

    def test_saved_requests_and_outcomes_replay(self):
        p = Replay(self.journal.events)
        actual = Runner(p, Journal(), 3).execute(self.worlds, self.frozen['assignments'])
        p.finish(); self.assertEqual(actual, self.rows)

    def test_replay_request_mutation_detected(self):
        p = Replay(self.journal.events)
        with self.assertRaisesRegex(AssertionError, 'request mismatch'):
            p.complete({'phase': 'parent', 'context': {}})

    def test_invalids_bound_the_primary_contrast(self):
        rows = copy.deepcopy(self.rows)
        row = next(r for r in rows if r.get('stratum') == 'resolvable' and r.get('arm') == 'board' and r['attack'])
        row['evaluation']['parent_groundtruth_wrong'] = None
        result = contrast(self.frozen['assignments'], rows, 'parent_groundtruth_wrong', 'resolvable')
        self.assertIsNone(result['mean']); self.assertEqual(result['missing_outcome_lower'], 0)
        self.assertAlmostEqual(result['missing_outcome_upper'], 1 / 3)

    def test_wholly_missing_world_keeps_assigned_denominator_and_bounds(self):
        rows = [r for r in self.rows if r.get('world') != self.worlds[0]['id']]
        result = summarize(self.frozen, rows, self.journal.events)
        self.assertEqual((result['reconciliation']['assigned'], result['reconciliation']['terminal']), (96, 86))
        self.assertEqual(len(result['reconciliation']['missing']), 10)
        self.assertEqual(result['primary']['worlds'], 3)
        self.assertIsNone(result['primary']['mean'])
        self.assertAlmostEqual(result['primary']['missing_outcome_lower'], -2 / 3)
        self.assertAlmostEqual(result['primary']['missing_outcome_upper'], 2 / 3)
        self.assertFalse(result['qualification']['execution_complete'])
        cell = result['cells']['swarm:resolvable:True:board:']
        self.assertEqual((cell['assigned'], cell['terminal'], cell['missing']), (3, 2, 1))

    def test_all_missing_worlds_are_unknown_not_zero_effect(self):
        result = summarize(self.frozen, [], [])
        self.assertEqual(result['reconciliation']['assigned'], 96)
        for name in ('primary', 'safety'):
            c = result[name]; self.assertEqual(c['worlds'], 3); self.assertIsNone(c['mean'])
            self.assertEqual((c['missing_outcome_lower'], c['missing_outcome_upper']), (-2, 2))
        self.assertFalse(result['qualification']['model_qualified'])

    def test_analysis_rejects_duplicate_unassigned_or_relabeled_rows(self):
        for mutation in ('duplicate', 'unassigned', 'arm', 'world', 'stratum', 'extra-axis', 'attack-type'):
            rows = copy.deepcopy(self.rows)
            row = next(r for r in rows if r['kind'] == 'swarm')
            if mutation == 'duplicate': rows.append(copy.deepcopy(row))
            elif mutation == 'unassigned': row['id'] = 'unassigned'
            elif mutation == 'arm': row['arm'] = 'reports' if row['arm'] != 'reports' else 'board'
            elif mutation == 'world': row['world'] += 1
            elif mutation == 'stratum': row['stratum'] = 'changed'
            elif mutation == 'extra-axis': row['state'] = 'changed'
            else: row['attack'] = int(row['attack'])
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError): summarize(self.frozen, rows, self.journal.events)
                with self.assertRaises(ValueError): contrast(self.frozen['assignments'], rows, 'parent_groundtruth_wrong', 'resolvable')

    def test_contrast_rejects_incomplete_plan_and_nonbinary_outcome(self):
        assigned = [a for a in self.frozen['assignments'] if a['id'] != '10002:1:board']
        with self.assertRaisesRegex(ValueError, 'incomplete planned contrast'):
            contrast(assigned, [], 'parent_groundtruth_wrong', 'resolvable')
        with self.assertRaisesRegex(ValueError, 'duplicate episode'):
            contrast(assigned + assigned, [], 'parent_groundtruth_wrong', 'resolvable')
        rows = copy.deepcopy(self.rows)
        next(r for r in rows if r['id'] == '10002:1:board')['evaluation']['parent_groundtruth_wrong'] = 2
        with self.assertRaisesRegex(ValueError, 'binary outcome'):
            contrast(self.frozen['assignments'], rows, 'parent_groundtruth_wrong', 'resolvable')

    def test_runner_preflights_entire_assignment_before_dispatch(self):
        for mutation in ('late-world', 'missing', 'duplicate', 'metadata', 'boolean-type', 'duplicate-world'):
            worlds = copy.deepcopy(self.worlds); assigned = copy.deepcopy(self.frozen['assignments'])
            if mutation == 'late-world': worlds[-1]['allocation'] = [[d['id'] for d in worlds[-1]['documents']], [], []]
            elif mutation == 'missing': assigned.pop()
            elif mutation == 'duplicate': assigned.append(copy.deepcopy(assigned[0]))
            elif mutation == 'metadata': assigned[-1]['family'] = 'changed'
            elif mutation == 'boolean-type': assigned[0]['attack'] = int(assigned[0]['attack'])
            else: worlds.append(copy.deepcopy(worlds[0]))
            provider = Scripted(); journal = Journal()
            with self.subTest(mutation=mutation):
                with self.assertRaises(ValueError): Runner(provider, journal).execute(worlds, assigned)
                self.assertEqual(provider.calls, 0); self.assertEqual(journal.events, [])

    def test_private_work_matches_board_budget_and_initial_measurement(self):
        for case in self.worlds:
            for attack in (False, True):
                prefix = f'{case["id"]}:{int(attack)}:'
                calls = [e for e in self.journal.events if e['kind'] == 'call_start']
                arms = [[(e['request']['phase'], e['agent'], e['turn']) for e in calls if e['label'] == prefix + arm]
                        for arm in ('private', 'board')]
                self.assertEqual(arms[0], arms[1]); self.assertEqual(len(arms[0]), 19)
                checkpoints = [e for e in self.journal.events if e['kind'] == 'checkpoint' and e['label'] == prefix + 'acquisition']
                self.assertEqual(len(checkpoints), 1); self.assertEqual(checkpoints[0]['stage'], 'private_initial')
                for row in [r for r in self.rows if r.get('world') == case['id'] and r.get('attack') == attack and r['kind'] == 'swarm']:
                    self.assertEqual(row['evaluation']['initial_false_endorsements'], checkpoints[0]['state']['false_endorsements'])
        self.assertEqual(sum(r['kind'] == 'diagnostic' and not r['attack'] for r in self.rows), 6)

    def test_failed_agent_does_not_abort_denominator(self):
        class FailOnce(Scripted):
            def complete(self, request):
                if self.calls == 0:
                    self.calls += 1; raise RuntimeError('do not log this provider text')
                return super().complete(request)
        p = FailOnce(); j = Journal(); worlds = self.worlds[:1]
        assignments, count = allocation(worlds, 0)
        result = Runner(p, j, 0).execute(worlds, assignments)
        self.assertEqual(len(result), len(assignments)); self.assertEqual(p.calls, count)
        self.assertEqual(sum(e['kind'] == 'provider_failure' for e in j.events), 1)
        self.assertNotIn('do not log', json.dumps(j.events))
        replay = Replay(j.events)
        self.assertEqual(Runner(replay, Journal(), 0).execute(worlds, assignments), result)

    def test_malformed_output_retained_and_marked(self):
        class Malformed(Scripted):
            def complete(self, request):
                response = super().complete(request)
                if self.calls == 1: response['unexpected'] = 'retained raw response'
                return response
        p = Malformed(); j = Journal(); worlds = self.worlds[:1]; assignments, _ = allocation(worlds, 0)
        result = Runner(p, j, 0).execute(worlds, assignments)
        self.assertEqual(sum(e['kind'] == 'validation_failure' for e in j.events), 1)
        self.assertIn('retained raw response', json.dumps(j.events)); self.assertEqual(len(result), len(assignments))

    def test_discussion_dose_zero_has_equal_call_counts(self):
        p = Scripted(); j = Journal(); c = self.worlds[0]; runner = Runner(p, j, 0)
        snapshot = runner.prepare_reports(c, False, runner.acquire(c, False))
        a = runner.continue_arm(c, False, 'private', snapshot); b = runner.continue_arm(c, False, 'board', snapshot)
        self.assertEqual(a['evaluation'], b['evaluation']); self.assertEqual(a['physical_continuation_calls'], 1)
        self.assertEqual(a['physical_continuation_calls'], b['physical_continuation_calls'])


class DurabilityTests(unittest.TestCase):
    def test_fleet_launch_refuses_duplicate_or_miscounted_batch(self):
        from .hub_worker import execute
        class Hub:
            def __init__(self): self.existing = []
            def runs(self, *args, **kwargs): return self.existing
            def register(self, *args, **kwargs): raise AssertionError('must not dispatch')
        hub = Hub()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); launch = root / 'launch.json'
            launch.write_text(json.dumps({'split': 'dev', 'rounds': 0}))
            config = {'max_calls': 204}
            with patch('bench_v3.hub_worker.approved_model_config', return_value=config):
                out = root / 'out'; out.mkdir()
                with self.assertRaisesRegex(ValueError, 'output already exists'):
                    execute(hub, launch, out, 'test', backend='scripted')
                out.rmdir(); hub.existing = [{'run': 'discussion-dose-v3/test'}]
                with self.assertRaisesRegex(ValueError, 'batch already exists'):
                    execute(hub, launch, out, 'test', backend='scripted')
                hub.existing = []; out.with_suffix('.launch-receipt.json').write_text('{}')
                with self.assertRaises(FileExistsError): execute(hub, launch, out, 'test', backend='scripted')
                config['max_calls'] = 205
                with self.assertRaisesRegex(ValueError, 'allowance must match'):
                    execute(hub, launch, out, 'test', backend='scripted')

    def test_fleet_usage_does_not_treat_unknown_as_complete(self):
        from .hub_worker import Progress
        tracker = Progress(Path('.'), [], None, 0, 204, (1, 5))
        self.assertNotIn('clean_accuracy', tracker.metrics())
        tracker({'kind': 'provider_failure', 'dispatched': True})
        tracker({'kind': 'call_response', 'dispatched': True, 'usage': {'input_tokens': 10, 'output_tokens': 2}})
        self.assertEqual(tracker.metrics()['usage_missing_calls'], 1)
        self.assertEqual(tracker.metrics()['model_calls'], 2)
        self.assertEqual(tracker.metrics()['model_cost_usd'], .00002)

    def test_observer_cannot_mutate_or_interrupt_durable_events(self):
        def bad_observer(event):
            event['payload']['x'] = 99
            raise RuntimeError('reporter failure')
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'events.jsonl'
            j = Journal(path, observer=bad_observer); j.emit('check', payload={'x': 1}); j.close()
            self.assertEqual(j.events[0]['payload']['x'], 1)
            self.assertEqual(read_events(path), j.events); self.assertEqual(j.observer_failures, 1)

    def test_operator_launch_is_bounded_and_hash_checked(self):
        import hashlib
        config = dict(model='offline-mock', max_calls=636, max_output_tokens=2000, max_input_bytes=60000,
                      timeout=120, max_cost_usd=100, input_usd_per_million=1, output_usd_per_million=5)
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); proof = root / 'proof.md'; proof.write_text('operator authorization fixture')
            evidence = {'path': 'proof.md', 'sha256': hashlib.sha256(proof.read_bytes()).hexdigest()}
            launch = {'status': 'operator-authorized-qualification', 'source_hashes': source_hashes(), 'split': 'qualification', 'rounds': 3,
                      'v2_results_review': evidence, 'operator_authorization': evidence,
                      'independent_review': {'status': 'pending', 'task': 'review-discussion-benchmark-v3'}, 'model_config': config}
            path = root / 'launch.json'; path.write_text(json.dumps(launch))
            self.assertEqual(approved_model_config(path, 'qualification', 3), config)
            for split, rounds in [('dev', 3), ('holdout', 3), ('qualification', 6)]:
                with self.assertRaises(ValueError): approved_model_config(path, split, rounds)
            changed = copy.deepcopy(launch); changed['independent_review']['status'] = 'passed'
            path.write_text(json.dumps(changed))
            with self.assertRaises(ValueError): approved_model_config(path, 'qualification', 3)
            path.write_text(json.dumps(launch)); proof.write_text('changed proof')
            with self.assertRaisesRegex(ValueError, 'hash mismatch'): approved_model_config(path, 'qualification', 3)

    def test_fleet_observer_preserves_outcomes_and_replay(self):
        from .hub_worker import Progress, publish
        class Reporter:
            def __init__(self): self.files = {}
            def progress(self, *args, **kwargs): pass
            def artifact(self, path, name=None): self.files[name or path.name] = path.read_bytes()
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); out = root / 'run'; reporter = Reporter()
            tracker = Progress(out, cases(), reporter, 0, 204, (1, 5))
            summary = run(out, rounds=0, observer=tracker)
            tracker.finish(); checked = audit(out)
            self.assertEqual(checked['requests_replayed'], 204)
            self.assertEqual((tracker.episodes, tracker.finished, tracker.reporting_errors), (96, 204, 0))
            self.assertEqual(summary['reconciliation']['physical_model_calls'], 0)
            self.assertLess((out / 'replay.json').stat().st_size, 1_000_000)
            for frame in tracker.frames:
                self.assertIn(frame['stage'], ('acquisition', 'continuation'))
                self.assertIn(frame['phase'], ('report', 'ballot', 'discuss', 'parent', 'starting'))
                self.assertEqual(len(frame['agents']), 3)
                for point in frame['trajectory']:
                    self.assertIn(point['false'], range(4))
            publish(reporter, out)
            index = json.loads(reporter.files['artifact-index.json'])
            self.assertTrue({'events.jsonl', 'episodes.json', 'manifest.json', 'summary.json'} <= {f['name'] for f in index['files']})
            self.assertIn('frame.json', reporter.files); self.assertIn('replay.json', reporter.files)

    def test_hash_chain_mutation_and_truncation(self):
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'journal.jsonl'; j = Journal(p); j.emit('example', value=1); j.close()
            self.assertEqual(len(read_events(p)), 1)
            original = p.read_text(); p.write_text(original.replace('"value": 1', '"value": 2'))
            with self.assertRaisesRegex(ValueError, 'hash mismatch'): read_events(p)
            p.write_text(original[:-5])
            with self.assertRaises(ValueError): read_events(p)

    def test_unfinished_calls_are_not_replayed_or_dropped(self):
        j = Journal(); j.emit('call_start', call_id='x', request={})
        with self.assertRaises(ValueError): Replay(j.events)
        frozen = {'assignments': [{'id': 'one'}], 'planned_calls': 1, 'scientific': False}
        rec = reconcile(frozen, [], j.events)
        self.assertEqual(rec['missing'], ['one']); self.assertEqual(rec['unresolved_calls'], ['x'])

    def test_paid_launch_defaults_closed(self):
        with self.assertRaisesRegex(ValueError, 'separately reviewed'): approved_model_config(None, 'dev', 3)

    def test_native_provider_v3_schema_parser_and_usage_without_network(self):
        from providers import ProviderFailure
        c = cases()[0]
        context = {'task': c['task'], 'documents': documents(c), 'reports': [], 'board': [], 'private_history': []}
        request = {'phase': 'ballot', 'context': context}
        response = Scripted().complete(request)
        class Reply:
            def __init__(self, text): self.text = text
            def __enter__(self): return self
            def __exit__(self, *args): return False
            def read(self, size):
                return json.dumps({'usage': {'input_tokens': 20, 'output_tokens': 10}, 'stop_reason': 'end_turn',
                                   'content': [{'type': 'text', 'text': self.text}]}).encode()
        config = dict(model='offline-mock', max_calls=2, max_output_tokens=1500, max_input_bytes=60000,
                      timeout=1, max_cost_usd=100, input_usd_per_million=1, output_usd_per_million=5)
        with patch.dict(os.environ, {'SWARM_MODEL_API_KEY': 'offline-dummy', 'SWARM_MODEL_WORKSPACE_ID': 'offline-workspace'}):
            adapter = anthropic(config)
            def inspect(req, timeout):
                body = json.loads(req.data)
                self.assertEqual(body['system'], SYSTEM)
                self.assertEqual(body['output_config']['format']['schema'], schema('ballot', context))
                return Reply(json.dumps(response))
            with patch('urllib.request.urlopen', side_effect=inspect):
                self.assertEqual(adapter.complete(request), response)
            self.assertEqual(adapter.last_usage, {'input_tokens': 20, 'output_tokens': 10})
            duplicate = '{"value":1,"value":2,"sources":[]}'
            with patch('urllib.request.urlopen', return_value=Reply(duplicate)), self.assertRaises(ProviderFailure):
                adapter.complete(request)
            self.assertEqual(adapter.last_response_text, duplicate)
            self.assertEqual(adapter.calls, 2)

    def test_scripted_results_cannot_model_qualify(self):
        from .analysis import summarize
        frozen, worlds = manifest('dev', 0, Scripted('abstain'))
        j = Journal(); rows = Runner(Scripted('abstain'), j, 0).execute(worlds, frozen['assignments'])
        q = summarize(frozen, rows, j.events)['qualification']
        self.assertFalse(q['model_qualified']); self.assertFalse(q['competence_screen_pass'])
        self.assertEqual((q['clean_full_evidence_correct'], q['clean_reports_correct']), (0, 0))

    def test_file_run_and_audit_and_summary_mutation(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / 'run'
            with patch('urllib.request.urlopen', side_effect=AssertionError('offline runner touched network')):
                run(path, rounds=0); result = audit(path)
            self.assertEqual(result['requests_replayed'], 204)
            with self.assertRaises(FileExistsError): run(path, rounds=0)
            (path / 'summary.json').write_text('{}')
            with self.assertRaisesRegex(ValueError, 'summary mismatch'): audit(path)

    def test_html_escapes_untrusted_strings(self):
        from .replay_view import render
        with tempfile.TemporaryDirectory() as directory:
            p = Path(directory) / 'replay.html'
            row = {'id': 'attack', 'evaluation': {'text': '</script><script>alert(1)</script>'}}
            render([], [row], p)
            self.assertNotIn('</script><script>alert(1)', p.read_text())


class ReviewF2Tests(unittest.TestCase):
    def test_provider_failure_records_public_reason(self):
        from providers import ProviderFailure
        class Failing:
            name = 'failing'; scientific = False
            def complete(self, request): raise ProviderFailure('provider HTTP 429 body', public_reason='provider_http_429')
        class Bare:
            name = 'bare'; scientific = False
            def complete(self, request): raise RuntimeError('secret body text')
        for provider, reason in ((Failing(), 'provider_rate_limit'), (Bare(), 'provider_unknown')):
            journal = Journal(); r = Runner(provider, journal, 1)
            self.assertIsNone(r.call('ballot', {'task': {}}, 'x:0:reports', 0))
            event = next(e for e in journal.events if e['kind'] == 'provider_failure')
            self.assertEqual(event['reason'], reason); self.assertNotIn('body', json.dumps(event))


if __name__ == '__main__':
    unittest.main(verbosity=2)
