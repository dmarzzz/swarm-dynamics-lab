"""Frozen Jev choice interface; no credentials or inference on import."""
import json,math,random,urllib.request
from providers import LABELS,validate_laya
MODEL='typesafe/jev-1.13'
SNAPSHOT='typesafe/jev-1.13-20260917'
PROVIDER='TypeSafe'
RATE=.000000042
RESERVE=.001344
CRITERIA={'SUPPORT':'The report describes improved, higher or better accuracy with the method.','REFUTE':'The report describes lower, worse or unchanged accuracy, or says the method failed to improve accuracy.','UNCERTAIN':'The report contains no observed accuracy result, does not measure accuracy, or leaves the effect untested.'}
def fixtures():
 templates={
 'SUPPORT':['Accuracy was higher with {m} than without it.','The evaluation recorded an accuracy gain after applying {m}.','The baseline was less accurate than {m} in the reported test.','An accuracy improvement was measured for {m}.','The observed accuracy of {m} exceeded the comparison system.'],
 'REFUTE':['Accuracy was lower with {m} than without it.','The evaluation recorded an accuracy loss after applying {m}.','The baseline was more accurate than {m} in the reported test.','No accuracy improvement was measured for {m}.','The observed accuracy of {m} was unchanged from the comparison system.'],
 'UNCERTAIN':['The evaluation of {m} recorded memory use but omitted accuracy.','There are no accuracy observations available for {m}.','An accuracy comparison for {m} is planned but has not been carried out.','The accuracy section of the {m} report is empty.','The authors have not collected accuracy results for {m}.']}
 out=[]
 for label in LABELS:
  for i in range(20):
   method=f'protocol Z{i+301}';out.append({'claim':f'{method} improves accuracy.','report':templates[label][i%5].format(m=method),'expected':label})
 random.Random(8600).shuffle(out);return out

def request(obs,index,scope=None):
 choices=LABELS[index%3:]+LABELS[:index%3]
 return {**({'session_id':scope+'-'+str(index)} if scope else {}),'model':MODEL,'provider':{'only':['typesafe'],'allow_fallbacks':False},'state':{'claim':obs['claim'],'report':obs['report']},'questions':{'label':{'type':'choice','instructions':'Determine whether the report supports the improvement claim, contradicts it, or provides insufficient evidence. Use only the reported findings; absent measurements are insufficient evidence.','criteria':{k:CRITERIA[k] for k in choices}}}}
def validate(data):
 if data.get('model')!=SNAPSHOT or data.get('provider')!=PROVIDER:raise ValueError('route_or_snapshot_mismatch')
 a=data['answers']['label'];label,p=validate_laya(a,LABELS);u=data['usage'];cost=u['cost'];tokens=u['input_tokens'];confidence=a['confidence']
 if isinstance(cost,bool) or not isinstance(cost,(int,float)) or not math.isfinite(cost) or not 0<=cost<=RESERVE:raise ValueError('invalid_cost')
 if isinstance(tokens,bool) or not isinstance(tokens,int) or not 0<tokens<=32000:raise ValueError('invalid_usage')
 if not isinstance(confidence,(int,float)) or not math.isfinite(confidence) or not 0<=confidence<=1:raise ValueError('invalid_confidence')
 return {'label':label,'probabilities':p,'confidence':confidence,'input_tokens':tokens,'output_tokens':u.get('output_tokens',0),'cost_usd':cost,'served_model':data['model'],'provider':data['provider'],'request_id':data.get('id')}
class Jev:
 metadata={'requested_model':MODEL,'served_model':SNAPSHOT,'provider':PROVIDER,'input_usd_per_token':RATE,'fallbacks':False}
 def __init__(self,scope=None):self.scope=scope
 def predict(self,obs,index,timeout):
  payload=json.dumps(request(obs,index,self.scope),separators=(',',':')).encode()
  with urllib.request.urlopen(urllib.request.Request('http://127.0.0.1:18443/decision',payload,{'Content-Type':'application/json'}),timeout=timeout) as r:data=json.load(r)
  return validate(data)
