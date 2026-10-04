import copy,io,json,sqlite3,unittest
from contextlib import closing
from unittest.mock import patch
from openrouter import wire,decode,OR_MODEL
from design import assignments,execution_request
from relay import allowlist,digest,reserve
from runner import invoke

def answer():return {'model':OR_MODEL,'provider':'Anthropic','choices':[{'message':{'content':'{}'},'finish_reason':'stop'}],'usage':{'prompt_tokens':100,'completion_tokens':5,'cost':.000125}}
class OpenRouterTests(unittest.TestCase):
    def test_translation_content_and_schema(self):
        for a in assignments():
            b=a['request'] if a['kind']=='learn' else execution_request(a,a['rule']);w=wire(b)
            self.assertEqual(w['messages'][0]['content'],b['system']);self.assertEqual(w['messages'][1:],b['messages'])
            self.assertEqual(w['response_format']['json_schema']['schema'],b['output_config']['format']['schema'])
            self.assertFalse(w['provider']['allow_fallbacks']);self.assertEqual(w['provider']['only'],['anthropic'])
    def test_success_and_cost(self):
        r=decode(answer());self.assertIsNone(r['error']);self.assertTrue(r['response_received']);self.assertEqual(r['actual_usd'],.000125)
    def test_wrong_route_and_bad_usage(self):
        for key,value in [('provider','Amazon Bedrock'),('model','wrong')]:
            d=answer();d[key]=value;self.assertEqual(decode(d)['error'],'served_route_mismatch')
        for cost in (None,-1,True,float('nan')):
            d=answer();d['usage']['cost']=cost;self.assertEqual(decode(d)['error'],'usage_missing')
    def test_truncation_and_invalid_json(self):
        d=answer();d['choices'][0]['finish_reason']='length';self.assertEqual(decode(d)['error'],'incomplete_output')
        d=answer();d['choices'][0]['message']['content']='not json';r=decode(d);self.assertIsNone(r['value']);self.assertIsNone(r['error'])
    def test_once_only_reservation_and_cap(self):
        with closing(sqlite3.connect(':memory:')) as db:
            db.execute('CREATE TABLE calls(id TEXT PRIMARY KEY,reserved REAL,status TEXT,cost REAL)');reserve(db,'one',1.5)
            with self.assertRaises(sqlite3.IntegrityError):reserve(db,'one',.1)
            with self.assertRaises(ValueError):reserve(db,'two',1.1)
            self.assertEqual(db.execute('SELECT count(*) FROM calls').fetchone()[0],1)
    def test_frozen_allowlist(self):
        allowed=allowlist();self.assertEqual(len(allowed),204)
        a=assignments()[0];self.assertIn(digest(a['request']),allowed[a['id']])
        b=copy.deepcopy(a['request']);b['temperature']=1;self.assertNotIn(digest(b),allowed[a['id']])
    def test_worker_uses_only_local_relay_once(self):
        r=decode(answer());response=io.BytesIO(json.dumps(r).encode())
        with patch.dict('os.environ',{'THESEUS_ASSIGNMENT':'FIXTURE'}),patch('urllib.request.urlopen',return_value=response) as call:
            result=invoke({},'FIXTURE-CAPABILITY',1)
        call.assert_called_once();self.assertTrue(call.call_args.args[0].full_url.startswith('http://127.0.0.1:18462/'));self.assertIsNone(result['error'])
if __name__=='__main__':unittest.main()
