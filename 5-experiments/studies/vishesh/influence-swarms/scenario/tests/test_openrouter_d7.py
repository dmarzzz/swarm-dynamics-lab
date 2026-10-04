import hashlib,importlib.util,json,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock
BASE=Path(__file__).resolve().parents[1];sys.path.insert(0,str(BASE/'analysis'))
import openrouter_d7 as m
import acquisition_d7_run as runner
class RouteTests(unittest.TestCase):
 def good(self):return {'model':m.MODEL,'provider':'Anthropic','choices':[{'finish_reason':'stop','message':{'content':'{}'}}],'usage':{'prompt_tokens':12,'completion_tokens':5,'cost':.000037}}
 def test_packet_prompt_preservation(self):
  old=json.loads((BASE/'reviews/D6-acquisition-packet.json').read_text());new=runner.verify_packet(json.loads(runner.PACKET.read_text()))
  for a,b in zip(old['requests'],new['requests']):
   self.assertEqual(m.wire_from_d6(a['wire_body']),b['wire_body']);self.assertEqual(a['request'],b['request'])
 def test_no_fallback_or_mutated_route(self):
  for key,value in [('provider',{}),('reasoning',{'enabled':True}),('model','different')]:
   p=json.loads(runner.PACKET.read_text());p['requests'][0]['wire_body'][key]=value
   raw=json.dumps(p['requests'][0]['wire_body']).encode();p['requests'][0].update(wire_sha256=hashlib.sha256(raw).hexdigest(),wire_bytes=len(raw))
   with self.assertRaises(AssertionError):runner.verify_packet(p)
 def test_normalization_and_identity(self):
  r=m.normalize(self.good());m.verify_route(r);self.assertEqual(r['usage']['input_tokens'],12);self.assertEqual(r['provider_cost_usd'],.000037)
  for key in ('model','provider'):
   value=self.good();value[key]='other'
   with self.assertRaises(AssertionError):m.verify_route(m.normalize(value))
 def test_truncation_missing_cost_error(self):
  r=self.good();r['choices'][0]['finish_reason']='length';self.assertEqual(m.normalize(r)['stop_reason'],'incomplete')
  r=self.good();del r['usage']['cost'];self.assertIsNone(m.normalize(r)['provider_cost_usd'])
  with self.assertRaises(AssertionError):m.normalize({'error':{'message':'private'}})
 def test_relay_exact_order_duplicates_and_total(self):
  p=json.loads(runner.PACKET.read_text());raw=[json.dumps(i['wire_body']).encode() for i in p['requests']]
  with tempfile.TemporaryDirectory() as d:
   relay=m.Relay(p,Path(d)/'relay');send=Mock(return_value=b'{}')
   relay.send(raw[0],send);relay.send(raw[1],send)
   with self.assertRaises(ValueError):relay.send(raw[1],send)
   self.assertEqual(send.call_count,2)
   with self.assertRaises(FileExistsError):m.Relay(p,Path(d)/'relay')
  for first in (raw[1],b'wrong'):
   with tempfile.TemporaryDirectory() as d:
    relay=m.Relay(p,Path(d)/'relay');send=Mock(return_value=b'{}')
    with self.assertRaises(ValueError):relay.send(first,send)
    with self.assertRaises(ValueError):relay.send(raw[0],send)
    send.assert_not_called()
 def test_relay_failure_no_retry(self):
  p=json.loads(runner.PACKET.read_text());raw=json.dumps(p['requests'][0]['wire_body']).encode()
  with tempfile.TemporaryDirectory() as d:
   relay=m.Relay(p,Path(d)/'relay');send=Mock(side_effect=TimeoutError('private'))
   with self.assertRaises(TimeoutError):relay.send(raw,send)
   with self.assertRaises(ValueError):relay.send(raw,send)
   self.assertEqual(send.call_count,1);self.assertTrue((Path(d)/'relay/1.start').exists())
 def test_two_contracts_and_usage_failure_stop(self):
  import sqlite3
  from contextlib import closing
  from typed_diagnostic import FixturePolicy,scripted
  p=json.loads(runner.PACKET.read_text())
  for missing in (False,True):
   with tempfile.TemporaryDirectory() as d:
    root=Path(d);dbpath=root/'budget'
    with closing(sqlite3.connect(dbpath)) as db,db:
     db.execute('CREATE TABLE budget(id INTEGER PRIMARY KEY,cap REAL,reserved REAL,calls INTEGER)');db.execute('INSERT INTO budget VALUES(1,8,4.917472,247)')
    answers=[FixturePolicy().complete(i['request'],scripted) for i in p['requests']]
    def send(raw):
     r=self.good();r['choices'][0]['message']['content']=json.dumps(answers.pop(0))
     if missing:del r['usage']['cost']
     return json.dumps(r).encode()
    result=runner.collect(p,root/'out',dbpath,send)
    self.assertEqual(result['valid'],0 if missing else 2)
    self.assertEqual(result['unstarted'],1 if missing else 0)
    if missing:self.assertEqual(result['failures'][0]['category'],'missing_or_invalid_cost')
    else:self.assertAlmostEqual(result['actual_usd'],.000074)
    self.assertIn('choices',json.loads((root/'out/01-response.bin').read_text()))
