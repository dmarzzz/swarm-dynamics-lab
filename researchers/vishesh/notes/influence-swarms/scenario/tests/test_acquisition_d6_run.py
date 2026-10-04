import copy,json,sqlite3,tempfile,unittest,urllib.error,sys
from pathlib import Path
from contextlib import closing
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import acquisition_d6_run as run
from typed_diagnostic import FixturePolicy,scripted
class BoundRunnerTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.db=self.root/'ledger';self.packet=json.loads(run.PACKET.read_text())
  with closing(sqlite3.connect(self.db)) as db,db:db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,8,4.868832,246)')
 def tearDown(self):self.tmp.cleanup()
 def test_429_retains_second_assignment_unstarted(self):
  calls=[]
  def transport(raw):calls.append(raw);raise urllib.error.HTTPError('x',429,'not retained',{'retry-after':'20'},None)
  s=run.collect(self.packet,self.root/'result',self.db,transport)
  self.assertEqual((s['started'],s['failed'],s['unstarted']),(1,1,1));self.assertEqual(len(calls),1);self.assertEqual(s['failures'][0]['http_status'],429);self.assertIsNone(s['actual_usd'])
 def test_both_contracts_pass_with_offline_fixture_only(self):
  answers=[FixturePolicy().complete(i['request'],scripted) for i in self.packet['requests']]
  def transport(raw):return json.dumps({'content':[{'type':'text','text':json.dumps(answers.pop(0))}],'stop_reason':'end_turn','usage':{'input_tokens':1,'output_tokens':1}}).encode()
  s=run.collect(self.packet,self.root/'result',self.db,transport);self.assertEqual(s['valid'],2);self.assertEqual(s['unstarted'],0);self.assertFalse(s['qualified'])
 def test_changed_wire_refused(self):
  bad=copy.deepcopy(self.packet);bad['requests'][0]['wire_body']['max_tokens']=4000
  with self.assertRaises(AssertionError):run.verify_packet(bad)
