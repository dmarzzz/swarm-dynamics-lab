"""Measured PNG/GIF outputs. Standard Pillow renderer; no invented observations."""
import json,textwrap
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont

W,H=1800,1080
BG='#101820';FG='#eef4f6';MUTED='#b6c6cf';GREEN='#50d8a2';RED='#ff958f';BLUE='#75baff';GOLD='#f2c772'
def font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        if Path(p).exists():return ImageFont.truetype(p,size)
    return ImageFont.load_default(size=size)
def base(title,subtitle):
    im=Image.new('RGB',(W,H),BG);d=ImageDraw.Draw(im)
    d.text((70,50),title,font=font(48),fill=FG)
    d.text((70,120),subtitle,font=font(25),fill=MUTED)
    return im,d
def render(out):
    out=Path(out);s=json.loads((out/'summary.json').read_text());rows=json.loads((out/'records.json').read_text())
    origin='SOFTWARE FIXTURE - no model observations' if s.get('software_fixture') else 'Native Jev'
    im,d=base('The Right Dissenter',f"{origin} | {s['stage']} | {s['terminal']}/{s['assigned']} terminal opportunities | synthetic tasks")
    if s['stage']=='Q0':
        for i,(scenario,v) in enumerate(s['by_scenario'].items()):
            y=250+i*180;d.text((70,y),scenario.title(),font=font(34),fill=FG)
            d.rectangle((380,y,1500,y+55),fill='#253642');d.rectangle((380,y,380+1120*v['correct']/v['assigned'],y+55),fill=GREEN)
            d.text((1530,y),f"{v['correct']}/6",font=font(34),fill=FG)
            d.text((380,y+70),f"{v['valid']}/6 valid responses",font=font(25),fill=MUTED)
        d.text((70,850),'Qualification: '+('PASS' if s['qualification_passed'] else 'FAIL'),font=font(44),fill=GREEN if s['qualification_passed'] else RED)
        d.text((70,920),'Thresholds: 17/18 valid, 16/18 correct, at least 5/6 correct in every scenario.',font=font(25),fill=MUTED)
    else:
        d.text((70,205),'Policy',font=font(26),fill=MUTED);d.text((420,205),'Correct on time / 60 assigned',font=font(26),fill=MUTED)
        d.text((1310,205),'Harmful flips',font=font(25),fill=MUTED);d.text((1550,205),'Checks',font=font(25),fill=MUTED)
        for i,(arm,v) in enumerate(s['by_arm'].items()):
            y=270+i*86;d.text((70,y),arm,font=font(28),fill=FG)
            d.rectangle((420,y,1110,y+35),fill='#253642')
            if v['correct_on_time']:d.rectangle((420,y,420+690*v['correct_on_time']/60,y+35),fill=GREEN if arm=='evidence-gate' else BLUE)
            d.text((1140,y),f"{v['correct_on_time']}/60",font=font(28),fill=FG)
            d.text((1330,y),str(v['harmful_reversals']),font=font(28),fill=RED if v['harmful_reversals'] else FG)
            d.text((1570,y),str(v['checks']),font=font(28),fill=FG)
        d.text((70,930),'Scripted initial votes. Exact-reference is deterministic. Random arm has a fixed 50% allocation.',font=font(25),fill=MUTED)
        d.text((70,976),'Shared identical Jev responses across policies; descriptive paired comparison, not independent samples.',font=font(24),fill=MUTED)
    im.save(out/'final_frame.png')
    if s['stage']!='S1':return
    selected=[]
    for scenario,condition in (('bridge','standard'),('build','content_agrees'),('alarm','standard')):
        candidates=[r for r in rows if r['scenario']==scenario and r['condition']==condition and r['arm']=='evidence-gate' and (scenario!='bridge' or not r['initial_correct'])]
        if candidates:selected.append((scenario,candidates[0]['case_id']))
    frames=[]
    for scenario,cid in selected:
        arm_rows={a:[r for r in rows if r['case_id']==cid and r['arm']==a] for a in ('evidence-gate','always-check')}
        for epoch in range(max(len(v) for v in arm_rows.values())):
            pairs={a:v[epoch] if epoch<len(v) else None for a,v in arm_rows.items()}
            for idx in range(max(len(r['events']) if r else 1 for r in pairs.values())):
                title='The Right Dissenter | software fixture' if s.get('software_fixture') else 'The Right Dissenter | measured replay'
                provenance='no model observations' if s.get('software_fixture') else 'scripted initial votes; real Jev decisions'
                im,d=base(title,f'{scenario.title()} | decision epoch {epoch+1} | event {idx+1} | {provenance}')
                for ai,(arm,row) in enumerate(pairs.items()):
                    x=70+ai*860;d.text((x,210),arm,font=font(38),fill=GREEN if ai==0 else BLUE)
                    if row is None:d.text((x,290),'Missing observation',font=font(30),fill=RED);continue
                    events=row['events'];event=events[min(idx,len(events)-1)]
                    details=[f"Phase: {event['phase']} | logical tick {event['tick']}",f"Action: {event.get('action','pending')}",f"Status: {event.get('status',event.get('reason','observing'))}"]
                    if event.get('record'):details.extend(textwrap.wrap(event['record']['text'],48))
                    if event.get('closure'):details.append('Closure: '+event['closure'])
                    for li,line in enumerate(details):d.text((x,300+li*57),line,font=font(28),fill=FG)
                    # The flow is driven by saved phases, not inferred model reasoning.
                    visible=events[:min(idx+1,len(events))]
                    phases={e['phase'] for e in visible}
                    steps=[('initial','Votes'),('challenge','Objection'),('verification','Check'),('resolution','Decision')]
                    d.line((x+35,700,x+695,700),fill=MUTED,width=3)
                    for ni,(phase,label) in enumerate(steps):
                        nx=x+35+220*ni;active=phase in phases
                        color=(GREEN if ai==0 else BLUE) if active else '#253642'
                        d.ellipse((nx-14,686,nx+14,714),fill=color,outline=MUTED,width=2)
                        d.text((nx-30,734),label,font=font(23),fill=FG if active else MUTED)
                    initial=events[0]
                    d.text((x,627),f"{len(initial.get('votes',[]))} votes / {initial.get('unique_sources','?')} original sources",font=font(24),fill=MUTED)
                    d.text((x,800),'Evaluator-only truth: '+row['evaluator']['gold_action'],font=font(28),fill=GOLD)
                    if idx>=len(events)-1:d.text((x,857),'Correct on time: '+str(row['correct_completion']),font=font(28),fill=GREEN if row['correct_completion'] else RED)
                d.text((70,990),'Fixed trace selection; no replacement of failed or adverse cases. Gold is never sent to the actor.',font=font(24),fill=MUTED)
                frames.append(im)
    if frames:frames[0].save(out/'measured_replay.gif',save_all=True,append_images=frames[1:],duration=1000,loop=1,optimize=False)
