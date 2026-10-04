import io,json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
import structured as s

class StructuredTest(unittest.TestCase):
    def test_fresh_roots_and_success(self):
        spec=s.read_spec('split-sonnet-linked-strong-or-json',False)
        aa=s.assignments(spec)
        self.assertEqual({a['task'] for a in aa if a['stage']=='Q'},{5140,5145})
        a=aa[0]
        data={'model':spec['model'],'provider':'Anthropic','usage':{'cost':.01,'prompt_tokens':100,'completion_tokens':30},
              'choices':[{'finish_reason':'stop','message':{'content':json.dumps({'values':a['expected']})}}]}
        seen=[]
        def urlopen(req,timeout):
            body=json.loads(req.data);seen.append(body)
            self.assertTrue(body['response_format']['json_schema']['strict'])
            self.assertEqual(body['response_format']['json_schema']['schema']['additionalProperties'],False)
            return io.BytesIO(json.dumps(data).encode())
        with tempfile.TemporaryDirectory() as d,patch.object(s,'LEDGER',s.Ledger(Path(d)/'ledger')):
            with patch.object(s.f,'enforce_launch_hold'),patch('structured.urllib.request.urlopen',side_effect=urlopen):r=s.call(spec,a,'test-key')
            self.assertEqual(r['status'],'completed');self.assertTrue(r['exact'])
            self.assertAlmostEqual(s.LEDGER.accounted(spec['id']),.01)
        self.assertEqual(len(seen),1)
if __name__=='__main__':unittest.main()
