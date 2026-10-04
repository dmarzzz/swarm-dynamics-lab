"""Replay measured terminal transitions; fixed event cadence, not original wall time."""
import argparse,json,sys,tempfile
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).parent));from approval_review import render
p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('out');a=p.parse_args();root=Path(a.root);rows=[];frames=[]
with tempfile.TemporaryDirectory() as directory:
 frame=Path(directory)/'frame.png';render([],frame);frames.append(Image.open(frame).copy())
 for ep in sorted(root.glob('events-*.jsonl'),key=lambda p:int(p.stem.split('-')[1])):
  for line in ep.read_text().splitlines():
   e=json.loads(line)
   if e['kind']=='terminal':rows.append(e['outcome']);render(rows,frame);frames.append(Image.open(frame).copy())
 assert rows==json.loads((root/'outcomes.json').read_text())
 frames[0].save(a.out,save_all=True,append_images=frames[1:],duration=[800]*(len(frames)-1)+[5000],loop=0,optimize=True)
print(json.dumps({'frames':len(frames),'terminal':len(rows),'cadence':'fixed event playback; original timestamps in JSONL'}))
