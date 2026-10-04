"""Offline C4 policy and scoring. Never imports providers or dispatches calls."""
import hashlib,json,math
LABELS=('SUPPORT','REFUTE','UNCERTAIN')
ARMS=('qwen','jev','cascade','matched')
LIMITS={'S0':{'cases':60,'qwen':120,'jev':60},'S1':{'cases':432,'qwen':864,'jev':432}}

def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,separators=(',',':')).encode()).hexdigest()

def actor_input(case):
    return {k:case[k] for k in ('claim','report')}

def qwen_payload(case,variant):
    if variant not in (0,1):raise ValueError('invalid_variant')
    visible=actor_input(case)
    choices=list(LABELS[variant:]+LABELS[:variant])
    return {'model':'qwen3:0.6b','messages':[{'role':'user','content':'Classify REPORT relative to CLAIM. SUPPORT: accuracy improved on the named task. REFUTE: measured accuracy was worse or unchanged. UNCERTAIN: the report does not establish the named comparison. Use only the report. Return JSON with label.\nCLAIM: '+visible['claim']+'\nREPORT: '+visible['report']}],'think':False,'stream':False,'format':{'type':'object','properties':{'label':{'type':'string','enum':choices}},'required':['label'],'additionalProperties':False},'options':{'temperature':0,'seed':9400,'num_ctx':2048,'num_predict':32},'keep_alive':'30m'}

def rank(row):
    return digest({'salt':'C4-matched-v1','id':row['id']})

def score(rows):
    if not rows or len({r['id'] for r in rows})!=len(rows):raise ValueError('empty_or_duplicate_assignments')
    for r in rows:
        if r['expected'] not in LABELS:raise ValueError('invalid_truth')
        if any(v not in LABELS for v in r.get('labels',{}).values()):raise ValueError('invalid_output')
    families=sorted({r['family'] for r in rows});details=[];strata={}
    for family in families:
        assigned=[r for r in rows if r['family']==family]
        complete=[r for r in assigned if r.get('status')=='completed' and all(k in r.get('labels',{}) for k in ('a','b','jev'))]
        k=sum(r['labels']['a']!=r['labels']['b'] for r in complete)
        chosen={r['id'] for r in sorted(complete,key=rank)[:k]}
        group=[]
        for r in assigned:
            valid=r in complete;l=r.get('labels',{});refer=valid and l['a']!=l['b']
            predictions=({'qwen':l['a'],'jev':l['jev'],'cascade':l['jev'] if refer else l['a'],'matched':l['jev'] if r['id'] in chosen else l['a']} if valid else dict.fromkeys(ARMS))
            group.append({'id':r['id'],'family':family,'curator':int(hashlib.sha256(r['id'].encode()).hexdigest()[:8],16)%200,'complete':valid,'referred':refer if valid else None,'matched_referred':r['id'] in chosen if valid else None,'predictions':predictions,'correct':{a:predictions[a]==r['expected'] for a in ARMS},'expected':r['expected']})
        n=len(assigned);done=len(complete)
        error={a:sum(not x['correct'][a] for x in group)/n for a in ARMS}
        # Analytic expectation over every equally likely size-k random subset.
        random_error=((n-done)+sum((1-k/done)*(r['labels']['a']!=r['expected'])+(k/done)*(r['labels']['jev']!=r['expected']) for r in complete))/n if done else 1.
        qwrong=sum(r['labels']['a']!=r['expected'] for r in complete)
        caught=sum(r['labels']['a']!=r['expected'] and r['labels']['a']!=r['labels']['b'] for r in complete)
        accepted=[r for r in complete if r['labels']['a']==r['labels']['b']]
        missed=sum(r['labels']['a']!=r['expected'] for r in accepted)
        strata[family]={'assigned':n,'completed':done,'error':error,'referrals':k,'avoided':done-k,'accepted_wrong':missed,'accepted_wrong_rate':missed/len(accepted) if accepted else None,'error_detection_recall':caught/qwrong if qwrong else None,'uniform_random_expected_error':random_error,'safety_delta':error['cascade']-error['jev'],'matched_delta':error['cascade']-error['matched'],'expected_random_delta':error['cascade']-random_error}
        details.extend(group)
    complete=sum(v['completed'] for v in strata.values());referrals=sum(v['referrals'] for v in strata.values());n=len(rows)
    mean=lambda key:sum(v[key] for v in strata.values())/len(strata)
    safety=mean('safety_delta');contrast=mean('matched_delta');saving=(complete-referrals)/n
    loo={f:sum(v['matched_delta'] for k,v in strata.items() if k!=f)/(len(strata)-1) for f in families} if len(families)>1 else {}
    return {'assigned':n,'completed':complete,'missing':n-complete,'families':strata,'macro_safety_delta':safety,'macro_matched_delta':contrast,'macro_expected_random_delta':mean('expected_random_delta'),'jev_calls_avoided_fraction':saving,'actual_collection_jev_calls_expected':complete,'counterfactual_cascade_jev_calls':referrals,'leave_one_family_out_matched_delta':loo,'complete_evidence':complete==n,'criteria':{'save_at_least_25_percent':saving>=.25,'safety_within_2_points':safety<=.02,'beat_matched_control':contrast<0},'useful_descriptive_result':complete==n and saving>=.25 and safety<=.02 and contrast<0,'missingness_note':'Missing scores incorrect; safety/matched paired contrasts involving missing outcomes remain unidentified, not observed zero effects.','paired_delta_missing_bounds':{'lower':(sum(int(x['correct']['matched'])-int(x['correct']['cascade']) for x in details if x['complete'])-(n-complete))/n,'upper':(sum(int(x['correct']['matched'])-int(x['correct']['cascade']) for x in details if x['complete'])+(n-complete))/n},'details':details}

