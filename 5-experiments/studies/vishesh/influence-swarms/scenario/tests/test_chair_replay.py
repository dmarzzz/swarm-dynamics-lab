import json,sqlite3,tempfile,sys,unittest,io,urllib.error
from pathlib import Path
from unittest.mock import Mock
from contextlib import closing
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import chair_replay_run as run
from study import scripted
class ChairReplayTests(unittest.TestCase):
 def setUp(self):
  self.t=tempfile.TemporaryDirectory();self.root=Path(self.t.name);self.db=self.root/'ledger';self.p=run.verify_packet(json.loads((BASE/'reviews/D10-packet.json').read_text()))
  with closing(sqlite3.connect(self.db)) as d, d:d.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');d.execute('INSERT INTO budget VALUES(1,8,5.501152,259)')
 def tearDown(self):self.t.cleanup()
 def test_full_frozen_fixture_and_accounting(self):
  def transport(raw):
   wire=json.loads(raw);a=scripted(json.loads(wire['messages'][1]['content']));return json.dumps({'model':run.MODEL,'provider':'Anthropic','choices':[{'finish_reason':'stop','message':{'content':json.dumps(a)}}],'usage':{'prompt_tokens':1,'completion_tokens':1,'cost':.000006}}).encode()
  s=run.collect(self.p,self.root/'out',self.db,transport);self.assertEqual((s['planned'],s['valid'],s['calls'],s['usage_missing']),(10,10,10,0))
  with closing(sqlite3.connect(self.db)) as d, d:cap,reserved,calls=d.execute('SELECT cap,reserved,calls FROM budget').fetchone()
  self.assertEqual(calls,269);self.assertAlmostEqual(reserved,5.987552)
 def test_failure_preserves_unstarted(self):
  t=Mock(side_effect=urllib.error.HTTPError('x',429,'private',{},io.BytesIO(b'{}')));s=run.collect(self.p,self.root/'out',self.db,t)
  self.assertEqual((s['failed'],s['unstarted'],s['calls']),(1,9,1));self.assertEqual(t.call_count,1)
 def test_modified_parent_packet_rejected(self):
  self.p['requests'][0]['wire_body']['model']='different'
  with self.assertRaises(AssertionError):run.verify_packet(self.p)
