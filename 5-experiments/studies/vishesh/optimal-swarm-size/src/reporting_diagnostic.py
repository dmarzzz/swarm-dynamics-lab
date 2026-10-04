"""One prospectively documented synthetic reporting episode. No model imports/calls."""
import argparse
import hashlib
import json
from pathlib import Path
from reporting import Reporter
from replay import render


def main():
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args()
    a.output.mkdir(exist_ok=False)
    row={'id':'reporting-q0-a1','stage':'reporting-diagnostic','family':'synthetic-plumbing','structure':'known-interval','root':0,'n':0}
    tldr='TLDR: Synthetic reporting-q0-a1 adapter diagnostic, zero model calls. Compare four uploaded artifacts and terminal status with known local bytes; measure delivery and public visibility. Synthetic intervals and scores are plumbing fixtures, not agent performance.'
    (a.output/'assignment.json').write_text(json.dumps(row|{'tldr':tldr,'synthetic':True},indent=2))
    reporter=Reporter('optimal-swarm-size-reporting-q0',row,tldr)
    trace=[{'kind':'service_start','t':0,'actor':0,'phase':'synthetic','item':'fixture'}, {'kind':'service_end','t':1,'actor':0,'phase':'synthetic','item':'fixture'}, {'kind':'terminal','t':1,'synthetic':True}]
    (a.output/'trace.jsonl').write_text('\n'.join(json.dumps(v|{'synthetic':True}) for v in trace)+'\n')
    record={'synthetic':True,'model_calls':0,'evaluation':{'quality':1},'operational_success':True,'elapsed_s':0,'exposure_microdollars':0,'failure':None,'note':'All scores and intervals are synthetic reporting fixtures, not measured model performance.'}
    (a.output/'outcome.json').write_text(json.dumps(record,indent=2))
    render(a.output/'trace.jsonl',a.output/'replay.html')
    replay=a.output/'replay.html';replay.write_text(replay.read_text().replace('<h1>','<p>SYNTHETIC REPORTING FIXTURE — ZERO MODEL CALLS</p><h1>'))
    progress=reporter.progress(16)
    receipt=reporter.finish(a.output,record)
    summary={'run':reporter.id,'model_calls':0,'progress_acknowledged':progress.get('acknowledged') is True,'publication_complete':receipt['complete'],'sha256':{name:hashlib.sha256((a.output/name).read_bytes()).hexdigest() for name in ('assignment.json','trace.jsonl','outcome.json','replay.html')}}
    (a.output/'diagnostic.json').write_text(json.dumps(summary,indent=2)+'\n')
    print(json.dumps(summary));return 0 if receipt['complete'] else 2

if __name__=='__main__':
    try:raise SystemExit(main())
    except Exception as exc:
        print(json.dumps({'diagnostic_failed':True,'error_class':type(exc).__name__,'model_calls':0}));raise SystemExit(2)
