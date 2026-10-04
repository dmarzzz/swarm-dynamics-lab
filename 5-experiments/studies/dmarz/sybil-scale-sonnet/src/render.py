"""Measured scaling curves and bounded completion-prefix replay."""
from PIL import Image,ImageDraw,ImageFont
import math
import study
COLORS={'coverage':'#5fd7d0','random':'#f4c777','degree':'#bb9df6','no_verification':'#8796aa'}
INK='#edf3fb';MUTED='#a7b5c7'
def font(size):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:return ImageFont.truetype(path,size)
        except OSError:pass
    return ImageFont.load_default()
def series(rows,rate,arm,mode,visibility,metric,reference=False):
    values=[]
    for n in study.design()['sizes']:
        checks=0 if arm=='no_verification' else 4 if mode=='fixed' else n//9
        rr=[r for r in rows if r['status']=='completed' and r['kind']=='pilot' and r['n']==n and r['arm']==arm and r['checks']==checks and r['attacker_pass']==rate and r['visibility']==visibility]
        field='scripted_evaluation' if reference else 'evaluation'
        values.append((n,sum(r[field][metric] for r in rr)/len(rr) if rr else None,len(rr)))
    return values

def frame(rows,total,stage,elapsed=0,accounting=None,visibility='visible'):
    im=Image.new('RGB',(1800,1200),'#111b2a');d=ImageDraw.Draw(im)
    def text(x,y,t,size=23,fill=INK):d.text((x,y),str(t),font=font(size),fill=fill)
    good=[r for r in rows if r['status']=='completed'];failed=sum(r['status']=='failed' for r in rows)
    text(62,30,'Can Sybil defenses scale with the swarm?',42)
    text(62,92,f'{stage} | '+('SCRIPTED' if stage=='S0' else 'SONNET 4.6')+f' | badges {visibility} | exploratory',25,COLORS['coverage'])
    text(62,137,f'Completed {len(good)}/{total} | failed {failed} | not started {sum(r["status"]=="not_started" for r in rows)} | elapsed {elapsed:.0f}s',24)
    if stage=='Q0':
        q=study.qualification(rows)
        for i,c in enumerate(q['cells']):
            y=240+i*150;text(95,y,f'{c["n"]} identities: {c["count"]}/{c["expected"]} clean packets',29)
            text(95,y+48,f'Fields {c["fact_accuracy"]:.1%} | exact packets {c["exact_packet_rate"]:.1%} | missing-fact abstention {c["missing_abstention"]:.1%}',26)
    else:
        for i,(arm,color) in enumerate(COLORS.items()):
            x=62+i*310;d.line((x,203,x+36,203),fill=color,width=4);text(x+45,185,arm.replace('_',' '),22,color)
        text(62,227,'Solid: 4 checks   Dashed: N/9 checks   White squares: coverage proportional, simple voting',22,MUTED)
        for col,rate in enumerate((.1,.9)):
            for row,metric in enumerate(('rare_accuracy','bad_seat_share')):
                x=120+col*860;y=342+row*365;w=650;h=220
                text(x-40,y-53,('Specialist accuracy' if row==0 else 'Attacker share of admitted seats')+f' | pass {rate:.0%}',24)
                for tick in (0,.25,.5,.75,1):
                    yy=y+h*(1-tick);d.line((x,yy,x+w,yy),fill='#324153',width=1);text(x-63,yy-12,f'{tick:.0%}',18,MUTED)
                for j,n in enumerate(study.design()['sizes']):text(x+j*w/3-16,y+h+12,n,20)
                for arm,color in COLORS.items():
                    for mode in ('fixed','proportional') if arm!='no_verification' else ('fixed',):
                        points=series(rows,rate,arm,mode,visibility,metric)
                        coords=[(x+j*w/3,y+h*(1-v)) if v is not None else None for j,(_,v,_) in enumerate(points)]
                        for a,b in zip(coords,coords[1:]):
                            if a and b:
                                if mode=='fixed':d.line((*a,*b),fill=color,width=4)
                                else:
                                    for t in range(0,20,2):
                                        aa=tuple(a[k]+(b[k]-a[k])*t/20 for k in (0,1));bb=tuple(a[k]+(b[k]-a[k])*(t+1)/20 for k in (0,1));d.line((*aa,*bb),fill=color,width=4)
                        for pt in coords:
                            if pt:d.ellipse((pt[0]-5,pt[1]-5,pt[0]+5,pt[1]+5),fill=color)
                if row==0:
                    points=series(rows,rate,'coverage','proportional',visibility,metric,True)
                    for j,(_,v,_) in enumerate(points):
                        if v is not None:d.rectangle((x+j*w/3-4,y+h*(1-v)-4,x+j*w/3+4,y+h*(1-v)+4),outline='white',width=2)
                counts=[p[2] for arm in COLORS for mode in ('fixed','proportional') for p in series(rows,rate,arm,mode,visibility,metric)]
                text(x,y+h+44,f'Identities (log scale) | observed cell counts {min(counts)}–{max(counts)}',18,MUTED)
    a=accounting or {};stagecost=sum(r.get('accounting',{}).get('actual_usd',0) for r in rows)
    text(62,1060,f'Stage cost ${stagecost:.4f} | study cost ${a.get("actual_usd",0):.4f} | reserved ${a.get("reserved_usd",0):.2f}',23,COLORS['coverage'])
    text(62,1103,'N=36 budgets and no-check points are shared observations. Missing cells are pending, never zero.',22,MUTED)
    text(62,1145,'Simulated reporters and verification; model synthesis only. Replay tracks completed calls, not agent conversations.',21,MUTED)
    return im

def replay(rows,out,stage,total,initial_accounting=None):
    terminal=[r for r in rows if r['status']!='not_started'];count=len(terminal)
    counts=sorted(set([0,count,*[round(count*i/32) for i in range(1,32)]]))
    images=[]
    for n in counts:
        prefix=terminal[:n];last=prefix[-1] if prefix else {}
        images.append(frame(rows if n==count else prefix,total,stage,last.get('elapsed_seconds',0),last.get('study_accounting',initial_accounting)))
    images[0].save(out/'initial_frame.png');images[-1].save(out/'final_frame.png')
    images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=[550]*(len(images)-1)+[2500],loop=0)
    frame(rows,total,stage,rows[-1].get('elapsed_seconds',0) if rows else 0,rows[-1].get('study_accounting',{}) if rows else {},'masked').save(out/'badges_hidden.png')
    return len(images)
