"""Bounded local model adapters. Diagnostics never include raw provider errors."""
import json,math,multiprocessing as mp,time,urllib.request
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
QWEN_DIGEST='7df6b6e09427a769808717c0a93cadc4ae99ed4eb8bf5ca557c90846becea435'
LAYA_REV='55cf4c4ebb4ebe31b2550e8bdf3bd21b99753851'
RULE='Classify the report relative to the claim. SUPPORT means the report says the claim is true. REFUTE means the report says the opposite or says there was no improvement. UNCERTAIN means the report gives no answer about the claim. Use only the report.'
class Budget:
 def __init__(self,deadline,limits=None):self.deadline=deadline;self.limits=limits or {'qwen':2000,'laya':300};self.attempts={'qwen':0,'laya':0}
 def reserve(self,model):
  if time.monotonic()>=self.deadline:raise TimeoutError('wall_budget')
  if self.attempts[model]>=self.limits[model]:raise RuntimeError('call_budget')
  self.attempts[model]+=1
  return min(30,max(.01,self.deadline-time.monotonic()))
def validate_label(label):
 if label not in LABELS:raise ValueError('invalid_label')
 return label
class Qwen:
 def __init__(self):
  with urllib.request.urlopen('http://127.0.0.1:11434/api/tags',timeout=10) as r:models=json.load(r)['models']
  self.metadata=next(m for m in models if m['name']=='qwen3:0.6b')
  if self.metadata['digest']!=QWEN_DIGEST:raise ValueError('model_digest_mismatch')
 def predict(self,obs,index,timeout):
  choices=list(LABELS[index%3:]+LABELS[:index%3])
  prompt=RULE+'\nCLAIM: '+obs['claim']+'\nREPORT: '+obs['report']+'\nReturn JSON with the label.'
  payload={'model':'qwen3:0.6b','messages':[{'role':'user','content':prompt}],'think':False,'stream':False,'format':{'type':'object','properties':{'label':{'type':'string','enum':choices}},'required':['label'],'additionalProperties':False},'options':{'temperature':0,'seed':8000+index,'num_ctx':2048,'num_predict':32},'keep_alive':'30m'}
  with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/chat',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=timeout) as r:data=json.load(r)
  label=validate_label(json.loads(data['message']['content'])['label'])
  return {'label':label,'input_tokens':data.get('prompt_eval_count',0),'output_tokens':data.get('eval_count',0)}
def validate_laya(a,choices):
 p=a['probabilities'];label=validate_label(a['choice'])
 if set(p)!=set(choices) or any(not isinstance(v,(float,int)) or not math.isfinite(v) or not 0<=v<=1 for v in p.values()) or abs(sum(p.values())-1)>.001 or p[label]<max(p.values())-1e-5:raise ValueError('invalid_probabilities')
 return label,p
def laya_worker(pipe):
 try:
  import torch,importlib.metadata,subprocess
  import laya
  from pathlib import Path
  source=Path(laya.__file__).resolve().parent.parent
  revision=subprocess.check_output(['git','-C',str(source),'rev-parse','HEAD'],text=True).strip()
  if revision!='2e4d9c87e8b1621deb344eac7de5c7258f32f849':raise ValueError('laya_source_mismatch')
  torch.set_num_threads(2);torch.manual_seed(8000)
  model=laya.load('convaiinnovations/laya',revision=LAYA_REV,device='cpu',backend='eager')
  pipe.send({'ready':True,'source_revision':revision,'weights_revision':LAYA_REV,'versions':{p:importlib.metadata.version(p) for p in ('laya','torch','transformers')}})
  while True:
   req=pipe.recv()
   if req is None:return
   obs,index=req;choices=list(LABELS[index%3:]+LABELS[:index%3]);criteria={k:{'SUPPORT':'The report supports the claim.','REFUTE':'The report contradicts the claim.','UNCERTAIN':'The report does not answer the claim.'}[k] for k in choices}
   text='CLAIM: '+obs['claim']+'\nREPORT: '+obs['report'];question={'label':{'type':'choice','instructions':RULE,'criteria':criteria}}
   try:
    result=model.predict(text,question,max_len=1024);label,probs=validate_laya(result['answers']['label'],choices)
    pipe.send({'label':label,'probabilities':probs,'input_tokens_estimate':len(model.tok.encode(text))+len(model.tok.encode(json.dumps(question)))})
   except Exception as e:pipe.send({'error_type':type(e).__name__})
 except Exception as e:pipe.send({'error_type':type(e).__name__})
class Laya:
 def __init__(self):
  ctx=mp.get_context('spawn');self.pipe,child=ctx.Pipe();self.process=ctx.Process(target=laya_worker,args=(child,),daemon=True);self.process.start()
  if not self.pipe.poll(90):self.close();raise TimeoutError('laya_load_timeout')
  self.metadata=self.pipe.recv()
  if not self.metadata.get('ready'):self.close();raise RuntimeError('laya_initialization_failed')
 def predict(self,obs,index,timeout):
  self.pipe.send((obs,index))
  if not self.pipe.poll(timeout):self.close();raise TimeoutError('laya_request_timeout')
  result=self.pipe.recv()
  if 'error_type' in result:raise RuntimeError('laya_prediction_failed')
  return result
 def close(self):
  if self.process.is_alive():self.process.terminate()
  self.process.join(timeout=2)
