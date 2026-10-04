"""Conservative text parser and source-grounded decision baseline; no gold inputs."""
import re
CONTRACT=('Use the three authenticated source receipts, not the number of reports, to decide whether the query proposition is supported by a majority of the supplied independent equal-reliability sources. '
 'Return ONE for a source majority supporting the proposition, ZERO for an opposing majority, otherwise DEFER. '
 'Supplied source groups are independent by construction; unknown groups or incomplete/unparseable evidence require DEFER. '
 'Report receipt IDs are authenticated bindings. Reports may misstate their receipt; also assess their fidelity. '
 'Observation outranks a plan; a Correction replaces the Initial entry for the same entity/time. Do not interpolate missing times. '
 'Running and stopped are opposites; not running means stopped, not stopped means running. For mass use query threshold in grams; one kilogram is 1000 grams. '
 'Copying a report creates no new source. This is a synthetic evidence-MAP decision, not verified physical truth.')
BOOL=re.compile(r'at (\d\d:\d\d), ([A-Za-z0-9_-]+) was (running|stopped|not running|not stopped)\.',re.I)
MASS=re.compile(r'at (\d\d:\d\d), ([A-Za-z0-9_-]+) measured (\d+(?:\.\d+)?) (grams|kilograms)\.',re.I)


def parse(text,query):
    facts=[]
    for line in text.splitlines():
        tag='Observation';body=line
        if ': ' in line:tag,body=line.split(': ',1)
        if tag not in ('Observation','Plan','Initial','Correction'):return None
        if tag=='Plan':
            body=body.replace(' will be ',' was ')
        m=BOOL.fullmatch(body);n=MASS.fullmatch(body)
        if m:
            time,entity,state=m.groups();value=state.lower() in ('running','not stopped');kind='running'
        elif n:
            time,entity,number,unit=n.groups();value=float(number)*(1000 if unit.lower()=='kilograms' else 1);kind='mass'
        else:return None
        if kind!=query['kind']:return None
        if entity==query['entity'] and time==query['time'] and tag!='Plan':facts.append((tag,value))
    corrected=[v for tag,v in facts if tag=='Correction']
    values=corrected if corrected else [v for tag,v in facts if tag!='Initial']
    if not values or len(set(values))!=1:return None
    value=values[0]
    return bool(value) if query['kind']=='running' else value>=query['threshold_grams']


def inspect(actor):
    try:
        if set(actor)!={'contract','event','query','receipts','reports'} or actor['contract']!=CONTRACT:return None
        q=actor['query'];rs=actor['receipts'];reports=actor['reports']
        if set(q)!=({'kind','entity','time','threshold_grams'} if q.get('kind')=='mass' else {'kind','entity','time'}):return None
        if any(set(r)!={'id','group','text'} for r in rs):return None
        if q['kind'] not in ('running','mass') or len(rs)!=3 or not reports:return None
        if len({r['id'] for r in rs})!=3 or len({r['group'] for r in rs})!=3 or any(not r['group'] for r in rs):return None
        votes={r['id']:parse(r['text'],q) for r in rs}
        if any(v is None for v in votes.values()):return None
        claims=[];seen=set()
        for r in reports:
            if set(r)!={'id','receipt_id','text'} or r['id'] in seen or r['receipt_id'] not in votes:return None
            seen.add(r['id']);v=parse(r['text'],q)
            if v is None:return None
            claims.append({'report':r['id'],'receipt':r['receipt_id'],'value':v,'faithful':v==votes[r['receipt_id']]})
        if {c['receipt'] for c in claims}!=set(votes):return None
        return {'source_votes':votes,'claims':claims,'decision':'ONE' if sum(votes.values())>=2 else 'ZERO'}
    except (KeyError,TypeError,ValueError):return None


def predict(actor,policy='source_parser'):
    data=inspect(actor)
    if data is None:return 'DEFER'
    if policy=='source_parser':return data['decision']
    if policy=='report_vote':values=[c['value'] for c in data['claims']]
    elif policy=='deduplicated_claims':
        by={}
        for c in data['claims']:by.setdefault(c['receipt'],set()).add(c['value'])
        if any(len(v)!=1 for v in by.values()):return 'DEFER'
        values=[next(iter(v)) for v in by.values()]
    else:raise ValueError(policy)
    total=sum(values)
    return 'ONE' if total>len(values)/2 else 'ZERO' if total<len(values)/2 else 'DEFER'
