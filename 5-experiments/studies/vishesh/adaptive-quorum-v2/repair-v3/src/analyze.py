"""Reconcile durable outcomes and export conditional, task-paired evidence."""
import argparse,csv,json,collections,hashlib
from pathlib import Path
from PIL import Image,ImageDraw
from render import BG,INK,MUTED,text,panel
from engine import ARMS


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--run',type=Path,required=True);ap.add_argument('--prefix',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True)
    records=[json.loads(x) for x in (a.run/'episodes.jsonl').read_text().splitlines()];summary=json.loads((a.run/'summary.json').read_text());assignments=json.loads((a.run/'assignments.json').read_text());old=[json.loads(x) for x in (a.prefix/'episodes.jsonl').read_text().splitlines()]
    assert records[:len(old)]==old and len(records)==len(assignments)==384
    keys=[tuple(r[k] for k in ('task','agents','deadline','world','timing','seed')) for r in records];assert len(set(keys))==384
    rows=[]
    for r,c in zip(records,assignments):
        assert all(r[k if k!='n' else 'agents']==v for k,v in c.items())
        for arm in ARMS:
            o=r['outcomes'][arm];ev=o['evaluation'];assert o['valid'] and not o['error'];assert 1<=o['round']<=r['deadline']
            rows.append({k:r[k] for k in ('task','agents','deadline','world','timing')}|{'arm':arm,'choice':o['choice'],'commit_tick':o['round'],'logical_actor_calls':o['logical_actor_calls']}|ev)
    for arm in ARMS:
        rs=[r for r in rows if r['arm']==arm];s=summary['arms'][arm]
        assert len(rs)==s['assigned'] and sum(r['correct'] for r in rs)==s['correct'] and sum(r['constraint_violation'] for r in rs)==s['violations'] and sum(r['abstention'] for r in rs)==s['abstentions']
        assert abs(sum(r['loss'] for r in rs)/len(rs)-s['mean_loss'])<1e-12
        assert collections.Counter(r['target'] for r in rs)==dict.fromkeys(('A','B','C','NONE'),96)
    receipts=json.loads((a.run/'receipts.json').read_text());assert all(r['valid'] and not r['encoding']['truncated'] and not r['head_truncated'] for r in receipts)
    assert len(receipts)==summary['physical_calls'];assert sum(r['encoded_tokens'] for r in receipts)==summary['encoded_input_tokens']
    with (a.out/'outcomes.csv').open('w') as f:
        w=csv.DictWriter(f,fieldnames=list(rows[0]));w.writeheader();w.writerows(rows)
    cells=[]
    for world in ('clean','copies','early-wrong','late-wrong'):
        for timing in ('late','stalled'):
            for n in (5,9):
                for deadline in (3,6):
                    rs=[r for r in records if (r['world'],r['timing'],r['agents'],r['deadline'])==(world,timing,n,deadline)]
                    for baseline in ('fixed-three','fixed-two'):
                        delta=[r['outcomes']['adaptive']['evaluation']['loss']-r['outcomes'][baseline]['evaluation']['loss'] for r in rs]
                        cells.append({'world':world,'timing':timing,'agents':n,'deadline':deadline,'baseline':baseline,'tasks':len(rs),'mean_paired_loss_difference':sum(delta)/len(delta),'per_task':dict(zip([r['task'] for r in rs],delta))})
    (a.out/'paired-contrasts.json').write_text(json.dumps(cells,indent=2))
    integrity={'assigned_blocks':384,'unique_blocks':len(set(keys)),'policy_outcomes':len(rows),'preserved_prefix_blocks':len(old),'prefix_exact':True,'balanced_targets_per_arm':96,'summary_reconciled':True,'all_receipts_valid_untruncated':True,'events_sha256':hashlib.sha256((a.run/'episodes.jsonl').read_bytes()).hexdigest()}
    (a.out/'integrity.json').write_text(json.dumps(integrity,indent=2))
    im=Image.new('RGB',(1600,1030),BG);d=ImageDraw.Draw(im)
    text(d,(48,25),'ANTSY / why timing matters',40);text(d,(48,86),'Nine scouts, six-tick cutoff. Each row: the same 12 task clusters, paired across policies.',23,MUTED)
    text(d,(48,126),'Green = correct   /   coral = constraint violation   /   gray = abstention',22,MUTED)
    for j,arm in enumerate(('fixed-two','fixed-three','adaptive')):text(d,(590+j*325,186),arm,26)
    for i,(world,timing) in enumerate(( (w,t) for w in ('clean','copies','early-wrong','late-wrong') for t in ('late','stalled'))):
        y=245+i*80;text(d,(48,y),world,24);text(d,(290,y),timing,23,MUTED)
        rs=[r for r in records if (r['world'],r['timing'],r['agents'],r['deadline'])==(world,timing,9,6)]
        for j,arm in enumerate(('fixed-two','fixed-three','adaptive')):
            x=555+j*325;os=[r['outcomes'][arm]['evaluation'] for r in rs]
            counts=[sum(o['correct'] for o in os),sum(o['constraint_violation'] for o in os),sum(o['abstention'] for o in os)]
            pos=x
            for count,color in zip(counts,('#65ddb4','#ff8f82','#72849c')):
                if count:d.rectangle((pos,y,pos+count/12*270,y+28),fill=color);pos+=count/12*270
            text(d,(x,y+35),f'{counts[0]} correct / {counts[1]} violate / {counts[2]} wait',16,MUTED)
    text(d,(48,930),'Late correction rewards waiting. Late misinformation punishes it. A fixed low quorum remains essential.',21)
    text(d,(48,973),'Designed synthetic stress cases; no policy dominates, and learned extraction matched symbolic code.',21,MUTED)
    im.save(a.out/'tradeoffs.png');print(json.dumps(integrity))


if __name__=='__main__':main()
