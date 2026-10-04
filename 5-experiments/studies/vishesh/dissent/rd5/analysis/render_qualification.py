"""Render saved native qualification evidence; never constructs or invokes a model."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

p=argparse.ArgumentParser();p.add_argument('results',type=Path);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
packet=json.loads((a.results/'packet.json').read_text());summary=json.loads((a.results/'summary.json').read_text());rows=json.loads((a.results/'records.json').read_text())
assert packet['stage']=='Q5' and summary['origin']=='native-jev'
by_id={r['id']:r for r in rows};roots={}
for definition in packet['definition']:roots.setdefault(definition['root'],{})[definition['representation']]=definition
W,H=1400,1120;im=Image.new('RGB',(W,H),'#101720');draw=ImageDraw.Draw(im)
fonts=[Path('/System/Library/Fonts/Supplemental/Arial.ttf'),Path('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf')]
font=next((str(x) for x in fonts if x.exists()),None)
f=lambda size:ImageFont.truetype(font,size) if font else ImageFont.load_default()
white='#e9eff6';muted='#b3c0ce';green='#173e39';red='#522d34';gray='#27323f'
draw.text((55,38),'Does a source-preserving evidence card help Jev?',font=f(38),fill=white)
draw.text((55,99),'RD5 Q5 | Native answers | 12 authored packets, paired raw and card representations',font=f(22),fill=muted)
counts=summary['by_representation'];gate='PASS' if summary['qualification_passed'] else 'FAIL'
draw.text((55,146),f"Raw {counts['raw']['correct']}/12 correct     Card {counts['card']['correct']}/12 correct     Qualification {gate}",font=f(27),fill=white)
for x,t in ((55,'CASE'),(475,'EXPECTED'),(710,'RAW'),(1030,'CARD')):draw.text((x,211),t,font=f(20),fill=muted)
for i,(root,defs) in enumerate(roots.items()):
 y=253+i*54;d=defs['raw'];label=f"{d['domain']} / {d['condition']}"
 draw.text((55,y+10),label,font=f(20),fill=white);draw.text((475,y+10),d['expected'],font=f(20),fill=muted)
 for x,rep in ((710,'raw'),(1030,'card')):
  row=by_id.get(defs[rep]['id']);complete=row is not None and row['status']=='completed'
  correct=complete and row['action']==defs[rep]['expected']
  label=row['action'] if complete else ('FAILED' if row else 'UNSTARTED')
  draw.rounded_rectangle((x-10,y,x+250,y+44),radius=6,fill=green if correct else red if complete else gray)
  draw.text((x+5,y+9),label+('  correct' if correct else '  wrong' if complete else ''),font=f(20),fill=white)
notes=[f"Complete valid responses: {summary['valid_responses']}/24. Card qualification requires 12/12 correct and all 24 valid.",
       'Raw scores are diagnostic; representation and gate were fixed before native answers.',
       'Finite same-author semantic templates. Paired observations are not 24 independent tasks.',
       'A failed gate stops H5. This screen does not establish swarm efficacy or generalization.']
for i,t in enumerate(notes):draw.text((55,943+i*33),t,font=f(20),fill=muted)
a.output.parent.mkdir(parents=True,exist_ok=True);im.save(a.output)
print(json.dumps({'rendered':str(a.output),'native_rows':len(rows),'assigned':24}))
