"""Saved-evidence visualization. Scripted inspections are labeled; no fresh inference."""
import json
from pathlib import Path
from PIL import Image,ImageDraw
COLORS={'LAND':'#66b9a0','WATER':'#82b3d6','UNKNOWN':'#c6ccd5'}
def render(out):
    out=Path(out);es=json.loads((out/'episodes.json').read_text());root=min(e['seed'] for e in es)
    chosen=[next(e for e in es if e['seed']==root and e['false_count']==4 and e['policy']==p) for p in ('q4','uniform')]
    frames=[]
    for slot in range(13):
        im=Image.new('RGB',(900,420),'#f5f7fa');d=ImageDraw.Draw(im)
        d.text((22,15),f'PC-4 | saved root {root} | four false reports | scripted inspection {slot}/12',fill='#102030')
        for j,e in enumerate(chosen):
            x=22+j*445;d.text((x,48),e['policy']+' - native consensus only at slot 12',fill='#102030')
            labels={r['cell']:r['label'] for r in e['packet']['evidence']['observations'] if r['source']=='report' or int(r['id'][1:])<=slot}
            if slot==12:labels=e['endpoint']['map']
            for i,c in enumerate(e['truth']):
                rr,cc=map(int,c.split(','));xx=x+cc*52;yy=82+rr*46
                d.rectangle((xx,yy,xx+47,yy+41),fill=COLORS[labels.get(c,'UNKNOWN')],outline='#a32966' if c in e['report_cells'] else '#697384',width=3 if c in e['report_cells'] else 1)
                d.text((xx+5,yy+12),labels.get(c,'UNKNOWN')[0],fill='#102030')
            m=e['endpoint']['whole'];d.text((x,373),f"Wrong {m['wrong']}/36; unknown {m['missing']}/36" if slot==12 else 'Evidence view; endpoint not yet revealed',fill='#102030')
        d.text((22,401),'L=LAND | W=WATER | U=UNKNOWN | pink border=reported cell | representative root only',fill='#102030')
        frames.append(im)
    frames[-1].save(out/'final_frame.png');frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=450,loop=0)
    template=(Path(__file__).parent/'replay-template.html').read_text();(out/'measured-replay.html').write_text(template.replace('__DATA__',json.dumps(es).replace('</',r'<\/')))
