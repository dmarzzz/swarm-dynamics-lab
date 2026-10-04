"""Offline tests. No network, no model, no hub.  Run: python3 src/selftest.py"""
import io
import json
import os
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path

import adapter
import analyze
import budget
import config
import contexts
import coordinator
import generate
import journal
import launch
import parse
import policy
import prompts
import protocol
import render
import s0
import score
import seeds
import study
import worker
from state import AccessDenied, Board, Vault

PLAN = {'s1q': (12, 12, 0), 's1r': (672, 480, 192), 's1l': (4080, 2880, 1200)}


class Seeds(unittest.TestCase):
    def test_derivation_is_stable_and_keyed(self):
        self.assertEqual(seeds.derive(730071, 'world', 's1l', 7), seeds.derive(730071, 'world', 's1l', 7))
        distinct = {seeds.derive(730071, s, 's1l', 7) for s in seeds.STREAMS}
        self.assertEqual(len(distinct), len(seeds.STREAMS))
        with self.assertRaises(ValueError):
            seeds.derive(730071, 'mutable', 1)

    def test_known_vector(self):
        # sha256('[730071,"world","s1l",7]') first 8 bytes, big-endian: fixes the derivation rule.
        import hashlib
        expected = int.from_bytes(hashlib.sha256(b'[730071,"world","s1l",7]').digest()[:8], 'big')
        self.assertEqual(seeds.derive(730071, 'world', 's1l', 7), expected)

    def test_stream_is_portable_and_unbiased_enough(self):
        a, b = seeds.Stream(5), seeds.Stream(5)
        self.assertEqual([a.randbelow(10) for _ in range(50)], [b.randbelow(10) for _ in range(50)])
        self.assertEqual(sorted(seeds.Stream(9).shuffled(range(20))), list(range(20)))
        counts = [0] * 5
        s = seeds.Stream(11)
        for _ in range(5000):
            counts[s.randbelow(5)] += 1
        self.assertTrue(all(850 < c < 1150 for c in counts), counts)

    def test_shared_first_pass_seed_excludes_arm(self):
        with tempfile.TemporaryDirectory() as td:
            log = journal.Journal(Path(td) / 'j', {})
            self.addCleanup(log.close)
            c = protocol.Controller('s1l', None, None, log)
            world, _ = generate.generate('s1l', 3)
            self.assertEqual(c._meta(world, 1, 'shared', 2, 'initial')['seed'],
                             seeds.derive(730071, 'initial', 's1l', 3, 1, 2))
            a = c._meta(world, 1, 'private', 2, 'discussion')['seed']
            b = c._meta(world, 1, 'public', 2, 'discussion')['seed']
            self.assertNotEqual(a, b)


class Generator(unittest.TestCase):
    def test_every_world_has_one_checked_answer(self):
        for stage in config.STAGES:
            cfg = config.stage_config(stage)
            pairs = study.worlds(stage)   # raises if the independent solver disagrees
            self.assertEqual(len(pairs), cfg['worlds'])
            regimes = [w['meta']['regime'] for w, _ in pairs]
            for regime in config.REGIMES:
                self.assertEqual(regimes.count(regime), cfg['worlds_per_regime'])
            for world, truth in pairs:
                costs = {r['supplier']: r['value'] for r in world['records'] if r['field'] == 'cost'}
                self.assertEqual(len(world['records']), 5)
                self.assertTrue(all(20 <= r['value'] <= 100 for r in world['records'] if r['field'] == 'cost'))
                self.assertTrue(all(1 <= r['value'] <= 10 for r in world['records'] if r['field'] == 'delivery'))
                self.assertEqual(world['records'][4]['source'], 'audit')
                self.assertTrue(all(world['records'][4]['day'] > r['day'] for r in world['records'][:4]))
                self.assertNotIn('"correct"', json.dumps(world))      # the answer key is not in the public world
                self.assertNotIn('TRUTH-', json.dumps(world))
                if world['meta']['regime'] != 'clean':
                    self.assertNotEqual(truth['correct'], truth['old_favored'])

    def test_allocation_matches_regimes(self):
        for world, truth in study.worlds('s1l'):
            holds = [len(world['allocation'][a]) for a in range(5)]
            regime = world['meta']['regime']
            if regime == 'clean':
                self.assertEqual(holds, [5] * 5)
                self.assertIsNone(world['special_agent'])
            elif regime == 'informed_minority':
                self.assertEqual(sorted(holds), [4, 4, 4, 4, 5])
                self.assertEqual(holds[world['special_agent']], 5)
            else:
                self.assertEqual(sorted(holds), [4, 5, 5, 5, 5])
                self.assertEqual(holds[world['special_agent']], 4)

    def test_truth_is_keyed_by_stage_and_world_not_repeat(self):
        w1, t1 = generate.generate('s1l', 5)
        w2, t2 = generate.generate('s1l', 5)
        self.assertEqual((w1, t1), (w2, t2))
        self.assertNotEqual(generate.generate('s1r', 5)[0]['records'], w1['records'])
        p0, p1 = generate.presentation(w1, t1, 0), generate.presentation(w1, t1, 1)
        self.assertNotEqual(p0['label_of'], p1['label_of'])          # counterbalanced presentation
        self.assertEqual(set(p0['label_of'].values()), {'A', 'B'})

    def test_displayed_correct_label_is_balanced(self):
        for stage in ('s1q', 's1r', 's1l', 's0'):
            cfg = config.stage_config(stage)
            repeats = 1 if stage in ('s1q', 's0') else cfg['repeats']
            for repeat in range(repeats):
                for regime in config.REGIMES:
                    labels = [generate.presentation(w, t, repeat)['label_of'][t['correct']]
                              for w, t in study.worlds(stage) if w['meta']['regime'] == regime]
                    self.assertEqual(labels.count('A'), labels.count('B'), (stage, repeat, regime))

    def test_replay_focal_is_never_the_special_agent(self):
        for world, _ in study.worlds('s1r'):
            focal = generate.replay_focal(world)
            self.assertNotEqual(focal, world['special_agent'])
            self.assertIn(focal, range(5))


