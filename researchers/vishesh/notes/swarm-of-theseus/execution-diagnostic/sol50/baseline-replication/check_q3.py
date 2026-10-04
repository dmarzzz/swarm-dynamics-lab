from pathlib import Path
import json,sys,tempfile,os,io,collections
from unittest.mock import patch
base=Path(__file__).resolve().parent;sys.path.insert(0,str(base))
import engine,contract,admission,q3_runner as runner,test_q3
p=test_q3.packet();r,g=test_q3.evidence(p);phases=collections.Counter();wires=[]
class Reporter:
 def report(self,*a,**kw):return True
with tempfile.TemporaryDirectory() as tmp,patch.dict(os.environ,{'THESEUS_R3_CAPABILITY':'test-only-not-native'}):
 root=Path(tmp);caller=runner.Calls(root,r,g,root/'ledger.sqlite',Reporter())
 def respond(req,timeout):
  payload=json.loads(req.data);value=test_q3.oracle(payload['family'],payload['phase'],payload['packet'],'fixture');phases[payload['phase']]+=1;wires.append(len(json.dumps(payload['request'],separators=(',',':')).encode()))
  return io.BytesIO(json.dumps({'error':None,'actual_usd':.001,'response':{'model':'openai/gpt-6-sol','provider':'OpenAI','choices':[{'finish_reason':'stop','message':{'content':json.dumps(value)}}]}}).encode())
 with patch('urllib.request.urlopen',side_effect=respond):result=engine.qualify(p,caller)
 assert result['passed'];assert caller.count<=105;assert caller.ledger.db.execute('select count(*) from r3_calls').fetchone()[0]==caller.count
 paths=sorted(root.glob('*-request.json'));index=0
 def replay(family,phase,packet,condition):
  global index
  saved=json.loads(paths[index].read_text());assert saved['request']==contract.wire(phase,family,packet) and saved['family']==family and saved['phase']==phase;answer=json.loads(paths[index].with_name(paths[index].name.replace('-request','-response')).read_text());index+=1;return runner.parse(answer)
 assert engine.qualify(p,replay)==result and index==caller.count
 out={'evidence_type':'scripted full worker-caller custody/replay fixture; no provider calls','scripted_calls':caller.count,'families_passed':3,'phases':dict(phases),'maximum_request_bytes':max(wires),'exact_replayed_requests':index,'replay_disagreements':0,'native_calls':0};caller.ledger.db.close()
(base/'Q3-OFFLINE.json').write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
