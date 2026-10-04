"""Explicit recovery of validated prefix; failed physical output is never parsed."""
import hashlib,json
from pathlib import Path
import scale_pilot as sp
BASE=sp.BASE;encode=sp.encode;CONFIGS={'SC-LUNA':sp.CONFIGS['SP-LUNA']}
PARENT=BASE/'reviews/native-SP-LUNA-01'
def parent():
 names=('summary.json','protocol.jsonl','events.jsonl','raw-records.tar.gz');hashes={name:hashlib.sha256((PARENT/name).read_bytes()).hexdigest() for name in names};summary=json.loads((PARENT/'summary.json').read_text());assert (summary['valid'],summary['calls'],summary['failed'],summary['unstarted'])==(67,68,1,128)
 rows=[json.loads(x) for x in (PARENT/'protocol.jsonl').read_text().splitlines()];assert len(rows)==67
 return rows,hashes
class Protocol(sp.Protocol):
 def __init__(self,stage):
  assert stage=='SC-LUNA';rows,hashes=parent();base=sp.Protocol('SP-LUNA')
  for row in rows:
   i=base.next();assert i['wire_sha256']==row['wire_sha256'],'prefix_wire_mismatch'
   r={'route':{'provider':'OpenAI','model':i['wire_body']['model']},'tool_calls':None,'content':[{'type':'text','text':json.dumps(row['answer'])}]};a=base.check(i,r);base.accept(i,a)
  self.__dict__.update(base.__dict__);self.parent_rows=rows;self.parent_hashes=hashes
 def next(self):
  i=super().next()
  if i['role']=='opinion':
   i['wire_body']['verbosity']='low';raw=encode(i['wire_body']);assert len(raw)<=9216;i.update(wire_bytes=len(raw),wire_sha256=hashlib.sha256(raw).hexdigest())
  return i

def build(stage):
 assert stage=='SC-LUNA';rows,hashes=parent();p=sp.manifest('SP-LUNA');p.update(stage=stage,launch_enabled=True,expected_budget={'cap':8,'reserved':7.7769408,'calls':401},requests=[],maximum_transport_attempts=129,maximum_total_reservation_usd=.1847552,parent_attempt='native-SP-LUNA-01',parent_files_sha256=hashes,reused_valid_outputs=67,tldr='Explicit fifty-agent recovery: retain67validated prefix responses; one failed slot retried with low verbosity, then128unstarted assignments. No failed-output salvage or hidden retry. Report original failure and changed formatting setting; combined paired results are exploratory.')
 return p

def assessment(protocol):
 a=sp.assessment(protocol);a.update(stage='SC-LUNA',parent_attempt='native-SP-LUNA-01',reused_valid_outputs=67,new_valid_outputs=protocol.position-67,combined_logical_valid=protocol.position,interpretation='Recovery with changed adviser verbosity; original failed attempt retained. Paired effects cannot be attributed solely to advocacy.')
 return a
class DynamicRelay(sp.DynamicRelay):
 def __init__(self,stage,journal):
  self.protocol=Protocol(stage);self.journal=Path(journal);self.journal.mkdir(mode=0o700);self.count=0;self.stopped=False
if __name__=='__main__':(BASE/'reviews/SC-LUNA-packet.json').write_text(json.dumps(build('SC-LUNA'),indent=2)+'\n')
