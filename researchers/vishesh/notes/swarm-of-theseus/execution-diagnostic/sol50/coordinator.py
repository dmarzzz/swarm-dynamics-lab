"""Deterministic private-context scheduling, with an injected native-call function.
The injected function must perform admission, durable reservation and trace capture.
This module neither holds credentials nor provides an ungated network entry point.
"""
import copy,json
import instrument as i
import native as n
KINDS=('allow','veto','missing','stale','conflict','irrelevant_veto')

def initialize(w,call):
    states={};grades=[]
    for p in w['members']:
        packet,cases=n.founder_packet(w,p);value=call('learn',packet)
        grades.append({'position':p,**n.grade_founder(value,w,p,cases)})
        if isinstance(value,dict):states[p]=copy.deepcopy(value.get('note'))
    return states,grades

def replace(g,p,call,changed=False,require_teacher=False):
    old=g.identity(p);inherited=copy.deepcopy(g.notes.get(p));teaching=None;inspection=None
    if g.arm=='interactive':
        question=call('question',{'position':p,'successor_identity':f'{p}/g{g.generation[p]+1}','inherited_note':inherited})
        q=question.get('question') if isinstance(question,dict) else None
        if not isinstance(q,str) or len(q)>400:raise ValueError('question_contract')
        teaching=call('teach',n.teach_packet(g,p,question=q))
    elif g.arm=='static':
        teaching=call('teach',n.teach_packet(g,p))
        inspection=call('question',{'position':p,'inherited_note':inherited,'mode':'private_self_inspection_not_sent_to_teacher'})
        if not isinstance(inspection,dict) or not isinstance(inspection.get('question'),str) or len(inspection['question'])>400:raise ValueError('inspection_contract')
    elif g.arm!='broken':raise ValueError('invalid_replacement_arm')
    # Teacher semantic defects are outcomes, not hidden repairs. Never inject truth.
    teacher_ok=None if teaching is None else n.qualified_teacher(teaching,g.world,p,changed)
    if require_teacher and teacher_ok is not True:raise ValueError('qualification_teacher_semantics')
    g.replace(p,None)
    packet=g.actor(p)
    if g.arm!='broken':packet.update(inherited_note=inherited,predecessor_message=teaching)
    if inspection is not None:packet['private_self_inspection']=inspection
    result=call('commit',packet)
    if isinstance(result,dict):g.notes[p]=copy.deepcopy(result.get('note'))
    return {'retired':old,'successor':g.identity(p),'teacher_semantics_correct':teacher_ok,'behavior_evaluated_at_checkpoint':True,'note_correct':i.valid_note(g.notes.get(p),p,i.route_at(g.world,p,changed))}

