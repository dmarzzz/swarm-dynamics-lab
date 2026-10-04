"""Synthetic ledgers only. Never opens a real experiment authority."""
import copy
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from common import digest
from diagnostic_renewal import RenewalError, apply_approved_window


class DiagnosticRenewalTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.path=Path(self.tmp.name)/'synthetic.sqlite'
        self.now=1700000100.0
        self.auth=dict(study='poietic-agents',stage='S0',owner_approved=True,reference='synthetic-only',
            api_cap_usd=1.5,infrastructure_cap_usd=.5,total_cumulative_cap_usd=2,
            physical_call_cap=288,deadline=1700000000.0)
        self.db=sqlite3.connect(self.path,isolation_level=None)
        self.db.executescript('''CREATE TABLE authority(id INTEGER PRIMARY KEY,hash TEXT,host TEXT,cap INTEGER,calls INTEGER,deadline REAL);
            CREATE TABLE charges(id TEXT PRIMARY KEY,request_hash TEXT,reserve INTEGER,settled INTEGER,status TEXT,created REAL);''')
        self.old=dict(hash=digest(self.auth),host='synthetic-host',cap=1500000000,calls=288,deadline=self.auth['deadline'])
        self.db.execute('INSERT INTO authority VALUES(1,?,?,?,?,?)',tuple(self.old.values()))
        self.db.execute('INSERT INTO charges VALUES(?,?,?,?,?,?)',('prior','synthetic-request',60000000,None,'uncertain',1699999900))
        self.before=self.snapshot()
        self.receipt=dict(schema_version=1,study='poietic-agents',attempt='D0-01',approved=True,
            receipt_id='synthetic-receipt',decision_reference='unit-test-only',approved_at=self.now-30,
            duration_seconds=3600,maximum_new_calls=36,workers_and_relays_stopped=True,
            quiescence_checked_at=self.now-5,quiescence_reference='synthetic-stop-check',
            expected_authority=self.old,old_authorization=self.auth,expected_charge_count=1,
            charges_sha256=digest(self.before[1]))
    def tearDown(self):self.db.close();self.tmp.cleanup()
    def snapshot(self):
        return (self.db.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone(),
                self.db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall())
    def apply(self,r=None):return apply_approved_window(self.path,self.receipt if r is None else r,now=self.now)
    def test_valid_transition_preserves_charges_caps_host_and_old_history(self):
        out=self.apply();after=self.snapshot()
        self.assertEqual(after[0][1:4],self.before[0][1:4]);self.assertEqual(after[1],self.before[1])
        self.assertEqual(after[0][4],self.now+3600)
        old_auth=copy.deepcopy(out['authorization']);old_auth['deadline']=self.auth['deadline']
        self.assertEqual(old_auth,self.auth)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM authority_renewals').fetchone()[0],1)
    def test_no_receipt_or_pending_decision_cannot_transition(self):
        for receipt in (None,{},dict(self.receipt,approved=False)):
            with self.subTest(receipt=receipt is None),self.assertRaises(RenewalError):
                apply_approved_window(self.path,receipt,now=self.now)
            self.assertEqual(self.snapshot(),self.before)
    def test_full_old_authority_mismatch_rejected(self):
        for field,value in [('host','other-host'),('cap',1600000000),('calls',300),('hash','wrong'),('deadline',self.now)]:
            r=copy.deepcopy(self.receipt);r['expected_authority'][field]=value
            with self.subTest(field=field),self.assertRaisesRegex(RenewalError,'old_authority_changed'):self.apply(r)
            self.assertEqual(self.snapshot(),self.before)
    def test_charge_fingerprint_or_count_mismatch_rejected(self):
        for field,value in [('charges_sha256','wrong'),('expected_charge_count',0)]:
            r=dict(self.receipt,**{field:value})
            with self.subTest(field=field),self.assertRaisesRegex(RenewalError,'charge_history_changed'):self.apply(r)
            self.assertEqual(self.snapshot(),self.before)
    def test_changed_old_authorization_is_not_new_budget(self):
        r=copy.deepcopy(self.receipt);r['old_authorization']['total_cumulative_cap_usd']=3
        with self.assertRaisesRegex(RenewalError,'old_authorization_mismatch'):self.apply(r)
        self.assertEqual(self.snapshot(),self.before)
    def test_duplicate_receipt_cannot_add_another_window(self):
        self.apply();after=self.snapshot()
        with self.assertRaisesRegex(RenewalError,'receipt_already_used'):self.apply()
        self.assertEqual(self.snapshot(),after)
        self.assertEqual(self.db.execute('SELECT COUNT(*) FROM authority_renewals').fetchone()[0],1)
    def test_concurrent_writer_rejected_without_wait_or_mutation(self):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            with self.assertRaisesRegex(RenewalError,'concurrent_writer'):self.apply()
            self.assertEqual(self.snapshot(),self.before)
        finally:self.db.rollback()
    def test_sql_failure_rolls_back_authority_and_history(self):
        self.db.execute("CREATE TRIGGER fail_renewal BEFORE UPDATE ON authority BEGIN SELECT RAISE(ABORT,'synthetic fault'); END")
        with self.assertRaises(sqlite3.IntegrityError):self.apply()
        self.assertEqual(self.snapshot(),self.before)
        self.assertFalse(self.db.execute("SELECT1 FROM sqlite_master WHERE name='authority_renewals'".replace('SELECT1','SELECT 1')).fetchone())
    def test_stale_quiescence_or_approval_rejected(self):
        for update in ({'quiescence_checked_at':self.now-301},{'workers_and_relays_stopped':False},{'approved_at':self.now-3601}):
            with self.subTest(update=update),self.assertRaises(RenewalError):self.apply(dict(self.receipt,**update))
            self.assertEqual(self.snapshot(),self.before)
    def test_missing_ledger_does_not_create_allowance(self):
        path=Path(self.tmp.name)/'missing.sqlite'
        with self.assertRaisesRegex(RenewalError,'existing_ledger_required'):
            apply_approved_window(path,self.receipt,now=self.now)
        self.assertFalse(path.exists())
    def test_unreconciled_reservation_rejected(self):
        self.db.execute("UPDATE charges SET status='reserved'");before=self.snapshot()
        r=dict(self.receipt,charges_sha256=digest(before[1]))
        with self.assertRaisesRegex(RenewalError,'inflight_reservation'):self.apply(r)
        self.assertEqual(self.snapshot(),before)
    def test_scope_cannot_expand_window_or_calls(self):
        for update in ({'duration_seconds':7201},{'maximum_new_calls':145},{'attempt':'S0-03'}):
            with self.subTest(update=update),self.assertRaisesRegex(RenewalError,'renewal_scope'):self.apply(dict(self.receipt,**update))
            self.assertEqual(self.snapshot(),self.before)
