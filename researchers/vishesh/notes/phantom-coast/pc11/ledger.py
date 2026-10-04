"""Q1-only cumulative envelope. A new stage cannot create an allowance."""
import hashlib,sqlite3
from pathlib import Path
PRIOR_NANO=859838490
KNOWN_PRIOR_NANO=847742490
PREDECESSOR='8637bd97fef2be548a310a0c8d60b69dd3eb226f030b8a974fce70658e2932e3'
MAX_CALLS=128
CEILING_NANO=2744320000
class Ledger:
 def __init__(self,path,predecessor):
  if hashlib.sha256(Path(predecessor).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('predecessor')
  self.db=sqlite3.connect(path)
  self.db.execute('CREATE TABLE IF NOT EXISTS authority(id INTEGER PRIMARY KEY,prior INTEGER,predecessor TEXT,ceiling INTEGER)')
  row=(PRIOR_NANO,PREDECESSOR,CEILING_NANO);self.db.execute('INSERT OR IGNORE INTO authority VALUES(1,?,?,?)',row)
  if self.db.execute('SELECT prior,predecessor,ceiling FROM authority').fetchone()!=row:raise ValueError('authority')
  self.db.execute('CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,reserved INTEGER,actual INTEGER,status TEXT)');self.db.execute('CREATE TABLE IF NOT EXISTS attempt(id TEXT PRIMARY KEY)');self.db.commit()
 def claim(self):
  try:self.db.execute("INSERT INTO attempt VALUES('pc11-cycle-a1')");self.db.commit()
  except BaseException:self.db.rollback();raise
 def reserve(self,id,amount):
  if type(amount)!=int or not 0<amount<=21440000:raise ValueError('reservation')
  if not self.db.execute('SELECT id FROM attempt').fetchone():raise ValueError('unclaimed')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   n,total=self.db.execute('SELECT count(*),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
   if n>=128 or total+amount>CEILING_NANO or PRIOR_NANO+total+amount>4000000000:raise ValueError('budget')
   self.db.execute('INSERT INTO calls VALUES(?,?,NULL,?)',(id,amount,'started'));self.db.commit()
  except BaseException:self.db.rollback();raise
 def finish(self,id,actual):
  row=self.db.execute('SELECT reserved,status FROM calls WHERE id=?',(id,)).fetchone()
  if row is None or row[1]!='started' or (actual is not None and (type(actual)!=int or not 0<=actual<=row[0])):raise ValueError('settlement')
  self.db.execute('UPDATE calls SET actual=?,status=? WHERE id=?',(actual,'known' if actual is not None else 'uncertain',id));self.db.commit()
 def summary(self):
  n,actual,exposure=self.db.execute('SELECT count(*),coalesce(sum(actual),0),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
  return dict(calls=n,new_known_nano=actual,cumulative_known_nano=KNOWN_PRIOR_NANO+actual,cumulative_exposure_nano=PRIOR_NANO+exposure,original_api_cap_nano=4000000000,original_total_cap_nano=5000000000)
