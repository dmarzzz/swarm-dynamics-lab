"""Offline public-rule contrast; no hidden route/gold override or native dispatch."""
import copy
import families as f

def evaluate(pair,records,target):
 return f.decide(pair,records,target)

def boundary_fixture():
 target={'owner':'owner','case':'case','family':'failover','now':10,'service':'payments','region':'west','generation':3}
 def record(source,at,value=True):return dict(target,id=source+'-'+str(at),source=source,observed_at=at,value=value)
 rows=[record('peer-a',10),record('peer-b',10),record('decoy',10,False)]
 checks={}
 for label,at in [('current',10),('lower-bound',8),('future',11),('stale',7)]:
  changed=copy.deepcopy(rows);changed[1]['observed_at']=at;checks[label]=evaluate(['peer-a','peer-b'],changed,target)
 checks['missing']=evaluate(['peer-a','peer-b'],rows[:1],target)
 checks['wrong-pair-missing']=evaluate(['peer-a','absent'],rows,target)
 checks['wrong-pair-present']=evaluate(['peer-a','decoy'],rows,target)
 return checks
