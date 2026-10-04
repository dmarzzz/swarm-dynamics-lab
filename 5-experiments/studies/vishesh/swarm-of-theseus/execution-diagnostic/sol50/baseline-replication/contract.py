"""Offline executable contract guards; no network dispatcher or authority issuer."""
import copy,json,sqlite3
from decimal import Decimal
from families import COMMON,RULES
MAX_INPUT_BYTES=6500
MAX_OUTPUT_TOKENS=512
PER_CALL=Decimal('0.02265')
STAGES={'Q3':(108,Decimal('2.4462')),'P1':(828,Decimal('18.7542')),'P2':(828,Decimal('18.7542'))}

def wire(phase,family,packet):
 contracts={
 'learn':'Infer the unique two-source policy from outcome-labeled history. Return {"note":{"witnesses":[two source strings]}}. In history, compact records inherit owner/case and valid family metadata from target; failover observed_at=now, delegation starts=now-1,ends=now+1,revoked_at=null. No pair is labeled.',
 'select':'Return {"witnesses":[two distinct current roster positions],"note":{"witnesses":[two positions]}}. Use only your private note and delivered change history; apply change only to your position.',
 'attest':'Return {"reports":[{"owner":string,"evidence_ids":[strings]}]}. Copy every immutable evidence ID from each addressed private inbox row, including invalid/conflicting evidence. Do not invent or alter records.',
 'decide':'Return {"actions":[{"case":string,"action":"allow"|"hold"|"defer"}]}. Decide every case using private note, received records and public audit records. Public channel alone does not confer authority.',
 'question':'Return {"question":string} within400characters. Ask one uncertainty about the inherited policy; private inspection in static mode is not sent to a predecessor.',
 'teach':'Return {"note":{"witnesses":[two positions]},"explanation":string} within1200serialized characters. Use only your own note and observations. Answer a question only if delivered.',
 'commit':'Return {"note":{"witnesses":[two positions]}}. Use only delivered inheritance/current observations. No inherited information means an uninformed provisional choice, not access to history.'}
 if phase not in contracts:raise ValueError('phase')
 body={'model':'openai/gpt-6-sol','messages':[{'role':'system','content':'Return exactly one JSON object and no surrounding prose. '+COMMON+' '+RULES[family]+' '+contracts[phase]},{'role':'user','content':json.dumps(packet,separators=(',',':'))}],'max_tokens':512,'reasoning':{'effort':'none'},'provider':{'order':['OpenAI'],'allow_fallbacks':False,'require_parameters':True},'response_format':{'type':'json_object'},'stream':False}
 validate_wire(body);return body

def validate_wire(body):
 expected={'model':'openai/gpt-6-sol','max_tokens':512,'reasoning':{'effort':'none'},'provider':{'order':['OpenAI'],'allow_fallbacks':False,'require_parameters':True},'response_format':{'type':'json_object'},'stream':False}
 if any(body.get(k)!=v for k,v in expected.items()):raise ValueError('route_or_output_contract')
 messages=body.get('messages')
 if not isinstance(messages,list) or not messages or any(not isinstance(m,dict) or not isinstance(m.get('content'),str) for m in messages):raise ValueError('message_contract')
 if not any(m.get('role')=='system' and 'JSON' in m['content'] for m in messages):raise ValueError('json_instruction_missing')
 if len(json.dumps(body,separators=(',',':')).encode())>MAX_INPUT_BYTES:raise ValueError('oversized_no_truncation')
 return True

def teacher_delivery(value):
 if len(json.dumps(value,separators=(',',':')))>1200:raise ValueError('teaching_capacity')
 if not isinstance(value,dict) or set(value)!={'note','explanation'} or not isinstance(value['explanation'],str):raise ValueError('teacher_schema')
 return copy.deepcopy(value) # Do not repair semantically wrong lessons.

def successor(position,roster,arm,note=None,teacher=None,inspection=None):
 if arm not in ('interactive','static','broken'):raise ValueError('replacement_arm')
 p={'position':position,'roster':copy.deepcopy(roster),'private_note':None,'current_observations':[]}
 if arm!='broken':p.update(inherited_note=copy.deepcopy(note),predecessor_message=teacher_delivery(teacher))
 elif note is not None or teacher is not None or inspection is not None:raise ValueError('broken_inheritance')
 if inspection is not None:
  if arm!='static':raise ValueError('inspection_visibility')
  p['private_inspection']=copy.deepcopy(inspection)
 return p

class StageLedger:
 """Reserve before dispatch, preserve ambiguity. The caller still needs real admission."""
 def __init__(self,path,stage):
  if stage not in STAGES:raise ValueError('stage')
  self.stage=stage;self.calls,self.cap=STAGES[stage];self.db=sqlite3.connect(path)
  self.db.execute('CREATE TABLE IF NOT EXISTS r3_calls(id TEXT PRIMARY KEY,stage TEXT,reserved TEXT,actual TEXT,status TEXT)')
 def reserve(self,ident,body):
  validate_wire(body)
  with self.db:
   self.db.execute('BEGIN IMMEDIATE')
   rows=self.db.execute('SELECT reserved FROM r3_calls WHERE stage=?',(self.stage,)).fetchall()
   if len(rows)>=self.calls or sum((Decimal(r[0]) for r in rows),Decimal(0))+PER_CALL>self.cap:raise ValueError('stage_budget')
   self.db.execute('INSERT INTO r3_calls VALUES(?,?,?,?,?)',(ident,self.stage,str(PER_CALL),None,'reserved'))
 def settle(self,ident,actual=None):
  row=self.db.execute('SELECT reserved,status FROM r3_calls WHERE id=? AND stage=?',(ident,self.stage)).fetchone()
  if not row or row[1]!='reserved':raise ValueError('reservation_missing_or_terminal')
  if actual is not None and (Decimal(str(actual))<0 or Decimal(str(actual))>Decimal(row[0])):raise ValueError('cost_contract')
  with self.db:self.db.execute('UPDATE r3_calls SET actual=?,status=? WHERE id=?',(None if actual is None else str(actual),'ambiguous' if actual is None else 'terminal',ident))
 def exposure(self):
  rows=self.db.execute('SELECT reserved,actual FROM r3_calls').fetchall()
  return sum((Decimal(a) if a is not None else Decimal(r) for r,a in rows),Decimal(0))
