"""Authored synthetic development fixtures and deterministic mapping controls. No models."""
from collections import defaultdict
import hashlib,json,re,unicodedata
from pathlib import Path
HERE=Path(__file__).resolve().parent
PAIRS=[
 ('At dawn the access gate was unobstructed.','At sunrise the entry barrier was clear.','At sunrise the entry barrier was blocked.'),
 ('The container was vacant after unloading.','The vessel was empty after unloading.','The vessel was full after unloading.'),
 ('The motor ceased rotating during inspection.','The engine stopped turning during inspection.','The engine continued turning during inspection.'),
 ('The inlet remained shut during the check.','The intake stayed closed during the check.','The intake stayed open during the check.'),
 ('The pipe emitted no fluid at midday.','The conduit released no liquid at noon.','The conduit released liquid at noon.'),
 ('The warning lamp was illuminated before departure.','The alert light was lit before departure.','The alert light was dark before departure.')]
SYNONYMS={'dawn':'sunrise','access':'entry','gate':'barrier','unobstructed':'clear','container':'vessel','vacant':'empty',
 'motor':'engine','ceased':'stopped','rotating':'turning','inlet':'intake','remained':'stayed','shut':'closed',
 'pipe':'conduit','emitted':'released','fluid':'liquid','midday':'noon','warning':'alert','lamp':'light','illuminated':'lit'}


def tokens(text,semantic=False):
    words=re.findall(r'[a-z0-9]+',unicodedata.normalize('NFKC',text).lower())
    return [SYNONYMS.get(w,w) if semantic else w for w in words]


def bundles():
    output=[]
    for family in ('paraphrase','identical_independent','missing','common_cause'):
        for i,(report,positive,negative) in enumerate(PAIRS):
            event=f'event-{family}-{i}'
            target_id=f'R{i%3}';other_id=f'R{(i+1)%3}'
            candidates=[{'id':target_id,'event':event,'capture':'capture-a','text':positive,'acquisition':'a','dependency_group':'new'},
                        {'id':other_id,'event':event,'capture':'capture-b','text':negative,'acquisition':'b','dependency_group':'other'},
                        {'id':f'R{(i+2)%3}','event':event+'-old','capture':'capture-c','text':positive,'acquisition':'c','dependency_group':'old'}]
            query={'text':report,'event':event};expected=target_id;expected_new=True
            if family=='identical_independent':
                query['text']=positive;candidates[1]['text']=positive
                if i%2==0:query['capture']='capture-a'
                else:expected=None;expected_new=False
            elif family=='missing':query['event']=event+'-unrecorded';expected=None;expected_new=False
            elif family=='common_cause':
                query['receipt_ref']=target_id;query['text']=positive
                candidates[0]['dependency_group']=candidates[1]['dependency_group']='known-cause'
                expected_new=False
            candidates.sort(key=lambda c:hashlib.sha256(f"{family}:{i}:{c['id']}".encode()).hexdigest())
            actor={'report':query,'receipts':candidates,'known_dependency_groups':['old','known-cause'],
                   'registry_scope':'fixture assumes authenticated receipts and supplied dependence groups'}
            output.append({'id':f'{family}-{i}','family':family,'evidence_type':'authored synthetic development; not held out or native',
                'actor':actor,'expected_receipt':expected,'expected_new_group':expected_new})
    return output


def resolve(actor,policy):
    report=actor['report'];candidates=actor['receipts']
    if policy not in ('exact_ref','normalized_text','lexical','hybrid'):raise ValueError('unknown_policy')
    if policy in ('exact_ref','hybrid') and report.get('receipt_ref'):
        matches=[r for r in candidates if r['id']==report['receipt_ref'] and r['event']==report['event']]
        return matches[0]['id'] if len(matches)==1 else None
    if policy=='exact_ref':return None
    candidates=[r for r in candidates if r['event']==report['event'] and ('capture' not in report or r['capture']==report['capture'])]
    if not candidates:return None
    query=tokens(report['text'],policy=='hybrid')
    if policy in ('normalized_text','hybrid'):
        matches=[r for r in candidates if tokens(r['text'],policy=='hybrid')==query]
        return matches[0]['id'] if len(matches)==1 else None
    scores=[]
    for r in candidates:
        terms=set(tokens(r['text']));q=set(query)
        scores.append((len(terms&q)/len(terms|q) if terms|q else 0,r['id']))
    scores.sort(reverse=True)
    return scores[0][1] if scores[0][0]>=.5 and (len(scores)==1 or scores[0][0]-scores[1][0]>=.2) else None


def new_group(actor,receipt):
    if receipt is None:return False
    record=next(r for r in actor['receipts'] if r['id']==receipt)
    group=record.get('dependency_group')
    return bool(group) and group not in actor['known_dependency_groups']


def evaluate(rows):
    outcomes=[];summary={}
    for policy in ('exact_ref','normalized_text','lexical','hybrid'):
        counts=defaultdict(int)
        for row in rows:
            got=resolve(row['actor'],policy);new=new_group(row['actor'],got)
            item={'id':row['id'],'family':row['family'],'policy':policy,'expected_receipt':row['expected_receipt'],
                'receipt':got,'correct':got==row['expected_receipt'],'incorrect_admission':got is not None and got!=row['expected_receipt'],
                'false_new_group':new and not row['expected_new_group'],'new_group':new}
            outcomes.append(item);counts['assigned']+=1;counts['correct']+=item['correct'];counts['resolvable']+=row['expected_receipt'] is not None
            counts['resolved_correct']+=got is not None and got==row['expected_receipt'];counts['incorrect_admissions']+=item['incorrect_admission']
            counts['false_new_groups']+=item['false_new_group'];counts['abstentions']+=got is None
        summary[policy]=dict(counts)
    return {'scope':'development only; hybrid synonyms chosen from these six templates, hence optimistic in-sample fit',
            'bundles':24,'template_families':4,'summary':summary,'outcomes':outcomes}


def main():
    rows=bundles();result=evaluate(rows)
    (HERE/'development-bundles.json').write_text(json.dumps(rows,indent=2)+'\n')
    (HERE/'baseline-results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result['summary'],indent=2))
if __name__=='__main__':main()
