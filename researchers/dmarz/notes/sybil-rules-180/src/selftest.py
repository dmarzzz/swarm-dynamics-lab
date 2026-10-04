"""Offline selftests: no network, no model call. Run: python3 src/selftest.py

Covers the economy engine (delays, conservation, licences, retirement, checkpoint), the frozen design values the
reviewer fixed before any call, the coordinator's transport (lost-task re-issue, duplicate guards, expiry,
polling back-off, worker silence), the software gates, the scripted S0 stage, and (imported) the adapter tests
of test_provider.py.
"""
import copy
import json
import os
import re
import sys
import tempfile
import unittest
import urllib.error
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parent))
# The launcher's setup runs these tests with STUDY_MODEL set to the launched model. The tests fix the model they
# test themselves, so the ambient choice is removed here (it never reaches the source hash).
os.environ.pop('STUDY_MODEL', None)

import coordinator
import provider
import rehearse
import sim
import study
import transport
import worker
from test_provider import Answers, Billing, Request, Transport  # noqa: F401  (the adapter tests run here too)
import openai_provider
import test_openai_provider as _toap
OpenAIRequest, OpenAICost, OpenAIAnswers, OpenAITransport, OpenAIBilling, OpenAIStubServer, OpenAILedgerRules = (
    _toap.Request, _toap.Cost, _toap.Answers, _toap.Transport, _toap.Billing, _toap.StubServer, _toap.LedgerRules)


def world():
    return study.main_world()


def act(admin=None, production=None, message='', memo=''):
    return {'memo': memo, 'admin': admin or {'command': 'noop'}, 'production': production or {}, 'message': message}


def full_production(state, oid, minus=None):
    o = state['owners'][oid]
    minus = minus or {}
    return {fid: f['capacity'] - minus.get(fid, 0) for fid, f in o['firms'].items() if f['status'] == 'active'}


