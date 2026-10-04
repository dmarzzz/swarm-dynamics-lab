import json,tempfile,unittest
from pathlib import Path
from unittest.mock import Mock,patch
from provider import native_payload
from openrouter_route import MODEL,ROUTE,charge,settle,request_child
from tasks import generate
from response_contract import schema_for
from budget import Budget

class OpenRouterTests(unittest.TestCase):
    def test_actual_payload_preserves_exact_phase_schemas(self):
        cfg=json.loads((Path(__file__).parent.parent/'input-binding-config.json').read_text())
        public=generate('evidence','chain',6,width=16).public
        for phase,item in [('plan',None),('plan_repair',None),('integrate',None),('work',public['items'][0])]:
            b=native_payload([{'role':'system','content':'instruction'},{'role':'user','content':'task'}],cfg,phase,public,item)
            self.assertEqual(b['model'],MODEL);self.assertEqual(b['provider'],ROUTE)
            self.assertEqual(b['response_format']['json_schema']['schema'],schema_for(public,phase,item))
            self.assertEqual(b['messages'][0],{'role':'system','content':'instruction'})
            self.assertNotIn('system',b);self.assertNotIn('output_config',b)
    def test_child_never_uses_remote_url_or_credentials(self):
        for url in (None,'https://openrouter.ai/api/v1/chat/completions','http://example.invalid/invoke'):
            c=Mock()
            with patch('openrouter_route.os.environ.get',return_value=url),patch('openrouter_route.urllib.request.urlopen') as transport:request_child(c,{},1);transport.assert_not_called()
            self.assertEqual(c.send.call_args.args[0],{'ok':False,'failure':'credential_unavailable'})
    def test_fee_uncertainty_carries_forward(self):
        with tempfile.TemporaryDirectory() as t:
            b=Budget(Path(t)/'ledger',20_000_000,'q-a7',2_000_000);b.reserve('a','ep',242528,2_000_000)
            actual=charge({'prompt_tokens':100,'completion_tokens':20,'cost':.0002});settle(b,'a',actual)
            self.assertEqual(b.exposure('ep'),220)
            with b.connect() as db:self.assertEqual(db.execute('SELECT SUM(actual),SUM(held) FROM calls').fetchone(),(200,220))

if __name__=='__main__':unittest.main()
