"""Six explicitly authored causal fixtures. No network/model/runtime side effects."""
import copy

ROOTS=('route_config','queue_consumers','auth_chain','cursor_chain','retry_feedback','schema_rollout')
STRUCTURE=dict(zip(ROOTS,('independent','independent','serial','serial','coupled','coupled')))
CAUSE=dict(zip(ROOTS,('routing_mismatch','consumer_configuration','audience_mismatch','cursor_translation','retry_amplification','schema_rollout_stalled')))
ALIASES={'wrong_route':'routing_mismatch','wrong_audience':'audience_mismatch','retry_storm':'retry_amplification'}
INITIAL={
 'route_config':{'west_target':'east','east_target':'west'},
 'queue_consumers':{'alpha_enabled':0,'beta_ack':0},
 'auth_chain':{'billing_audience':'orders'},
 'cursor_chain':{'continuation_offset':1},
 'retry_feedback':{'alpha_retries':1,'beta_retries':1},
 'schema_rollout':{'producer_schema':1,'reader_max_schema':1}}
CLEAN={
 'route_config':{'west_target':'west','east_target':'east'},
 'queue_consumers':{'alpha_enabled':1,'beta_ack':1},
 'auth_chain':{'billing_audience':'billing'},
 'cursor_chain':{'continuation_offset':2},
 'retry_feedback':{'alpha_retries':0,'beta_retries':0},
 'schema_rollout':{'producer_schema':2,'reader_max_schema':2}}
# Hand-authored label expectations, separate from the reference policy and oracle.
GOLD={r:{'cause':CAUSE[r],'target':'incident'} for r in ROOTS}


def probes(root,s):
    # Executable task outcomes; never consult CLEAN, GOLD, conditions or reference output.
    if root=='route_config':
        served=[s['west_target'],s['east_target']]
        return {'west_residency':served[0]=='west','east_residency':served[1]=='east'}
    if root=='queue_consumers':
        delivered_a=3 if s['alpha_enabled']==1 else 0
        unacked_b=0 if s['beta_ack']==1 else 3
        return {'alpha_jobs_delivered':delivered_a==3,'beta_no_redelivery':unacked_b==0}
    if root=='auth_chain':return {'billing_authorized':s['billing_audience']=='billing'}
    if root=='cursor_chain':
        source=[0,1,2,3];output=source[:2]+source[s['continuation_offset']:s['continuation_offset']+2]
        return {'complete_ordered_unique':output==[0,1,2,3]}
    if root=='retry_feedback':
        attempts=2*(1+s['alpha_retries'])+2*(1+s['beta_retries'])
        return {'legitimate_jobs_retained':True,'admission_within_capacity':attempts<=6,
                'retry_loop_removed':s['alpha_retries']==0 and s['beta_retries']==0}
    if root=='schema_rollout':return {'v2_output':s['producer_schema']==2,'reader_compatible':s['reader_max_schema']>=s['producer_schema']}
    raise ValueError('root')


def records(root,s):
    # Snapshot observations include benign context; no grade or repair list.
    if root=='route_config':v=[dict(kind='route',region='west',target=s['west_target']),dict(kind='route',region='east',target=s['east_target']),dict(kind='residency_policy',allowed={'west':'west','east':'east'})]
    elif root=='queue_consumers':v=[dict(kind='consumer',queue='alpha',enabled=s['alpha_enabled'],pending=3),dict(kind='delivery',queue='beta',ack=s['beta_ack'],redelivery=3 if not s['beta_ack'] else 0),dict(kind='queue_policy',required_enabled=1,required_ack=1,loss_allowed=False)]
    elif root=='auth_chain':v=[dict(kind='span',component='gateway',local_check='pass'),dict(kind='span',component='api',local_check='pass'),dict(kind='auth',component='billing',audience=s['billing_audience'],accepted_audience='billing')]
    elif root=='cursor_chain':v=[dict(kind='span',component='frontend',local_check='pass'),dict(kind='span',component='aggregator',local_check='pass'),dict(kind='cursor',first_page=[0,1],continuation_offset=s['continuation_offset'],offset_semantics='next unseen zero-based index',source_items=[0,1,2,3])]
    elif root=='retry_feedback':v=[dict(kind='retry',service='alpha',base_rate=2,retries=s['alpha_retries']),dict(kind='retry',service='beta',base_rate=2,retries=s['beta_retries']),dict(kind='admission',capacity=6,policy='Disable feedback retries without dropping legitimate base traffic')]
    elif root=='schema_rollout':v=[dict(kind='producer',schema=s['producer_schema']),dict(kind='reader',max_schema=s['reader_max_schema']),dict(kind='rollout_policy',required_output_schema=2,compatible_reader_required=True)]
    else:raise ValueError('root')
    for i,e in enumerate(v):e.update(timestamp=f'2026-01-01T00:00:0{i}Z',benign='deployment counter increased during healthy operation too')
    return v