def admit(receipt,stage,plan_sha256,now):
    if stage not in LIMITS:raise ValueError('invalid_stage')
    required=('owner_plan_approved','public_plan_verified','exclusive_claim_verified','workload_verified','account_verified','source_verified','model_verified','original_ledger_verified')
    if any(receipt.get(k) is not True for k in required):raise ValueError('missing_admission_evidence')
    if receipt.get('plan_sha256')!=plan_sha256 or receipt.get('approval_plan_sha256')!=plan_sha256:raise ValueError('plan_drift')
    if receipt.get('stage')!=stage or not 0<=now-receipt.get('checked_epoch',0)<=300:raise ValueError('stale_or_wrong_stage')
    if receipt.get('cumulative_call_cap')!=2671 or receipt.get('cumulative_usd_cap')!=.10 or receipt.get('incremental_usd_cap')!=.03:raise ValueError('wrong_budget')
    spent=receipt.get('spent_usd',math.inf);uncertain=receipt.get('uncertain_usd',math.inf)
    projected=receipt.get('projected_stage_usd',math.inf);incremental=receipt.get('incremental_spent_usd',math.inf)
    if not all(math.isfinite(x) and x>=0 for x in (spent,uncertain,projected,incremental)):raise ValueError('invalid_budget')
    if spent+uncertain+projected>.10 or incremental+projected>.03:raise ValueError('insufficient_budget')
    if receipt.get('ledger_entries',2672)+LIMITS[stage]['jev']>2671:raise ValueError('insufficient_slots')
    if receipt.get('claim_expires_epoch',0)<now+(1200 if stage=='S0' else 3900):raise ValueError('claim_too_short')
    if stage=='S1' and (receipt.get('s0_qualified') is not True or receipt.get('s0_scientific_hash')!=receipt.get('scientific_hash')):raise ValueError('unqualified_instrument')
    return True

def qualify(rows):
    if len(rows)!=60 or len({r['id'] for r in rows})!=60:return {'qualified':False,'reason':'wrong_assignment'}
    totals={l:sum(r['expected']==l for r in rows) for l in LABELS}
    if any(n!=20 for n in totals.values()):return {'qualified':False,'reason':'unbalanced_assignment'}
    complete=all(r.get('status')=='completed' and all(r.get('labels',{}).get(k) in LABELS for k in ('a','b','jev')) for r in rows)
    correct={l:sum(r.get('labels',{}).get('jev')==l for r in rows if r['expected']==l) for l in LABELS}
    return {'qualified':complete and sum(correct.values())>=51 and min(correct.values())>=14,'complete_valid':complete,'jev_correct':correct,'overall_correct':sum(correct.values()),'required_overall':51,'required_per_class':14}
