"""Original authored development evidence; gold never enters actor payloads."""
from copy import deepcopy
import hashlib,json

def digest(x):return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()
RECORDS=[
 {'id':'m01','time':'09:00','text':'R7 covers Cedar and Bay. GO requires both sites within the current latency limit, rollback tested at both, and recorded approval. Otherwise HOLD.'},
 {'id':'m02','time':'09:10','text':'Correction: the latency limit is 120 ms, replacing 80 ms. This changes the limit, not earlier measurements.'},
 {'id':'m03','time':'09:20','text':'Cedar latency was 100 ms over 20 read-only requests. They passed the current limit. No write-path result is reported.'},
 {'id':'m04','time':'09:22','text':'No Bay latency measurement is available.'},
 {'id':'m05','time':'09:25','text':'Two Cedar summary reports reuse the same acquisition as m03; they are not independent tests.'},
 {'id':'m06','time':'09:30','text':'Rollback was tested at Cedar only. Bay rollback has not been tested.'},
 {'id':'m07','time':'09:35','text':'Approval was requested. Its linked receipt is unavailable, so approval is unverified, not granted or denied.'},
 {'id':'m08','time':'09:40','text':'A post-release monitor is proposed; it has not been started. The next handover is at 10:00.'},
]
TARGETS=[
 ('release_scope','m01','R7 covers both Cedar and Bay; no single-site release substituted.'),
 ('decision_rule','m01','GO needs both sites within current latency limit, rollback tested at both, recorded approval; otherwise HOLD.'),
 ('corrected_limit','m02','120 ms supersedes80 ms without changing historical measurements.'),
 ('cedar_result','m03','Cedar100 ms passed the current latency limit.'),
 ('test_scope','m03','20 read-only requests; write-path result not reported.'),
 ('bay_measurement','m04','Bay latency is unavailable, not failed or passed.'),
 ('dependent_reports','m05','Two Cedar summaries share one acquisition; no independent corroboration.'),
 ('cedar_rollback','m06','Rollback tested at Cedar.'),
 ('bay_rollback','m06','Bay rollback not tested.'),
 ('approval_evidence','m07','Approval receipt unavailable; approval remains unverified, not granted or denied.'),
 ('approval_request','m07','Approval requested, not completed by requesting.'),
 ('monitor_plan','m08','Post-release monitor proposed but not started.'),
]
# Evaluator-only machine state, independently checked against source spans.
STATE={'sites':['Cedar','Bay'],'limit_ms':120,'latency_ms':{'Cedar':100,'Bay':None},'rollback_tested':{'Cedar':True,'Bay':False},'approval':'unknown'}
def decide(state):
 return 'GO' if all(state['latency_ms'][s] is not None and state['latency_ms'][s]<=state['limit_ms'] and state['rollback_tested'][s] for s in state['sites']) and state['approval']=='recorded' else 'HOLD'
def actor_packet(records=None):return {'records':deepcopy(RECORDS if records is None else records)}
def copy_handoff(packet):return '\n'.join(f"{r['id']} [{r['time']}] {r['text']}" for r in packet['records'])
def controls():
 base=deepcopy(STATE);rows=[]
 for name,bay,approval in [('base',False,False),('bay_only',True,False),('approval_only',False,True),('all_conditions',True,True)]:
  state=deepcopy(base)
  if bay:state['latency_ms']['Bay']=110;state['rollback_tested']['Bay']=True
  if approval:state['approval']='recorded'
  rows.append({'name':name,'state':state,'expected':'GO' if name=='all_conditions' else 'HOLD','changes':{'bay_evidence':bay,'approval_evidence':approval}})
 return rows
QUALIFICATION=[
 {'id':'q-go','records':[{'id':'q1','time':'10:00','text':'For this control GO requires all three conditions: latency at most120 ms, rollback tested and recorded approval; otherwise HOLD. Latency is100 ms, rollback is tested and approval is recorded.'}],'expected':'GO'},
 {'id':'q-hold','records':[{'id':'q2','time':'10:00','text':'For this control GO requires all three conditions: latency at most120 ms, rollback tested and recorded approval; otherwise HOLD. Latency is100 ms and rollback is tested. Approval was requested but its receipt is unavailable; approval remains unknown.'}],'expected':'HOLD'},
]

def build():
 packet=actor_packet();text=copy_handoff(packet)
 return {'case':packet,'gold':{'targets':[{'id':i,'source_id':s,'required_meaning':m} for i,s,m in TARGETS],'state':STATE,'decision':decide(STATE)},'qualification_actor':[{'id':x['id'],'records':x['records']} for x in QUALIFICATION],'qualification_gold':{x['id']:x['expected'] for x in QUALIFICATION},'packet_sha256':digest(packet),'copy_handoff_bytes':len(text.encode())}

def control_packet(name):
 packet=actor_packet()
 if name in ('bay_only','all_conditions'):
  packet['records'][3]['text']='Bay latency was 110 ms over 20 read-only requests. They passed the current limit. No write-path result is reported.'
  packet['records'][5]['text']='Rollback was tested at Cedar and Bay.'
 if name in ('approval_only','all_conditions'):
  packet['records'][6]['text']='Approval is recorded. Its receipt is available.'
 return packet

def exact_source_baseline(packet):
 """Narrow source-grammar controller; never applied as a free-prose semantic judge."""
 import re
 records=sorted(packet['records'],key=lambda r:r['time']);texts=[r['text'] for r in records]
 scope=next(re.search(r'R7 covers (\w+) and (\w+)\.',t) for t in texts if re.search(r'R7 covers (\w+) and (\w+)\.',t))
 sites=list(scope.groups());limit=None;latency={s:None for s in sites};rollback={s:False for s in sites};approval=False
 for t in texts:
  m=re.search(r'latency limit is (\d+) ms',t)
  if m:limit=int(m[1])
  for s in sites:
   m=re.search(re.escape(s)+r' latency was (\d+) ms',t)
   if m:latency[s]=int(m[1])
   if re.search(r'No '+re.escape(s)+r' latency measurement is available',t):latency[s]=None
  if t.startswith('Rollback was tested at '):
   for s in sites:
    if re.search(r'(?:at |and )'+re.escape(s)+r'(?: only| and |\.)',t):rollback[s]=True
    if re.search(re.escape(s)+r' rollback has not been tested',t):rollback[s]=False
  if t.startswith('Approval is recorded.'):approval=True
  elif t.startswith('Approval was requested.'):approval=False
 assert limit is not None
 return 'GO' if approval and all(latency[s] is not None and latency[s]<=limit and rollback[s] for s in sites) else 'HOLD'