class PlanCounts(unittest.TestCase):
    def test_manifest_matches_the_plan_table_and_declared_caps(self):
        declared = config.execution()['budget']['stages']
        for stage, (total, public, aux) in PLAN.items():
            m = study.manifest(stage)
            self.assertEqual((m['counts']['total'], m['counts']['public'], m['counts']['aux']), (total, public, aux))
            self.assertEqual(len({c['call_id'] for c in m['calls']}), total)
            self.assertEqual(declared[stage]['max_calls'], total)
            self.assertEqual((declared[stage]['public'], declared[stage]['aux']), (public, aux))
        self.assertEqual(study.manifest('s1q')['counts']['episodes'], 12)
        self.assertEqual(study.manifest('s1r')['counts']['episodes'], 192)
        self.assertEqual(study.manifest('s1l')['counts']['episodes'], 240)

    def test_manifest_is_deterministic_and_public_safe(self):
        a, b = study.manifest('s1l'), study.manifest('s1l')
        self.assertEqual(a['manifest_hash'], b['manifest_hash'])
        text = json.dumps(a)
        self.assertNotIn('TRUTH-', text)
        self.assertNotIn('old_favored', text)

    def test_s2_is_closed(self):
        for stage in ('s2l', 's3', 'S2'):
            with self.assertRaises(ValueError):
                study.manifest(stage)
            with self.assertRaises(ValueError):
                coordinator.params(stage)

    def test_plan_check_still_passes(self):
        r = subprocess.run([sys.executable, str(config.ROOT / 'check_plan.py')], capture_output=True, text=True)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn('s1l | 24 | 240 | 4,800 | 4,080', r.stdout)

    def test_amendment_keeps_plan_values(self):
        d, ex = config.design(), config.execution()
        self.assertEqual(d['protocol']['automatic_retries'], 0)
        self.assertEqual(ex['retry']['answer_retries'], 0)
        self.assertEqual(ex['retry']['invalid_output_repairs'], 0)
        self.assertEqual(ex['limits']['request_timeout_seconds'], d['protocol']['request_timeout_seconds'])
        self.assertEqual(ex['limits']['episode_timeout_seconds'], d['protocol']['episode_timeout_seconds'])
        self.assertEqual(ex['limits']['max_inflight_requests'], d['protocol']['max_inflight_requests'])
        self.assertEqual(ex['limits']['input_token_cap_per_request'], d['model']['input_token_cap_per_request'])
        self.assertEqual(config.launch_manifest()['temperature'], d['model']['temperature'])
        self.assertEqual(config.launch_manifest()['model'], 'claude-haiku-4-5-20251001')
        self.assertEqual(config.thinking_budget(), 0)
        plan_caps = {p['id']: p['max_output_tokens'] for p in d['protocol']['phases']}
        plan_caps['qualification'] = config.stage_config('s1q')['output_tokens_per_agent']
        self.assertEqual(config.phase_caps(), plan_caps)       # launch manifest m1 keeps the plan's caps
        self.assertIsNone(ex['provider']['fallback_model'])
        self.assertEqual(ex['budget']['public_path_usd'] + ex['budget']['auxiliary_private_usd'], ex['budget']['study_usd_cap'])
        self.assertEqual(config.phase_caps(), {'initial': 256, 'discussion': 256, 'final_public': 64,
                                               'final_private': 64, 'qualification': 128})


class Parser(unittest.TestCase):
    GOOD = {'initial': {'choice': 'A', 'confidence': 0.7, 'evidence_ids': ['e03', 'e05'], 'justification': 'x'},
            'prepare': {'evidence_ids': ['e01'], 'inventory': 'x', 'uncertainties': 'y'},
            'discussion': {'message': 'm', 'evidence_ids': [], 'recommendation': 'NONE'},
            'final': {'choice': 'ABSTAIN', 'confidence': 1},
            'qualification': {'choice': 'B', 'confidence': 0, 'justification': 'x'}}

    def test_valid_records(self):
        for kind, record in self.GOOD.items():
            self.assertEqual(parse.parse(kind, json.dumps(record)), record)

    def test_no_repair(self):
        bad = [
            ('final', '{"choice":"A","confidence":0.7'),                       # malformed
            ('final', 'Answer: {"choice":"A","confidence":0.7}'),              # prose around JSON
            ('final', '{"choice":"A"}'),                                       # missing field
            ('final', '{"choice":"A","confidence":0.7,"note":"x"}'),           # extra field
            ('final', '{"choice":"a","confidence":0.7}'),                      # wrong case
            ('final', '{"choice":"C","confidence":0.7}'),
            ('final', '{"choice":"A","confidence":70}'),                       # out of range
            ('final', '{"choice":"A","confidence":"0.7"}'),
            ('final', '{"choice":"A","confidence":true}'),
            ('final', '{"choice":"A","confidence":NaN}'),
            ('final', '[{"choice":"A","confidence":0.7}]'),
            ('initial', json.dumps(dict(self.GOOD['initial'], evidence_ids=['e03', 'e03']))),
            ('initial', json.dumps(dict(self.GOOD['initial'], evidence_ids=['e09']))),
            ('initial', json.dumps(dict(self.GOOD['initial'], justification='  '))),
            ('discussion', json.dumps(dict(self.GOOD['discussion'], recommendation='maybe'))),
            ('final', None),
        ]
        for kind, text in bad:
            with self.assertRaises(parse.Invalid, msg=text):
                parse.parse(kind, text)

    def test_schemas_use_only_supported_keywords(self):
        text = json.dumps(parse.SCHEMAS)
        for keyword in ('minimum', 'maximum', 'minLength', 'maxLength', 'pattern', 'minItems'):
            self.assertNotIn(keyword, text)
        for schema in parse.SCHEMAS.values():
            self.assertIs(schema['additionalProperties'], False)
            self.assertEqual(set(schema['required']), set(schema['properties']))


class Scorer(unittest.TestCase):
    def setUp(self):
        self.world, self.truth = generate.generate('s1l', 1)
        self.pres = generate.presentation(self.world, self.truth, 0)
        self.ev = score.Evaluator(self.world, self.truth, self.pres)
        self.right = self.ev.correct_label()
        self.wrong = 'B' if self.right == 'A' else 'A'

    def test_grading_goes_through_the_repeat_mapping(self):
        other = score.Evaluator(self.world, self.truth, generate.presentation(self.world, self.truth, 1))
        self.assertNotEqual(self.right, other.correct_label())
        self.assertEqual(self.ev.grade({'choice': self.right}), 'correct')
        self.assertEqual(self.ev.grade({'choice': self.wrong}), 'wrong')
        self.assertEqual(self.ev.grade({'choice': 'ABSTAIN'}), 'abstain')
        self.assertIsNone(self.ev.grade(None))

    def test_majority_needs_three_of_five_assigned(self):
        v = lambda c: {'choice': c, 'confidence': .5}
        r, w = self.right, self.wrong
        self.assertEqual(score.decision_outcome(self.ev, [v(r), v(r), v(r), v(w), v(w)])[0], 'correct')
        self.assertEqual(score.decision_outcome(self.ev, [v(w), v(w), v(w), v(r), v(r)])[0], 'wrong')
        self.assertEqual(score.decision_outcome(self.ev, [v(r), v(r), v(w), v(w), v('ABSTAIN')])[0], 'no_majority')
        self.assertEqual(score.decision_outcome(self.ev, [v(r), v(r), None, None, None])[0], 'no_majority')
        self.assertEqual(score.decision_outcome(self.ev, [v(r), v(r), v(r), None, None])[0], 'correct')  # team may succeed with failed members
        self.assertEqual(score.decision_outcome(self.ev, [v('ABSTAIN')] * 5)[0], 'no_majority')
        self.assertEqual(score.decision_outcome(self.ev, [v(r)] * 5, execution='interrupted')[0], 'unavailable')
        self.assertEqual(score.decision_outcome(self.ev, [v(r)] * 5, on_time=False)[0], 'unavailable')

    def test_transitions(self):
        t = score.transition
        self.assertTrue(t('correct', 'wrong')['harmful'])
        self.assertTrue(t('wrong', 'correct')['useful'])
        self.assertFalse(t('correct', None)['harmful'])       # an invalid ending is not a harmful revision
        self.assertFalse(t('wrong', 'abstain')['useful'])
        self.assertFalse(t(None, 'correct')['eligible_useful'])   # no initial answer: revision undefined
        self.assertEqual(t('correct', None)['to'], 'missing')
        self.assertEqual(t('abstain', 'correct'), {'from': 'abstain', 'to': 'correct', 'harmful': False, 'useful': False,
                                                   'eligible_harmful': False, 'eligible_useful': False})

    def test_stale_citation_and_premature_choice(self):
        audit = self.pres['evidence_id']['r4']
        a = self.world['records'][4]
        old = next(self.pres['evidence_id'][r['key']] for r in self.world['records'][:4]
                   if r['supplier'] == a['supplier'] and r['field'] == a['field'])
        self.assertTrue(self.ev.stale_citation({'evidence_ids': [old]}))
        self.assertFalse(self.ev.stale_citation({'evidence_ids': [old, audit]}))
        self.assertTrue(score.premature_choice({'inventory': 'I recommend Option A.', 'uncertainties': 'none'}))
        self.assertTrue(score.premature_choice({'inventory': 'Option B is cheaper so we should pick it', 'uncertainties': 'x'}))
        self.assertFalse(score.premature_choice({'inventory': 'Option A costs 40 units; Option B costs 50 units.',
                                                 'uncertainties': 'A later record could replace these values.'}))

    def test_solver_is_independent_and_rejects_ambiguity(self):
        records = [dict(r) for r in self.world['records']]
        self.assertEqual(score.solve(records, 5), self.truth['correct'])
        tie = [{'supplier': s, 'field': f, 'value': v, 'day': 1} for s in ('s0', 's1') for f, v in (('cost', 50), ('delivery', 3))]
        self.assertIsNone(score.solve(tie, 5))
        late = [dict(r, value=9) if r['field'] == 'delivery' else r for r in tie]
        self.assertIsNone(score.solve(late, 5))
        self.assertIsNone(score.solve(tie[:3], 5))
        with self.assertRaises(AssertionError):
            score.check_world(self.world, dict(self.truth, correct=self.truth['old_favored']))


