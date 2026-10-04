"""Append RD7 reservations to the original ledger; never create or reset it."""
import fcntl
import hashlib
import json
import math
from pathlib import Path
import sqlite3
import sys
from urllib.parse import quote
from cases import digest, BASE
from native_gates import RESERVE, CAP, STAGES, SNAPSHOT, require
sys.path.insert(0, str(BASE.parent/'src'))
from jev import validate, response_fingerprint


def baseline(db):
    rows = db.execute("SELECT key,status,reserved_nano,actual_nano FROM calls WHERE key NOT LIKE 'RD7:%' ORDER BY key").fetchall()
    return {'baseline_calls': len(rows),
            'baseline_committed_nano': sum(r[3] if r[3] is not None else r[2] for r in rows),
            'baseline_sha256': digest(rows)}


def snapshot(db):
    count, committed = db.execute('SELECT count(*),coalesce(sum(coalesce(actual_nano,reserved_nano)),0) FROM calls').fetchone()
    return {'lifetime_calls': count, 'api_committed_nano': committed}


class Ledger:
    def __init__(self, path, authority):
        self.path = Path(path).resolve(strict=True)
        st = self.path.stat()
        require(str(self.path) == authority['ledger_path'] and st.st_dev == authority['ledger_device']
                and st.st_ino == authority['ledger_inode'], 'original_ledger_identity')
        # A sidecar flock avoids conflicting with SQLite's own locks on macOS.
        self.lock = self.path.with_name(self.path.name+'.rd6.lock').open('a+b')
        try:
            fcntl.flock(self.lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.db = sqlite3.connect('file:'+quote(str(self.path))+'?mode=rw',uri=True)
            require(baseline(self.db) == {k: authority[k] for k in baseline(self.db)}, 'ledger_baseline_mismatch')
            require(authority['baseline_calls'] == 506 and authority['baseline_committed_nano'] == 23_434_447, 'historical_budget_required')
            self.db.execute('CREATE TABLE IF NOT EXISTS rd7_attempts(stage TEXT PRIMARY KEY,attempt TEXT UNIQUE,packet TEXT,status TEXT)')
            self.db.execute('CREATE TABLE IF NOT EXISTS rd7_responses(key TEXT PRIMARY KEY,data TEXT)')
            self.db.commit()
            self.active = {}
        except BaseException:
            if hasattr(self, 'db'): self.db.close()
            self.lock.close()
            raise

    def close(self):
        self.db.close()
        self.lock.close()

    def begin(self, packet, attempt, replacement=None):
        require(replacement is None and packet['stage']=='F0' and attempt=='rd7-f0-a1', 'single_diagnostic_scope')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            self.db.execute('INSERT INTO rd7_attempts VALUES(?,?,?,?)',('F0',attempt,digest(packet),'started'))
            self.db.commit(); self.active['F0']=('rd7_attempts',attempt)
        except BaseException:
            self.db.rollback(); raise

    def reserve(self, packet, assignment):
        db = self.db
        db.execute('BEGIN IMMEDIATE')
        try:
            stage = packet['stage']
            table,attempt=self.active.get(stage,('rd7_attempts',''))
            row = db.execute('SELECT packet,status FROM '+table+' WHERE stage=? AND attempt=?',(stage,attempt)).fetchone()
            require(row == (digest(packet),'started'), 'inactive_attempt')
            prior = snapshot(db)
            used = db.execute("SELECT count(*) FROM calls WHERE key LIKE 'RD7:%'").fetchone()[0]
            stage_used = db.execute('SELECT count(*) FROM calls WHERE key LIKE ?',('RD7:'+stage+':%',)).fetchone()[0]
            require(stage_used < STAGES[stage] and used < 48 and prior['lifetime_calls'] < 554
                    and prior['api_committed_nano']+RESERVE <= CAP, 'budget_exhausted')
            require(assignment == packet['assignments'][stage_used], 'assignment_order_or_duplicate')
            key = 'RD7:'+stage+':'+assignment['id']
            db.execute('INSERT INTO calls(key,status,reserved_nano) VALUES(?,?,?)',(key,'dispatch_unknown',RESERVE))
            db.commit()
            return key
        except BaseException:
            db.rollback()
            raise

    def settle(self, key, response, request):
        db = self.db
        require(db.execute('SELECT status FROM calls WHERE key=?',(key,)).fetchone() == ('dispatch_unknown',), 'unreserved_or_duplicate_response')
        usage = response.get('usage', {}) if isinstance(response,dict) else {}
        usage = usage if isinstance(usage,dict) else {}
        cost = usage.get('cost')
        nano = math.ceil(cost*1e9) if type(cost) in (int,float) and math.isfinite(cost) and cost >= 0 else None
        # Even an over-cap charge is recorded; it cannot be hidden by validation.
        if nano is not None and nano <= 9_000_000_000_000_000_000:
            db.execute('UPDATE calls SET actual_nano=? WHERE key=?',(nano,key))
            db.commit()
        diagnostic = response_fingerprint(response,request,SNAPSHOT)
        try:
            checked = validate(response,request,SNAPSHOT)
            require(nano is not None and nano <= RESERVE and checked['input_tokens'] <= 32000, 'response_cost_or_context')
        except Exception:
            db.execute('UPDATE calls SET status=? WHERE key=?',('invalid_response',key))
            db.execute('INSERT INTO rd7_responses VALUES(?,?)',(key,json.dumps({'diagnostic':diagnostic})))
            db.commit()
            raise ValueError('invalid_provider_response') from None
        # Retain all exposed decision fields, only allowlisted fields. Never arbitrary
        # provider error strings, headers or bodies, which could echo a credential.
        visible = {'model':SNAPSHOT,'provider':'TypeSafe','answers':{'action':{
            'choice':checked['action'],'probabilities':checked['probabilities'],'confidence':checked['confidence']}},
            'usage':{'input_tokens':checked['input_tokens'],'cost':checked['cost_usd']}}
        result = {'checked': checked, 'visible_response': visible, 'diagnostic':diagnostic,
                  'settled_nano':nano}
        db.execute('UPDATE calls SET status=? WHERE key=?',('completed',key))
        db.execute('INSERT INTO rd7_responses VALUES(?,?)',(key,json.dumps(result,allow_nan=False)))
        db.commit()
        return result

    def accounting(self, packet):
        rows=[]
        for a in packet['assignments']:
            key='RD7:'+packet['stage']+':'+a['id']
            result=self.db.execute('SELECT status,reserved_nano,actual_nano FROM calls WHERE key=?',(key,)).fetchone()
            if result is None: continue
            data=self.db.execute('SELECT data FROM rd7_responses WHERE key=?',(key,)).fetchone()
            rows.append({'id':a['id'],'status':result[0],'reserved_nano':result[1],
                         'actual_nano':result[2],'response':json.loads(data[0]) if data else None})
        return {'packet_sha256':digest(packet),'calls':rows,'cumulative':snapshot(self.db),
                'baseline':baseline(self.db),'authority':'operator-export-from-original-ledger'}

    def finish(self, stage, status):
        require(status in ('completed','stopped'), 'terminal_attempt_status')
        require(stage in self.active,'inactive_attempt')
        table,attempt=self.active[stage]
        self.db.execute('UPDATE '+table+' SET status=? WHERE stage=? AND attempt=?',(status,stage,attempt))
        self.db.commit()
