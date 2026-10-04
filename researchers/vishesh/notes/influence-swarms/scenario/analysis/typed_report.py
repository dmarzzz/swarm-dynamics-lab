"""Independent reconciliation and honest fixture/native reports from saved D5 data."""
import argparse,html,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from typed_diagnostic import ARMS
from audit_approval import source_score
from dossier import digest

def live_frame(rows,path,scientific=False):
 from PIL import Image,ImageDraw,ImageFont
 im=Image.new('RGB',(1700,870),'#10202e');d=ImageDraw.Draw(im)
 def text(x,y,value,size=22,color='#e5f0f5'):
  font=None
  for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
   try:font=ImageFont.truetype(p,size);break
   except OSError:pass
  d.text((x,y),value,fill=color,font=font)
 text(35,28,'CITED FACTS → FIXED POLICY → PURCHASE AUTHORITY',34)
 text(35,83,'NATIVE D5 DIAGNOSTIC' if scientific else 'SCRIPTED — NOT MODEL EVIDENCE',26,'#e8c982')
 text(35,130,f'{len(rows)}/24 terminal decisions · six frozen development cases · raw choices below')
 names=list(dict.fromkeys(r['case_id'] for r in rows));labels=['Matrix / inherited','Facts / inherited','Matrix / records','Facts / records']
 for j,label in enumerate(labels):text(490+j*295,191,label,20)
 for i in range(6):
  name=names[i] if i<len(names) else 'case '+str(i+1)+' pending';y=245+i*82;text(35,y,name,19)
  for j,arm in enumerate(ARMS):
   r=next((r for r in rows if r['case_id']==name and r['arm']==arm),None);x=485+j*295;okay=r and r['valid'] and r['evaluation']['acceptable_decision'];d.rounded_rectangle((x,y-5,x+277,y+62),radius=8,fill='#155448' if okay else '#713f40' if r else '#294354');text(x+10,y,r['decision']['choice'] if r and r['valid'] else 'INVALID' if r else 'PENDING',23)
   if r and r['measurements']:text(x+10,y+33,str(r['measurements']['statuses_correct'])+'/15 source-correct checks',16)
 text(35,770,'Authorized actions are separate in the replay. Correct fixtures are software checks, not model results.',21)
 text(35,815,'No automatic follow-up. Excerpt verification supports this synthetic record grammar only.',20,'#acc2cf');im.save(path)

def reconcile(root):
 root=Path(root);s=json.loads((root/'summary.json').read_text());rows=json.loads((root/'outcomes.json').read_text());assert len(rows)==s['planned']==s['terminal']==24;assert digest(rows)==s['outcomes_hash'];cost=0;calls=0;events_total=0;observations=[]
 for i in range(6):
  case=json.loads((root/f'case-{i}.json').read_text());source,acceptable=source_score(case);ee=[json.loads(x) for x in (root/f'events-{i}.jsonl').read_text().splitlines()];events_total+=len(ee);requests=[e for e in ee if e['kind']=='request'];by_arm={a:[e['request'] for e in requests if e['arm']==a] for a in ARMS}
  for e in requests:
   assert digest(e['request'])==e['request_hash'];obs=e['request']['observation'];assert not set(obs)&{'evaluator','truth_hash','source_checks','acceptable','scorecard'}
  for context in ('inherited','records_only'):
   x,y=by_arm['matrix_'+context],by_arm['typed_'+context]
   if x and y:assert x[0]['observation']==y[0]['observation']
  for e in ee:
   if e['kind'] in ('response','call_error'):cost+=e['usage']['actual_usd'];calls+=e['usage']['calls']
  for r in [r for r in rows if r['case_id']==case['case_id']]:
   if r['valid']:
    assert bool(r['evaluation']['acceptable_decision'])==(r['decision']['choice'] in acceptable)
    assert bool(r['authorized_evaluation']['acceptable_decision'])==(r['authority']['action'] in acceptable)
    for n,v in source.items():assert v['feasible']==r['evaluation']['scorecard'][n]['feasible'];assert abs(v['total']-r['evaluation']['scorecard'][n]['total'])<.011
  observations.append({'case_id':case['case_id'],'source_acceptable':acceptable})
 assert abs(cost-s['actual_usd'])<1e-8 and calls==s['calls']
 return {'scientific':s['scientific'],'assigned':24,'terminal':len(rows),'source_grades_agree':True,'usage_reconciles':True,'matched_reviewer_observations':True,'events':events_total,'calls':calls,'cost_usd':cost,'cases':observations,'scope':'Same-author audit; independent Decimal primary-record arithmetic, not a new researcher approval.'}

