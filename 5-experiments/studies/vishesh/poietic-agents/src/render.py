"""Dependency-free SVG progress and HTML event replay from recorded values only."""
import html
import json
from pathlib import Path


def qualification_png(summary, path, scripted=False):
    from PIL import Image, ImageDraw, ImageFont
    canvas=Image.new('RGB',(1600,720),'#101923');draw=ImageDraw.Draw(canvas)
    title=ImageFont.load_default(size=40);body=ImageFont.load_default(size=24)
    draw.text((55,42),'Poietic Agents | qualification',fill='#eff4f7',font=title)
    label='SCRIPTED - NOT MODEL EVIDENCE' if scripted else 'S0 qualification - not swarm efficacy'
    draw.text((55,105),label,fill='#b5c8d8',font=body)
    for i,(role,g) in enumerate(summary['contracts'].items()):
        y=190+i*140
        draw.text((55,y),role,fill='#eff4f7',font=body)
        draw.rectangle((395,y,1450,y+40),fill='#374453')
        if g['correct']:draw.rectangle((395,y,395+1055*g['correct']/48,y+40),fill='#54b5a7')
        draw.text((395,y+52),f"Correct {g['correct']}/48 | valid {g['schema_valid']}/48 | started {g['started']}/48",fill='#eff4f7',font=body)
    draw.text((55,650),'Per contract: >=44 correct, 48 valid, zero protected-access violations. All assignments retained.',fill='#b5c8d8',font=ImageFont.load_default(size=22))
    canvas.save(path)


def qualification_frame(summary, path, scripted=False):
    label='SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'S0 model qualification — not swarm efficacy'
    chunks=['<svg xmlns="http://www.w3.org/2000/svg" width="1600" height="720" viewBox="0 0 1600 720">',
            '<rect width="1600" height="720" fill="#101923"/>',
            '<g fill="#eff4f7" font-family="sans-serif">',
            '<text x="60" y="75" font-size="40">Poietic Agents · qualification</text>',
            f'<text x="60" y="120" font-size="23">{html.escape(label)}</text>']
    for i,(role,group) in enumerate(summary['contracts'].items()):
        y=205+i*145; correct=group['correct']; valid=group['schema_valid']
        chunks.extend([f'<text x="60" y="{y}" font-size="26">{html.escape(role)}</text>',
                       f'<rect x="400" y="{y-30}" width="1000" height="44" fill="#374453"/>',
                       f'<rect x="400" y="{y-30}" width="{1000*correct/48}" height="44" fill="#54b5a7"/>',
                       f'<text x="400" y="{y+50}" font-size="23">Correct {correct}/48 · valid {valid}/48 · started {group["started"]}/48</text>'])
    chunks+=['<text x="60" y="680" font-size="21">Threshold per contract: 44 correct, 48 valid, zero protected-access violations. All assignments retained.</text>','</g></svg>']
    Path(path).write_text(''.join(chunks))


def replay(frames, path, scripted=False):
    # Inline data is escaped before embedding; model text never becomes executable markup.
    data=json.dumps(frames).replace('<','\\u003c').replace('>','\\u003e').replace('&','\\u0026')
    label='SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'Recorded events — observer view'
    page='''<!doctype html><meta charset="utf-8"><title>Poietic Agents replay</title>
<style>body{background:#101923;color:#eff4f7;font:18px system-ui;margin:40px}button,input{font:inherit}#grid{display:grid;grid-template-columns:repeat(3,1fr);gap:18px}.agent{border:1px solid #607487;border-radius:12px;padding:20px}pre{white-space:pre-wrap}#metrics{font-size:22px;margin:22px 0}</style>
<h1>Poietic Agents</h1><p>LABEL</p><button id="play">Play</button> <input id="cursor" type="range" min="0" max="MAX" value="0"><span id="position"></span>
<div id="metrics"></div><div id="grid"></div><pre id="events"></pre>
<script>const frames=DATA;let timer=null;const c=document.getElementById('cursor');function draw(){const i=+c.value,f=frames[i];document.getElementById('position').textContent=` ${i+1}/${frames.length} · epoch ${f.epoch} · elapsed ${f.elapsed_s}s`;document.getElementById('metrics').textContent=`All assigned: ${f.assigned} · successes: ${f.successes} · actual cost: $${f.cost_usd}`;const g=document.getElementById('grid');g.replaceChildren();for(const a of f.agents){const e=document.createElement('div');e.className='agent';e.textContent=`${a.id} | ${a.model} | ${a.tools.length} tools | ${a.skills.length} skills`;g.append(e)}document.getElementById('events').textContent=JSON.stringify(f.events,null,2)}c.oninput=draw;document.getElementById('play').onclick=()=>{if(timer){clearInterval(timer);timer=null;return}timer=setInterval(()=>{c.value=(+c.value+1)%frames.length;draw()},1000)};draw()</script>'''
    Path(path).write_text(page.replace('LABEL',label).replace('MAX',str(len(frames)-1)).replace('DATA',data))
