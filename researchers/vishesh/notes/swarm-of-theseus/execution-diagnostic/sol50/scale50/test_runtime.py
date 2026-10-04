import copy,json,sqlite3,tempfile,unittest
from unittest.mock import patch
from pathlib import Path
import scale_runtime as r,scale_contract as c,scale_study as s

class RuntimeTests(unittest.TestCase):
 def test_operational_amendment_preserves_exact_scientific_closure(self):
  receipt={'source_sha256':'operational-successor','qualification':{'source_sha256':r.Q50_SOURCE},'operational_amendment':'explicit-sqlite-close-only'}
  self.assertEqual(r.scientific_hash(),r.Q50_SCIENCE);self.assertTrue(r.qualification_source_matches(receipt))
  with patch.object(r,'scientific_hash',return_value='changed-actor-wire'):
   self.assertFalse(r.qualification_source_matches(receipt))
  receipt['qualification']['source_sha256']='unqualified-other';self.assertFalse(r.qualification_source_matches(receipt))
 def test_connections_close_on_success_and_rollback_without_gc(self):
  original=sqlite3.connect;opened=[]
  class Tracked(sqlite3.Connection):
   def close(self):self.closed=True;return super().close()
  def connect(*args,**kwargs):
   value=original(*args,**kwargs,factory=Tracked);value.closed=False;opened.append(value);return value
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'ledger.sqlite';db=original(p);db.close()
   with patch.object(r.sqlite3,'connect',connect):
    l=r.Ledger(p,'Q50');self.assertTrue(all(x.closed for x in opened))
    body=c.wire('commit','failover',{})
    for i in range(60):
     ident=l.reserve(i,body);self.assertTrue(all(x.closed for x in opened))
     with self.assertRaisesRegex(ValueError,'sequence'):l.reserve(i,body)
     self.assertTrue(all(x.closed for x in opened));l.settle(ident,.001,{},.1);self.assertTrue(all(x.closed for x in opened))
    with self.assertRaisesRegex(ValueError,'stage_cap'):l.reserve(60,body)
    self.assertTrue(all(x.closed for x in opened))
    with self.assertRaisesRegex(ValueError,'terminal'):l.settle('Q50-0000',.001,{},.1)
    self.assertTrue(all(x.closed for x in opened));self.assertEqual(len(l.rows()),60)
 def test_mirror_matches_every_qualification_request(self):
  m=r.Mirror('Q50');count=0
  def call(family,phase,p,condition):
   nonlocal count
   expected=m.next();self.assertEqual(expected,{'family':family,'phase':phase,'packet':p,'condition':condition,'request':c.wire(phase,family,p)})
   answer=s.scripted(family,phase,p,condition);m.answer(answer);count+=1;return c.to_engine(phase,answer)
  result=s.qualify(call);self.assertEqual(m.next(),{'terminal':result});self.assertTrue(result['passed']);self.assertLessEqual(count,60)

 def test_original_rows_preserved_duplicate_ambiguity_and_cap(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'original.sqlite';db=sqlite3.connect(p)
   for table in ('calls','r3_calls','r3_successor'):
    db.execute('CREATE TABLE '+table+' (id TEXT, value TEXT)');db.execute('INSERT INTO '+table+' VALUES(?,?)',('historical','preserve'))
   db.commit();db.close();before=r.historical_hash(p);l=r.Ledger(p,'Q50');body=c.wire('commit','failover',{})
   ident=l.reserve(0,body)
   with self.assertRaisesRegex(ValueError,'sequence'):l.reserve(0,body)
   l.settle(ident,None,None,1)
   with self.assertRaisesRegex(ValueError,'sequence'):l.reserve(1,body)
   self.assertEqual(r.historical_hash(p),before);self.assertEqual(l.rows()[0][1:4],('0.0364',None,'ambiguous'))
   with self.assertRaisesRegex(ValueError,'terminal'):l.settle(ident,0.001,{},1)
   other=r.Ledger(p,'S50')
   with self.assertRaisesRegex(ValueError,'sequence'):other.reserve(0,body)
   fresh=Path(tmp)/'cap.sqlite';sqlite3.connect(fresh).close();other=r.Ledger(fresh,'S50')
   for i in range(c.CAPS['S50']):
    key=other.reserve(i,body);other.settle(key,.001,{},.01)
   with self.assertRaisesRegex(ValueError,'stage_cap'):other.reserve(1150,body)
   self.assertEqual(r.historical_hash(p),before)

 def test_native_route_and_shape(self):
  value={'response':{'model':'gpt-6-sol','provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'content':'{"note":{"witnesses":["position_01","position_02"]},"decision":"defer"}'}}]}}
  # Parsing preserves the extra field for the strict semantic engine to reject.
  self.assertIn('decision',r.parse(value))
  bad=copy.deepcopy(value);bad['response']['choices'][0]['finish_reason']='length'
  with self.assertRaisesRegex(ValueError,'incomplete'):r.parse(bad)
  bad=copy.deepcopy(value);bad['response']['provider']='other'
  with self.assertRaisesRegex(ValueError,'route'):r.parse(bad)

 def test_admission_rejects_unfunded_scope(self):
  with self.assertRaisesRegex(ValueError,'funding'):
   r.admit({'stage':'Q50','packet_sha256':c.digest(s.packet()),'source_sha256':r.source_hash(),'plan_sha256':r.hashlib.sha256((r.ROOT/'PLAN.md').read_bytes()).hexdigest()},'/absent',now=1)

if __name__=='__main__':unittest.main()
