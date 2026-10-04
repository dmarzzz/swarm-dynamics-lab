"""All-assigned, within-world paired estimates; no pseudoreplicated intervals."""
import json
from pathlib import Path
import sys
from statistics import mean

CONTRASTS=[('shared_restore_with_filter','Q11','Q10F'),('filter_with_restore','Q11','Q11R'),('shared_restore_without_filter','Q11R','Q10'),('filter_without_restore','Q10F','Q10')]

def analyze(out):
    manifest=json.loads((out/'manifest.json').read_text())
    rows=[json.loads(line) for line in (out/'episodes.jsonl').read_text().splitlines()]
    def key(r):return (r['world'],r['task_id'],r['seed'],r['dose'],r['arm'])
    observed={key(r):r for r in rows}
    if len(observed)!=len(rows):raise ValueError('duplicate outcomes')
    assigned={key(r) for r in manifest['planned_outcomes']}
    if not set(observed)<=assigned:raise ValueError('unassigned outcome')
    result={'model_backed':manifest['model_backed'],'source_hash':manifest['source_hash'],'assigned':len(assigned),'recorded':len(rows),'missing':len(assigned-set(observed)),'invalid':sum(not r['validity']['ok'] for r in rows),'strata':{}}
    for world in sorted({k[0] for k in assigned}):
        worlds=sorted({k[:4] for k in assigned if k[0]==world})
        effects={}
        def utility(k):
            value=observed.get(k,{}).get('evaluation',{}).get('utility')
            return float(value) if isinstance(value,(int,float)) else 0.0
        for name,a,b in CONTRASTS:
            pairs=[k for k in worlds if k+(a,) in assigned and k+(b,) in assigned]
            diffs=[utility(k+(a,))-utility(k+(b,)) for k in pairs]
            valid=[k for k in pairs if all(observed.get(k+(arm,),{}).get('validity',{}).get('ok',False) for arm in (a,b))]
            effects[name]={'all_assigned_difference':mean(diffs) if diffs else None,'assigned_pairs':len(pairs),'valid_pairs':len(valid),'complete_pair_difference':mean([utility(k+(a,))-utility(k+(b,)) for k in valid]) if valid else None}
        effects['interaction']=effects['shared_restore_with_filter']['all_assigned_difference']-effects['shared_restore_without_filter']['all_assigned_difference']
        result['strata'][world]=effects
    return result

if __name__=='__main__':
    out=Path(sys.argv[1]);result=analyze(out)
    (out/'factorial-analysis.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
