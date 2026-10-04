"""Freeze actor cases, evaluator answers, assignments and exact integer bounds."""
from pathlib import Path
import hashlib,json
from corpus import cases,mutation,reference,assignments,canonical
from contract import request,PER,MAX_OUTPUT
ROOT=Path(__file__).resolve().parents[1]
def envelope():
    return {'main_calls':384,'qualification_calls':2,'max_calls':386,'per_call_nano':PER,'model_max_nano':386*PER,'infrastructure_max_nano':250000000,'prior_nano':450886510,'additional_max_nano':386*PER+250000000,'cumulative_max_nano':450886510+386*PER+250000000,'proposed_study_cap_nano':50000000000,'funded':False}
def build():
    dest=ROOT/'prepared';dest.mkdir(exist_ok=True);cs=cases();checks=[]
    for c in cs:
        m=mutation(c)
        assert reference(c['actor'],c['question'])==c['gold']['answer']
        assert reference(m['actor'],m['question'])==m['gold']['answer']!=c['gold']['answer']
        text='\n'.join(r['text'] for r in c['actor']['records']);previous={'handoff':text,'decision':c['gold']['initial_decision']}
        # UTF-8 bytes are a conservative upper bound for this plain ASCII corpus.
        size=len(canonical(previous).encode());assert size<=MAX_OUTPUT
        bounds=[len(canonical(request(a,c['actor'],previous,c['question'] if reader else None)).encode())+1024 for a in ('P','R') for reader in (True,False)]
        checks.append({'id':c['id'],'family':c['family'],'label':c['gold']['answer'],'mutated_label':m['gold']['answer'],'copy_json_bytes':size,'max_input_bound':max(bounds)})
    qual={
      'q01':{'actor':{'records':[{'id':'q1','time':'09:00','text':'The recorded restore test succeeded.'}]},'question':'Does the recorded restore test establish successful recovery?'},
      'q02':{'actor':{'records':[{'id':'q1','time':'09:00','text':'Export permission was requested. Its response receipt is unavailable.'}]},'question':'Is an effective permission grant recorded for export?'}}
    artifacts={'actors.json':{c['id']:c['actor'] for c in cs},'questions.json':{c['id']:c['question'] for c in cs},'gold.json':{c['id']:c['gold'] for c in cs},'mutations.json':{c['id']:{'actor':mutation(c)['actor'],'gold':mutation(c)['gold']} for c in cs},'assignments.json':assignments(),'qualification.json':qual,'qualification-gold.json':{'q01':'YES','q02':'UNKNOWN'},'envelope.json':envelope(),'validation.json':{'native_calls':0,'source_worlds':24,'shared_families':8,'blocks':2,'assignments':384,'reader_endpoints':96,'checks':checks}}
    for name,obj in artifacts.items():(dest/name).write_text(json.dumps(obj,indent=2)+'\n')
    paths=list(dest.glob('*.json'))+list((ROOT/'src').glob('*.py'))+list((ROOT/'tests').glob('*.py'))+list(ROOT.glob('*.md'))
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.name!='manifest.json'}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'offline_only':True,'cases':24,'families':8,'main_calls':384,'max_calls':386,'envelope':envelope()}))
if __name__=='__main__':build()
