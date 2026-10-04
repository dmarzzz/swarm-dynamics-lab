"""Offline same-author replay of saved requests and independent row arithmetic."""
import collections,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/'src'))
from cases import digest
from rd4_design import execute,trajectories,ARMS,wire
from live_worker import TransportFailure

def audit(out):
 out=Path(out);records=json.loads((out/'records.json').read_text());calls=json.loads((out/'calls.json').read_text());summary=json.loads((out/'summary.json').read_text())
 mapping={x['request_sha256']:x for x in calls};assert len(mapping)==len(calls)
 class Saved:
  def __init__(self):self.cache={};self.logical_calls=0;self.request_history=[]
  def __call__(self,phase,p):
   req=wire(phase,p);key=digest(req);self.logical_calls+=1;self.request_history.append(key)
   assert key in mapping and mapping[key]['request']==req
   self.cache[key]=mapping[key]
   if mapping[key]['status']!='completed':raise TransportFailure('saved_failure')
   return mapping[key]['checked']['action']
 native=Saved();replayed=[]
 for c in trajectories():
  for arm in ARMS:replayed.extend(execute(c,arm,native))
 assert replayed==records,'Saved decisions do not exactly reproduce recorded trajectories'
 assert native.logical_calls==summary['logical_calls']
 assert len(native.cache)==len(calls)
 paired={};per={}
 for arm in ARMS:
  rows=[r for r in records if r['arm']==arm]
  correctness=[r['final']==r['evaluator']['gold_action'] and r['final']!='DEFER' and r['status']=='completed' and r['on_time'] for r in rows]
  assert correctness==[r['correct_completion'] for r in rows]
  assert sum(correctness)==summary['by_arm'][arm]['correct_on_time']
  assert sum(r['checks'] for r in rows)==summary['by_arm'][arm]['checks']
  per[arm]={}
  for domain in ('bridge','build','alarm'):
   selected=[r for r in rows if r['scenario']==domain];per[arm][domain]={'assigned':len(selected),'correct':sum(r['correct_completion'] for r in selected),'checks':sum(r['checks'] for r in selected)}
  for regime in ('supported','withdrawn','wrong_scope','absent'):
   selected=[r for r in rows if r['condition']==regime];per[arm][regime]={'assigned':len(selected),'correct':sum(r['correct_completion'] for r in selected),'checks':sum(r['checks'] for r in selected)}
 failure_usage={k:[] for k,v in mapping.items() if v['status']!='completed'}
 for r in records:
  for key in r['request_hashes']:
   if key in failure_usage:failure_usage[key].append({k:r[k] for k in ('case_id','arm','epoch')})
 result={'exact_replay_rows':len(records),'all_match':True,'independent_author':False,'native_calls':0,'logical_calls':native.logical_calls,'source_cache_requests':len(native.cache),'by_domain_and_regime':per,'failed_request_usage':failure_usage,'repeat_checks':{a:summary['by_arm'][a]['repeat_checks'] for a in ARMS}}
 (out/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
 print(json.dumps({'exact_replay_rows':len(records),'all_match':True,'model_calls':0}))
if __name__=='__main__':audit(Path(sys.argv[1]))
