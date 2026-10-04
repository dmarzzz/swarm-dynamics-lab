"""Typed construction labels; no parser used by this generator."""
import random,copy
FAMILIES=['timelines','entities','corrections','decimal_units','plans']
def build(seed,per_family=4,stage='evaluation'):
 rng=random.Random(seed);rows=[]
 for family_index,family in enumerate(FAMILIES):
  for n in range(per_family):
   root=''.join(rng.choices('abcdef0123456789',k=16));entity='asset-'+str(rng.randrange(100000,999999));time=f'{rng.randrange(10,20):02}:{rng.randrange(60):02}'
   prop='mass_g' if family in ['decimal_units','plans'] else 'running';positive=(n if per_family>1 else family_index)%2==0;observed=n%4<2 if per_family>1 else family_index%2==0
   threshold=5000 if prop=='mass_g' else 1
   value=((6000 if positive else 3000)+rng.randrange(1,10)*25) if prop=='mass_g' else int(positive);wrong=value+500 if prop=='mass_g' else 1-value
   def sentence(v,e=entity,t=time,alt=False,mode='ASSERTION'):
    prefix={'ASSERTION':'','HEDGE':'Unconfirmed: ','PLAN':'Plan: '}[mode]
    if prop=='running':verb=('was ' if mode!='PLAN' else 'will be ')+(('operating' if v else 'not running') if alt else ('running' if v else 'stopped'))
    else:verb=('measured ' if mode!='PLAN' else 'will measure ')+(f'{v/1000:g} kilograms' if alt else f'{v} grams')
    return prefix+f'At {t}, {e} {verb}.'
   def fact(v,quote,e=entity,t=time,mode=None):
    f=dict(entity=e,time=t,property=prop,value=v,status='unknown' if v is None else 'observed',quote=quote)
    if mode:f['mode']=mode
    return f
   sources=[];sg={}
   for j,v in enumerate([value,7000 if prop=='mass_g' else 1,2000 if prop=='mass_g' else 0]):
    sid='s'+str(j);selected=sentence(v,alt=True);text=selected
    if j==0:
     if not observed:selected=sentence(wrong,mode='PLAN');text=selected;v=None
     elif family=='timelines':text=sentence(wrong,t='09:00')+'\n'+selected
     elif family=='entities':text=sentence(wrong,e=entity+'-other')+'\n'+selected
     elif family=='corrections':text='Initial: '+sentence(wrong)+'\nCorrection: '+selected
     elif family=='plans':text=sentence(wrong,mode='PLAN')+'\nObservation: '+selected
    sources.append(dict(id=sid,independent_group=sid,text=text));sg[sid]=fact(v,selected)
   reports=[];rg={};labels={};changed=None
   for k,(v,e,alt,mode) in enumerate([(value,entity,False,'ASSERTION'),(value,entity,True,'ASSERTION'),(wrong,entity,False,'ASSERTION'),(value,entity+'-unseen',False,'ASSERTION'),(value,entity,False,'HEDGE'),(value,entity,False,'PLAN')]):
    rid='r'+''.join(rng.choices('abcdef0123456789',k=8));selected=sentence(v,e=e,alt=alt,mode=mode);text=selected
    if family=='entities' and k<3:text=sentence(wrong,e=entity+'-other')+' '+selected
    reports.append(dict(id=rid,source_id='s0',text=text));rg[rid]=fact(v,selected,e=e,mode=mode)
    labels[rid]='NOT_ESTABLISHED' if not observed or e!=entity or mode!='ASSERTION' else ('SUPPORTED' if v==value else 'CONTRADICTED')
    if k==2:changed=rid
   for copies in [1,3]:
    rr=copy.deepcopy(reports);gg=copy.deepcopy(rg);ll=labels.copy()
    for z in range(copies-1):
     original=next(r for r in reports if r['id']==changed);rid=changed+'c'+str(z);rr.append(original|{'id':rid});gg[rid]=copy.deepcopy(rg[changed]);ll[rid]=labels[changed]
    rng.shuffle(rr)
    actor={'contract':'Sources are authenticated, independent across groups, and counted once. Query-matching explicit corrections replace initial observations. Plans are not observations. Operating=running; not running=stopped. Extract report ASSERTION/HEDGE/PLAN and its value independently of source support; an Unconfirmed clause is HEDGE. Select the query-matching clause in multi-claim reports; retain a sole unmatched claim. Only ASSERTION can establish an observation. No two agreeing observed sources means DEFER.','query':dict(entity=entity,time=time,property=prop,threshold=threshold),'sources':copy.deepcopy(sources),'reports':rr}
    rows.append(dict(id=root+'-'+str(copies),root=root,stage=stage,family=family,condition={'copies':copies,'source_observed':observed},actor=actor,gold={'sources':copy.deepcopy(sg),'reports':gg,'labels':ll,'decision':('ONE' if positive else 'ZERO') if observed else 'DEFER'}))
 rng.shuffle(rows);return rows
