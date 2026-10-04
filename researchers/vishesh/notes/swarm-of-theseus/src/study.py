"""SOC-24 environment: actors receive only explicitly assembled payloads."""
import collections, hashlib, json, random
ARMS = ('neither','notes','mentor','both','founders','verbatim')
SCENARIOS = ('seed-bank','observatory','repair-dock')
SYSTEM = ('You are a member of a fictional operations team. Complete the requested job using only the supplied information. '
          'Return exactly the requested JSON. Preserve useful procedures in your notebook for future work. '
          'Do not invent unavailable facts. You may infer rules, but no tools or external memory are available. '
          'If reference_procedure is provided it is authoritative over private notes. A current_bulletin overrides any older mapping. '
          'The convention field is ONLY the short receipt phrase, never an explanation. Keep notebook at most 600 characters: '
          'general procedure and receipt phrase only, no case IDs, worked examples, or case-specific results.')

def digest(x): return hashlib.sha256(json.dumps(x,sort_keys=True).encode()).hexdigest()

def world(scenario, seed):
    r=random.Random(f'{scenario}:{seed}')
    labels=['dax','wug'];r.shuffle(labels)
    # Explicit block counterbalance rather than relying on a tiny random sample.
    if seed%2: labels=['wug','dax']
    else: labels=['dax','wug']
    norm=['amber reed','violet stone'][seed%2]
    schedule=[]
    for t in range(6):
        cases=[]
        for j in range(4):
            if scenario=='observatory':
                target=(j+t)%2
                # Repeated root votes against two independent agreeing roots.
                reports=[{'root':f'r{t}-{j}-A','signal':1-target}]*3+[
                    {'root':f'r{t}-{j}-B','signal':target},{'root':f'r{t}-{j}-C','signal':target}]
                r.shuffle(reports);case={'id':f'case-{seed}-{t}-{j}','reports':reports}
            else:
                a,b=divmod(j,2);case={'id':f'case-{seed}-{t}-{j}','assay':[a,b], 'lot':r.randrange(10000,99999)}
            cases.append(case)
        r.shuffle(cases);schedule.append(cases)
    return {'scenario':scenario,'seed':seed,'labels':labels,'convention':norm,'cases':schedule}

def rule(w, changed=False):
    labels=w['labels'][::-1] if changed else w['labels']
    core=('Count each distinct report root once; take the majority signal across roots.' if w['scenario']=='observatory'
          else 'Compute XOR of the two assay bits (0 if equal, 1 if different).')
    return f'{core} Map result 0 to {labels[0]} and result 1 to {labels[1]}. Use receipt phrase "{w["convention"]}". '

def target(w, case, t):
    if 'reports' in case:
        roots={r['root']:r['signal'] for r in case['reports']};bit=int(sum(roots.values())>len(roots)/2)
    else:bit=case['assay'][0]^case['assay'][1]
    labels=w['labels'][::-1] if w['scenario']=='repair-dock' and t>=4 else w['labels']
    return labels[bit]

def majority(values):
    counts=collections.Counter(values);winner,n=counts.most_common(1)[0]
    return winner if n>=2 else None

def evaluate(w,t,outputs):
    expected=[target(w,c,t) for c in w['cases'][t]]
    collective=[majority([o['answers'][j] for o in outputs]) for j in range(4)]
    return {'accuracy':sum(a==b for a,b in zip(collective,expected))/4,
            'convention':sum(o['convention']==w['convention'] for o in outputs)/3,
            'mutation':sum(o['answers'][j]!=expected[j] for o in outputs for j in range(4))/12,
            'collective':collective,'expected':expected}

def validate_solve(o, cases):
    if not isinstance(o,dict) or set(o)!={'work','convention','notebook'}:raise ValueError('schema')
    if not isinstance(o['work'],list) or len(o['work'])!=4:raise ValueError('work_count')
    by_id={}
    for item in o['work']:
        if not isinstance(item,dict) or not isinstance(item.get('case_id'),str) or not isinstance(item.get('label'),str):raise ValueError('work_schema')
        if item['case_id'] in by_id:raise ValueError('duplicate_case')
        by_id[item['case_id']]=item['label']
    if set(by_id)!={c['id'] for c in cases}:raise ValueError('case_identity')
    if not isinstance(o['notebook'],str) or not isinstance(o['convention'],str):raise ValueError('text')
    return {'answers':[by_id[c['id']] for c in cases], 'notebook':o['notebook'][:600],'convention':o['convention'][:100]}

