"""Measured repair comparisons and chronological state replay."""
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
BG='#101827';FG='#edf4ff';MUTED='#a7b4cb';COLORS=['#b6c2d3','#51d7bc','#a69aff']
def canvas(title,subtitle):
 im=Image.new('RGB',(1800,1100),BG);d=ImageDraw.Draw(im);text(d,(60,35),title,38);text(d,(60,95),subtitle,23,MUTED);return im,d
def font(size):
 for p in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
  if Path(p).exists():return ImageFont.truetype(p,size)
 return ImageFont.load_default(size=size)
def text(d,xy,s,size=25,color=FG):d.text(xy,str(s),font=font(size),fill=color)
def render(out,stage,summary,traces,rows):
 if stage=='D0':
  im,d=canvas('Antsy | does the update rule cause the damage?','Same recorded purchases; changed estimator only. Retrospective diagnostic, not new agent behavior.')
  text(d,(1120,170),'Recall     Harmful switches',25)
  for i,r in enumerate(x for x in summary['conditions'] if x['arm']=='swarm-adaptive'):
   y=220+i*112;color=COLORS[['original','null-neutral','global-empty'].index(r['estimator'])]
   text(d,(60,y),r['backend']+' / '+r['estimator'],25);d.rectangle((440,y,440+1000*r['quality'],y+36),fill=color);text(d,(1120,y),f"{r['quality']:.2%}        {r['harms']}/70",25)
  text(d,(60,950),'Harm = selected recall below the original no-check confidence choice. All 70 prior receipts retained.',23,MUTED)
  text(d,(60,1000),'Null-neutral retains the prior on null; global-empty removes the region symmetrically for all modes.',22,MUTED)
  im.save(out/'final_frame.png')
  for backend in ['Laya','Jev']:
   candidates=[t for t in traces if t['backend']==backend]
   losses={r['id']:r['initial_quality']-r['quality'] for r in rows if r['backend']==backend and r['arm']=='swarm-adaptive' and r['estimator']=='original'}
   worst=max(losses,key=losses.get)
   for t in [t for t in candidates if t['id'] in {30,31,32,worst}]:
    frames=[]
    for event in t['events']:
     im,d=canvas(f"Antsy | {backend} receipt {t['id']} | check {event['step']}",'Post-hoc diagnostic replay: actual purchases held fixed; alternatives are estimator counterfactuals.')
     text(d,(60,165),'Response: '+str(event['check']),23)
     for i,(v,scores) in enumerate(event['scores'].items()):
      text(d,(60,240+i*190),v,28,COLORS[i])
      for j,(m,q) in enumerate(scores.items()):text(d,(470+j*390,240+i*190),f'{m}: {q:.3f}',30,COLORS[i])
     text(d,(60,900),'Evaluator truth: '+('hidden until final state' if event['step']<len(t['events'])-1 else ', '.join(f'{m}={q:.3f}' for m,q in t['truth'].items())),25)
     text(d,(60,980),'First three assigned receipts plus largest original loss (explicitly selected after analysis).',23,MUTED);frames.append(im)
    frames[0].save(out/f"{backend.lower()}-{t['id']:03}.gif",save_all=True,append_images=frames[1:],duration=1800,loop=0)
 else:
  im,d=canvas('Antsy | buy a check only when it can earn its cost','Development diagnostic. Quality = token recall; review costs are assumptions, not measured dollars.')
  text(d,(60,175),'Cost / policy',25);text(d,(690,175),'Recall',25);text(d,(1000,175),'Checks',25);text(d,(1270,175),'Net utility',25)
  shown=[r for r in summary['conditions'] if r['cost'] in [.0,.02,.10] and r['arm'] in ['confidence-only','forced-two','cost-aware']]
  for i,r in enumerate(shown):
   y=240+i*76;color='#51d7bc' if r['arm']=='cost-aware' else FG
   text(d,(60,y),f"{r['cost']:.2f} / {r['arm']}",26,color);text(d,(690,y),f"{r['quality']:.2%}",26,color);text(d,(1000,y),f"{r['checks']:.2f}",26,color);text(d,(1270,y),f"{r['utility']:.3f}",26,color)
  text(d,(60,1000),'70 reused receipts; no new model calls. Costs and receipts are paired, not independent replications.',23,MUTED);im.save(out/'final_frame.png')
  for row in [r for r in rows if r['arm']=='cost-aware' and r['cost']==.02 and r['id'] in [30,31,32]]:
   frames=[]
   for event in row['events']:
    im,d=canvas(f"Antsy | receipt {row['id']} | cost-aware step {event['step']}",'Development-only policy trace. Hypothetical gains come from old calibration receipts, not current truth.')
    text(d,(60,200),'Current estimated scores: '+str({m:round(v,3) for m,v in event['scores_before'].items()}),27)
    text(d,(60,280),f"Action: {event['action']} | STOP: {event['stop']} | check price: {event['cost']}",27)
    for i,(a,g) in enumerate(event['projected_gains'].items()):text(d,(60+(i%3)*550,390+(i//3)*110),f'{a}: gain {g:.4f}',26)
    text(d,(60,820),'Purchased response: '+str(event.get('response','none')),25)
    text(d,(60,910),'No annotation labels are supplied to the action selector.',24,MUTED);frames.append(im)
   im,d=canvas(f"Antsy | receipt {row['id']} | committed",'Evaluator reveal after the decision; not an actor input.')
   text(d,(60,250),f"Choice {row['choice']} | measured recall {row['quality']:.3f}",35)
   text(d,(60,350),f"Checks {row['checks']} | net utility {row['utility']:.3f}",35);frames.append(im)
   frames[0].save(out/f"cost-aware-{row['id']:03}.gif",save_all=True,append_images=frames[1:],duration=1800,loop=0)
