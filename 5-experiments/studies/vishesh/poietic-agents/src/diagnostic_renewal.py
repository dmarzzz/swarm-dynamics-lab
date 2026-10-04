"""Apply one explicitly approved time renewal to an existing, quiescent authority.

No CLI, credentials, network, allocation or dispatch. The private receipt is an
operator attestation of a real owner decision, not an authentication mechanism.
This function must never be called against a live authority without that decision.
"""
import copy
import math
import sqlite3
import time
from decimal import Decimal
from common import canonical, digest


class RenewalError(ValueError):
    pass


def _timestamp(value):
    return type(value) in (int, float) and math.isfinite(value)


def apply_approved_window(path, receipt, *, now=None):
    now = time.time() if now is None else now
    if not isinstance(receipt, dict) or receipt.get('approved') is not True:
        raise RenewalError('explicit_renewal_receipt_required')
    if (receipt.get('schema_version') != 1 or receipt.get('study') != 'poietic-agents' or
        receipt.get('attempt') not in ('D0-01','D0-02') or receipt.get('duration_seconds') != 3600 or
        receipt.get('maximum_new_calls') != 36):
        raise RenewalError('renewal_scope')
    for key in ('receipt_id', 'decision_reference'):
        if not isinstance(receipt.get(key), str) or not receipt[key].strip():
            raise RenewalError('renewal_decision_reference')
    approved = receipt.get('approved_at')
    quiet = receipt.get('quiescence_checked_at')
    if (not _timestamp(now) or not _timestamp(approved) or not 0<approved<=now or
        (receipt['attempt']=='D0-01' and now-approved>3600)):
        raise RenewalError('approval_activation_window')
    if (receipt.get('workers_and_relays_stopped') is not True or not _timestamp(quiet) or
        not 0 <= now-quiet <= 300 or not receipt.get('quiescence_reference')):
        raise RenewalError('fresh_quiescence_required')
    old_auth = receipt.get('old_authorization')
    if not isinstance(old_auth, dict):
        raise RenewalError('old_authorization_required')
    # mode=rw refuses a missing ledger; this path can never create a new allowance.
    try:
        db = sqlite3.connect(path.resolve().as_uri()+'?mode=rw', uri=True,
                             timeout=0, isolation_level=None)
    except sqlite3.Error as exc:
        raise RenewalError('existing_ledger_required') from exc
    try:
        try:
            db.execute('BEGIN IMMEDIATE')
        except sqlite3.OperationalError as exc:
            raise RenewalError('concurrent_writer') from exc
        row = db.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone()
        if not row or db.execute('SELECT COUNT(*) FROM authority').fetchone()[0] != 1:
            raise RenewalError('single_authority_required')
        tables = {x[0] for x in db.execute("SELECT name FROM sqlite_master WHERE type='table'")}
        if 'authority_renewals' in tables and db.execute(
                'SELECT 1 FROM authority_renewals WHERE receipt_id=?', (receipt['receipt_id'],)).fetchone():
            raise RenewalError('receipt_already_used')
        old = dict(zip(('hash', 'host', 'cap', 'calls', 'deadline'), row))
        if old != receipt.get('expected_authority'):
            raise RenewalError('old_authority_changed')
        charges = db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        if digest(charges) != receipt.get('charges_sha256') or len(charges) != receipt.get('expected_charge_count'):
            raise RenewalError('charge_history_changed')
        if any(c[4] == 'reserved' for c in charges):
            raise RenewalError('inflight_reservation_unreconciled')
        if receipt['attempt']=='D0-02':
            if (len(charges)!=40 or sum(c[3] if c[3] is not None else c[2] for c in charges)!=482269482):
                raise RenewalError('d002_history_required')
            if receipt.get('allocation_mode')=='existing':
                if (old['host']!='sim-vishesh' or receipt.get('existing_host_owner_approved') is not True or
                    not receipt.get('allocation_reference') or receipt.get('exclusive_approved_account_allocation') is not True or
                    receipt.get('mirror_history_matches') is not True or not receipt.get('mirror_check_reference')):
                    raise RenewalError('d002_existing_host_evidence_required')
            elif (old['host']!='sim-vishesh-poietic' or 'authority_relocations' not in tables or not db.execute(
                    'SELECT 1 FROM authority_relocations WHERE attempt=?',('D0-02',)).fetchone()):
                raise RenewalError('d002_relocated_history_required')
            if 'diagnostic_windows' in tables and db.execute(
                    'SELECT 1 FROM diagnostic_windows WHERE attempt=?',('D0-02',)).fetchone():
                raise RenewalError('diagnostic_window_already_used')
        if not _timestamp(old['deadline']) or old['deadline'] >= now:
            raise RenewalError('original_window_not_expired')
        if old['hash'] != digest(old_auth) or old_auth.get('deadline') != old['deadline']:
            raise RenewalError('old_authorization_mismatch')
        if (old_auth.get('study') != 'poietic-agents' or old_auth.get('stage') != 'S0' or
            old_auth.get('physical_call_cap') != old['calls'] or
            Decimal(str(old_auth.get('api_cap_usd'))) * 10**9 != old['cap']):
            raise RenewalError('old_budget_binding')
        if old['calls']-len(charges) < receipt['maximum_new_calls']:
            raise RenewalError('insufficient_remaining_call_ceiling')
        renewed = copy.deepcopy(old_auth)
        renewed['deadline'] = now + receipt['duration_seconds']
        new = dict(old, hash=digest(renewed), deadline=renewed['deadline'])
        db.execute('''CREATE TABLE IF NOT EXISTS authority_renewals (
            receipt_id TEXT PRIMARY KEY, decision_reference TEXT NOT NULL,
            applied_at REAL NOT NULL, old_authority TEXT NOT NULL,
            new_authority TEXT NOT NULL, charges_sha256 TEXT NOT NULL)''')
        db.execute('INSERT INTO authority_renewals VALUES (?,?,?,?,?,?)',
                   (receipt['receipt_id'], receipt['decision_reference'], now,
                    canonical(old), canonical(new), digest(charges)))
        if receipt['attempt']=='D0-02':
            db.execute('CREATE TABLE IF NOT EXISTS diagnostic_windows (attempt TEXT PRIMARY KEY, receipt_id TEXT NOT NULL)')
            db.execute('INSERT INTO diagnostic_windows VALUES (?,?)',('D0-02',receipt['receipt_id']))
        changed = db.execute('UPDATE authority SET hash=?,deadline=? WHERE id=1 AND hash=? AND deadline=?',
                             (new['hash'], new['deadline'], old['hash'], old['deadline'])).rowcount
        after = db.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone()
        after_charges = db.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        if changed != 1 or after != tuple(new[k] for k in ('hash','host','cap','calls','deadline')) or after_charges != charges:
            raise RenewalError('transition_invariant')
        db.commit()
        return dict(authorization=renewed, authority_sha256=digest(new),
                    charges_sha256=digest(charges), physical_calls=len(charges),
                    receipt_id=receipt['receipt_id'])
    except BaseException:
        if db.in_transaction:
            db.rollback()
        raise
    finally:
        db.close()
