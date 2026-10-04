"""Generate finite controlled packets. Actor text and typed construction gold are separate."""
import copy,hashlib,json,random
from instrument import CONTRACT,inspect,predict
FAMILIES=('polarity','time','entity','units','modality','correction')
DOMAINS={'development':('workshop','loading','utility'), 'qualification':('archive','sorting','ventilation'), 'evaluation':('observatory','packaging','irrigation','assembly')}
PATTERNS=((False,True,True),(True,False,False),(True,True,False),(False,False,True))


def render(family,entity,time,value,style=0):
    state=('not stopped' if value else 'not running') if style else ('running' if value else 'stopped')
    opposite='stopped' if value else 'running'
    line=f'At {time}, {entity} was {state}.'
    if family=='polarity':return line
    if family=='time':return f'At 08:00, {entity} was {opposite}.\n'+line
    if family=='entity':return f'At {time}, {entity}-other was {opposite}.\n'+line
    if family=='units':return f'At {time}, {entity} measured {6 if value else 4} kilograms.' if style else f'At {time}, {entity} measured {6000 if value else 4000} grams.'
    if family=='modality':return f'Plan: at {time}, {entity} will be {opposite}.\nObservation: '+line
    if family=='correction':return f'Initial: at {time}, {entity} was {opposite}.\nCorrection: '+line
    raise ValueError(family)


def generate(split,seed):
    rng=random.Random(seed);n={'development':2,'qualification':1,'evaluation':4}[split];rows=[]
    for family in FAMILIES:
        for index in range(n):
            root=f'{split}-{family}-{index}';domain=DOMAINS[split][index%len(DOMAINS[split])]
            entity=domain+'-'+str(rng.randrange(10000,99999));event=hashlib.sha256((root+str(seed)).encode()).hexdigest()[:16]
            bits=PATTERNS[(index+(0 if split=='evaluation' else 1))%4];time=f'{rng.randrange(10,17):02}:00'
            q={'kind':'mass' if family=='units' else 'running','entity':entity,'time':time}
            if family=='units':q['threshold_grams']=5000
            ids=[hashlib.sha256((event+str(i)).encode()).hexdigest()[:10] for i in range(3)]
            receipts=[{'id':ids[i],'group':'group-'+ids[i],'text':render(family,entity,time,bits[i],rng.randrange(2))} for i in range(3)]
            rng.shuffle(receipts)
            for count in (1,5):
                for inverted in (False,True):
                    reports=[];report_gold={}
                    for i,bit in enumerate(bits):
                        claim=not bit if i==0 and inverted else bit
                        for rep in range(count if i==0 else 1):
                            rid=hashlib.sha256((event+str(i)+'copy'+str(rep)).encode()).hexdigest()[:12]
                            text=render('units' if family=='units' else 'polarity',entity,time,claim,0)
                            reports.append({'id':rid,'receipt_id':ids[i],'text':text});report_gold[rid]=claim==bit
                    reports.sort(key=lambda r:r['id'])
                    actor={'contract':CONTRACT,'event':event,'query':q,'receipts':copy.deepcopy(receipts),'reports':reports}
                    rows.append({'id':root+f'-n{count}-d{int(inverted)}','root':root,'family':family,'domain':domain,
                                 'condition':{'copies':count,'inverted':inverted},'actor':actor,
                                 'gold':{'decision':'ONE' if sum(bits)>=2 else 'ZERO','source_votes':dict(zip(ids,bits)),
                                         'report_fidelity':report_gold,'focal_receipt':ids[0]}})
    return rows


def validate(rows,split):
    assert len({r['id'] for r in rows})==len(rows)
    groups={};correct={p:0 for p in ('source_parser','report_vote','deduplicated_claims')};mismatches=0;outcomes=[]
    for row in rows:
        groups.setdefault(row['root'],[]).append(row);d=inspect(row['actor']);assert d is not None
        assert d['source_votes']==row['gold']['source_votes']
        assert {c['report']:c['faithful'] for c in d['claims']}==row['gold']['report_fidelity']
        assert d['decision']==row['gold']['decision'];mismatches+=d['decision']!=row['gold']['decision']
        assert set(row['actor'])=={'contract','event','query','receipts','reports'}
        for policy in correct:
            got=predict(row['actor'],policy);correct[policy]+=got==row['gold']['decision']
            outcomes.append({'id':row['id'],'policy':policy,'decision':got,'correct':got==row['gold']['decision']})
    for group in groups.values():
        assert len(group)==4
        base=group[0]['actor'];focal=group[0]['gold']['focal_receipt']
        for r in group:
            a=r['actor'];assert a['query']==base['query'] and a['receipts']==base['receipts']
            assert r['gold']['decision']==group[0]['gold']['decision']
            assert sum(x['receipt_id']==focal for x in a['reports'])==r['condition']['copies']
            assert len(a['reports'])==r['condition']['copies']+2
            assert sum(not v for v in r['gold']['report_fidelity'].values())==(r['condition']['copies'] if r['condition']['inverted'] else 0)
            assert [x for x in a['reports'] if x['receipt_id']!=focal]==[x for x in base['reports'] if x['receipt_id']!=focal]
    return {'split':split,'roots':len(groups),'packets':len(rows),'family_counts':{f:sum(r['family']==f for r in rows) for f in FAMILIES},
            'critical_mismatches':mismatches,'correct':correct,'outcomes':outcomes}


def publish_development(path):
    rows=generate('development',20261004);result=validate(rows,'development')
    (path/'development.json').write_text(json.dumps(rows,indent=2)+'\n')
    (path/'development-results.json').write_text(json.dumps(result,indent=2)+'\n')
    lines=['# Development packet explorer','48 packets / 12 authored roots. Each source set is fixed across four conditions. Exact expected answers below are development labels, not native results.']
    for group in range(0,len(rows),4):
        r=rows[group];a=r['actor'];lines += ['## '+r['root'], 'Query: '+json.dumps(a['query']), 'Source receipts:']
        lines += ['- '+x['id']+': '+x['text'].replace('\n',' / ') for x in a['receipts']]
        lines += ['Expected source decision: **'+r['gold']['decision']+'**. Focal source: '+r['gold']['focal_receipt']+'.',
                  '| Copies | Inverted | Report-vote | Deduplicated claims | Source-parser |','|---|---|---|---|---|']
        for c in rows[group:group+4]:lines.append('| '+str(c['condition']['copies'])+' | '+str(c['condition']['inverted'])+' | '+' | '.join(predict(c['actor'],p) for p in ('report_vote','deduplicated_claims','source_parser'))+' |')
    (path/'DEVELOPMENT.md').write_text('\n'.join(lines)+'\n')
    return {k:v for k,v in result.items() if k!='outcomes'}
