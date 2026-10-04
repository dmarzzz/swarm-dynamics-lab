import json,hashlib,html,io
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
from freshness import CASES

def plot(rows,path,tick=4,backend="native"):
 plt.style.use('dark_background');fig,axes=plt.subplots(3,2,figsize=(18,12));fig.suptitle('Immune Response | '+backend+' | '+str(len(rows))+'/12 complete episodes | recorded interventions',fontsize=22)
 for ax,case in zip(axes.flat,CASES):
  ax.set_title(case.replace('_',' '));ax.set_ylim(-.4,1.2);ax.set_xlim(-.2,4.2);ax.set_yticks([0,1],['unhealthy','healthy']);ax.set_xticks(range(5));ax.grid(alpha=.15)
  for arm,color,offset in [('raw','#ffba72',-.035),('checked','#67dec3',.035)]:
   row=next((r for r in rows if r['case']==case and r['arm']==arm),None)
   if row is None:continue
   trace=row['trace'][:tick];ys=[row['initial_healthy']]+[x['healthy'] for x in trace];ax.plot(range(len(ys)),[v+offset for v in ys],color=color,label=arm,marker='o' if arm=='raw' else 's',fillstyle='none')
   for x in trace:
    marker='X' if x['redundant'] else '*' if x['useful_restart'] else '^' if x['configuration_change'] else 'D' if x['action']['action']=='inspect' else None
    if marker:ax.scatter([x['tick']],[x['healthy']+offset],marker=marker,s=115,color=color,zorder=4)
    stale=x['observation']['cached_probe']['epoch']!=x['observation']['current_epoch']
    if stale:ax.scatter([x['tick']],[-.22+offset],marker='_',s=200,color=color)
  ax.legend(loc='lower right');ax.set_xlabel('Initial state (0), then measured action ticks')
 fig.text(.05,.025,'X redundant restart | ★ useful restart | ▲ configuration change | ◆ inspect | bottom dash: stale evidence at decision\nPaired lines offset slightly for visibility. Fixed constructed cases; missing panels are not outcomes.',fontsize=11)
 fig.tight_layout(rect=(0,.065,1,.94));fig.savefig(path,dpi=100);plt.close(fig)

def render(out):
 out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];backend=json.loads((out/'manifest.json').read_text())['backend'];plot(rows,out/'final_frame.png',backend=backend);images=[]
 for t in range(5):
  b=io.BytesIO();plot(rows,b,t,backend=backend);b.seek(0);images.append(Image.open(b).convert('RGB'))
 images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=1000,loop=0)
 payload=json.dumps(rows).replace('<','\\u003c')
 doc='''<!doctype html><meta charset="utf-8"><title>Immune Response</title><style>body{background:#10232d;color:#eaf4f7;font:16px system-ui;margin:32px}h1{margin-bottom:5px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:15px}.card{background:#193440;padding:18px;border-radius:12px}.state{display:flex;gap:10px}.part{padding:10px;background:#254957;border-radius:8px}pre{white-space:pre-wrap;font:14px system-ui}.ok{color:#7ee5bf}.bad{color:#ffaf89}input{width:60%}button{padding:10px}small{color:#bacfd5}</style><h1>Immune Response</h1><p>Actual service state vs actor-visible cached evidence. Every intervention is shown.</p><button id="play">Play / pause</button> <input id="time" type="range" min="0" max="4" value="0"><b id="label"></b><p><small>Six constructed cases × raw/checked evidence. Partial A5: 3 complete, 1 invalid, 8 unstarted episodes. Invalid action is retained in the trace audit, not drawn as an applied action. A same-version restart may be useful or redundant.</small></p><div class="grid" id="grid"></div><script>const rows=DATA;const slider=document.querySelector('#time');let timer;document.querySelector('#play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else{timer=setInterval(()=>{slider.value=(+slider.value+1)%5;draw()},1000)}};slider.oninput=draw;function draw(){let t=+slider.value;document.querySelector('#label').textContent='Tick '+t;let grid=document.querySelector('#grid');grid.replaceChildren();for(let r of rows){let x=t?r.trace[t-1]:null,s=x?x.state:r.initial,ob=x?x.observation:null;let c=document.createElement('div');c.className='card';let title=document.createElement('h3');title.textContent=r.case.replaceAll('_',' ')+' · '+r.arm;c.append(title);let parts=document.createElement('div');parts.className='state';for(let name of Object.keys(s.deployed)){let p=document.createElement('div');p.className='part';p.textContent=name+' v'+s.deployed[name]+' · '+(s.live[name]?'live':'DOWN');parts.append(p)}c.append(parts);let p=document.createElement('pre');p.textContent='Actual health: '+((x?x.healthy:r.initial_healthy)?'healthy':'unhealthy')+'\n'+(x?'Action: '+x.action.action+' '+x.action.service+' '+x.action.version+'\n'+x.action.reason+'\nRedundant: '+x.redundant+' · Useful restart: '+x.useful_restart+'\nEvidence at decision: epoch '+ob.cached_probe.epoch+' vs current '+ob.current_epoch+'\nCached processes live: '+ob.cached_probe.checks.processes_live+'\nReceipt: '+JSON.stringify(ob.probe_receipt||'raw record'):'Initial cached probe epoch '+s.probe.epoch+' vs current '+s.epoch);c.append(p);grid.append(c)}}draw()</script>'''.replace('DATA',payload)
 (out/'replay.html').write_text(doc)
 (out/'visualization-provenance.json').write_text(json.dumps({'episodes_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest(),'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'frames':5,'panels':6,'all_applied_actions_visible':True,'invalid_actions_require_trace_audit':True,'completed_episodes':len(rows)},indent=2))
if __name__=='__main__':
 import sys;render(sys.argv[1])
