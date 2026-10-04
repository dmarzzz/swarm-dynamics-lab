import json,sqlite3,tempfile,unittest,sys,io,urllib.error
from pathlib import Path
from contextlib import closing
from unittest.mock import Mock
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import readiness_run as run
from acquisition_d6 import Session,AcquisitionStopped
from typed_diagnostic import FixturePolicy,scripted
class ReadinessTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.db=self.root/'ledger';self.p=run.verify_packet(json.loads((BASE/'reviews/D9-A-packet.json').read_text()))
  with closing(sqlite3.connect(self.db)) as db,db:
   db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,8,5.063392,250)')
 def tearDown(self):self.tmp.cleanup()
 def test_typed_success_fixture_and_exact_one_limit(self):
  answer=FixturePolicy().complete(self.p['requests'][0]['request'],scripted)
  raw=json.dumps({'model':run.MODEL,'provider':'Anthropic','choices':[{'finish_reason':'stop','message':{'content':json.dumps(answer)}}],'usage':{'prompt_tokens':1,'completion_tokens':1,'cost':.000006}}).encode()
  t=Mock(return_value=raw);out=run.collect(self.p,self.root/'run',self.db,t)
  self.assertEqual((out['planned'],out['valid'],out['calls']),(1,1,1));self.assertEqual(t.call_count,1)
  self.assertEqual(json.loads((self.root/'run/state.json').read_text())['state'],'complete')
 def test_reason_retained_without_provider_text(self):
  body=json.dumps({'reported_reason':'schema_complexity','error_body_status':'parsed','message':'PRIVATE_SENTINEL'}).encode()
  t=Mock(side_effect=urllib.error.HTTPError('x',400,'private',{},io.BytesIO(body)))
  out=run.collect(self.p,self.root/'run',self.db,t)
  self.assertEqual(out['failures'][0]['reported_reason'],'schema_complexity');self.assertNotIn('PRIVATE_SENTINEL',json.dumps(out));self.assertEqual(t.call_count,1)
 def test_campaign_reservation_ceiling(self):
  with closing(sqlite3.connect(self.db)) as db,db:db.execute('UPDATE budget SET reserved=5.647072,calls=262')
  session=Session(self.root/'run',self.db,maximum_requests=1,reserved_ceiling=5.647072,calls_ceiling=262);t=Mock()
  with self.assertRaises(AcquisitionStopped):session.dispatch(b'{}',t,lambda x:x,.048640)
  t.assert_not_called()
 def test_invalid_count_and_wire_refused(self):
  with self.assertRaises(AcquisitionStopped):Session(self.root/'bad',self.db,maximum_requests=13)
  self.p['requests'][0]['wire_body']['provider']['allow_fallbacks']=True
  with self.assertRaises((ValueError,AssertionError)):run.verify_packet(self.p)
 def test_shared_schema_is_exact_and_tampering_refused(self):
  from readiness_contract import expand
  p=run.verify_packet(json.loads((BASE/'reviews/D9-B-packet.json').read_text()))
  get=lambda p:p['requests'][0]['wire_body']['response_format']['json_schema']['schema']
  self.assertEqual(expand(get(p)),get(self.p))
  get(p)['$defs']['scope']['properties']['storage_region']['type']='number'
  with self.assertRaises(ValueError):run.verify_packet(p)
 def test_five_case_packet_stops_at_first_failure(self):
  p=run.verify_packet(json.loads((BASE/'reviews/D9-C-packet.json').read_text()))
  self.assertEqual(len({i['case_id'] for i in p['requests']}),5)
  self.assertNotIn(self.p['requests'][0]['case_id'],[i['case_id'] for i in p['requests']])
  error=urllib.error.HTTPError('x',400,'private',{},io.BytesIO(b'{}'));t=Mock(side_effect=error)
  out=run.collect(p,self.root/'five',self.db,t)
  self.assertEqual((out['planned'],out['failed'],out['unstarted'],out['calls']),(5,1,4,1));self.assertEqual(t.call_count,1)
 def test_existing_length_bound_regex(self):
  import re
  p=run.verify_packet(json.loads((BASE/'reviews/D9-D-packet.json').read_text()))
  pattern=p['requests'][0]['wire_body']['response_format']['json_schema']['schema']['properties']['limitations']['pattern']
  for value in ('','x'*200,'x'*201,'é'*200,'\n'*200,'\n'*201):
   self.assertEqual(re.fullmatch(pattern,value) is not None,len(value)<=200)
  for value in ('x'*300,'x'*300+'\n','\n'*301):self.assertIsNone(re.search(pattern,value))
