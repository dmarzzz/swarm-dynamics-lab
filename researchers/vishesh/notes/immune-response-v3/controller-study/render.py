"""Measured two-tick trajectories; all conditions and missing assignments stay explicit."""
import json,io,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
import cases

def plot(rows,path,tick=2):
 plt.style.use('dark_background');fig,axes=plt.subplots(1,2,figsize=(15,max(5,len(rows)*.32)))
 for ax,split in zip(axes,['development','holdout']):
  selected=[r for r in rows if r['split']==split];ax.set_title(split.title());ax.set_xlim(-.15,2.2);ax.set_xticks([0,1,2]);ax.set_xlabel('Simulator tick');ax.grid(alpha=.15)
  labels=[]
  for i,r in enumerate(selected):
   labels.append(r['model']+' / '+r['case']['kind']+' / '+r['condition']);states=[int(all(cases.f.health(r['case']['fixture'],r['case']['initial']).values()))]+[x['healthy'] for x in r['trace'][:tick]]
   ax.plot(range(len(states)),[i]*len(states),c='#687b90',lw=2)
   for t,healthy in enumerate(states):
    ax.scatter(t,i,c='#61dbc0' if healthy else '#fa7285',s=90,marker='o')
    if t:
     x=r['trace'][t-1];mark='R' if x['useful_restart'] else 'C' if x['configuration_change'] else 'I' if x['action']['action']=='inspect' else '·';ax.text(t+.07,i,mark+(' !' if not x['diagnosis_correct'] else ''),va='center',fontsize=9)
  ax.set_yticks(range(len(labels)),labels,fontsize=8);ax.invert_yaxis()
  if not selected:ax.text(.5,.5,'Conditional stage not opened',ha='center',transform=ax.transAxes)
 fig.suptitle('Immune Response | native controller qualification');fig.text(.03,.02,'Green: healthy; red: unhealthy. R: useful restart; C: configuration change; I: inspect; !: diagnosis error. Repeated roots are dependent.',fontsize=9);fig.tight_layout(rect=(0,.055,1,.95));fig.savefig(path,dpi=120);plt.close(fig)
def render(out):
 out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];plot(rows,out/'final_frame.png');frames=[]
 for tick in range(3):
  b=io.BytesIO();plot(rows,b,tick);b.seek(0);frames.append(Image.open(b).convert('RGB'))
 frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=1600,loop=0)
 data=json.dumps(rows).replace('<','\\u003c')
 html='''<!doctype html><meta charset="utf-8"><title>Immune Response</title><style>body{background:#10232d;color:#edf4f5;font:16px system-ui;margin:24px}article{background:#193440;padding:16px;margin:12px 0}pre{white-space:pre-wrap}summary{cursor:pointer}</style><h1>Immune Response</h1><p>Native diagnosis → selected action → verified service outcome. Authored qualification, not a population reliability estimate.</p><button id="play">Play/pause</button><input id="tick" type="range" min="0" max="2" value="0"><b id="time"></b><main id="rows"></main><script>const data=DATA;let timer;const slider=document.querySelector('#tick');document.querySelector('#play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>{slider.value=(+slider.value+1)%3;draw()},1600)};slider.oninput=draw;function draw(){let t=+slider.value;document.querySelector('#time').textContent='Tick '+t;const root=document.querySelector('#rows');root.replaceChildren();for(const r of data){const a=document.createElement('article'),h=document.createElement('h2'),pre=document.createElement('pre');h.textContent=r.model+' / '+r.split+' / '+r.case.kind+' / '+r.condition;a.append(h);const x=t?r.trace[t-1]:null;pre.textContent=JSON.stringify(x?{diagnosis:x.diagnosis,diagnosis_correct:x.diagnosis_correct,selected_action:x.action,visible_reason:x.raw_response.reason,healthy:x.healthy,useful_restart:x.useful_restart}:r.case.initial,null,2);a.append(pre);if(x){const d=document.createElement('details'),s=document.createElement('summary'),p=document.createElement('pre');s.textContent='Exact model-visible evidence';p.textContent=JSON.stringify(x.observation,null,2);d.append(s,p);a.append(d)}root.append(a)}}draw()</script>'''.replace('DATA',data)
 (out/'replay.html').write_text(html);(out/'visualization-provenance.json').write_text(json.dumps({'input_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frames':3,'completed':len(rows),'backend':'openrouter'},indent=2))