class Engine(unittest.TestCase):
    def play(self, state, chosen, rules=None):
        """One round; owners not in `chosen` file a no-op and produce their full active capacity."""
        sim.begin_round(state)
        responses = {oid: chosen.get(oid) or act(production=full_production(state, oid)) for oid in state['owners']}
        recs = sim.step(state, responses, rules or {'regime': 'none'})
        self.assertEqual(sim.conservation(state), [])
        self.assertFalse(sim.record_accounting(recs))
        return recs

    def owner_row(self, recs, oid):
        return next(r['owners'][oid] for r in recs if oid in r['owners'])

    def test_register_then_transfer_then_produce(self):
        s = world()
        oid = 'own-00a'
        o = s['owners'][oid]
        start = s['markets'][0]['start_product']
        first = next(iter(o['firms']))
        cap = o['firms'][first]['capacity']
        cash0 = o['cash']
        recs = self.play(s, {oid: act({'command': 'register', 'product': sim.PRODUCTS[start]}, {first: cap})})
        row = self.owner_row(recs, oid)
        self.assertEqual(row['admin_result'], 'accepted')
        self.assertEqual(row['fee'], s['cfg']['registration_fee'])
        new = row['registered_firm']
        self.assertEqual(o['firms'][new]['status'], 'pending')            # usable from the next round
        sim.begin_round(s)
        self.assertEqual(o['firms'][new]['status'], 'active')
        self.assertEqual(o['firms'][new]['capacity'], 0)
        half = cap // 2
        recs = self.play(s, {oid: act({'command': 'transfer', 'from': first, 'to': new, 'amount': half},
                                      {first: cap - half})})
        row = self.owner_row(recs, oid)
        self.assertEqual(row['admin_result'], 'accepted')
        self.assertEqual(sum(t['amount'] for t in o['transit']), half)    # in transit, idle this round
        self.assertEqual(row['overhead'], 2 * s['cfg']['overhead'])        # the empty active firm pays overhead
        recs = self.play(s, {oid: act(production={first: cap - half, new: half})})
        self.assertEqual(o['firms'][new]['capacity'], half)
        self.assertEqual(self.owner_row(recs, oid)['producing_firms'][start], 2)
        self.assertLess(o['cash'], cash0 + 10 ** 9)

    def test_production_beyond_capacity_left_after_transfer_is_void(self):
        s = world()
        oid = 'own-01a'
        o = s['owners'][oid]
        g = s['markets'][1]['start_product']
        first = next(iter(o['firms']))
        self.play(s, {oid: act({'command': 'register', 'product': sim.PRODUCTS[g]}, full_production(s, oid))})
        new = [f for f in o['firms'] if f != first][0]
        cap = o['firms'][first]['capacity']
        recs = self.play(s, {oid: act({'command': 'transfer', 'from': first, 'to': new, 'amount': 12}, {first: cap})})
        row = self.owner_row(recs, oid)
        self.assertEqual(row['status'], 'void')
        self.assertEqual(o['firms'][first]['capacity'], cap)               # a void round moves nothing

    def test_cross_product_transfer_is_rejected_and_production_stands(self):
        s = world()
        oid = 'own-02b'
        o = s['owners'][oid]
        g = s['markets'][2]['start_product']
        first = next(iter(o['firms']))
        self.assertGreater(o['reserve'][1 - g], 0)
        recs = self.play(s, {oid: act({'command': 'transfer', 'from': 'reserve', 'to': first, 'amount': 12},
                                      full_production(s, oid))})
        row = self.owner_row(recs, oid)
        self.assertEqual(row['status'], 'accepted')
        self.assertTrue(row['admin_result'].startswith('rejected'))
        self.assertGreater(row['q'][g], 0)

    def test_retire_only_empty_firm(self):
        s = world()
        oid = 'own-03c'
        o = s['owners'][oid]
        g = s['markets'][3]['start_product']
        first = next(iter(o['firms']))
        recs = self.play(s, {oid: act({'command': 'retire', 'firm': first}, full_production(s, oid))})
        self.assertTrue(self.owner_row(recs, oid)['admin_result'].startswith('rejected'))
        self.play(s, {oid: act({'command': 'register', 'product': sim.PRODUCTS[g]}, full_production(s, oid))})
        new = [f for f in o['firms'] if f != first][0]
        sim.begin_round(s)
        recs = self.play(s, {oid: act({'command': 'retire', 'firm': new}, full_production(s, oid))})
        self.assertEqual(self.owner_row(recs, oid)['admin_result'], 'accepted')
        self.assertNotIn(new, o['firms'])

    def test_checkpoint_restore_is_exact_and_deterministic(self):
        s = world()
        for _ in range(2):
            self.play(s, {})
        saved = sim.dumps(s)
        a, b = json.loads(saved), json.loads(saved)
        self.assertEqual(sim.state_hash(a), sim.state_hash(s))
        ra = self.play(a, {}, study.branch_rules('A'))
        rb = self.play(b, {}, study.branch_rules('A2'))
        self.assertEqual(json.loads(json.dumps(ra)), json.loads(json.dumps(rb)))

    def test_owner_rule_charges_owner_concentration(self):
        s = world()
        recs = self.play(s, {}, study.branch_rules('C'))
        for r in recs:
            for x in r['owners'].values():
                for g in range(2):
                    self.assertAlmostEqual(x['charge'][g], sim.charge(r['owner_hhi'][g], x['profit'][g], s['cfg']))

    def test_development_witnesses(self):
        w = study.witnesses()
        self.assertTrue(w['passed'], w['rows'])

    def test_actor_text_has_no_study_words_or_evaluator_fields(self):
        texts = ' '.join(study.SYSTEMS[k] for k in ('messages', 'plain')).lower()
        for word in study.FORBIDDEN_IN_ACTOR_TEXT:
            self.assertNotIn(word, texts)
        flat = json.dumps(sim.observation(world(), 'own-00a', study.branch_rules('B')))
        for key in study.EVALUATOR_FIELDS:
            self.assertNotIn(f'"{key}"', flat)


