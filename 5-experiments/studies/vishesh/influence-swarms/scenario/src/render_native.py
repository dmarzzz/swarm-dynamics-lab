"""Measured terminal choices; missing observations remain pending."""
from PIL import Image,ImageDraw,ImageFont

def render(rows,total,path,stage,events):
    im=Image.new('RGB',(1800,1100),'#101c27');d=ImageDraw.Draw(im)
    def font(size):
        for name in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
            try:return ImageFont.truetype(name,size)
            except OSError:pass
        return ImageFont.load_default()
    def t(x,y,s,size=24,color='#dce9ef'):d.text((x,y),s,font=font(size),fill=color)
    t(60,45,'HOW TO WIN AGENTS AND INFLUENCE SWARMS',38)
    t(60,105,f'{stage} | native model evidence | {len(rows)}/{total} terminal decisions | {events} recorded events',24,'#7bdac5')
    valid=[r for r in rows if r['valid']];good=sum(r['evaluation']['acceptable_decision'] for r in valid)
    t(60,160,f'{good} acceptable    {len(valid)-good} valid adverse    {len(rows)-len(valid)} invalid    {total-len(rows)} pending',30)
    t(60,230,'CASE / WORLD',20);t(610,230,'WORKFLOW',20);t(1000,230,'MODEL CHOICE',20);t(1340,230,'ASSESSMENT',20)
    for i,r in enumerate(rows[-15:]):
        y=275+i*43
        choice=r['decision']['choice'] if r['decision'] else 'NO VALID OUTPUT'
        status='INVALID' if not r['valid'] else ('ACCEPTABLE' if r['evaluation']['acceptable_decision'] else 'ADVERSE')
        t(60,y,(r['case_id']+' / '+r['world'])[:42],19);t(610,y,r['arm'],19);t(1000,y,choice,19)
        t(1340,y,status,19,'#7bdac5' if status=='ACCEPTABLE' else '#ffaf98')
    t(60,990,'Team chairs share a prefix. Counts are decisions, not independent cases.',23)
    t(60,1030,'Synthetic procurement records; no real vendor performance or general robustness claim.',21,'#a9bfcb')
    im.save(path)
