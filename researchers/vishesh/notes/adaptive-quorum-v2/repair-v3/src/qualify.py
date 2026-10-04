import argparse
import json
import signal
import subprocess
from pathlib import Path
from runtime import Runtime
from adapter import Hybrid
from engine import fixture,symbolic


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
    a.out.mkdir(parents=True,exist_ok=False);signal.alarm(1200)
    manifest={'stage':'Q1','code':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'complete':False}
    assignments=[{'task':t,'rows':fixture(t)['truth']} for t in range(8000,8016)]
    # Qualification of the declared bounded scenario, plus separately scored threshold edge probes.
    edges=[{'scanned':s,'retention_days':r,'accuracy':acc,'price':1} for s,r,acc in [(True,0,89),(True,0,90),(True,1,95),(False,0,95),(True,0,95),(False,30,70)]]
    (a.out/'assignments.json').write_text(json.dumps({'tasks':assignments,'edges':edges},indent=2))
    (a.out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    runtime=Runtime();hybrid=Hybrid(runtime);results=[]
    with (a.out/'results.jsonl').open('x') as out:
        for c in assignments+ [{'task':f'edge-{i}','rows':{k:dict(row,price=j+1) for j,k in enumerate(('A','B','C'))}} for i,row in enumerate(edges)]:
            try:choice=hybrid(c['rows'],{'qualification':c['task']});error=None
            except Exception as exc:choice=None;error=type(exc).__name__
            r={'task':c['task'],'target':symbolic(c['rows']),'choice':choice,'error':error,'correct':choice==symbolic(c['rows'])};results.append(r);out.write(json.dumps(r)+'\n');out.flush()
            (a.out/'receipts.json').write_text(json.dumps(runtime.receipts));(a.out/'invocations.json').write_text(json.dumps(hybrid.invocations))
    core=results[:16];edge=results[16:]
    bylabel={k:sum(r['correct'] for r in core if r['target']==k) for k in ('A','B','C','NONE')}
    summary={'assigned':22,'completed':len(results),'core_correct':sum(r['correct'] for r in core),'core_by_target_out_of_4':bylabel,'edge_correct_out_of_6':sum(r['correct'] for r in edge),'invalid':sum(r['error'] is not None for r in results),'physical_calls':len(runtime.receipts),'logical_predicates':len(hybrid.invocations),'qualification_pass':all(v==4 for v in bylabel.values()) and all(r['correct'] for r in edge) and all(r['error'] is None for r in results)}
    manifest.update(runtime.metadata,complete=True);(a.out/'manifest.json').write_text(json.dumps(manifest,indent=2));(a.out/'summary.json').write_text(json.dumps(summary,indent=2));print(json.dumps(summary))


if __name__=='__main__':main()
