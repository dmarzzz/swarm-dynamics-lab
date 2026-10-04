"""Render recorded response progression; never calls a model."""
import argparse, collections, json
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

def render(out):
    rows=sorted([json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()],key=lambda r:r['assignment'])
    events=[json.loads(x) for x in (out/'events.jsonl').read_text().splitlines()]
    summary=json.loads((out/'summary.json').read_text())
    try:
        font=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',24)
        small=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',19)
        title=ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial.ttf',36)
    except OSError:font=small=title=ImageFont.load_default()
    selected=[0]+[i+1 for i,e in enumerate(events) if e['kind'] in ('response','terminal')]
    if selected[-1]!=len(events):selected.append(len(events))
    all_selected=len(selected)
    if len(rows)>12:
        selected=sorted({selected[round(i*(len(selected)-1)/47)] for i in range(48)})
    frames=[]
    for n in selected:
        seen=events[:n];by=collections.defaultdict(list)
        for e in seen:by[e['assignment']].append(e)
        img=Image.new('RGB',(1600,1000 if len(rows)>12 else 220+len(rows)*80),'#101a24');d=ImageDraw.Draw(img)
        d.text((35,25),f"Local agents · {summary['stage']} · {summary['model']}",font=title,fill='#f5f8fa')
        d.text((35,82),f"Recorded event {n}/{len(events)} · logical playback · nine identities per team · evaluator-only correctness",font=small,fill='#bfcedb')
        d.text((35,148),'Every response retained in HTML/JSON; GIF samples 48 recorded steps.' if len(rows)>12 else 'Every recorded response/terminal is included.',font=small,fill='#bfcedb')
        d.text((35,118),'Gray: pending    Cyan: responses received    Green: correct    Amber: incorrect    Red: invalid',font=small,fill='#bfcedb')
        groups=sorted({(r['domain'],r['world']) for r in rows})
        arms=sorted({r['arm'] for r in rows})
        if len(rows)>12:
            for j,arm in enumerate(arms):d.text((260+j*260,190),arm.replace('_',' '),font=small,fill='#eef4f9')
            for j,(domain,world) in enumerate(groups):
                d.text((35,245+j*66),domain,font=small,fill='#eef4f9');d.text((35,270+j*66),world,font=small,fill='#bfcedb')
        for j,r in enumerate(rows):
            es=by[r['assignment']];count=sum(e['kind']=='response' for e in es);terminal=any(e['kind']=='terminal' for e in es)
            state='pending';color='#40515f'
            if count:state='in progress';color='#26bcca'
            if terminal:
                state='INVALID' if not r['validity']['ok'] else ('correct' if r['evaluation']['correct'] else 'incorrect')
                color={'INVALID':'#f17073','correct':'#66d4a5','incorrect':'#efbc68'}[state]
            if len(rows)>12:
                x=260+arms.index(r['arm'])*260;y=240+groups.index((r['domain'],r['world']))*66
                d.rounded_rectangle((x,y,x+242,y+56),radius=6,fill='#182735',outline=color,width=2)
                d.text((x+10,y+6),str(count)+'/15 responses',font=small,fill='#bfcedb')
                d.text((x+10,y+30),state,font=small,fill=color)
                continue
            y=178+j*80
            d.text((35,y),f"{r['assignment']+1:02}  {r['domain']} / {r['world']} / {r['arm']}",font=font,fill='#eef4f9')
            d.rectangle((920,y,920+min(count,15)*22,y+25),fill=color)
            d.text((1270,y),f'{count}/15 · {state}',font=small,fill=color)
            if terminal:d.text((35,y+33),'Choice: '+r.get('choice','unavailable; no harmful-choice label inferred'),font=small,fill='#bfcedb')
        frames.append(img)
    frames[-1].save(out/'final.png')
    frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=[400]*(len(frames)-1)+[1800],loop=0,optimize=True)
    assert sum(e['kind']=='terminal' for e in events)==len(rows)
    return {'stage':summary['stage'],'frames':len(frames),'events':len(events),'all_terminals_included':len(selected)==all_selected,'final_contains_all_terminal_states':True,'all_responses_included':len(selected)==all_selected,'sampled_frames':len(selected),'available_response_terminal_frames':all_selected,'final_valid':sum(r['validity']['ok'] for r in rows),'final_correct':sum(r['evaluation']['correct'] for r in rows),'gif_frames':Image.open(out/'replay.gif').n_frames}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();v=render(a.directory);(a.directory/'image-validation.json').write_text(json.dumps(v,indent=2)+'\n');print(json.dumps(v))
