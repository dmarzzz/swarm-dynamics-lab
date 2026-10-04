"""Synthetic ledgers only: a new host cannot reset history or the allowance."""
import contextlib
from pathlib import Path
import sqlite3
import sys
import tempfile
import time
import unittest

BASE=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(BASE/'src'))
from budget import Budget
from common import digest
from diagnostic_relocation import relocate_authority
from diagnostic_renewal import apply_approved_window
from diagnostic_admission import verify_prior_budget


class RelocationTests(unittest.TestCase):
    def fixture(self,root):
        path=root/'budget.sqlite';now=time.time()
        auth=dict(study='poietic-agents',stage='S0',api_cap_usd=1.5,
                  physical_call_cap=288,deadline=now+100)
        b=Budget(path,digest(auth),'old-fixture',1_500_000_000,288,auth['deadline'])
        for i in range(40):
            b.reserve(f'history-{i}','fixture',482269443 if i==0 else 1)
            b.settle(f'history-{i}')
        auth['deadline']=now-100
        b.db.execute('UPDATE authority SET hash=?,deadline=?',(digest(auth),auth['deadline']))
        old=dict(zip(('hash','host','cap','calls','deadline'),b.db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchone()))
        charges=b.db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        b.close()
        receipt=dict(approved=True,approved_at=now,checked_at=now,attempt='D0-02',study='poietic-agents',
            new_host='sim-vishesh-poietic',receipt_id='OFFLINE-ONLY',decision_reference='OFFLINE-ONLY',
            allocation_reference='OFFLINE-ONLY',host_key_reference='OFFLINE-ONLY',
            quiescence_reference='OFFLINE-ONLY',old_mirror_fence_reference='OFFLINE-ONLY',
            workers_and_relays_stopped=True,old_worker_mirror_fenced=True,
            exclusive_approved_account_allocation=True,expected_authority=old,charges_sha256=digest(charges))
        return path,receipt,auth,charges,now

    def snapshot(self,path):
        with contextlib.closing(sqlite3.connect(path,isolation_level=None)) as db:
            return (db.execute('SELECT * FROM authority').fetchall(),
                    db.execute('SELECT * FROM charges ORDER BY id').fetchall())

    def test_relocation_then_one_renewal_preserve_every_charge_and_cap(self):
        with tempfile.TemporaryDirectory() as directory:
            path,r,auth,charges,now=self.fixture(Path(directory))
            result=relocate_authority(path,r,now=now)
            self.assertEqual(result['historical_charges'],40)
            self.assertEqual(result['api_exposure_nano'],482269482)
            with contextlib.closing(sqlite3.connect(path,isolation_level=None)) as db:
                new=dict(zip(('hash','host','cap','calls','deadline'),db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchone()))
                self.assertEqual(db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall(),charges)
            self.assertEqual(new,dict(r['expected_authority'],host='sim-vishesh-poietic'))
            renewal=dict(schema_version=1,study='poietic-agents',attempt='D0-02',approved=True,
                duration_seconds=3600,maximum_new_calls=36,receipt_id='OFFLINE-RENEWAL',decision_reference='OFFLINE-ONLY',
                approved_at=now,quiescence_checked_at=now,workers_and_relays_stopped=True,quiescence_reference='OFFLINE-ONLY',
                old_authorization=auth,expected_authority=new,charges_sha256=digest(charges),expected_charge_count=40)
            renewed=apply_approved_window(path,renewal,now=now)
            b=Budget(path,digest(renewed['authorization']),'sim-vishesh-poietic',1_500_000_000,288,now+3600)
            self.assertTrue(verify_prior_budget(b,{'prior_budget':{'physical_calls':40,'exposure_nano':482269482}}))
            with self.assertRaises(ValueError):verify_prior_budget(b,{'prior_budget':{'physical_calls':0,'exposure_nano':0}})
            b.close()
            with self.assertRaises(ValueError):relocate_authority(path,r,now=now)
            with self.assertRaises(ValueError):apply_approved_window(path,renewal,now=now)
            # A different receipt cannot buy a second window for the same attempt.
            later=now+7200
            with contextlib.closing(sqlite3.connect(path)) as db:
                current=dict(zip(('hash','host','cap','calls','deadline'),db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchone()))
            repeated=dict(renewal,receipt_id='ANOTHER-RECEIPT',approved_at=later,
                          quiescence_checked_at=later,old_authorization=renewed['authorization'],expected_authority=current)
            before=self.snapshot(path)
            with self.assertRaisesRegex(ValueError,'diagnostic_window_already_used'):
                apply_approved_window(path,repeated,now=later)
            self.assertEqual(self.snapshot(path),before)

    def test_existing_host_renewal_preserves_history_and_permits_only_one_window(self):
        with tempfile.TemporaryDirectory() as directory:
            path,r,auth,charges,now=self.fixture(Path(directory))
            with contextlib.closing(sqlite3.connect(path,isolation_level=None)) as db:
                db.execute('UPDATE authority SET host=?',('sim-vishesh',))
            renewal=dict(schema_version=1,study='poietic-agents',attempt='D0-02',approved=True,
                duration_seconds=3600,maximum_new_calls=36,receipt_id='OFFLINE-REUSE',decision_reference='OFFLINE',
                approved_at=now,quiescence_checked_at=now,workers_and_relays_stopped=True,quiescence_reference='OFFLINE',
                old_authorization=auth,expected_authority=dict(r['expected_authority'],host='sim-vishesh'),
                charges_sha256=digest(charges),expected_charge_count=40,allocation_mode='existing',
                existing_host_owner_approved=True,allocation_reference='OFFLINE',exclusive_approved_account_allocation=True,
                mirror_history_matches=True,mirror_check_reference='OFFLINE')
            before=self.snapshot(path)
            for field in ['existing_host_owner_approved','allocation_reference','exclusive_approved_account_allocation','mirror_history_matches','mirror_check_reference']:
                bad=dict(renewal);bad[field]=None
                with self.subTest(field=field),self.assertRaises(ValueError):apply_approved_window(path,bad,now=now)
                self.assertEqual(self.snapshot(path),before)
            result=apply_approved_window(path,renewal,now=now)
            after=self.snapshot(path)
            self.assertEqual(before[1],after[1]);self.assertEqual(after[0][0][2],'sim-vishesh')
            with self.assertRaises(ValueError):apply_approved_window(path,renewal,now=now)
            with contextlib.closing(sqlite3.connect(path)) as db:
                current=dict(zip(('hash','host','cap','calls','deadline'),db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchone()))
            later=now+7200
            repeated=dict(renewal,receipt_id='DIFFERENT',quiescence_checked_at=later,
                old_authorization=result['authorization'],expected_authority=current)
            with self.assertRaisesRegex(ValueError,'diagnostic_window_already_used'):apply_approved_window(path,repeated,now=later)
            self.assertEqual(self.snapshot(path),after)

    def test_owner_decision_survives_provisioning_wait_but_checks_must_be_fresh(self):
        with tempfile.TemporaryDirectory() as directory:
            path,r,_,_,now=self.fixture(Path(directory))
            r['approved_at']=now-7200
            self.assertEqual(relocate_authority(path,r,now=now)['historical_charges'],40)

    def test_missing_stale_or_wrong_evidence_never_mutates_ledger(self):
        mutations=[('approved',False),('attempt','D0-03'),('new_host','other-host'),
                   ('workers_and_relays_stopped',False),('old_worker_mirror_fenced',False),
                   ('exclusive_approved_account_allocation',False),('allocation_reference',None),
                   ('host_key_reference',None),('old_mirror_fence_reference',None),
                   ('charges_sha256','bad'),('expected_authority',{}),('checked_at',0),('approved_at',0)]
        for key,value in mutations:
            with self.subTest(key=key),tempfile.TemporaryDirectory() as directory:
                path,r,_,_,now=self.fixture(Path(directory));before=self.snapshot(path)
                r[key]=value
                with self.assertRaises(ValueError):relocate_authority(path,r,now=now)
                self.assertEqual(self.snapshot(path),before)

    def test_missing_ledger_cannot_create_new_authority(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory);_,r,_,_,now=self.fixture(root);missing=root/'absent.sqlite'
            with self.assertRaises(sqlite3.OperationalError):relocate_authority(missing,r,now=now)
            self.assertFalse(missing.exists())

    def test_inflight_history_or_live_window_blocks_relocation(self):
        for mutation in ['UPDATE charges SET status="reserved" WHERE id="history-0"',
                         'DELETE FROM charges WHERE id="history-0"',
                         'UPDATE authority SET deadline=99999999999']:
            with self.subTest(mutation=mutation),tempfile.TemporaryDirectory() as directory:
                path,r,_,_,now=self.fixture(Path(directory))
                with contextlib.closing(sqlite3.connect(path,isolation_level=None)) as db: db.execute(mutation)
                before=self.snapshot(path)
                with self.assertRaises(ValueError):relocate_authority(path,r,now=now)
                self.assertEqual(self.snapshot(path),before)


if __name__=='__main__':unittest.main()
