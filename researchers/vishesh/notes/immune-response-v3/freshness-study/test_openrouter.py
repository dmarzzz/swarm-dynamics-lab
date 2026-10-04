import json,tempfile,sqlite3,os,unittest
from pathlib import Path
from unittest.mock import patch
import freshness
from openrouter_provider import OpenRouterPolicy,wire,validate_wire,MODEL
from test_trace import Reply
class RoutingTests(unittest.TestCase):
 def test_route_and_fallback_rejected(self):
  b=wire({'instructions':'fixture','observation':{},'response_schema':{'type':'object'}});validate_wire(b);b['provider']['allow_fallbacks']=True
  try:
   with self.assertRaises(AssertionError):validate_wire(b)
  finally:b['provider']['allow_fallbacks']=False
 def run_reply(self,reply):
  with tempfile.TemporaryDirectory() as td:
   path=Path(td);ledger=path/'ledger.sqlite'
   with sqlite3.connect(ledger) as db:
    db.execute('create table budget(id integer primary key,cap real,reserved real,calls integer)');db.execute('insert into budget values(1,8,3.185495,388)');db.execute('CREATE TABLE immune_requests (request_id TEXT PRIMARY KEY, run_id TEXT, request_hash TEXT, state TEXT, reserved_usd REAL, input_tokens INTEGER, output_tokens INTEGER, actual_usd REAL, started REAL, ended REAL)')
   env={'SWARM_BUDGET_LEDGER':str(ledger),'SWARM_ATTEMPT_ID':'freshness-a5','SWARM_USAGE_LOG':str(path/'usage.jsonl'),'SWARM_MODEL_CONFIG_FILE':str(Path(__file__).with_name('model-config.json')),'SWARM_MODEL_BASE_URL':'http://127.0.0.1:18765'}
   with patch.dict(os.environ,env,clear=True):p=OpenRouterPolicy()
   with patch('urllib.request.urlopen',return_value=Reply(reply)) as call:
    try:answer=p.complete({'instructions':'fixture','observation':{},'response_schema':{'type':'object'}},None)
    except ValueError:answer=None
    self.assertEqual(call.call_count,1);self.assertNotIn('Authorization',dict(call.call_args.args[0].header_items()))
   return answer,json.loads((path/'usage.jsonl').read_text()),(path/'transport.jsonl').read_text()
 def test_cost_recorded_before_malformed_answer(self):
  a,u,t=self.run_reply({'model':MODEL,'provider':'Anthropic','usage':{'prompt_tokens':10,'completion_tokens':2,'cost':.00002},'choices':[{'finish_reason':'stop','message':{'content':'not-json'}}]});self.assertIsNone(a);self.assertEqual(u['actual_usd'],.00002);self.assertIn('not-json',t)
 def test_missing_cost_fails_closed(self):
  a,u,t=self.run_reply({'model':MODEL,'provider':'Anthropic','usage':{'prompt_tokens':10,'completion_tokens':2},'choices':[{'finish_reason':'stop','message':{'content':'{}'}}]});self.assertIsNone(a);self.assertIsNone(u['actual_usd'])
 def test_valid_native_contract(self):
  a,u,t=self.run_reply({'model':MODEL,'provider':'Anthropic','usage':{'prompt_tokens':10,'completion_tokens':2,'cost':.00002},'choices':[{'finish_reason':'stop','message':{'content':'{"ok":true}'}}]});self.assertEqual(a,{'ok':True})
if __name__=='__main__':unittest.main()
