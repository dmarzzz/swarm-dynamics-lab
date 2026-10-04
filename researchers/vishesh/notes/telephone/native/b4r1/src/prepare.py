from pathlib import Path
import hashlib,json
from corpus import cases,ablations,reference,assignments,canonical
from contract import request,PER,MAX_OUTPUT
ROOT=Path(__file__).resolve().parents[1]
def envelope():return {'main_calls':90,'qualification_calls':2,'max_calls':92,'per_call_nano':PER,'model_max_nano':92*PER,'infrastructure_max_nano':250000000,'prior_nano':452862510,'additional_max_nano':92*PER+250000000,'cumulative_max_nano':452862510+92*PER+250000000,'proposed_study_cap_nano':50000000000,'funded':False}
def build():
 dest=ROOT/'prepared';dest.mkdir(exist_ok=True);cs=cases();checks=[]
 for c in cs:
  assert reference(c['actor'],c['question'])==c['gold']['answer']
  prev={'handoff':'\n'.join(r['text'] for r in c['actor']['records']),'decision':'GO'};size=len(canonical(prev).encode());assert size<=MAX_OUTPUT,(c['id'],size)
  for a in ablations(c):assert a['expected']!='RELEASE'
  bounds=[len(canonical(request(arm,c['actor'],prev,c['question'])).encode())+1024 for arm in ('P','R')]
  checks.append({'id':c['id'],'family':c['family'],'label':c['gold']['answer'],'copy_json_bytes':size,'max_input_bound':max(bounds)})
 import copy
 qs={}
 for cid,label in (('q01','RELEASE'),('q02','INSUFFICIENT')):
  c=copy.deepcopy(next(c for c in cs if c['family']=='version_exception' and c['gold']['answer']==label))
  for r in c['actor']['records']:r['text']=r['text'].replace('v3','v11').replace('West','Harbor')
  question=c['question'].replace('v3','v11').replace('West','Harbor')
  assert reference(c['actor'],question)==label
  qs[cid]={'actor':c['actor'],'question':question}
 data={'actors.json':{c['id']:c['actor'] for c in cs},'questions.json':{c['id']:c['question'] for c in cs},'gold.json':{c['id']:c['gold'] for c in cs},'ablations.json':{c['id']:ablations(c) for c in cs},'assignments.json':assignments(),'qualification.json':qs,'qualification-gold.json':{'q01':'RELEASE','q02':'INSUFFICIENT'},'envelope.json':envelope(),'validation.json':{'native_calls':0,'worlds':9,'shared_scenario_recipes':3,'blocks':2,'assignments':90,'reader_endpoints':36,'checks':checks}}
 for name,obj in data.items():(dest/name).write_text(json.dumps(obj,indent=2)+'\n')
 paths=list(dest.glob('*.json'))+list((ROOT/'src').glob('*.py'))+list((ROOT/'tests').glob('*.py'))+list(ROOT.glob('*.md'))
 (dest/'manifest.json').write_text(json.dumps({str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.name!='manifest.json'},indent=2)+'\n')
 print(json.dumps({'offline_only':True,'envelope':envelope(),'max_copy_bytes':max(c['copy_json_bytes'] for c in checks)}))
if __name__=='__main__':build()
