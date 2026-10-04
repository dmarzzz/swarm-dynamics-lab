import json,sys,sqlite3,tempfile,unittest,urllib.error
from contextlib import closing
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import acquisition_d8_run as run
from typed_diagnostic import FixturePolicy,scripted
class D8BoundTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.db=self.root/'budget';self.packet=run.verify_packet(json.loads(run.PACKET.read_text()))
  with closing(sqlite3.connect(self.db)) as db,db:
   db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,8,4.966112,248)')
 def tearDown(self):self.tmp.cleanup()
 def test_two_corrected_contracts(self):
  answers=[FixturePolicy().complete(i['request'],scripted) for i in self.packet['requests']]
  def send(raw):
   wire=json.loads(raw);self.assertTrue(wire['response_format']['json_schema']['strict'])
   return json.dumps({'model':run.MODEL,'provider':'Anthropic','choices':[{'finish_reason':'stop','message':{'content':json.dumps(answers.pop(0))}}],'usage':{'prompt_tokens':1,'completion_tokens':1,'cost':.000006}}).encode()
  result=run.collect(self.packet,self.root/'out',self.db,send);self.assertEqual(result['valid'],2);self.assertEqual(result['actual_usd'],.000012)
 def test_schema_deleted_rejected(self):
  del self.packet['requests'][0]['wire_body']['response_format']
  with self.assertRaises(ValueError):run.verify_packet(self.packet)
 def test_first_http_failure_stops(self):
  def send(raw):raise urllib.error.HTTPError('x',429,'private',{},None)
  result=run.collect(self.packet,self.root/'out',self.db,send)
  self.assertEqual((result['calls'],result['failed'],result['unstarted']),(1,1,1));self.assertIsNone(result['actual_usd'])
 def test_actual_d7_markdown_remains_invalid(self):
  raw=(BASE/'reviews/native-D7-01/01-response.bin').read_bytes()
  result=run.collect(self.packet,self.root/'out',self.db,lambda _:raw)
  self.assertEqual((result['valid'],result['unstarted']),(0,1));self.assertEqual(result['failures'][0]['category'],'contract');self.assertEqual(result['actual_usd'],.014422)
