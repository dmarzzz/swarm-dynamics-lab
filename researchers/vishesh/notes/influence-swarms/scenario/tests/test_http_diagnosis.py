import importlib.util,io,json,sqlite3,tempfile,unittest,urllib.error
from pathlib import Path
from contextlib import closing
from unittest.mock import Mock

BASE=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('diagnosis',BASE/'analysis/acquisition_d6.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)

class HttpDiagnosisTests(unittest.TestCase):
    def error(self,message='',kind='rate_limit_error',code=429,raw=None):
        if raw is None:raw=json.dumps({'type':'error','error':{'type':kind,'message':message}}).encode()
        return urllib.error.HTTPError('https://private.invalid',code,'private reason',{},io.BytesIO(raw))

    def test_explicit_limit_labels(self):
        for message,label in [('Monthly spending limit reached','spend_limit'),('Limit is 100 input tokens per minute','input_token_rate'),('20 output tokens per minute exceeded','output_token_rate'),('Maximum requests per minute','request_rate'),('Acceleration limit reached','acceleration')]:
            with self.subTest(label=label):
                result=m.safe_http(self.error(message),classify_body=True)
                self.assertEqual(result['reported_limit'],label)
                self.assertFalse(result['retry_permitted'])

    def test_unknown_ambiguous_and_wrong_status(self):
        self.assertEqual(m.classified_error(self.error('requests per minute or input tokens per minute'))['reported_limit'],'ambiguous')
        for error in [self.error('Please try later'),self.error('spend limit',code=400),self.error('spend limit',kind='authentication_error')]:
            self.assertEqual(m.classified_error(error)['reported_limit'],'unknown')

    def test_never_returns_provider_text(self):
        marker='PRIVATE_SENTINEL'
        result=m.safe_http(self.error('spend limit '+marker,kind='unrecognized_'+marker),classify_body=True)
        serialized=json.dumps(result)
        for forbidden in (marker,'private.invalid','private reason','spend limit'):
            self.assertNotIn(forbidden,serialized)
        self.assertEqual(result['provider_error_type'],'unknown')

    def test_bounded_and_failed_reads(self):
        for raw,state in [(b'x'*8193,'oversized'),(b'{bad','malformed'),(b'[]','malformed'),(b'\xff','malformed'),(b'{"error":{}}','malformed')]:
            error=self.error(raw=raw);error.read=Mock(return_value=raw)
            self.assertEqual(m.classified_error(error)['error_body_status'],state)
            error.read.assert_called_once_with(8193)
        error=self.error();error.read=Mock(side_effect=OSError('PRIVATE_SENTINEL'))
        self.assertEqual(m.classified_error(error)['error_body_status'],'unreadable')

    def test_default_never_reads_body(self):
        error=self.error('spend limit');error.read=Mock(side_effect=AssertionError('must not read'))
        self.assertNotIn('reported_limit',m.safe_http(error));error.read.assert_not_called()

    def test_session_stops_preserves_reservation_and_discards_raw_error(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);ledger=root/'budget.sqlite'
            with closing(sqlite3.connect(ledger)) as db, db:
                db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)')
                db.execute('INSERT INTO budget VALUES(1,8,4.917472,247)')
            session=m.Session(root/'attempt',ledger,classify_http_body=True)
            transport=Mock(side_effect=self.error('spending limit PRIVATE_SENTINEL'))
            for _ in range(2):
                with self.assertRaises(m.AcquisitionStopped):session.dispatch(b'{}',transport,lambda x:x,.048640)
            self.assertEqual(transport.call_count,1)
            events=(session.directory/'events.jsonl').read_text()
            self.assertNotIn('PRIVATE_SENTINEL',events)
            self.assertEqual(json.loads(events.splitlines()[-1])['reported_limit'],'spend_limit')
            self.assertFalse((session.directory/'01-response.bin').exists())
            with closing(sqlite3.connect(ledger)) as db, db:
                reserved,calls=db.execute('SELECT reserved,calls FROM budget').fetchone()
            self.assertAlmostEqual(reserved,4.966112);self.assertEqual(calls,248)
