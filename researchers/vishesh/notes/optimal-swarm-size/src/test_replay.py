import json
from pathlib import Path
import tempfile
import unittest
from replay import render
class Replay(unittest.TestCase):
    def test_recorded_intervals_missing_ends_and_escaping(self):
        with tempfile.TemporaryDirectory() as temp:
            trace=Path(temp)/'trace.jsonl';output=Path(temp)/'replay.html'
            trace.write_text('\n'.join(json.dumps(e) for e in [
                {'t':1,'kind':'service_start','actor':0,'phase':'work','item':'</script><script>alert(1)</script>'},
                {'t':3,'kind':'service_end','actor':0,'phase':'work','item':'</script><script>alert(1)</script>'},
                {'t':4,'kind':'service_start','actor':1,'phase':'integrate','item':None},
                {'t':5,'kind':'terminal'}]))
            segments=render(trace,output)
            self.assertEqual(segments[0]['end']-segments[0]['start'],2)
            self.assertIsNone(segments[1]['end']);self.assertTrue(segments[1]['incomplete'])
            self.assertNotIn('</script><script>alert(1)',output.read_text())
if __name__=='__main__':unittest.main()
