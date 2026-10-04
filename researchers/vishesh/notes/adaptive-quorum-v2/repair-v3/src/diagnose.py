import argparse
import json
import platform
import signal
import subprocess
import sys
from pathlib import Path
from runtime import Runtime

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT.parent/'src'))
import study


def prose(state):
    lines=[]
    for d in state['observations']:
        lines.append(f"Source {d['root']}, revision {d['revision']}: Provider {d['provider']} {'supports' if d['scanned'] else 'does not support'} scanned PDFs; retains documents for {d['retention_days']} days; accuracy {d['accuracy']} percent; price {d['price']} per document.")
    for d in state['tests']:
        lines.append(f"Independent test of provider {d['provider']}: measured accuracy {d['accuracy']} percent. This test says nothing about retention or price.")
    return '\n'.join(lines)


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--out',type=Path,required=True);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=False);signal.alarm(1200)
    meta={'stage':'D0','code':subprocess.check_output(['git','rev-parse','HEAD'],text=True).strip(),'platform':platform.platform(),'complete':False}
    (a.out/'manifest.json').write_text(json.dumps(meta,indent=2));model=Runtime();meta.update(model.metadata)
    cases=[]
    for task in range(7400,7408):
        f=study.fixture(task);docs=study.reports(f,'clean','fast',9);target=study.best(f['truth'])
        for tool in (False,True):
            state=study.state_for(docs,[study.mock_probe(f,k) for k in ('A','B')] if tool else [])
            for representation in ('json','prose'):
                cases.append({'id':f'{task}-{representation}-{tool}','kind':representation+'-tools' if tool else representation,'state':json.dumps(state) if representation=='json' else prose(state),'instructions':study.RULE,'criteria':{k:k for k in study.CHOICES},'target':target})
        row=f['truth']['A']
        for field,question,target in [('scanned','Does provider A support scanned PDFs?',row['scanned']),('retention_days','Does provider A retain documents for zero days?',row['retention_days']==0),('accuracy','Does provider A have accuracy at least 90 percent?',row['accuracy']>=90)]:
            cases.append({'id':f'{task}-atomic-{field}','kind':'atomic-'+field,'state':f"Provider A: scanned PDF support is {row['scanned']}; retention is {row['retention_days']} days; accuracy is {row['accuracy']} percent.",'instructions':question,'criteria':{'YES':'Yes','NO':'No'},'target':'YES' if target else 'NO'})
    (a.out/'assignments.json').write_text(json.dumps(cases,indent=2))
    results=[]
    with (a.out/'results.jsonl').open('x') as out:
        for c in cases:
            try:choice=model.choose(c['state'],c['instructions'],c['criteria'],{'case':c['id']});error=None
            except Exception as exc:choice=None;error=type(exc).__name__
            r={'id':c['id'],'kind':c['kind'],'target':c['target'],'choice':choice,'error':error,'correct':choice==c['target']};results.append(r);out.write(json.dumps(r)+'\n');out.flush()
            (a.out/'receipts.json').write_text(json.dumps(model.receipts))
    summary={k:{'assigned':sum(r['kind']==k for r in results),'correct':sum(r['kind']==k and r['correct'] for r in results),'invalid':sum(r['kind']==k and r['error'] is not None for r in results)} for k in sorted({r['kind'] for r in results})}
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2));meta['complete']=True;(a.out/'manifest.json').write_text(json.dumps(meta,indent=2));print(json.dumps(summary))


if __name__=='__main__':main()
