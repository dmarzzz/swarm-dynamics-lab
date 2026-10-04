import json,random,statistics
from pathlib import Path
from study import ARMS,SCENARIOS

def analyze(rows):
    summary={'assigned':len(rows),'completed':sum(r['status']=='completed' for r in rows),'failed':sum(r['status']!='completed' for r in rows),'by_scenario':{}}
    for s in SCENARIOS:
        cells={}
        for a in ARMS:
            rr=[r for r in rows if r['scenario']==s and r['arm']==a]
            if rr:cells[a]={'n':len(rr),'completed':sum(r['status']=='completed' for r in rr),
              'accuracy':statistics.mean(r.get('final_accuracy',0) for r in rr),
              'convention':statistics.mean(r.get('final_convention',0) for r in rr)}
        summary['by_scenario'][s]=cells
    diffs={}
    for s in SCENARIOS:
        lookup={(r['seed'],r['arm']):r for r in rows if r['scenario']==s}
        seeds=sorted({seed for seed,a in lookup if a=='both' and (seed,'neither') in lookup})
        if seeds:diffs[s]=[lookup[seed,'both'].get('final_accuracy',0)-lookup[seed,'neither'].get('final_accuracy',0) for seed in seeds]
    if len(diffs)==3:
        rng=random.Random(24404);boot=sorted(statistics.mean(statistics.mean(rng.choices(d,k=len(d))) for d in diffs.values()) for _ in range(2000))
        summary['primary']={'contrast':'both-minus-neither','difference':statistics.mean(statistics.mean(d) for d in diffs.values()),'ci95':[boot[49],boot[1949]],'worlds':sum(map(len,diffs.values())),'paired_differences':diffs,'note':'Exploratory; two worlds per scenario give weak precision. Failures scored zero.'}
    complete_diffs={}
    for scenario in SCENARIOS:
        lookup={(r['seed'],r['arm']):r for r in rows if r['scenario']==scenario}
        values=[]
        for seed,a in lookup:
            if a=='both' and (seed,'neither') in lookup:
                b,n=lookup[seed,'both'],lookup[seed,'neither']
                if b['status']==n['status']=='completed':values.append(b['final_accuracy']-n['final_accuracy'])
        if values:complete_diffs[scenario]=values
    if complete_diffs:
        summary['complete_case']={'difference':statistics.mean(statistics.mean(d) for d in complete_diffs.values()),
          'worlds':sum(map(len,complete_diffs.values())),'scenarios':len(complete_diffs),
          'note':'Equal weight over available scenarios; compare denominator to conservative primary.'}
    summary['qualification_passed']=all(r['status']=='completed' for r in rows) and all(
      summary['by_scenario'][s].get('verbatim',{}).get('accuracy',0)>=.85 and summary['by_scenario'][s].get('verbatim',{}).get('convention',0)>=.8 for s in SCENARIOS)
    summary['cost']={k:sum(r.get('usage',{}).get(k,0) for r in rows) for k in ['calls','actual_usd','input_tokens','output_tokens','usage_missing']}
    return summary
if __name__=='__main__':
    import sys
    root=Path(sys.argv[1]);rows=[json.loads(p.read_text()) for p in sorted(root.glob('*/outcome.json'))]
    (root/'summary.json').write_text(json.dumps(analyze(rows),indent=2))
    print(json.dumps(analyze(rows),indent=2))
