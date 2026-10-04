"""Deterministic offline B2 packet preparation; no native dispatch."""
import hashlib, importlib.util, json
from pathlib import Path
from corpus import CASES, actor, canonical, copy_output, decide, gold, mutated, reference, source_controller

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('sol50_contract',ROOT.parent/'sol50/src/contract.py')
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
SYSTEM=base.SYSTEM.replace('engineering handoff','operational handoff')

def request(arm, packet, previous=None):
    if arm not in ('P','R'):raise ValueError('arm')
    # Reuse validated route/limits; supply B2's declared evidence policy.
    req=base.request(packet=packet)
    req['messages'][0]['content']=SYSTEM
    payload={}
    if previous is None or arm=='R':payload['source_packet']=packet
    if previous is not None:
        base.validate_object(previous);payload['previous_handoff']=previous
    req['messages'][1]['content']=canonical(payload)
    if len(canonical(req).encode())+1024>base.MAX_INPUT:raise ValueError('input_bound')
    return req

def assignments():
    rows=[]
    for block in (1,2):
        order=list(range(12)) if block==1 else list(reversed(range(12)))
        for ix in order:
            c=CASES[ix]
            arms=('P','R') if (ix+block)%2 else ('R','P')
            for arm in arms:
                for hop in (1,2,3):
                    prefix=f"block-{block}:{c['id']}:{arm}"
                    rows.append({'id':prefix+f':{hop}','block':block,'case_id':c['id'],'arm':arm,'hop':hop,'parent':None if hop==1 else prefix+f':{hop-1}'})
    return rows

def validate():
    report=[]
    for c in CASES:
        m=mutated(c)
        assert decide(c)==reference(c)==source_controller(actor(c))==c['expected']
        assert decide(m)==reference(m)==source_controller(actor(m))==m['expected']
        output=copy_output(c);size=len(canonical(output).encode())
        assert size<=base.MAX_OUTPUT # conservative byte ceiling, not tokenizer count
        bounds={a:len(canonical(request(a,actor(c),output)).encode())+1024 for a in ('P','R')}
        report.append({'id':c['id'],'gold':c['expected'],'reference':reference(c),'source_controller':source_controller(actor(c)),'mutation_gold':m['expected'],'mutation_reference':reference(m),'mutation_source_controller':source_controller(actor(m)),'targets':len(gold(c)['targets']),'full_copy_json_bytes':size,'input_bounds_with_full_copy':bounds})
    return report

def build():
    dest=ROOT/'prepared';dest.mkdir(exist_ok=True)
    artifacts={'actor-packets.json':{c['id']:actor(c) for c in CASES},
      'qualification-actor.json':{
        'q01':{'records':[{'id':'q1','time':'09:00','text':'GO requires latency at most 120 ms, rollback tested and recorded approval; otherwise HOLD. Latency is 100 ms, rollback is tested and approval is recorded.'}]},
        'q02':{'records':[{'id':'q2','time':'09:00','text':'GO requires latency at most 120 ms, rollback tested and recorded approval; otherwise HOLD. Latency is 100 ms and rollback is tested. Approval was requested, but the receipt is unavailable and approval remains unknown.'}]}},
      'qualification-gold.json':{'q01':'GO','q02':'HOLD'},
      'gold.json':{c['id']:gold(c) for c in CASES},
      'mutation-packets.json':{c['id']:actor(mutated(c)) for c in CASES},
      'mutation-gold.json':{c['id']:gold(mutated(c)) for c in CASES},
      'assignments.json':assignments(),'validation.json':{'native_calls':0,'source_roots':12,'fresh_blocks_planned':2,'rows':validate()},
      'envelope.json':{'max_calls':146,'main_calls':144,'qualification_calls':2,'per_call_nano':31744001,'model_max_nano':146*31744001,'infrastructure_max_nano':250000000,'prior_nano':113744701,'additional_max_nano':146*31744001+250000000,'cumulative_max_nano':146*31744001+250000000+113744701,'study_cap_nano':5000000000,'funded':False}}
    for name,obj in artifacts.items():(dest/name).write_text(json.dumps(obj,indent=2)+'\n')
    files=list(dest.glob('*.json'))+list((ROOT/'src').glob('*.py'))+list((ROOT/'tests').glob('*.py'))+list(ROOT.glob('*.md'))+[ROOT/'CASE-SPECS.json']
    files=[p for p in files if p.name!='manifest.json']
    manifest={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(files)}
    (dest/'manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    print(json.dumps({'cases':12,'targets':sum(len(gold(c)['targets']) for c in CASES),'main_assignments':len(assignments()),'max_full_copy_bytes':max(r['full_copy_json_bytes'] for r in validate()),'native_calls':0}))

if __name__=='__main__':build()
