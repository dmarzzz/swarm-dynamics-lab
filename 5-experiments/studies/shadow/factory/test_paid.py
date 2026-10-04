import concurrent.futures,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import paid as p

class BudgetTests(unittest.TestCase):
    def test_per_spec_cap_and_unknown_reservation(self):
        with tempfile.TemporaryDirectory() as d:
            l=p.Ledger(Path(d)/'ledger.jsonl')
            l.event('reserve','a','1',3)
            self.assertEqual(l.accounted('a'),3)
            with self.assertRaises(p.BudgetStop):l.event('reserve','a','2',2)
            l.event('settle','a','1',.1)
            l.event('reserve','a','2',2)
            self.assertAlmostEqual(l.accounted('a'),2.1)
            with self.assertRaises(p.BudgetStop):l.event('reserve','a','2',.1)
    def test_total_cap(self):
        with tempfile.TemporaryDirectory() as d:
            l=p.Ledger(Path(d)/'ledger.jsonl')
            for i in range(5):l.event('reserve',str(i),'1',4)
            with self.assertRaises(p.BudgetStop):l.event('reserve','new','1',.000001)
    def test_parallel_cap(self):
        with tempfile.TemporaryDirectory() as d:
            l=p.Ledger(Path(d)/'ledger.jsonl')
            def reserve(i):
                try:l.event('reserve','a',str(i),1);return 1
                except p.BudgetStop:return 0
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                self.assertEqual(sum(pool.map(reserve,range(20))),4)
    def test_corruption_fail_closed(self):
        with tempfile.TemporaryDirectory() as d:
            file=Path(d)/'ledger.jsonl';file.write_text('invalid\n');l=p.Ledger(file)
            with self.assertRaises(json.JSONDecodeError):l.event('reserve','a','1',1)
    def test_deadline_no_network(self):
        s={'id':'test','model':'anthropic/claude-sonnet-4.6','route':'openrouter','max_paid_usd':4}
        a={'id':'test','packet':{},'stage':'Q'}
        with patch.object(p.f,'enforce_launch_hold'),patch('paid.time.time',return_value=p.f.DEADLINE+1),patch('paid.urllib.request.urlopen') as net:
            r=p.call(s,a,'not-a-key')
        self.assertEqual(r['error'],'BudgetStop:deadline');net.assert_not_called()
if __name__=='__main__':unittest.main()
