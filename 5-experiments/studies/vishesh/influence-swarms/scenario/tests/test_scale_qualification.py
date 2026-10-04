import json,sys,tempfile,sqlite3,unittest,copy
from pathlib import Path
from contextlib import closing
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import scale_qualification as sq
from scale_acquisition import Session,AcquisitionStopped
from study import scripted
import typed_diagnostic as td

def response(item):
 o=json.loads(item['wire_body']['messages'][1]['content']);a=td.fixture_answer(o) if item['role']=='auditor' else scripted(o)
 return {'model':item['wire_body']['model'],'provider':'OpenAI','usage':{'prompt_tokens':10,'completion_tokens':20,'cost':.000001},'choices':[{'finish_reason':'stop','message':{'content':json.dumps(a)}}]}
class ScaleTests(unittest.TestCase):
 def test_frozen_primary_records_and_budget(self):
  for stage in sq.MODELS:
   p=sq.build(stage);self.assertEqual(p,json.loads((BASE/f'reviews/{stage}-packet.json').read_text()));self.assertEqual(9,len(p['requests']))
   for i in p['requests']:
    o=json.loads(i['wire_body']['messages'][1]['content']);self.assertFalse(any(d['kind']=='comparison' for d in o['documents']));self.assertNotIn('evaluator',o);self.assertNotIn('reports',o)
    parent=sq.saved()[i['case_id']][0]['request']['observation'];original={d['id']:d['text'] for d in parent['documents'] if d['kind']!='comparison'};self.assertEqual(original,{d['id']:d['text'] for d in o['documents']})
    self.assertLessEqual(i['wire_bytes'],32768 if i['role']=='auditor' else 9216)
 def test_wrong_route_rejected(self):
  i=sq.build('SQ-SOL')['requests'][0];r=sq.normalize(response(i));r['route']['provider']='Other'
  with self.assertRaises(AssertionError):sq.validator(i)(r)
 def test_qualification_rejects_wrong_raw_chair(self):
  p=sq.build('SQ-LUNA');rows=[]
  for i in p['requests']:rows.append({'status':'valid','answer':sq.validator(i)(sq.normalize(response(i)))})
  summary={'assignments':rows,'usage_missing':0};self.assertTrue(sq.grade(p,summary)['qualified'])
  rows[2]['answer']['choice']='Birch';self.assertFalse(sq.grade(p,summary)['qualified'])
 def test_reserves_before_failure_and_refuses_retry(self):
  with tempfile.TemporaryDirectory() as d:
   db=Path(d)/'budget.sqlite'
   with closing(sqlite3.connect(db)) as c,c:c.execute('CREATE TABLE budget (id,cap,reserved,calls)');c.execute('INSERT INTO budget VALUES (1,8,5.987552,269)')
   p=sq.build('SQ-LUNA');i=p['requests'][0];s=Session(Path(d)/'run',db,maximum_requests=9)
   def fail(raw):raise TimeoutError()
   with self.assertRaises(AcquisitionStopped):s.dispatch(sq.encode(i['wire_body']),fail,sq.validator(i),i['maximum_reservation_usd'],input_rate=.1,output_rate=.5,response_adapter=sq.normalize)
   with closing(sqlite3.connect(db)) as c:self.assertEqual(270,c.execute('SELECT calls FROM budget').fetchone()[0])
   with self.assertRaises(AcquisitionStopped):s.dispatch(sq.encode(i['wire_body']),fail,sq.validator(i),i['maximum_reservation_usd'],input_rate=.1,output_rate=.5,response_adapter=sq.normalize)
 def test_nonapproved_rates_fail_before_dispatch(self):
  with tempfile.TemporaryDirectory() as d:
   db=Path(d)/'b';db.touch();s=Session(Path(d)/'r',db);i=sq.build('SQ-SOL')['requests'][0]
   with self.assertRaises(AcquisitionStopped):s.dispatch(sq.encode(i['wire_body']),lambda _:self.fail('transport must not run'),sq.validator(i),i['maximum_reservation_usd'])
