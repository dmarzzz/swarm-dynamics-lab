"""One prospective R1 repair. D2 case generator; fresh fixed seeds only."""
import sys,random,json,hashlib,itertools,copy,importlib.util
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('d2design',ROOT/'d2/design.py');d2=importlib.util.module_from_spec(spec);spec.loader.exec_module(d2)
d1=d2.d1;digest=d2.digest;MODEL=d2.MODEL;MAPPINGS=d2.MAPPINGS;world=d2.world
EXPERIMENT='swarm-of-theseus-execution-r1'
def request(c,rule,context,arm):
 body=d1.request([c],rule,context,'E')
 if arm=='F':
  decision=body['output_config']['format']['schema']['properties']['decisions'];decision.update(minItems=1,maxItems=1);decision['items']['properties']['id']['enum']=[c['id']]
  if context=='incident':
   body['system']+=' Apply this conditional table exactly: first select the source from the supplied mapping for this case class. Read ONLY that selected source signal. If selected signal is false, command is console1/none. If selected signal is true, command is console1/ followed by the selected source name. Selecting a source does not itself activate it. Freshness, other sources, summary and queue are not predicates.'
 return body

def assignments():
 out=[]
 for i,m in enumerate(MAPPINGS):
  seed=7200+i;cases,rule=world(seed,m)
  for context in ('release','incident'):
   for repeat in (0,1):
    for arm in ('E','F'):
     for n,c in enumerate(cases):
      ident=f'R1-{seed}-{context}-r{repeat}-{arm}-{n}'
      out.append({'id':ident,'seed':seed,'context':context,'order':'single','repeat':repeat,'arm':arm,'cases':[c],'rule':rule,'positions':{c['id']:n+1},'request':request(c,rule,context,arm),'tldr':f'TLDR: R1 {context}, world {seed}, repetition {repeat+1}, arm {arm}. Compare unchanged atomic E with F exact-ID schema and explicit incident conditional; score assigned strict accuracy, useful-release recall, false actions and cost. Six finite worlds, bundled repair, dependent repeats; no culture or component-causality claim.'})
 random.Random('R1-dispatch-v1').shuffle(out);return out

def source_hash():
 paths=[ROOT/'R1-PLAN.md',ROOT/'d2/design.py',ROOT/'src/instrument.py',ROOT/'src/legacy-instructions.json']+sorted((ROOT/'r1').glob('*.py'))
 return hashlib.sha256(b''.join(str(p.relative_to(ROOT)).encode()+p.read_bytes() for p in paths)).hexdigest()

def check(design):
 assert len(design)==384 and sum(len(a['cases']) for a in design)==384 and len({a['id'] for a in design})==384
 hard={s:0 for s in d1.SOURCES}
 for i,m in enumerate(MAPPINGS):
  cases,rule=world(7200+i,m)
  for c in cases:
   src=rule[c['class']];e=c['evidence']
   if e[src]['signal'] and e[src]['fresh'] and all(not(e[s]['signal'] and e[s]['fresh']) for s in d1.SOURCES if s!=src):hard[src]+=1
 assert all(hard.values()),hard
 for a in design:
  assert len(json.dumps(a['request']).encode())<=2500
  other=next(x for x in design if all(x[k]==a[k] for k in ('seed','context','arm','cases')) and x['repeat']!=a['repeat']);assert other['request']==a['request']
  if a['arm']=='E':assert a['request']==d1.request(a['cases'],a['rule'],a['context'],'E')
 return {'calls':384,'decisions':384,'hard_conflict_positive_cases':hard,'max_request_bytes':max(len(json.dumps(a['request']).encode()) for a in design),'assignments_sha256':digest(design)}
if __name__=='__main__':print(json.dumps(check(assignments()),indent=2))
