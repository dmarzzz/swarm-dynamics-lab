"""Public PNG/GIF from recorded events only; no future commitment leaks."""
import collections
import json
from pathlib import Path
from PIL import Image,ImageDraw,ImageFont
from engine import ARMS

BG='#0b1220'; PANEL='#152238'; INK='#edf4ff'; MUTED='#a8bad1'
COLORS={'A':'#68d6f4','B':'#f6bf66','C':'#b49afa','NONE':'#ed93b1','WAIT':'#72849c',None:'#72849c'}


def font(n):
    for path in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf','/System/Library/Fonts/Supplemental/Arial.ttf'):
        if Path(path).exists():return ImageFont.truetype(path,n)
    return ImageFont.load_default(size=n)


def text(d,xy,s,n=22,fill=INK):d.text(xy,str(s),font=font(n),fill=fill)
def panel(d,box):d.rounded_rectangle(box,radius=14,fill=PANEL)


def visible_decisions(record,t):
    return {arm:out for arm,out in record['outcomes'].items() if out['round']<=t}


def frame(record,t):
    im=Image.new('RGB',(1600,1000),BG);d=ImageDraw.Draw(im)
    text(d,(48,28),'ANTSY',44);text(d,(260,46),'When should the swarm commit?',28)
    text(d,(48,96),f"{record['world']} / {record['timing']}  |  task {record['task']}  |  {record['agents']} scouts  |  tick {t}/{record['deadline']}",23,MUTED)
    text(d,(48,145),'EVIDENCE ARRIVAL  /  supplied ancestry, not certified independence',19,MUTED)
    for r in range(4):
        ds=[x for x in record['documents'] if x['root']==f'root-{r}'];arrival=min(x['arrival'] for x in ds)
        x=48+r*385;panel(d,(x,180,x+360,280))
        text(d,(x+18,194),f'Source {r+1}',24)
        text(d,(x+18,233),f'{len(ds)} rows delivered' if arrival<=t else 'Awaiting evidence',20,'#65ddb4' if arrival<=t else MUTED)
    text(d,(48,308),'SCOUT BALLOTS  /  color = current choice; same pinned model, different visible facts',19,MUTED)
    ballots=record['trace'][t-1]['ballots'] if t else [{'choice':'WAIT','roots':[],'error':None} for _ in range(record['agents'])]
    for i,b in enumerate(ballots):
        x=100+i*1400/max(1,len(ballots)-1)
        d.ellipse((x-37,355,x+37,429),fill=COLORS[b['choice']]);text(d,(x-24,373),b['choice'] if b['choice']!='NONE' else 'N',21,BG)
        text(d,(x-34,445),f'Scout {i+1}',16,MUTED);text(d,(x-30,470),f"{len(b['roots'])} roots",16)
        if b['error']:text(d,(x-30,492),'ERROR',15,'#ff7979')
    text(d,(48,525),'POLICY COMMITMENTS  /  frozen once made; future outcomes hidden',19,MUTED)
    visible=visible_decisions(record,t)
    for j,(arm,out) in enumerate((a,record['outcomes'][a]) for a in ARMS):
        y=565+j*47;panel(d,(48,y,1552,y+41));text(d,(66,y+7),arm,20)
        if arm in visible:
            text(d,(375,y+7),out['choice'] or 'ABSTAIN',20,COLORS[out['choice']]);text(d,(565,y+7),f"tick {out['round']}  |  {len(out['roots'])} supporting roots",19)
            result='execution error' if not out['valid'] else 'correct' if out['evaluation']['correct'] else 'violation' if out['evaluation']['constraint_violation'] else 'abstained' if out['evaluation']['abstention'] else 'wrong'
            text(d,(1060,y+7),f'Evaluator: {result}',19,'#65ddb4' if result=='correct' else '#f6bf66')
        else:text(d,(375,y+7),'observing / no decision yet',19,MUTED)
    text(d,(48,920),'Replay of measured events. Logical ticks are evidence releases, not seconds.',20,MUTED)
    text(d,(48,952),'Laya extracts predicates; host code applies eligibility and price rules. Evaluator labels never enter actor input.',18,MUTED)
    return im


def animation(record,destination):
    frames=[frame(record,t) for t in range(record['deadline']+1)]
    frames[-1].save(destination.with_suffix('.png'))
    frames[0].save(destination.with_suffix('.gif'),save_all=True,append_images=frames[1:],duration=[900]*(len(frames)-1)+2400,loop=0,optimize=True)


def diagnostic(results,destination,title):
    groups=collections.defaultdict(list)
    for r in results:groups[r.get('kind','boundary' if isinstance(r.get('task'),str) else 'core')].append(r)
    im=Image.new('RGB',(1600,900),BG);d=ImageDraw.Draw(im)
    text(d,(50,35),'ANTSY / '+title,36);text(d,(50,93),'Every assigned case remains visible; green = correct, amber = wrong, red = execution error.',22,MUTED)
    for j,(kind,rs) in enumerate(groups.items()):
        y=160+j*85;panel(d,(45,y,1555,y+70));text(d,(65,y+20),kind,22)
        for i,r in enumerate(rs):
            x=400+i*55;d.rounded_rectangle((x,y+18,x+40,y+54),radius=5,fill='#ff7979' if r['error'] else '#65ddb4' if r['correct'] else '#f6bf66')
        text(d,(1330,y+20),f"{sum(r['correct'] for r in rs)}/{len(rs)} correct",20)
    text(d,(50,825),'Narrow synthetic competence screen; completion is not proof of scientific validity.',22,MUTED);im.save(destination)


def overview(records,summary,destination):
    im=Image.new('RGB',(1600,1050),BG);d=ImageDraw.Draw(im)
    text(d,(48,28),'ANTSY / robustness atlas',40)
    text(d,(48,87),f"{len(records)} paired blocks / 12 task clusters / descriptive synthetic stress test",23,MUTED)
    arms=ARMS;worlds=['clean','copies','early-wrong','late-wrong']
    text(d,(48,139),'Cells show correct / violation / abstention. Each world pools both deadlines, populations and delivery schedules.',20,MUTED)
    for j,w in enumerate(worlds):text(d,(480+j*265,192),w,23)
    for i,a in enumerate(arms):
        y=245+i*92;text(d,(48,y+20),a,24)
        for j,w in enumerate(worlds):
            rs=[r['outcomes'][a] for r in records if r['world']==w];n=len(rs)
            c=sum(o['evaluation']['correct'] for o in rs);v=sum(o['evaluation']['constraint_violation'] for o in rs);ab=sum(o['evaluation']['abstention'] for o in rs)
            x=470+j*265;panel(d,(x,y,x+240,y+75));text(d,(x+12,y+12),f'{c}/{n} correct',21);text(d,(x+12,y+42),f'{v} violations | {ab} abstain',15,MUTED)
    text(d,(48,925),f"Physical model calls: {summary['physical_calls']}  |  Runtime/schema failures: {summary['invalid_outcomes']}",23)
    text(d,(48,970),'Paired arms reuse one ballot tape. Repeated agents and blocks are not independent samples.',21,MUTED)
    text(d,(48,1005),'Adaptive can help or hurt. A symbolic baseline tests whether learned extraction adds value.',21,MUTED);im.save(destination)
