import json,sys
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from matplotlib import font_manager
p=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);m=json.loads((p/'manifest.json').read_text());fontpath=font_manager.findfont('DejaVu Sans');fonts={n:ImageFont.truetype(fontpath,n) for n in (14,17,19,22,28,36)};labels={'SUPPORT':'+','REFUTE':'−','UNCERTAIN':'?'}
for a in m['assignments']:
 if a['status']!='completed':continue
 w=json.loads((p/(a['id']+'.json')).read_text());f=w['frames'][-1];im=Image.new('RGB',(1600,820),'#101716');d=ImageDraw.Draw(im)
 d.text((45,25),'Healing Helping Hands · recorded final frame',fill='#edf4e9',font=fonts[36]);d.text((45,79),f"Seed {a['seed']} · {a['arm']} · {a['policy']} · {a['scenario']} · round 23/23",fill='#aebeb3',font=fonts[22]);d.text((45,125),f"Atlas accuracy {f['atlas_accuracy']:.0%}   |   Local accuracy {f['local_accuracy']:.1%}   |   Stale citations {f['stale_fraction']:.1%}",fill='#edf4e9',font=fonts[28])
 for i,label in enumerate(f['local']):
  x=45+i%20*36;y=195+i//20*36;fill='#436552' if f['correct'][i] else '#834f41';d.rounded_rectangle((x,y,x+32,y+32),radius=3,fill=fill,outline='#f1cd76' if f['known_withdrawals'][i] else fill,width=2);d.text((x+8,y+4),labels[label],font=fonts[19],fill='#edf4e9')
 for n,(key,color,title) in enumerate([('atlas_accuracy','#76ddad','Atlas accuracy'),('coverage','#87bce7','Valid source coverage'),('stale_fraction','#f1cd76','Stale citation fraction')]):
  ox=850;oy=220+n*155;d.text((ox,oy-33),title+' (0–100%)',font=fonts[19],fill=color);pts=[(ox+t/23*650,oy+90-r[key]*90) for t,r in enumerate(w['frames'])];d.line(pts,fill=color,width=3);eventx=ox+10/23*650;d.line((eventx,oy,eventx,oy+95),fill='#aebeb3');d.text((ox,oy+99),'0',font=fonts[14],fill='#aebeb3');d.text((eventx-8,oy+99),'10',font=fonts[14],fill='#aebeb3');d.text((ox+630,oy+99),'23',font=fonts[14],fill='#aebeb3')
 d.text((45,586),'200 scout identities · 20 claim curators per grid row',font=fonts[19],fill='#aebeb3');d.text((45,625),'+ / − / ? = supports / refutes / uncertain',font=fonts[19],fill='#aebeb3');d.text((45,664),'Green / rust = correct / incorrect; gold border = notice received',font=fonts[17],fill='#aebeb3');d.text((45,738),'Measured logical rounds. Fixture truth is evaluator-only. After extraction, sharing and aggregation are programmed.',font=fonts[19],fill='#edf4e9');d.text((45,773),'No successful Qwen or heterogeneous-head result is claimed. Full histories and failed qualifications are retained.',font=fonts[17],fill='#aebeb3');im.save(out/(a['id'].replace('+','-and-')+'.png'))
print('Rendered 72 per-world final frames from completed records.')
