"""Retrospective measured report derivative; leaves raw attempt visuals unchanged."""
import json
import sys
import textwrap
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent/'src'))
from live_render import base, font, FG, MUTED, GREEN, BLUE, RED, GOLD
from PIL import Image, ImageDraw


def render(data, output):
    data, output = Path(data), Path(output)
    output.mkdir(parents=True, exist_ok=True)
    rows = json.loads((data/'records.json').read_text())
    im = Image.open(data/'final_frame.png').convert('RGB')
    d = ImageDraw.Draw(im)
    d.rectangle((0,955,1800,1080), fill='#0e171e')
    d.text((70,970),'Sensitivity bounds overlap: gates 87–91; always-check 88–92. No established accuracy winner.',font=font(24),fill=MUTED)
    im.save(output/'results.png')
    frames=[]
    selections=[(domain,direction,'supported',False) for domain in ('bridge','build','alarm') for direction in ('recovery','deterioration')]
    selections += [('alarm',direction,'withdrawn',True) for direction in ('recovery','deterioration')]
    for domain,direction,regime,posthoc in selections:
        for epoch in range(4):
            subtitle=f'{domain} | {direction} | {regime} | epoch {epoch+1}/4'
            im,d=base('The Right Dissenter | measured decision replay',subtitle)
            caption='Retrospective failure illustration' if posthoc else 'Prospectively selected supported-objection illustration'
            d.text((65,175),caption+' | Combined S4; prior failures retained',font=font(23),fill=MUTED)
            for i,arm in enumerate(('original-gate','symmetric-gate','always-check')):
                x=65+575*i
                r=next(r for r in rows if r['scenario']==domain and r['direction']==direction and r['condition']==regime and r['epoch']==epoch and r['arm']==arm)
                d.text((x,245),arm,font=font(30),fill=GREEN if arm=='symmetric-gate' else BLUE)
                lines=[('Frozen vote',r['initial']),('Current before',r['actor']['current_decision']),('Final action',r['final']),('Reason',r['reason']),('Check spent',str(r['checks'])),('Closure',r['closure']),('Status',r['status'])]
                for j,(label,value) in enumerate(lines):
                    y=322+j*68
                    d.text((x,y),label,font=font(22),fill=MUTED)
                    d.text((x+210,y),value,font=font(23),fill=RED if r['status']=='failed' and j in (2,6) else FG)
                d.text((x,822),'Evaluator truth: '+r['evaluator']['gold_action'],font=font(24),fill=GOLD)
                checks=[e for e in r['events'] if e['phase']=='verification' and e.get('record')]
                observation=checks[-1]['record']['text'] if checks else 'No new verifier observation at this epoch.'
                d.text((x,868),'Acquired verification:',font=font(19),fill=MUTED)
                for j,line in enumerate(textwrap.wrap(observation,width=48)[:3]):
                    d.text((x,897+25*j),line,font=font(19),fill=FG)
            d.text((65,1002),'Resolved repeats reuse the decision. Unresolved repeats can spend checks. Fresh evidence may reopen.',font=font(24),fill=MUTED)
            frames.append(im)
    frames[0].save(output/'replay.gif',save_all=True,append_images=frames[1:],duration=1100,loop=1,optimize=False)
    frames[27].save(output/'failure-example.png')
    print(json.dumps({'measured_frames':len(frames),'native_calls':0,'raw_visuals_unchanged':True}))


if __name__=='__main__':
    render(sys.argv[1],sys.argv[2])
