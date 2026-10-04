#!/usr/bin/env python3
import argparse
import hashlib
import random
import common

def plans(stage,attempt):
    d=common.design()
    if stage not in ('S0','Q0','S1'):raise ValueError('S2_blocked')
    st=d['stages'][stage];ps=[]
    for task in st['tasks']:
        for seed in st['seeds']:
            for reg in st['regulators']:
                arms=list(d['arms']);random.Random(f'arm-order:{task}:{seed}:{reg}').shuffle(arms)
                ps.append({'stage':stage,'backend':st['backend'],'attempt_id':attempt,'task_id':task,'seed':seed,
                    'regulator':reg,'threshold':d['threshold'],'registration_fee':d['registration_fee'],
                    'rounds':st['rounds'],'arms':arms,'model':d['model'],'code':common.git('rev-parse','HEAD'),**common.hashes()})
    random.Random('stage-order:'+stage).shuffle(ps)
    return ps

def gate(stage,runs):
    if stage=='S0':return
    parent='S0' if stage=='Q0' else 'Q0';d=common.design();st=d['stages'][parent]
    expected={(t,s,r) for t in st['tasks'] for s in st['seeds'] for r in st['regulators']}
    probes=[r for r in runs if r['params'].get('stage')=='I0' and all(r['params'].get(k)==v for k,v in common.hashes().items()) and r['status']=='done' and r.get('metrics',{}).get('qualification_pass')==1]
    if not probes:raise ValueError('matching_interface_probes_incomplete')
    found=set()
    for r in runs:
        p=r['params'];m=r.get('metrics',{})
        if p.get('stage')!=parent or any(p.get(k)!=v for k,v in common.hashes().items()):continue
        if r['status']=='done' and m.get('invalid')==0 and m.get('visual_ok')==1 and m.get('qualification_pass')==1 and m.get('unpriced_calls',0)==0:
            names={a['name'] for a in r.get('artifacts',[])}
            if {'final_frame.png','replay.gif','episodes.jsonl','calls.jsonl'}<=names:found.add((p['task_id'],p['seed'],p['regulator']))
    if found!=expected:raise ValueError('matching_parent_qualification_incomplete')

def main():
    ap=argparse.ArgumentParser();ap.add_argument('command',choices=['register','stage']);ap.add_argument('stage',nargs='?',choices=['S0','Q0','S1']);ap.add_argument('--attempt');ap.add_argument('--dry-run',action='store_true');a=ap.parse_args()
    if a.command=='stage':
        if not a.attempt or not a.stage:ap.error('stage and attempt required')
        common.frozen(a.attempt)
        ps=plans(a.stage,a.attempt)
        if a.dry_run:
            print({'runs':len(ps),'episodes':2*len(ps),'max_model_calls':sum(2*p['rounds'] for p in ps) if a.stage!='S0' else 0});return
    import swarm_report as sr
    if a.command=='register':
        import yaml
        spec=yaml.safe_load((common.ROOT/'experiment.yaml').read_text());ident=spec.pop('id')
        # The registered plan is the README at the exact checked-out commit, never mutable main.
        spec['url']=f"https://github.com/dmarzzz/swarm-lab/blob/{common.git('rev-parse','HEAD')}/researchers/dmarz/notes/{common.EXP}/README.md"
        sr.register(ident,**spec);print('registered',ident,spec['url']);return
    existing=sr.runs(common.EXP,limit=500)
    if any(r['params'].get('attempt_id')==a.attempt for r in existing):raise ValueError('duplicate_attempt')
    gate(a.stage,[sr.get_run(r['run']) for r in existing])
    ids=[common.EXP+'/'+hashlib.sha256(f"{a.attempt}:{p['task_id']}:{p['seed']}:{p['regulator']}".encode()).hexdigest()[:12] for p in ps]
    print(sr.enqueue(common.EXP,ps,run_ids=ids,tags=['exploratory',a.stage]))
if __name__=='__main__':main()
