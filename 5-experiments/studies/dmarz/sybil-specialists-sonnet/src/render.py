"""Measured-prefix replay; no invented intermediate model decisions."""
from PIL import Image, ImageDraw, ImageFont
import study

INK='#eaf0f8'; MUTED='#a5b4c7'; BLUE='#5fd7d0'; GRAY='#71839a'; RED='#ff9b8e'


def font(size):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try: return ImageFont.truetype(path,size)
        except OSError: pass
    return ImageFont.load_default()


def frame(rows, total, stage, elapsed=0, accounting=None):
    im=Image.new('RGB',(1800,1180),'#101a29'); d=ImageDraw.Draw(im)
    def text(x,y,t,size=24,fill=INK): d.text((x,y),str(t),font=font(size),fill=fill)
    text(64,40,'Sybil resistance / useful specialist answers',42)
    text(64,102,('SCRIPTED REHEARSAL' if stage=='S0' else 'SONNET 4.6')+'  |  '+stage+'  |  exploratory synthetic worlds',24,BLUE)
    good=[r for r in rows if r['status']=='completed']
    failed=sum(r['status']=='failed' for r in rows)
    text(64,148,f'Completion cursor: {len(good)+failed}/{total} calls or scripted cases  |  elapsed {elapsed:.1f}s',24)
    text(64,190,'Blue: measured answer accuracy     Gray: scripted plurality on the same reports',23,MUTED)
    clean=stage=='Q0'
    keys=[(a,v) for a in (('full','common_only') if clean else (.1,.9)) for v in ('masked','visible')]
    for index,(condition,visibility) in enumerate(keys):
        x=64+(index%2)*850; y=252+(index//2)*370
        d.rounded_rectangle((x,y,x+818,y+344),radius=14,fill='#1c2a3d')
        title=(('All facts available' if condition=='full' else 'Rare facts missing') if clean else f'Attacker check pass: {condition:.0%}')
        text(x+24,y+18,title+' / badges '+visibility,25)
        arms=[condition] if clean else list(study.sim.ARMS)
        for j,arm in enumerate(arms):
            yy=y+75+j*61
            subset=[r for r in good if r['visibility']==visibility and r['arm']==arm and
                    (r['kind']=='qualification' if clean else r['kind']=='pilot' and r['attacker_pass']==condition)]
            metric='qualification_accuracy' if clean else 'rare_accuracy'
            text(x+24,yy,arm.replace('_',' '),21)
            bx=x+220; by=yy+4; width=305
            d.rectangle((bx,by,bx+width,by+17),fill='#101a29')
            if subset:
                mean=sum(r['evaluation'][metric] for r in subset)/len(subset)
                ref=sum(r['scripted_evaluation'][metric] for r in subset)/len(subset)
                if mean: d.rectangle((bx,by,bx+width*mean,by+17),fill=BLUE)
                if ref: d.rectangle((bx,by+23,bx+width*ref,by+28),fill=GRAY)
                text(x+542,yy,f'{mean:.1%}  n={len(subset)}',20)
                if not clean:
                    bad=sum(r['evaluation']['malicious_admission'] for r in subset)/len(subset)
                    text(x+542,yy+24,f'bad admitted {bad:.1%}',16,RED)
            else: text(x+542,yy,'pending',20,MUTED)
        if clean:
            text(x+24,y+172,'Score includes required nulls for missing facts.',22,MUTED)
        text(x+220,y+311,'0%                      accuracy                       100%',16,MUTED)
    not_started=sum(r['status']=='not_started' for r in rows)
    text(64,1013,f'Completed {len(good)}  |  Failed {failed}  |  Not started {not_started}  |  Planned {total}',24)
    a=accounting or {}
    text(64,1055,f"Study cost reported ${a.get('actual_usd',0):.4f}  |  reserved ${a.get('reserved_usd',0):.4f} / $5 cap",23,BLUE)
    text(64,1103,'Model synthesis only. Graph admission and verification are simulated. Missing cells are not zero scores.',21,MUTED)
    return im


def replay(rows, out, stage, total, initial_accounting=None):
    terminal=[r for r in rows if r['status']!='not_started']
    counts=sorted(set([0,len(terminal),*range(8,len(terminal),8)]))
    images=[]
    for n in counts:
        prefix=terminal[:n]
        shown=rows if n==len(terminal) else prefix
        last=prefix[-1] if prefix else {}
        images.append(frame(shown,total,stage,last.get('elapsed_seconds',0),last.get('study_accounting',initial_accounting)))
    images[0].save(out/'initial_frame.png')
    images[-1].save(out/'final_frame.png')
    images[0].save(out/'replay.gif',save_all=True,append_images=images[1:],duration=[500]*(len(images)-1)+[2200],loop=0)
    return len(images)
