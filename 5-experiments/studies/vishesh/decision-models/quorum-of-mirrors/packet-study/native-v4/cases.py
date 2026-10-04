"""Four paired assertion/evidence roots; typed oracle independent of parser."""
import random,copy

def build(seed):
 rng=random.Random(seed);rows=[]
 for prop in ['running','mass_g']:
  for positive in [False,True]:
   root=''.join(rng.choices('abcdef0123456789',k=12));e='asset-'+str(rng.randrange(10000,99999));t=f'{rng.randrange(10,18)}:00';threshold=1 if prop=='running' else 5000
   value=int(positive) if prop=='running' else (6000 if positive else 3000);wrong=(1-value) if prop=='running' else value+1000
   def sent(v,entity=e,alt=False):
    if prop=='mass_g':return f'At {t}, {entity} measured {v//1000} kilograms.' if alt else f'At {t}, {entity} measured {v} grams.'
    return f"At {t}, {entity} was {('operating' if v else 'not running') if alt else ('running' if v else 'stopped')}."
   def f(v,q,entity=e):return dict(entity=entity,time=t,property=prop,value=v,status='unknown' if v is None else 'observed',quote=q)
   plan=f'Plan: at {t}, {e} will '+(('be running.' if wrong else 'be stopped.') if prop=='running' else f'measure {wrong} grams.')
   report_specs=[(value,e,False,'SUPPORTED'),(value,e,True,'SUPPORTED'),(wrong,e,False,'CONTRADICTED'),(value,e+'-unseen',False,'NOT_ESTABLISHED')]
   reports=[];rg={};labels={}
   for v,entity,alt,label in report_specs:
    rid='r'+''.join(rng.choices('abcdef0123456789',k=6));text=sent(v,entity,alt);reports.append({'id':rid,'source_id':'s0','text':text});rg[rid]=f(v,text,entity);labels[rid]=label
   rng.shuffle(reports)
   for observed in [True,False]:
    sources=[];sg={}
    values=[value,1 if prop=='running' else 7000,0 if prop=='running' else 2000]
    for j,v in enumerate(values):
     sid='s'+str(j);selected=sent(v,alt=True);text=selected
     if j==0:
      text=plan+'\nObservation: '+selected if observed else plan
      if not observed:v=None;selected=plan
     sources.append({'id':sid,'independent_group':sid,'text':text});sg[sid]=f(v,selected)
    actor={'contract':'Sources are authenticated and independent across supplied groups. Plans are not observations. Operating=running and not running=stopped. Each report asserts a definite observation: extract what it claims separately from whether its bound source supports it. Count only observed sources, once each. Without two agreeing observed sources, decision is DEFER.','query':{'entity':e,'time':t,'property':prop,'threshold':threshold},'sources':sources,'reports':copy.deepcopy(reports)}
    rows.append({'id':root+('-observed' if observed else '-plan'),'root':root,'family':prop+('-positive' if positive else '-negative'),'condition':{'source_observed':observed},'actor':actor,'gold':{'sources':sg,'reports':copy.deepcopy(rg),'labels':labels.copy() if observed else {i:'NOT_ESTABLISHED' for i in labels},'decision':('ONE' if positive else 'ZERO') if observed else 'DEFER'}})
 rng.shuffle(rows);return rows
