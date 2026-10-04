"""Q0-only cumulative envelope. A new stage cannot create an allowance."""
import hashlib,sqlite3
from pathlib import Path
PRIOR_NANO=858328842
KNOWN_PRIOR_NANO=846232842
PREDECESSOR='765c4004d5e9e259c7afac09860862e14bc4a6a8596258a4e839725b9a905029'
MAX_CALLS=8
CEILING_NANO=53760000
class Ledger:
 def __init__(self,path,predecessor):
  if hashlib.sha256(Path(predecessor).read_bytes()).hexdigest()!=PREDECESSOR:raise ValueError('predecessor')
  self.db=sqlite3.connect(path)
  self.db.execute('CREATE TABLE IF NOT EXISTS authority(id INTEGER PRIMARY KEY,prior INTEGER,predecessor TEXT,ceiling INTEGER)')
  row=(PRIOR_NANO,PREDECESSOR,CEILING_NANO);self.db.execute('INSERT OR IGNORE INTO authority VALUES(1,?,?,?)',row)
  if self.db.execute('SELECT prior,predecessor,ceiling FROM authority').fetchone()!=row:raise ValueError('authority')
  self.db.execute('CREATE TABLE IF NOT EXISTS calls(id TEXT PRIMARY KEY,reserved INTEGER,actual INTEGER,status TEXT)');self.db.execute('CREATE TABLE IF NOT EXISTS attempt(id TEXT PRIMARY KEY)');self.db.commit()
 def claim(self):
  try:self.db.execute("INSERT INTO attempt VALUES('pc9-q0-a1')");self.db.commit()
  except BaseException:self.db.rollback();raise
 def reserve(self,id,amount):
  if type(amount)!=int or not 0<amount<=6720000:raise ValueError('reservation')
  if not self.db.execute('SELECT id FROM attempt').fetchone():raise ValueError('unclaimed')
  self.db.execute('BEGIN IMMEDIATE')
  try:
   n,total=self.db.execute('SELECT count(*),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
   if n>=8 or total+amount>CEILING_NANO or PRIOR_NANO+total+amount>4000000000:raise ValueError('budget')
   self.db.execute('INSERT INTO calls VALUES(?,?,NULL,?)',(id,amount,'started'));self.db.commit()
  except BaseException:self.db.rollback();raise
 def finish(self,id,actual):
  row=self.db.execute('SELECT reserved,status FROM calls WHERE id=?',(id,)).fetchone()
  if row is None or row[1]!='started' or (actual is not None and (type(actual)!=int or not 0<=actual<=row[0])):raise ValueError('settlement')
  self.db.execute('UPDATE calls SET actual=?,status=? WHERE id=?',(actual,'known' if actual is not None else 'uncertain',id));self.db.commit()
 def summary(self):
  n,actual,exposure=self.db.execute('SELECT count(*),coalesce(sum(actual),0),coalesce(sum(coalesce(actual,reserved)),0) FROM calls').fetchone()
  return dict(calls=n,new_known_nano=actual,cumulative_known_nano=KNOWN_PRIOR_NANO+actual,cumulative_exposure_nano=PRIOR_NANO+exposure,original_api_cap_nano=4000000000,original_total_cap_nano=5000000000)
