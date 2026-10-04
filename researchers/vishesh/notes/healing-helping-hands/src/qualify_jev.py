import argparse,json,time
from pathlib import Path
from jev import Jev,fixtures,LABELS
from run import check,source_check,write,Journal
from providers import Budget

def execute(out,tldr):
 receipt=check('healing-helping-hands',tldr);hashes=source_check(receipt['commit']);out.mkdir(parents=True,exist_ok=False);write(out/'plan-receipt.json',receipt);b=Budget(time.monotonic()+600,{'jev':60});b.attempts={'jev':0};j=Journal(out/'calls.jsonl',b);cases=fixtures();records=[];started=time.monotonic();backend=Jev();write(out/'fixtures.json',cases)
 try:
  for i,c in enumerate(cases):
   label=j.call(backend,'jev',{k:c[k] for k in ('claim','report')},i,{'stage':'qualification','case':i});records.append({'case':i,'expected':c['expected'],'label':label,'status':'completed'});write(out/'progress.json',{'completed':len(records),'total':60})
 except Exception as e:
  i=len(records);records.append({'case':i,'expected':cases[i]['expected'],'status':'failed','error_type':type(e).__name__});records.extend({'case':k,'expected':cases[k]['expected'],'status':'not_run','reason':'preceding_call_failed'} for k in range(i+1,60))
 per={k:sum(r.get('label')==k for r in records if r['expected']==k)/20 for k in LABELS};accuracy=sum(r.get('label')==r['expected'] for r in records)/60;status='passed' if accuracy>=.85 and min(per.values())>=.7 and all(r['status']=='completed' for r in records) else 'failed'
 result={'status':status,'accuracy':accuracy,'per_label':per,'records':records};write(out/'qualification.json',result);write(out/'manifest.json',{'attempt':'jev-qualification-01','parent_attempt':'diagnostic-03','plan':receipt,'source_hashes':hashes,'metadata':backend.metadata,'host':'sim-vishesh','claim':'vishesh-healing-helping-hands','calls':b.attempts,'seconds':time.monotonic()-started,'qualification':result});print(json.dumps({k:v for k,v in result.items() if k!='records'}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',type=Path,required=True);p.add_argument('--run-tldr',required=True);a=p.parse_args()
 try:execute(a.out,a.run_tldr)
 except Exception as e:print('Qualification launch failed: '+type(e).__name__);raise SystemExit(1)
