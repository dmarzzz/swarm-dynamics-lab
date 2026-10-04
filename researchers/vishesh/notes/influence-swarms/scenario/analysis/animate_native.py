"""Animate only recorded responses/terminal events for one declared case."""
import argparse,json,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
p=argparse.ArgumentParser();p.add_argument('run');p.add_argument('out');p.add_argument('--case',type=int,default=0);a=p.parse_args();root=Path(a.run)
case=json.loads((root/f'case-{a.case}.json').read_text());events=[json.loads(x) for x in (root/f'events-{a.case}.jsonl').read_text().splitlines()]
requests={e['call']:e['request']['observation'] for e in events if e['kind']=='request'}
frames=[];reports={};checks=[];decisions={}
def font(n):
 for path in ['/System/Library/Fonts/Supplemental/Arial.ttf','/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
  try:return ImageFont.truetype(path,n)
  except OSError:pass
 return ImageFont.load_default()
def frame(label,seconds):
 im=Image.new('RGB',(1280,800),'#101c27');d=ImageDraw.Draw(im)
 def t(x,y,v,n=19,col='#dbe9f0'):d.text((x,y),v,font=font(n),fill=col)
 t(35,25,'How to win agents and influence swarms',31)
 t(35,70,case['case_id']+' / '+case['world']+' • measured model responses',20,'#76d9c5')
 t(35,110,f'{label} | recorded elapsed {seconds:.1f}s',19)
 for i,role in enumerate(('finance','security','implementation','service quality','operations','source audit')):
  x=35+(i%3)*415;y=160+(i//3)*155;r=reports.get(role)
  d.rounded_rectangle((x,y,x+395,y+135),8,fill='#1b303e',outline='#4a6575')
  t(x+14,y+10,role,18,'#a7c0cf');t(x+14,y+43,r['choice'] if r else 'Pending',24)
  if r:
   conf=r.get('confidence');t(x+14,y+78,'Confidence '+(f'{conf:.0%}' if conf is not None else 'unreported'),17)
 t(35,490,'Retrieved checks: '+(' · '.join(checks) if checks else 'Pending'),18)
 for i,arm in enumerate(('team_ballots','team_evidence','solo')):
  x=35+i*415;y=545;r=decisions.get(arm)
  d.rounded_rectangle((x,y,x+395,y+130),8,fill='#1b303e',outline='#4a6575')
  t(x+14,y+10,arm,18,'#a7c0cf');t(x+14,y+43,(r['decision']['choice'] if r['valid'] else 'Invalid output') if r else 'Pending',24)
  if r:t(x+14,y+83,('Acceptable' if r['evaluation']['acceptable_decision'] else 'Adverse') if r['valid'] else 'Invalid',19,'#76d9c5' if r['valid'] and r['evaluation']['acceptable_decision'] else '#ffab92')
 t(35,720,'Two team chairs share a prefix; evaluator labels appear only after a terminal decision.',18)
 t(35,752,'Synthetic pilot. Fixed playback rate; no independent-agent or population robustness claim.',17,'#a7c0cf')
 frames.append(im)
frame('Initial state',0)
for e in events:
 if e['kind']=='response':
  obs=requests[e['call']];role=obs.get('role');answer=e['answer']
  if role and role!='generalist':reports[role]=answer
  if e['phase']=='check' and len(checks)<2:checks.append(obs['document']['id'])
  frame((role or e['phase'])+' response',e['elapsed_seconds'])
 elif e['kind']=='terminal':
  decisions[e['outcome']['arm']]=e['outcome'];frame(e['outcome']['arm']+' decision',e['elapsed_seconds'])
frames[0].save(a.out,save_all=True,append_images=frames[1:],duration=[1000]*(len(frames)-1)+[4000],loop=0)
print(json.dumps({'frames':len(frames),'case':case['case_id'],'world':case['world'],'responses':sum(e['kind']=='response' for e in events)}))
