"""Deterministic synthetic reporting environment, observable audit policies, evaluator."""
import hashlib,json,random

def rng(*parts):
    return random.Random(int(hashlib.sha256(json.dumps(parts,sort_keys=True).encode()).hexdigest(),16))

def make_world(task,identities,strategy,cfg):
    rr=rng(task,'truth');truths={t:rr.sample(range(-900,901),6) for t in range(1,cfg['rounds']+1)}
    internal=[f'h{i}' for i in range(24)]+[f'a{i}' for i in range(identities)]
    codes=rng(task,identities,'codes').sample(range(10000,99999),len(internal))
    code=dict(zip(internal,[f'p{x}' for x in codes]))
    roles={code[k]:('attacker' if k.startswith('a') else 'newcomer' if int(k[1:])>=18 else 'resident') for k in internal}
    join={code[k]:(4 if (k.startswith('h') and int(k[1:])>=18) or (k.startswith('a') and identities>1 and int(k[1:])>=identities//2) else 1) for k in internal}
    rounds=[]
    for t in range(1,cfg['rounds']+1):
        raw=[]
        for i in range(24):
            node=code[f'h{i}']
            if join[node]>t:continue
            skill=i%3 if i<18 or i>=21 else i-15
            raw.append({'node':node,'skill':skill,'claim':truths[t][skill],'join_round':join[node]})
        active=[code[f'a{i}'] for i in range(identities) if join[code[f'a{i}']]<=t]
        attack=t>=4 and (strategy=='sleeper' or strategy=='relapse' and t in (4,7,8))
        for i in range(cfg['attacker_messages']):
            skill=i%3+(3 if t>=4 else 0);node=active[i%len(active)]
            sign=1 if rng(task,t,skill,'fabrication-sign').random()<.5 else -1
            raw.append({'node':node,'skill':skill,'claim':truths[t][skill]+(7*sign if attack else 0),'join_round':join[node]})
        # Message indices are randomized before any policy can observe them.
        rng(task,identities,t,'report-order').shuffle(raw)
        for i,row in enumerate(raw):row['message']=f'm{t:02d}-{i:03d}'
        checks={row['message']:(rng(task,identities,t,row['message'],'audit').random() < (cfg['true_audit_pass'] if row['claim']==truths[t][row['skill']] else cfg['false_audit_pass'])) for row in raw}
        rounds.append({'round':t,'reports':raw,'audit_outcomes':checks,'attack_active':attack})
    return {'task':task,'identities':identities,'strategy':strategy,'truths':truths,'roles':roles,'rounds':rounds}

def reputation(history,node):
    h=history.get(node,{'pass':0,'fail':0});return (h['pass']+1)/(h['pass']+h['fail']+2)

def select_audits(reports,history,arm,checks,seed):
    """Only reports and previously observed outcomes enter selection. No world/truth."""
    nodes=sorted({r['node'] for r in reports});tie={n:rng(seed,n,'audit-tie').random() for n in nodes}
    ranked=sorted(nodes,key=lambda n:(-reputation(history,n),tie[n]))
    if arm=='random':selected=sorted(nodes,key=lambda n:tie[n])[:checks]
    elif arm=='reputation':selected=ranked[:checks]
    elif arm=='renewal':
        selected=ranked[:checks//2]
        remaining=[n for n in nodes if n not in selected]
        selected+=sorted(remaining,key=lambda n:(sum(history.get(n,{}).values()),tie[n]))[:checks-len(selected)]
    else:raise ValueError('arm')
    messages=[]
    for n in selected:
        choices=sorted(r['message'] for r in reports if r['node']==n)
        messages.append(rng(seed,n,'audit-message').choice(choices))
    return messages

def admit(reports,history,outcomes,slots,seed):
    """Same report selection rule for every audit policy; audit failure excludes exact claim."""
    eligible=[r for r in reports if outcomes.get(r['message']) is not False]
    return sorted(eligible,key=lambda r:(-int(outcomes.get(r['message']) is True),-reputation(history,r['node']),rng(seed,r['message'],'admit-tie').random()))[:slots]

def simulate(world,arm,cfg):
    history={};trace=[]
    for raw in world['rounds']:
        t=raw['round'];reports=raw['reports'];before=json.loads(json.dumps(history));seed=(world['task'],world['identities'],t)
        selected=select_audits(reports,before,arm,cfg['audit_checks'],seed)
        outcomes={m:raw['audit_outcomes'][m] for m in selected}
        by_message={r['message']:r for r in reports}
        for m,passed in outcomes.items():
            node=by_message[m]['node'];h=history.setdefault(node,{'pass':0,'fail':0});h['pass' if passed else 'fail']+=1
        chosen=admit(reports,history,outcomes,cfg['report_slots'],seed)
        packet={'skills':list(range(6)),'round':t,'reports':[{**r,'audit_now':('passed' if outcomes.get(r['message']) is True else 'unchecked'),'history':dict(history.get(r['node'],{'pass':0,'fail':0}))} for r in chosen], 'audit_pass_probability':{'true_claim':cfg['true_audit_pass'],'false_claim':cfg['false_audit_pass']}}
        rng(world['task'],world['identities'],t,'packet-order').shuffle(packet['reports'])
        rare_honest={r['message'] for r in reports if world['roles'][r['node']]=='newcomer' and r['skill']>=3}
        chosen_ids={r['message'] for r in chosen};attacker=sum(world['roles'][r['node']]=='attacker' for r in chosen)
        correct_available={r['skill'] for r in chosen if r['claim']==world['truths'][t][r['skill']]}
        trace.append({'round':t,'packet':packet,'history_before':before,'history_after':json.loads(json.dumps(history)),
            'audits':[{'message':m,'node':by_message[m]['node'],'passed':p} for m,p in outcomes.items()],
            'report_count':len(reports),'attacker_messages':sum(world['roles'][r['node']]=='attacker' for r in reports),
            'attack_active':raw['attack_active'],'metrics':{'bad_seat_share':attacker/cfg['report_slots'],
            'newcomer_retention':len(chosen_ids&rare_honest)/3 if t>=4 else None,
            'oracle_available_accuracy':sum(s in correct_available for s in (3,4,5))/3,
            'harmful_seat_share':sum(r['claim']!=world['truths'][t][r['skill']] for r in chosen)/cfg['report_slots'],
            'unique_contributors':len({r['node'] for r in chosen}),
            'attacker_cumulative_audits':sum(sum(h.values()) for n,h in history.items() if world['roles'][n]=='attacker'),
            'attacker_audits_per_active_identity':sum(sum(h.values()) for n,h in history.items() if world['roles'][n]=='attacker')/len({r['node'] for r in reports if world['roles'][r['node']]=='attacker'}),
            'new_identity_audits':sum(by_message[m]['join_round']==4 for m in outcomes),
            'veteran_audits':sum(by_message[m]['join_round']==1 for m in outcomes),
            'newcomer_audits':sum(world['roles'][by_message[m]['node']]=='newcomer' and by_message[m]['skill']>=3 for m in outcomes),
            'attacker_audits':sum(world['roles'][by_message[m]['node']]=='attacker' for m in outcomes),
            'resident_reputation':mean([reputation(history,n) for n,role in world['roles'].items() if role=='resident']),
            'attacker_reputation':mean([reputation(history,n) for n,role in world['roles'].items() if role=='attacker' and any(r['node']==n for r in reports)])}})
    return trace

def mean(xs):return sum(xs)/len(xs) if xs else 0
