"""Standalone publication image from frozen summaries; no model execution."""
import json,sys
from PIL import Image,ImageDraw,ImageFont

def draw(summary,path):
    im=Image.new('RGB',(1800,1100),'#101827');d=ImageDraw.Draw(im)
    paths=['/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf']
    def font(n):
        for p in paths:
            try:return ImageFont.truetype(p,n)
            except OSError:pass
        return ImageFont.load_default()
    d.text((65,40),'Swarm of Theseus',font=font(50),fill='white')
    stage=summary.get('stage','exploratory')
    d.text((65,110),f'SOC-24 | {stage} | Post-turnover task performance and convention retention',font=font(26),fill='#c1cce0')
    d.text((65,160),'Green: useful task accuracy       Gold: arbitrary receipt convention       Scale: 0 - 100%',font=font(24),fill='#c1cce0')
    scenarios=list(summary['by_scenario']);arms=[a for a in ['neither','notes','mentor','both','founders','verbatim'] if any(a in x for x in summary['by_scenario'].values())]
    for i,s in enumerate(scenarios):d.text((320+i*480,225),s,font=font(28),fill='white')
    for j,a in enumerate(arms):
        y=290+j*105;d.text((65,y+10),a,font=font(27),fill='white')
        for i,s in enumerate(scenarios):
            x=320+i*480;cell=summary['by_scenario'][s].get(a)
            if not cell:d.text((x,y),'unmeasured',font=font(22),fill='#768197');continue
            for k,(metric,color) in enumerate([('accuracy','#6fe3be'),('convention','#f9c66b')]):
                yy=y+k*34;v=cell[metric];d.rectangle((x,yy,x+300,yy+23),fill='#25334a')
                if v>0:d.rectangle((x,yy,x+300*v,yy+23),fill=color)
                d.text((x+315,yy-4),f'{v*100:.1f}%',font=font(23),fill=color)
    y=970
    if summary.get('primary'):
        p=summary['primary'];text=f"Both minus neither: {p['difference']*100:+.1f} points; exploratory 95% bootstrap interval [{p['ci95'][0]*100:.1f}, {p['ci95'][1]*100:.1f}]"
    else:text='Competence screen only; this is not the inheritance-channel comparison.'
    d.text((65,y),text,font=font(24),fill='white')
    d.text((65,y+45),f"{summary['completed']}/{summary['assigned']} complete; {summary['failed']} failed. Two worlds per scenario; synthetic tasks, one model, seeded procedures.",font=font(23),fill='#c1cce0')
    im.save(path)
if __name__=='__main__':draw(json.load(open(sys.argv[1])),sys.argv[2])
