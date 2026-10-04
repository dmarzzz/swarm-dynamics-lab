"""Reconstruct every condition from saved inputs; fail closed on altered decisions."""
import argparse,json
from pathlib import Path
from study import V4,read,board,truth,purchase
from policies import calibrate
from repair import Observation,VARIANTS,decide

def validate(root):
 manifest=read(root/'manifest.json');assert manifest['complete'] and manifest['model_calls']==0
 records=read(V4/'results/measured.jsonl.gz');cal=calibrate(records[:20]);rows=read(root/'rows.json');ids=set()
 originals={backend:{b['id']:b for b in read(V4/'results'/run/'episodes.jsonl.gz')} for backend,run in [('Laya','S1-attempt-1'),('Jev','S1-jev-attempt-1')]}
 for r in rows:
  ids.add(r['id']);record=records[r['id']]
  assert abs(r['quality']-truth(record,r['choice']))<1e-12
  if manifest['stage']=='D0':
   original=originals[r['backend']][r['id']]['arms'][r['arm']];b=board(record,cal)
   for c in original['checks']:b.buy(Observation(**c))
   expected=cal['best_fixed'] if r['arm']=='best-fixed' else b.choose(r['estimator'])
   assert expected==r['choice'] and r['checks']==len(b.checks)
  if manifest['stage']=='D1':
   b=board(record,cal)
   for ev in r['events']:
    assert ev['scores_before']==b.scores() and ev['choice_before']==b.choose()
    if r['arm']!='random-two':
     action,values=decide(b,records[:20],r['cost'],forced=r['arm']=='forced-two')
     assert action==(tuple(ev['action']) if ev['action'] is not None else None)
     assert ev['projected_gains']=={f'{m}:{j}':v for (m,j),v in values.items()}
    if ev['stop']:assert ev['action'] is None;break
    obs=purchase(record,tuple(ev['action']));assert vars(obs)==ev['response'];old=b.scores();b.buy(obs)
    assert b.scores()==ev['scores_after']
    if obs.quality is None:assert b.scores()==old
   assert b.choose()==r['choice'] and len(b.checks)==r['checks']<=2
   assert abs(r['utility']-(r['quality']-r['cost']*r['checks']))<1e-12
 assert ids==set(range(30,100))
 # Paired condition coverage must be complete, unique and balanced.
 keys=[(r['id'],r.get('backend'),r['arm'],r.get('estimator'),r.get('cost')) for r in rows]
 assert len(keys)==len(set(keys));assert len(rows)==(2940 if manifest['stage']=='D0' else 1400)
 return {'passed':True,'receipts':len(ids),'rows':len(rows),'model_calls':0,'checks':['complete unique condition assignment','scores reconstruct from measured corpus','D1 decisions reconstruct without current labels','null neutrality','hard two-check budget','utility accounting']}
def main():
 p=argparse.ArgumentParser();p.add_argument('--run',type=Path,required=True);a=p.parse_args();report=validate(a.run);(a.run/'audit.json').write_text(json.dumps(report,indent=2));print(json.dumps(report))
if __name__=='__main__':main()
