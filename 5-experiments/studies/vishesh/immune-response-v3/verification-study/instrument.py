"""Frozen finite verification instrument. Shared episode logic; command-line entry is offline replay only."""
import copy, hashlib, importlib.util, json, random, sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE))
import verification as study
import cases, controller, public_reference, native_provider
spec=importlib.util.spec_from_file_location('verification_candidate',BASE.parent/'controller-study/next-contract/candidate.py')
candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
MODEL='anthropic/claude-opus-4.6'
SEED=3100401
MAX_CALLS=192
MAX_WIRE_BYTES=8000
MAX_OUTPUT_TOKENS=512

def digest(x):
    return hashlib.sha256(json.dumps(x,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def assignments():
    rng=random.Random(SEED); result=[]
    for root in dict.fromkeys(c['root'] for c in study.roots()):
        for repeat in (1,2):
            block=[(b,g) for b in ('confirmed','contradicted') for g in (False,True)]
            rng.shuffle(block)
            for branch,guarded in block:
                result.append({'id':f'{root}/{branch}/{"guarded" if guarded else "unguarded"}/{repeat}',
                               'root':root,'family':root.split('-')[0],'branch':branch,
                               'guarded':guarded,'repeat':repeat,'case_id':root+'-'+branch})
    return result

def request(c,o,phase,diagnosis=None):
    q=candidate.diagnosis_request(o) if phase=='diagnosis' else candidate.action_request(c,o,diagnosis,'justification_first')
    body=native_provider.wire(q,MODEL);native_provider.validate_wire(body)
    return q,body

def episode(c,a,respond=None,event=None):
    state=copy.deepcopy(c['initial']);trace=[];history=[];events=[]
    def record(e):
        events.append(e)
        if event:event(e)
    for tick in (1,2):
        o=study.observation(c,state,tick,history)
        q,body=request(c,o,'diagnosis')
        d=respond(q,body) if respond else public_reference.labels(o)
        record({'tick':tick,'phase':'diagnosis','wire':body,'response':d})
        controller.validate_diagnosis(o,d)
        q,body=request(c,o,'action',d)
        raw=respond(q,body) if respond else public_reference.choose(o)
        if not respond:raw={k:raw[k] for k in q['response_schema']['required']}
        record({'tick':tick,'phase':'action','wire':body,'response':raw})
        if list(raw)!=q['response_schema']['required']:raise ValueError('action_order_failed')
        decoded=cases.f.controller.decode(c['fixture'],raw)
        x=study.step(c,state,decoded,o,a['guarded'])
        x.update(tick=tick,observation=o,diagnosis=d,diagnosis_correct=d==public_reference.labels(o),raw_response=raw)
        trace.append(x)
        if event:event({'kind':'frame',**x})
        history.append({'proposal':decoded,'action':x['action'],'result':x['result']})
    s=study.summarize(c,trace);s['diagnosis_pass']=all(x['diagnosis_correct'] for x in trace)
    s['qualified']=s['proposal_contract_pass'] and s['diagnosis_pass']
    return {**a,**s,'trace':trace,'events':events}

METRICS=('post_state_gate','proposal_contract_pass','qualified','diagnosis_pass','served_opportunities',
         'unnecessary_proposed','unnecessary_executed','guard_denials','missed_repair','post_action_verified')

def analyze(rows):
    """Descriptive paired estimates; no tick/call pseudoreplication or invented missing zeros."""
    expected=assignments(); known={a['id']:a for a in expected}; cells={}
    for row in rows:
        if row['id'] not in known or row['id'] in cells:raise ValueError('unknown_or_duplicate_assignment')
        if any(row[k]!=v for k,v in known[row['id']].items()):raise ValueError('assignment_mismatch')
        cells[row['id']]=row
    contrasts=[]; disagreement=[]
    for root in dict.fromkeys(a['root'] for a in expected):
        family=root.split('-')[0]
        for branch in ('confirmed','contradicted'):
            for repeat in (1,2):
                pair=[cells.get(f'{root}/{branch}/{arm}/{repeat}') for arm in ('unguarded','guarded')]
                contrasts.append({'root':root,'family':family,'branch':branch,'repeat':repeat,
                    'complete':all(x is not None for x in pair),
                    'guarded_minus_unguarded':{m:(float(pair[1][m])-float(pair[0][m])) if all(x is not None and x[m] is not None for x in pair) else None for m in METRICS}})
            for arm in ('unguarded','guarded'):
                pair=[cells.get(f'{root}/{branch}/{arm}/{r}') for r in (1,2)]
                disagreement.append({'root':root,'family':family,'branch':branch,'arm':arm,
                    'complete':all(x is not None for x in pair),
                    'outcome_disagrees':{m:pair[0][m]!=pair[1][m] if all(x is not None for x in pair) else None for m in METRICS},
                    'proposal_sequence_disagrees':([{k:v for k,v in x['proposal'].items() if k!='reason'} for x in pair[0]['trace']]!=[{k:v for k,v in x['proposal'].items() if k!='reason'} for x in pair[1]['trace']]) if all(x is not None for x in pair) else None})
    def group_summary(field):
        result=[]
        for value in dict.fromkeys(x[field] for x in contrasts):
            for branch in ('confirmed','contradicted'):
                group=[x for x in contrasts if x[field]==value and x['branch']==branch]
                complete=[x for x in group if x['complete']]
                means={}
                for m in METRICS:
                    vals=[x['guarded_minus_unguarded'][m] for x in complete if x['guarded_minus_unguarded'][m] is not None]
                    means[m]={'mean':sum(vals)/len(vals) if vals else None,'paired_count':len(vals)}
                result.append({field:value,'branch':branch,'assigned_pairs':len(group),'complete_pairs':len(complete),'paired_differences':means})
        return result
    return {'assigned':len(expected),'completed':len(cells),'missing_ids':[a['id'] for a in expected if a['id'] not in cells],
            'paired_contrasts':contrasts,'root_summaries':group_summary('root'),'family_summaries':group_summary('family'),
            'fresh_repeat_disagreement':disagreement,'inference':'descriptive; six authored roots clustered in three families; no population interval'}

def replay(out):
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    packet=json.loads((BASE/'packet.json').read_text())
    if packet['assignments']!=assignments():raise ValueError('assignments_changed')
    for rel,sha in packet['source_sha256'].items():
        if hashlib.sha256((BASE.parent/rel).read_bytes()).hexdigest()!=sha:raise ValueError('source_changed')
    worlds={c['id']:c for c in study.roots()};rows=[]
    for a in assignments():rows.append(episode(worlds[a['case_id']],a))
    (out/'episodes.json').write_text(json.dumps(rows,indent=2)+'\n')
    summary={'kind':'offline_rule_replay','native_calls':0,'scripted_responses':192,**analyze(rows)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary

if __name__=='__main__':
    import argparse
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--backend',choices=['offline'],default='offline');a=p.parse_args()
    s=replay(a.out);print(json.dumps({k:s[k] for k in ('native_calls','scripted_responses','assigned','completed')}))