def render(root,path):
 root=Path(root);s=json.loads((root/'summary.json').read_text());rows=json.loads((root/'outcomes.json').read_text());m=json.loads((root/'manifest.json').read_text());label='NATIVE D5 DIAGNOSTIC' if s['scientific'] else 'SCRIPTED — NOT MODEL EVIDENCE';audit=reconcile(root);(root/'reconciliation.json').write_text(json.dumps(audit,indent=2))
 data={'summary':s,'rows':rows,'audit':audit,'events':[[json.loads(x) for x in (root/f'events-{i}.jsonl').read_text().splitlines()] for i in range(6)]};blob=json.dumps(data).replace('</','<\\/')
 page='''<!doctype html><html><meta charset="utf-8"><title>D5 cited facts and purchase authority</title><style>body{font:17px system-ui;background:#10202e;color:#e5f0f5;max-width:1240px;margin:35px auto;padding:0 24px}p{line-height:1.6;color:#b9ccd8}.banner{padding:16px;background:#694719;color:#ffdc91;font-weight:bold}table{border-collapse:collapse;width:100%;margin:18px 0}th,td{border-bottom:1px solid #385368;padding:11px;text-align:left}.good{color:#8bdfb4}.bad{color:#ffaaa0}th{color:#7bdccd}select,button{background:#28485d;color:white;padding:9px;border:1px solid #789bad}pre{background:#193043;padding:16px;white-space:pre-wrap;overflow-wrap:anywhere;max-height:430px;overflow:auto}small{color:#acc2cf}</style><div class="banner">LABEL</div><h1>Cited facts → fixed buyer policy → explicit purchase authority</h1><p>All six frozen development cases; four paired workflows. Both reviewer architectures see identical evidence within each context. Raw recommendations and authorized actions remain separate. Excerpt verification understands only these synthetic document templates; it is not a general semantic verifier.</p><p id="summary"></p><label>Displayed action <select id="mode"><option value="raw">Raw model choice</option><option value="authority">Separate authorized action</option></select></label><div id="grid"></div><h2>Inspect a workflow</h2><select id="case"></select> <select id="arm"></select><div id="detail"></div><h2>Recorded event replay</h2><p>Use the slider to inspect actual retained events. The elapsed timestamps are recorded; no simulated agent activity is added.</p><input id="step" type="range" min="0" value="0" style="width:75%"><button id="next">Next event</button><pre id="event"></pre><script>const D=DATA;const A=['matrix_inherited','typed_inherited','matrix_records_only','typed_records_only'];const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));const names=D.audit.cases.map(c=>c.case_id);const $=x=>document.getElementById(x);$('summary').textContent=`${D.summary.valid}/24 valid decisions; ${D.summary.calls} ${D.summary.scientific?'native':'fixture'} calls; $${D.summary.actual_usd.toFixed(6)} reported provider cost. No automatic continuation or S1 qualification.`;function grid(){let t='<table><tr><th>Case</th>'+A.map(a=>'<th>'+a.replaceAll('_',' ')+'</th>').join('')+'</tr>';for(const n of names){t+='<tr><td>'+esc(n)+'</td>';for(const a of A){const r=D.rows.find(r=>r.case_id===n&&r.arm===a),raw=$('mode').value==='raw';const choice=raw?r.decision?.choice:r.authority?.action;const okay=raw?r.evaluation?.acceptable_decision:r.authorized_evaluation?.acceptable_decision;t+=`<td class="${okay?'good':'bad'}">${esc(choice||'INVALID')}<br><small>${r.measurements?r.measurements.statuses_correct+'/15 correct statuses':'not assessed'}</small></td>`}t+='</tr>'}$('grid').innerHTML=t+'</table>'}grid();$('mode').onchange=grid;$('case').innerHTML=names.map(n=>`<option>${esc(n)}</option>`).join('');$('arm').innerHTML=A.map(n=>`<option>${esc(n)}</option>`).join('');function detail(){const r=D.rows.find(r=>r.case_id===$('case').value&&r.arm===$('arm').value);let t='<p>Errors are retained. “Aligned” means the extracted value matches its candidate-specific cited excerpt under the template validator.</p>';if(r.compiled?.check_receipts){t+='<table><tr><th>Candidate / clause</th><th>Observed</th><th>Required</th><th>Status / reason</th></tr>';for(const [n,checks] of Object.entries(r.compiled.check_receipts))for(const [f,c]of Object.entries(checks))t+=`<tr><td>${esc(n)} / ${esc(f)}</td><td>${esc(JSON.stringify(c.observed))}</td><td>${esc(JSON.stringify(c.required))}</td><td>${esc(c.status)}<br><small>${esc(c.reason)}</small></td></tr>`;t+='</table>'}for(const [name,v]of Object.entries({'Model extraction/review':r.review,'Evidence alignment':r.compiled?.extraction_alignment,'Policy receipts':r.compiled?.check_receipts,'Raw decision':r.decision,'Separate purchase authority':r.authority,'Evaluation (not actor input)':r.measurements}))t+='<details><summary>'+esc(name)+'</summary><pre>'+esc(JSON.stringify(v??null,null,2))+'</pre></details>';$('detail').innerHTML=t}detail();$('case').onchange=detail;$('arm').onchange=detail;const E=D.events.flat();$('step').max=E.length-1;function event(){ $('event').textContent=JSON.stringify(E[+$('step').value],null,2)}event();$('step').oninput=event;$('next').onclick=()=>{$('step').value=Math.min(+$('step').max,+$('step').value+1);event()};</script></html>'''.replace('LABEL',label).replace('DATA',blob)
 Path(path).write_text(page)
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('root');p.add_argument('out');a=p.parse_args();render(a.root,a.out)