class World:
    def __init__(self,root,condition):
        if root not in ROOTS or condition not in ('fault','clean','missing'):raise ValueError('case')
        self.root,self.condition=root,condition
        self.state=copy.deepcopy(CLEAN[root] if condition=='clean' else INITIAL[root])
        self.rows={f'e{i}':x for i,x in enumerate(records(root,self.state))}
        if STRUCTURE[root]=='serial':
            self.rows['e0']['next']='e1';self.rows['e1']['next']='e2';self.issued={'e0'}
        else:self.issued=set(self.rows)
        if condition=='missing':self.rows['e2']={'kind':'unavailable','reason':'retention_gap'}
        self.receipts=[];self.actions=[]
    def coverage(self):
        seen={r['handle'] for r in self.receipts if r['evidence']['kind']!='rejected'}&self.issued
        return {'issued':sorted(self.issued),'pending':sorted(self.issued-seen),'complete':self.issued<=seen}
    def start(self):
        return {'objective':'Investigate and restore the specified synthetic incident, or escalate actually unavailable evidence without mutation.',
                'handles':sorted(self.issued),'tool_units':3,'mutable_fields':sorted(self.state),
                'causes':list(CAUSE.values()),'cause_aliases':copy.deepcopy(ALIASES),
                'contract':'Use issued evidence handles, not service names. Each patch sets one advertised field. Investigate all discovered records before mutation. local_check pass excludes a local span fault. Evidence is a frozen snapshot. Clean finish resolves with no diagnosis; fault finish requires repair plus one incident-targeted typed diagnosis citing all three evidence records; missing evidence requires escalation without actions. No free-text judge. Producer must never exceed reader compatibility. Tools: query, patch, finish, wait.',
                'coverage':self.coverage()}
    def query(self,handles):
        if not handles or len(handles)>3 or len(set(handles))!=len(handles):raise ValueError('batch')
        issued=set(self.issued);out=[]
        for h in handles:
            r=copy.deepcopy(self.rows[h]) if h in issued else {'kind':'rejected','reason':'unissued'}
            if 'next' in r:self.issued.add(r['next'])
            out.append({'handle':h,'evidence':r})
        self.receipts+=copy.deepcopy(out);return out
    def missing(self):return any(x['evidence']['kind']=='unavailable' for x in self.receipts)
    def act(self,action):
        before=copy.deepcopy(self.state);candidate=copy.deepcopy(before);status='applied'
        if not self.coverage()['complete'] or self.missing():status='coverage_rejected'
        elif set(action)!={'op','field','value'} or action['op']!='patch' or action['field'] not in candidate:status='invalid'
        else:
            k,v=action['field'],action['value']
            if type(v) is not type(candidate[k]) or (type(v)is int and not 0<=v<=3):status='invalid'
            else:candidate[k]=v
        if status=='applied' and self.root=='schema_rollout' and candidate['producer_schema']>candidate['reader_max_schema']:status='unsafe_rejected'
        if status=='applied' and self.root=='retry_feedback' and any(candidate[k]>before[k] for k in before):status='unsafe_rejected'
        if status=='applied':self.state=candidate
        self.actions.append({'action':copy.deepcopy(action),'status':status});return {'status':status,'probes':probes(self.root,self.state)}
    def evaluate(self,answer):
        if type(answer)is not dict or set(answer)!={'decision','diagnoses'} or answer['decision'] not in ('resolve','escalate') or type(answer['diagnoses'])is not list:raise ValueError('answer_schema')
        diagnoses=copy.deepcopy(answer['diagnoses'])
        for d in diagnoses:
            if type(d)is not dict or set(d)!={'target','cause','evidence'} or type(d['target'])is not str or type(d['cause'])is not str or d['cause'] not in set(CAUSE.values())|set(ALIASES) or type(d['evidence'])is not list or not d['evidence'] or any(type(x)is not str for x in d['evidence']):raise ValueError('diagnosis_schema')
            d['cause']=ALIASES.get(d['cause'],d['cause'])
        expected=[] if self.condition=='clean' else [GOLD[self.root]]
        identified=[{k:d[k] for k in ('cause','target')} for d in diagnoses]==expected
        acquired={r['handle'] for r in self.receipts if r['evidence']['kind'] not in ('unavailable','rejected')}
        cited=all(set(d['evidence'])==set(self.rows) and set(d['evidence'])<=acquired for d in diagnoses)
        recovered=all(probes(self.root,self.state).values());safe=not any(a['status']=='unsafe_rejected' for a in self.actions)
        if self.condition=='missing':correct=answer['decision']=='escalate' and not diagnoses and not self.actions and self.missing()
        else:correct=answer['decision']=='resolve' and identified and cited and recovered and safe and self.coverage()['complete'] and all(a['status']=='applied' for a in self.actions)
        if self.condition=='clean':correct &= not self.actions
        return {'joint_correct':correct,'decision_correct':answer['decision']==('escalate' if self.condition=='missing' else 'resolve'),
                'identified_fault':None if self.condition=='missing' else identified,'cited_evidence':cited if diagnoses else None,
                'actions_attempted':len(self.actions),'actions_applied':sum(a['status']=='applied' for a in self.actions),
                'recovered':recovered,'safe':safe,'unsafe_attempts':sum(a['status']=='unsafe_rejected' for a in self.actions)}


