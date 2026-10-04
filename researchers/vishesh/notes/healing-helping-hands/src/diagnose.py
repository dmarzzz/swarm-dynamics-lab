"""Bounded development diagnostics; never executes swarm worlds."""
import argparse,json,time,urllib.request
from pathlib import Path
from corpus import qualification,LABELS
from providers import Qwen,Laya,Budget,RULE,validate_label
from run import Journal,write,check,source_check
class DiagnosticQwen(Qwen):
 def __init__(self,variant):super().__init__();self.variant=variant
 def predict(self,obs,index,timeout):
  if self.variant=='neutral':
   codes=('A','B','C');mapping=dict(zip(codes,LABELS));choices=list(codes[index%3:]+codes[:index%3])
   prompt='Read the report. A: the measured accuracy improved. B: accuracy got worse or did not improve. C: accuracy was not measured or no result is reported. First explain the reported outcome in one sentence in the explanation field, then select A, B or C in the label field. Do not infer an improvement just because the intervention is mentioned.\n'
   schema={'type':'object','properties':{'explanation':{'type':'string'},'label':{'type':'string','enum':choices}},'required':['explanation','label'],'additionalProperties':False}
  else:
   mapping=dict(zip(LABELS,LABELS));choices=list(LABELS[index%3:]+LABELS[:index%3]);prompt=RULE+' Think carefully about negation and absent measurements. Return JSON with label.\n';schema={'type':'object','properties':{'label':{'type':'string','enum':choices}},'required':['label'],'additionalProperties':False}
  prompt+='CLAIM: '+obs['claim']+'\nREPORT: '+obs['report']
  payload={'model':'qwen3:0.6b','messages':[{'role':'user','content':prompt}],'think':self.variant=='thinking','stream':False,'format':schema,'options':{'temperature':0,'seed':9000+index,'num_ctx':2048,'num_predict':512,'num_thread':4},'keep_alive':'30m'}
  with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/chat',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=timeout) as r:data=json.load(r)
  result=json.loads(data['message']['content']);label=validate_label(mapping[result['label']])
  return {'label':label,'input_tokens':data.get('prompt_eval_count',0),'output_tokens':data.get('eval_count',0),'done_reason':data.get('done_reason')}
class DiagnosticBudget(Budget):
 def reserve(self,model):
  super().reserve(model)
  return min(90,max(.01,self.deadline-time.monotonic()))
def fixtures():
 all_cases=qualification();return [x for k in LABELS for x in [q for q in all_cases if q['expected']==k][:6]]
def execute(out,tldr):
 receipt=check('healing-helping-hands',tldr);hashes=source_check(receipt['commit']);out.mkdir(parents=True,exist_ok=False)
 write(out/'plan-receipt.json',receipt);budget=DiagnosticBudget(time.monotonic()+1200,{'qwen':36,'laya':18});j=Journal(out/'calls.jsonl',budget);cases=fixtures();results={}
 write(out/'fixtures.json',cases);started=time.monotonic()
 for variant in ('neutral','thinking','laya-explicit'):
  records=[];backend=None;name='laya' if variant=='laya-explicit' else 'qwen'
  try:
   backend=Laya(diagnostic=True) if name=='laya' else DiagnosticQwen(variant)
   for i,c in enumerate(cases):
    label=j.call(backend,name,{k:c[k] for k in ('claim','report')},i,{'stage':'diagnostic','variant':variant,'case':i});records.append({'case':i,'expected':c['expected'],'label':label,'status':'completed'});write(out/'progress.json',{'variant':variant,'records':records})
  except Exception as e:records.extend({'case':i,'expected':cases[i]['expected'],'status':'not_run','reason':type(e).__name__} for i in range(len(records),18))
  finally:
   if name=='laya' and backend:backend.close()
  per={k:sum(x.get('label')==k for x in records if x['expected']==k) for k in LABELS};score=sum(per.values());results[variant]={'records':records,'correct':score,'per_label_correct':per,'eligible':score>=16 and min(per.values())>=5 and all(x['status']=='completed' for x in records)}
  write(out/'summary.json',results);print(json.dumps({'variant':variant,'correct':score,'per_label':per,'eligible':results[variant]['eligible']}),flush=True)
 write(out/'manifest.json',{'attempt':'diagnostic-03','parent_attempt':'pilot-02','plan':receipt,'source_hashes':hashes,'calls':budget.attempts,'seconds':time.monotonic()-started,'results':results,'host':'sim-vishesh','claim':'vishesh-healing-helping-hands'})
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--run-tldr',required=True);a=p.parse_args();execute(Path(a.out),a.run_tldr)
