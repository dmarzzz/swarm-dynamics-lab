from pathlib import Path
import json,math
from PIL import Image,ImageDraw,ImageFont
p=Path(__file__).resolve().parents[1];a=json.loads((p/'S50-AUDIT.json').read_text());events=json.loads((p/'S50-EVENTS.json').read_text());out=Path(__file__).resolve().parents[1]
fontpath='/System/Library/Fonts/Helvetica.ttc'
if not Path(fontpath).exists():
 from matplotlib.font_manager import findfont
 fontpath=findfont('DejaVu Sans')
def ft(n):return ImageFont.truetype(fontpath,n)
arms=['interactive','static','broken','retained'];labels=['Interactive handover','Static handover','Broken inheritance','Retained founders'];frames=[]
steps=list(range(0,a['calls']+1,25))+[a['calls']]
for step in steps:
 st={arm:{'nodes':[{'known':False,'correct':False,'g':0} for _ in range(50)],'replaced':0,'correct':0,'assigned':0,'harmful':0} for arm in arms};base={'correct':0,'assigned':0}
 for ev in events:
  if ev['seq']>=step:break
  i=int(ev['owner'].split('_')[1]);arm=ev.get('arm','common')
  if ev['type'] in ('founder','selection'):
   for x in arms if arm=='common' else [arm]:st[x]['nodes'][i].update(known=True,correct=ev['correct'])
  elif ev['type']=='replacement':st[arm]['nodes'][i].update(known=ev['valid'],correct=ev['correct'],g=1);st[arm]['replaced']+=1
  elif ev['type']=='decision':
   if arm=='common':base['correct']+=ev['correct'];base['assigned']+=ev['assigned']
   else:
    for k in ('correct','assigned','harmful'):st[arm][k]+=ev[k]
 im=Image.new('RGB',(1040,900),'#101519');d=ImageDraw.Draw(im)
 d.text((28,20),'Swarm of Theseus · measured turnover',font=ft(32),fill='#eef5f5');d.text((28,65),f"50 positions | {step:,} / {a['calls']:,} completed native calls | one shared ancestor",font=ft(19),fill='#bac6cd')
 for j,arm in enumerate(arms):
  x=24+(j%2)*510;y=112+(j//2)*342;v=st[arm];d.rounded_rectangle((x,y,x+490,y+325),radius=12,fill='#1a2329',outline='#374750');d.text((x+18,y+13),labels[j],font=ft(23),fill='#eef5f5')
  cx=x+150;cy=y+170
  for i,n in enumerate(v['nodes']):
   theta=2*math.pi*i/50-math.pi/2;nx=cx+104*math.cos(theta);ny=cy+104*math.sin(theta);color=('#73d8c3' if n['correct'] else '#fa887c') if n['known'] else '#65747c';d.ellipse((nx-5,ny-5,nx+5,ny+5),fill=color,outline='white' if n['g'] else color,width=2)
  routes=sum(n['known'] and n['correct'] for n in v['nodes']);d.text((cx-43,cy-18),f'{routes}/50',font=ft(30),fill='#eef5f5');d.text((cx-59,cy+20),'correct routes',font=ft(17),fill='#bac6cd')
  d.text((x+283,y+91),f"{v['replaced']}/50",font=ft(26),fill='#eef5f5');d.text((x+283,y+123),'successor commits',font=ft(15),fill='#bac6cd');d.text((x+283,y+164),f"{v['correct']}/{v['assigned']}",font=ft(26),fill='#eef5f5');d.text((x+283,y+197),'observed correct',font=ft(15),fill='#bac6cd');d.text((x+283,y+240),f"{v['harmful']} harmful",font=ft(20),fill='#fa887c')
 d.text((28,812),'Green: correct route  |  Red: wrong route  |  Gray: unobserved  |  White outline: successor',font=ft(17),fill='#bac6cd');d.text((28,842),'One synthetic world (n=1). Nodes show positions, not observed communication links.',font=ft(17),fill='#bac6cd');d.text((28,867),'Recorded events only; no interpolated behavioral scores. Knowledge and actions are separate.',font=ft(16),fill='#bac6cd')
 frames.append(im)
frames[0].save(out/'S50-TURNOVER.gif',save_all=True,append_images=frames[1:],duration=[240]*(len(frames)-1)+[2500],loop=0,optimize=True);frames[-1].save(out/'S50-TURNOVER-FINAL.png');print(json.dumps({'frames':len(frames),'native_event_count':len(events),'gif':str(out/'S50-TURNOVER.gif')}))
