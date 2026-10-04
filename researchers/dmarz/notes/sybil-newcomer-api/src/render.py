"""Recorded logical history, honest missing model observations, and measured tradeoffs."""
from PIL import Image,ImageDraw,ImageFont
import study,sim
COLORS={'random':'#f4c777','reputation':'#bb9df6','renewal':'#5fd7d0'}
INK='#edf3fb';MUTED='#a7b5c7'
def font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default()
def frame(rows,total,stage,elapsed=0,accounting=None,history=None,round_cursor=8):
    im=Image.new('RGB',(1800,1200),'#111b2a');d=ImageDraw.Draw(im)
    def txt(x,y,s,size=24,color=INK):d.text((x,y),str(s),font=font(size),fill=color)
    good=[r for r in rows if r['status']=='completed'];failed=sum(r['status']=='failed' for r in rows)
    txt(60,30,'Can earned trust survive a coordinated lie?',42)
    txt(60,90,f'{stage} | '+('SCRIPTED' if stage=='S0' else 'HAIKU 4.5')+' | exploratory | simulated identities, API synthesis',25,COLORS['renewal'])
    txt(60,135,f'Completed {len(good)}/{total} | failed {failed} | not started {sum(r["status"]=="not_started" for r in rows)} | elapsed {elapsed:.0f}s')
    if stage=='Q0':
        q=study.qualification(rows)
        for i,c in enumerate(q['cells']):
            y=250+i*200;txt(80,y,f'{c["shape"]}: {c["count"]}/{c["expected"]} clean packets',32)
            txt(80,y+60,f'Fields {c["fact_accuracy"]:.1%} | exact {c["exact_packet_rate"]:.1%} | absent-fact abstention {c["missing_abstention"]:.1%}',28)
    else:
        for i,(arm,color) in enumerate(COLORS.items()):
            x=62+i*390;d.line((x,203,x+40,203),fill=color,width=5);txt(x+52,184,arm+' audits',24,color)
        txt(60,230,'Same resources: 16 controller messages, 4 audits, 12 admitted reports per round',24,MUTED)
        hs=[h for h in (history or []) if h['identities']==16 and h['strategy']=='sleeper' and h['round']<=round_cursor]
        for panel,metric,label in ((0,'attacker_reputation','Coalition reputation (public audit history)'),(1,'newcomer_retention','Rare honest newcomer reports admitted')):
            x=115+panel*855;y=365;w=640;h=245;txt(x-35,y-62,label,25)
            for tick in (0,.5,1):
                yy=y+h*(1-tick);d.line((x,yy,x+w,yy),fill='#334253');txt(x-65,yy-13,f'{tick:.0%}',18,MUTED)
            for t in range(1,9):txt(x+(t-1)*w/7-6,y+h+12,t,19)
            onset=x+3*w/7;d.line((onset,y-8,onset,y+h),fill='#ff899b',width=2);txt(onset-20,y-37,'switch + arrival',18,'#ff899b')
            for arm,color in COLORS.items():
                prev=None
                for t in range(1,round_cursor+1):
                    rr=[z['metrics'][metric] for z in hs if z['arm']==arm and z['round']==t and z['metrics'][metric] is not None]
                    if not rr:prev=None;continue
                    pt=(x+(t-1)*w/7,y+h*(1-sim.mean(rr)))
                    if prev:d.line((*prev,*pt),fill=color,width=4)
                    d.ellipse((pt[0]-5,pt[1]-5,pt[0]+5,pt[1]+5),fill=color);prev=pt
            txt(x,y+h+43,f'Logical round 1–8 | cursor {round_cursor} | 16 identities, sleeper',19,MUTED)
        txt(80,737,'Final-round tradeoff | sleeper | marker label = attacker identities',26)
        x=150;y=814;w=640;h=205
        for tick in (0,.5,1):
            yy=y+h*(1-tick);d.line((x,yy,x+w,yy),fill='#334253');txt(x-67,yy-12,f'{tick:.0%}',17,MUTED)
            xx=x+w*tick;txt(xx-20,y+h+9,f'{tick:.0%}',17,MUTED)
        txt(x-12,y+h+45,'Attacker share of admitted reports →',20,MUTED)
        txt(x-55,y-31,'Specialist accuracy ↑',20,MUTED)
        if round_cursor==8:
            for arm,color in COLORS.items():
                for n in (1,4,16):
                    rr=[r for r in good if r['kind']=='pilot' and r['arm']==arm and r['identities']==n and r['strategy']=='sleeper' and r['round']==8]
                    if rr:
                        px=x+w*sim.mean([r['evaluation']['bad_seat_share'] for r in rr]);py=y+h*(1-sim.mean([r['evaluation']['rare_accuracy'] for r in rr]));d.ellipse((px-7,py-7,px+7,py+7),fill=color);txt(px+10,py-14,n,18,color)
        txt(965,738,'Model measurements | 16 identities, sleeper',26)
        for i,t in enumerate((4,5,8)):
            txt(975,796+i*70,f'Round {t}',24)
            for j,(arm,color) in enumerate(COLORS.items()):
                rr=[r for r in good if r['kind']=='pilot' and r['round']==t and r['arm']==arm and r['identities']==16 and r['strategy']=='sleeper'] if t<=round_cursor else []
                value=f'{sim.mean([r["evaluation"]["rare_accuracy"] for r in rr]):.1%} ({len(rr)})' if rr else 'pending'
                txt(1110+j*200,797+i*70,value,23,color)
        txt(970,1010,'No model calls in other rounds; no inferred model memory.',19,MUTED)
    a=accounting or {};txt(62,1110,f'Stage cost ${sum(r.get("accounting",{}).get("actual_usd",0) for r in rows):.4f} | study ${a.get("actual_usd",0):.4f} | reserved ${a.get("reserved_usd",0):.2f}',23,COLORS['renewal'])
    txt(62,1151,'Lines: recorded simulated histories. Dots/table: completed API snapshots. Missing observations never become zero.',20,MUTED)
    return im

def replay(rows,out,stage,total,initial_accounting=None,history=None):
    last=rows[-1] if rows else {};account=last.get('study_accounting',initial_accounting or {})
    if stage=='Q0':
        counts=[round(len(rows)*i/8) for i in range(9)];images=[frame(rows[:n],total,stage,accounting=account) for n in counts]
    else:images=[frame(rows,total,stage,last.get('elapsed_seconds',0),account,history,t) for t in range(1,9)]
    images[-1].save(out/'final_frame.png');images[0].save(out/'replay_start.png')
    images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=[1000]*(len(images)-1)+[3000],loop=0)
    return len(images)
