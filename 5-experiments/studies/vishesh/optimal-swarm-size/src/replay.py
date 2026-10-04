"""Standalone replay of recorded service intervals; no generated agent trajectories."""
import html
import json
import math
from pathlib import Path


def render(trace_path,out_path,record=None):
    events=[json.loads(line) for line in Path(trace_path).read_text().splitlines() if line.strip()]
    events=[e for e in events if type(e.get('t')) in (float,int) and math.isfinite(e['t']) and e['t']>=0]
    duration=max([e['t'] for e in events]+[0.001]);active={};segments=[]
    for e in events:
        key=(e.get('actor'),e.get('phase'),e.get('item'))
        if e['kind']=='service_start':active[key]=e
        if e['kind']=='service_end' and key in active:
            start=active.pop(key);segments.append(dict(actor=e['actor'],phase=e['phase'],item=e.get('item'),start=start['t'],end=e['t'],incomplete=False))
    for key,start in active.items():
        segments.append(dict(actor=key[0],phase=key[1],item=key[2],start=start['t'],end=None,incomplete=True))
    data=json.dumps({'duration':duration,'segments':segments}).replace('<','\\u003c')
    summary=''
    if record is not None:
        row=record['assignment'];valid=bool(record.get('operational_success'))
        label='TASK SUCCESS' if valid else 'TASK UNSUCCESSFUL'
        summary='<p style="color:'+('#8ee2ab' if valid else '#ff9e9e')+'">'+html.escape(f"{label} · {row['structure']} root {row['root']} · arm {row.get('arm','roster')} · N={row['n']} · used contexts {len(record['used_contexts'])} · quality {record['evaluation']['quality']:.3f} · exposure ${record['exposure_microdollars']/1e6:.6f}")+html.escape(f" · correct items/s {record.get('correct_items_per_second','not recorded')}")+'</p><p>Quality and cost are final episode totals, not interpolated intermediate measurements.</p>'
    rows=''.join('<tr>'+''.join('<td>'+html.escape(str(s[k]))+'</td>' for k in ('actor','phase','item','start','end','incomplete'))+'</tr>' for s in segments)
    page='''<!doctype html><meta charset="utf-8"><title>Swarm-size measured replay</title>
<style>body{background:#100c18;color:#eae6f0;font:16px system-ui;margin:32px}input{width:90%}.lane{height:38px;border-bottom:1px solid #443b50;position:relative;margin:10px 0 10px 90px}.label{position:absolute;left:-85px}.bar{position:absolute;top:5px;height:22px;background:#43c7e6}.bar.integration{background:#b08bea}.bar.incomplete{background:#e86b75}table{width:100%;font:12px monospace}td,th{text-align:left;padding:8px}#readout{font-variant-numeric:tabular-nums}</style>
<h1>Recorded agent service</h1>SUMMARY<button id="play">Play measured timeline</button><p>Elapsed wall time. Bars show model-request intervals, including provider latency; gaps do not prove an actor was idle. Red intervals lack a recorded end. No simulated movement or interpolated outcomes.</p><label for="time">Inspect elapsed seconds</label><input id="time" type="range" min="0" step="any"><output id="readout"></output><div id="lanes"></div><details><summary>Static interval table</summary><table><tr><th>Actor</th><th>Phase</th><th>Item</th><th>Start</th><th>End</th><th>Incomplete</th></tr>ROWS</table></details>
<script>const data=DATA;const slider=document.querySelector('#time');slider.max=data.duration;slider.value=data.duration;
function draw(){const t=Number(slider.value);document.querySelector('#readout').textContent=t.toFixed(2)+' s';const lanes=document.querySelector('#lanes');lanes.replaceChildren();const actors=[...new Set(data.segments.map(s=>s.actor))].sort((a,b)=>a-b);for(const actor of actors){const lane=document.createElement('div');lane.className='lane';const label=document.createElement('span');label.className='label';label.textContent='Actor '+actor;lane.append(label);for(const s of data.segments.filter(s=>s.actor===actor&&s.start<=t)){const bar=document.createElement('span');bar.className='bar'+(s.phase==='integrate'?' integration':'')+(s.incomplete?' incomplete':'');bar.style.left=(100*s.start/data.duration)+'%';bar.style.width=(100*Math.max(0,Math.min(t,s.end??data.duration)-s.start)/data.duration)+'%';bar.title=s.phase+' '+(s.item??'')+(s.incomplete?' (end missing)':'');lane.append(bar)}lanes.append(lane)}}let playing=false,last=0;const play=document.querySelector('#play');play.onclick=()=>{playing=!playing;play.textContent=playing?'Pause':'Play measured timeline';if(playing&&Number(slider.value)>=data.duration)slider.value=0;last=performance.now();};function tick(now){if(playing){slider.value=Math.min(data.duration,Number(slider.value)+(now-last)/1000);draw();if(Number(slider.value)>=data.duration){playing=false;play.textContent='Replay measured timeline';}}last=now;requestAnimationFrame(tick);}requestAnimationFrame(tick);slider.addEventListener('input',draw);draw();</script>'''
    Path(out_path).write_text(page.replace('SUMMARY',summary).replace('ROWS',rows).replace('DATA',data))
    return segments