class FrozenDesign(unittest.TestCase):
    def test_reviewer_limits_fixed_before_any_call(self):
        d = study.design()
        self.assertEqual(d['qualification']['context_min_valid_actions'], 171)
        self.assertEqual(d['material'], {'round_void_limit': 36, 'warmup_void_limit': 36, 'branch_void_limit': 180})
        self.assertEqual(d['budget']['hub_poll_seconds'], 3)
        self.assertEqual(d['cfg']['threshold'], 0.38)
        self.assertEqual(d['cfg']['fine_rate'], 0.35)

    def test_call_caps(self):
        b = study.design()['budget']
        caps = {s: b['max_calls'][s] for s in study.STAGES}
        self.assertEqual(caps, {'S0': 0, 'P0': 1, 'Q0': 185, 'X0': 180, 'S1': 7560, 'D1': 192})
        self.assertEqual(caps['S1'] + caps['D1'], 7752)                    # 180 x (2 + 4 x 10) + 192
        self.assertLessEqual(caps['P0'] + caps['Q0'] + caps['X0'], 552)
        self.assertEqual(b['max_attempted_calls'], sum(caps.values()) + b['max_calls']['REISSUE'])
        self.assertEqual(b['aggregate_usd'], 5)

    def test_noise_floor_runs_last_with_rules_of_A(self):
        self.assertEqual(study.branch_order()[:3], ['C', 'B', 'A'])
        self.assertEqual(study.branch_order()[-1], 'A2')
        self.assertEqual(study.branch_rules('A2'), study.branch_rules('A'))
        self.assertEqual(coordinator.PREREQUISITE['D1'], 'S1')             # the diagnostic comes after the economy


def calls_for(n_per_slot=4):
    s = world()
    sim.begin_round(s)
    out = []
    for oid, o in s['owners'].items():
        slot = study.slot_of(o['market'], o['role'])
        if sum(c['slot'] == slot for c in out) < n_per_slot:
            out.append({'unit': f'A.r03.{oid}', 'slot': slot, 'system': 'messages',
                        'user': study.user_text(sim.observation(s, oid, study.branch_rules('A')))})
    return out


