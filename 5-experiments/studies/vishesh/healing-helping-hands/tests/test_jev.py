import sys,unittest,sqlite3,collections,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from jev import *
from jev_relay import reserve,RESERVE_NANO
class JevTests(unittest.TestCase):
 def test_frozen_inputs_and_route(self):
  cases=fixtures();self.assertEqual(collections.Counter(c['expected'] for c in cases),dict.fromkeys(LABELS,20))
  for i,c in enumerate(cases):
   r=request(c,i);self.assertEqual(set(r['state']),{'claim','report'});self.assertEqual(r['model'],MODEL);self.assertFalse(r['provider']['allow_fallbacks']);self.assertLess(len(json.dumps(r)),3000)
 def test_response_pin_and_probabilities(self):
  r={'model':SNAPSHOT,'provider':'TypeSafe','answers':{'label':{'choice':'SUPPORT','probabilities':{'SUPPORT':.8,'REFUTE':.1,'UNCERTAIN':.1},'confidence':.7}},'usage':{'input_tokens':400,'cost':.0000168}}
  self.assertEqual(validate(r)['label'],'SUPPORT');r['provider']='other'
  with self.assertRaises(ValueError):validate(r)
 def test_duplicate_or_overbudget_never_dispatches(self):
  db=sqlite3.connect(':memory:');self.addCleanup(db.close);db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');reserve(db,'one')
  with self.assertRaises(sqlite3.IntegrityError):reserve(db,'one')
  self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],1)
  for i in range(59):reserve(db,str(i))
  with self.assertRaises(RuntimeError):reserve(db,'over')
  self.assertEqual(db.execute('SELECT sum(reserved) FROM calls').fetchone()[0],60*RESERVE_NANO)
 def test_wire_order_is_preserved(self):
  from jev_relay import canonical
  x=fixtures()[0]
  orders=[list(json.loads(canonical(request(x,i)))['questions']['label']['criteria']) for i in range(3)]
  self.assertEqual(orders,[list(LABELS[i:]+LABELS[:i]) for i in range(3)])
  self.assertNotEqual(request(x,0,'seed-1')['session_id'],request(x,0,'seed-2')['session_id'])
 def test_budget_settlement_preserves_failed_reservations(self):
  db=sqlite3.connect(':memory:');self.addCleanup(db.close);db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)')
  for i in range(200):
   reserve(db,str(i),720,True);db.execute('UPDATE calls SET status=?,cost=? WHERE hash=?',('completed',.00002,str(i)));db.commit()
  for i in range(201,272):reserve(db,str(i),720,True)
  with self.assertRaises(RuntimeError):reserve(db,'exhausted-by-uncertain-calls',720,True)
 def test_fresh_qualification_text(self):
  from reference import new_qualification
  old={x['report'] for x in fixtures()};new=new_qualification();self.assertFalse(old & {x['report'] for x in new});self.assertEqual(collections.Counter(x['expected'] for x in new),dict.fromkeys(LABELS,20))
 def test_contiguous_erasure_is_measured_and_recovers(self):
  from reference import corpus
  from sim import rollout
  for seed in (8701,8702,8703):
   c=corpus(seed);tape=[d['label'] for d in c['docs']];r=rollout(c,tape,'evidence-only','erasure');control=rollout(c,tape,'evidence-only','none');self.assertEqual(len(c['erased']),40);self.assertEqual(r['event_snapshot']['memory_count'].count(0),40);self.assertLess(r['frames'][10]['coverage'],control['frames'][10]['coverage']);self.assertEqual(r['metrics']['final_accuracy'],1);self.assertEqual(r['metrics']['final_coverage'],1)
