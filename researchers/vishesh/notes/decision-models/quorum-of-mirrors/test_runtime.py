import json,sqlite3,tempfile,unittest
from pathlib import Path
from relay import Budget
from worker import render
from qualification import manifest

class RuntimeContracts(unittest.TestCase):
    def test_reservation_is_durable_and_duplicate_fails(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ledger.sqlite';b=Budget(p);b.reserve('first');b.finish('first','failed_or_uncertain')
            with self.assertRaises(sqlite3.IntegrityError):Budget(p).reserve('first')
            with sqlite3.connect(p) as db:
                self.assertEqual(db.execute('SELECT status FROM calls').fetchone()[0],'failed_or_uncertain')
                self.assertGreater(db.execute('SELECT SUM(reserved) FROM calls').fetchone()[0],0)
    def test_call_limit_and_authority_mismatch(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'ledger.sqlite';b=Budget(p)
            for i in range(32):b.reserve(str(i))
            with self.assertRaises(ValueError):b.reserve('extra')
            with self.assertRaises(ValueError):Budget(p,2.)
    def test_render_preserves_pending_and_failure(self):
        with tempfile.TemporaryDirectory() as d:
            p=Path(d);m=manifest();render(m,[],p)
            self.assertEqual((p/'matrix.html').read_text().count('<td>unstarted</td>'),32)
            r={'id':m['assignments'][0]['id'],'status':'failed'};render(m,[r],p)
            self.assertEqual((p/'matrix.html').read_text().count('<td>failed</td>'),1)
            self.assertEqual((p/'matrix.html').read_text().count('<td>unstarted</td>'),31)
if __name__=='__main__':unittest.main()
