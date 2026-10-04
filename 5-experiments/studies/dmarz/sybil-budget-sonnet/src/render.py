"""Heatmaps and measured completion-prefix replay, independent of decision RNG."""
from PIL import Image,ImageDraw,ImageFont
import study
INK='#ecf3f9';MUTED='#a8b8ca';BG='#111b2a'

def font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        try:return ImageFont.truetype(p,size)
        except OSError:pass
    return ImageFont.load_default()

def color(value,metric):
    quality=1-value if metric=='bad_seat_share' else value
    low=(152,63,82);high=(49,173,158)
    return tuple(round(a+(b-a)*quality) for a,b in zip(low,high))

def cell_values(rows,n,arm,checks,rate,metric):
    rr=[r for r in rows if r['status']=='completed' and r['kind']=='pilot' and r['n']==n and r['arm']==arm and r['checks']==checks and r['attacker_pass']==rate]
    return (sum(r['evaluation'][metric] for r in rr)/len(rr),len(rr)) if rr else (None,0)

def frame(rows,total,stage,elapsed=0,accounting=None,view='main'):
    im=Image.new('RGB',(1920,1440),BG);draw=ImageDraw.Draw(im)
    def text(x,y,t,size=23,fill=INK):draw.text((x,y),str(t),font=font(size),fill=fill)
    good=[r for r in rows if r['status']=='completed'];failed=sum(r['status']=='failed' for r in rows)
    text(60,25,'How much verification does Sybil resistance need?',40)
    text(60,83,f'{stage} | '+('SCRIPTED' if stage=='S0' else 'SONNET 4.6')+' | visible verification badges | exploratory',24,'#66d6c5')
    text(60,125,f'Completed {len(good)}/{total} | failed {failed} | not started {sum(r["status"]=="not_started" for r in rows)} | elapsed {elapsed:.0f}s',23)
    if stage=='Q0':
        for i,c in enumerate(study.qualification(rows)['cells']):
            y=280+i*220;text(90,y,f'N={c["n"]}: {c["count"]}/{c["expected"]} clean packets',34)
            text(90,y+62,f'Fields {c["fact_accuracy"]:.1%} | exact packets {c["exact_packet_rate"]:.1%} | missing-fact abstention {c["missing_abstention"]:.1%}',28)
    else:
        metrics=('rare_accuracy','bad_seat_share') if view=='main' else ('specialist_retention','rare_accuracy')
        text(60,163,'Columns: number of checks     Rows: attacker check-pass probability',18,MUTED)
        labels={'rare_accuracy':'Specialist accuracy','bad_seat_share':'Attacker share of admitted seats','specialist_retention':'Honest specialist retention'}
        budgets=study.design()['checks'];rates=study.design()['pilot']['attacker_pass']
        for row,(n,metric) in enumerate((n,m) for n in study.design()['sizes'] for m in metrics):
            for col,arm in enumerate(study.design()['arms']):
                x=130+col*935;y=232+row*260;cw=110;ch=34
                text(x-65,y-44,f'N={n} | {arm} | {labels[metric]}',23)
                for j,b in enumerate(budgets):text(x+j*cw+30,y-4,b,19)
                for i,rate in enumerate(rates):
                    text(x-64,y+34+i*ch,f'{rate:.0%}',19,MUTED)
                    for j,b in enumerate(budgets):
                        value,count=cell_values(rows,n,arm,b,rate,metric);xx=x+j*cw;yy=y+28+i*ch
                        draw.rectangle((xx,yy,xx+cw-5,yy+ch-3),fill=color(value,metric) if value is not None else '#293b50')
                        text(xx+12,yy+4,f'{value:.1%}' if value is not None else 'pending',18)
                        if count:
                            acc,_=cell_values(rows,n,arm,b,rate,'rare_accuracy');bad,_=cell_values(rows,n,arm,b,rate,'bad_seat_share')
                            if count==len(study.design()['worlds']) and acc>=.9 and bad<=.05:
                                draw.rectangle((xx,yy,xx+cw-5,yy+ch-3),outline='#fff2a8',width=3)
        counts=[cell_values(rows,n,arm,b,rate,'rare_accuracy')[1] for n in study.design()['sizes'] for arm in study.design()['arms'] for b in budgets for rate in rates]
        text(60,1267,f'Cells: means; observed counts {min(counts)}–{max(counts)} paired worlds. Yellow outline: accuracy ≥90% AND attacker seats ≤5%.',21)
        text(60,1300,'Engineering target, not a guarantee. Uncertainty in analysis tables. Missing cells are pending, never zero.',21,MUTED)
    a=accounting or {};stagecost=sum(r.get('accounting',{}).get('actual_usd',0) for r in rows)
    text(60,1350,f'Stage cost ${stagecost:.4f} | study cost ${a.get("actual_usd",0):.4f} | reserved ${a.get("reserved_usd",0):.2f}',23,'#66d6c5')
    text(60,1395,'Simulated identities and checks; model synthesis only. Replay shows recorded call completions, not agent interactions.',20,MUTED)
    return im

def replay(rows,out,stage,total,initial_accounting=None):
    terminal=[r for r in rows if r['status']!='not_started'];count=len(terminal)
    counts=sorted(set([0,count,*[round(count*i/24) for i in range(1,24)]]));images=[]
    for n in counts:
        prefix=terminal[:n];last=prefix[-1] if prefix else {}
        images.append(frame(rows if n==count else prefix,total,stage,last.get('elapsed_seconds',0),last.get('study_accounting',initial_accounting)))
    images[0].save(out/'initial_frame.png');images[-1].save(out/'final_frame.png')
    images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=[600]*(len(images)-1)+[2500],loop=0)
    frame(rows,total,stage,rows[-1].get('elapsed_seconds',0) if rows else 0,rows[-1].get('study_accounting',{}) if rows else {},'retention').save(out/'retention.png')
    return len(images)
