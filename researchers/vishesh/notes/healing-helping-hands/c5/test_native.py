"""SCRIPTED offline faults, not model evidence or held-out assignments."""
import unittest,sqlite3,tempfile,json,urllib.error
from pathlib import Path
from unittest.mock import patch
import runtime,worker
from relay import store_response,stored_response
class NativeTests(unittest.TestCase):
    def db(self):
        d=sqlite3.connect(':memory:');d.execute('CREATE TABLE calls(hash TEXT PRIMARY KEY,reserved INTEGER,status TEXT,cost REAL)');d.executemany('INSERT INTO calls VALUES(?,?,?,?)',[(str(i),1344000,'completed',.04/2239) for i in range(2239)]);d.execute('CREATE TABLE c4_hashes(hash TEXT PRIMARY KEY)');d.commit();return d
    def test_rejected_qwen_preserves_task_output_without_retry(self):
        for content in ('not JSON','{"label":"INVALID"}'):
            class Response:
                def __enter__(self):return self
                def __exit__(self,*args):pass
                def read(self):return json.dumps({'message':{'content':content},'headers':{'secret':'excluded'}}).encode()
            with patch('worker.urllib.request.urlopen',return_value=Response()) as request:
                with self.assertRaises(worker.RejectedResponse) as caught:worker.call_http('qwen',{},90)
                self.assertEqual(caught.exception.raw,{'message':{'content':content}})
                self.assertEqual(request.call_count,1)
    def test_rejected_jev_recovery_is_not_completion(self):
        class Response:
            def __enter__(self):return self
            def __exit__(self,*args):pass
            def read(self):return b'{"rejected_task_response":{"answers":[]}}'
        with patch('worker.urllib.request.urlopen',side_effect=[urllib.error.URLError('scripted'),Response()]) as request:
            with self.assertRaises(worker.RejectedResponse) as caught:worker.call_http('jev',{},90)
            self.assertEqual(caught.exception.raw,{'answers':[]})
            self.assertEqual(request.call_count,2)
            self.assertIsInstance(request.call_args_list[1].args[0],str)
    def test_prior_C4_spend_counts_against_same_cycle_cap(self):
        d=self.db();d.execute('INSERT INTO c4_hashes VALUES("0")');d.execute('UPDATE calls SET cost=.029 WHERE hash="0"');d.commit()
        with self.assertRaises(RuntimeError):runtime.reserve(d,'new_C5')
        self.assertFalse(d.execute('SELECT 1 FROM calls WHERE hash="new_C5"').fetchone())
    def test_original_ledger_required(self):
        d=self.db();d.execute('DELETE FROM calls WHERE hash="0"');d.commit()
        with self.assertRaises(RuntimeError):runtime.reserve(d,'fresh')
        self.assertEqual(d.execute('SELECT count(*) FROM calls').fetchone()[0],2238)
    def test_incremental_cap_preserves_reservations(self):
        d=self.db();runtime.reserve(d,'fresh');self.assertEqual(d.execute('SELECT count(*) FROM c5_hashes').fetchone()[0],1)
        d.execute('UPDATE calls SET reserved=29000000 WHERE hash="fresh"');d.commit()
        with self.assertRaises(RuntimeError):runtime.reserve(d,'second')
        self.assertFalse(d.execute('SELECT 1 FROM calls WHERE hash="second"').fetchone())
    def test_ambiguous_slot_cannot_repeat(self):
        d=self.db();runtime.reserve(d,'fresh')
        with self.assertRaises(sqlite3.IntegrityError):runtime.reserve(d,'fresh')
        self.assertEqual(d.execute('SELECT status FROM calls WHERE hash="fresh"').fetchone()[0],'started')
    def test_original_dollar_cap(self):
        d=self.db();d.execute('UPDATE calls SET cost=.099/2239');d.commit()
        with self.assertRaises(RuntimeError):runtime.reserve(d,'fresh')
    def test_get_only_recovery(self):
        requests=[]
        class Response:
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def read(self):return b'{"cached":true}'
        def url(req,**kw):
            requests.append(req)
            if len(requests)==1:raise urllib.error.URLError('scripted disconnect')
            return Response()
        with patch('worker.urllib.request.urlopen',side_effect=url),patch('worker.validate',return_value={'label':'SUPPORT'}):r=worker.call_http('jev',{'a':1},90)
        self.assertTrue(r['recovered_cached_response']);self.assertEqual(len(requests),2);self.assertEqual(requests[0].get_method(),'POST');self.assertIn('/result/',requests[1])
    def test_qwen_does_not_retry(self):
        with patch('worker.urllib.request.urlopen',side_effect=urllib.error.URLError('scripted')) as p:
            with self.assertRaises(urllib.error.URLError):worker.call_http('qwen',{},90)
            self.assertEqual(p.call_count,1)
    def test_duplicate_output_blocks_before_preflight(self):
        with tempfile.TemporaryDirectory() as t,patch('worker.preflight') as p:
            with self.assertRaises(ValueError):worker.run(Path(t),'S0',Path(t)/'unused')
            p.assert_not_called()
    def test_stage_mismatched_health(self):
        class R:
            def __enter__(self):return self
            def __exit__(self,*a):pass
            def read(self):return b'{"ready":true,"attempt":"C3","stage":"S0","seconds_remaining":900}'
        with patch('worker.urllib.request.urlopen',return_value=R()):
            with self.assertRaises(ValueError):worker.health('S0')
if __name__=='__main__':unittest.main()
