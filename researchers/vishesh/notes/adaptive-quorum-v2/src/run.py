import argparse
import itertools
import json
import platform
import signal
import subprocess
import time
from pathlib import Path
import study

ROOT=Path(__file__).resolve().parents[1]


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--backend',choices=['scripted','laya'],required=True);ap.add_argument('--out',type=Path,required=True)
    a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);signal.alarm(1800)
    design=json.loads((ROOT/'design.json').read_text())
    assignments=list(itertools.product(design['qualification_tasks'],design['agents'],design['deadlines']))
    (a.out/'assignments.json').write_text(json.dumps(assignments))
    meta={'backend':a.backend,'code':subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip(),
          'stage':'S0','platform':platform.platform(),'design':design,'complete':False}
    (a.out/'manifest.json').write_text(json.dumps(meta,indent=2))
    decide=study.scripted
    if a.backend=='laya':
        from model import Laya
        decide=Laya();meta.update(decide.metadata)
    rows=[];started=time.monotonic()
    with (a.out/'episodes.jsonl').open('x') as out,(a.out/'model-receipts.jsonl').open('x') as receipts:
        for task,n,d in assignments:
            start=len(getattr(decide,'receipts',[]))
            block=study.episode(task,n,d,'clean','fast',decide)
            for r in block:r.update(backend=a.backend,code=meta['code']);out.write(json.dumps(r)+'\n')
            out.flush();rows+=block
            for rec in getattr(decide,'receipts',[])[start:]:receipts.write(json.dumps({'task_id':task,'agents':n,'deadline':d,**rec})+'\n')
            receipts.flush()
    cells=[]
    for arm,n,d in itertools.product(study.ARMS,design['agents'],design['deadlines']):
        cell=[r for r in rows if (r['arm'],r['agents'],r['deadline'])==(arm,n,d)]
        cells.append({'arm':arm,'agents':n,'deadline':d,'assigned':len(cell),
                      **{k:sum(r['evaluation'][k] for r in cell) for k in ('correct','constraint_violation','abstention','false_none')},
                      'invalid':sum(not r['validity']['ok'] for r in cell)})
    summary={'episodes':len(rows),'cells':cells,'qualified':all(c['invalid']==0 and c['correct']/c['assigned']>=.8 for c in cells),
             'physical_calls':getattr(decide,'calls',None),'input_tokens_estimate':getattr(decide,'input_tokens',None),
             'wall_s':time.monotonic()-started}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2));meta['complete']=True
    (a.out/'manifest.json').write_text(json.dumps(meta,indent=2))
    from replay import render
    render(rows,a.out/'replay.html')
    print(json.dumps({k:v for k,v in summary.items() if k!='cells'}))


if __name__=='__main__':main()
