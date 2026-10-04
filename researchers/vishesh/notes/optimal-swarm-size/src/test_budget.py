import concurrent.futures
import tempfile
import unittest
from pathlib import Path
from budget import Budget

class Reservations(unittest.TestCase):
    def test_race_persistence_and_unknown_charges(self):
        with tempfile.TemporaryDirectory() as temp:
            path=Path(temp)/'budget.sqlite';b=Budget(path,100)
            def reserve(i):
                try: b.reserve(str(i),'episode',30,100);return True
                except ValueError:return False
            with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
                self.assertEqual(sum(pool.map(reserve,range(20))),3)
            self.assertEqual(Budget(path,100).exposure('episode'),90)
            with self.assertRaises(ValueError): Budget(path,200)
            with b.connect() as db:call=db.execute('SELECT id FROM calls LIMIT 1').fetchone()[0]
            b.settle(call,10);self.assertEqual(b.exposure('episode'),70)
            with self.assertRaises(ValueError):b.settle(call,0)
            with self.assertRaises(ValueError):b.reserve('more','episode',40,100)
            with self.assertRaises(ValueError):b.reserve('more','episode',10,200)
    def test_shared_stage_cap_and_overrun(self):
        with tempfile.TemporaryDirectory() as temp:
            b=Budget(Path(temp)/'budget.sqlite',100)
            b.reserve('one','a',60,90)
            with self.assertRaises(ValueError):b.reserve('two','b',60,90)
            with self.assertRaises(ValueError):b.settle('one',110)
            self.assertFalse(b.healthy());self.assertEqual(b.exposure('a'),110)
if __name__=='__main__': unittest.main()
