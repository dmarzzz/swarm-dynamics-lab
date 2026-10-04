"""Saved-event PC-V4 view. No model calls and no synthetic movement paths."""
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
COLORS={'LAND':'#67bf97','WATER':'#437dcc','UNKNOWN':'#465365'}

def frame(episodes,seed,policy,guard,slot,fixture=False):
    im=Image.new('RGB',(1600,920),'#101925');d=ImageDraw.Draw(im);font=ImageFont.load_default(size=22);small=ImageFont.load_default(size=17)
    def text(x,y,s,color='white'):d.text((x,y),s,font=font,fill=color)
    text(35,20,'SCRIPTED FIXTURE - NOT MODEL EVIDENCE' if fixture else 'PHANTOM COAST PC-3 | recorded inspection choices')
    text(35,57,f'Root {seed} | {policy} | coverage guard {"on" if guard else "off"} | logical slot {slot}/12')
    def grid(x,y,labels,outline=(),target=None,proposals=()):
        for r in range(6):
            for c in range(6):
                cell=f'{r},{c}';xx=x+c*54;yy=y+r*54
                d.rectangle((xx,yy,xx+50,yy+50),fill=COLORS.get(labels.get(cell),'#465365'),outline='#e7c877' if cell in outline else '#152334',width=3)
                d.text((xx+5,yy+3),cell,font=small,fill='white')
                if cell in proposals:d.ellipse((xx+4,yy+31,xx+14,yy+41),fill='#e0bfff')
                if cell==target:d.rectangle((xx+1,yy+1,xx+49,yy+49),outline='white',width=4)
    for side,report in enumerate(('misleading','benign')):
        e=next(e for e in episodes if (e['seed'],e['policy'],e['guard'],e['report'])==(seed,policy,guard,report));x=35+side*785
        events=e['events'][:slot];last=events[-1] if events else {};observations={v['target']:v['observation']['label'] for v in events if v['target'] is not None};visited=set(observations)
        text(x,105,report.upper());text(x,145,'Evaluator truth');text(x+355,145,'Acquired direct evidence')
        grid(x,180,e['truth'],e['report_cells']);grid(x+355,180,observations,target=last.get('target'),proposals=last.get('proposals',[]))
        text(x,520,f'Spent {len(events)}/12 | unique {len(visited)}/12 | report cells {len(visited&set(e["report_cells"]))}/4')
        text(x,555,f'Target {last.get("target")} | coverage guard {e["guard"]} | repeat {last.get("repeated",False)}')
        text(x,590,'Proposals: '+str(last.get('proposals',[])))
        text(x,625,'Native endpoint: '+('available below as bounds' if slot==12 else 'not yet measured'))
        if slot==12:
            m=e['endpoint']['metrics']['whole'];text(x,660,f'Wrong {m["wrong"]}/36 | unresolved {m["missing"]}/36 | risk {m["lower"]:.3f} - {m["upper"]:.3f}')
            text(x,695,e['status'])
    text(35,770,'Gold outline: reported cells in evaluator view. Purple dot: proposal. White outline: actual target.')
    text(35,810,'Gray: no direct observation. Repeats spend a slot; no travel or continuous motion is implied.')
    text(35,850,'Endpoint maps, actor responses, request hashes and every event are retained in JSON.')
    return im

def render(directory,fixture=False):
    out=Path(directory);episodes=json.loads((out/'episodes.json').read_text());roots=sorted({e['seed'] for e in episodes})
    frames=[];index=[];palette=None
    for seed in roots:
        for policy in ('team','single','uniform'):
            for guard in (False,True):
                for slot in range(13):
                    im=frame(episodes,seed,policy,guard,slot,fixture)
                    small=im.resize((800,460))
                    if palette is None:palette=small.quantize(colors=64)
                    frames.append(small.quantize(palette=palette,dither=Image.Dither.NONE));index.append(dict(seed=seed,policy=policy,guard=guard,slot=slot))
    im.save(out/'final_frame.png');frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=160,loop=0)
    (out/'replay-manifest.json').write_text(json.dumps(dict(fixture=fixture,frames=index),indent=2))
