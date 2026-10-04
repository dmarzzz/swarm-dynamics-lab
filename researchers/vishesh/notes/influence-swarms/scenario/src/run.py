"""Offline, bounded development runner. Paid collection intentionally disabled.
Qualification requires independent task review and a fresh dedicated allocation.
"""
import argparse
import json
from pathlib import Path
from dossier import FAMILIES,WORLDS,build,digest
from study import run
class Scripted:
    def complete(self,request,fallback):return fallback(request['observation'])

def execute(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    results=[];calls=0
    for family in FAMILIES:
        for profile in range(4):
            for world in WORLDS:
                case=build(family,profile,world)
                with (out/f'{case["case_id"]}-{world}.jsonl').open('x') as f:
                    def emit(e):f.write(json.dumps(e,sort_keys=True)+'\n');f.flush()
                    result=run(case,Scripted(),emit)
                results.extend(result['outcomes']);calls+=result['calls']
    summary={'status':'offline engineering only','dossiers':24,'families':6,'worlds':4,'assigned':288,
             'terminal':len(results),'invalid':sum(not r['valid'] for r in results),'logical_calls':calls,'api_calls':0,'usd':0,
             'acceptable':sum(r['evaluation']['acceptable_decision'] for r in results if r['valid']),
             'outcome_hash':digest(results),'source_hash':digest({p.name:p.read_text() for p in Path(__file__).parent.glob('*.py')})}
    (out/'outcomes.json').write_text(json.dumps(results,indent=2));(out/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);a=p.parse_args();print(json.dumps(execute(a.out)))
