import sys,tempfile,unittest,json
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
try:
 from PIL import Image
 from live_render import render
 AVAILABLE=True
except ImportError:AVAILABLE=False
@unittest.skipUnless(AVAILABLE,'Pillow required for renderer checks')
class Render(unittest.TestCase):
 def test_missing_frame_and_gif(self):
  with tempfile.TemporaryDirectory() as d:
   rows=[{'id':'fixture-1','seed':200,'status':'failed'},{'id':'fixture-2','seed':201,'status':'failed'}]
   render(rows,Path(d),'Q0',fixture=True)
   with Image.open(Path(d)/'final_frame.png') as im:
    self.assertEqual(im.size,(1600,1000));self.assertEqual(im.getpixel((832,202)),(86,97,106))
   with Image.open(Path(d)/'replay.gif') as im:self.assertEqual(im.n_frames,2)
   m=json.loads((Path(d)/'replay-manifest.json').read_text());self.assertEqual(m['mode'],'software fixture');self.assertEqual(len(m['frame_ids']),2)
