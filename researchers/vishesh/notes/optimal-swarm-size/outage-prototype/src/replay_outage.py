"""Self-contained trace player; renders observations, never invents model activity."""
import json
from pathlib import Path

def render(record,path,origin='native'):
    data=json.dumps(record).replace('<','\\u003c')
    html='''<!doctype html><meta charset="utf-8"><title>Outage / trace replay</title><style>
body{background:#111521;color:#dfe6f8;font:16px system-ui;margin:40px;max-width:1100px}h1{font-weight:500}button,input{accent-color:#ac9aff}button{background:#ac9aff;border:0;padding:10px 20px;border-radius:5px}#cards{display:flex;flex-wrap:wrap;gap:14px;margin:25px 0}.card{border:1px solid #5d6379;border-radius:8px;padding:20px;flex:1;min-width:170px;transition:background .35s}.up{background:#153f3a}.down{background:#502831}pre{white-space:pre-wrap;font-size:12px;max-height:330px;overflow:auto}small{color:#a9b4cc}</style>
<small>SWARM LAB / CONTROLLED OUTAGE EMULATOR</small><h1>Repair, recheck, recover.</h1><p id="label"></p><button id="play">Play</button> <input id="seek" type="range" min="0" value="0"><span id="tick"></span><div id="cards"></div><p id="summary"></p><details><summary>Exact tool receipts</summary><pre id="receipts"></pre></details><p><small>Animation interpolates saved states only. Simulation ticks are not physical seconds.</small></p><script>
const r=DATA,origin=ORIGIN,frames=r.events.filter(e=>e.kind==='step');let i=0,timer;
const q=id=>document.getElementById(id);q('seek').max=Math.max(0,frames.length-1);q('label').textContent=origin+' · '+(r.label||r.arm)+' · '+r.case_id;
function show(){const f=frames[i];q('tick').textContent=f?' tick '+f.tick:' no completed simulation ticks';q('cards').replaceChildren();if(f)Object.entries(f.health).forEach(([name,ok])=>{const d=document.createElement('div');d.className='card '+(ok?'up':'down');d.textContent=name+' / '+(ok?'healthy':'impaired');q('cards').append(d)});q('receipts').textContent=JSON.stringify(f?.receipts||[],null,2);q('summary').textContent='Final: '+(r.failure?'operational failure / '+r.failure:r.evaluation.success?'success':'task incomplete')+' · policy turns submitted: '+r.model_calls+' · stale writes: '+r.stale_writes;q('seek').value=i;}
q('seek').oninput=e=>{i=+e.target.value;show()};q('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;return}i=0;show();timer=setInterval(()=>{if(i>=frames.length-1){clearInterval(timer);timer=null;return}i++;show()},700)};show();</script>'''.replace('DATA',data).replace('ORIGIN',json.dumps(origin))
    Path(path).write_text(html)
