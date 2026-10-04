"""D0-02-only host rebinding of an existing stopped ledger, never a new allowance.

The operator must first authenticate the new allocation and fence the old worker
mirror. This function verifies a private evidence receipt; it does not establish
those external facts, transfer a database or authorize provisioning/dispatch.
"""
import math
import sqlite3
import time
from common import canonical, digest


def relocate_authority(path, receipt, *, now=None):
    now=time.time() if now is None else now
    def recent(value, seconds):
        return type(value) in (int,float) and math.isfinite(value) and 0<=now-value<=seconds
    if (receipt.get('approved') is not True or receipt.get('attempt')!='D0-02' or
        receipt.get('study')!='poietic-agents' or receipt.get('new_host')!='sim-vishesh-poietic' or
        type(receipt.get('approved_at')) not in (int,float) or
        not math.isfinite(receipt['approved_at']) or not 0<receipt['approved_at']<=now):
        raise ValueError('relocation_scope_or_approval')
    for key in ('receipt_id','decision_reference','allocation_reference','host_key_reference',
                'quiescence_reference','old_mirror_fence_reference'):
        if not isinstance(receipt.get(key),str) or not receipt[key].strip():
            raise ValueError('relocation_evidence_missing')
    if (receipt.get('workers_and_relays_stopped') is not True or
        receipt.get('old_worker_mirror_fenced') is not True or
        receipt.get('exclusive_approved_account_allocation') is not True or
        not recent(receipt.get('checked_at'),300)):
        raise ValueError('relocation_external_checks')
    # mode=rw is intentional: a missing authority cannot become a blank database.
    db=sqlite3.connect(path.resolve().as_uri()+'?mode=rw',uri=True,timeout=0,isolation_level=None)
    try:
        db.execute('BEGIN IMMEDIATE')
        rows=db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchall()
        if len(rows)!=1: raise ValueError('single_original_authority_required')
        old=dict(zip(('hash','host','cap','calls','deadline'),rows[0]))
        if (old!=receipt.get('expected_authority') or old['host']==receipt['new_host'] or
            old['cap']!=1_500_000_000 or old['calls']!=288 or old['deadline']>=now):
            raise ValueError('original_authority_changed_or_live')
        charges=db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        exposure=sum(row[3] if row[3] is not None else row[2] for row in charges)
        if (len(charges)!=40 or digest(charges)!=receipt.get('charges_sha256') or
            exposure!=482269482 or any(row[4]=='reserved' for row in charges)):
            raise ValueError('original_charge_history_changed_or_inflight')
        db.execute('''CREATE TABLE IF NOT EXISTS authority_relocations (
            receipt_id TEXT PRIMARY KEY, attempt TEXT UNIQUE NOT NULL,
            decision_reference TEXT NOT NULL, applied_at REAL NOT NULL,
            old_authority TEXT NOT NULL, new_authority TEXT NOT NULL,
            charges_sha256 TEXT NOT NULL, evidence_sha256 TEXT NOT NULL)''')
        new=dict(old,host=receipt['new_host'])
        db.execute('INSERT INTO authority_relocations VALUES (?,?,?,?,?,?,?,?)',
                   (receipt['receipt_id'],'D0-02',receipt['decision_reference'],now,
                    canonical(old),canonical(new),digest(charges),digest(receipt)))
        changed=db.execute('UPDATE authority SET host=? WHERE id=1 AND host=? AND hash=?',
                           (new['host'],old['host'],old['hash'])).rowcount
        after=db.execute('SELECT hash,host,cap,calls,deadline FROM authority').fetchall()
        after_charges=db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        if changed!=1 or after!=[tuple(new[k] for k in ('hash','host','cap','calls','deadline'))] or after_charges!=charges:
            raise ValueError('relocation_invariant')
        db.commit()
        return dict(attempt='D0-02',host=new['host'],historical_charges=40,
                    api_exposure_nano=exposure,charges_sha256=digest(charges),
                    receipt_id=receipt['receipt_id'],authority_sha256=digest(new))
    except BaseException:
        if db.in_transaction: db.rollback()
        raise
    finally: db.close()