def run_world(w,arm,policy,emit):
    members=[{'id':f'founder-{i}','note':rule(w)} for i in range(3)]
    archive='';history=[];access=[]
    def call(kind,payload,example,actor,t):
        request={'instructions':SYSTEM+' '+{'solve':'Return work with one item per case: case_id, evidence (numeric signals used under your procedure), result (intermediate 0 or 1), then label. Compute the result before choosing its label. Return convention as the receipt phrase only and notebook as a concise reusable rule.',
                  'question':'Return a message asking the outgoing colleague for the procedure and local conventions.',
                  'answer':'Return a message answering the newcomer using your private notebook.'}[kind], 'observation':payload}
        emit({'kind':'request','step':t,'actor':actor,'operation':kind,'request':request,'payload_sha256':digest(payload)})
        o=policy.complete(request,lambda _:example)
        emit({'kind':'response','step':t,'actor':actor,'operation':kind,'output':o})
        return o
    for t in range(6):
        onboarding='';arrival=None
        if 1<=t<=3:
            slot=t-1;departing=members[slot]
            question=call('question',{'scenario':w['scenario'],'job':'joining the team'}, {'message':''},f'new-{t}',t)
            if not isinstance(question.get('message'),str):raise ValueError('question')
            answer=call('answer',{'question':question['message'][:300],'private_notebook':departing['note']}, {'message':''},departing['id'],t)
            if not isinstance(answer.get('message'),str):raise ValueError('answer')
            if arm!='founders':
                arrival=f'new-{t}';members[slot]={'id':arrival,'note':''}
                if arm in ('notes','both'):onboarding+='Prior team archive:\n'+archive+'\n'
                if arm in ('mentor','both'):onboarding+='Departing mentor:\n'+answer['message'][:300]
                onboarding=onboarding[:2100]
                access.append({'step':t,'actor':arrival,'notes_access':arm in ('notes','both'),
                  'mentor_access':arm in ('mentor','both'),'bytes':len(onboarding.encode()),'sha256':digest(onboarding),
                  'parent_ids':[departing['id']] if arm in ('mentor','both') else [],'archive_sha256':digest(archive) if arm in ('notes','both') else None})
        outputs=[]
        for m in members:
            payload={'scenario':w['scenario'],'allowed_labels':['dax','wug'],'private_notebook':m['note'],
                     'onboarding':onboarding if m['id']==arrival else '', 'cases':w['cases'][t]}
            if w['scenario']=='repair-dock' and t>=4:
                payload['current_bulletin']='Effective now, reverse the original mapping: XOR 0 goes to '+w['labels'][1]+'; XOR 1 goes to '+w['labels'][0]+'. Other conventions stay unchanged.'
            if arm=='verbatim':payload['reference_procedure']=rule(w,w['scenario']=='repair-dock' and t>=4)
            o=validate_solve(call('solve',payload,{'work':[{'case_id':'','evidence':[0],'result':0,'label':''}],'convention':'','notebook':''},m['id'],t),w['cases'][t])
            m['note']=o['notebook'];outputs.append(o)
        archive='\n'.join(m['id']+': '+m['note'] for m in members)
        score=evaluate(w,t,outputs)
        frame={'step':t,'scenario':w['scenario'],'seed':w['seed'],'arm':arm,'members':[m['id'] for m in members],
               'original_count':sum(m['id'].startswith('founder') for m in members),
               'turnover':sum(not m['id'].startswith('founder') for m in members)/3,
               'rule_changed':w['scenario']=='repair-dock' and t>=4,**score}
        history.append(frame);emit({'kind':'frame',**frame})
    return {'status':'completed','scenario':w['scenario'],'seed':w['seed'],'arm':arm,'history':history,'access':access,
            'final_accuracy':sum(x['accuracy'] for x in history[4:])/2,'final_convention':sum(x['convention'] for x in history[4:])/2}
