import copy,io,os,json,sqlite3,tempfile,unittest,threading
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from unittest.mock import patch
import selector_expansion_runtime as x,test_q3,contract
from development import dev_world

def fixture(path):
 with sqlite3.connect(path) as db:
  for table in ('calls','sol50_calls'):
   db.execute(f'CREATE TABLE {table}(actual_usd REAL,reserved_usd REAL)');db.executemany(f'INSERT INTO {table} VALUES(?,?)',[(.122835/44,.01)]*44)
  db.execute('CREATE TABLE r3_calls(id TEXT PRIMARY KEY,stage TEXT,reserved TEXT,actual TEXT,status TEXT)');db.executemany('INSERT INTO r3_calls VALUES(?,?,?,?,?)',[('old','Q3','0.02265',None,'ambiguous'),('c1','C1','0.02265','0.000172','terminal')])

def packet():return {'assignments':{'Q3-A2':[{'family':f,'world':dev_world(9900+i)} for i,f in enumerate(x.FAMILIES)],'P1':[{'family':f,'world':dev_world(9950+i),'repeats':[0,1]} for i,f in enumerate(x.FAMILIES)]}}
def answer(expected):
 phase=expected['phase'];p=expected['packet'];family=expected['family'];condition=expected['condition']
 if phase=='commit' and 'broken' in condition:return {'note':{'witnesses':[v['position'] for v in p['roster'] if v['position']!=p['position']][:2]}}
 value=test_q3.oracle(family,phase,p,condition)
 return {'witnesses':value['witnesses']} if phase=='select' else value

class ExpansionTests(unittest.TestCase):
 def test_independent_validator_rejects_input_change_and_early_P1(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,True);v=x.Validator(packet(),l);family,w=x.assignments(packet(),'Q3-A3')['Q3-A3-release'];expected,_=x.next_request('Q3-A3',family,w,[]);p={'stage':'Q3-A3','trajectory':'Q3-A3-release','seq':0,'call':expected}
   self.assertEqual(v.check(p),expected['request']);bad=copy.deepcopy(p);bad['call']['packet']['history']=[]
   with self.assertRaisesRegex(ValueError,'unexpected_actor_request'):v.check(bad)
   p.update(stage='P1',trajectory='P1-release-r0')
   with self.assertRaisesRegex(ValueError,'Q3_gate'):v.check(p)
 def test_duplicate_concurrent_reservations_only_one_wins(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,True)
   def reserve(_):
    try:l.reserve('Q3-A3','Q3-A3-release',0);return 1
    except (ValueError,sqlite3.IntegrityError):return 0
   with ThreadPoolExecutor(max_workers=6) as pool:self.assertEqual(sum(pool.map(reserve,range(6))),1)
   l.settle('Q3-A3-release-0000',None);self.assertEqual(l.summary()['Q3-A3']['unknown_usd'],'0.02265')
 def test_shared_stop_prevents_reservation_and_dispatch(self):
  stop=threading.Event();stop.set()
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,False);calls=x.Calls('Q3-A3','Q3-A3-release',Path(td),{'deadline':1e20},l,stop)
   with patch('urllib.request.urlopen') as network:
    with self.assertRaisesRegex(ValueError,'shared_stop'):calls('release','question',{},'test')
    network.assert_not_called()
   self.assertEqual(l.summary()['Q3-A3']['started'],0)
 def test_full_qualification_and_six_parallel_prefix_replays(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,True);p=packet();v=x.Validator(p,l)
   def execute(stage,ident,pair):
    family,w=pair;history=[];seq=0
    while True:
     expected,result=x.next_request(stage,family,w,history)
     if expected is None:return seq,result
     payload={'stage':stage,'trajectory':ident,'seq':seq,'call':expected};self.assertEqual(v.check(payload),expected['request']);value=answer(expected);rid=l.reserve(stage,ident,seq);l.settle(rid,.001,value,1);history.append(value);seq+=1
   for ident,pair in x.assignments(p,'Q3-A3').items():n,r=execute('Q3-A3',ident,pair);self.assertTrue(r['passed']);self.assertLessEqual(n,35)
   self.assertTrue(v.qualified())
   with ThreadPoolExecutor(max_workers=6) as pool:results=list(pool.map(lambda item:execute('P1',*item),x.assignments(p,'P1').items()))
   self.assertEqual(len(results),6)
   for n,r in results:self.assertLessEqual(n,138);self.assertTrue(r['complete'])
   self.assertLessEqual(l.summary()['P1']['started'],828)
   with l.connect() as db:self.assertEqual(db.execute("SELECT status FROM r3_calls WHERE stage='Q3'").fetchone()[0],'ambiguous')
 def test_stage_cap_and_unknown_cost_preserved(self):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,True)
   for i in range(108):rid=l.reserve('Q3-A3','test',i);l.settle(rid,None)
   with self.assertRaisesRegex(ValueError,'stage_cap'):l.reserve('Q3-A3','test',108)
   self.assertEqual(l.summary()['Q3-A3']['unknown_usd'],'2.44620')
 def test_known_usage_retained_on_bad_route_and_no_retry(self):
  with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'THESEUS_V2_CAPABILITY':'test-only'}):
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,False);stop=threading.Event();r={'deadline':1e20,'source_sha256':'fixture'};calls=x.Calls('Q3-A3','Q3-A3-release',Path(td),r,l,stop)
   response={'actual_usd':.001,'error':None,'response':{'model':'wrong'}}
   with patch('urllib.request.urlopen',return_value=io.BytesIO(json.dumps(response).encode())) as network:
    with self.assertRaises(ValueError):calls('release','question',{},'fixture')
    network.assert_called_once()
   self.assertTrue(stop.is_set());self.assertEqual(l.summary()['Q3-A3']['actual_usd'],'0.001');self.assertEqual(l.summary()['Q3-A3']['unknown_usd'],'0')
 def test_unknown_usage_stops_and_retains_full_reservation(self):
  with tempfile.TemporaryDirectory() as td,patch.dict(os.environ,{'THESEUS_V2_CAPABILITY':'test-only'}):
   path=Path(td)/'db';fixture(path);l=x.Ledger(path,False);stop=threading.Event();calls=x.Calls('Q3-A3','Q3-A3-release',Path(td),{'deadline':1e20,'source_sha256':'fixture'},l,stop)
   with patch('urllib.request.urlopen',side_effect=TimeoutError()):
    with self.assertRaises(TimeoutError):calls('release','question',{},'fixture')
   self.assertTrue(stop.is_set());self.assertEqual(l.summary()['Q3-A3']['unknown_usd'],'0.02265')
if __name__=='__main__':unittest.main()