def checkpoint(g,index,call,changed=False,owners=None):
    w=g.world;owners=owners or w['members'];selections={};cases={};inboxes={p:[] for p in w['members']};events=[];overflow=[]
    for owner in owners:
        new=i.examples(w,owner,True) if changed and w['routes'][owner]!=w['changed_routes'][owner] else []
        packet=g.actor(owner,current=new);value=call('select',packet)
        peers=value.get('witnesses') if isinstance(value,dict) else None
        good=isinstance(peers,list) and len(peers)==2 and len(set(peers))==2 and all(p in w['members'] and p!=owner for p in peers)
        selections[owner]=peers if good else []
        if isinstance(value,dict) and isinstance(value.get('note'),dict):g.notes[owner]=copy.deepcopy(value['note'])
        cases[owner]=[i.challenge(w,owner,index,k,changed) for k in KINDS]
        for peer in selections[owner]:
            observations=[]
            for c in cases[owner]:
                rows=[r for r in c['receipts'] if r['witness']==peer]
                if peer not in i.route_at(w,owner,changed):rows=[i.receipt(owner,peer,c['case'],c['epoch'],True)]
                observations.extend({k:r[k] for k in ('case','epoch','allow')} for r in rows)
            if len(inboxes[peer])<2:inboxes[peer].append({'owner':owner,'observations':observations})
            else:overflow.append({'owner':owner,'witness':peer,'reason':'two_request_attention_capacity'})
        events.append({'phase':'select','owner':owner,'valid':good,'route_correct':good and set(peers)==set(i.route_at(w,owner,changed)),'selected':selections[owner]})
    received={p:[] for p in owners};witness_audit=[]
    for peer in w['members']:
        if not inboxes[peer]:continue
        packet=g.actor(peer);packet['private_inbox']=inboxes[peer]
        value=call('attest',packet);rows=value.get('reports',[]) if isinstance(value,dict) else []
        exact=rows==inboxes[peer];witness_audit.append({'witness':peer,'copied_exactly':exact})
        # Native output is delivered as returned; signer is established by transport.
        # Wrong values are scored, not replaced with true private observations.
        if not isinstance(rows,list):rows=[]
        permitted={row['owner'] for row in inboxes[peer]}
        for row in rows:
            if not isinstance(row,dict) or row.get('owner') not in permitted or not isinstance(row.get('observations'),list):continue
            for obs in row['observations']:
                if isinstance(obs,dict) and set(obs)=={'case','epoch','allow'} and type(obs['epoch']) is int and type(obs['allow']) is bool:
                    received[row['owner']].append(i.receipt(row['owner'],peer,obs['case'],obs['epoch'],obs['allow']))
    results=[]
    for owner in owners:
        packet=g.actor(owner);packet['cases']=[{'case':c['case'],'epoch':c['epoch']} for c in cases[owner]];packet['received_receipts']=received[owner]
        value=call('decide',packet);score=n.score_actions(value,cases[owner]);results.append({'owner':owner,**score})
    return {'checkpoint':index,'arm':g.arm,'active_members':len(w['members']),'founders_remaining':sum(x==0 for x in g.generation.values()),'selections':events,'witnesses':witness_audit,'attention_overflow':overflow,'decisions':results}

def evaluate_world(w,call):
    founding,grades=initialize(w,call);out={'founders':grades,'arms':{},'qualification_passed':all(g['qualified'] for g in grades)}
    if not out['qualification_passed']:return out
    for arm in ('interactive','static','broken','retained'):
        g=i.Institution(w,arm,copy.deepcopy(founding));history=[checkpoint(g,0,call)];handovers=[]
        for number,p in enumerate(w['replacement_order'],1):
            if arm!='retained':handovers.append(replace(g,p,call))
            if number in (len(w['members'])//2,len(w['members'])):history.append(checkpoint(g,number,call,changed=number==len(w['members'])))
        out['arms'][arm]={'checkpoints':history,'handovers':handovers,'events':g.events}
    out['controller']=[controller_reference(w,founding,k,changed=k==len(w['members'])) for k in (0,len(w['members'])//2,len(w['members']))]
    return out

def controller_reference(w,founding_notes,checkpoint_index,changed=False):
    """Strong simple controller, using learned notes rather than hidden routing.
    This is a deterministic architecture comparator, never native evidence.
    """
    memory=copy.deepcopy(founding_notes);results=[]
    for owner in w['members']:
        if changed and w['routes'][owner]!=w['changed_routes'][owner]:
            memory=i.selective_update(memory,owner,i.examples(w,owner,True))
        required=memory.get(owner,{}).get('witnesses',[])
        cases=[i.challenge(w,owner,checkpoint_index,k,changed) for k in KINDS]
        actions=[]
        for case in cases:
            receipts=[]
            for peer in required:
                records=[r for r in case['receipts'] if r['witness']==peer]
                if peer not in i.route_at(w,owner,changed):records=[i.receipt(owner,peer,case['case'],case['epoch'],True)]
                receipts.extend(records)
            action=i.reference(required,receipts,owner,case['case'],case['epoch']) if len(set(required))==2 else 'defer'
            actions.append({'case':case['case'],'action':action})
        results.append({'owner':owner,**n.score_actions({'actions':actions},cases)})
    return {'evidence_type':'deterministic_controller_from_learned_founder_notes','checkpoint':checkpoint_index,'decisions':results,'model_calls':0}
