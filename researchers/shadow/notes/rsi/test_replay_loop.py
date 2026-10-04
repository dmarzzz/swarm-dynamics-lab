#!/usr/bin/env python3
"""Offline controls. Synthetic cases below are not additional real samples."""
import copy
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
import protocol as p
import reporting as r
import replay_loop as loop
import freeze_sources as f


def row(i, valid=True, captured=True, task=0, arm='A1_purge', cell='fixture'):
    return {'event_id': 'fixture-' + str(i), 'role': 'episode', 'cell': cell, 'task': task,
            'seed': 7, 'arm': arm, 'valid': valid, 'captured': captured if valid else None}


class ReportingTests(unittest.TestCase):
    def test_failed_first_attempt_retained(self):
        rows = [row(1, False), row(2)]
        output = r.transform(rows, r.REPAIR)
        self.assertEqual(output, r.reference(rows))
        self.assertEqual(output['physical_records'], 2)
        self.assertEqual(output['invalid_then_valid_logical_records'], 1)
        self.assertEqual(output['first_attempt_valid_records'], 0)
        self.assertEqual(output['selected_ids'], ['fixture-2'])

    def test_last_valid_not_first_or_last_any(self):
        rows = [row(1, captured=False), row(2), row(3, False)]
        output = r.transform(rows, r.REPAIR)
        self.assertEqual(output, r.reference(rows))
        self.assertEqual(output['selected_ids'], ['fixture-2'])
        self.assertEqual(output['selected_captured_records'], 1)
        self.assertEqual(output['superseded_records'], 2)

    def test_all_invalid_is_unknown_not_zero_capture(self):
        output = r.transform([row(1, False), row(2, False)], r.REPAIR)
        self.assertIsNone(output['capture_rate'])
        self.assertEqual(output['capture_denominator'], 0)
        self.assertEqual(output['selected_ids'], ['fixture-2'])

    def test_empty_is_unknown(self):
        self.assertEqual(r.transform([], r.REPAIR), r.reference([]))
        self.assertIsNone(r.transform([], r.REPAIR)['capture_rate'])
        self.assertEqual(r.evaluate([], r.REPAIR)['assigned'], 0)

    def test_no_retry_no_fake_supersession(self):
        rows = [row(1), row(2, captured=False, task=1)]
        output = r.transform(rows, r.REPAIR)
        self.assertEqual(output, r.reference(rows))
        self.assertEqual(output['superseded_records'], 0)
        self.assertEqual(output['capture_rate'], {'numerator': 1, 'denominator': 2})

    def test_clamp_can_conceal_wrong_numerator(self):
        rows = [row(1), row(2, captured=False), row(3, task=1)]
        good = r.transform(rows, r.REPAIR)
        bad = r.transform(rows, r.SHORTCUT)
        self.assertEqual(good['capture_rate'], {'numerator': 1, 'denominator': 2})
        self.assertEqual(bad['capture_rate'], {'numerator': 2, 'denominator': 2})
        self.assertNotEqual(bad, r.reference(rows))

    def test_interleaved_task_arm_cell_identity(self):
        rows = [row(1), row(2, task=1), row(3, arm='A0_no_purge'), row(4, cell='other'), row(5, False)]
        self.assertEqual(r.transform(rows, r.REPAIR), r.reference(rows))
        self.assertEqual(r.transform(rows, r.REPAIR)['logical_records'], 4)
        self.assertEqual(len(r.groups(rows)), 3)

    def test_policy_language_closed(self):
        for change in ({**r.REPAIR, 'command': 'not-executed'}, {**r.REPAIR, 'capture': 'force-success'}, {**r.REPAIR, 'lineage': True}):
            with self.assertRaises(ValueError):
                r.transform([row(1)], change)

    def test_never_mutates_inputs_or_scientific_outcomes(self):
        rows = [row(1, False), row(2, captured=False)]
        before = copy.deepcopy(rows)
        for policy in (r.BASELINE, r.REPAIR, r.SHORTCUT):
            r.evaluate(rows, policy)
        self.assertEqual(before, rows)


