"""Reporting-only progress frame; decisions and RNG never depend on rendering."""
from pathlib import Path

def render(rows,total,path):
    from PIL import Image,ImageDraw,ImageFont
    im=Image.new('RGB',(1800,1080),'#101827');d=ImageDraw.Draw(im)
    def font(size):
        for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
            if Path(p).exists():return ImageFont.truetype(p,size)
        return ImageFont.load_default(size=size)
    d.text((70,45),'How to win agents and influence swarms',font=font(44),fill='#edf3fb')
    d.text((70,115),f'{len(rows)} / {total} outcomes recorded — exploratory repair, measured states only',font=font(24),fill='#99afc5')
    for i,r in enumerate(rows[-12:]):
        y=185+i*62;ok=r['validity']['ok'];e=r['evaluation']
        color='#99afc5' if not ok else '#43d9b2' if e['correct'] else '#ff7b79' if e.get('harmful_target') else '#f3c969'
        status='INVALID' if not ok else 'CORRECT' if e['correct'] else 'TARGET' if e.get('harmful_target') else 'OTHER ERROR'
        d.rounded_rectangle((65,y,1735,y+52),radius=9,fill='#192538')
        d.text((85,y+10),f"{r['domain']} / {r['world']} / task {r['task_id']} / {r['arm']}",font=font(20),fill='#edf3fb')
        d.text((1270,y+10),status,font=font(20),fill=color)
        if ok:d.text((1460,y+10),'chair agrees' if not e.get('chair_rule_disagreement') else 'chair overridden',font=font(17),fill='#99afc5')
    d.text((70,1005),'Latest 12 outcomes shown; complete history is retained in events and episodes. Invalid is not a scientific adverse result.',font=font(20),fill='#99afc5')
    im.save(path)
