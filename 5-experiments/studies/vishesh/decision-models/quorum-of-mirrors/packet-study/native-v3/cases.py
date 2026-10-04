"""Typed construction oracle; fresh instances share six declared grammar families."""
import random,copy
FAMILIES=['polarity','time','entity','units','modality','correction']
def fact(entity,time,prop,value,quote):return dict(entity=entity,time=time,property=prop,value=value,status='unknown' if value is None else 'observed',quote=quote)
def build(seed):
 rng=random.Random(seed);rows=[]
 for family in FAMILIES:
  for variant in range(2):
   root=''.join(rng.choices('abcdef0123456789',k=12));entity='device-'+str(rng.randrange(10000,99999));time=f'{rng.randrange(10,18)}:00';prop='mass_g' if family=='units' else 'running';threshold=5000 if prop=='mass_g' else 1
   # Both mass roots include a true changed value on the same side of threshold.
   base=(6000 if variant else 3000) if prop=='mass_g' else variant
   values=[base,base,(2000 if variant else 7000) if prop=='mass_g' else 1-variant]
   def sentence(v,e=entity,t=time,alternate=False):
    if prop=='mass_g':return f'At {t}, {e} measured {v//1000} kilograms.' if alternate else f'At {t}, {e} measured {v} grams.'
    state=('operating' if v else 'not running') if alternate else ('running' if v else 'stopped')
    return f'At {t}, {e} was {state}.'
   sources=[];sg={}
   for j,v in enumerate(values):
    sid='s'+str(j);selected=sentence(v,alternate=True);text=selected;gv=v
    opposite=1-v if prop=='running' else v+1000
    if family=='time':text=sentence(opposite,t='08:00')+'\n'+selected
    if family=='entity':text=sentence(opposite,e=entity+'-other')+'\n'+selected
    if family=='modality':
     text=f'Plan: at {time}, {entity} will be '+('running.' if opposite else 'stopped.')+'\nObservation: '+selected
     if variant==1 and j==2:text=text.split('\n')[0];selected=text;gv=None
    if family=='correction':text='Initial: '+sentence(opposite)+'\nCorrection: '+selected
    sources.append({'id':sid,'independent_group':sid,'text':text});sg[sid]=fact(entity,time,prop,gv,selected)
   # Four deliberate types. The unknown type is a different target; one root also has missing source evidence.
   supported=values[0];wrong=(supported+1000) if prop=='mass_g' else 1-supported
   report_specs=[(sentence(supported),fact(entity,time,prop,supported,sentence(supported)),'SUPPORTED'),(sentence(supported,alternate=True),fact(entity,time,prop,supported,sentence(supported,alternate=True)),'SUPPORTED'),(sentence(wrong),fact(entity,time,prop,wrong,sentence(wrong)),'CONTRADICTED')]
   unknown_text=sentence(supported,e=entity+'-unseen')
   report_specs.append((unknown_text,fact(entity+'-unseen',time,prop,supported,unknown_text),'NOT_ESTABLISHED'))
   if family=='modality' and variant==1:
    unknown_text=sentence(values[2]);report_specs[-1]=(unknown_text,fact(entity,time,prop,values[2],unknown_text),'NOT_ESTABLISHED')
   for copies in [1,3]:
    reports=[];rg={};labels={}
    for n,(text,f,label) in enumerate(report_specs):
     for _ in range(copies if n==2 else 1):
      rid='r'+''.join(rng.choices('abcdef0123456789',k=6));reports.append({'id':rid,'source_id':'s2' if family=='modality' and variant==1 and n==3 else 's0','text':text});rg[rid]=f;labels[rid]=label
    rng.shuffle(reports)
    actor={'contract':'Receipts are authenticated and independent across supplied groups. Resolve query observations; explicit corrections supersede initial entries. Operating=running; not running=stopped. Plans are not observations. Reports claim one observation and are bound to source_id. Missing evidence is not contradiction.','query':{'entity':entity,'time':time,'property':prop,'threshold':threshold},'sources':copy.deepcopy(sources),'reports':reports}
    # Majority from typed construction, not parser or comparator.
    known=[f['value']>=threshold for f in sg.values() if f['value'] is not None];target='ONE' if known.count(True)>=2 else 'ZERO' if known.count(False)>=2 else 'DEFER'
    rows.append({'id':root+'-'+str(copies),'root':root,'family':family,'condition':{'copies':copies},'actor':actor,'gold':{'sources':copy.deepcopy(sg),'reports':copy.deepcopy(rg),'labels':labels,'decision':target}})
 rng.shuffle(rows);return rows
