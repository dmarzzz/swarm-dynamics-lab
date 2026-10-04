"""Paired-by-world Sonnet minus Haiku comparison against sybil-budget-api S1 (no API calls).

Assignments are identical by id and packet hash; the world (task) is the independent unit.
Usage: python3.12 reporting/compare_haiku.py <sonnet S1 records dir> <out.json>
"""
import json,random,sys
from collections import defaultdict
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import analyze

HAIKU=Path(__file__).resolve().parents[2]/'sybil-budget-api/records/s1-001-episodes.jsonl.gz'
METRICS=('rare_accuracy','bad_seat_share','specialist_retention')

def boot(per_world,reps=4000,seed=20261004):
    worlds=sorted(per_world);rng=random.Random(seed);means=[]
    for _ in range(reps):
        s=[per_world[rng.choice(worlds)] for _ in worlds];means.append(sum(s)/len(s))
    means.sort();return [means[int(0.025*reps)],means[int(0.975*reps)-1]]

def main(sdir,out):
    s={r['id']:r for r in analyze.read_rows(Path(sdir)/'episodes.jsonl.gz')}
    h={r['id']:r for r in analyze.read_rows(HAIKU)}
    assert set(s)==set(h),'assignment_sets_differ'
    assert all(s[i]['packet_hash']==h[i]['packet_hash'] for i in s),'packet_hash_mismatch'
    assert all(r['status']=='completed' for r in list(s.values())+list(h.values())),'invalid_rows'
    cells=defaultdict(lambda:defaultdict(list));overall=defaultdict(list)
    for i,a in s.items():
        b=h[i];key=tuple(a[k] for k in analyze.KEYS);d=a['evaluation']['rare_accuracy']-b['evaluation']['rare_accuracy']
        cells[key][a['task']].append(d);overall[a['task']].append(d)
    def wmean(per):return {w:sum(v)/len(v) for w,v in per.items()}
    ow=wmean(overall);res={'pairs':len(s),'worlds':len(ow),'overall_rare_accuracy_diff':sum(ow.values())/len(ow),'overall_interval':boot(ow),'cells':[]}
    for key,per in sorted(cells.items()):
        w=wmean(per);sm=[s[i]['evaluation'] for i in s if tuple(s[i][k] for k in analyze.KEYS)==key];hm=[h[i]['evaluation'] for i in h if tuple(h[i][k] for k in analyze.KEYS)==key]
        res['cells'].append({**dict(zip(analyze.KEYS,key)),'sonnet':{m:sum(e[m] for e in sm)/len(sm) for m in METRICS},'haiku':{m:sum(e[m] for e in hm)/len(hm) for m in METRICS},'rare_accuracy_diff':sum(w.values())/len(w),'interval':boot(w,reps=2000)})
    # Primary contrast per model: coverage, visible, N972, pass 0.1, 108 minus 4 checks
    def primary(rows):
        per=defaultdict(dict)
        for r in rows.values():
            if r['n']==972 and r['arm']=='coverage' and r['attacker_pass']==0.1 and r['visibility']=='visible' and r['checks'] in (4,108):
                per[r['task']][r['checks']]=r['evaluation']['rare_accuracy']
        return {w:v[108]-v[4] for w,v in per.items()}
    ps,ph=primary(s),primary(h);dd={w:ps[w]-ph[w] for w in ps}
    res['primary']={'sonnet':sum(ps.values())/len(ps),'sonnet_interval':boot(ps),'haiku':sum(ph.values())/len(ph),'haiku_interval':boot(ph),'sonnet_minus_haiku':sum(dd.values())/len(dd),'difference_interval':boot(dd),'worlds':len(dd)}
    res['cells_sonnet_higher']=sum(c['rare_accuracy_diff']>0 for c in res['cells']);res['cells_haiku_higher']=sum(c['rare_accuracy_diff']<0 for c in res['cells'])
    Path(out).write_text(json.dumps(res,indent=1));return res

if __name__=='__main__':
    r=main(sys.argv[1],sys.argv[2]);print(json.dumps({k:v for k,v in r.items() if k!='cells'},indent=1))
