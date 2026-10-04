"""Saved-data replay. No model, evaluator intervention or experimental RNG."""
import html
import json
from pathlib import Path


def render(directory):
    directory=Path(directory)
    packet=json.loads((directory/'packet.json').read_text())
    rows=json.loads((directory/'records.json').read_text())
    manifest=json.loads((directory/'manifest.json').read_text())
    summary=json.loads((directory/'summary.json').read_text())
    scripted=summary.get('origin')!='native-jev'
    title='SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'RD5 measured decision replay'
    by={r['id']:r for r in rows}
    data=[dict(a,record=by.get(a['id'])) for a in manifest]
    content=json.dumps(data,allow_nan=False).replace('<','\\u003c')
    caption=html.escape(json.dumps({k:summary[k] for k in ('stage','origin','assigned','terminal') if k in summary}))
    document='''<!doctype html><html lang="en"><meta charset="utf-8"><title>RD5 evidence and attention</title>
<style>body{font:16px system-ui;background:#0c1423;color:#edf3ff;margin:32px;max-width:1400px}h1{font-size:30px;margin-bottom:8px}.muted{color:#9fb1ca}table{border-collapse:collapse;width:100%;margin-top:24px}td,th{padding:12px;text-align:left;border-bottom:1px solid #2f4159}th{color:#9fb1ca}.HOLD{color:#ffb879}.PROCEED{color:#71e0bc}.DEFER{color:#b8bcff}.missing{color:#9fb1ca}input{width:360px}button{padding:8px 18px;background:#2a4266;color:white;border:0;border-radius:5px}code{font-size:13px}section{background:#142239;padding:18px;margin-top:20px;border-radius:12px}</style>
<h1>__TITLE__</h1><p class="muted">The right to reopen: evidence memory versus a protected future check.</p>
<p>Current action, historical action and evaluator truth are separate. DEFER is a noncompletion in H5. Missing outcomes remain assigned.</p>
<section><label>Reveal decision tick <input id="tick" type="range" min="0" max="3" value="3"> <strong id="label">6</strong></label> <button id="play">Play</button>
<p class="muted">A source receipt authorizes an inspection. It does not establish which action is correct. Truth below is reader-only.</p></section>
<table><thead><tr><th>Stream / policy</th><th>Tick</th><th>Current</th><th>Historical</th><th>Reader truth</th><th>Checks left</th><th>Receipt / inference</th><th>Outcome</th></tr></thead><tbody id="rows"></tbody></table>
<p class="muted"><code>__CAPTION__</code></p>
<script>const data=__DATA__;const slider=document.getElementById('tick');
function cell(tr,value,cls=''){const td=document.createElement('td');td.textContent=String(value??'—');td.className=cls;tr.append(td)}
function draw(){const t=Number(slider.value)*2;document.getElementById('label').textContent=t;const body=document.getElementById('rows');body.replaceChildren();for(const a of data){const r=a.record;if((a.epoch??0)*2>t)continue;const tr=document.createElement('tr');cell(tr,(a.root??a.id)+' / '+(a.arm??a.representation));cell(tr,r?.tick??a.epoch*2);cell(tr,r?.action??'UNSTARTED',r?.action??'missing');cell(tr,r?.historical_action);cell(tr,r?.truth);cell(tr,r?.available_checks);cell(tr,r?String(r.acquired??'n/a')+' / '+String(r.inference_attempted??'n/a'):'—');cell(tr,r?.reason??(r?.status??a.status));body.append(tr)}}
slider.addEventListener('input',draw);let timer;document.getElementById('play').onclick=()=>{clearInterval(timer);slider.value=0;draw();timer=setInterval(()=>{if(Number(slider.value)===3){clearInterval(timer);return}slider.value=Number(slider.value)+1;draw()},1200)};draw();</script></html>'''
    document=document.replace('__TITLE__',title).replace('__CAPTION__',caption).replace('__DATA__',content)
    (directory/'replay.html').write_text(document)
    # Source rows, including status and truth separation, also remain accessible in
    # records.json; this visual never substitutes for all-assigned arithmetic.
    return directory/'replay.html'
