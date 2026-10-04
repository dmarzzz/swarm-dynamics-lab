"""RD7 authored development diagnostic and actor-visible eligibility controller."""
from copy import deepcopy
import hashlib
import importlib.util
import json
from pathlib import Path
import random

BASE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('rd6_case_definitions',BASE.parent/'reopening/cases.py')
prior=importlib.util.module_from_spec(spec);spec.loader.exec_module(prior)
digest=prior.digest
CONDITIONS=('R0','R1','E0','E1')
SEED=71004


def eligibility(request):
    """No content interpretation or evaluator access; metadata from actor input."""
    task=request['state']['task'];rows=[]
    for r in request['state']['observations']:
        age=task['now']-r['observed_at']
        matches_scope=r['scope']==task['scope'];matches_revision=r['revision']==task['revision']
        rows.append({'acquisition_id':r['acquisition_id'],'root':r['root'],'age':age,'ttl':task['ttl'],
                     'scope_matches':matches_scope,'revision_matches':matches_revision,
                     'eligible':matches_scope and matches_revision and 0<=age<=task['ttl']})
    return {'observations':rows,'eligible_observation_count':sum(x['eligible'] for x in rows),
            'rule':'Only scope/revision-matching observations with 0 <= age <= ttl are current evidence.'}


def gate(request):
    """Practical no-evidence guard; keep rejected facts in a separate audit."""
    checked=eligibility(request);req=deepcopy(request)
    ids={r['acquisition_id'] for r in checked['observations'] if r['eligible']}
    state=req['state'];rejected=[r for r in state['observations'] if r['acquisition_id'] not in ids]
    state['observations']=[r for r in state['observations'] if r['acquisition_id'] in ids]
    originals={r['acquisition_id']:r for r in request['state']['observations']}
    for card in state['evidence_cards']:
        original=originals.get(card['acquisition_id'])
        if original is None or any(card[k]!=original[k] for k in ('root','scope','revision','observed_at','text')):
            raise ValueError('card_source_mismatch')
    state['evidence_cards']=[r for r in state['evidence_cards'] if r['acquisition_id'] in ids]
    state.pop('evidence_eligibility',None)
    return {'action':'DEFER' if not ids else None,'model_required':bool(ids),'request':req,
            'audit':{'eligibility':checked,'rejected_observations':rejected}}


def reference(request):
    return prior.reference(request)


def build():
    cases=[];assignments=[]
    for domain in ('alarm','bridge','build'):
        for direction in ('stop','resume'):
            base=prior.make_case(domain,0,direction,True)
            for expired in (False,True):
                case=deepcopy(base);group='expired' if expired else 'fresh'
                case['id']=base['id']+'-'+group;case['root_id']=base['id'];case['group']=group
                case['records'][0]['observed_at']=91 if expired else 99
                case['expected']='DEFER' if expired else base['expected'];cases.append(case)
                for condition in CONDITIONS:
                    req=prior.request_for(case,'C11' if condition.endswith('1') else 'C00')
                    if condition.startswith('E'):req['state']['evidence_eligibility']=eligibility(req)
                    identity='F0-'+case['id']+'-'+condition
                    assignments.append({'id':identity,'stage':'F0','case':case['id'],'root':case['root_id'],
                        'family':case['family'],'domain':domain,'direction':direction,'group':group,
                        'condition':condition,'repeat':0,'expected':case['expected'],
                        'request_sha256':digest(req),'ordered_request_sha256':hashlib.sha256(json.dumps(req,separators=(',',':'),allow_nan=False).encode()).hexdigest(),
                        'request':req})
    random.Random(SEED).shuffle(assignments)
    return {'schema':'rd7-freshness-development-v1','seed':SEED,'native_dispatch':False,
        'claim':'Inspected authored development controls; 6 semantic roots, 12 task/age cases, 48 dependent requests.',
        'cases':cases,'assignments':assignments}


