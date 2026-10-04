import json,re,gzip,datetime,hashlib,collections,os
from pathlib import Path
os.umask(0o077)
import sys
base=Path(sys.argv[1])
def dt(s):return datetime.datetime.fromisoformat(s.replace('Z','+00:00')).replace(tzinfo=None)
goals=[json.loads(x) for x in gzip.open(sys.argv[2],'rt')];goals.sort(key=lambda x:x['start_time'])
events={}
for line in (base/'events.jsonl').open():
 r=json.loads(line);data=r.get('data') or {}
 if data.get('messageId'):events.setdefault(data['messageId'],[]).append(r)
bygoal=collections.defaultdict(list);rejected=collections.Counter()
for line in (base/'chat_messages.jsonl').open():
 r=json.loads(line);text=r.get('content') or ''
 if r.get('speaker_type')!='agent':rejected['human']+=1;continue
 if not isinstance(text,str) or not 180<=len(text)<=1100:rejected['length']+=1;continue
 if re.search(r'(secret|password|api.key|token|bearer|sk-|ssh-|PRIVATE KEY|[A-Za-z0-9_+/=-]{38,}|\b\d{1,3}(?:\.\d{1,3}){3}\b|[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}|https?://|\[REDACTED\])',text,re.I):rejected['privacy_or_external_reference']+=1;continue
 if len(events.get(r['id'],[]))!=1:rejected['event_link_ambiguous']+=1;continue
 if not re.search(r'\b(not|pending|failed|only|haven.t|couldn.t|unverified|uncertain|corrected|actually|however)\b',text,re.I):rejected['no_qualification_marker']+=1;continue
 ts=dt(r['created_at']);gs=[i for i,g in enumerate(goals) if dt(g['start_time'])<=ts and (not g.get('end_time') or ts<dt(g['end_time']))]
 if len(gs)!=1:rejected['goal_boundary']+=1;continue
 bygoal[gs[0]].append(r)
selected=[]
# Earliest eligible message in eight temporally distributed goals; no outcome-based selection.
keys=sorted(bygoal)
for i in range(8):
 k=keys[round(i*(len(keys)-1)/7)];r=sorted(bygoal[k],key=lambda r:(r['created_at'],r['id']))[0]
 selected.append({'candidate':f'V{i:02d}','goal_block':k,'record':r,'event':events[r['id']][0],'status':'development_candidate_not_gold'})
(base/'selected-candidates.json').write_text(json.dumps(selected,indent=2)+'\n')
print(json.dumps({'candidate_goal_blocks':len(keys),'selected':len(selected),'exclusions':dict(rejected),'native_cases':0}))
