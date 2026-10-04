"""Re-encode all native GIF frames with a shared 64-color palette for public delivery."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageSequence
p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();r=a.directory
im=Image.open(r/'replay.gif');im.seek(1);palette=im.convert('RGB').quantize(colors=64);im.seek(0);frames=[];durations=[]
for f in ImageSequence.Iterator(im):
 frames.append(f.convert('RGB').quantize(palette=palette,dither=Image.Dither.NONE));durations.append(f.info.get('duration',160))
out=r/'replay-public.gif';frames[0].save(out,save_all=True,append_images=frames[1:],duration=durations,loop=0,optimize=True)
print(json.dumps({'frames':len(frames),'bytes':out.stat().st_size,'original_bytes':(r/'replay.gif').stat().st_size,'changes':'Shared palette encoding only; same dimensions, frame order and durations.'}))