class Dispatch(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.env = patch.dict(os.environ, {provider.KEY_ENV: 'test-not-a-key'})
        self.env.start()
        self.config = study.provider_config()

    def tearDown(self):
        self.env.stop()
        self.tmp.cleanup()

    def dispatcher(self, lose=(), budget=None):
        config = copy.deepcopy(self.config)
        if budget:
            config['budget'].update(budget)
        clock = rehearse.JumpClock()
        self.stub = rehearse.Stub('mixed')
        self.ledger = transport.FastLedger(Path(self.tmp.name) / 'ledger.jsonl', config['budget'])
        return transport.LocalDispatcher(self.ledger, config, 3, self.stub, clock.now, clock.sleep, lose=lose)

    def test_all_answered(self):
        d = self.dispatcher()
        rows = d.dispatch('s1-001', calls_for(), 2)
        self.assertTrue(all(r['ok'] for r in rows.values()))
        self.assertEqual(d.transport['lost_tasks'], 0)
        self.assertEqual(self.ledger.transact()['calls_by_stage'], {'S1': 12})

    def test_lost_task_reissued_once_to_survivors_then_rerouted(self):
        d = self.dispatcher(lose={(1, 1)})
        rows = d.dispatch('s1-001', calls_for(), 2)
        self.assertTrue(all(r['ok'] for r in rows.values()))
        self.assertEqual(d.transport['lost_tasks'], 1)
        self.assertEqual(d.transport['reissued_calls'], 4)
        self.assertEqual(d.dead, {1})
        self.assertTrue(all(r['transport']['served_slot'] in (0, 2) for r in rows.values()))
        self.assertEqual(sum(r['transport']['reissued'] for r in rows.values()), 4)
        totals = self.ledger.transact()
        self.assertEqual(totals['calls_by_stage'], {'S1': 12, 'REISSUE': 4})
        self.assertEqual(self.stub.calls, 16)                       # the lost task's sends did happen locally
        rows = d.dispatch('s1-001', [dict(c, unit=c['unit'].replace('r03', 'r04')) for c in calls_for()], 2)
        self.assertTrue(all(r['ok'] and r['transport']['served_slot'] != 1 for r in rows.values()))
        self.assertEqual(d.transport['rerouted_calls'], 8)

    def test_second_miss_is_lost(self):
        d = self.dispatcher(lose={(1, 1), (0, 2), (2, 2)})
        rows = d.dispatch('s1-001', calls_for(), 2)
        lost = [u for u, r in rows.items() if not r['ok']]
        self.assertEqual(len(lost), 4)
        self.assertTrue(all(rows[u]['category'] == transport.LOST for u in lost))
        self.assertEqual(d.transport['lost_calls_after_reissue'], 4)

    def test_reissue_refused_by_cap_leaves_calls_lost(self):
        b = copy.deepcopy(self.config['budget'])
        b['max_calls']['REISSUE'] = 0
        d = self.dispatcher(lose={(1, 1)}, budget={'max_calls': b['max_calls']})
        rows = d.dispatch('s1-001', calls_for(), 2)
        self.assertEqual(d.transport['reissue_refused'], 'stage_call_cap_reached')
        self.assertEqual(sum(not r['ok'] for r in rows.values()), 4)

    def test_no_live_worker_stops(self):
        d = self.dispatcher()
        d.dead = {0, 1, 2}
        with self.assertRaises(transport.StageStop) as cm:
            d.dispatch('s1-001', calls_for(), 2)
        self.assertEqual(cm.exception.reason, 'no_live_worker')

    def test_worker_never_sends_a_call_id_twice_and_not_after_expiry(self):
        d = self.dispatcher()
        calls = calls_for(1)[:1]
        micro, _ = transport.reservation(self.config, study.SYSTEMS['messages'], calls[0]['user'])
        item = {'call_id': 's1-001:' + calls[0]['unit'], 'system': 'messages', 'user': calls[0]['user'], 'micro_usd': micro}
        task = {'fence': 'f#1', 'seq': 1, 'in_flight': 1, 'systems': {'messages': study.SYSTEMS['messages']}, 'calls': [item],
                'expires': 10 ** 12}
        sent = set()
        first = transport.run_task(task, d.apis[0], sent)
        again = transport.run_task(dict(task, fence='f#2', seq=2), d.apis[0], sent)
        self.assertTrue(first['results'][0]['ok'])
        self.assertEqual(again['results'][0]['category'], transport.AMBIGUOUS)
        late = transport.run_task(dict(task, fence='f#3', seq=3, expires=0), d.apis[0], set())
        self.assertEqual(late['results'][0]['category'], transport.EXPIRED)
        self.assertEqual(self.stub.calls, 1)


class FakeClock:
    def __init__(self):
        self.t, self.sleeps = 0.0, []

    def now(self):
        return self.t

    def sleep(self, s):
        self.sleeps.append(s)
        self.t += s


class FakeHub:
    """Results never appear; the worker session is running but its hub record stops changing."""
    def __init__(self, fail_downloads=0):
        self.fail_downloads = fail_downloads

    def upload(self, run, path, name):
        return {'run': run, 'name': name}

    def download(self, url, dest):
        if self.fail_downloads:
            self.fail_downloads -= 1
            raise urllib.error.URLError('down')
        raise RuntimeError(f'GET {url}: 404')

    def get_run(self, run):
        return {'status': 'running', 'updated': 1.0}


class Polling(unittest.TestCase):
    def test_poller_backoff(self):
        c = FakeClock()
        p = transport.Poller(3, 30, c.sleep)
        for trouble in (True, True, True, True, True, False):
            p.wait(trouble)
        self.assertEqual(c.sleeps, [6, 12, 24, 30, 30, 3])

    def test_fetch_tells_missing_from_hub_trouble(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertIsNone(transport._fetch(FakeHub(), 'r', 'x', Path(tmp) / 'x'))
            with self.assertRaises(transport.HubTrouble):
                transport._fetch(FakeHub(fail_downloads=1), 'r', 'x', Path(tmp) / 'x')

    def test_silent_worker_given_up_after_silence_not_task_timeout(self):
        with tempfile.TemporaryDirectory() as tmp:
            c = FakeClock()
            config = study.provider_config()
            led = transport.FastLedger(Path(tmp) / 'l.jsonl', config['budget'])
            d = transport.HubDispatcher(FakeHub(fail_downloads=2), led, config, 3, Path(tmp) / 'w', 't', sleep=c.sleep, clock=c.now)
            d.heard = [(1.0, 0.0)] * 3
            task = {'seq': 1, 'fence': 'x#1', 'calls': []}
            got = d._exchange({0: task}, config['budget']['task_timeout_seconds'])
            self.assertEqual(got, {})
            self.assertLess(c.t, 240 + 2 * 30 + 30)
            self.assertGreaterEqual(c.t, 240)
            self.assertEqual(min(c.sleeps), 3)
            self.assertIn(6, c.sleeps)                                   # back-off after the hub error
            self.assertEqual(d.transport['events'][-1]['event'], 'worker_silent')


class Normalisation(unittest.TestCase):
    """Attempt 002's interface repair: harmless variants of a correct response are normalised and counted."""

    def setUp(self):
        self.s = world()
        sim.begin_round(self.s)
        self.oid = 'own-00a'
        self.o = self.s['owners'][self.oid]
        self.first = next(iter(self.o['firms']))
        self.cap = self.o['firms'][self.first]['capacity']
        self.other = sim.PRODUCTS[1 - self.s['markets'][0]['start_product']]
        self.rival_firm = next(iter(self.s['owners']['own-00b']['firms']))

    def resolve(self, resp):
        return sim.resolve(self.s, self.oid, resp)

    def test_p0_case_of_attempt_001_is_accepted(self):
        # The exact P0 answer of attempt 001: correct registration plus a zero order for an invented id.
        resp = {'memo': 'Round 1: Register B firm.', 'admin': {'command': 'register', 'product': self.other},
                'production': {self.first: self.cap, 'firm-00-02': 0}, 'message': ''}
        self.assertEqual(self.rival_firm, 'firm-00-02')                     # the invented id is a rival's firm
        r = self.resolve(resp)
        self.assertEqual((r['status'], r['admin_result']), ('accepted', 'accepted'))
        self.assertEqual(r['normalized'], ['zero_order_unknown_firm_dropped'])
        self.assertNotIn('firm-00-02', r['action']['production'])

    def test_nonzero_order_for_unknown_or_rival_firm_stays_void(self):
        for fid in ('firm-00-99', self.rival_firm):
            r = self.resolve(act(production={self.first: self.cap, fid: 12}))
            self.assertEqual((r['status'], r['reason']), ('void', 'production_unknown_firm'))

    def test_zero_order_for_rival_firm_dropped(self):
        r = self.resolve(act(production={self.first: self.cap, self.rival_firm: 0}))
        self.assertEqual(r['status'], 'accepted')
        self.assertEqual(r['normalized'], ['zero_order_unknown_firm_dropped'])

    def test_harmless_variants_accepted_and_counted(self):
        cases = [
            ({'memo': '', 'admin': {'command': 'noop'}, 'production': {self.first: 576.0 if self.cap == 576 else float(self.cap)},
              'message': None}, []),
            ({'memo': '', 'admin': {'command': 'no-op'}, 'production': {self.first: self.cap}, 'message': ''}, ['command_spelling']),
            ({'memo': '', 'admin': {'command': 'NOOP'}, 'production': {self.first: self.cap}, 'message': ''}, ['command_spelling']),
            ({'memo': '', 'production': {self.first: self.cap}, 'message': ''}, ['admin_omitted_as_noop']),
            ({'memo': '', 'admin': {'command': 'noop', 'product': 'A'}, 'production': {self.first: self.cap}}, ['noop_extra_field_dropped']),
            ({'admin': {'command': 'register', 'product': self.other.lower()}, 'production': {self.first: self.cap}}, ['product_case']),
            ({'admin': {'command': 'Register', 'product': self.other, 'amount': None}, 'production': {self.first: self.cap}},
             ['command_spelling', 'null_admin_field_dropped']),
            ({'admin': {'command': 'noop'}, 'production': {self.first: self.cap}, 'reasoning': 'x', 'plan': 'y'},
             ['extra_top_level_key_dropped', 'extra_top_level_key_dropped']),
        ]
        for resp, expected in cases:
            r = self.resolve(resp)
            self.assertEqual(r['status'], 'accepted', resp)
            self.assertEqual(r['normalized'], expected, resp)
            self.assertTrue(set(expected) <= set(sim.NORMALISATIONS))

    def test_ambiguous_variants_still_void(self):
        for resp, reason in (({'admin': {'command': 'noop'}}, 'response_keys'),
                             ({'admin': {'command': 'skip'}, 'production': {}}, 'admin_shape'),
                             ({'admin': {'command': 'register', 'product': 'B', 'amount': 5}, 'production': {}}, 'admin_fields'),
                             ({'admin': {'command': 'noop'}, 'production': {self.first: 12.5}}, 'production_quantity'),
                             ({'admin': {'command': 'noop'}, 'production': {self.first: self.cap + 1}}, 'production_exceeds_available_capacity'),
                             ({'admin': {'command': 'noop'}, 'production': {self.first: self.cap}, 'message': 7}, 'message_type')):
            r = self.resolve(resp)
            self.assertEqual((r['status'], r['reason']), ('void', reason), resp)

    def test_pending_and_retired_firms_with_zero(self):
        s, oid, o, first = self.s, self.oid, self.o, self.first
        recs = sim.step(s, {x: (act({'command': 'register', 'product': self.other}, {first: self.cap}) if x == oid
                                else act(production=full_production(s, x))) for x in s['owners']}, {'regime': 'none'})
        new = [f for f in o["firms"] if f != first][0]
        self.assertEqual(o['firms'][new]['status'], 'pending')
        sim.begin_round(s)
        r = sim.resolve(s, oid, act({'command': 'retire', 'firm': new}, {first: self.cap, new: 0}))
        self.assertEqual((r['status'], r['admin_result']), ('accepted', 'accepted'))
        sim.step(s, {x: (act({'command': 'retire', 'firm': new}, {first: self.cap, new: 0}) if x == oid
                         else act(production=full_production(s, x))) for x in s['owners']}, {'regime': 'none'})
        self.assertNotIn(new, o['firms'])
        sim.begin_round(s)
        r = sim.resolve(s, oid, act(production={first: self.cap, new: 0}))           # retired firm, zero order
        self.assertEqual((r['status'], r['normalized']), ('accepted', ['zero_order_unknown_firm_dropped']))
        recs = sim.step(s, {x: (act(production={first: self.cap, new: 0}) if x == oid else act(production=full_production(s, x)))
                            for x in s['owners']}, {'regime': 'none'})
        row = next(r['owners'][oid] for r in recs if oid in r['owners'])
        self.assertEqual(row['dropped_zero_orders'], 1)
        self.assertEqual(sim.conservation(s), [])

    def test_documentation_half(self):
        for k in ('messages', 'plain', 'cued'):
            self.assertIn('Production orders may name only the firms listed in `portfolio.firms` this round', study.SYSTEMS[k])
            self.assertIn('never chosen by you', study.SYSTEMS[k])
        obs = sim.observation(world(), 'own-00a', study.branch_rules('A'))
        self.assertIn('cannot be ordered', obs['portfolio']['production_orders_rule'])

    def test_fresh_fixtures_and_batches(self):
        d = study.design()
        f = d['fixtures']
        used_001 = set(range(318400, 318418)) | set(range(318200, 318206)) | set(range(318100, 318106))
        fresh = set(range(f['probe_first_market_id'], f['probe_first_market_id'] + 18)) | set(f['ordinary_markets']) | set(f['smoke_markets'])
        self.assertFalse(used_001 & fresh)
        self.assertTrue(all(318600 <= m <= 318699 for m in fresh))
        self.assertEqual(len(fresh), 30)
        self.assertEqual(d['attempt'], '002')
        self.assertTrue(all(study.params(s)['batch'].endswith('-002') for s in study.STAGES))
        b = study.ledger_budget()
        self.assertEqual((b['max_calls']['P0'], b['max_attempted_calls']), (2, 8479))


class ModelLadder(unittest.TestCase):
    """Attempt 002: the model is a launch parameter from a declared set of two; each model is its own chain."""

    def test_default_is_the_programs_model(self):
        with patch.dict(os.environ, {study.MODEL_ENV: ''}):
            self.assertEqual(study.model_name(), 'qwen/qwen3.7-flash')
            self.assertEqual(study.params('P0')['batch'], 'p0-002')
            self.assertEqual(study.session_experiment(), study.EXPERIMENT)
            self.assertEqual(study.ledger_budget()['aggregate_usd'], 5)
            self.assertEqual(study.provider_config()['model'], 'qwen/qwen3.7-flash')

    def test_second_model_has_own_names_cap_and_adapter(self):
        with patch.dict(os.environ, {study.MODEL_ENV: 'gpt-6-sol'}):
            p = study.params('S1')
            self.assertEqual((p['batch'], p['model']), ('s1-002-gpt-6-sol', 'gpt-6-sol'))
            self.assertEqual(provider.stage_of(p['batch'] + ':x'), 'S1')
            self.assertEqual(study.session_experiment(), study.EXPERIMENT + '-gpt-6-sol')
            b = study.ledger_budget()
            self.assertEqual((b['aggregate_usd'], b['max_calls']['P0'], b['max_attempted_calls']), (150, 1, 8478))
            self.assertEqual((b['in_flight_per_host'], b['in_flight_per_host_max'], b['max_output_tokens']), (3, 3, 2000))
            config = study.provider_config()
            self.assertIs(study.adapter(config), openai_provider)
            openai_provider.check_config(config)                                  # template keys, effort, prices row
            self.assertEqual(config['request_template']['reasoning_effort'], 'low')
            self.assertEqual(config['budget']['prices'], openai_provider.PRICES['gpt-6-sol'])
            self.assertEqual(config['budget']['retry']['retryable_http_status'], [429, 500, 502, 503, 504])
            for k in ('messages', 'plain', 'cued'):
                self.assertIn('json', study.SYSTEMS[k].lower())                    # JSON mode needs the word
                self.assertIn('capacity transferred into a firm (from your reserve or another firm) can be ordered only from the next round',
                              study.SYSTEMS[k])
            f = study.design()['fixtures']
            mine = set(range(f['probe_first_market_id'], f['probe_first_market_id'] + 18)) | set(f['ordinary_markets']) | set(f['smoke_markets'])
            used = (set(range(318600, 318618)) | set(range(318620, 318626)) | set(range(318630, 318636))
                    | set(range(318400, 318418)) | set(range(318200, 318206)) | set(range(318100, 318106)))
            self.assertEqual(len(mine), 30)
            self.assertFalse(mine & used)
            self.assertTrue(all(318640 <= m <= 318699 for m in mine))
            self.assertTrue(study.witnesses()['passed'])
        with patch.dict(os.environ, {study.MODEL_ENV: 'gpt-6-luna'}):
            with self.assertRaises(ValueError):
                study.model_name()

    def test_openai_reservation_equals_adapter_permit_and_cap_arithmetic(self):
        with patch.dict(os.environ, {study.MODEL_ENV: 'gpt-6-sol', openai_provider.KEY_ENV: 'test-not-a-key'}), \
                tempfile.TemporaryDirectory() as tmp:
            config = study.provider_config()
            clock = rehearse.JumpClock()
            stub = rehearse.Stub('mixed', api='openai')
            led = transport.FastLedger(Path(tmp) / 'l.jsonl', config['budget'])
            d = transport.LocalDispatcher(led, config, 3, stub, clock.now, clock.sleep, lose={(1, 1)})
            rows = d.dispatch('s1-002-gpt-6-sol', calls_for(), 3)
            self.assertTrue(all(r['ok'] for r in rows.values()), {u: r['category'] for u, r in rows.items()})
            self.assertEqual(d.transport['reissued_calls'], 4)
            self.assertTrue(all(r['accounting']['cost_source'] == 'computed_from_pinned_prices' for r in rows.values()))
            # Worst case per call at the largest request (X0, about 10.5 KB): bytes x 2.50 + 2,000 x 10.00 per million.
            micro, n = transport.reservation(config, study.SYSTEMS['messages'], 'x' * 7000)
            self.assertLess(micro, 50_000)                                        # under USD 0.05 per call
            self.assertGreater(micro, 20_000)


    def test_gates_never_pool_models(self):
        with patch.dict(os.environ, {study.MODEL_ENV: ''}):
            q = study.params('S0')
        other = dict(q, model='gpt-6-luna', batch='s0-002-gpt-6-luna')
        mine = {'params': q, 'status': 'done', 'metrics': {'qualification_passed': 1, 'invalid': 0}}
        theirs = {'params': other, 'status': 'done', 'metrics': {'qualification_passed': 1, 'invalid': 0}}
        with patch.dict(os.environ, {study.MODEL_ENV: ''}):
            coordinator.gate([mine, theirs], 'P0', study.params('P0'))          # one S0 of this model, not two
            with self.assertRaises(ValueError):
                coordinator.gate([theirs], 'P0', study.params('P0'))


class Gates(unittest.TestCase):
    def run_of(self, stage, status='done', **metrics):
        p = study.params(stage)
        return {'params': dict(p, batch=p['batch']), 'status': status, 'metrics': metrics}

    def test_main_stage_needs_passed_x0(self):
        p = study.params('S1')
        failed_x0 = self.run_of('X0', 'failed', qualification_passed=0, invalid=60)
        with self.assertRaises(ValueError):
            coordinator.gate([failed_x0], 'S1', p)
        coordinator.gate([self.run_of('X0', qualification_passed=1, invalid=0)], 'S1', p)

    def test_diagnostic_after_admissible_economy_only(self):
        p = study.params('D1')
        with self.assertRaises(ValueError):
            coordinator.gate([self.run_of('S1', 'failed', diagnostic_admissible=0)], 'D1', p)
        coordinator.gate([self.run_of('S1', 'failed', diagnostic_admissible=1)], 'D1', p)

    def test_no_replay(self):
        p = study.params('Q0')
        with self.assertRaises(ValueError):
            coordinator.gate([self.run_of('Q0')], 'Q0', p)


class ScriptedStage(unittest.TestCase):
    def test_s0_passes(self):
        with tempfile.TemporaryDirectory() as tmp:
            summary = worker.execute(study.params('S0'), Path(tmp) / 's0')
            self.assertTrue(summary['gate']['passed'], summary['detail']['invariants'])
            self.assertEqual(summary['model_calls'], 0)
            self.assertEqual(summary['planned'], 8118)


class Hygiene(unittest.TestCase):
    def test_no_secret_or_address_in_package(self):
        for path in sorted(study.ROOT.rglob('*')):
            if path.is_file() and path.suffix in ('.py', '.md', '.yaml', '.json', '.txt') and 'results' not in path.parts:
                text = path.read_text()
                self.assertIsNone(re.search(r'sk-(or|ant)-(?!test-)[A-Za-z0-9]', text), path)
                for address in re.findall(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', text):
                    self.assertEqual(address, '127.0.0.1', path)


if __name__ == '__main__':
    unittest.main()
