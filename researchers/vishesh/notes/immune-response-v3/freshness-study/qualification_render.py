import json,hashlib,html,io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
CASES=['healthy_fresh','fresh_crash','stale_false_alarm']
def plot(rows,path,tick=2,backend="openrouter"):
 plt.style.use('dark_background');fig,axes=plt.subplots(1,3,figsize=(15,5));fig.suptitle(f'Immune Response | A6 {backend} | {len(rows)}/6 complete episodes')
 for ax,c in zip(axes,CASES):
  ax.set_title(c.replace('_',' '));ax.set_xlim(-.1,2.1);ax.set_ylim(-.3,1.15);ax.set_xticks([0,1,2]);ax.set_yticks([0,1],['unhealthy','healthy']);ax.grid(alpha=.2);found=False
  for arm,color,offset in [('raw','#ffba72',-.03),('checked','#67dec3',.03)]:
   r=next((r for r in rows if r['case']==c and r['arm']==arm),None)
   if not r:continue
   found=True;tr=r['trace'][:tick];ax.plot(range(len(tr)+1),[v+offset for v in [r['initial_healthy']]+[x['healthy'] for x in tr]],color=color,label=arm,marker='o')
   for x in tr:
    marker='*' if x['useful_restart'] else '^' if x['configuration_change'] else 'D' if x['action']['action']=='inspect' else 'x' if x['redundant'] else None
    if marker:ax.scatter([x['tick']],[x['healthy']+offset],marker=marker,s=130,color=color)
    if x['observation']['cached_probe']['epoch']!=x['observation']['current_epoch']:ax.scatter([x['tick']],[-.2+offset],marker='_',color=color,s=180)
  if found:ax.legend(loc='lower right')
  else:ax.text(.5,.5,'No complete trajectory',transform=ax.transAxes,ha='center')
 fig.text(.04,.025,'★ useful restart | ▲ configuration change | ◆ inspect | x redundant restart | lower dash: stale evidence\nInitial state then two measured ticks. Three inspected development roots; missing outcomes are not zeros.',fontsize=10);fig.tight_layout(rect=(0,.11,1,.91));fig.savefig(path,dpi=120);plt.close(fig)
def render(out):
 out=Path(out);rows=[json.loads(l) for l in (out/'episodes.jsonl').read_text().splitlines()];backend=json.loads((out/'manifest.json').read_text())['backend'];plot(rows,out/'final_frame.png',backend=backend);images=[]
 for t in range(3):
  data=io.BytesIO();plot(rows,data,t,backend);data.seek(0);images.append(Image.open(data).convert('RGB'))
 images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=1300,loop=0)
 payload=json.dumps(rows).replace('<','\\u003c');doc='''<!doctype html><meta charset="utf-8"><title>Immune Response A6</title><style>body{background:#10232d;color:#edf4f5;font:16px system-ui;margin:30px}.row{background:#193440;padding:15px;margin:10px}pre{white-space:pre-wrap}</style><h1>Immune Response — A6 BACKEND qualification</h1><p>Three familiar development worlds, six assigned episodes. Missing trajectories remain missing; no treatment-effect claim.</p><button id="play">Play/pause</button><input id="tick" type="range" min="0" max="2" value="0"><b id="time"></b><div id="grid"></div><script>const rows=DATA;let timer;const slider=document.querySelector('#tick');document.querySelector('#play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>{slider.value=(+slider.value+1)%3;draw()},1300)};slider.oninput=draw;function draw(){let t=+slider.value;document.querySelector('#time').textContent='Tick '+t;let grid=document.querySelector('#grid');grid.replaceChildren();for(let r of rows){let x=t?r.trace[t-1]:null;let el=document.createElement('pre');el.className='row';el.textContent=r.case+' / '+r.arm+'\\n'+JSON.stringify(x?{action:x.action,health:x.healthy,actual:x.state,observed:x.observation.cached_probe}:r.initial,null,2);grid.append(el)}}draw()</script>'''.replace('DATA',payload).replace('BACKEND',backend);(out/'replay.html').write_text(doc)
 (out/'visualization-provenance.json').write_text(json.dumps({'input_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frames':3,'complete_episodes':len(rows)},indent=2))
if __name__=='__main__':
 import sys;render(sys.argv[1])
