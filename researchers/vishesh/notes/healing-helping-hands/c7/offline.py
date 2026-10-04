"""Offline C7 development constructor and separate visible-text rule baseline. No API."""
import hashlib,json,random,re
from pathlib import Path
STRATA=('task_distraction','metric_distraction','superseded','conflict','duplicates','missingness')
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
RULE='Decide whether the target method improves accuracy over baseline for the named task and session. Use active target-task, target-session accuracy records only. Withdrawn records are invalid. Duplicates add no evidence. Positive delta means SUPPORT; zero or negative means REFUTE. No target measurement or unresolved positive and nonpositive measurements means UNCERTAIN.'
def construct(seed,stratum,label):
 rng=random.Random(seed);task='T'+hashlib.sha256(str(seed).encode()).hexdigest()[:10];rows=[];delta=rng.randint(1,19)*(1 if label=='SUPPORT' else -1);session='S1'
 def add(t=task,m='accuracy',s=session,d=delta,status='active',source=None):rows.append(dict(task=t,session=s,metric=m,delta=d,status=status,source=source or f'R{len(rows)+1}'))
 if label!='UNCERTAIN':add()
 elif stratum=='conflict':add(d=7);add(d=-3)
 if stratum=='task_distraction':add(t='OTHER',d=-delta)
 elif stratum=='metric_distraction':add(m='latency',d=-delta)
 elif stratum=='superseded':add(d=-delta,status='withdrawn')
 elif stratum=='conflict' and label!='UNCERTAIN':add(d=2 if label=='SUPPORT' else -2)
 elif stratum=='duplicates':
  if rows:rows.append(dict(rows[0]))
  else:add(t='OTHER');rows.append(dict(rows[0]))
 elif stratum=='missingness':add(s='S2',d=-delta)
 # Always include additional irrelevant scope so completeness cannot be inferred from row count.
 add(t='OTHER',m='latency',d=rng.randint(-20,20));rng.shuffle(rows)
 relevant={1 if x['delta']>0 else 0 for x in rows if x['task']==task and x['session']==session and x['metric']=='accuracy' and x['status']=='active'}
 gold='SUPPORT' if relevant=={1} else 'REFUTE' if relevant=={0} else 'UNCERTAIN'
 assert gold==label
 return dict(id=hashlib.sha256(f'{seed}-{stratum}'.encode()).hexdigest()[:16],stratum=stratum,target=task,session=session,records=rows,expected=gold)
def visible(r):
 return RULE+f'\nTarget task={r["target"]}; session={r["session"]}.\n'+ '\n'.join(f'Source {x["source"]}: task={x["task"]}; session={x["session"]}; metric={x["metric"]}; delta={x["delta"]}; status={x["status"]}.' for x in r['records'])
def baseline(text):
 task,session=re.search(r'Target task=(\w+); session=(\w+)\.',text).groups();vals=[]
 for t,s,m,d,status in re.findall(r'Source \w+: task=(\w+); session=(\w+); metric=(\w+); delta=(-?\d+); status=(\w+)\.',text):
  if t==task and s==session and m=='accuracy' and status=='active':vals.append(int(d))
 if not vals:return 'UNCERTAIN'
 if min(vals)>0:return 'SUPPORT'
 if max(vals)<=0:return 'REFUTE'
 return 'UNCERTAIN'
def check():
 roots=[construct(f'development-{f}-{l}',f,l) for f in STRATA for l in LABELS];n=0
 for r in roots:
  assert baseline(visible(r))==r['expected'];n+=1
  for changed in ({**r,'records':list(reversed(r['records']))},{**r,'records':r['records']*2},{**r,'expected':'INVALID','id':'GOLD-MUTATION'}):
   assert baseline(visible(changed))==r['expected'];n+=1
  changed=json.loads(json.dumps(r));old=changed['target'];changed['target']='RENAMED'
  for row in changed['records']:
   if row['task']==old:row['task']='RENAMED'
  assert baseline(visible(changed))==r['expected'];n+=1
  if r['expected']!='UNCERTAIN':
   changed=json.loads(json.dumps(r))
   for row in changed['records']:
    if row['task']==r['target'] and row['session']==r['session'] and row['metric']=='accuracy' and row['status']=='active':row['delta']=-row['delta']
   assert baseline(visible(changed))==('REFUTE' if r['expected']=='SUPPORT' else 'SUPPORT');n+=1
 assert len(set(visible(r) for r in roots))==18
 output={'scope':'inspected synthetic structured-text development; not natural documents or evaluation holdout','native_calls':0,'roots':18,'checks_passed':n,'same_author':True,'cases':[{'id':r['id'],'stratum':r['stratum'],'expected':r['expected'],'actor_input':visible(r)} for r in roots]}
 Path(__file__).with_name('OFFLINE.json').write_text(json.dumps(output,indent=2)+'\n');print(json.dumps({k:v for k,v in output.items() if k!='cases'}))
if __name__=='__main__':check()
