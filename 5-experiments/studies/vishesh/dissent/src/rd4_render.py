"""RD-V4 measured outputs; evaluator truth is labelled, never inferred reasoning."""
import json
from pathlib import Path
from live_render import base,font,FG,MUTED,GREEN,BLUE,RED,GOLD

def render(out):
    out=Path(out);s=json.loads((out/'summary.json').read_text());rows=json.loads((out/'records.json').read_text())
    origin='SOFTWARE FIXTURE' if s.get('software_fixture') else 'Native Jev'
    im,d=base('The Right Dissenter | the right to resume',f"{origin} | {s['stage']} | {s['terminal']}/{s['assigned']} terminal opportunities | finite synthetic tasks")
    if s['stage']=='Q4':
        for i,(domain,v) in enumerate(s['by_scenario'].items()):
            y=260+i*165;d.text((70,y),domain.title(),font=font(36),fill=FG)
            d.rectangle((400,y,1430,y+50),fill='#253642')
            if v['correct']:d.rectangle((400,y,400+1030*v['correct']/6,y+50),fill=GREEN)
            d.text((1490,y),str(v['correct'])+'/6',font=font(36),fill=FG)
        d.text((70,820),f"Uncertainty controls: {s['uncertainty_correct']}/6",font=font(36),fill=FG)
        d.text((70,905),'Qualification: '+('PASS' if s['qualification_passed'] else 'FAIL'),font=font(44),fill=GREEN if s['qualification_passed'] else RED)
    else:
        columns=[(70,'Policy'),(520,'Correct / 96'),(850,'Checks'),(1050,'Resume / 12'),(1370,'Model calls')]
        for x,label in columns:d.text((x,225),label,font=font(28),fill=MUTED)
        for i,(arm,v) in enumerate(s['by_arm'].items()):
            y=305+i*90
            for (x,_),label in zip(columns,[arm,str(v['correct_on_time']),str(v['checks']),str(v['recovery_correct']),str(v['logical_calls'])]):d.text((x,y),label,font=font(31),fill=GREEN if arm=='symmetric-gate' else FG)
        d.text((70,905),'24 fixed roots; 4 epochs; 6 policies. Scripted votes and shared identical model responses.',font=font(25),fill=MUTED)
        d.text((70,970),'A simpler checking rule remains a decisive comparator. Failures stay in every denominator.',font=font(25),fill=MUTED)
    im.save(out/'final_frame.png')
    if s['stage']!='S4':return
    frames=[]
    for domain in ('bridge','build','alarm'):
        for direction in ('recovery','deterioration'):
            candidates=[r for r in rows if r['scenario']==domain and r['condition']=='supported' and r['direction']==direction]
            if not candidates:continue
            cid=candidates[0]['case_id']
            for epoch in range(4):
                im,d=base('The Right Dissenter | measured recovery replay',f'{origin} | {domain} | {direction} | epoch {epoch+1}/4 | supported objection and its repeats')
                for i,arm in enumerate(('original-gate','symmetric-gate','always-check')):
                    x=65+575*i;r=next((r for r in rows if r['case_id']==cid and r['arm']==arm and r['epoch']==epoch),None)
                    d.text((x,245),arm,font=font(31),fill=GREEN if arm=='symmetric-gate' else BLUE)
                    if not r:d.text((x,350),'Missing outcome',font=font(30),fill=RED);continue
                    lines=[('Frozen vote',r['initial']),('Current before',r['actor'].get('current_decision','unknown')),('Final action',r['final']),('Reason',r['reason']),('Check spent',str(r['checks'])),('Closure',r['closure']),('Correct',str(r['correct_completion']))]
                    for j,(label,value) in enumerate(lines):
                        y=325+j*72;d.text((x,y),label,font=font(22),fill=MUTED);d.text((x+210,y),str(value),font=font(24),fill=FG)
                    d.text((x,875),'Evaluator truth: '+r['evaluator']['gold_action'],font=font(24),fill=GOLD)
                d.text((65,980),'Exact repeat and aliases cannot spend another check. Fresh evidence may reopen in either direction.',font=font(25),fill=MUTED)
                frames.append(im)
    if frames:frames[0].save(out/'measured_replay.gif',save_all=True,append_images=frames[1:],duration=1100,loop=1,optimize=False)
