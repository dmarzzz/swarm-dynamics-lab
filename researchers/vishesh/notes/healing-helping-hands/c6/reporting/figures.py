"""Scientific plots and observed-call replay from saved C6R2 evidence only."""
import argparse,collections,html,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from design import LABELS,score
from report import report

def render(root,out):
 import matplotlib
 matplotlib.use('Agg')
 import matplotlib.pyplot as plt
 import numpy as np
 out.mkdir(parents=True,exist_ok=True);rows=json.loads((root/'observations.json').read_text());manifest=json.loads((root/'manifest.json').read_text());review=report(root);result=score(rows);stage=manifest['stage'];n=len(rows)
 plt.rcParams.update({'font.family':'DejaVu Sans','font.size':11,'figure.facecolor':'#101725','axes.facecolor':'#182235','axes.edgecolor':'#6e7e97','axes.labelcolor':'#e7efff','text.color':'#e7efff','xtick.color':'#b9c8df','ytick.color':'#b9c8df','savefig.facecolor':'#101725'})
 fig,axes=plt.subplots(1,3,figsize=(16,5),layout='constrained')
 for ax,key,title in zip(axes,('a','b','jev'),('Haiku A','Haiku B','Jev')):
  mat=np.array([[sum(r['expected']==gold and r.get('labels',{}).get(key)==pred for r in rows) for pred in LABELS] for gold in LABELS]);ax.imshow(mat,cmap='Blues',vmin=0,vmax=n/3)
  for y in range(3):
   for x in range(3):ax.text(x,y,str(mat[y,x]),ha='center',va='center',color='#102030' if mat[y,x]<n/6 else 'white',fontsize=16)
  ax.set(xticks=range(3),xticklabels=LABELS,yticks=range(3),yticklabels=LABELS,title=title,xlabel='Returned label',ylabel='Ground truth')
 fig.suptitle(f'Healing Helping Hands • C6R2 {stage}\n{n} synthetic cases; counts within authored templates, not independent domains',fontsize=17)
 fig.savefig(out/'confusion.png',dpi=140);plt.close(fig)
 policies={'Haiku A':'qwen','Always Jev':'jev','Agreement route':'cascade','Matched random':'matched'}
 errors={name:100*sum(v['error'][key] for v in result['families'].values())/len(result['families']) for name,key in policies.items()}
 fig,(a,b)=plt.subplots(1,2,figsize=(15,6),layout='constrained');colors=['#8ca4ff','#65dfb0','#ffba70','#bac7da']
 a.barh(list(errors),list(errors.values()),color=colors);a.set_xlim(0,max(5,max(errors.values())*1.25));a.set_xlabel('Error rate (%)');a.invert_yaxis()
 for i,val in enumerate(errors.values()):a.text(val+.12,i,f'{val:.2f}%',va='center')
 costs=review.get('derived_policy_cost_usd',{});names={'haiku_a':'Haiku A','always_jev':'Always Jev','agreement_routing':'Agreement route'}
 if costs:
  b.barh([names[k] for k in costs],[1000*v/n for v in costs.values()],color=colors[:3]);b.invert_yaxis();b.set_xlabel('Measured API dollars per 1,000 reports\nDerived deployment policy; both Haiku passes charged')
  for i,v in enumerate(costs.values()):b.text(1000*v/n+.003,i,f'${1000*v/n:.3f}',va='center')
  b.set_xlim(0,max(1000*v/n for v in costs.values())*1.25)
 fig.suptitle(f'C6R2 {stage}: correctness and the actual API cost tradeoff\n{n} cases • 12 authored semantic families in main • no population CI',fontsize=17)
 fig.savefig(out/'outcomes.png',dpi=140);plt.close(fig)
 families=list(result['families']);keys=('qwen','jev','cascade','matched');values=np.array([[100*result['families'][f]['error'][k] for k in keys] for f in families])
 fig,ax=plt.subplots(figsize=(12,max(4,len(families)*.5)),layout='constrained');im=ax.imshow(values,cmap='YlOrRd',vmin=0,vmax=max(5,float(values.max())),aspect='auto')
 for y in range(len(families)):
  for x in range(len(keys)):ax.text(x,y,f'{values[y,x]:.1f}%',ha='center',va='center',color='#172132')
 ax.set(xticks=range(4),xticklabels=('Haiku A','Always Jev','Agreement route','Matched random'),yticks=range(len(families)),yticklabels=families,title=f'C6R2 {stage}: error within each authored family\nFinite synthetic cells; no population uncertainty claim');fig.colorbar(im,ax=ax,label='Error (%)');fig.savefig(out/'family-errors.png',dpi=150);plt.close(fig)
 events=[json.loads(x) for x in (root/'calls.jsonl').read_text().splitlines()];starts={e['id']:e for e in events if e['type']=='start'};responses={e['id']:e for e in events if e['type']=='response'};complete=[e for e in events if e['type']=='completed'];byid={r['id']:r for r in rows};timeline=[]
 for e in complete:
  st=starts[e['id']];r=byid[st['row_id']];raw=responses[e['id']]['raw'];timeline.append({'seconds':round(responses[e['id']]['epoch']-manifest['started_epoch'],3),'case':r['id'],'agent':st['variant'],'label':e['result']['label'],'truth':r['expected'],'claim':r['claim'],'report':r['report'],'raw':raw.get('answers') or raw.get('choices')})
 data=json.dumps(timeline).replace('</','<\\/');title=f'C6R2 {stage}: recorded answer timeline'
 doc='''<!doctype html><meta charset="utf-8"><title>TITLE</title><style>body{background:#101725;color:#eef2ff;font:16px system-ui;padding:30px;max-width:1200px;margin:auto}button,input{margin:10px}#tiles{display:grid;grid-template-columns:repeat(18,1fr);gap:5px}.tile{aspect-ratio:1;border:0;background:#344054;color:white;padding:1px;font-size:11px;cursor:pointer}pre{white-space:pre-wrap;background:#1b273e;padding:20px}#status{font-size:23px;padding:20px 0}</style><h1>TITLE</h1><p>Actual recorded responses, in arrival order. Time is measured from native collection start. These are dependent model calls on synthetic cases, not independent agents or learning steps.</p><button id="play">Play recorded responses</button><input id="seek" type="range" min="0" value="0"><span id="clock"></span><div id="status"></div><div id="tiles"></div><pre id="detail">Select a tile to inspect its exact visible evidence and returned answer.</pre><script>const data=DATA;let pos=0,timer=null;const seek=document.querySelector('#seek'),tiles=document.querySelector('#tiles');seek.max=data.length;function draw(){let seen=data.slice(0,pos),wrong=seen.filter(x=>x.label!==x.truth).length;document.querySelector('#status').textContent=pos+' / '+data.length+' responses · '+wrong+' incorrect';document.querySelector('#clock').textContent=pos?data[pos-1].seconds+' recorded seconds':'';seek.value=pos;tiles.replaceChildren();seen.forEach((x,i)=>{let b=document.createElement('button');b.className='tile';b.style.background=x.label===x.truth?'#207d69':'#b44d52';b.textContent=x.agent;b.title=x.case+' '+x.label;b.onclick=()=>document.querySelector('#detail').textContent=JSON.stringify(x,null,2);tiles.append(b)})}seek.oninput=()=>{pos=Number(seek.value);draw()};document.querySelector('#play').onclick=()=>{if(timer){clearInterval(timer);timer=null;return}if(pos===data.length)pos=0;timer=setInterval(()=>{pos=Math.min(data.length,pos+1);draw();if(pos===data.length){clearInterval(timer);timer=null}},80)};draw();</script>'''.replace('TITLE',html.escape(title)).replace('DATA',data)
 (out/'replay.html').write_text(doc);(out/'metrics.json').write_text(json.dumps(review,indent=2));return {'images':['confusion.png','outcomes.png'],'replay_calls':len(timeline)}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args();print(json.dumps(render(a.root,a.out)))
