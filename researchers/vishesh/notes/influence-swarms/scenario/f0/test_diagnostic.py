import copy,json,unittest
import diagnostic as d
class Test(unittest.TestCase):
 def wire(self):return {'model':d.i.MODEL,'provider':{'only':['openai'],'order':['openai'],'allow_fallbacks':False,'require_parameters':True,'max_price':{'prompt':.1,'completion':.5}},'max_tokens':3072,'messages':[{'role':'system','content':'original'},{'role':'user','content':'frozen facts'}],'response_format':{'json_schema':{'strict':True,'schema':{'type':'object','properties':{'s':{'type':'string','maxLength':120,'pattern':'^[ -~]*$'},'e':{'type':'string','enum':['a','b']}}}}}}
 def test_matrix_and_isolation(self):
  w=self.wire();contexts={k:{'wire':w,'case_id':k} for k in ('failed','unaffected')};old=copy.deepcopy(contexts);rows=d.compile_packet(contexts)
  self.assertEqual(contexts,old);self.assertEqual(len(rows),12)
  for condition in d.CONDITIONS:self.assertEqual([r['context'] for r in rows if r['condition']==condition],['failed','failed','unaffected'])
  for row in rows:
   self.assertEqual(row['wire']['messages'][1],w['messages'][1]);self.assertEqual(row['wire']['provider'],w['provider']);self.assertNotIn('wire',d.public_manifest(rows)['rows'][0])
 def test_relax_only_text_constraints(self):
  w=self.wire();before=copy.deepcopy(w);d.relax(w['response_format']['json_schema']['schema']);self.assertEqual(w['response_format']['json_schema']['schema']['properties']['s'],{'type':'string'});self.assertEqual(w['response_format']['json_schema']['schema']['properties']['e'],before['response_format']['json_schema']['schema']['properties']['e'])
 def test_usage_stops(self):
  for usage in ({},{'prompt_tokens':1,'completion_tokens':1,'cost':1}):
   with self.assertRaises(ValueError):d.assess({'usage':usage},None)
 def test_length_is_endpoint(self):
  b={'usage':{'prompt_tokens':2,'completion_tokens':3072,'cost':.002},'model':d.i.MODEL,'provider':'OpenAI','choices':[{'finish_reason':'length','message':{'content':'{"a":"x"   '}}]};r=d.assess(b,None);self.assertFalse(r['local_valid']);self.assertEqual(r['trailing_whitespace'],3)
 def test_relax_not_local_validation(self):
  case=json.loads((d.H.parent/'b2/dossiers.json').read_text())[0]
  with self.assertRaises(ValueError):d.i.decode('{}',case,True)
 def test_oversize_fails(self):
  w=self.wire();w['messages'][1]['content']='x'*40000
  with self.assertRaises(AssertionError):d.compile_packet({k:{'wire':w,'case_id':k} for k in ('failed','unaffected')})
class WorkerTest(unittest.TestCase):
 def test_known_format_failure_continues_and_transport_stops(self):
  import f0_worker as worker
  import tempfile,sqlite3
  from pathlib import Path
  original=worker.LEDGER
  for transport_failure in (False,True):
   with tempfile.TemporaryDirectory() as temp:
    worker.LEDGER=Path(temp)/'budget.sqlite'
    with sqlite3.connect(worker.LEDGER) as db:
     db.execute('CREATE TABLE budget(id INTEGER,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,50,9.907296,930)')
     db.execute('CREATE TABLE b1_scope(packet_sha256 TEXT,maximum_model REAL,model_debited REAL,hosting_reserved REAL,status TEXT)');db.execute('INSERT INTO b1_scope VALUES(?,9.805824,.77824,.5,"funded")',(worker.PARENT,))
     db.execute('CREATE TABLE b1_dispatch(attempt TEXT,ordinal INTEGER,wire_sha256 TEXT,reserved REAL,status TEXT,cost REAL,PRIMARY KEY(attempt,ordinal))')
    rows=[{'ordinal':n,'wire':{},'wire_sha256':d.sha(b'{}'),'case_id':'b2-cost-0'} for n in range(1,13)]
    def transport(raw,n):
     if transport_failure:raise RuntimeError('simulated')
     return json.dumps({'usage':{'prompt_tokens':2,'completion_tokens':3,'cost':.00001},'model':d.i.MODEL,'provider':'OpenAI','choices':[{'finish_reason':'length','message':{'content':'  '}}]}).encode()
    a={'attempt':'test','budget':[50,9.907296,930],'manifest_sha256':'test','authority':'test','until':'2099-01-01T00:00:00+00:00'}
    old_sleep=worker.time.sleep;worker.time.sleep=lambda _:None
    try:summary=worker.run(a,rows,Path(temp)/'out',transport)
    finally:worker.time.sleep=old_sleep
    self.assertEqual(summary['calls'],1 if transport_failure else 12);self.assertEqual(summary['valid_calls'],0);self.assertEqual(summary['usage_missing'],1 if transport_failure else 0);self.assertEqual(summary['complete'],not transport_failure)
    self.assertAlmostEqual(summary['budget_after'][1],9.907296+summary['calls']*d.RESERVE)
  worker.LEDGER=original
if __name__=='__main__':unittest.main()