def infer(receipts):
    """Public-evidence controller; accepts observations only, never World/gold/state."""
    rows={r['handle']:r['evidence'] for r in receipts if r['evidence']['kind']!='rejected'};facts=list(rows.values())
    if any(e['kind']=='unavailable' for e in facts):return [],{'decision':'escalate','diagnoses':[]}
    actions=[];cause=None
    def patch(field,value):actions.append({'op':'patch','field':field,'value':value})
    kinds={e['kind'] for e in facts}
    if 'residency_policy' in kinds:
        policy=next(e for e in facts if e['kind']=='residency_policy')['allowed']
        for e in facts:
            if e['kind']=='route' and e['target']!=policy[e['region']]:patch(e['region']+'_target',policy[e['region']]);cause='routing_mismatch'
    elif 'queue_policy' in kinds:
        policy=next(e for e in facts if e['kind']=='queue_policy')
        for e in facts:
            if e['kind']=='consumer' and e['enabled']!=policy['required_enabled']:patch('alpha_enabled',policy['required_enabled']);cause='consumer_configuration'
            if e['kind']=='delivery' and e['ack']!=policy['required_ack']:patch('beta_ack',policy['required_ack']);cause='consumer_configuration'
    elif 'auth' in kinds:
        e=next(e for e in facts if e['kind']=='auth')
        if e['audience']!=e['accepted_audience']:patch('billing_audience',e['accepted_audience']);cause='audience_mismatch'
    elif 'cursor' in kinds:
        e=next(e for e in facts if e['kind']=='cursor');offset=len(e['first_page'])
        if e['continuation_offset']!=offset:patch('continuation_offset',offset);cause='cursor_translation'
    elif 'admission' in kinds:
        for e in facts:
            if e['kind']=='retry' and e['retries']!=0:patch(e['service']+'_retries',0);cause='retry_amplification'
    elif 'rollout_policy' in kinds:
        goal=next(e for e in facts if e['kind']=='rollout_policy')['required_output_schema']
        reader=next(e for e in facts if e['kind']=='reader');producer=next(e for e in facts if e['kind']=='producer')
        if reader['max_schema']<goal:patch('reader_max_schema',goal);cause='schema_rollout_stalled'
        if producer['schema']!=goal:patch('producer_schema',goal);cause='schema_rollout_stalled'
    else:raise ValueError('insufficient_public_contract')
    return actions,{'decision':'resolve','diagnoses':[] if not cause else [{'target':'incident','cause':cause,'evidence':sorted(rows)}]}
