"""Offline-only prepared factorial study. No native transport or allocation."""
import copy,hashlib,json,sys
from pathlib import Path
import freshness as f
import qualification as q
import grounding
BASE=Path(__file__).resolve().parent
CONDITIONS=('plain_solo','plain_advice','grounded_solo','grounded_advice')
def assignments():
 return [{'case':case,'condition':CONDITIONS[(j+i)%4],'seed':9401}
         for i,case in enumerate(q.CASES) for j in range(4)]
def request(fixture,state,tick,history,advice,condition):
 if condition not in CONDITIONS:raise ValueError('unknown_condition')
 o=f.observe(fixture,state,tick,history,advice if condition.endswith('_advice') else [],True)
 o['ticks_remaining']=3-tick
 if condition.startswith('grounded_'):o['evidence_table']=grounding.evidence(o)
 return f.controller_request(fixture,o)
def execute(out):
 out=Path(out);out.mkdir(parents=True,exist_ok=False)
 packet=json.loads((BASE/'grounding-advice.json').read_text());rows=[]
 for assignment in assignments():
  case=assignment['case'];condition=assignment['condition'];fixture,state=f.fixture(case,9401);initial=copy.deepcopy(state);trace=[];history=[]
  for tick in (1,2):
   req=request(fixture,state,tick,history,packet['advice'][case],condition)
   # Same visible reference used in A8, not a model and not an efficacy estimate.
   raw=f.controller.encode(fixture,f.reference(req['observation']));action=f.controller.decode(fixture,raw)
   transition=f.step(fixture,state,action);transition.update(tick=tick,observation=req['observation'],raw_response=raw,controller_contract=f.controller.VERSION)
   trace.append(transition);history.append({'action':action,'result':transition['result']})
  row={**assignment,'arm':condition,'initial':initial,'initial_healthy':int(all(f.health(fixture,initial).values())),'trace':trace};row['capability_pass']=q.gate(row);rows.append(row)
 (out/'episodes.jsonl').write_text(''.join(json.dumps(x)+'\n' for x in rows))
 result={'backend':'scripted','assigned':12,'completed':len(rows),'capability_passes':sum(x['capability_pass'] for x in rows),'model_calls':0,'native_admitted':False,'advice_sha256':hashlib.sha256((BASE/'grounding-advice.json').read_bytes()).hexdigest(),'contract':f.controller.VERSION,'grounding':grounding.VERSION}
 (out/'summary.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':print(json.dumps(execute(sys.argv[1]),indent=2))
