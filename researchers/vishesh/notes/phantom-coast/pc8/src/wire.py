import json,hashlib,math
from contract import LABELS
MODEL='typesafe/jev-1.13';SNAPSHOT='typesafe/jev-1.13-20260917';RATE_NANO=42
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),allow_nan=False)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def reservation(req):return len(req['questions'])*32000*RATE_NANO
def request(packet,kind=None):
 return dict(model=MODEL,provider={'only':['typesafe'],'allow_fallbacks':False},state=packet,questions={r['id']:dict(type='choice',instructions=f"Classify record {r['id']} using the policy and complete history in state. Return its eligibility and calibrated outcome, not your confidence.",criteria={'MATCH':'Retain as independent current verified calibration: reference agrees with source.','MISMATCH':'Retain as independent current verified calibration: reference disagrees with source.','EXCLUDE':'Do not retain: copy, stale, superseded or unverified.','UNKNOWN':'Interpretation cannot be resolved from the provided history.'}) for r in packet['records']})
def number(x,lo,hi):return type(x) in (int,float) and math.isfinite(x) and lo<=x<=hi
def validate(raw,req):
 if not isinstance(raw,dict) or raw.get('model')!=SNAPSHOT or raw.get('provider')!='TypeSafe':raise ValueError('route_mismatch')
 answers=raw.get('answers')
 if not isinstance(answers,dict) or set(answers)!=set(req['questions']):raise ValueError('answer_set')
 safe={}
 for key,a in answers.items():
  if not isinstance(a,dict) or a.get('type')!='choice' or a.get('choice') not in LABELS:raise ValueError('choice')
  p=a.get('probabilities')
  if not isinstance(p,dict) or set(p)!=set(LABELS) or not all(number(v,0,1) for v in p.values()):raise ValueError('probabilities')
  tol=.020000001 if all(abs(v*100-round(v*100))<1e-8 for v in p.values()) else .001
  if abs(sum(p.values())-1)>tol:raise ValueError('probability_mass')
  if p[a['choice']]<max(p.values())-1e-8:raise ValueError('selected_maximum')
  if not number(a.get('confidence'),0,1):raise ValueError('confidence')
  safe[key]={k:a[k] for k in ('type','choice','probabilities','confidence')}
 u=raw.get('usage')
 if not isinstance(u,dict) or not number(u.get('cost'),0,reservation(req)/1e9):raise ValueError('cost')
 if type(u.get('input_tokens')) is not int or not 0<u['input_tokens']<=len(answers)*32000 or type(u.get('output_tokens')) is not int or u['output_tokens']<0:raise ValueError('usage')
 return dict(result={'labels':{k:a['choice'] for k,a in safe.items()}},safe_raw_answers=safe,usage={k:u[k] for k in ('cost','input_tokens','output_tokens')},request_sha256=digest(req),response_sha256=digest(raw),model=SNAPSHOT,provider='TypeSafe')
CODES=frozenset(('route_mismatch','answer_set','choice','probabilities','probability_mass','selected_maximum','confidence','cost','usage'))
def failure_code(exc):return str(exc) if type(exc) is ValueError and str(exc) in CODES else type(exc).__name__ if type(exc).__name__ in ('TimeoutError','URLError','HTTPError','ValueError') else 'transport_or_validation_failure'
