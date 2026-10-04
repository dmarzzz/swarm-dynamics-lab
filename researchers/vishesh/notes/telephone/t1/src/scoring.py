"""Aggregate reviewed semantic annotations. Does not infer semantics from raw prose."""
import hashlib
import json
from fractions import Fraction

FIELDS = ('entity','predicate','value_unit','time','scope','modality','attribution')
SUPPORT = {'supported','contradicted','unknown'}
STATUSES = {'scored','missing','invalid','unreviewed'}


def digest(value):
    return hashlib.sha256(json.dumps(value,sort_keys=True,ensure_ascii=False,separators=(',',':')).encode()).hexdigest()


def text_hash(text):
    return hashlib.sha256(text.encode()).hexdigest()


def validate_fact(fact):
    if not isinstance(fact,dict) or set(fact) != set(FIELDS):
        raise ValueError('seven canonical meaning fields required')
    if any(v is not None and not isinstance(v,str) for v in fact.values()):
        raise ValueError('canonical fields must be text or null')


def validate_gold(gold):
    if not isinstance(gold,dict) or not isinstance(gold.get('obligations'),list) or not gold['obligations']:
        raise ValueError('nonempty frozen obligation inventory required')
    ids=set()
    for item in gold['obligations']:
        if not isinstance(item.get('id'),str) or not item['id'] or item['id'] in ids:
            raise ValueError('duplicate or empty gold id')
        ids.add(item['id'])
        if not isinstance(item.get('acceptable'),list) or not item['acceptable']:
            raise ValueError('acceptable forms required')
        for variant in item['acceptable']:
            validate_fact(variant['fact'])
            if variant.get('support') not in SUPPORT:
                raise ValueError('unknown gold support')
    return {x['id']:x for x in gold['obligations']}


def score(text, review, gold, visible_source_ids):
    expected=validate_gold(gold)
    if text is None:
        if review is not None:
            raise ValueError('annotation without output')
        return {'status':'missing','retention':None}
    if not isinstance(text,str):
        return {'status':'invalid','retention':None}
    if review is None:
        return {'status':'unreviewed','retention':None}
    if review.get('reviewed') is not True or not review.get('review_id'):
        raise ValueError('completed annotation receipt required')
    if review.get('output_sha256') != text_hash(text) or review.get('gold_sha256') != digest(gold):
        raise ValueError('annotation binding mismatch')
    if not isinstance(review.get('claims'),list):
        raise ValueError('claim list required')
    # Annotation completeness is an attestation, not an automated semantic guarantee.
    if review.get('all_assertions_reviewed') is not True:
        raise ValueError('incomplete assertion review')
    dedup={}
    for claim in review['claims']:
        validate_fact(claim['fact'])
        oid=claim.get('obligation_id')
        if oid is not None and oid not in expected:
            raise ValueError('unknown obligation mapping')
        if claim.get('support') not in SUPPORT or not isinstance(claim.get('critical_addition'),bool):
            raise ValueError('invalid reviewed judgment')
        if not isinstance(claim.get('citations'),list) or not all(isinstance(x,str) for x in claim['citations']):
            raise ValueError('invalid citations')
        key=digest({'fact':claim['fact'],'obligation_id':oid})
        if key in dedup:
            old=dedup[key]
            if (old['support'],old['critical_addition']) != (claim['support'],claim['critical_addition']):
                raise ValueError('inconsistent duplicate judgments')
            old['citations']=sorted(set(old['citations'])|set(claim['citations']))
        else:
            dedup[key]={**claim,'citations':list(claim['citations'])}
    outcomes={}
    for oid,item in expected.items():
        matches=[c for c in dedup.values() if c['obligation_id']==oid]
        # A correct assertion cannot cancel a contradictory restatement of the same obligation.
        outcomes[oid]=bool(matches) and all(any(c['fact']==v['fact'] and c['support']==v['support'] for v in item['acceptable']) for c in matches)
    claims=list(dedup.values())
    unsupported=[c for c in claims if c['support']=='contradicted']
    unresolved=[c for c in claims if c['support']=='unknown']
    return {'status':'scored','retention':sum(outcomes.values())/len(expected),
            'retained':sum(outcomes.values()),'assigned_obligations':len(expected),
            'obligation_outcomes':outcomes,'unique_assertions':len(claims),
            'contradicted_assertions':len(unsupported),'unknown_support_assertions':len(unresolved),
            'unsupported_critical_additions':sum(c['critical_addition'] for c in unsupported+unresolved),
            'invalid_citation_ids':len({x for c in claims for x in c['citations'] if x not in visible_source_ids})}


def reconcile_chain(outputs):
    """Exactly three assigned hops; retain failed parent and unavailable descendants."""
    if len(outputs)!=3 or any(r.get('status') not in STATUSES for r in outputs):
        raise ValueError('three assigned hop outcomes required')
    for row in outputs:
        value=row.get('retention')
        if row['status']=='scored':
            if isinstance(value,bool) or not isinstance(value,(int,float)) or not 0<=value<=1:
                raise ValueError('invalid scored retention')
        elif value is not None:
            raise ValueError('unobserved retention must remain null')
    broken=False
    for row in outputs:
        if broken and row['status']!='missing':
            raise ValueError('descendant supplied after unavailable parent')
        # Unreviewed output exists and can have descendants; failed/missing output cannot.
        if row['status'] in {'missing','invalid'}:
            broken=True
    return {'assigned_hops':3,'scored_hops':sum(r['status']=='scored' for r in outputs),
            'terminal_retention':outputs[-1]['retention'] if outputs[-1]['status']=='scored' else None}


def paired_summary(assigned_components, p, s):
    if not assigned_components or len(set(assigned_components))!=len(assigned_components):
        raise ValueError('nonempty unique component assignment required')
    assigned=set(assigned_components)
    if set(p)-assigned or set(s)-assigned:
        raise ValueError('unassigned component result')
    diffs=[]
    for cid in assigned_components:
        a,b=p.get(cid),s.get(cid)
        for value in (a,b):
            if value is not None and (not isinstance(value,(int,float)) or isinstance(value,bool) or not 0<=value<=1):
                raise ValueError('invalid retention')
        if a is not None and b is not None:
            diffs.append(Fraction(str(b))-Fraction(str(a)))
    total=sum(diffs,Fraction());n=len(assigned);missing=n-len(diffs)
    return {'assigned_components':n,'complete_pairs':len(diffs),'unavailable_pairs':missing,
            'complete_pair_mean':float(total/len(diffs)) if diffs else None,
            'all_assigned_bounds':[float((total-missing)/n),float((total+missing)/n)]}