def score(manifest,observed,stage='F0'):
    if stage!='F0':raise ValueError('stage')
    assignments=manifest['assignments'];expected={a['id']:a for a in assignments};seen={}
    for r in observed:
        if r['id'] not in expected or r['id'] in seen:raise ValueError('unexpected_or_duplicate_outcome')
        a=expected[r['id']]
        if r['request_sha256']!=a['request_sha256'] or r['ordered_request_sha256']!=a['ordered_request_sha256']:raise ValueError('request_binding')
        if r['status'] not in ('completed','invalid','failed','unstarted'):raise ValueError('status')
        if r['status']=='completed' and r.get('action') not in ('PROCEED','HOLD','DEFER'):raise ValueError('action')
        if r['status']!='completed' and r.get('action') is not None:raise ValueError('failed_action_must_be_null')
        seen[r['id']]=r
    counts={};statuses={};values={};case_pairs=[]
    for a in assignments:
        r=seen.get(a['id'],{'status':'unstarted','action':None});valid=r['status']=='completed'
        statuses[r['status']]=statuses.get(r['status'],0)+1
        correct=int(r['action']==a['expected']) if valid else None;values[a['id']]=correct
        for key in (a['condition'],a['condition']+'/'+a['group'],a['condition']+'/'+a['domain']+'/'+a['direction']+'/'+a['group']):
            c=counts.setdefault(key,dict(assigned=0,valid=0,correct=0,wrong_PROCEED=0,unsupported_HOLD=0,unnecessary_DEFER=0))
            c['assigned']+=1;c['valid']+=int(valid);c['correct']+=correct or 0
            c['wrong_PROCEED']+=int(valid and r['action']=='PROCEED' and a['expected']!='PROCEED')
            c['unsupported_HOLD']+=int(valid and r['action']=='HOLD' and a['expected']=='DEFER')
            c['unnecessary_DEFER']+=int(valid and r['action']=='DEFER' and a['expected']!='DEFER')
    contrasts={}
    for group in ('fresh','expired'):
        for context in (0,1):
            pairs=[]
            for case in sorted({a['case'] for a in assignments if a['group']==group}):
                slots={a['condition']:a for a in assignments if a['case']==case}
                raw=values[slots['R'+str(context)]['id']];explicit=values[slots['E'+str(context)]['id']]
                low=(explicit or 0)-(1 if raw is None else raw)
                high=(1 if explicit is None else explicit)-(raw or 0)
                row={'case':case,'group':group,'context':context,'raw_correct':raw,'explicit_correct':explicit,'difference_bounds':[low,high]}
                case_pairs.append(row);pairs.append(row)
            contrasts[group+'/'+str(context)]={'paired_cases':len(pairs),'complete_pairs':sum(p['raw_correct'] is not None and p['explicit_correct'] is not None for p in pairs),
                'corrected':sum(p['raw_correct']==0 and p['explicit_correct']==1 for p in pairs),
                'harmed':sum(p['raw_correct']==1 and p['explicit_correct']==0 for p in pairs),
                'bounds':[sum(p['difference_bounds'][i] for p in pairs)/len(pairs) for i in (0,1)]}
    explicit_complete=all(counts[c]['valid']==12 and counts[c]['correct']==12 for c in ('E0','E1'))
    return {'stage':'F0','assigned':len(assignments),'provided_outcomes':len(seen),'statuses':statuses,'by_condition':counts,
        'paired_contrasts':contrasts,'pairs':case_pairs,'explicit_repair_signal':explicit_complete,
        'native_qualification':False,'native_evidence':False,'next_stage':'none',
        'note':'Finite diagnostic; a repair signal is not fresh qualification or field reliability. Native authenticity requires relay reconciliation.'}


def qualification_corpus(seed):
    """Reserve distinct synthetic qualification inputs; never dispatch here."""
    rng=random.Random(seed);out=[]
    variants=('inside','boundary','expired','future','wrong_scope','wrong_revision','mixed_stale','current_conflict','missing')
    for domain in ('alarm','bridge','build'):
        for direction in ('stop','resume'):
            for variant in variants:
                case=prior.make_case(domain,0,direction,True);token=hashlib.sha256(str(rng.getrandbits(192)).encode()).hexdigest()[:20]
                case['id']='reserved-'+token;case['task']['scope']=case['id'];case['task']['now']=rng.randrange(1000,9000)
                case['task']['deadline']=case['task']['now']+1;case['task']['horizon']=case['task']['now']+8
                rec=case['records'][0];rec.update(scope=case['id'],acquisition_id=token+'-a',root=token+'-a',observed_at=case['task']['now']-6)
                if domain=='alarm':rec['text']='The current process reading is '+str(rng.choice([11,12,14,17,24,28,29] if direction=='resume' else [31,34,39,42,47]))+'.'
                if domain=='bridge':rec['text']='The certified load limit is '+str(rng.choice([21,22,24,25,28,31] if direction=='resume' else [9,11,13,15,17,18]))+' tonnes.'
                if variant in ('boundary','expired','future'):rec['observed_at']=case['task']['now']-{'boundary':7,'expired':8,'future':-1}[variant]
                if variant=='wrong_scope':rec['scope']='other-'+token
                if variant=='wrong_revision':rec['revision']='v0'
                if variant in ('mixed_stale','current_conflict'):
                    other=prior.make_case(domain,0,'stop' if direction=='resume' else 'resume',True)['records'][0]
                    other.update(scope=case['id'],acquisition_id=token+'-b',root=token+'-b',observed_at=case['task']['now']-(8 if variant=='mixed_stale' else 6))
                    case['records'].append(other)
                if variant=='missing':case['records']=[]
                expected=case['expected'] if variant in ('inside','boundary','mixed_stale') else 'DEFER'
                req=prior.request_for(case,'C00');req['state']['evidence_eligibility']=eligibility(req)
                out.append({'id':case['id'],'variant':variant,'domain':domain,'direction':direction,'request':req,'expected':expected})
    rng.shuffle(out);return out
