"""Recorded metrics only; no invented points, no spatial culture metaphor."""
import json
from pathlib import Path

def image(row,path):
    from PIL import Image,ImageDraw,ImageFont
    im=Image.new('RGB',(1600,900),'#101827');d=ImageDraw.Draw(im)
    try:font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',28);small=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf',22)
    except OSError:font=small=ImageFont.load_default()
    d.text((60,35),'Swarm of Theseus | '+row['scenario']+' | '+row['arm']+' | seed '+str(row['seed']),fill='white',font=font)
    colors={'accuracy':'#6fe3be','convention':'#f9c66b','turnover':'#94aafa'}
    hist=row.get('history',[])
    for k,(metric,color) in enumerate(colors.items()):
        y0=150+k*230;d.text((60,y0),metric+' (0 - 100%)',fill=color,font=font)
        d.line((400,y0+150,1450,y0+150),fill='#68778c',width=2)
        for f in hist:
            x=425+f['step']*190;value=f[metric];d.rectangle((x,y0+150-value*130,x+95,y0+150),fill=color)
            d.text((x,y0+160),str(f['step']),fill='white',font=small)
            d.text((x,y0+120-value*130),str(round(value*100))+'%',fill=color,font=small)
    d.text((60,850),'Steps 1-3: replace founders. Step 4: repair-dock only changes rule. '+row.get('status','running'),fill='white',font=small)
    im.save(path)

def replay(rows,path):
    data=json.dumps(rows).replace('</','<\\/')
    html='''<!doctype html><meta charset="utf-8"><title>Swarm of Theseus</title>
<style>body{background:#101827;color:#eef4ff;font:18px system-ui;margin:40px auto;max-width:1100px}button,select,input{font:inherit;margin:8px;padding:8px}canvas{width:100%;background:#182335}pre{white-space:pre-wrap}a{color:#70dfba}</style>
<h1>Swarm of Theseus</h1><p>SOC-24 · Recorded exploratory trajectories. Useful task accuracy and arbitrary convention retention are separate.</p>
<select id="world"></select><button id="play">Play / pause</button><input id="step" type="range" min="0" max="5" value="0"><span id="time"></span><canvas id="c" width="1100" height="480"></canvas><pre id="roster"></pre><p>Steps 1–3 replace one founder each. At step 4 the repair-dock mapping changes. Grey means unrecorded; a missing frame is not a zero score. Members and turns are not independent samples.</p>
<script>const rows=DATA;const sel=document.querySelector('#world'),slider=document.querySelector('#step'),ctx=document.querySelector('#c').getContext('2d');
rows.forEach((r,i)=>{let o=document.createElement('option');o.value=i;o.textContent=r.scenario+' / '+r.arm+' / seed '+r.seed;sel.appendChild(o)});
function draw(){let r=rows[+sel.value],t=+slider.value;ctx.clearRect(0,0,1100,480);let metrics=['accuracy','convention','turnover'],colors=['#6fe3be','#f9c66b','#94aafa'];metrics.forEach((m,k)=>{ctx.fillStyle=colors[k];ctx.font='22px system-ui';ctx.fillText(m,25,65+k*140);for(let s=0;s<6;s++){let f=r.history.find(x=>x.step===s),x=270+s*135,y=120+k*140;ctx.globalAlpha=s>t?.25:1;ctx.fillStyle=f?colors[k]:'#68778c';ctx.fillRect(x,y-(f?f[m]*80:4),75,f?f[m]*80:4);ctx.fillText(f?Math.round(f[m]*100)+'%':'?',x,y-88);ctx.fillText(''+s,x,y+26)}});ctx.globalAlpha=1;document.querySelector('#time').textContent='Step '+t;let f=r.history.find(x=>x.step===t);document.querySelector('#roster').textContent=f?JSON.stringify({members:f.members,founders_remaining:f.original_count,rule_changed:f.rule_changed,status:r.status},null,2):'Missing frame; status: '+r.status}
sel.onchange=slider.oninput=draw;let playing=false;document.querySelector('#play').onclick=()=>playing=!playing;setInterval(()=>{if(playing){slider.value=(+slider.value+1)%6;draw()}},1000);draw();</script>'''
    Path(path).write_text(html.replace('DATA',data))
