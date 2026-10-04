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
  db=sqlite3.connect(':memory:');db.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');reserve(db,'one')
  with self.assertRaises(sqlite3.IntegrityError):reserve(db,'one')
  self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],1)
  for i in range(59):reserve(db,str(i))
  with self.assertRaises(RuntimeError):reserve(db,'over')
  self.assertEqual(db.execute('SELECT sum(reserved) FROM calls').fetchone()[0],60*RESERVE_NANO)
