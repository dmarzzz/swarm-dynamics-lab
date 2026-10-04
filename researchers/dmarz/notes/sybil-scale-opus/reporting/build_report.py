"""Reconcile saved synthetic observations and produce public aggregate tables/figures.

This post-collection script never calls a model or changes the frozen runtime.
"""
import argparse,csv,gzip,hashlib,json,sys
from collections import defaultdict
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
sys.path.insert(0,str(ROOT/'src'))
import analyze,render,study

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input',type=Path);ap.add_argument('output',type=Path);a=ap.parse_args()
    a.output.mkdir(parents=True,exist_ok=True)
    rows=analyze.read_rows(a.input/'episodes.jsonl.gz');assigned={r['id']:r for r in analyze.read_rows(a.input/'assignments.jsonl.gz')}
    summary=json.loads((a.input/'summary.json').read_text())
    assert len(rows)==len(assigned)==summary['planned'];assert len({r['id'] for r in rows})==len(rows)
    for row in rows:
        if row['status']=='completed':
            assignment=assigned[row['id']]
            assert study.digest(assignment['packet'])==row['packet_hash']
            assert study.evaluate(assignment,row['answer'])==row['evaluation']
            assert study.evaluate(assignment,study.scripted(assignment['packet']))==row['scripted_evaluation']
    result=analyze.analyze(rows)
    assert result==json.loads((a.input/'analysis.json').read_text())
    result['execution']=summary
    by=defaultdict(list)
    for row in rows:
        if row['status']=='completed' and row['kind']=='pilot':by[(row['n'],row['arm'],row['checks'],row['attacker_pass'])].append(row)
    badges=[]
    for key,rr in sorted(by.items()):
        masked={r['task']:r for r in rr if r['visibility']=='masked'};visible={r['task']:r for r in rr if r['visibility']=='visible'}
        tasks=sorted(set(masked)&set(visible));diffs=[visible[t]['evaluation']['rare_accuracy']-masked[t]['evaluation']['rare_accuracy'] for t in tasks]
        badges.append(dict(zip(['n','arm','checks','attacker_pass'],key),clusters=len(tasks),mean=sum(diffs)/len(diffs),interval=analyze.interval(diffs)))
    result['badge_contrasts']=badges
    # Descriptive paired comparisons use worlds, never individual skill answers.
    # These supplements do not change the frozen primary analysis above.
    cells=defaultdict(dict)
    for row in rows:
        if row['status']=='completed' and row['kind']=='pilot':
            cells[tuple(row[k] for k in ('n','arm','checks','attacker_pass','visibility'))][row['task']]=row
    def paired(left,right,metric):
        tasks=sorted(set(left)&set(right))
        values=[left[t]['evaluation'][metric]-right[t]['evaluation'][metric] for t in tasks]
        return {'clusters':len(tasks),'mean':sum(values)/len(values) if values else None,'interval':analyze.interval(values)}
    result['budget_security_contrasts']=[]
    result['coverage_random_contrasts']=[]
    result['model_plurality_contrasts']=[]
    for key,cc in sorted(cells.items()):
        n,arm,checks,rate,visibility=key
        labels=dict(zip(('n','arm','checks','attacker_pass','visibility'),key))
        values=[r['evaluation']['rare_accuracy']-r['scripted_evaluation']['rare_accuracy'] for _,r in sorted(cc.items())]
        result['model_plurality_contrasts'].append({**labels,'clusters':len(values),'mean':sum(values)/len(values),'interval':analyze.interval(values)})
        if arm!='no_verification' and checks==n//9:
            fixed=cells.get((n,arm,4,rate,visibility),{})
            result['budget_security_contrasts'].append({**labels,**paired(cc,fixed,'bad_seat_share')})
        if arm=='coverage':
            random=cells.get((n,'random',checks,rate,visibility),{})
            result['coverage_random_contrasts'].append({**labels,'rare_accuracy':paired(cc,random,'rare_accuracy'),'bad_seat_share':paired(cc,random,'bad_seat_share')})
    result['failure_modes']=[]
    for cell in result['cells']:
        rr=[r for r in rows if r['status']=='completed' and all(r[k]==cell[k] for k in ('n','arm','checks','attacker_pass','visibility'))]
        truth_wrong=0;abstentions=0
        for row in rr:
            for s in range(3,6):
                v=row['answer']['values'][str(s)];truth=assigned[row['id']]['answers'][s]
                abstentions+=v is None;truth_wrong+=v is not None and v!=truth
        result['failure_modes'].append({**{k:cell[k] for k in ('n','arm','checks','attacker_pass','visibility')},'rare_fields':len(rr)*3,'wrong_nonnull':truth_wrong,'abstentions':abstentions})
    result['inputs']={p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(a.input.iterdir()) if p.is_file()}
    (a.output/'results-summary.json').write_text(json.dumps(result,indent=2)+'\n')
    flat=[]
    for c in result['cells']:
        row={k:c[k] for k in ('n','arm','checks','attacker_pass','visibility','assigned','valid','assigned_accuracy','scripted_accuracy')}
        for key,values in c['metrics'].items():
            row[key]=values['mean'];row[key+'_low']=values['interval'][0] if values['interval'] else None;row[key+'_high']=values['interval'][1] if values['interval'] else None
        flat.append(row)
    if flat:
        with (a.output/'results-cells.csv').open('w') as f:
            w=csv.DictWriter(f,fieldnames=list(flat[0]));w.writeheader();w.writerows(flat)
    for visibility,name in [('visible','results-visible.png'),('masked','results-hidden.png')]:
        render.frame(rows,len(rows),summary['params']['stage'],summary['elapsed_seconds'],summary['study_accounting'],visibility).save(a.output/name)
    (a.output/'reconciliation.json').write_text(json.dumps({'assigned':len(assigned),'rows':len(rows),'recomputed':sum(r['status']=='completed' for r in rows),'source_hash':summary['params']['source_hash'],'analysis_matches':True},indent=2)+'\n')
    print(json.dumps({'rows':len(rows),'cells':len(result['cells']),'primary':result['primary'],'cost_usd':summary['cost_usd']}))
if __name__=='__main__':main()
