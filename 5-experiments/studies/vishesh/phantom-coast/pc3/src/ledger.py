"""PC-3 non-overlapping envelope. The reconciled PC-1 ledger is never modified."""
import sqlite3
HISTORICAL_NANO=358051260
CAP_NANO=4000000000
MAX_CALLS=1816

class Ledger:
    def __init__(self,path,predecessor_sha256):
        if len(predecessor_sha256)!=64 or any(c not in '0123456789abcdef' for c in predecessor_sha256):raise ValueError('predecessor_hash')
        self.db=sqlite3.connect(path)
        self.db.execute('CREATE TABLE IF NOT EXISTS authority(id INTEGER PRIMARY KEY,cap INTEGER,prior INTEGER,max_calls INTEGER,predecessor TEXT)')
        expected=(CAP_NANO,HISTORICAL_NANO,MAX_CALLS,predecessor_sha256)
        self.db.execute('INSERT OR IGNORE INTO authority VALUES(1,?,?,?,?)',expected)
        if self.db.execute('SELECT cap,prior,max_calls,predecessor FROM authority').fetchone()!=expected:
            self.db.close();raise ValueError('authority_changed')
        self.db.execute('CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,reserved INTEGER,actual INTEGER,status TEXT)')
        self.db.execute('CREATE TABLE IF NOT EXISTS attempts(stage TEXT PRIMARY KEY,attempt TEXT UNIQUE)');self.db.commit()
    def claim(self,stage,attempt):
        self.db.execute('INSERT INTO attempts VALUES(?,?)',(stage,attempt));self.db.commit()
    def reserve(self,id,amount):
        if type(amount) is not int or not 0<amount<=48384000:raise ValueError('reservation')
        self.db.execute('BEGIN IMMEDIATE')
        try:
            n,cost=self.db.execute('SELECT count(*),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
            if n>=MAX_CALLS or cost+HISTORICAL_NANO+amount>CAP_NANO:raise ValueError('budget_exhausted')
            self.db.execute('INSERT INTO calls VALUES(?,?,NULL,?)',(id,amount,'started'));self.db.commit()
        except BaseException:self.db.rollback();raise
    def finish(self,id,actual=None):
        row=self.db.execute('SELECT reserved,status FROM calls WHERE id=?',(id,)).fetchone()
        if not row or row[1]!='started' or (actual is not None and (type(actual) is not int or not 0<=actual<=row[0])):raise ValueError('settlement')
        self.db.execute('UPDATE calls SET actual=?,status=? WHERE id=?',(actual,'valid' if actual is not None else 'uncertain',id));self.db.commit()
    def summary(self):
        n,actual,exposure=self.db.execute('SELECT count(*),coalesce(sum(actual),0),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
        return dict(calls=n,prior_usd=HISTORICAL_NANO/1e9,new_known_usd=actual/1e9,cumulative_exposure_usd=(HISTORICAL_NANO+exposure)/1e9,api_cap_usd=4,max_calls=MAX_CALLS)
