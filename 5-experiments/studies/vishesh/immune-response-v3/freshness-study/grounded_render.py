"""Saved-data-only four-condition trajectories and evidence replay."""
import json,io,hashlib
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
CASES=('healthy_fresh','fresh_crash','stale_false_alarm')
COLORS={'plain_solo':'#ffb86b','plain_advice':'#ff657a','grounded_solo':'#63d9bd','grounded_advice':'#8fa7ff'}
def plot(rows,path,tick=2,backend='openrouter'):
 plt.style.use('dark_background');fig,axes=plt.subplots(1,3,figsize=(16,5));fig.suptitle(f'Immune Response A9 | {backend} | {len(rows)}/12 complete trajectories')
 for ax,case in zip(axes,CASES):
  ax.set_title(case.replace('_',' '));ax.set_xlim(-.15,2.15);ax.set_ylim(-.25,1.25);ax.set_xticks([0,1,2]);ax.set_yticks([0,1],['unhealthy','healthy']);ax.grid(alpha=.2)
  for i,(condition,color) in enumerate(COLORS.items()):
   r=next((x for x in rows if x['case']==case and x['condition']==condition),None)
   if r is None:continue
   offset=(i-1.5)*.04;trace=r['trace'][:tick];ax.plot(range(len(trace)+1),[v+offset for v in [r['initial_healthy']]+[x['healthy'] for x in trace]],color=color,marker='o',label=condition.replace('_',' '))
   for x in trace:
    marker='*' if x['useful_restart'] else '^' if x['configuration_change'] else 'D' if x['action']['action']=='inspect' else None
    if marker:ax.scatter([x['tick']],[x['healthy']+offset],marker=marker,color=color,s=110)
  if not any(x['case']==case for x in rows):ax.text(.5,.5,'No complete trajectory',ha='center',transform=ax.transAxes)
 handles,labels=axes[0].get_legend_handles_labels()
 if handles:fig.legend(handles,labels,loc='lower center',ncol=4,bbox_to_anchor=(.5,.035))
 fig.text(.04,.012,'★ useful restart | ▲ configuration change | ◆ inspect. Small vertical offsets separate conditions; health is binary. Three inspected roots, not population inference.',fontsize=9)
 fig.tight_layout(rect=(0,.14,1,.92));fig.savefig(path,dpi=120);plt.close(fig)
def render(out):
 out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];backend=json.loads((out/'manifest.json').read_text())['backend'];plot(rows,out/'final_frame.png',backend=backend);frames=[]
 for tick in range(3):
  buf=io.BytesIO();plot(rows,buf,tick,backend);buf.seek(0);frames.append(Image.open(buf).convert('RGB'))
 frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=1500,loop=0)
 data=json.dumps(rows).replace('<','\\u003c');doc='''<!doctype html><meta charset="utf-8"><title>Immune Response A9</title><style>body{background:#10232d;color:#edf4f5;font:16px system-ui;margin:24px}article{background:#193440;padding:16px;margin:12px 0}pre{white-space:pre-wrap}summary{cursor:pointer}</style><h1>Immune Response A9 — BACKEND</h1><p>Four conditions × three inspected worlds. No population inference. Missing trajectories stay missing.</p><button id="play">Play/pause</button><input id="tick" type="range" min="0" max="2" value="0"><b id="time"></b><main id="rows"></main><script>const data=DATA;let timer;const slider=document.querySelector('#tick');document.querySelector('#play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>{slider.value=(+slider.value+1)%3;draw()},1500)};slider.oninput=draw;function draw(){let t=+slider.value;document.querySelector('#time').textContent='Tick '+t+' | '+data.length+'/12 complete';const root=document.querySelector('#rows');root.replaceChildren();for(const r of data){const a=document.createElement('article');const h=document.createElement('h2');h.textContent=r.case+' / '+r.condition;a.append(h);const x=t?r.trace[t-1]:null;const pre=document.createElement('pre');pre.textContent=JSON.stringify(x?{health:x.healthy,actual_action:x.action,raw_response:x.raw_response}:r.initial,null,2);a.append(pre);if(x){const d=document.createElement('details'),s=document.createElement('summary'),p=document.createElement('pre');s.textContent='Visible catalog, advice, grounding and telemetry';p.textContent=JSON.stringify({catalog:x.observation.catalog,advice:x.observation.team_advice,grounding:x.observation.evidence_table??'absent',probe:x.observation.cached_probe,current_epoch:x.observation.current_epoch},null,2);d.append(s,p);a.append(d)}root.append(a)}}draw()</script>'''.replace('DATA',data).replace('BACKEND',backend)
 (out/'replay.html').write_text(doc);(out/'visualization-provenance.json').write_text(json.dumps({'input_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frames':3,'completed':len(rows),'backend':backend},indent=2))
