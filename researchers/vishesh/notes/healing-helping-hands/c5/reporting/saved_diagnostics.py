"""Saved-response diagnostics only. Never imports a provider or dispatches calls."""
import json, argparse, collections, hashlib
from pathlib import Path

def run(root,out):
    out.mkdir(parents=True,exist_ok=True)
    obs=json.loads((root/'observations.json').read_text()); summary=json.loads((root/'summary.json').read_text())
    events=[json.loads(s) for s in (root/'calls.jsonl').read_text().splitlines()]
    starts={e['id']:e for e in events if e['type']=='start'}
    referred={r['id'] for r in obs if r['status']=='completed' and r['labels']['a']!=r['labels']['b']}
    actual=collections.Counter(); derived=collections.Counter(); models=collections.Counter(); endings=collections.Counter()
    for e in events:
        if e['type']!='completed':continue
        s=starts[e['id']]; v=e['result']; model=s['model']; models[v.get('served_model',v['raw'].get('model'))]+=1
        actual[model+'_calls']+=1;actual[model+'_seconds']+=e['seconds'];actual[model+'_recorded_api_usd']+=v.get('cost_usd',0)
        if model=='qwen':endings[v['raw'].get('done_reason','unknown')]+=1
        for k in ['input_tokens','output_tokens']:actual[model+'_'+k]+=v.get(k,0)
        if model=='qwen' or s['row_id'] in referred:
            derived[model+'_calls']+=1;derived['summed_observed_call_seconds']+=e['seconds'];derived['recorded_jev_api_usd']+=v.get('cost_usd',0)
    complete=[r for r in obs if r['status']=='completed']
    conf={k:{g:{v:sum(r['expected']==g and r['labels'][k]==v for r in complete) for v in ['SUPPORT','REFUTE','UNCERTAIN']} for g in ['SUPPORT','REFUTE','UNCERTAIN']} for k in ['a','b','jev']}
    wrong=sum(r['labels']['a']!=r['expected'] for r in complete); caught=sum(r['id'] in referred and r['labels']['a']!=r['expected'] for r in complete)
    result={'saved_data_only':True,'calls_sha256':hashlib.sha256((root/'calls.jsonl').read_bytes()).hexdigest(),'assigned':len(obs),'completed':len(complete),'actual_collection':dict(actual),'counterfactual_cascade':dict(derived),'served_models':dict(models),'qwen_done_reasons':dict(endings),'qwen_A_errors':wrong,'qwen_A_errors_referred':caught,'error_detection_recall':caught/wrong if wrong else None,'confusion':conf,'limits':['Counterfactual cascade derives selections from actual all-controls collection.','Local Qwen computation has no dollar price here; API-charge reduction is not total-cost reduction.','Summed call seconds are observed serial service time, not a randomized production-latency comparison; call order and caching can matter.','Instances are nested in authored families; no population confidence interval or powered noninferiority claim.']}
    (out/'diagnostics.json').write_text(json.dumps(result,indent=2)+'\n')
    # Correct presentation wording without changing the frozen collection source.
    if (out/'replay.html').exists():
        page=(out/'replay.html').read_text().replace('grouped by a stable logical curator ID','grouped by authored family, with a stable logical curator ID in the inspector').replace('Replay recorded order','Reveal report tiles')
        (out/'replay-reviewed.html').write_text(page)
    import matplotlib;matplotlib.use('Agg');import matplotlib.pyplot as plt
    families=summary['families'];arms=['qwen','jev','cascade','matched']; names=['Qwen A','Always Jev','Agreement routing','Matched random']
    matrix=[[100*f['error'][a] for a in arms] for f in families.values()]
    fig,ax=plt.subplots(figsize=(11,max(4,len(families)*.47+2)),dpi=140)
    ax.imshow(matrix,vmin=0,vmax=100,cmap='YlOrRd',aspect='auto')
    ax.set_xticks(range(4),names);ax.set_yticks(range(len(families)),[f.replace('_',' ') for f in families]);ax.xaxis.tick_top()
    for i,row in enumerate(matrix):
        for j,v in enumerate(row):ax.text(j,i,f'{v:.1f}%',ha='center',va='center',color='white' if v>=65 else '#172936')
    ax.set_title(root.name+' | assigned error by authored family',pad=32,loc='left')
    fig.text(.02,.018,'Recorded decisions; missing assignments count as errors. Family rows are authored strata, not independent real-world domains.',fontsize=8)
    fig.tight_layout(rect=[0,.045,1,1]);fig.savefig(out/'family-errors.png');plt.close(fig)
    print(json.dumps({'saved_diagnostics_written':True,'assigned':len(obs),'completed':len(complete)}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args();run(a.root,a.out)