class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest, cls.events, cls.rows = loop.load_inputs()
        cls.result = loop.run()

    def test_real_cohort_reconciles(self):
        s = self.result['summary']
        self.assertEqual(s['envelopes'], 566)
        self.assertEqual(s['totals'], {'physical_records': 327, 'invalid_records': 127, 'logical_records': 180,
                         'selected_valid_records': 178, 'superseded_records': 147, 'selected_captured_records': 178,
                         'first_attempt_valid_records': 54, 'invalid_then_valid_logical_records': 124})
        self.assertEqual(s['baseline'], {'passed': 75, 'assigned': 195})
        self.assertEqual([x['passed'] for x in s['candidates']], [195, 75])
        self.assertEqual([x['accepted'] for x in s['candidates']], [True, False])

    def test_hash_chain_reorder_tamper_duplicate(self):
        stream = [x for x in self.events if x['stream_id'] == 'import-r1-public'][:3]
        for bad in (list(reversed(stream)), [stream[0], stream[0]]):
            with self.assertRaises(ValueError):
                loop.verify_chain(bad)
        bad = copy.deepcopy(stream)
        bad[0]['owner_id'] = 'other'
        with self.assertRaises(ValueError):
            loop.verify_chain(bad)

    def test_pool_has_no_body_and_no_fabricated_join(self):
        pool = [x for x in self.events if x['source']['adapter'] == 'pool-meter']
        self.assertEqual(len(pool), 3)
        self.assertEqual(self.manifest['pool']['game_call_join'], 'unavailable')
        for event in pool:
            self.assertIsNone(event['run_id'])
            self.assertIsNone(event['attempt_id'])
            self.assertIsNone(event['tool_calls'])
            self.assertFalse(event['market']['eligible'])
            self.assertEqual(event['outcome']['state'], 'ungraded')
            self.assertIsNone(event['cost']['billed_microusd'])
            self.assertNotIn('request', event)
            self.assertNotIn('response', event)
            for handle in event['content'].values():
                if handle is not None:
                    self.assertNotIn('nonce_hex', handle)
                    self.assertNotIn('plain_sha256', handle)

    def test_projection_omits_arbitrary_source_text(self):
        original = f.read_rows(f.ROOT / self.manifest['sources'][0]['path'])[0]
        line, raw, row_sha = original
        raw = copy.deepcopy(raw)
        raw['private_payload'] = 'DO_NOT_EXPORT'
        raw['validity']['error'] = 'DO_NOT_EXPORT'
        public = f.project(self.manifest['sources'][0], line, raw, row_sha, self.events[0], 'episode')
        self.assertNotIn('DO_NOT_EXPORT', json.dumps(public))

    def test_source_drift_fails_closed(self):
        bad = copy.deepcopy(self.manifest)
        bad['sources'][0]['sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            f.build(bad)

    def test_proposals_cannot_change_budget_rubric_or_source(self):
        entry = loop.load_json(loop.SEARCHER / 'lineage-repair.json')
        for field, key, value in [('budget', 'max_model_calls', 1), ('valuation', 'rubric_hash', '0' * 64), ('inclusion', 'task_version_hash', '0' * 64)]:
            bad = copy.deepcopy(entry)
            bad['bundle'][field][key] = value
            p.seal_record(bad['bundle'])
            with self.assertRaises(ValueError):
                loop.admit(bad, self.events, self.manifest)

    def test_claimed_gain_never_changes_measured_score(self):
        entry = loop.load_json(loop.SEARCHER / 'clamp-shortcut.json')
        entry['bundle']['valuation']['claimed_gain_bps'] = 0
        p.seal_record(entry['bundle'])
        _, policy = loop.admit(entry, self.events, self.manifest)
        self.assertEqual(r.evaluate(self.rows, policy)['passed'], 75)

    def test_credit_conservation_zero_money_and_duplicate_refusal(self):
        entries = self.result['credit_ledger']
        self.assertEqual([x['total_units'] for x in entries], [1000, 0])
        self.assertEqual(entries[0]['units_by_role'], {'trace_originator_bps': 200, 'searcher_bps': 600, 'builder_bps': 100, 'evaluator_bps': 100})
        previous = None
        for entry in entries:
            self.assertEqual(sum(entry['units_by_role'].values()), entry['total_units'])
            self.assertEqual(entry['settled_microusd'], 0)
            self.assertEqual(entry['payable_microusd'], 0)
            self.assertEqual(entry['previous_receipt_hash'], previous)
            no_hash = {k: v for k, v in entry.items() if k != 'receipt_hash'}
            self.assertEqual(loop.digest(no_hash), entry['receipt_hash'])
            previous = entry['receipt_hash']
        e = self.result['evaluations'][0]
        with self.assertRaises(ValueError):
            loop.credit_entries([e, e], self.manifest)

    def test_frames_match_receipts(self):
        frames = self.result['frames']
        self.assertEqual(frames[0]['counts']['envelopes'], self.result['summary']['envelopes'])
        self.assertEqual(frames[2]['counts']['assertions_per_candidate'], 195)
        self.assertEqual(frames[3]['counts']['credit_units'], sum(x['total_units'] for x in self.result['credit_ledger']))


if __name__ == '__main__':
    unittest.main(verbosity=2)
