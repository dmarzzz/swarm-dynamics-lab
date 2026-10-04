"""One cumulative Telephone ledger; reservations survive failures and attempts."""
import sqlite3,time
class Ledger:
 def __init__(self,path,total_cap_nano,authority_ref):
  if type(total_cap_nano) is not int or not 0<total_cap_nano<=20000000000 or not authority_ref:raise ValueError('authority')
  self.db=sqlite3.connect(path,isolation_level=None);self.db.execute('PRAGMA journal_mode=WAL');self.db.execute('PRAGMA synchronous=FULL')
  self.db.executescript('CREATE TABLE IF NOT EXISTS authority (id INTEGER PRIMARY KEY CHECK(id=1),cap INTEGER,ref TEXT);CREATE TABLE IF NOT EXISTS charges (id TEXT PRIMARY KEY,stage TEXT,kind TEXT,reserve INTEGER,actual INTEGER,status TEXT,request_hash TEXT);')
  row=self.db.execute('SELECT cap,ref FROM authority').fetchone()
  if row is None:self.db.execute('INSERT INTO authority VALUES (1,?,?)',(total_cap_nano,authority_ref))
  elif row!=(total_cap_nano,authority_ref):
   self.db.close();raise ValueError('cannot_reset_authority')
 def reserve(self,cid,stage,kind,amount,request_hash,stage_call_cap=72):
  self.db.execute('BEGIN IMMEDIATE')
  try:
   cap=self.db.execute('SELECT cap FROM authority').fetchone()[0]
   used=self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserve)),0) FROM charges').fetchone()[0]
   calls=self.db.execute("SELECT COUNT(*) FROM charges WHERE stage=? AND kind='model'",(stage,)).fetchone()[0]
   if type(amount) is not int or amount<=0 or amount+used>cap:raise ValueError('budget_exceeded')
   if kind not in ('model','infrastructure') or (kind=='model' and calls>=stage_call_cap):raise ValueError('call_limit')
   self.db.execute('INSERT INTO charges VALUES (?,?,?,?,NULL,?,?)',(cid,stage,kind,amount,'reserved',request_hash));self.db.commit()
  except Exception:self.db.rollback();raise
 def settle(self,cid,actual):
  self.db.execute('BEGIN IMMEDIATE')
  try:
   row=self.db.execute('SELECT reserve,status FROM charges WHERE id=?',(cid,)).fetchone()
   if not row or row[1]!='reserved' or (actual is not None and (type(actual) is not int or not 0<=actual<=row[0])):raise ValueError('settlement')
   self.db.execute('UPDATE charges SET actual=?,status=? WHERE id=?',(actual,'known' if actual is not None else 'uncertain',cid));self.db.commit()
  except Exception:self.db.rollback();raise
 def summary(self):
  r=self.db.execute("SELECT COUNT(*),COALESCE(SUM(actual),0),COALESCE(SUM(COALESCE(actual,reserve)),0),COALESCE(SUM(status!='known'),0) FROM charges WHERE kind='model'").fetchone()
  total=self.db.execute('SELECT COALESCE(SUM(COALESCE(actual,reserve)),0) FROM charges').fetchone()[0]
  return dict(model_calls=r[0],known_model_nano=r[1],model_upper_nano=r[2],unresolved_model_calls=r[3],total_upper_nano=total)
