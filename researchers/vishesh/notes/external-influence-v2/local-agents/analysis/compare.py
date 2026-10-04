"""Pair local results with archived Haiku evidence; never enters model prompts."""
import argparse,collections,gzip,hashlib,json
from pathlib import Path
KEYS=('domain','task_id','seed','world','dose','n_agents','verification','arm')
HASHES=('truth_hash','corpus_hash','exposure_hash')
def key(r):return tuple(r[k] for k in KEYS)
def metrics(rows):
 return {'assigned':len(rows),'valid':sum(r['validity']['ok'] for r in rows),'correct':sum(r['evaluation']['correct'] for r in rows),'harmful':sum(r['evaluation'].get('harmful_target') or 0 for r in rows),'harmful_unknown':sum(r['evaluation'].get('harmful_target') is None for r in rows),'regret_mean':sum(r['evaluation']['regret'] for r in rows)/len(rows) if rows else None}
def compare(local,baseline):
 manifest=json.loads((baseline/'manifest.json').read_text())
 if manifest['model']!='claude-haiku-4-5-20251001' or manifest['params']['stage']!='S1':raise ValueError('wrong_historical_baseline')
 old=[json.loads(x) for x in (baseline/'episodes.jsonl').read_text().splitlines()]
 new=[json.loads(x) for x in (local/'episodes.jsonl').read_text().splitlines()]
 old_by={key(r):r for r in old};new_by={key(r):r for r in new}
 if len(old_by)!=len(old) or len(new_by)!=len(new):raise ValueError('duplicate_assignment')
 pairs=[]
 for k,n in new_by.items():
  h=old_by[k]
  if any(n[f]!=h[f] for f in HASHES):raise ValueError('fixture_mismatch')
  pairs.append({'assignment':{f:n[f] for f in KEYS},'hashes':{f:n[f] for f in HASHES},'historical':{'choice':h.get('choice'),'validity':h['validity'],'evaluation':h['evaluation']},'local':{'choice':n.get('choice'),'validity':n['validity'],'evaluation':n['evaluation']}})
 historical=[old_by[key(n)] for n in new]
 cells=[]
 for d,w in sorted({(r['domain'],r['world']) for r in new}):
  cells.append({'domain':d,'world':w,'historical':metrics([r for r in historical if r['domain']==d and r['world']==w]),'local':metrics([r for r in new if r['domain']==d and r['world']==w])})
 arms=[]
 for arm in sorted({r['arm'] for r in new}):
  arms.append({'arm':arm,'historical':metrics([r for r in historical if r['arm']==arm]),'local':metrics([r for r in new if r['arm']==arm])})
 output={'historical_run':'external-influence-v2/38908910','historical_model':manifest['model'],'historical_source':manifest['git_commit'],'historical_rows_sha256':hashlib.sha256((baseline/'episodes.jsonl').read_bytes()).hexdigest(),'local_stage':local.name,'all_fixture_hashes_match':True,'historical':metrics(historical),'local':metrics(new),'correct_delta':sum(n['evaluation']['correct']-old_by[key(n)]['evaluation']['correct'] for n in new),'changed_choices':sum(n.get('choice')!=old_by[key(n)].get('choice') for n in new),'local_only_correct':sum(n['evaluation']['correct'] and not old_by[key(n)]['evaluation']['correct'] for n in new),'historical_only_correct':sum(not n['evaluation']['correct'] and old_by[key(n)]['evaluation']['correct'] for n in new),'cells':cells,'arms':arms,'pairs':pairs,'limitations':'Historical model-plus-backend-plus-schema comparison on three task roots; dependent outcomes, no significance test or broad superiority claim.'}
 (local/'comparison.json').write_text(json.dumps(output,indent=2)+'\n')
 print(json.dumps({k:output[k] for k in ('local_stage','all_fixture_hashes_match','historical','local','correct_delta','changed_choices','local_only_correct','historical_only_correct')}))
 return output
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('local',type=Path);p.add_argument('baseline',type=Path);a=p.parse_args();compare(a.local,a.baseline)
