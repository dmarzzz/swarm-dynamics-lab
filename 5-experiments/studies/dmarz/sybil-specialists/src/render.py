"""Measured PNG/GIF views; never called by policies or the simulator RNG."""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

W,H=1800,1180
BG='#0c1220'; PANEL='#121d2e'; TEXT='#edf2f7'; MUTED='#9cacbe'; EDGE='#34465d'
GOOD='#51d7ad'; BAD='#ff8678'; CHECK='#f6cf73'; OFF='#5f7189'
NAMES={'no_verification':'Graph only / no checks','degree':'Verify highest degree','random':'Verify at random','coverage':'Verify uncovered neighborhoods'}


def font(size):
    for path in ['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']:
        if Path(path).exists(): return ImageFont.truetype(path,size)
    return ImageFont.load_default(size=size)


def frame(world,records,step,stage='S0'):
    im=Image.new('RGB',(W,H),BG); d=ImageDraw.Draw(im)
    d.text((36,24),'Sybil defense and useful specialist teams',font=font(38),fill=TEXT)
    budget=records[0]['cell']['verification_budget']; cell=world['cell']
    d.text((36,79),f'SCRIPTED REHEARSAL | {stage} | world {world["task"]} | check step {step}/{budget}',font=font(23),fill=CHECK)
    d.text((36,116),f'Bridge swaps {cell["bridges"]}   |   attacker check-pass probability {cell["attacker_pass"]:.0%}   |   clean world: {cell["clean"]}',font=font(21),fill=MUTED)
    for idx,rec in enumerate(records):
        ox=30+(idx%2)*890; oy=166+(idx//2)*447
        d.rounded_rectangle((ox,oy,ox+865,oy+427),radius=10,fill=PANEL)
        snap=rec['trace'][min(step,len(rec['trace'])-1)]
        d.text((ox+20,oy+14),NAMES[rec['arm']],font=font(25),fill=TEXT)
        points={k:(ox+55+x*480,oy+55+y*330) for k,(x,y) in world['positions'].items()}
        for a,neighbors in world['public']['adj'].items():
            for b in neighbors:
                if a<b: d.line([points[a],points[b]],fill=EDGE,width=2)
        admitted=set(snap['admitted'])
        for ident,(x,y) in points.items():
            honest=world['truth'][ident]['honest']; color=GOOD if honest else BAD
            fill=color if ident in admitted else PANEL
            outline=color if ident in admitted else OFF
            r=10
            if honest: d.ellipse((x-r,y-r,x+r,y+r),fill=fill,outline=outline,width=2)
            else: d.polygon([(x,y-r-2),(x+r,y+r),(x-r,y+r)],fill=fill,outline=outline,width=2)
            if ident in world['public']['trusted']: d.rectangle((x-14,y-14,x+14,y+14),outline=TEXT,width=2)
            if ident in snap['passed']: d.ellipse((x-15,y-15,x+15,y+15),outline=CHECK,width=3)
            if ident in snap['failed']:
                d.line((x-12,y-12,x+12,y+12),fill=BAD,width=3); d.line((x-12,y+12,x+12,y-12),fill=BAD,width=3)
            if snap['event'] and ident==snap['event']['node']: d.ellipse((x-20,y-20,x+20,y+20),outline=TEXT,width=2)
        m=snap['metrics']; tx=ox+584
        for row,(label,key,color) in enumerate([('Rare-task accuracy','rare_accuracy',GOOD),('Honest excluded','honest_rejection',MUTED),('Malicious admitted','malicious_admission',BAD)]):
            yy=oy+78+row*82; v=m[key]
            d.text((tx,yy),label,font=font(20),fill=MUTED)
            d.text((tx,yy+27),'N/A (no attackers)' if v is None else f'{v:.0%}',font=font(26),fill=color)
        ev=snap['event']; status='No verification' if not ev else f'{ev["node"]}: check '+('passed' if ev['pass'] else 'failed')
        d.text((ox+20,oy+385),f'{status}   |   {m["verification_calls"]} checks   |   {m["correct_skills"]}/6 tasks correct',font=font(20),fill=TEXT)
    d.text((36,1081),'Evaluator overlay: circles = honest; triangles = controlled identities; filled = admitted; hollow = excluded.',font=font(21),fill=TEXT)
    d.text((36,1114),'Gold ring = passed check; cross = failed check; square = initial trusted seed. Policies never receive truth labels.',font=font(20),fill=MUTED)
    d.text((36,1145),'Fixed layout across policies. Logical verification steps, not wall time. No model calls and no scientific LLM finding.',font=font(19),fill=MUTED)
    return im


def replay(world,records,out,stage):
    out=Path(out); out.mkdir(parents=True,exist_ok=True)
    frames=[frame(world,records,s,stage) for s in range(len(records[0]['trace']))]
    frames[0].save(out/'initial_frame.png'); frames[-1].save(out/'final_frame.png')
    if len(frames)>1:
        frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=[1100]*(len(frames)-1)+[2400],loop=0,optimize=False)
    return len(frames)
