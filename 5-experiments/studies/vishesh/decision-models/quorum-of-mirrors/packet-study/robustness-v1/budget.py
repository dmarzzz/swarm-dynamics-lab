"""Append-only settlement receipts; retain original reservations and unknown holds."""
import hashlib,json,math
BASE_EXTENSION='PQ-02-owner-2026-10-04'
NEW_EXTENSION='R1-owner-2026-10-04'
def prior_digest(db):
 rows=db.execute('select id,reserved,status,actual from calls order by id').fetchall()
 return hashlib.sha256(json.dumps(rows,separators=(',',':')).encode()).hexdigest()
def exposure(db):
 total=0
 for rid,reserved,status,actual in db.execute('select id,reserved,status,actual from calls'):
  assert type(reserved) in (float,int) and math.isfinite(reserved) and reserved>=0,'invalid_reservation'
  if actual is None:
   assert status in ('reserved','failed_or_uncertain'),'missing_final_cost'
   total+=reserved
  else:
   assert status in ('complete','failed_accounted') and type(actual) in (float,int) and math.isfinite(actual) and 0<=actual<=reserved,'invalid_final_cost'
   total+=actual
 return total

def initialize(db,history_hash,prior_evidence,new_evidence):
 with db:
  db.execute('BEGIN IMMEDIATE')
  assert prior_digest(db)==history_hash,'historical_ledger'
  assert db.execute('select experiment,cap from authority where id=1').fetchone()==('quorum-of-mirrors',1.),'base_authority'
  assert db.execute('select amount,evidence from authority_extensions where id=?',(BASE_EXTENSION,)).fetchone()==(2.,prior_evidence),'prior_authority'
  assert not db.execute("select 1 from next_attempts where status='running'").fetchone(),'running_attempt'
  existing=db.execute('select amount,evidence from authority_extensions where id=?',(NEW_EXTENSION,)).fetchone()
  assert existing is None or existing==(5.,new_evidence),'extension_changed'
  if existing is None:db.execute('insert into authority_extensions values (?,?,?)',(NEW_EXTENSION,5.,new_evidence))
  assert db.execute('select count(*),sum(amount) from authority_extensions').fetchone()==(2,7.),'unexpected_authority'
  db.execute('create table if not exists settlements (call_id text primary key, original_reserved real not null, actual real not null, evidence text not null)')
  for rid,reserved,status,actual in db.execute('select id,reserved,status,actual from calls').fetchall():
   if actual is not None:db.execute('insert or ignore into settlements values (?,?,?,?)',(rid,reserved,actual,'historical-row-sha256:'+history_hash))
  return exposure(db)

def reserve(db,rid,reservation,attempt,max_calls,envelope,prior_evidence,new_evidence):
 with db:
  db.execute('BEGIN IMMEDIATE')
  assert db.execute('select amount,evidence from authority_extensions where id=?',(BASE_EXTENSION,)).fetchone()==(2.,prior_evidence)
  assert db.execute('select amount,evidence from authority_extensions where id=?',(NEW_EXTENSION,)).fetchone()==(5.,new_evidence)
  assert db.execute('select count(*),sum(amount) from authority_extensions').fetchone()==(2,7.)
  count,held=db.execute('select count(*),coalesce(sum(reserved),0) from calls where id like ?',(attempt+'-%',)).fetchone()
  assert count<max_calls and held+reservation<=envelope+1e-9,'attempt_envelope'
  assert exposure(db)+reservation<=8+1e-9,'cumulative_budget'
  db.execute('insert into calls values (?,?,?,NULL)',(rid,reservation,'reserved'))

def settle(db,rid,cost,evidence):
 with db:
  db.execute('BEGIN IMMEDIATE')
  reserved,status,actual=db.execute('select reserved,status,actual from calls where id=?',(rid,)).fetchone()
  assert actual==cost and status in ('complete','failed_accounted') and math.isfinite(cost) and 0<=cost<=reserved,'settlement_invalid'
  db.execute('insert into settlements values (?,?,?,?)',(rid,reserved,cost,evidence))
