"""Replay only recorded events. Fixture provenance is visible in every view."""
import argparse
import json
from pathlib import Path

PAGE = '''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Swarm of Theseus — procedure continuity</title>
<style>body{margin:0;background:#101921;color:#e8f0f2;font:16px system-ui}main{max-width:1200px;margin:auto;padding:32px}h1{font-size:34px;margin:8px 0}.muted{color:#aabac6}#provenance{position:sticky;top:0;background:#54340b;color:#ffe0a0;padding:12px;z-index:2;font-weight:700}select,button,input{font:inherit;margin:4px;padding:8px;background:#213441;color:white;border:1px solid #7c939d;border-radius:5px}.grid{display:grid;grid-template-columns:repeat(3,1fr);gap:12px}.card{background:#1b2c38;padding:16px;border-radius:8px;overflow-wrap:anywhere}.note{font-size:13px;white-space:pre-wrap;max-height:140px;overflow:auto}table{border-collapse:collapse;width:100%;font-size:14px}td,th{text-align:left;padding:10px;border-bottom:1px solid #41545e}.good{color:#72dfb6}.bad{color:#ffb68e}svg{width:100%;height:180px;background:#162630}#step{width:45%}@media(max-width:700px){.grid{grid-template-columns:1fr}main{padding:15px}}</style>
<div id="provenance"></div><main><div class="muted">SOC-24 · Exploratory instrument · Two complete replacements</div><h1>Swarm of Theseus</h1><p>Does an inherited procedure still work—and can successors correct it?</p><label>World <select id="world"></select></label><label>Condition <select id="arm"></select></label><button id="play">Play</button><input id="step" aria-label="Logical step" type="range" min="0" max="9" value="0"><span id="stepLabel"></span><p id="event" class="muted"></p><div id="crew" class="grid"></div><h2>Behavior across replacements</h2><p class="muted">Class A (orange) changes its rule at step 5. Class B (green) stays valid. Migration changes commands only. Gaps have no line.</p><svg id="chart" viewBox="0 0 1000 180" role="img" aria-label="Accuracy by service class and logical step"></svg><h2>Decision evidence</h2><p class="muted">Evaluator truth below is shown to viewers after the decision; it is withheld from actors for current cases.</p><div style="overflow:auto"><table><thead><tr><th>Case / class</th><th>Claim</th><th>Independent evidence</th><th>Crew action</th><th>Evaluator / outcome</th></tr></thead><tbody id="cases"></tbody></table></div><h2>Inherited record</h2><pre id="archive" class="card note"></pre><p class="muted">This bounded simulator measures learned procedural transmission. It does not establish emergent culture, a swarm advantage, or cross-model portability.</p></main><script>
const DATA=__DATA__;
const $=x=>document.getElementById(x), worlds=[...new Set(DATA.events.map(e=>e.scenario+':'+e.seed))];
$('provenance').textContent=DATA.fixture?'SCRIPTED — NOT MODEL EVIDENCE · unit-test interface fixture':'RECORDED MODEL OUTPUTS · exploratory; inspect missingness and qualification';
function opts(id,values){$(id).replaceChildren();values.forEach(v=>{let o=document.createElement('option');o.value=v;o.textContent=v;$(id).append(o)})}
opts('world',worlds);function setArms(){opts('arm',[...new Set(DATA.events.filter(e=>e.scenario+':'+e.seed===$('world').value).map(e=>e.arm))]);draw()}
function trajectory(){return DATA.events.filter(e=>e.scenario+':'+e.seed===$('world').value&&(e.arm===$('arm').value||e.step<2&&e.arm==='acquisition')).sort((a,b)=>a.step-b.step)}
function text(tag,value,parent,cls){let el=document.createElement(tag);el.textContent=value;if(cls)el.className=cls;parent.append(el);return el}
function svg(tag,attrs){let e=document.createElementNS('http://www.w3.org/2000/svg',tag);Object.entries(attrs).forEach(([k,v])=>e.setAttribute(k,v));$('chart').append(e);return e}
function draw(){let step=+$('step').value,es=trajectory(),e=es.find(x=>x.step===step);$('stepLabel').textContent='Step '+step+' / 9';$('event').textContent=step<2?'Shared acquisition':step<=7?'Replacement '+(step-1)+' of 6'+(step>=5?' · environment/interface changed':''):'All founders and first descendants gone';if(step>=6)$('event').textContent+=' · new outcome feedback withheld';$('crew').replaceChildren();$('cases').replaceChildren();$('archive').textContent='No recorded event';$('chart').replaceChildren();
[0,.5,1].forEach(v=>{svg('line',{x1:50,x2:970,y1:150-v*120,y2:150-v*120,stroke:'#41545e'});svg('text',{x:5,y:155-v*120,fill:'#aabac6'}).textContent=Math.round(v*100)+'%'});
['A','B'].forEach((cls,i)=>{let prev=null;es.forEach(ev=>{let rows=ev.scores.filter(r=>r.class===cls);if(!rows.length){prev=null;return}let obs=rows.filter(r=>r.observed).length;if(!obs){prev=null;return}let x=60+ev.step*99,y=150-rows.filter(r=>r.correct).length/rows.length*120,col=i?'#72dfb6':'#ffb68e';if(prev&&ev.step===prev.step+1)svg('line',{x1:prev.x,y1:prev.y,x2:x,y2:y,stroke:col,'stroke-width':3});svg('circle',{cx:x,cy:y,r:5,fill:col});prev={x,y,step:ev.step}})});svg('line',{x1:60+step*99,x2:60+step*99,y1:10,y2:165,stroke:'#fff','stroke-dasharray':'4 4'});
if(!e){text('p','Missing event: no outcome is imputed.',$('crew'));return}
(e.crew_before||[{id:'qualification reader',generation:'—',notebook:''}]).forEach(m=>{let c=text('div','',$('crew'),'card');text('strong',m.id,c);text('p','Generation '+m.generation,c);text('p',m.onboarding?'Archive parent '+m.onboarding.id.slice(0,12):'Private notes / no new onboarding',c,'muted');text('div',m.notebook||'(No private notebook)',c,'note')});
e.cases.forEach(c=>{let r=e.scores.find(r=>r.id===c.id),tr=document.createElement('tr');$('cases').append(tr);text('td',c.id.split(':').slice(-2).join(' / '),tr);text('td',c.summary,tr);text('td',Object.entries(c.evidence).map(([s,v])=>s+': '+(v.signal?'positive':'negative')+(v.fresh?' / fresh':' / stale')).join('; '),tr);let cell=text('td',r.action??'MISSING / NO MAJORITY',tr);let raw=e.calls.map(call=>{let ds=call.result.value?.decisions;return Array.isArray(ds)?ds.filter(d=>d&&d.id===c.id).map(d=>d.command).join(', '):'no output'}).join(' | ');text('div',raw,cell,'muted');text('td',r.truth+' · '+(r.correct?'correct':r.observed?'incorrect':'missing'),tr,r.correct?'good':'bad')});$('archive').textContent=e.archive?e.archive.text:'No shared archive in one-reader qualification';}
let timer=null;$('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;$('play').textContent='Play'}else{$('play').textContent='Pause';timer=setInterval(()=>{$('step').value=(+$('step').value+1)%10;draw()},1200)}};$('step').oninput=draw;$('world').onchange=setArms;$('arm').onchange=draw;setArms();</script></html>'''


