import importlib.util,json,sqlite3,tempfile,unittest,urllib.error
from pathlib import Path
from contextlib import closing
from unittest.mock import Mock,patch
BASE=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location('d6',BASE/'analysis/acquisition_d6.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m)
GOOD=json.dumps({'usage':{'input_tokens':10,'output_tokens':3},'stop_reason':'end_turn','content':[{'text':'{}'}]}).encode()
class AcquisitionTests(unittest.TestCase):
 def setUp(self):
  self.tmp=tempfile.TemporaryDirectory();self.root=Path(self.tmp.name);self.db=self.root/'ledger.sqlite'
  with closing(sqlite3.connect(self.db)) as db, db:db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,8,4.868832,246)')
 def tearDown(self):self.tmp.cleanup()
 def session(self,name='attempt'):return m.Session(self.root/name,self.db)
 def invoke(self,s,t,validator=lambda r:r):return s.dispatch(b'{}',t,validator,.048640)
 def test_http_first_failure_stops_all_statuses(self):
  for code in (429,502,503,504,401):
   s=self.session(str(code));t=Mock(side_effect=urllib.error.HTTPError('https://example.invalid',code,'DO NOT LOG',{'retry-after':'12','request-id':'req_12345678','Authorization':'NEVER LOG'},None))
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
   self.assertEqual(t.call_count,1);events=(s.directory/'events.jsonl').read_text();self.assertNotIn('NEVER',events);self.assertNotIn('DO NOT',events)
   e=json.loads(events.splitlines()[-1]);self.assertEqual(e['http_status'],code);self.assertEqual(e['retry_after_seconds'],12);self.assertFalse(e['retry_permitted']);self.assertIsNone(e['actual_usd'])
 def test_unsafe_headers_dropped(self):
  e=m.safe_http(urllib.error.HTTPError('x',429,'x',{'retry-after':'secret-text','request-id':'sk-ant-secret'},None));self.assertIsNone(e['request_id']);self.assertIsNone(e['retry_after_seconds'])
 def test_timeout_parse_and_missing_usage_stop(self):
  for name,transport in [('timeout',Mock(side_effect=TimeoutError('private'))),('parse',Mock(return_value=b'bad')),('missing',Mock(return_value=b'{}')),('negative',Mock(return_value=b'{"usage":{"input_tokens":-1,"output_tokens":0}}'))]:
   s=self.session(name)
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,transport)
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,transport)
   self.assertEqual(transport.call_count,1)
 def test_success_two_requests_only_and_reservation_before_send(self):
  def send(_):
   with closing(sqlite3.connect(self.db)) as db, db:cap,reserved,calls=db.execute('SELECT cap,reserved,calls FROM budget').fetchone()
   self.assertGreater(reserved,4.868832);self.assertGreater(calls,246);return GOOD
  s=self.session();t=Mock(side_effect=send);self.invoke(s,t);self.invoke(s,t)
  with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
  self.assertEqual(t.call_count,2)
  with self.assertRaises(m.AcquisitionStopped):self.session()
 def test_budget_shortage_never_sends(self):
  with closing(sqlite3.connect(self.db)) as db, db:db.execute('UPDATE budget SET reserved=7.99')
  s=self.session();t=Mock(return_value=GOOD)
  with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
  t.assert_not_called()
 def test_contract_failure_keeps_known_usage(self):
  s=self.session();t=Mock(return_value=GOOD)
  with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t,Mock(side_effect=ValueError('private content')))
  events=(s.directory/'events.jsonl').read_text();self.assertNotIn('private',events);e=json.loads(events.splitlines()[-1]);self.assertTrue(e['usage_known']);self.assertGreater(e['actual_usd'],0)
 def test_inflight_journal_refuses_dispatch(self):
  s=self.session();s._state('inflight');t=Mock(return_value=GOOD)
  with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
  t.assert_not_called()
 def test_missing_ledger_not_created(self):
  p=self.root/'absent'
  with self.assertRaises(m.AcquisitionStopped):m.Session(self.root/'new',p)
  self.assertFalse(p.exists())

 def test_failed_validation_retains_exact_bodies(self):
  for name,raw,validator in [('malformed',b'not-json',lambda r:r),('unknown-usage',b'{}',lambda r:r),('bad-contract',GOOD,Mock(side_effect=ValueError()))]:
   s=self.session(name);t=Mock(return_value=raw)
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t,validator)
   self.assertEqual((s.directory/'01-request.bin').read_bytes(),b'{}');self.assertEqual((s.directory/'01-response.bin').read_bytes(),raw)
   self.assertEqual((s.directory/'01-response.bin').stat().st_mode&0o777,0o600);self.assertEqual(s.directory.stat().st_mode&0o777,0o700)
   self.assertFalse((s.directory/'02-request.bin').exists());self.assertFalse((s.directory/'02-response.bin').exists())
 def test_artifact_writer_failure_closes_circuit(self):
  for fail_on in ('request','response'):
   s=self.session(fail_on);original=s._artifact;t=Mock(return_value=GOOD)
   def writer(kind,raw):
    if kind==fail_on:raise OSError('storage unavailable')
    return original(kind,raw)
   with patch.object(s,'_artifact',side_effect=writer):
    with self.assertRaises(OSError):self.invoke(s,t)
   with self.assertRaises(m.AcquisitionStopped):self.invoke(s,t)
   self.assertEqual(t.call_count,0 if fail_on=='request' else 1)
