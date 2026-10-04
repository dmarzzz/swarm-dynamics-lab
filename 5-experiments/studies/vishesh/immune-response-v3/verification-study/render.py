"""Saved-data paired timeline; rendering never contacts a model or fleet."""
import argparse,json
from pathlib import Path

def render(source,out,kind="offline"):
    if kind not in ("offline","native"):raise ValueError("unknown_evidence_kind")
    rows=json.loads(Path(source).read_text())
    # JSON is data in a script element; escape HTML delimiters before embedding.
    data=json.dumps(rows).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    html='''<!doctype html><meta charset="utf-8"><title>Immune Response · offline instrument replay</title>
<style>body{font:16px system-ui;background:#101923;color:#edf2f5;max-width:1100px;margin:30px auto;padding:20px}h1{margin-bottom:4px}.note{color:#c7d0d9}select,button{font:inherit;padding:8px;margin:5px;background:#263b50;color:white;border:1px solid #7790a6;border-radius:6px}.grid{display:grid;grid-template-columns:1fr 1fr;gap:16px}article{background:#1c2b3a;padding:18px;border-radius:12px}dt{color:#aac0d2;margin-top:12px}dd{margin:4px 0;overflow-wrap:anywhere}.yes{color:#8ae0ae}.no{color:#ffb08e}#context{background:#233749;padding:14px;border-radius:8px;margin:16px 0}@media(max-width:700px){.grid{grid-template-columns:1fr}}</style>
<h1>Immune Response</h1><p class="note">Offline rule-controller replay · 0 native calls · feasibility evidence, not model qualification</p>
<label>Incident <select id="root"></select></label><label>Branch <select id="branch"><option>confirmed</option><option>contradicted</option></select></label><label>Repeat <select id="repeat"><option>1</option><option>2</option></select></label><label>Tick <select id="tick"><option>1</option><option>2</option></select></label><button id="play">Play timeline</button>
<p id="context"></p><div class="grid"><article id="raw"></article><article id="guarded"></article></div>
<p class="note">One request opportunity per tick. A deployment consumes that opportunity even if post-action health is restored. Protection from a guard does not establish model competence. Both repeats shown here are deterministic scripted replays.</p>
<script id="rows" type="application/json">ROWS</script><script>
const rows=JSON.parse(document.getElementById('rows').textContent),$=id=>document.getElementById(id);
const esc=x=>String(x).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
for(const root of [...new Set(rows.map(r=>r.root))]){const o=document.createElement('option');o.textContent=root;$('root').append(o)}
function draw(){const selected=rows.filter(r=>r.root===$('root').value&&r.branch===$('branch').value&&r.repeat===Number($('repeat').value));
$('context').textContent='Older report: process down. Fresh report: '+($('branch').value==='confirmed'?'failure confirmed; repair required.':'service recovered; preserve healthy operation.');
for(const guarded of [false,true]){const row=selected.find(r=>r.guarded===guarded),el=$(guarded?'guarded':'raw');if(!row){el.textContent='Missing assignment';continue}const x=row.trace[Number($('tick').value)-1];
const fields={'Proposed action':JSON.stringify(x.proposal),'Guard disposition':x.guard_reason,'Executed action':JSON.stringify(x.action),'Service healthy after action':Boolean(x.healthy),'Request opportunity served':Boolean(x.served_opportunity),'Outcome gate (episode)':row.post_state_gate,'Proposal contract (episode)':row.proposal_contract_pass,'Actual post-repair verification (episode)':row.post_action_verified===null?'Not applicable':row.post_action_verified};
el.innerHTML='<h2>'+ (guarded?'Explicit guard':'Unguarded')+'</h2><dl>'+Object.entries(fields).map(([k,v])=>'<dt>'+esc(k)+'</dt><dd>'+esc(v)+'</dd>').join('')+'</dl>'}}
for(const id of ['root','branch','repeat','tick'])$(id).onchange=draw;let timer=null;$('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;$('play').textContent='Play timeline'}else{$('tick').value='1';draw();timer=setInterval(()=>{$('tick').value=$('tick').value==='1'?'2':'1';draw()},1400);$('play').textContent='Pause'}};draw();
</script>'''
    if kind=='native':
        html=html.replace('Offline rule-controller replay · 0 native calls · feasibility evidence, not model qualification','Native verification comparison · qualification assessed separately from collection').replace('Both repeats shown here are deterministic scripted replays.','Repeats are fresh native contexts; inspect missingness and paired disagreement.').replace('offline instrument replay','native verification replay')
    Path(out).write_text(html.replace('ROWS',data))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--source',required=True);p.add_argument('--out',required=True);a=p.parse_args();render(a.source,a.out)