def render(root):
    root = Path(root)
    manifest = json.loads((root / 'manifest.json').read_text())
    fixture = manifest.get('evidence_type') == 'unit_fixture'
    if manifest.get('evidence_type') not in ('unit_fixture', 'measured_model_outputs'):
        raise ValueError('explicit_evidence_provenance_required')
    events = [json.loads(p.read_text()) for p in sorted((root / 'events').glob('*.json'))]
    data = json.dumps({'fixture': fixture, 'events': events}).replace('<', '\\u003c')
    (root / 'replay.html').write_text(PAGE.replace('__DATA__', data))
    from PIL import Image, ImageDraw, ImageFont
    image = Image.new('RGB', (1800, 1000), '#101921'); draw = ImageDraw.Draw(image)
    try:
        font = ImageFont.truetype('DejaVuSans.ttf', 27); title = ImageFont.truetype('DejaVuSans.ttf', 48)
    except OSError:
        font = ImageFont.load_default(size=27); title = ImageFont.load_default(size=48)
    label = 'SCRIPTED | NOT MODEL EVIDENCE' if fixture else 'RECORDED MODEL OUTPUTS | EXPLORATORY'
    draw.rectangle((0, 0, 1800, 80), fill='#54340b'); draw.text((45, 20), label, font=font, fill='#ffe0a0')
    draw.text((55, 115), 'Swarm of Theseus · procedure continuity', font=title, fill='white')
    draw.text((55, 190), 'Two complete replacements. Preserve valid checks; retire obsolete rules.', font=font, fill='#aabac6')
    if events:
        last = sorted(events, key=lambda e: (e['step'], e['run']))[-1]
        draw.text((55, 260), f"{last['scenario']} / world {last['seed']} / {last['arm']} / step {last['step']}", font=font, fill='white')
        for i, row in enumerate(last['scores']):
            y = 330 + i * 80
            text = f"Case {i+1}: action {row.get('action') or 'MISSING'} | evaluator {row['truth']} | " + ('correct' if row['correct'] else 'incorrect' if row['observed'] else 'missing')
            draw.text((70, y), text, font=font, fill='#72dfb6' if row['correct'] else '#ffb68e')
        draw.text((55, 860), 'Truth displayed after scoring; withheld from current actor inputs.', font=font, fill='#aabac6')
    else:
        draw.text((55, 350), 'No recorded events. No outcome inferred.', font=font, fill='#ffb68e')
    draw.text((55, 930), 'Open replay.html for roster, ancestry, evidence, actions and time controls.', font=font, fill='#aabac6')
    image.save(root / 'summary.png')


if __name__ == '__main__':
    p = argparse.ArgumentParser(); p.add_argument('root'); a = p.parse_args(); render(a.root)
