import tempfile,unittest,urllib.error
from pathlib import Path
from unittest.mock import patch
import pool_structured as n

class NativeTests(unittest.TestCase):
    def test_root_blocks(self):
        spec=n.read_spec('split-sonnet-no-links-strong-native-json',False)
        aa=n.assignments(spec)
        self.assertEqual({a['task'] for a in aa[:12]},{5141,5146})
        for i in range(12,204,4):self.assertEqual(len({(a['family'],a['task']) for a in aa[i:i+4]}),1)
    def test_bounded_429_only(self):
        spec={'id':'test','model':'claude-sonnet-4-6','route':'anthropic-pool'}
        a={'id':'Q-test','packet':{},'stage':'Q'}
        for status,attempts in [(429,3),(403,1),(500,1)]:
            with tempfile.TemporaryDirectory() as d,patch.object(n.f,'ROOT',Path(d)):
                (Path(d)/'results/test').mkdir(parents=True)
                error=urllib.error.HTTPError('http://local',status,'refused',{},None)
                with patch('pool_structured.urllib.request.urlopen',side_effect=error) as request,patch('pool_structured.time.sleep') as sleep:
                    r=n.call(spec,a,'test-key')
                self.assertEqual(request.call_count,attempts)
                self.assertEqual(len(r['transport_attempts']),attempts)
                self.assertEqual(sleep.call_count,attempts-1)
if __name__=='__main__':unittest.main()
