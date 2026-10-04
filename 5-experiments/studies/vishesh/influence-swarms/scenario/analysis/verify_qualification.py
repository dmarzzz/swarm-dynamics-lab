"""Offline qualification instrument audit. Never calls a model or opens a gate."""
import argparse,json,sys,subprocess
from pathlib import Path
S=Path(__file__).resolve().parents[1];sys.path.insert(0,str(S/'src'))
from dossier import build,digest
from study import run
from run import Scripted

def execute(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False);results=[];calls=0
    spec=json.loads((S/'qualification-v2.json').read_text())
    for i,c in enumerate(spec['cases']):
        case=build(c['family'],i,c['world'],seed=37,dossier_spec=c)
        (out/f'case-{i}.json').write_text(json.dumps(case,indent=2))
        with (out/f'events-{i}.jsonl').open('x') as f:r=run(case,Scripted(),lambda e:f.write(json.dumps(e)+'\n'))
        results+=r['outcomes'];calls+=r['calls']
    summary={'status':'SCRIPTED / NOT MODEL EVIDENCE','commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=S,text=True).strip(),
             'cases':len(spec['cases']),'assigned':len(results),'valid':sum(r['valid'] for r in results),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in results),
             'logical_calls':calls,'api_calls':0,'usd':0,'qualification_file_hash':digest(spec),
             'outcome_hash':digest(results),'answer_labels':sorted({r['decision']['choice'] for r in results}),
             'decisions':[{'case':r['case_id'],'arm':r['arm'],'choice':r['decision']['choice'],'acceptable':r['evaluation']['acceptable_decision']} for r in results]}
    (out/'outcomes.json').write_text(json.dumps(results,indent=2));(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n');return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();print(json.dumps(execute(a.out)))
