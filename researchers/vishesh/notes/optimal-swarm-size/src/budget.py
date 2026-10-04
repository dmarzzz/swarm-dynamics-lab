"""Durable single-host atomic reservations; integer microdollars, no credentials."""
import sqlite3
from contextlib import contextmanager

class Budget:
    def __init__(self,path,stage_cap):
        if type(stage_cap) is not int or stage_cap<=0: raise ValueError('invalid_stage_cap')
        self.path=str(path)
        with self.connect() as db:
            db.executescript('CREATE TABLE IF NOT EXISTS settings(cap INTEGER NOT NULL); CREATE TABLE IF NOT EXISTS episodes(id TEXT PRIMARY KEY,cap INTEGER NOT NULL); CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,episode TEXT NOT NULL,held INTEGER NOT NULL,actual INTEGER,state TEXT NOT NULL);')
            row=db.execute('SELECT cap FROM settings').fetchone()
            if row is None: db.execute('INSERT INTO settings VALUES (?)',(stage_cap,))
            elif row[0]!=stage_cap: raise ValueError('cannot_reset_stage_cap')
    @contextmanager
    def connect(self):
        db=sqlite3.connect(self.path,timeout=30)
        try:
            with db: yield db
        finally: db.close()
    def reserve(self,call,episode,maximum,episode_cap):
        if any(type(v) is not int or v<=0 for v in (maximum,episode_cap)): raise ValueError('invalid_reservation')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            if db.execute("SELECT 1 FROM calls WHERE state='overrun'").fetchone(): raise ValueError('prior_overrun')
            db.execute('INSERT OR IGNORE INTO episodes VALUES (?,?)',(episode,episode_cap))
            if db.execute('SELECT cap FROM episodes WHERE id=?',(episode,)).fetchone()[0]!=episode_cap: raise ValueError('cannot_reset_episode_cap')
            if db.execute('SELECT 1 FROM calls WHERE id=?',(call,)).fetchone(): raise ValueError('duplicate_call')
            total=db.execute('SELECT COALESCE(SUM(held),0) FROM calls').fetchone()[0]
            used=db.execute('SELECT COALESCE(SUM(held),0) FROM calls WHERE episode=?',(episode,)).fetchone()[0]
            cap=db.execute('SELECT cap FROM settings').fetchone()[0]
            if total+maximum>cap or used+maximum>episode_cap: raise ValueError('budget_exhausted')
            db.execute('INSERT INTO calls VALUES (?,?,?,NULL,?)',(call,episode,maximum,'reserved'))
    def settle(self,call,actual):
        if type(actual) is not int or actual<0: raise ValueError('invalid_charge')
        with self.connect() as db:
            db.execute('BEGIN IMMEDIATE')
            row=db.execute('SELECT held,state FROM calls WHERE id=?',(call,)).fetchone()
            if row is None or row[1]!='reserved': raise ValueError('invalid_settlement')
            # Unknown/error calls retain full reservation. Overruns stop further admission.
            db.execute('UPDATE calls SET held=?,actual=?,state=? WHERE id=?',(actual,actual,'settled' if actual<=row[0] else 'overrun',call))
        if actual>row[0]: raise ValueError('provider_exceeded_bound')
    def exposure(self,episode):
        with self.connect() as db:
            return db.execute('SELECT COALESCE(SUM(held),0) FROM calls WHERE episode=?',(episode,)).fetchone()[0]
    def healthy(self):
        with self.connect() as db:
            return not db.execute("SELECT 1 FROM calls WHERE state='overrun'").fetchone()
