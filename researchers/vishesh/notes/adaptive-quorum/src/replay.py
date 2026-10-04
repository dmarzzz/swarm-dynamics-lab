"""Self-contained local replay; no remote scripts or network requests."""
import json


def render(records, path):
    data = json.dumps(records).replace('<', '\\u003c')
    path.write_text('''<!doctype html><meta charset="utf-8"><title>Adaptive quorum replay</title>
<style>body{font:18px system-ui;background:#101820;color:#edf4f5;max-width:1000px;margin:35px auto}select,input{font:inherit}svg{width:100%;height:430px}text{fill:#edf4f5}line{stroke:#7babb8;stroke-width:2}circle{fill:#286674}pre{white-space:pre-wrap}</style>
<h1>Scout, compare, commit</h1><p id="label"></p><select id="episode"></select><input id="round" type="range" min="1" value="1"><span id="step"></span><svg viewBox="0 0 1000 430" id="scene"></svg><pre id="details"></pre>
<script>const rows=''' + data + ''';
const select=document.querySelector('#episode'),slider=document.querySelector('#round');
rows.forEach((r,i)=>{let o=document.createElement('option');o.value=i;o.textContent=`${r.task_id} / ${r.world} / deadline ${r.dose} / ${r.arm}`;select.append(o)});
function draw(){let r=rows[+select.value];slider.max=r.dose;let t=Math.min(+slider.value,r.dose),f=r.trace[t-1];document.querySelector('#label').textContent=`${r.backend} · Exploratory S0 · Fixed evidence delivery · Not a Jev result`;document.querySelector('#step').textContent=` Round ${t}/${r.dose}`;let s='';
for(let i=0;i<5;i++){let x=100+i*200,v=f.votes[i],j=['A','B','C'].indexOf(v);if(j>=0)s+=`<line x1="${x}" y1="100" x2="${250+j*250}" y2="310"/>`;s+=`<circle cx="${x}" cy="80" r="30"/><text text-anchor="middle" x="${x}" y="85">${i+1}</text><text text-anchor="middle" x="${x}" y="135">${f.reports[i].root}</text>`}['A','B','C'].forEach((v,i)=>s+=`<circle cx="${250+i*250}" cy="330" r="38"/><text text-anchor="middle" x="${250+i*250}" y="335">${v}</text>`);document.querySelector('#scene').innerHTML=s;
document.querySelector('#details').textContent=JSON.stringify({ballots:f.votes,central:f.central,final:r.decision,evaluator:r.evaluation,validity:r.validity},null,2)}select.onchange=()=>{slider.value=1;draw()};slider.oninput=draw;draw();</script>''')
