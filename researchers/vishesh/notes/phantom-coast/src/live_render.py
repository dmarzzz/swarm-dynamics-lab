"""PNG/GIF from saved native outcomes; never invent missing responses."""
from PIL import Image,ImageDraw
from instrument import CELLS,world,bounds
COLORS={'LAND':'#a57935','WATER':'#285775','UNKNOWN':'#56616a'}
def frame(row,stage,total,fixture=False):
    w=world(row['seed'],stage=stage);m=row.get('checked',{}).get('response',{}).get('map',{}) if row['status']=='valid' else {}
    im=Image.new('RGB',(1600,1000),'#101b24');d=ImageDraw.Draw(im)
    d.text((45,30),'PHANTOM COAST / PC-1L / '+('SOFTWARE FIXTURE ' if fixture else 'NATIVE ')+stage,fill='#e9eff1',font_size=30)
    d.text((45,82),row['id']+' / '+row['status'],fill='#e9eff1',font_size=22)
    for x0,label,mp in ((50,'Evaluator truth',w['truth']),(830,'Observed map',m)):
        d.text((x0,150),label,fill='#e9eff1',font_size=26)
        for c in CELLS:
            r,col=map(int,c.split(','));v=mp.get(c,'UNKNOWN');x=x0+col*112;y=200+r*112
            d.rectangle((x,y,x+106,y+106),fill=COLORS[v]);d.text((x+40,y+35),'?' if v=='UNKNOWN' else v[0],fill='white',font_size=25)
    b=bounds(m,w['truth']);d.text((45,905),f"Whole-map error bounds {b['lower']:.1%} to {b['upper']:.1%}; unresolved {b['missing']}/36. Assigned maps: {total}.",fill='#e9eff1',font_size=24)
    d.text((45,949),'Fixed observations; no adaptive scouting claim. Truth never enters the actor packet.',fill='#afbdc5',font_size=22)
    return im

def render(records,out,stage,animate=True,fixture=False):
    visible=[r for r in records if r['status']!='not-started']
    if not visible:return
    final=frame(visible[-1],stage,len(records),fixture);final.save(out/'final_frame.png')
    if animate:
        stride=max(1,(len(visible)+58)//59);sample=visible[::stride]
        if sample[-1]['id']!=visible[-1]['id']:sample.append(visible[-1])
        frames=[frame(r,stage,len(records),fixture).resize((800,500)) for r in sample]
        frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=900,loop=0)
        from live_worker import save
        save(out/'replay-manifest.json',{'mode':'software fixture' if fixture else 'native saved outcomes','sampled':stride>1,'stride':stride,'frame_ids':[r['id'] for r in sample],'all_assignments_retained_in':'records.json'})
