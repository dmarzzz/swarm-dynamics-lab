"""Render operational reconciliation, never native answer accuracy."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
root=Path(__file__).resolve().parents[1];base=root/'results/activation-a1'
s=json.loads((base/'summary.json').read_text());m=json.loads((base/'manifest.json').read_text())
assert s['origin']=='operator_reconciliation_no_native_execution' and len(m)==24
assert all(r['status']=='unstarted' for r in m)
font=next(str(p) for p in [Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')] if p.exists())
f=lambda n:ImageFont.truetype(font,n)
im=Image.new('RGB',(1400,820),'#111b26');d=ImageDraw.Draw(im);white='#e4edf5';muted='#b9c8d7';amber='#f2ca7b'
d.text((55,35),'RD5 stopped before experimental execution',font=f(42),fill=white)
d.text((55,102),'Q5-A1 relay activation | Reconciled 4 October 2026 | No native result',font=f(24),fill=muted)
for i,r in enumerate(m):
 x=60+(i%12)*108;y=199+(i//12)*95
 d.rounded_rectangle((x,y,x+90,y+69),radius=7,fill='#314457',outline='#64798d',width=2)
 d.text((x+14,y+18),str(i+1).zfill(2),font=f(27),fill=white)
d.text((55,386),'24 frozen requests    0 started    0 responses    24 unstarted',font=f(29),fill=amber)
d.text((55,435),'Gray cells are unstarted assignments, not wrong answers. Qualification is unknown.',font=f(22),fill=muted)
for x,title,detail in [(55,'08:44','Relay healthy'),(390,'09:14','Relay expired'),(730,'15:19','No worker / no outputs'),(1100,'15:20','Claim released')]:
 d.line((x,529,x+190,529),fill='#5b768f',width=4)
 d.text((x,558),title+' UTC',font=f(24),fill=white)
 d.text((x,598),detail,font=f(19),fill=muted)
d.text((55,677),'New API calls: 0   |   Original API exposure: $0.02065245   |   H5 not admitted',font=f(23),fill=white)
d.text((55,724),'Next gate: central launch acknowledgement, then fresh dedicated allocation and Q5-A2 admission.',font=f(21),fill=muted)
im.save(base/'dispatch-closeout.png')
print('Saved operational status figure; no model accuracy is plotted.')
