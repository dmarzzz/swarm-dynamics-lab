"""One persistent experiment ledger; duplicate/uncertain calls cannot be retried."""
import sqlite3
from native import RESERVE_NANO

class Budget:
    def __init__(self,path,cap_nano,max_calls=540):
        if type(cap_nano)!=int or cap_nano<=0:raise ValueError('authorized_cap_required')
        self.cap=cap_nano;self.max_calls=max_calls;self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,reserved INTEGER NOT NULL,actual INTEGER,status TEXT NOT NULL)')
        self.db.execute('CREATE TABLE IF NOT EXISTS authority(id INTEGER PRIMARY KEY,cap INTEGER,max_calls INTEGER)')
        self.db.execute('INSERT OR IGNORE INTO authority VALUES(1,?,?)',(cap_nano,max_calls))
        if self.db.execute('SELECT cap,max_calls FROM authority').fetchone()!=(cap_nano,max_calls):
            self.db.close();raise ValueError('authority_changed')
        self.db.commit()
    def reserve(self,id):
        self.db.execute('BEGIN IMMEDIATE')
        try:
            count,used=self.db.execute('SELECT count(*),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
            if count>=self.max_calls or used+RESERVE_NANO>self.cap:raise ValueError('budget_exhausted')
            self.db.execute('INSERT INTO calls VALUES(?,?,NULL,?)',(id,RESERVE_NANO,'started'));self.db.commit()
        except BaseException:self.db.rollback();raise
    def finish(self,id,actual=None):
        if actual is not None and (type(actual)!=int or not 0<=actual<=RESERVE_NANO):raise ValueError('cost_above_reservation')
        cur=self.db.execute('UPDATE calls SET actual=?,status=? WHERE id=? AND status=?',(actual,'completed' if actual is not None else 'failed',id,'started'))
        if cur.rowcount!=1:self.db.rollback();raise ValueError('invalid_settlement')
        self.db.commit()
    def summary(self):
        n,actual,charged=self.db.execute('SELECT count(*),coalesce(sum(actual),0),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
        return dict(calls=n,known_cost_usd=actual/1e9,cost_with_unresolved_reservations_usd=charged/1e9,cap_usd=self.cap/1e9)

    def close(self):
        self.db.close()