class StateAndContexts(unittest.TestCase):
    def setUp(self):
        self.world, self.truth = generate.generate('s1l', 1)   # informed minority
        self.pres = generate.presentation(self.world, self.truth, 0)
        self.renderer = contexts.Renderer(5, self.pres['label_of'], self.pres['evidence_id'])
        by_key = {r['key']: r for r in self.world['records']}
        self.held = {a: [by_key[k] for k in self.world['allocation'][a]] for a in range(5)}
        self.first = json.dumps({'choice': 'A', 'confidence': 0.7, 'evidence_ids': [], 'justification': 'SECRET-JUSTIFICATION'})

    def test_vault_is_write_once_and_owner_only(self):
        v = Vault()
        v.put(0, {'choice': 'A', 'confidence': .5, 'justification': 'j'}, 'raw')
        with self.assertRaises(AccessDenied):
            v.put(0, {}, 'again')
        with self.assertRaises(AccessDenied):
            v.read(0, ('agent', 1))
        self.assertEqual(v.read(0, ('agent', 0))['raw'], 'raw')
        self.assertEqual(v.public_fields(0), {'agent': 0, 'choice': 'A', 'confidence': .5})   # no justification
        v.put(1, None, None)
        self.assertEqual(v.public_fields(1), {'agent': 1, 'unavailable': True})
        clone = v.clone()
        clone.put(2, {'choice': 'B', 'confidence': 1}, 'r')
        self.assertFalse(v.has(2))

    def test_board_snapshots_are_immutable(self):
        b = Board()
        snap = b.publish('facts', [{'x': 1}])
        content = snap.content()
        content[0]['x'] = 2
        self.assertEqual(snap.content(), [{'x': 1}])
        with self.assertRaises(AttributeError):
            snap.kind = 'other'
        with self.assertRaises(AccessDenied):
            b.publish('facts', [])
        self.assertEqual(len(snap.sha256), 64)

    def test_first_pass_prompt_hides_the_future_and_the_truth(self):
        c = contexts.build('initial', 'shared', 0, self.renderer, self.held[0])
        text = contexts.text_of(c)
        for word in ('private', 'public', 'shared with', 'posted', 'vote', 'revise', 'provisional', 'Keep the choice',
                     's0', 's1', 'informed', 'minority', 'TRUTH'):
            self.assertNotIn(word, text)
        self.assertEqual(text.count('[e0'), 4)     # this agent holds four records, not the audit
        self.assertEqual(c['schema'], 'initial')
        self.assertEqual(contexts.build('initial', 'prepare', 0, self.renderer, self.held[0])['schema'], 'prepare')
        self.assertIn('Do not choose, rank, recommend, or imply a preferred option.',
                      contexts.text_of(contexts.build('initial', 'prepare', 0, self.renderer, self.held[0])))

    def test_arm_overlays_use_the_plan_wording(self):
        facts = self.world['records']
        votes = [{'agent': a, 'choice': 'A', 'confidence': 0.7} for a in range(4)] + [{'agent': 4, 'unavailable': True}]
        text = {}
        for arm in ('private', 'never', 'prepare'):
            text[arm] = contexts.text_of(contexts.build('discussion', arm, 0, self.renderer, self.held[0],
                                                        own_initial=self.first, facts=facts))
        text['public'] = contexts.text_of(contexts.build('discussion', 'public', 0, self.renderer, self.held[0],
                                                         own_initial=self.first, facts=facts, initial_votes=votes))
        text['vote'] = contexts.text_of(contexts.build('discussion', 'vote', 0, self.renderer, self.held[0], own_initial=self.first))
        provisional = 'Your first answer is provisional. Retain it or revise it according to the available evidence.'
        keep = 'Keep the choice recorded in your first answer, even if later information suggests another choice.'
        self.assertIn(provisional, text['private'])
        self.assertIn(provisional, text['public'])
        self.assertIn(provisional, text['vote'])
        self.assertIn(keep, text['never'])
        self.assertNotIn(keep, text['private'] + text['public'] + text['vote'] + text['prepare'])
        self.assertIn('Form a provisional choice from the available evidence; you may revise it before your final response.', text['prepare'])
        self.assertIn('Analyst 2: choice A, confidence 0.7', text['public'])
        self.assertIn('Analyst 1 (you): choice A', text['public'])
        self.assertIn('Analyst 5: record unavailable', text['public'])
        self.assertNotIn(': choice ', text['private'])
        self.assertEqual(text['private'].count('[e0'), 4 + 5)    # own four records, then the released five
        self.assertEqual(text['vote'].count('[e0'), 4 + 4)       # VOTE: only its own records, twice
        # PRIVATE and PUBLIC differ only in the visibility block.
        strip = lambda t: t.split('First answers have')[0] + t.split('Your first answer is provisional')[1]
        self.assertEqual(strip(text['private']), strip(text['public']))

    def test_forbidden_sources_are_refused(self):
        facts = self.world['records']
        with self.assertRaises(contexts.AccessError):
            contexts.build('discussion', 'vote', 0, self.renderer, self.held[0], own_initial=self.first, facts=facts)
        with self.assertRaises(contexts.AccessError):
            contexts.build('discussion', 'private', 0, self.renderer, self.held[0], own_initial=self.first, facts=facts,
                           initial_votes=[{'agent': 1, 'choice': 'A', 'confidence': 1}])
        with self.assertRaises(contexts.AccessError):
            contexts.build('discussion', 'private', 0, self.renderer, self.held[0], own_initial=self.first)
        with self.assertRaises(contexts.AccessError):
            contexts.build('final', 'vote', 0, self.renderer, self.held[0], own_initial=self.first, own_discussion='{}',
                           discussion=[], final_kind='public')
        with self.assertRaises(contexts.AccessError):
            contexts.build('discussion', 'private', 0, self.renderer, self.held[0], facts=facts)

    def test_final_forks_differ_only_in_the_ask(self):
        facts = self.world['records']
        board = [{'agent': a, 'message': 'line one\nline two', 'evidence_ids': ['e01'], 'recommendation': 'A'} for a in range(4)]
        board.append({'agent': 4, 'unavailable': True})
        kw = dict(own_initial=self.first, own_discussion='{"message":"m","evidence_ids":[],"recommendation":"A"}',
                  facts=facts, discussion=board)
        pub = contexts.build('final', 'private', 0, self.renderer, self.held[0], final_kind='public', **kw)
        prv = contexts.build('final', 'private', 0, self.renderer, self.held[0], final_kind='private', **kw)
        again = contexts.build('final', 'private', 0, self.renderer, self.held[0], final_kind='private', **kw)
        self.assertEqual(prv, again)                                   # private/private fork: identical bytes
        self.assertEqual(pub['messages'][:-1], prv['messages'][:-1])
        self.assertIn("It is counted in the team's final vote.", pub['messages'][-1]['content'])
        self.assertIn('confidential', prv['messages'][-1]['content'])
        self.assertIn('Analyst 5 | message unavailable', pub['messages'][-1]['content'])
        self.assertIn('message: line one line two', pub['messages'][-1]['content'])   # one line per peer message
        self.assertEqual([m['role'] for m in pub['messages']], ['user', 'assistant', 'user', 'assistant', 'user'])

    def test_scripted_policy_reads_only_the_rendered_text(self):
        c = contexts.build('initial', 'shared', 4, self.renderer, self.held[4])
        records = policy.read_records(contexts.text_of(c))
        self.assertEqual(len(records), 5)
        choice, _ = policy.decide(records, 5)
        self.assertEqual(choice, self.pres['label_of'][self.truth['correct']])
        old, _ = policy.decide(policy.read_records(contexts.text_of(
            contexts.build('initial', 'shared', 0, self.renderer, self.held[0]))), 5)
        self.assertEqual(old, self.pres['label_of'][self.truth['old_favored']])


