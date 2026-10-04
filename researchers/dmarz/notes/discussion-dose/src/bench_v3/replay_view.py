"""Self-contained local stage replay; untrusted model strings are never HTML."""
import json


def render(events, rows, destination):
    labels = {r['id'] for r in rows}
    steps = [e for e in events if e.get('label') in labels and e['kind'] in ('fork', 'checkpoint', 'delivery', 'merge', 'provider_failure', 'validation_failure')]
    # Shared acquisition is recorded once physically, but belongs at the start
    # of each fork's visual history. Preserve the original event index.
    for row in rows:
        if row['kind'] != 'swarm': continue
        acquisition = f'{row["world"]}:{int(row["attack"])}:acquisition'
        steps += [{**e, 'label': row['id'], 'shared_acquisition': True} for e in events
                  if e.get('label') == acquisition and e['kind'] in ('tool_read', 'checkpoint', 'provider_failure', 'validation_failure')]
    steps += [{'kind': 'terminal', 'label': r['id'], 'record': r, 'seq': max((e['seq'] for e in events if e['kind'] == 'terminal' and e['record']['id'] == r['id']), default=0)} for r in rows]
    steps.sort(key=lambda e: e['seq'])
    payload = json.dumps({'steps': steps, 'rows': rows}, sort_keys=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = '''<!doctype html><meta charset="utf-8"><title>Discussion benchmark v3 — offline replay</title>
<style>body{font:16px system-ui;margin:32px auto;max-width:1100px;padding:0 24px;background:#f6f6f2;color:#20252a}h1{font-size:28px}select,button{font:inherit;padding:8px;margin:8px 8px 8px 0}input{width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:20px;border:1px solid #ddd;border-radius:8px}#summary{font-weight:600}label{display:block;margin-top:20px}#visual{background:white;padding:24px;border:1px solid #dadfdc;border-radius:12px;margin:16px 0;overflow:auto}table{width:100%;border-collapse:collapse}td,th{text-align:left;padding:12px;border-bottom:1px solid #e0e5e1}th{color:#52655b}h2{margin-top:0}summary{cursor:pointer;color:#52655b}</style>
<h1>Discussion & memory benchmark v3</h1><p>Local trace replay. Scripted runs test the instrument; they are not model findings. Evaluator labels shown here never enter agent requests.</p>
<label>Episode <select id="episode"></select></label><button id="play">Play</button><button id="back">Previous</button><button id="next">Next</button><input id="cursor" type="range" aria-label="Replay position" min="0" step="1"><p id="summary"></p><section id="visual"></section><details><summary>Recorded event data</summary><pre id="stage"></pre></details>
<script id="data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('data').textContent), select=document.getElementById('episode'), slider=document.getElementById('cursor');
let steps=[], timer=null;
for(const row of data.rows){const opt=document.createElement('option');opt.value=row.id;opt.textContent=row.id;select.append(opt)}
function show(){const e=steps[Number(slider.value)],visual=document.getElementById('visual');visual.replaceChildren();
  const add=(tag,text,parent=visual)=>{const node=document.createElement(tag);node.textContent=text;parent.append(node);return node};
  const table=(headers,rows)=>{const t=document.createElement('table');visual.append(t);const head=document.createElement('tr');t.append(head);headers.forEach(h=>add('th',h,head));rows.forEach(row=>{const tr=document.createElement('tr');t.append(tr);row.forEach(v=>add('td',v===null?'Unknown / abstain':String(v),tr))})};
  document.getElementById('summary').textContent=e?`${Number(slider.value)+1} / ${steps.length} · event ${e.seq}`:'No recorded events';document.getElementById('stage').textContent=e?JSON.stringify(e,null,2):'Unavailable';if(!e)return;
  if(e.kind==='tool_read'){add('h2','Private evidence received');add('p',`Agent ${e.agent+1} · ${e.document.authority} source · version ${e.document.version}`);table(['Fact','Value'],Object.entries(e.document.facts))}
  else if(e.kind==='checkpoint'){add('h2',e.stage==='private_initial'?'Before sharing':e.turn===0?'After the shared reports':`After round ${e.turn}`);add('p',`Team choice: ${e.state.decision} · Valid ballots: ${e.state.valid_ballots}/3 · False endorsements: ${e.state.false_endorsements}`);table(['Agent','Choice','Contested value','Choice follows own claims'],e.state.votes.map((v,i)=>[i+1,v,e.state.target_values[i],e.state.vote_claim_consistency[i]]))}
  else if(e.kind==='fork'){add('h2','Comparison starts');add('p','This arm continues from the same recorded starting state as its paired arms.')}
  else if(e.kind==='delivery'){add('h2',e.mode==='board'?'Peer messages delivered':'Private work recorded');table(['Agent','Message'],e.posts.map(p=>[p.agent+1,p.unavailable?'Unavailable':p.message]))}
  else if(e.kind==='merge'){add('h2','Memory passed to the parent');if(!e.memory.length)add('p','No facts reached the fixed majority threshold.');else table(['Fact','Value','Endorsing agents','Cited records'],e.memory.map(r=>[r.key,r.value,r.agents.length,r.sources.length]))}
  else if(e.kind==='terminal'){const r=e.record,m=r.evaluation;add('h2','Final outcome');const answer=r.parent??r.answer;add('p',r.kind==='diagnostic'?`Single-agent choice: ${answer?.vote??'Invalid'}`:`Parent answer: ${answer===null?'Invalid / unavailable':answer?.value??'Abstain'}`);const names={vote_correct:'Team choice correct',memory_false_records:'False facts in memory',memory_required_coverage:'Required fact retained',parent_groundtruth_wrong:'Parent answer wrong against truth',parent_unsupported:'Parent answer unsupported by memory',parent_inherited_error:'Grounded inherited error',parent_correct_abstain:'Correct abstention',parent_invalid:'Invalid parent response',justified:'Evidence-justified decision'};table(['Measure','Recorded value'],Object.entries(names).filter(([k])=>k in m).map(([k,name])=>[name,m[k]]))}
  else{add('h2','Observation unavailable');add('p','A failed call remains in the assigned ledger. It is not counted as a safe abstention.')}
}
function choose(){steps=data.steps.filter(e=>e.label===select.value);slider.max=Math.max(0,steps.length-1);slider.value=0;show()}
function advance(delta){slider.value=Math.min(Number(slider.max),Math.max(0,Number(slider.value)+delta));show()}
select.onchange=choose;slider.oninput=show;document.getElementById('back').onclick=()=>advance(-1);document.getElementById('next').onclick=()=>advance(1);
document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}else{if(slider.value===slider.max)slider.value=0;timer=setInterval(()=>{advance(1);if(slider.value===slider.max){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}},850);document.getElementById('play').textContent='Pause'}};choose();
</script>'''
    destination.write_text(page.replace('PAYLOAD', payload), encoding='utf-8')
