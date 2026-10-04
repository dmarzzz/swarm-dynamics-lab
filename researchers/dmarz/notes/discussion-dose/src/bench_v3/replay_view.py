"""Self-contained local stage replay; untrusted model strings are never HTML."""
import json


def render(events, rows, destination):
    labels = {r['id'] for r in rows}
    steps = [e for e in events if e.get('label') in labels and e['kind'] in ('fork', 'checkpoint', 'delivery', 'merge', 'provider_failure', 'validation_failure')]
    steps += [{'kind': 'terminal', 'label': r['id'], 'record': r, 'seq': max((e['seq'] for e in events if e['kind'] == 'terminal' and e['record']['id'] == r['id']), default=0)} for r in rows]
    steps.sort(key=lambda e: e['seq'])
    payload = json.dumps({'steps': steps, 'rows': rows}, sort_keys=True).replace('<', '\\u003c').replace('>', '\\u003e').replace('&', '\\u0026')
    page = '''<!doctype html><meta charset="utf-8"><title>Discussion benchmark v3 — offline replay</title>
<style>body{font:16px system-ui;margin:32px auto;max-width:1100px;padding:0 24px;background:#f6f6f2;color:#20252a}h1{font-size:28px}select,button{font:inherit;padding:8px;margin:8px 8px 8px 0}input{width:100%}pre{white-space:pre-wrap;overflow-wrap:anywhere;background:white;padding:20px;border:1px solid #ddd;border-radius:8px}#summary{font-weight:600}label{display:block;margin-top:20px}</style>
<h1>Discussion & memory benchmark v3</h1><p>Local trace replay. Scripted runs test the instrument; they are not model findings. Evaluator labels shown here never enter agent requests.</p>
<label>Episode <select id="episode"></select></label><button id="play">Play</button><button id="back">Previous</button><button id="next">Next</button><input id="cursor" type="range" min="0" step="1"><p id="summary"></p><pre id="stage"></pre>
<script id="data" type="application/json">PAYLOAD</script><script>
const data=JSON.parse(document.getElementById('data').textContent), select=document.getElementById('episode'), slider=document.getElementById('cursor');
let steps=[], timer=null;
for(const row of data.rows){const opt=document.createElement('option');opt.value=row.id;opt.textContent=row.id;select.append(opt)}
function show(){const e=steps[Number(slider.value)];document.getElementById('summary').textContent=e?`${Number(slider.value)+1} / ${steps.length} · ${e.kind} · event ${e.seq}`:'No recorded events';document.getElementById('stage').textContent=e?JSON.stringify(e.kind==='terminal'?{outcome:e.record.evaluation,parent:e.record.parent??e.record.answer,memory:e.record.memory}:e,null,2):'Unavailable';}
function choose(){steps=data.steps.filter(e=>e.label===select.value);slider.max=Math.max(0,steps.length-1);slider.value=0;show()}
function advance(delta){slider.value=Math.min(Number(slider.max),Math.max(0,Number(slider.value)+delta));show()}
select.onchange=choose;slider.oninput=show;document.getElementById('back').onclick=()=>advance(-1);document.getElementById('next').onclick=()=>advance(1);
document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}else{if(slider.value===slider.max)slider.value=0;timer=setInterval(()=>{advance(1);if(slider.value===slider.max){clearInterval(timer);timer=null;document.getElementById('play').textContent='Play'}},850);document.getElementById('play').textContent='Pause'}};choose();
</script>'''
    destination.write_text(page.replace('PAYLOAD', payload), encoding='utf-8')
