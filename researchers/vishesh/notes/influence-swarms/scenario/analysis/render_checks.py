"""Render observed check/action transitions; source grades are never actor input."""
import argparse,html,json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
ARMS=('narrative_standard','matrix_standard','matrix_consistent')
def frame(rows,path,stage='D3',scripted=False):
 im=Image.new('RGB',(1600,850),'#10202e');d=ImageDraw.Draw(im)
 def txt(x,y,s,n=23,color='#e5f0f5'):
  f=None
  for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
   try:f=ImageFont.truetype(p,n);break
   except OSError:pass
  d.text((x,y),s,font=f,fill=color)
 txt(40,24,'HOW TO WIN AGENTS AND INFLUENCE SWARMS',32)
 txt(40,77,'Complete checks → accurate checks → consistent action',27,'#7cddd0')
 arms=ARMS if stage=='D3' else ARMS[1:];planned=6*len(arms)
 txt(40,124,f'{stage} | {len(rows)}/{planned} terminal | '+('SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'Native decisions; six dependent case clusters'),20)
 names=list(dict.fromkeys(r['case_id'] for r in rows))
 labels={'narrative_standard':'Prose / standard','matrix_standard':'Matrix / standard','matrix_consistent':'Matrix / consistency'}
 for j,a in enumerate(arms):txt(600+j*320,187,labels[a],22)
 for i in range(6):
  y=237+i*82;name=names[i] if i<len(names) else f'case {i+1} pending';txt(40,y,name.replace('transfer-','T-'),20)
  for j,a in enumerate(arms):
   r=next((r for r in rows if r['case_id']==name and r['arm']==a),None);x=595+j*320
   color='#274152' if not r else '#155448' if r['valid'] and r['evaluation']['acceptable_decision'] else '#713f40';d.rounded_rectangle((x,y-5,x+300,y+62),radius=8,fill=color)
   txt(x+10,y,r['decision']['choice'] if r and r['valid'] else 'INVALID' if r else 'PENDING',23)
   detail=('checks '+str(r['matrix_correct'])+'/15 | '+('contradiction' if r['matrix_contradiction'] else 'agrees')) if r and r['valid'] and r['matrix_correct'] is not None else ('acceptable' if r and r['valid'] and r['evaluation']['acceptable_decision'] else 'adverse' if r and r['valid'] else '')
   txt(x+10,y+33,detail,16)
 txt(40,760,'Colors grade raw actions against sources. Agreement with a matrix does not prove correctness.',21)
 txt(40,800,'Shadow purchase guard reported separately. Synthetic diagnostic; no S1 qualification.',20,'#a6bdcb');im.save(path)

def package(root,destination):
 root=Path(root);dest=Path(destination);dest.mkdir(parents=True,exist_ok=True);summary=json.loads((root/'summary.json').read_text());rows=json.loads((root/'outcomes.json').read_text());audits=json.loads((root/'audit.json').read_text());stage=summary['stage'];prefix='native-'+stage
 frame(rows,dest/(prefix+'-grid.png'),stage);allrows=[];frames=[]
 for i in range(6):
  for line in (root/f'events-{i}.jsonl').read_text().splitlines():
   e=json.loads(line)
   if e['kind']=='terminal':
    allrows.append(e['outcome']);p=dest/(prefix+'-tmp.png');frame(allrows,p,stage);frames.append(Image.open(p).copy())
 if frames:frames[0].save(dest/(prefix+'-01.gif'),save_all=True,append_images=frames[1:],duration=[700]*(len(frames)-1)+[3500],loop=0);p.unlink()
 data={'summary':summary,'rows':rows,'audits':audits,'events':[[json.loads(s) for s in (root/f'events-{i}.jsonl').read_text().splitlines()] for i in range(6)]};blob=json.dumps(data).replace('</','<\\/')
 page='''<!doctype html><html><meta charset="utf-8"><title>Candidate checks — influence swarms</title><style>body{background:#10202e;color:#e5f0f5;font:17px system-ui;max-width:1300px;margin:40px auto;padding:0 24px}h1{font-size:36px}p{line-height:1.6;color:#b8cbd6}table{border-collapse:collapse;width:100%;margin:20px 0}td,th{padding:12px;text-align:left;border-bottom:1px solid #385164}th{color:#7cddd0}.good{color:#83e1ba}.bad{color:#ffaaa0}button,select{padding:10px;background:#284759;color:white;border:1px solid #6a899e;border-radius:6px}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:#192f40;padding:15px;font-size:13px}details{margin:18px 0}img{max-width:100%}.cards{display:flex;gap:35px;flex-wrap:wrap}.cards b{font-size:30px;display:block}small{color:#acc2cf}</style><h1>Do complete checks lead to better decisions?</h1><p>How to win agents and influence swarms · <span id="stage"></span>. Six authored procurement cases. Separate checklist coverage, source accuracy and action consistency. These dependent diagnostic outcomes are not evidence that a swarm is generally robust.</p><div id="cards" class="cards"></div><h2>Raw decisions and the separate execution safeguard</h2><p>“Agrees” means the purchase does not contradict the model's matrix. A wrong matrix can still authorize a bad purchase. The shadow safeguard refuses an unsupported purchase; it never selects an alternative and is not counted as model reasoning.</p><div id="results"></div><h2>Inspect every check</h2><select id="case"></select><div id="checks"></div><h2>Recorded event replay</h2><p>Playback advances through saved events at a fixed cadence; recorded elapsed seconds show actual timing. Source grades appear only after answers. No agents are running in this replay.</p><button id="play">Play / pause</button> <button id="next">Next event</button> <input id="step" type="range" min="0" value="0" style="width:50%"><pre id="event"></pre><h2>Outcome sequence</h2><img src="PREFIX-01.gif" alt="Recorded terminal decisions"><p>All native calls, including invalid/adverse outcomes, are retained. D3 repeats frozen D2 observations; D4, if admitted, uses fresh numeric variants without inherited team reports. No cohort pooling or S1 qualification.</p><script>const D=DATA;document.getElementById('stage').textContent=D.summary.stage;document.getElementById('cards').innerHTML=`<div><b>${D.summary.matrix_correct}/90</b>correct matrix fields</div><div><b>${D.summary.valid}/${D.summary.planned}</b>valid decisions</div><div><b>$${D.summary.actual_usd.toFixed(4)}</b>reported model cost</div>`;const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));document.getElementById('results').innerHTML='<table><tr><th>Case / arm</th><th>Raw choice</th><th>Source grade</th><th>Matrix agreement</th><th>Shadow choice / grade</th></tr>'+D.rows.map(r=>`<tr><td>${esc(r.case_id)}<br><small>${esc(r.arm)}</small></td><td>${esc(r.decision?.choice||'INVALID')}</td><td class="${r.evaluation?.acceptable_decision?'good':'bad'}">${r.valid?(r.evaluation.acceptable_decision?'acceptable':'adverse'):'invalid'}</td><td>${r.matrix_contradiction===null?'—':r.matrix_contradiction?'contradicts':'agrees'}</td><td>${r.guarded_choice?esc(r.guarded_choice)+' / '+(r.guarded_evaluation.acceptable_decision?'acceptable':'adverse'):'—'}</td></tr>`).join('')+'</table>';const picker=document.getElementById('case');picker.innerHTML=D.audits.map((a,i)=>`<option value="${i}">${esc(a.case_id)}</option>`).join('');function inspect(){const a=D.audits[+picker.value];let s='<table><tr><th>Candidate / requirement</th><th>Model status</th><th>Source status</th></tr>';for(const [n,v] of Object.entries(a.source_checks))for(const [f,g] of Object.entries(v)){let m=a.matrix?.candidate_checks[n]?.[f]||'MISSING';s+=`<tr><td>${esc(n)} / ${esc(f)}</td><td class="${m===g?'good':'bad'}">${esc(m)}</td><td>${esc(g)}</td></tr>`}s+='</table><details><summary>Model notes and citations</summary><pre>'+esc(JSON.stringify(a.matrix,null,2))+'</pre></details>';document.getElementById('checks').innerHTML=s}picker.onchange=inspect;inspect();const E=D.events.flatMap((ee,i)=>ee.map(e=>({case:D.audits[i].case_id,...e})));const slider=document.getElementById('step');slider.max=E.length-1;function show(){document.getElementById('event').textContent=JSON.stringify(E[+slider.value],null,2)}slider.oninput=show;document.getElementById('next').onclick=()=>{slider.value=Math.min(+slider.max,+slider.value+1);show()};let timer;document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null}else timer=setInterval(()=>{if(+slider.value>=+slider.max){clearInterval(timer);timer=null;return}slider.value=+slider.value+1;show()},600)};show();</script></html>'''.replace('PREFIX',prefix).replace('DATA',blob)
 (dest/(prefix+'-overview.html')).write_text(page)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('destination');a=p.parse_args();package(a.root,a.destination)
