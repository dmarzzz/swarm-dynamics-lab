"""Offline allocation/precision calculation, not native execution or simulation."""
from decimal import Decimal
from pathlib import Path
import json,math

def schedule():
 rows=[]
 for stage,n in [('Q-B32',8),('E-B32-R1',32),('E-B32-R2',32)]:
  for root in range(n):
   event=('qualification' if stage=='Q-B32' else 'evaluation')+f'-{root:02}'
   for seat in range(7):
    group='single' if seat==0 else 'committee'
    first=f'{stage}/{event}/{group}/{seat}/initial'
    rows.append(dict(id=first,parent=None,stage=stage,event=event,group=group,seat=seat,arm='initial'))
    for arm in (['private'] if group=='single' else ['private','peer']):
     rows.append(dict(id=f'{stage}/{event}/{group}/{seat}/{arm}',parent=first,stage=stage,event=event,group=group,seat=seat,arm=arm))
 return rows

def check():
 rows=schedule();ids={r['id'] for r in rows};assert len(rows)==len(ids)==1440
 for r in rows:
  if r['parent']:assert r['parent'] in ids and r['parent'].startswith(r['stage']+'/')
 for stage,n in [('Q-B32',160),('E-B32-R1',640),('E-B32-R2',640)]:assert sum(r['stage']==stage for r in rows)==n
 eval_events={r['event'] for r in rows if r['stage'].startswith('E-')};assert len(eval_events)==32
 qual_events={r['event'] for r in rows if r['stage']=='Q-B32'};assert not qual_events&eval_events
 for stage in ('E-B32-R1','E-B32-R2'):
  for event in eval_events:
   peers={r['parent'] for r in rows if r['stage']==stage and r['event']==event and r['arm']=='peer'}
   privates={r['parent'] for r in rows if r['stage']==stage and r['event']==event and r['group']=='committee' and r['arm']=='private'}
   assert len(peers)==6 and peers==privates
 unit=Decimal(4000)*Decimal('0.000002')+Decimal(2048)*Decimal('0.00001')
 return dict(status='offline_design_arithmetic_only',native_calls=0,qualification_clusters=8,evaluation_clusters=32,evaluation_fresh_executions=2,agents_per_committee=6,calls_per_cluster_execution=20,qualification_call_max=160,evaluation_call_max_each=640,total_call_max=1440,unit_ceiling_usd=str(unit),qualification_ceiling_usd=str(unit*160),each_evaluation_ceiling_usd=str(unit*640),model_ceiling_usd=str(unit*1440),infrastructure_ceiling_usd='0.50',incremental_total_ceiling_usd=str(unit*1440+Decimal('0.50')),precision_sensitivity=[dict(discordance=q,n=32,approx_95_half_width=1.96*math.sqrt(q/32)) for q in (.1,.25,.5)],limitations=['Event IDs are placeholders, not an assembled or admitted corpus.','Repeated execution does not double independent n.','Normal approximation omits repeat covariance; actual clustered intervals required.','This validates allocation relationships, not a native fork runner.'])
if __name__=='__main__':
 report=check();Path(__file__).with_name('design-check.json').write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report))
