"""One-use prospective P30 budget amendment, preserving the sole study ledger.

No authority is inferred here. Caller must verify owner scope, qualification, source,
allocation and public plan; both credential authority and worker mirror retain receipts.
"""
import sqlite3,time
from common import digest

def amend(path,packet,now=None):
    now=time.time() if now is None else now
    a=packet.get('authorization',{});r=packet.get('allocation',{});q=packet.get('qualification',{})
    if not path.is_file():raise ValueError('original_authority_required')
    if packet.get('attempt')!='P30-01' or a.get('study')!='poietic-agents' or a.get('stage')!='P30' or a.get('owner_approved') is not True or not a.get('reference'):raise ValueError('owner_scope')
    if (a.get('api_cap_usd')!=9.25 or a.get('infrastructure_cap_usd')!=.75 or a.get('total_cumulative_cap_usd')!=10 or a.get('physical_call_cap')!=6535 or not now+60<a.get('deadline',0)<=now+10800):raise ValueError('prospective_envelope')
    if q.get('attempt')!='Q30-02' or q.get('passed') is not True or not q.get('summary_sha256') or not q.get('contract_sha256'):raise ValueError('qualification_evidence')
    if r.get('host')!='sim-vishesh' or r.get('exclusive') is not True or r.get('approved_account_verified') is not True or not 0<=now-r.get('checked_at',0)<=300 or r.get('expires_at',0)<a['deadline']+600:raise ValueError('current_allocation')
    if packet.get('workers_stopped') is not True or not packet.get('source_commit') or not packet.get('plan_sha256'):raise ValueError('transition_evidence')
    c=sqlite3.connect(path,isolation_level=None);c.execute('PRAGMA synchronous=FULL');c.execute('BEGIN IMMEDIATE')
    try:
        old=c.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone()
        rows=c.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()
        if list(old or [])!=packet.get('prior_authority') or digest(rows)!=packet.get('prior_charges_sha256') or not 79<=len(rows)<=175 or any(r[4] not in ('known','uncertain') for r in rows):raise ValueError('prior_state_mismatch')
        if old[1]!='sim-vishesh' or old[2]!=1500000000 or old[3]!=288:raise ValueError('old_envelope')
        exposure=sum(r[3] if r[3] is not None else r[2] for r in rows)
        if exposure+3034890240>9250000000:raise ValueError('remaining_budget')
        c.execute('CREATE TABLE IF NOT EXISTS p30_amendments (attempt TEXT PRIMARY KEY, receipt TEXT NOT NULL)')
        if c.execute('SELECT 1 FROM p30_amendments WHERE attempt=?',('P30-01',)).fetchone():raise ValueError('amendment_used')
        after=(digest(a),'sim-vishesh',9250000000,6535,a['deadline'])
        c.execute('UPDATE authority SET hash=?,host=?,cap=?,calls=?,deadline=? WHERE id=1',after)
        receipt=dict(attempt='P30-01',before=list(old),after=list(after),prior_charges_sha256=digest(rows),preserved_calls=len(rows),preserved_exposure_nano=exposure,source_commit=packet['source_commit'],plan_sha256=packet['plan_sha256'],qualification=q,created=now)
        from common import canonical
        c.execute('INSERT INTO p30_amendments VALUES (?,?)',('P30-01',canonical(receipt)))
        assert c.execute('SELECT id,request_hash,reserve,settled,status,created FROM charges ORDER BY id').fetchall()==rows
        c.commit();return receipt
    except BaseException:c.rollback();raise
    finally:c.close()
