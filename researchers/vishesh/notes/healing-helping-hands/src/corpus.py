"""Synthetic reports. Only observation() is exposed to a model."""
import random
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
N=200
CLAIMS=20
TEMPLATES={
'SUPPORT':['The study found that {method} improved {outcome}.','Results showed better {outcome} when {method} was used.','Using {method} increased {outcome} compared with the baseline.'],
'REFUTE':['The study found that {method} did not improve {outcome}.','Results showed worse {outcome} when {method} was used.','Using {method} decreased {outcome} compared with the baseline.'],
'UNCERTAIN':['The study did not measure {outcome}; it measured runtime only.','The report lists the name {method} but provides no results for {outcome}.','Whether {method} improves {outcome} has not yet been tested.']}
def make(seed):
 r=random.Random(seed);claims=[];roots={};docs=[]
 for c in range(CLAIMS):
  method=f'method {chr(65+c)}';outcome='retrieval accuracy' if c%2 else 'answer accuracy'
  labels=[['SUPPORT','SUPPORT','REFUTE','UNCERTAIN','UNCERTAIN'],['REFUTE','REFUTE','SUPPORT','UNCERTAIN','UNCERTAIN'],['SUPPORT','REFUTE','UNCERTAIN','UNCERTAIN','UNCERTAIN'],['UNCERTAIN']*5][c%4][:];r.shuffle(labels)
  claims.append(f'{method.capitalize()} improves {outcome}.')
  for k,label in enumerate(labels):
   rid=f'C{c:02d}-R{k}';roots[rid]={'claim':c,'label':label,'text':r.choice(TEMPLATES[label]).format(method=method,outcome=outcome)}
 for i in range(N):
  c=i%20;k=(i//20)//2;rid=f'C{c:02d}-R{k}'
  docs.append({'id':i,'claim':c,'root':rid,'text':roots[rid]['text'],'label':roots[rid]['label']})
 withdrawn=[r.choice([k for k,v in roots.items() if v['claim']==c]) for c in range(CLAIMS)]
 erased=sorted(r.sample(range(N),40));heads=sorted(c+20*r.randrange(10) for c in range(CLAIMS))
 recipients={rid:next(d['id'] for d in docs if d['root']==rid) for rid in withdrawn}
 return {'seed':seed,'claims':claims,'roots':roots,'docs':docs,'withdrawn':withdrawn,'erased':erased,'heads':heads,'recipients':recipients}
def observation(corpus,doc):return {'claim':corpus['claims'][doc['claim']],'report':doc['text']}
def qualification():
 r=random.Random(8000);out=[]
 for label in LABELS:
  for i in range(10):
   method=f'procedure {i+31}';outcome='classification accuracy'
   out.append({'claim':f'{method.capitalize()} improves {outcome}.','report':TEMPLATES[label][i%3].format(method=method,outcome=outcome),'expected':label})
 r.shuffle(out);return out
