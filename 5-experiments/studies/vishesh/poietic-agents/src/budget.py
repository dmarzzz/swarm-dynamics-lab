"""Single-host transactional reservations. Uncertain requests keep their full reserve."""
import sqlite3
import time


class Budget:
    def __init__(self, path, authority_hash, host, cap_nano, call_cap, deadline):
        self.db = sqlite3.connect(path, timeout=10, isolation_level=None)
        self.db.execute('PRAGMA journal_mode=WAL')
        self.db.execute('PRAGMA synchronous=FULL')
        self.db.execute('CREATE TABLE IF NOT EXISTS authority (id INTEGER PRIMARY KEY, hash TEXT, host TEXT, cap INTEGER, calls INTEGER, deadline REAL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS charges (id TEXT PRIMARY KEY, request_hash TEXT, reserve INTEGER, settled INTEGER, status TEXT, created REAL)')
        self.db.execute('BEGIN IMMEDIATE')
        existing = self.db.execute('SELECT hash,host,cap,calls,deadline FROM authority WHERE id=1').fetchone()
        expected = (authority_hash, host, cap_nano, call_cap, deadline)
        if existing and existing != expected:
            self.db.rollback(); self.db.close(); raise ValueError('authority_cannot_reset')
        if not existing:
            if cap_nano <= 0 or call_cap <= 0 or deadline <= time.time():
                self.db.rollback(); self.db.close(); raise ValueError('invalid_authority')
            self.db.execute('INSERT INTO authority VALUES (1,?,?,?,?,?)', expected)
        self.db.commit()

    def reserve(self, call_id, request_hash, amount):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            cap, maximum, deadline = self.db.execute('SELECT cap,calls,deadline FROM authority').fetchone()
            count, used = self.db.execute('SELECT COUNT(*),COALESCE(SUM(COALESCE(settled,reserve)),0) FROM charges').fetchone()
            if self.db.execute('SELECT 1 FROM charges WHERE id=?', (call_id,)).fetchone():
                raise ValueError('duplicate_call')
            if type(amount) is not int or amount <= 0 or used+amount > cap or count >= maximum or time.time() >= deadline:
                raise ValueError('budget_or_deadline')
            self.db.execute('INSERT INTO charges VALUES (?,?,?,NULL,?,?)', (call_id,request_hash,amount,'reserved',time.time()))
            self.db.commit()
        except Exception:
            self.db.rollback(); raise

    def settle(self, call_id, actual=None):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            row = self.db.execute('SELECT reserve,status FROM charges WHERE id=?', (call_id,)).fetchone()
            if not row or row[1] != 'reserved': raise ValueError('settlement_state')
            if actual is not None and (type(actual) is not int or not 0 <= actual <= row[0]):
                raise ValueError('billing_exceeds_reserve')
            self.db.execute('UPDATE charges SET settled=?,status=? WHERE id=?', (actual,'known' if actual is not None else 'uncertain',call_id))
            self.db.commit()
        except Exception:
            self.db.rollback(); raise

    def summary(self):
        count, known, total, uncertain = self.db.execute("SELECT COUNT(*),COALESCE(SUM(settled),0),COALESCE(SUM(COALESCE(settled,reserve)),0),SUM(status!='known') FROM charges").fetchone()
        return dict(physical_calls=count, known_api_usd=known/1e9, charged_upper_usd=total/1e9, uncertain_requests=uncertain or 0)

    def close(self):
        self.db.close()