class Ledger(unittest.TestCase):
    def caps(self, public=3, aux=1, study=10.0, pub_usd=8.0, aux_usd=2.0):
        return {'study_micro_usd': int(study * 1e6), 'pool_micro_usd': {'public': int(pub_usd * 1e6), 'aux': int(aux_usd * 1e6)},
                'stages': {'s': {'public': public, 'aux': aux, 'attempts': public + aux + 1}}}

    def test_reservation_settlement_and_caps(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = budget.Ledger(Path(td) / 'ledger.jsonl', self.caps())
            ledger.reserve('a', 's', 'public', 2_000_000)
            with self.assertRaises(budget.BudgetError) as e:
                ledger.reserve('a', 's', 'public', 1)
            self.assertEqual(e.exception.category, 'duplicate_call_refused')
            ledger.settle('a', 500_000, 100, 20)
            self.assertEqual(ledger.totals()['committed_usd'], 0.5)       # reservation replaced by the billed amount
            ledger.reserve('b', 's', 'public', 7_000_000)
            with self.assertRaises(budget.BudgetError) as e:
                ledger.reserve('c', 's', 'public', 1_000_000)             # 0.5 + 7 + 1 > 8 public dollars
            self.assertEqual(e.exception.category, 'dollar_budget_exhausted')
            ledger.unknown('b')                                           # unknown outcome keeps the reservation
            self.assertEqual(ledger.totals()['committed_usd'], 7.5)
            with self.assertRaises(budget.BudgetError):
                ledger.settle('b', 1)
            ledger.reserve('p', 's', 'aux', 1_000_000)
            with self.assertRaises(budget.BudgetError) as e:
                ledger.reserve('q', 's', 'aux', 1)                        # aux call cap is 1
            self.assertEqual(e.exception.category, 'call_budget_exhausted')
            ledger.reserve('c', 's', 'public', 100)                       # public path unaffected by the aux pool
            with self.assertRaises(budget.BudgetError):
                ledger.reserve('d', 's', 'public', 1)                     # public call cap is 3
            with self.assertRaises(budget.BudgetError):
                ledger.reserve('z', 'other-stage', 'public', 1)
            # a second process sees the same state
            again = budget.Ledger(Path(td) / 'ledger.jsonl', self.caps())
            self.assertEqual(again.totals(), ledger.totals())
            with self.assertRaises(budget.BudgetError):
                again.reserve('a', 's', 'public', 1)

    def test_attempt_cap_and_partial_write(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'ledger.jsonl'
            ledger = budget.Ledger(path, self.caps())
            with self.assertRaises(budget.BudgetError):
                ledger.attempt('ghost', 's')
            ledger.reserve('a', 's', 'public', 1)
            for _ in range(5):
                ledger.attempt('a', 's')
            with self.assertRaises(budget.BudgetError) as e:
                ledger.attempt('a', 's')
            self.assertEqual(e.exception.category, 'attempt_budget_exhausted')
            with open(path, 'a') as f:
                f.write('{"type": "reserve", "call_id": "x"')            # torn write
            with self.assertRaises(budget.BudgetError) as e:
                budget.Ledger(path, self.caps()).totals()
            self.assertEqual(e.exception.category, 'ledger_partial_write')

    def test_declared_caps(self):
        ex = config.execution()
        caps = budget.caps_for({'s1l': {'public': 2880, 'aux': 1200}}, ex)
        self.assertEqual(caps['study_micro_usd'], 40_000_000)
        self.assertEqual(caps['pool_micro_usd'], {'public': 30_000_000, 'aux': 10_000_000})
        self.assertEqual(caps['stages']['s1q'], {'public': 12, 'aux': 0, 'attempts': 18})
        self.assertEqual(caps['stages']['s1r'], {'public': 480, 'aux': 192, 'attempts': 706})
        self.assertEqual(caps['stages']['s1l'], {'public': 2880, 'aux': 1200, 'attempts': 4284})
        with self.assertRaises(budget.BudgetError):
            budget.caps_for({'s1l': {'public': 2881, 'aux': 1200}}, ex)
        with self.assertRaises(budget.BudgetError):
            budget.caps_for({'s2l': {'public': 1, 'aux': 1}}, ex)


class FakeResponse:
    def __init__(self, payload):
        self.payload = json.dumps(payload).encode()

    def __enter__(self):
        return self

    def __exit__(self, *a):
        return False

    def read(self, n=-1):
        return self.payload


def http_error(code, message='x', headers=None):
    return urllib.error.HTTPError('https://api.anthropic.com/v1/messages', code, 'err', headers or {},
                                  io.BytesIO(json.dumps({'error': {'message': message}}).encode()))


def ok_payload(text='{"choice":"A","confidence":0.7}', **over):
    base = {'model': 'claude-haiku-4-5-20251001', 'stop_reason': 'end_turn',
            'content': [{'type': 'text', 'text': text}], 'usage': {'input_tokens': 300, 'output_tokens': 12}}
    base.update(over)
    return base


class Provider(unittest.TestCase):
    CALL = {'call_id': 'c1', 'system': 'sys', 'messages': [{'role': 'user', 'content': 'hi'}], 'schema': 'final', 'max_tokens': 64}

    def make(self, script, attempts=None):
        os.environ['SWARM_MODEL_API_KEY'] = 'test-key-not-real'
        os.environ['SWARM_MODEL_WORKSPACE_ID'] = 'test-workspace'
        self.requests = []
        clock = [0.0]

        def opener(request, timeout):
            self.requests.append((request, timeout))
            step = script.pop(0)
            if isinstance(step, Exception):
                raise step
            return FakeResponse(step)

        def sleep(seconds):
            clock[0] += seconds
        return adapter.AnthropicAdapter((attempts if attempts is not None else self.attempts).append, opener=opener,
                                        sleep=sleep, clock=lambda: clock[0])

    def setUp(self):
        self.attempts = []

    def tearDown(self):
        os.environ.pop('SWARM_MODEL_API_KEY', None)
        os.environ.pop('SWARM_MODEL_WORKSPACE_ID', None)

    def test_request_shape(self):
        a = self.make([ok_payload()])
        r = a.complete(self.CALL)
        self.assertTrue(r['ok'])
        self.assertEqual(r['billing'], 'billed')
        request, timeout = self.requests[0]
        body = json.loads(request.data)
        self.assertEqual(body['model'], 'claude-haiku-4-5-20251001')
        self.assertEqual(body['temperature'], 0.7)
        self.assertEqual(body['max_tokens'], 64)
        self.assertEqual(body['output_config'], {'format': {'type': 'json_schema', 'schema': parse.SCHEMAS['final']}})
        self.assertEqual(set(body), {'model', 'max_tokens', 'temperature', 'system', 'messages', 'output_config'})
        self.assertNotIn('thinking', body)
        self.assertEqual(request.full_url, 'https://api.anthropic.com/v1/messages')
        self.assertEqual(request.get_header('X-api-key'), 'test-key-not-real')
        self.assertLessEqual(timeout, 60)
        self.assertNotIn('test-key-not-real', json.dumps(r))

    def test_rate_limit_and_overload_are_retried_within_one_request_budget(self):
        a = self.make([http_error(429), http_error(529), ok_payload()])
        r = a.complete(self.CALL)
        self.assertTrue(r['ok'])
        self.assertEqual(r['attempts'], 3)
        self.assertEqual(self.attempts, ['c1'] * 3)
        a = self.make([http_error(529), http_error(529), http_error(529), ok_payload()])
        r = a.complete(self.CALL)
        self.assertEqual((r['ok'], r['failure'], r['attempts'], r['billing']), (False, 'http_529', 3, 'none'))
        a = self.make([http_error(429, headers={'retry-after': '500'}), ok_payload()])
        r = a.complete(self.CALL)                      # the wait is capped, never past the 60 s budget
        self.assertTrue(r['ok'])
        self.assertLessEqual(r['latency'], 60)

    def test_nothing_else_is_retried(self):
        for step, failure, billing in [
                (http_error(500), 'http_500', 'none'), (http_error(400), 'http_400', 'none'),
                (http_error(401), 'http_401', 'none'),
                (http_error(400, 'Your credit balance is too low to access the API'), 'credit_balance_low', 'none'),
                (TimeoutError(), 'timeout', 'unknown'), (urllib.error.URLError(TimeoutError()), 'timeout', 'unknown'),
                (urllib.error.URLError('refused'), 'transport_error', 'unknown'),
                (ok_payload(stop_reason='max_tokens'), 'truncated', 'billed'),
                (ok_payload(stop_reason='refusal'), 'refusal', 'billed'),
                (ok_payload(model='claude-haiku-4-5'), 'model_mismatch', 'billed'),
                (ok_payload(usage={'input_tokens': 5}), 'missing_usage', 'unknown'),
                (ok_payload(usage={'input_tokens': 5, 'output_tokens': 5, 'cache_read_input_tokens': 9}), 'unexpected_cache_usage', 'billed'),
                (ok_payload(content=[{'type': 'text', 'text': 'a'}, {'type': 'text', 'text': 'b'}]), 'unexpected_content_blocks', 'billed')]:
            a = self.make([step, ok_payload()])
            r = a.complete(self.CALL)
            self.assertEqual((r['ok'], r['failure'], r['billing'], r['attempts']), (False, failure, billing, 1), failure)
            self.assertEqual(len(self.requests), 1)

    def test_failed_calls_keep_their_text_for_the_journal_only(self):
        a = self.make([ok_payload(text='{"choice":"A","confi', stop_reason='max_tokens')])
        r = a.complete(self.CALL)
        self.assertEqual((r['ok'], r['failure'], r['text']), (False, 'truncated', '{"choice":"A","confi'))

    def test_attempt_refusal_and_missing_key(self):
        def refuse(call_id):
            raise budget.BudgetError('attempt_budget_exhausted')
        a = self.make([ok_payload()])
        a.on_attempt = refuse
        r = a.complete(self.CALL)
        self.assertEqual((r['ok'], r['failure'], len(self.requests)), (False, 'attempt_budget_exhausted', 0))
        os.environ.pop('SWARM_MODEL_API_KEY')
        with self.assertRaises(RuntimeError):
            adapter.AnthropicAdapter(lambda c: None)


class ControllerFaults(unittest.TestCase):
    """The controller against a fake provider: breaker, token cap, accounting."""

    def run_stage(self, td, script_for, stage='s1q', limits=None):
        plan = study.manifest(stage)
        ledger = study.paid_ledger(Path(td) / 'ledger.jsonl', plan)

        class Fake:
            scripted = False

            def __init__(self, on_attempt):
                self.on_attempt = on_attempt
                self.n = 0

            def complete(self, call):
                self.on_attempt(call['call_id'])
                self.n += 1
                return script_for(self.n, call)
        return study.run(plan, Path(td), Fake, ledger, limits=limits) + (ledger,)

    @staticmethod
    def good(call, tokens=300):
        text = policy.evidence_follower(call)
        return {'ok': True, 'text': text, 'failure': None, 'usage': {'input_tokens': tokens, 'output_tokens': 20},
                'billing': 'billed', 'latency': 1.0, 'attempts': 1, 'stop_reason': 'end_turn'}

    @staticmethod
    def bad(failure, billing='none'):
        return {'ok': False, 'text': None, 'failure': failure, 'usage': {}, 'billing': billing, 'latency': 1.0,
                'attempts': 1, 'stop_reason': None}

    def test_clean_qualification_bills_exactly(self):
        with tempfile.TemporaryDirectory() as td:
            episodes, controller, crash, ledger = self.run_stage(td, lambda n, call: self.good(call))
            self.assertEqual(analyze.qualification(episodes)['passed'], True)
            totals = ledger.totals()
            self.assertEqual(totals['logical_calls'], 12)
            self.assertAlmostEqual(totals['billed_usd'], 12 * (300 * 1 + 20 * 5) / 1e6)
            self.assertEqual(totals['open_reserved_usd'], 0)
            self.assertAlmostEqual(controller.totals['billed_usd'], totals['billed_usd'])

    def test_auth_failure_halts_at_once(self):
        with tempfile.TemporaryDirectory() as td:
            episodes, controller, crash, ledger = self.run_stage(td, lambda n, call: self.bad('http_401'))
            self.assertEqual(controller.halted, 'http_401')
            self.assertEqual(ledger.totals()['logical_calls'], 1)
            self.assertEqual(len(episodes), 12)
            self.assertEqual([e['execution'] for e in episodes].count('incomplete'), 11)
            self.assertFalse(analyze.qualification(episodes)['passed'])

    def test_five_consecutive_provider_failures_halt(self):
        with tempfile.TemporaryDirectory() as td:
            episodes, controller, crash, ledger = self.run_stage(
                td, lambda n, call: self.good(call) if n <= 2 else self.bad('timeout', 'unknown'))
            self.assertEqual(controller.halted, 'consecutive_provider_failures')
            totals = ledger.totals()
            self.assertEqual(totals['logical_calls'], 7)
            self.assertEqual(totals['unknown_cost_calls'], 5)
            self.assertGreater(totals['open_reserved_usd'], 0)

    def test_input_token_cap_is_enforced_on_measured_usage(self):
        with tempfile.TemporaryDirectory() as td:
            # A roomy reservation envelope, so the measured-usage cap (not the reservation bound) is what trips.
            episodes, controller, crash, ledger = self.run_stage(
                td, lambda n, call: self.good(call, tokens=4097 if n == 3 else 300), limits={'reservation_envelope_tokens': 8000})
            self.assertIsNone(controller.halted)
            failed = [e for e in episodes if not e['valid']]
            self.assertEqual(len(failed), 1)
            self.assertEqual(failed[0]['failure'], 'input_token_cap_exceeded')
            self.assertEqual(failed[0]['flags'], ['qualification:overflow'])

    def test_reservation_breach_halts(self):
        with tempfile.TemporaryDirectory() as td:
            episodes, controller, crash, ledger = self.run_stage(td, lambda n, call: self.good(call, tokens=10 ** 6))
            self.assertEqual(controller.halted, 'reservation_bound_breached')

    def test_reservation_covers_the_worst_case(self):
        with tempfile.TemporaryDirectory() as td:
            log = journal.Journal(Path(td) / 'j', {})
            self.addCleanup(log.close)
            c = protocol.Controller('s1l', None, None, log)
            world, truth = generate.generate('s1l', 0)
            pres = generate.presentation(world, truth, 0)
            ctx = contexts.build('initial', 'shared', 0, contexts.Renderer(5, pres['label_of'], pres['evidence_id']), world['records'])
            micro = c._reservation(ctx, 256)
            self.assertEqual(micro, (contexts.request_bytes(ctx) + 1024) * 1 + 256 * 5)
            self.assertLess(micro / 1e6, 0.01)


class PaidPathRehearsal(unittest.TestCase):
    """The paid code path end to end with a scripted provider. No approval record exists, so the
    real path must refuse; the rehearsal substitutes the gate, the provider and the ledger."""

    def test_no_model_call_without_approval(self):
        if launch.APPROVAL.exists():
            self.skipTest('approval record present')
        with self.assertRaises(launch.NotApproved):
            launch.check('s1q')
        with tempfile.TemporaryDirectory() as td:
            with self.assertRaises(launch.NotApproved):
                worker.execute(dict(coordinator.params('s1q')), Path(td) / 'out')
            self.assertFalse((Path(td) / 'out' / 'manifest.json').exists())

        class Hub:
            def runs(self, *a, **k):
                return []
        with self.assertRaises(launch.NotApproved):
            coordinator.enqueue(Hub(), 's1q')
        with self.assertRaises(launch.NotApproved):
            launch.check('s2l')

    def test_approval_is_pinned_to_runtime_review_and_waiver(self):
        if launch.APPROVAL.exists():
            self.skipTest('approval record present')
        review, waiver = config.ROOT / 'reviews' / 's1-pre.md', config.ROOT / 'launch' / 'review-waiver.md'
        if not (review.exists() and waiver.exists()):
            self.skipTest('review documents not written yet')
        record = {'status': 'approved', 'reviewer': 'dmarz/fleet-monitor', 'stages': ['s1q'],
                  'source_hash': config.source_hash(),
                  'pre_run_review': {'path': 'reviews/s1-pre.md', 'sha256': config.sha256_file(review)},
                  'review_waiver': {'path': 'launch/review-waiver.md', 'sha256': config.sha256_file(waiver)}}
        try:
            launch.APPROVAL.write_text(json.dumps(record))
            self.assertEqual(launch.check('s1q')['status'], 'approved')
            with self.assertRaises(launch.NotApproved):
                launch.check('s1l')                                  # stage not covered
            for change in ({'status': 'pending'}, {'reviewer': 'dmarz/soc07-private'}, {'source_hash': 'x'},
                           {'pre_run_review': {'path': 'reviews/s1-pre.md', 'sha256': 'x'}}):
                launch.APPROVAL.write_text(json.dumps(dict(record, **change)))
                with self.assertRaises(launch.NotApproved):
                    launch.check('s1q')
        finally:
            launch.APPROVAL.unlink()

    def rehearse(self, stage):
        original = launch.check
        launch.check = lambda s: {'status': 'rehearsal'}
        try:
            with tempfile.TemporaryDirectory() as td:
                plan = study.manifest(stage)
                ledger = study.paid_ledger(Path(td) / 'ledger.jsonl', plan)
                table = {w['id']: (w, t) for w, t in study.worlds(stage)}
                factory = lambda on_attempt: adapter.ScriptedAdapter('evidence_follower', on_attempt=on_attempt)
                doc = worker.execute(dict(coordinator.params(stage), backend='anthropic'), Path(td) / 'out',
                                     adapter_factory=factory, ledger=ledger)
                analysis = json.loads((Path(td) / 'out' / 'analysis.json').read_text())
                from PIL import Image
                with Image.open(Path(td) / 'out' / 'final_frame.png') as im:
                    self.assertEqual(im.size, (1800, 1200))
                with Image.open(Path(td) / 'out' / 'replay.gif') as im:
                    self.assertLessEqual(im.n_frames, 25)
                    self.assertEqual(im.n_frames, doc['visualization']['frames'])
                return doc, analysis, ledger.totals()
        finally:
            launch.check = original

    def test_s1q_rehearsal(self):
        doc, analysis, totals = self.rehearse('s1q')
        self.assertTrue(doc['gate']['passed'])
        self.assertEqual(doc['reconciliation'], {'planned': 12, 'terminal': 12, 'completed': 12, 'interrupted': 0,
                                                 'incomplete': 0, 'graded': 12, 'analyzed': 12})
        self.assertEqual(totals['calls_by_stage'], {'s1q': {'public': 12, 'aux': 0}})

    def test_s1r_rehearsal(self):
        doc, analysis, totals = self.rehearse('s1r')
        self.assertTrue(doc['gate']['passed'])
        self.assertEqual(doc['calls']['valid'], 672)
        self.assertEqual(totals['calls_by_stage'], {'s1r': {'public': 480, 'aux': 192}})
        self.assertEqual(doc['reconciliation']['completed'], 192)
        self.assertEqual(analysis['primary']['difference'], 0.0)
        self.assertEqual(analysis['arms']['private']['team_success'], 48)
        self.assertTrue(doc['gate']['checks']['clean_competence'])
        self.assertEqual(doc['calls']['by_phase']['final_private'], {'dispatched': 192, 'valid': 192, 'truncated': 0})

    def test_s1l_rehearsal(self):
        doc, analysis, totals = self.rehearse('s1l')
        self.assertTrue(doc['gate']['passed'])
        self.assertEqual(doc['calls']['valid'], 4080)
        self.assertEqual(doc['calls']['not_reached'], 0)
        self.assertEqual(totals['calls_by_stage'], {'s1l': {'public': 2880, 'aux': 1200}})
        self.assertEqual(doc['reconciliation']['completed'], 240)
        arms = analysis['arms']
        self.assertEqual({a: arms[a]['team_success'] for a in config.ARMS},
                         {'private': 48, 'public': 48, 'never': 48, 'prepare': 48, 'vote': 32})
        self.assertEqual(analysis['primary']['difference'], 0.0)
        self.assertEqual(analysis['primary']['worlds'], 24)
        vote = next(c for c in analysis['secondary'] if c['arm'] == 'vote')
        self.assertAlmostEqual(vote['difference'], -1 / 3)
        self.assertEqual(vote['by_regime']['informed_minority']['difference'], -1.0)
        self.assertEqual(analysis['designated_minority_guardrail']['shared_eligible'], 16)
        self.assertEqual(analysis['designated_minority_guardrail']['difference'], 0.0)
        self.assertLess(totals['committed_usd'], 40)


class amended:
    """Temporarily amend the launch manifest, as a dated amendment to execution.json would."""

    def __init__(self, **changes):
        self.changes = changes

    def __enter__(self):
        self.manifest = config.execution()['launch_manifest']
        self.saved = dict(self.manifest)
        self.manifest.update(self.changes)

    def __exit__(self, *a):
        self.manifest.clear()
        self.manifest.update(self.saved)


class LaunchManifest(unittest.TestCase):
    """A model switch is configuration: model id, reasoning allowance, output caps, prices and a
    fresh qualification set all come from the launch manifest and are recorded on the run."""

    def test_run_parameters_record_the_manifest(self):
        p = coordinator.params('s1q')
        self.assertEqual((p['model'], p['reasoning_tokens'], p['output_caps'], p['launch_manifest'], p['batch']),
                         ('claude-haiku-4-5-20251001', 0, '256/256/64/64/128', 'm1', 's1q-a1'))
        self.assertEqual(coordinator.params('s0')['model'], 'none')
        plan = study.manifest('s1q')
        self.assertEqual(plan['launch_manifest'], config.launch_manifest())
        registered = json.loads((config.ROOT / 'experiment.json').read_text())
        self.assertTrue(set(p) <= set(registered['params']), set(p) - set(registered['params']))

    def test_switch_needs_no_code_change(self):
        before = study.manifest('s1q')
        old_worlds = [w['records'] for w, _ in study.worlds('s1q')]
        switch = dict(version='m2', model='some-other-model', thinking={'type': 'budget', 'budget_tokens': 2048},
                      input_usd_per_million=3, output_usd_per_million=15, qualification_set=1)
        with amended(**switch):
            plan = study.manifest('s1q')
            self.assertEqual(plan['namespace'], 's1q.1')
            self.assertEqual(plan['counts']['total'], 12)
            self.assertTrue(all(c['call_id'].startswith('s1q.1/') for c in plan['calls']))
            new_worlds = [w['records'] for w, _ in study.worlds('s1q')]
            self.assertFalse(any(w in old_worlds for w in new_worlds))          # twelve fresh worlds
            self.assertEqual(study.manifest('s1l')['hashes']['public_worlds'],
                             json.loads(json.dumps(self.s1l_hash)))             # S1-L worlds do not move
            p = coordinator.params('s1q')
            self.assertEqual((p['model'], p['reasoning_tokens'], p['launch_manifest'], p['batch']),
                             ('some-other-model', 2048, 'm2', 's1q.1-a1'))
            os.environ['SWARM_MODEL_API_KEY'] = 'test-key-not-real'
            try:
                seen = []

                def opener(request, timeout):
                    seen.append(json.loads(request.data))
                    return FakeResponse(ok_payload(model='some-other-model', content=[
                        {'type': 'thinking', 'thinking': 'reasoning', 'signature': 'x'},
                        {'type': 'text', 'text': '{"choice":"A","confidence":0.7}'}],
                        usage={'input_tokens': 300, 'output_tokens': 900}))
                a = adapter.AnthropicAdapter(lambda c: None, opener=opener)
                with tempfile.TemporaryDirectory() as td:
                    log = journal.Journal(Path(td) / 'j', {})
                    self.addCleanup(log.close)
                    c = protocol.Controller('s1q', a, None, log)
                    self.assertEqual(c.caps['qualification'] + c.thinking, 128 + 2048)
                r = a.complete({'call_id': 'c', 'system': 's', 'messages': [{'role': 'user', 'content': 'u'}],
                                'schema': 'final', 'max_tokens': 64 + 2048})
            finally:
                os.environ.pop('SWARM_MODEL_API_KEY', None)
            self.assertTrue(r['ok'])
            self.assertEqual(r['text'], '{"choice":"A","confidence":0.7}')      # the reasoning block is never the answer
            self.assertEqual(seen[0]['model'], 'some-other-model')
            self.assertEqual(seen[0]['thinking'], {'type': 'enabled', 'budget_tokens': 2048})
            self.assertEqual(seen[0]['max_tokens'], 64 + 2048)
            self.assertNotIn('temperature', seen[0])
            # the ledger needs a declared cap for the new qualification set: without it the stage refuses to start
            with self.assertRaises(budget.BudgetError):
                budget.caps_for({plan['namespace']: plan['counts']}, config.execution())
        self.assertEqual(study.manifest('s1q')['manifest_hash'], before['manifest_hash'])

    def setUp(self):
        self.s1l_hash = study.manifest('s1l')['hashes']['public_worlds']

    def test_thinking_configuration_is_validated(self):
        for bad in ({'type': 'off', 'budget_tokens': 5}, {'type': 'budget', 'budget_tokens': 100}, {'type': 'adaptive', 'budget_tokens': 0}):
            with amended(thinking=bad):
                with self.assertRaises(ValueError):
                    config.thinking_budget()


class Analysis(unittest.TestCase):
    def episode(self, world, regime, arm, repeat, decision):
        return {'episode': '%s-%s-%d' % (world, arm, repeat), 'world': world, 'regime': regime, 'arm': arm, 'repeat': repeat,
                'decision': decision, 'execution': 'completed', 'private_vote_decision': decision, 'agents': [],
                'usage': {'calls': 20, 'input_tokens': 100 if arm == 'private' else 110, 'output_tokens': 10, 'billed_usd': 0.0}}

    def test_primary_contrast_averages_repeats_then_worlds_then_regimes(self):
        eps = []
        for regime, worlds in (('clean', ['c1', 'c2']), ('informed_minority', ['i1', 'i2']), ('correctable_minority', ['m1', 'm2'])):
            for w in worlds:
                for repeat in (0, 1):
                    private = 'correct'
                    public = 'wrong' if (regime == 'informed_minority' and (w == 'i1' or repeat == 0)) else 'correct'
                    eps += [self.episode(w, regime, 'private', repeat, private), self.episode(w, regime, 'public', repeat, public)]
        s = analyze.summarize(eps, bootstrap_repetitions=300)
        # informed minority: world i1 difference 1.0, world i2 difference 0.5 -> 0.75; other regimes 0 -> mean 0.25
        self.assertAlmostEqual(s['primary']['difference'], 0.25)
        self.assertAlmostEqual(s['primary']['by_regime']['informed_minority']['difference'], 0.75)
        self.assertEqual(s['primary']['worlds'], 6)
        self.assertEqual(s['primary']['interval_95'], analyze.summarize(eps, bootstrap_repetitions=300)['primary']['interval_95'])
        low, high = s['primary']['interval_95']['low_2.5'], s['primary']['interval_95']['high_97.5']
        self.assertTrue(1 / 6 - 1e-9 <= low <= 0.25 <= high <= 1 / 3 + 1e-9, (low, high))
        self.assertAlmostEqual(s['token_ratio_private_over_public']['ratio'], 110 / 120)

    def test_unfinished_episodes_count_as_failures(self):
        eps = [self.episode('c1', 'clean', 'private', 0, 'unavailable'), self.episode('c1', 'clean', 'public', 0, 'correct')]
        eps[0]['execution'] = 'interrupted'
        s = analyze.summarize(eps, bootstrap_repetitions=50)
        self.assertEqual(s['arms']['private']['by_regime']['clean']['team_success_rate'], 0.0)
        self.assertEqual(s['primary']['difference'], -1.0)
        self.assertEqual(s['execution'], {'completed': 1, 'interrupted': 1, 'incomplete': 0})

    def test_gate(self):
        stats = {'valid_rate': 0.96, 'budget_timeout_failure_rate': 0.01, 'duplicate_call_ids': 0, 'unplanned_call_ids': 0,
                 'by_phase': {'initial': {'dispatched': 100, 'valid': 96, 'truncated': 4}}}
        over = dict(stats, by_phase={'final_public': {'dispatched': 100, 'valid': 94, 'truncated': 6}})
        self.assertFalse(analyze.s1_gate(over, 0, None, None)['passed'])
        cell = lambda k: {'by_regime': {'clean': {'episodes': 16, 'team_success': k}}}
        self.assertTrue(analyze.s1_gate(stats, 0, None, None, 'replay', {'arms': {'private': cell(13), 'public': cell(16)}})['passed'])
        self.assertFalse(analyze.s1_gate(stats, 0, None, None, 'replay', {'arms': {'private': cell(12), 'public': cell(16)}})['passed'])
        self.assertFalse(analyze.s1_gate(stats, 0, None, None, 'replay', {'arms': {'private': cell(16)}})['passed'])
        self.assertNotIn('clean_competence', analyze.s1_gate(stats, 0, None, None, 'live', {'arms': {}})['checks'])
        self.assertTrue(analyze.s1_gate(stats, 0, None, None)['passed'])
        self.assertFalse(analyze.s1_gate(dict(stats, valid_rate=0.94), 0, None, None)['passed'])
        self.assertFalse(analyze.s1_gate(dict(stats, budget_timeout_failure_rate=0.05), 0, None, None)['passed'])
        self.assertFalse(analyze.s1_gate(stats, 1, None, None)['passed'])
        self.assertFalse(analyze.s1_gate(stats, 0, None, 'http_401')['passed'])


class JournalAndFrames(unittest.TestCase):
    def test_chain_detects_tampering(self):
        with tempfile.TemporaryDirectory() as td:
            path = Path(td) / 'j.jsonl'
            log = journal.Journal(path, {'a': 1})
            log.append('call', x=1)
            log.append('call', x=2)
            log.close()
            self.assertEqual([e['kind'] for e in journal.read(path)], ['journal_open', 'call', 'call'])
            lines = path.read_text().splitlines()
            path.write_text('\n'.join([lines[0], lines[1].replace('"x": 1', '"x": 9'), lines[2]]) + '\n')
            with self.assertRaises(ValueError):
                list(journal.read(path))
            path.write_text('\n'.join([lines[0], lines[2]]) + '\n')
            with self.assertRaises(ValueError):
                list(journal.read(path))

    def test_frames_render_empty_partial_and_failed_states(self):
        base = {'stage': 's1l', 'mode': 'live', 'backend': 'anthropic', 'planned_episodes': 240, 'blocks': 48,
                'blocks_done': 0, 'elapsed': 0.0, 'calls': 0, 'cost_usd': 0.0, 'input_tokens': 0, 'output_tokens': 0, 'failures': 0}
        self.assertEqual(render.frame([], base).size, (1800, 1200))
        self.assertEqual(render.cells([]), {})
        failed = study.incomplete_episode('x', 's1l', 's1l', 'interrupted')
        self.assertEqual(render.frame([failed], dict(base, blocks_done=1, failures=3)).size, (1800, 1200))
        self.assertEqual(render.cells([failed]), {})        # an unfinished episode never becomes a zero-height bar
        for stage, mode in (('s1q', 'qualification'), ('s1r', 'replay')):
            self.assertEqual(render.frame([], dict(base, stage=stage, mode=mode)).size, (1800, 1200))


class S0Suite(unittest.TestCase):
    def test_full_s0(self):
        with tempfile.TemporaryDirectory() as td:
            result = s0.run_suite(Path(td))
        failed = [c for c in result['report'].checks if not c['passed']]
        self.assertEqual(failed, [])
        self.assertEqual(result['counts'], {'worlds': 60, 'episodes': 1500, 'scripted_calls': 21300})
        self.assertGreaterEqual(len(result['report'].checks), 69)


class PublicRepositoryHygiene(unittest.TestCase):
    def test_no_addresses_or_credentials_in_this_directory(self):
        import re
        ip = re.compile(r'\b(?:\d{1,3}\.){3}\d{1,3}\b')
        for path in list(config.ROOT.glob('*')) + list(config.SRC.glob('*.py')) + list((config.ROOT / 'reviews').glob('*')) \
                + list((config.ROOT / 'launch').glob('*')):
            if not path.is_file() or path.suffix in ('.png', '.gif', '.gz'):
                continue
            text = path.read_text()
            self.assertIsNone(ip.search(text), path.name)
            for needle in ('sk-' + 'ant', 'SWARM_HUB_' + 'TOKEN=', 'sslip' + '.io', 'BEGIN ' + 'OPENSSH'):
                self.assertNotIn(needle, text, path.name)


if __name__ == '__main__':
    unittest.main(verbosity=1)
