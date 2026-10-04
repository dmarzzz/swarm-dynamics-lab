"""Authored development cases; actor records and evaluator witnesses stay separate."""
import copy, hashlib, json
LABELS=('YES','NO','UNKNOWN')
FAMILIES=('restore','version','provenance','check','rollback','consent','permission','exception')
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
def sha(x):return hashlib.sha256(canonical(x).encode()).hexdigest()

def specification(f,label,name):
    # The witness vocabulary belongs to source evidence, not an actor answer field.
    data={
      'restore':('Does the recorded restore test establish successful recovery?',
        {'YES':'Recovery probe: succeeded.','NO':'Recovery probe: failed.','UNKNOWN':'Recovery probe: no result available.'}),
      'version':('Is revision v3 the currently deployed revision?',
        {'YES':'Deployment at 10:20: v3.','NO':'Deployment at 10:20: v2; v3 is proposed only.','UNKNOWN':'Deployment at 10:20: revision unrecorded; v3 is proposed.'}),
      'provenance':('Do the two reports represent independent acquisitions?',
        {'YES':'Report A acquisition: alpha; report B acquisition: beta; these are distinct collections.',
         'NO':'Report A acquisition: alpha; report B acquisition: alpha; the same collection is reused.',
         'UNKNOWN':'Report A acquisition: alpha; report B acquisition: identifier unavailable; independence unresolved.'}),
      'check':('Does the evidence establish that the required integrity check passed?',
        {'YES':'Integrity check outcome: passed.','NO':'Integrity check outcome: failed.','UNKNOWN':'Integrity check outcome: not recorded; it was performed.'}),
      'rollback':(f'Was rollback tested for {name}-west?',
        {'YES':f'Rollback coverage: {name}-east and {name}-west tested.',
         'NO':f'Rollback coverage: {name}-east tested; {name}-west explicitly untested.',
         'UNKNOWN':f'Rollback coverage: {name}-east tested; {name}-west status not recorded.'}),
      'consent':('Did the actual recorded consent scope include analytics?',
        {'YES':'Effective consent scope: operations and analytics.',
         'NO':'Effective consent scope: operations only; analytics excluded.',
         'UNKNOWN':'Effective consent scope: receipt unavailable; analytics was suggested.'}),
      'permission':('Is analytics export authorized by the recorded permission and its scope?',
        {'YES':'Export authorization: granted, receipt E7 recorded; its scope explicitly includes analytics.',
         'NO':'Export authorization: granted, receipt E7 recorded; operations only, analytics excluded.',
         'UNKNOWN':'Export authorization: granted, receipt E7 recorded; scope receipt unavailable.'}),
      'exception':('Does the exception cover every deployment site?',
        {'YES':'Exception coverage: all deployment sites.',
         'NO':f'Exception coverage: {name}-east only; other deployment sites excluded.',
         'UNKNOWN':'Exception coverage: signed scope unavailable; universal coverage not established.'})}
    return data[f][0],data[f][1][label]

def make(f,label,index):
    name=('Aster','Birch','Coral','Dune','Ember','Fjord','Grove','Harbor')[index//3]+str(index+1)
    question,witness=specification(f,label,name)
    ready=index%2==0
    texts=[
      'The handoff release decision concerns only whether the current staging slot is ready: GO if ready, otherwise HOLD. Other observations must still be preserved for later colleagues.',
      'Current staging slot: '+('ready.' if ready else 'not ready.'),
      f'09:00 preliminary note for {name}: recovery unassessed, deployment v1, analytics suggested, and permission requested. Later entries supersede preliminary entries for their named fields only.',
      '10:20 authoritative observation: '+witness,
      f'{name} has two deployment sites, {name}-east and {name}-west. The next handover is 11:00.',
      'The latency threshold was corrected from 80 to 120 ms. A 100 ms read-only probe passed; no write-path measurement is supplied.',
      'A monitor is proposed for the next shift; it has not been started. Suggestions and requests are not evidence of completed actions.',
      ('Export requires both a recorded grant and scope explicitly covering analytics. A request alone or an operations-only grant is insufficient.' if f=='permission' else 'Preserve the distinction between an explicitly negative result and unavailable evidence. Do not infer a later action from an earlier proposal.')
    ]
    records=[{'id':f'e{i+1}','time':f'{i:02d}:00','text':t} for i,t in enumerate(texts)]
    # Position changes are fixed before outputs; chronology lives in explicit source text.
    shift=index%len(records);records=records[shift:]+records[:shift]
    cid=f'{f}-{label.lower()}'
    return {'id':cid,'family':f,'actor':{'records':records},'question':question,
            'gold':{'answer':label,'witness_id':'e4','witness':witness,'initial_decision':'GO' if ready else 'HOLD'},'name':name}

def cases():return [make(f,l,i*3+j) for i,f in enumerate(FAMILIES) for j,l in enumerate(LABELS)]

def reference(packet,question):
    """Exact source controller for this authored grammar, not free-prose grading."""
    lines=[r['text'] for r in packet['records']]
    matches=[x.split('10:20 authoritative observation: ',1)[1] for x in lines if x.startswith('10:20 authoritative observation: ')]
    if len(matches)!=1:raise ValueError('missing_or_conflicting_witness')
    w=matches[0]
    # Independently specified explicit vocabulary; UNKNOWN checked before positive tokens.
    if any(t in w for t in ('no result available','revision unrecorded','independence unresolved','not recorded','receipt unavailable','status not recorded','signed scope unavailable')):return 'UNKNOWN'
    if any(t in w for t in ('failed','Deployment at 10:20: v2','same collection is reused','explicitly untested','analytics excluded','authorization: denied','other deployment sites excluded')):return 'NO'
    if any(t in w for t in ('succeeded','Deployment at 10:20: v3','distinct collections','outcome: passed','-west tested','operations and analytics','authorization: granted','all deployment sites')):return 'YES'
    raise ValueError('outside_reference_grammar')

def mutation(c):
    x=copy.deepcopy(c);answer=LABELS[(LABELS.index(c['gold']['answer'])+1)%3]
    _,witness=specification(c['family'],answer,c['name'])
    for r in x['actor']['records']:
        if r['id']=='e4':r['text']='10:20 authoritative observation: '+witness
    x['gold'].update(answer=answer,witness=witness);return x

def assignments():
    out=[]
    for block in (1,2):
        ordered=cases() if block==1 else list(reversed(cases()))
        for ix,c in enumerate(ordered):
            for arm in (('P','R') if (ix+block)%2 else ('R','P')):
                chain=f'b{block}-{c["id"]}-{arm}'
                for hop in range(1,5):
                    out.append({'id':f'{chain}-h{hop}','chain':chain,'block':block,'case_id':c['id'],'family':c['family'],'arm':arm,'hop':hop,'role':'reader' if hop==4 else 'writer','parent':None if hop==1 else f'{chain}-h{hop-1}'})
    return out
