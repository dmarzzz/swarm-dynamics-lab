import json,sqlite3,tempfile,unittest,threading
from pathlib import Path
from unittest.mock import patch
import continuation_runtime as c,selector_expansion_runtime as x,turnover,test_selector_expansion as fixtures
class ContinuationTests(unittest.TestCase):
 def test_failed_and_old_requests_rejected(self):
  class L:
   def history(self,ident):return [{}]*26
  v=c.Validator({},L())
  for p in ({'stage':'C2','trajectory':'P1-failover-r0','seq':24},{'stage':'C2','trajectory':'P1-release-r0','seq':25}):
   with self.assertRaises(ValueError):v.check(p)
 def test_cached_prefix_uses_no_network_or_reservation(self):
  class L:
   def history(self,ident):return [{'witnesses':['a','b']}]
  p={'position':'x'};expected={'family':'release','phase':'select','packet':p,'condition':'fixture','request':x.selection.wire('select','release',p)}
  caller=c.Calls('P1-release-r0',Path('/unused'),{},L(),threading.Event(),[expected])
  with patch('urllib.request.urlopen') as net:
   self.assertEqual(caller('release','select',p,'fixture'),{'witnesses':['a','b'],'note':{'witnesses':['a','b']}});net.assert_not_called()
  self.assertEqual(caller.seq,1)
 def test_global_operational_stop_no_new_dispatch(self):
  class L:
   def history(self,ident):return []
  stop=threading.Event();stop.set();caller=c.Calls('P1-release-r0',Path('/unused'),{'deadline':1e20},L(),stop,[])
  with patch('urllib.request.urlopen') as net:
   with self.assertRaisesRegex(ValueError,'shared_stop'):caller('release','select',{},'fixture')
   net.assert_not_called()
class ReservationTests(unittest.TestCase):
 def test_duplicate_next_id_only_one_wins_and_old_ids_rejected(self):
  from concurrent.futures import ThreadPoolExecutor
  from test_expansion_runtime import fixture
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,True)
   for i in range(26):
    rid=l.reserve('P1','P1-release-r0',i);l.settle(rid,.001,{},1)
   with self.assertRaises(ValueError):l.reserve('C2','P1-release-r0',25)
   def reserve(_):
    try:l.reserve('C2','P1-release-r0',26);return 1
    except (ValueError,sqlite3.IntegrityError):return 0
   with ThreadPoolExecutor(max_workers=5) as pool:self.assertEqual(sum(pool.map(reserve,range(5))),1)
   l.settle('P1-release-r0-0026',None);self.assertEqual(l.summary()['C2']['unknown_usd'],'0.02265')
   with l.connect() as db:self.assertEqual(db.execute("SELECT count(*) FROM r3_successor WHERE stage='P1'").fetchone()[0],26)
if __name__=='__main__':unittest.main()
