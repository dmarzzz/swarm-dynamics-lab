"""Paired world summaries; scripted outcomes never become model findings."""
import argparse,json,random,statistics
from pathlib import Path


def analyze(paths):
    records=[]
    for path in paths:
        records.extend(json.loads(line) for line in path.read_text().splitlines() if line.strip())
    by={}; invalid=0
    for r in records:
        if not r['validity']['ok']: invalid+=1; continue
        if r['stage']=='S1' and r['cell']=={'bridges':1,'attacker_pass':.1,'clean':False,'verification_budget':4}:
            by.setdefault(r['task'],{})[r['arm']]=r['evaluation']
    pairs=[{'task':task,'rare_accuracy_difference':v['coverage']['rare_accuracy']-v['degree']['rare_accuracy'],
            'malicious_admission_difference':v['coverage']['malicious_admission']-v['degree']['malicious_admission']}
           for task,v in sorted(by.items()) if 'coverage' in v and 'degree' in v]
    out={'backend':'scripted','assigned_arm_records':len(records),'invalid':invalid,'model_calls':0,'api_spend_usd':0,
         'primary_development_contrast':'coverage minus degree; bridges=1; attacker_pass=0.1; verification_budget=4',
         'independent_world_clusters':len(pairs),'paired_differences':pairs,
         'interpretation':'Exploratory synthetic fixture; no LLM finding or general security guarantee.'}
    if pairs:
        vals=[p['rare_accuracy_difference'] for p in pairs]; r=random.Random(712)
        boot=sorted(statistics.mean(r.choices(vals,k=len(vals))) for _ in range(2000))
        out.update(mean_rare_accuracy_difference=statistics.mean(vals),descriptive_cluster_bootstrap_95=[boot[50],boot[1949]],
                   mean_malicious_admission_difference=statistics.mean(p['malicious_admission_difference'] for p in pairs))
    return out

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('directory',type=Path); ap.add_argument('--output',type=Path); a=ap.parse_args()
    result=analyze(sorted(a.directory.rglob('episodes.jsonl')))
    if a.output:
        with a.output.open('x') as f: json.dump(result,f,indent=2)
    print(json.dumps(result,indent=2))
