"""Offline adapter boundary regressions; fixtures are not scientific observations."""
from contextlib import closing, contextmanager
import importlib.util
import json
import os
from pathlib import Path
import shutil
import sqlite3
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from experiment_ops import theseus as adapter

ENTRY = {'id': 'swarm-of-theseus-v2', 'study_path': adapter.STUDY, 'adapter': 'theseus-v2'}


class TheseusAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name).resolve()
        self.study = self.root / adapter.STUDY
        self.study.mkdir(parents=True)
        shutil.copytree(ROOT / adapter.STUDY / 'src', self.study / 'src', ignore=shutil.ignore_patterns('__pycache__'))
        shutil.copyfile(ROOT / adapter.STUDY / 'PLAN.md', self.study / 'PLAN.md')
        (self.root / '.gitignore').write_text('__pycache__/\ndata/\n')
        for args in (['init', '-q'], ['add', '.'], ['-c', 'user.name=Offline Fixture', '-c', 'user.email=fixture@example.invalid', 'commit', '-qm', 'offline fixture']):
            subprocess.run(['git', *args], cwd=self.root, check=True, capture_output=True)
        self.data = self.root / 'data' / 'experiment-operations'
        self.data.mkdir(parents=True)
        self.config = self.data / 'config.json'
        head = adapter._head(self.root)
        cfg = {'model': 'claude-haiku-4-5-20251001', 'input_rate': 1, 'output_rate': 5,
               'max_output_tokens': 900, 'max_input_bytes': 18000, 'pricing_verified_epoch': time.time(),
               'source_commit': head, 'plan_url': 'https://github.com/dmarzzz/swarm-dynamics-lab/blob/' + head + '/' + adapter.STUDY + '/PLAN.md',
               'plan_sha256': adapter._hash(self.study / 'PLAN.md'),
               'pre_run_review_url': 'https://github.com/dmarzzz/swarm-dynamics-lab/blob/' + head + '/' + adapter.STUDY + '/reviews/S0-pre.md',
               'pre_run_review_sha256': 'a' * 64}
        self.config.write_text(json.dumps(cfg))

    def prepared(self):
        return adapter.prepare(self.root, ENTRY, 'S0', self.config)

    def ledger(self, reserved=.3, calls=24, deadline=None, path=None):
        path = path or self.data / 'authoritative.sqlite'
        with closing(sqlite3.connect(path)) as db, db:
            db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)')
            db.execute('INSERT INTO budget VALUES(1,15,?,?)', (reserved, calls))
            db.execute('CREATE TABLE study_limit(id INTEGER PRIMARY KEY,deadline REAL)')
            db.execute('INSERT INTO study_limit VALUES(1,?)', (deadline or time.time() + 8000,))
            db.execute('CREATE TABLE attempts(stage TEXT PRIMARY KEY,output TEXT)')
        return path

    def receipt(self, ledger):
        now = time.time()
        value = {'experiment': 'swarm-of-theseus-v2', 'source_commit': adapter._head(self.root),
                 'exclusive_claim_verified': True, 'claim_id': 'unit', 'host': 'unit',
                 'verified_epoch': now, 'claim_until_epoch': now + 8000, 'reserved_usd': 15,
                 'max_calls': 660, 'authority_allocation_id': 'unit', 'owner_authorization_ref': 'unit',
                 'approved_account_verified': True,
                 'native_budget_ledger': str(ledger),
                 'minimum_prior_reserved_calls': 24, 'minimum_prior_reserved_usd': .3}
        path = self.data / 'receipt.json'
        path.write_text(json.dumps(value))
        return path, value

    def test_prepare_counts_and_operator_context_contract(self):
        with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            p = self.prepared()
        self.assertEqual(p['sample_size_summary']['worlds'], 6)
        self.assertEqual(p['sample_size_summary']['planned_calls'], 24)
        self.assertEqual(p['cost_envelope']['maximum_reserved_usd'], .552288)
        self.assertFalse(p['initialization_contract']['operator_context_injected'])
        self.assertEqual(p['initialization_contract']['status'], 'intended_not_observed')
        self.assertFalse(p['resume_supported'])
        self.assertEqual(adapter._verify_prepared(self.root, ENTRY, p)['model'], 'claude-haiku-4-5-20251001')

    def test_component_drift_and_source_drift_block(self):
        p = self.prepared()
        (self.study / 'src' / 'presentation.py').write_text('# changed renderer\n')
        with self.assertRaisesRegex(adapter.AdapterError, 'prepared_input_drift'):
            adapter._verify_prepared(self.root, ENTRY, p)
        p['source_commit'] = '0' * 40
        with self.assertRaisesRegex(adapter.AdapterError, 'prepared_source_or_stage_drift'):
            adapter._verify_prepared(self.root, ENTRY, p)

    def test_unknown_config_and_tampered_assignment_block(self):
        p = self.prepared()
        p['assignments'][0]['seed'] = 999
        with self.assertRaisesRegex(adapter.AdapterError, 'prepared_packet_drift'):
            adapter._verify_prepared(self.root, ENTRY, p)
        c = json.loads(self.config.read_text()); c['operator_memory'] = 'must not become experimental context'
        self.config.write_text(json.dumps(c))
        with self.assertRaisesRegex(adapter.AdapterError, 'config_fields_not_allowlisted'):
            self.prepared()

    def test_missing_qualification_blocks_scientific_stage(self):
        with self.assertRaisesRegex(adapter.AdapterError, 'qualification_required'):
            adapter.prepare(self.root, ENTRY, 'S1', self.config)

    def test_existing_ledger_binding_continuity_and_consumed_stage(self):
        ledger = self.ledger(); _, receipt = self.receipt(ledger)
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            self.assertEqual(adapter._ledger(self.root, receipt, 'S0-repair')['reserved_calls'], 24)
            receipt['minimum_prior_reserved_calls'] = 25
            with self.assertRaisesRegex(adapter.AdapterError, 'native_budget_history_missing'):
                adapter._ledger(self.root, receipt, 'S0-repair')
            receipt['minimum_prior_reserved_calls'] = 24
            with closing(sqlite3.connect(ledger)) as db, db:
                db.execute("INSERT INTO attempts VALUES('S0','retained')")
            with self.assertRaisesRegex(adapter.AdapterError, 'native_stage_already_attempted'):
                adapter._ledger(self.root, receipt, 'S0')
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(self.data / 'missing.sqlite')}):
            with self.assertRaisesRegex(adapter.AdapterError, 'existing_native_budget_ledger_required'):
                adapter._ledger(self.root, receipt, 'S0')
        self.assertFalse((self.data / 'missing.sqlite').exists())

    def test_expired_or_nonfinite_ledger_blocks(self):
        ledger = self.ledger(deadline=time.time() - 10); _, receipt = self.receipt(ledger)
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            with self.assertRaisesRegex(adapter.AdapterError, 'native_study_deadline_expired'):
                adapter._ledger(self.root, receipt, 'S0')
            with closing(sqlite3.connect(ledger)) as db, db:
                db.execute('UPDATE study_limit SET deadline=?', (time.time() + 8000,))
                db.execute('UPDATE budget SET reserved=?', (float('inf'),))
            with self.assertRaisesRegex(adapter.AdapterError, 'native_budget_ledger_mismatch'):
                adapter._ledger(self.root, receipt, 'S0')

    def test_native_unknown_response_keeps_reservation(self):
        ledger = self.ledger()
        cfg = json.loads(self.config.read_text())
        _, receipt = self.receipt(ledger)
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger), 'SWARM_MODEL_API_KEY': 'offline-test-fixture'}):
            with adapter._native(self.root, ENTRY, 'provider') as provider:
                connections = []; real_connect = sqlite3.connect
                def connect(*args, **kwargs):
                    db = real_connect(*args, **kwargs); connections.append(db); return db
                try:
                    with patch.object(provider.sqlite3, 'connect', side_effect=connect):
                        policy = provider.AnthropicPolicy(cfg, receipt, self.data / 'calls')
                        with patch('urllib.request.urlopen', side_effect=TimeoutError):
                            result = policy.complete({'instructions': 'Offline fixture only', 'observation': {'step': 0, 'commands': {'hold': 'hold'}, 'cases': []}})
                finally:
                    for connection in connections: connection.close()
        self.assertIsNone(result['usage'])
        with closing(sqlite3.connect(ledger)) as db, db:
            held, calls = db.execute('SELECT reserved,calls FROM budget').fetchone()
        self.assertGreater(held, .3)
        self.assertEqual(calls, 25)
        (self.data / 'manifest.json').write_text(json.dumps({'stage': 'S0', 'assignments': []}))
        observed = adapter._observed_contexts(self.data)
        self.assertEqual(len(observed['calls']), 1)
        self.assertNotIn('Offline fixture only', json.dumps(observed))
        self.assertEqual(observed['status'], 'observed_native_predispatch_journal')

    def test_report_is_offline_nonmutating_and_allowlisted(self):
        p = self.prepared(); source = self.data / 'saved'; source.mkdir()
        (source / 'events').mkdir()
        (source / 'manifest.json').write_text(json.dumps({'stage': 'S0', 'assignments': p['assignments'], 'config': {'private': 'must-not-export'}}))
        (source / 'summary.json').write_text('historical summary unchanged')
        with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
            status = adapter.report(self.root, ENTRY, source, self.data / 'report')
        self.assertEqual(status['model_calls'], 0)
        self.assertEqual((source / 'summary.json').read_text(), 'historical summary unchanged')
        report = (self.data / 'report' / 'summary.json').read_text()
        self.assertNotIn('must-not-export', report)
        self.assertFalse(json.loads(report)['qualification_passed'])
        self.assertEqual((self.data / 'report' / 'summary.json').stat().st_mode & 0o777, 0o600)

    def test_native_stale_claim_still_blocks_before_provider(self):
        p = self.prepared(); ledger = self.ledger(); path, receipt = self.receipt(ledger)
        receipt['verified_epoch'] = time.time() - 901; path.write_text(json.dumps(receipt))
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')) as transport:
                result = adapter.run(self.root, ENTRY, p, path, self.data / 'blocked-output')
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['reason'], 'stale_deployment_verification')
        transport.assert_not_called()
        self.assertFalse((self.data / 'blocked-output').exists())

    def test_existing_ledger_outside_checkout_is_used_in_place(self):
        with tempfile.TemporaryDirectory() as td:
            ledger = self.ledger(path=Path(td).resolve() / 'authority.sqlite')
            _, receipt = self.receipt(ledger)
            with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
                result = adapter._ledger(self.root, receipt, 'S0-repair')
            self.assertEqual(result['reserved_calls'], 24)
            self.assertFalse((self.data / 'authoritative.sqlite').exists())

    def test_nonfinite_claim_expiry_blocks(self):
        p = self.prepared(); ledger = self.ledger(); path, receipt = self.receipt(ledger)
        for value in (float('nan'), float('inf'), True):
            receipt['claim_until_epoch'] = value; path.write_text(json.dumps(receipt))
            with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
                with self.assertRaisesRegex(adapter.AdapterError, 'receipt_numeric_field_invalid'):
                    adapter.run(self.root, ENTRY, p, path, self.data / 'not-started')

    def test_nested_evidence_symlink_is_never_read(self):
        p = self.prepared(); source = self.data / 'saved'; source.mkdir()
        (source / 'manifest.json').write_text(json.dumps({'stage': 'S0', 'assignments': p['assignments']}))
        with tempfile.TemporaryDirectory() as td:
            external = Path(td); (external / 'private.json').write_text('{}')
            (source / 'events').symlink_to(external, target_is_directory=True)
            with self.assertRaisesRegex(adapter.AdapterError, 'symlink_evidence_refused'):
                adapter.report(self.root, ENTRY, source, self.data / 'report')
            with self.assertRaisesRegex(adapter.AdapterError, 'symlink_evidence_refused'):
                adapter._qualification_files(self.root, source)
        self.assertFalse((self.data / 'report').exists())

    def test_native_s1_gets_scratch_qualification_not_original(self):
        p = self.prepared(); p['stage'] = 'S1'
        source = self.data / 'qualification'; source.mkdir()
        (source / 'manifest.json').write_text(json.dumps({'stage': 'S0', 'assignments': p['assignments']}))
        (source / 'summary.json').write_text('immutable previous summary')
        p['qualification_path'] = str(source.relative_to(self.root))
        p['input_files'].update(adapter._qualification_files(self.root, source))
        ledger = self.ledger(); receipt, _ = self.receipt(ledger)
        test = self
        class NativeFixture:
            def run(self, config, receipt, stage, output, qualification):
                test.assertNotEqual(qualification, source)
                test.assertEqual(adapter._hash(qualification / 'manifest.json'), adapter._hash(source / 'manifest.json'))
                (qualification / 'summary.json').write_text('native recomputation')
                output.mkdir(); (output / 'manifest.json').write_text(json.dumps({'stage': stage, 'assignments': []}))
                return {}
        @contextmanager
        def native_fixture(*args, **kwargs):
            yield NativeFixture()
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            with patch.object(adapter, '_verify_prepared', return_value=json.loads(self.config.read_text())):
                with patch.object(adapter, '_native', native_fixture):
                    result = adapter.run(self.root, ENTRY, p, receipt, self.data / 'new-result')
        self.assertEqual(result['status'], 'completed')
        self.assertEqual((source / 'summary.json').read_text(), 'immutable previous summary')

    def test_waived_researcher_review_does_not_erase_historical_failure(self):
        p = self.prepared(); ledger = self.ledger(); path, receipt = self.receipt(ledger)
        self.assertNotIn('researcher_review_passed', receipt)
        receipt.update(researcher_review_passed=False, researcher_review_ref='retained-historical-review')
        receipt['verified_epoch'] = time.time() - 901
        path.write_text(json.dumps(receipt))
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')) as transport:
                result = adapter.run(self.root, ENTRY, p, path, self.data / 'blocked-history')
        self.assertEqual(result['status'], 'blocked')
        self.assertEqual(result['reason'], 'stale_deployment_verification')
        self.assertFalse(json.loads(path.read_text())['researcher_review_passed'])
        transport.assert_not_called()

    def test_private_attestation_fails_before_native_dispatch(self):
        p = self.prepared(); ledger = self.ledger(); path, receipt = self.receipt(ledger)
        receipt['approved_account_verified'] = False; path.write_text(json.dumps(receipt))
        with patch.dict(os.environ, {'THESEUS_V2_LEDGER': str(ledger)}):
            with patch('urllib.request.urlopen', side_effect=AssertionError('network forbidden')):
                with self.assertRaisesRegex(adapter.AdapterError, 'external_account_attestation_missing'):
                    adapter.run(self.root, ENTRY, p, path, self.data / 'new-output')
        self.assertFalse((self.data / 'new-output').exists())


if __name__ == '__main__':
    unittest.main()
