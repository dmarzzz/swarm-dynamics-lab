"""Exact-total outcomes and real checker trace, no raw receipt content."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BG='#111a2b';FG='#eef4ff';MUTED='#a7b6d0'
def font(n):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
  if Path(p).exists():return ImageFont.truetype(p,n)
 return ImageFont.load_default(size=n)
def text(d,xy,s,n=26,c=FG):d.text(xy,str(s),font=font(n),fill=c)
def canvas(title,subtitle):
 im=Image.new('RGB',(1800,1100),BG);d=ImageDraw.Draw(im);text(d,(60,40),title,40);text(d,(60,110),subtitle,24,MUTED);return im,d

def render(out,records,outcomes,summary):
 im,d=canvas('Antsy | accept, check, or refer?',f"{summary['assigned']} assigned receipts | {summary['scorable']} scorable | {summary['unscorable']} unscorable references | actual OCR tools")
 text(d,(60,190),'Policy',28);text(d,(600,190),'Correct / wrong / refer',28);text(d,(1170,190),'Checks / tool seconds',28)
 for i,(arm,r) in enumerate(summary['arms'].items()):
  y=270+i*115;text(d,(60,y),arm,28);text(d,(600,y),f"{r['correct']} / {r['wrong']} / {r['refer']}",32);text(d,(1170,y),f"{r['checks']} / {r['checker_wall_s']:.1f}s",30)
 text(d,(60,910),'Correct and wrong counts concern accepted exact totals; referrals are not counted as correct.',25,MUTED)
 text(d,(60,970),'Measured compute latency, not human review time. Shared Tesseract pipelines can agree on the wrong answer.',23,MUTED)
 text(d,(60,1020),'Exploratory instrument pilot; no model committee, payment safety or generalization claim.',23,MUTED);im.save(out/'final_frame.png')
 for r in records[:3]:
  result=next(x for x in outcomes if x['id']==r['id'] and x['arm']=='selective-check');visible={k:r['pipelines'][k]['candidate'] for k in 'ABC'};frames=[]
  states=[('Initial candidates',dict(visible))]
  for ev in result['events']:visible[ev['tool']]=ev['response'];states.append((f"Checker {ev['tool']} returned after {r['pipelines'][ev['tool']]['wall_s']:.2f}s",dict(visible)))
  states.append(('Commit and evaluator reveal',dict(visible)))
  for i,(label,candidates) in enumerate(states):
   im,d=canvas(f"Antsy | receipt {r['id']} | {label}",'Actual candidate amounts and checker outputs. Ground truth hidden until commitment.')
   for j,(tool,c) in enumerate(candidates.items()):text(d,(60,220+j*105),f"{tool}  {c['status']}  total={c['value']}  confidence={c['confidence']:.2f}",29)
   if i==len(states)-1:
    text(d,(60,830),f"Decision: {result['action']} {result['value']} | reference: {r['gold']['status']} {r['gold']['value']}",29)
    text(d,(60,910),f"Correct={result['correct']}  wrong={result['wrong']}  refer={result['refer']}",27)
   else:text(d,(60,910),'Evaluator reference: hidden',28,MUTED)
   text(d,(60,1010),'First three assigned cases; no success-based example selection.',24,MUTED);frames.append(im)
  frames[0].save(out/f"receipt-{r['id']:03}.gif",save_all=True,append_images=frames[1:],duration=1800,loop=0)
