"""Post-hoc observed-input rule replay; not a newly executed intervention."""
import argparse,collections,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(BASE/'src'))
from protocol import aggregate,apply_checks,validate_report
from environment import choose

def diagnose(directory):
 rows=[json.loads(s) for s in (directory/'episodes.jsonl').read_text().splitlines()]
 events=collections.defaultdict(list)
 for line in (directory/'events.jsonl').read_text().splitlines():
  e=json.loads(line);events[e['assignment']].append(e)
 details=[];structural=[]
 for i,es in sorted(events.items()):
  request=None
  for e in es:
   if e['kind']=='request':request=e['request']
   if e['kind']=='response' and e['phase'] in ('initial','revision'):
    o=request['observation'];allowed={d['id'] for d in o['documents']}|{c for p in o.get('peers',[]) for x in p['estimates'] for c in x['citations']}
    try:validate_report(e['answer'],o['brief'],allowed)
    except Exception as exc:structural.append({'assignment':i,'phase':e['phase'],'reason':str(exc)})
  chair=next((e['request']['observation'] for e in es if e['kind']=='request' and e['phase']=='chair'),None)
  decision=next((e['answer'] for e in es if e['kind']=='response' and e['phase']=='chair'),None)
  truth=next((e for e in es if e['kind']=='evaluation_only'),None)
  if chair and decision and truth:
   estimates=aggregate(chair['reports']);before=choose(estimates,chair['brief']);apply_checks(estimates,chair['checks']);after=choose(estimates,chair['brief'])
   details.append({'assignment':i,'observed_choice':decision['choice'],'before_checks_rule_choice':before,'after_checks_rule_choice':after,'evaluator_best':truth['best'],'observed_correct':int(decision['choice']==truth['best']),'counterfactual_correct':int(after==truth['best']),'chair_rule_disagreement':int(after!=decision['choice']),'available_checks':sum(c['result']['available'] for c in chair['checks'])})
 output={'label':'Post-hoc deterministic replay of identical chair-visible inputs; not a model run or measured intervention effect. Truth is only used to score the counterfactual.','assigned':len(rows),'valid_chair_cases':len(details),'structural_failures':structural,'observed_correct_among_valid':sum(x['observed_correct'] for x in details),'counterfactual_correct_among_valid':sum(x['counterfactual_correct'] for x in details),'disagreements':sum(x['chair_rule_disagreement'] for x in details),'details':details}
 (directory/'decision-diagnosis.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='details'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();diagnose(a.directory)
