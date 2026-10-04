"""Offline replay against a retained native trace directory; no network/model calls."""
import argparse,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
from native import packet
from contract import request,normalize
from corpus import canonical,sha
ap=argparse.ArgumentParser();ap.add_argument('traces',type=Path);args=ap.parse_args();p=packet();parents={};ids=set();correct={'P':0,'R':0};seen={};load=lambda n:json.loads((args.traces/n).read_text())
for cid,q in p['qualification'].items():
 req=load(cid+'.request.json');raw=load(cid+'.response.json');assert req==request('R',q['actor'],question=q['question']);obj,u=normalize(raw,len(canonical(req).encode())+1024,'reader');assert u['generation_id'] not in ids;ids.add(u['generation_id']);assert obj['answer']=={'q01':'RELEASE','q02':'HOLD','q03':'INSUFFICIENT'}[cid]
for a in p['assignments']:
 cid=a['id'];req=load(cid+'.request.json');raw=load(cid+'.response.json');prev=parents.get(a['parent']);assert req==request(a['arm'],p['actors'][a['case_id']],prev,p['questions'][a['case_id']] if a['role']=='reader' else None);obj,u=normalize(raw,len(canonical(req).encode())+1024,a['role']);assert u['generation_id'] not in ids;ids.add(u['generation_id']);parents[cid]=obj
 if a['role']=='reader':
  gold={'Cedar':'RELEASE','Bay':'HOLD','Delta':'INSUFFICIENT'}[a['case_id']];correct[a['arm']]+=obj['answer']==gold
  key=(a['hop'],a['case_id']);parent_hash=sha(load(a['parent']+'.response.json'));assert seen.get(key,parent_hash)==parent_hash;seen[key]=parent_hash
assert len(ids)==77 and len(parents)==74 and len(seen)==12 and correct=={'P':12,'R':12}
print(json.dumps({'physical_requests_replayed':77,'writers':50,'paired_checkpoints_questions':12,'correct':correct,'new_model_calls':0}))
