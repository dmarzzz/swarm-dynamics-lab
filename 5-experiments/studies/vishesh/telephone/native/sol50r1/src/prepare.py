from pathlib import Path
import hashlib,json,copy
from corpus import actor,questions,controls,reference,assignments,canonical
from contract import request,PER,MAX_OUTPUT
ROOT=Path(__file__).resolve().parents[1]
def envelope():return {'main_calls':74,'qualification_calls':3,'max_calls':77,'per_call_nano':PER,'model_max_nano':77*PER,'infrastructure_max_nano':250000000,'prior_nano':673196669,'additional_max_nano':77*PER+250000000,'cumulative_max_nano':673196669+77*PER+250000000,'proposed_study_cap_nano':50000000000,'funded':False}
def build():
 dest=ROOT/'prepared';dest.mkdir(exist_ok=True);a=actor();qs=questions();labels={'Cedar':'RELEASE','Bay':'HOLD','Delta':'INSUFFICIENT'}
 assert {s:reference(a,q) for s,q in qs.items()}==labels
 for c in controls():assert reference(c['actor'],c['question'])==c['expected'],c['kind']
 prev={'handoff':'\n'.join(r['text'] for r in a['records'])};size=len(canonical(prev).encode());assert size<=MAX_OUTPUT,size
 bounds=[len(canonical(request(arm,a,prev,q)).encode())+1024 for q in qs.values() for arm in ('P','R')]
 qualification={};qgold={}
 for i,(site,q) in enumerate(qs.items(),1):
  renamed={'Cedar':'Harbor','Bay':'Inlet','Delta':'Ridge'};qa=canonical(a);qq=q
  for old,new in renamed.items():qa=qa.replace(old,new);qq=qq.replace(old,new)
  cid=f'q{i:02}';qa=json.loads(qa);assert reference(qa,qq)==labels[site];qualification[cid]={'actor':qa,'question':qq};qgold[cid]=labels[site]
 data={'actors.json':{s:a for s in qs},'questions.json':qs,'gold.json':{s:{'answer':v} for s,v in labels.items()},'controls.json':controls(),'assignments.json':assignments(),'qualification.json':qualification,'qualification-gold.json':qgold,'envelope.json':envelope(),'validation.json':{'native_calls':0,'roots':1,'writers':50,'reader_endpoints':24,'checkpoints':[1,10,25,50],'controls':len(controls()),'copy_json_bytes':size,'max_lossless_request_bound':max(bounds)}}
 for n,x in data.items():(dest/n).write_text(json.dumps(x,indent=2)+'\n')
 paths=list(dest.glob('*.json'))+list((ROOT/'src').glob('*.py'))+list((ROOT/'tests').glob('*.py'))+list(ROOT.glob('*.md'))
 (dest/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.name!='manifest.json'},indent=2)+'\n')
 print(json.dumps(data['validation.json']))
if __name__=='__main__':build()
