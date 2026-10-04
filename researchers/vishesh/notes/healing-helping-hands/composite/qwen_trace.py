"""Same pinned Qwen prompt/options, with full wire/response provenance."""
import json,urllib.request
from providers import Qwen as Base
class Qwen(Base):
 def predict(self,obs,index,timeout):
  outcomes=('IMPROVED','NOT_IMPROVED','NOT_MEASURED');choices=list(outcomes[index%3:]+outcomes[:index%3])
  prompt=('Extract the result reported in the text. Choose IMPROVED for better or increased accuracy. Choose NOT_IMPROVED for worse, decreased accuracy, or no improvement. Choose NOT_MEASURED when accuracy was not tested or no results were given. Example: did not improve accuracy -> NOT_IMPROVED. Example: measured runtime only -> NOT_MEASURED.\nREPORT: '+obs['report']+'\nReturn JSON with label.')
  payload={'model':'qwen3:0.6b','messages':[{'role':'user','content':prompt}],'think':False,'stream':False,'format':{'type':'object','properties':{'label':{'type':'string','enum':choices}},'required':['label'],'additionalProperties':False},'options':{'temperature':0,'seed':8000+index,'num_ctx':2048,'num_predict':32},'keep_alive':'30m'}
  with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:11434/api/chat',json.dumps(payload).encode(),{'Content-Type':'application/json'}),timeout=timeout) as r:data=json.load(r)
  outcome=json.loads(data['message']['content'])['label']
  label={'IMPROVED':'SUPPORT','NOT_IMPROVED':'REFUTE','NOT_MEASURED':'UNCERTAIN'}[outcome]
  return {'label':label,'reported_outcome':outcome,'input_tokens':data.get('prompt_eval_count',0),'output_tokens':data.get('eval_count',0),'raw':data,'request_payload':payload}
