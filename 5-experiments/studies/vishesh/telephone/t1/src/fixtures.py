"""Original fixed software fixtures; never sampled Village or native-agent outcomes."""
import copy
from scoring import digest,text_hash,score,reconcile_chain

SPECS=[
 ('qualification','A prototype may work; no test has been performed.','prototype','works','unverified','modality','verified'),
 ('attribution','Sensor A measured the temperature; sensor B did not measure it.','measurement','performed','sensor A','attribution','sensor B'),
 ('scope','Two checked records passed, with no claim about other records.','audit','passed','two checked records','scope','all records'),
 ('time','The gate was open at 14:00; later state is not reported.','gate','open','14:00','time','now'),
 ('correction','The count of 12 was corrected to 9; the current count is 9.','count','equals','9 items','value_unit','12 items'),
 ('dependence','Two reports reference one acquisition, so they are one evidence source.','reports','derive from','one acquisition','value_unit','two acquisitions'),
 ('unavailable','The linked receipt is unavailable, so approval is unverified.','approval','status','unverified','modality','verified'),
 ('polarity','The recorded deployment failed; the report link resolves to that failure.','deployment','failed','failed','predicate','succeeded'),
]

BAD_TEXT = {
 'qualification':'The prototype has been tested and works.',
 'attribution':'Sensor B performed the temperature measurement.',
 'scope':'Every record passed the audit.',
 'time':'The gate is open now.',
 'correction':'The current count is 12 items.',
 'dependence':'The two reports provide two independent acquisitions.',
 'unavailable':'The missing receipt confirms verified approval.',
 'polarity':'The recorded deployment succeeded.',
}


def fact(entity,predicate,**kw):
    return {'entity':entity,'predicate':predicate,'value_unit':None,'time':None,'scope':None,'modality':None,'attribution':None,**kw}


def copy_source(records):
    return '\n'.join(r['text'] for r in records)


def reference_lookup(records, requested_ids):
    index={r['id']:r for r in records}
    if len(index)!=len(records) or any(x not in index for x in requested_ids):
        raise ValueError('ambiguous or absent source')
    return '\n'.join(index[x]['text'] for x in requested_ids)


def cases():
    rows=[]
    for n,(family,text,entity,predicate,value,field,wrong) in enumerate(SPECS):
        main=fact(entity,predicate)
        main[field]=value
        facts=[main,fact('archive','contains',value_unit='3 records'),fact('review','status',modality='pending')]
        records=[{'id':f'r{n:02d}-{i}','text':t} for i,t in enumerate([text,'The archive contains three records.','Review is still pending.'])]
        gold={'obligations':[{'id':f'o{i}','acceptable':[{'fact':f,'support':'supported'}]} for i,f in enumerate(facts)]}
        claims=[{'obligation_id':f'o{i}','fact':f,'support':'supported','critical_addition':False,'citations':[records[i]['id']]} for i,f in enumerate(facts)]
        trajectories={}
        for condition in ('faithful','distorted','omitted'):
            hops=[]
            for hop in (1,2,3):
                output=copy_source(records);annotated=copy.deepcopy(claims)
                if hop>=2 and condition=='distorted':
                    output=BAD_TEXT[family]+'\n'+ '\n'.join(r['text'] for r in records[1:])
                    annotated[0]['fact'][field]=wrong
                    annotated[0]['support']='contradicted'
                if hop>=2 and condition=='omitted':
                    output='\n'.join(r['text'] for r in records[1:]);annotated=annotated[1:]
                review={'review_id':f'original-fixture-{n}-{condition}-{hop}','reviewed':True,'all_assertions_reviewed':True,
                        'output_sha256':text_hash(output),'gold_sha256':digest(gold),'claims':annotated}
                hops.append({'text':output,'review':review})
            trajectories[condition]=hops
        rows.append({'id':f'dev-{n:02d}','family':family,'split':'development',
                     'notice':'SCRIPTED SOFTWARE FIXTURE — NOT MODEL OR VILLAGE EVIDENCE',
                     'records':records,'gold':gold,'trajectories':trajectories})
    return rows


def validate():
    results=[]
    for case in cases():
        known={r['id'] for r in case['records']}
        baseline=copy_source(case['records'])
        assert reference_lookup(case['records'],[r['id'] for r in case['records']])==baseline
        for condition,hops in case['trajectories'].items():
            scored=[score(h['text'],h['review'],case['gold'],known) for h in hops]
            summary=reconcile_chain(scored)
            expected=1.0 if condition=='faithful' else 2/3
            assert summary['terminal_retention']==expected
            assert scored[-1]['contradicted_assertions']==(1 if condition=='distorted' else 0)
            results.append({'component':case['id'],'fixture_condition':condition,'hop_retention':[s['retention'] for s in scored],
                            'contradicted_assertions':[s['contradicted_assertions'] for s in scored],
                            'terminal_retention':summary['terminal_retention']})
    return {'scope':'fixed authored software acceptance fixtures; no experimental sweep or native outcome',
            'roots':8,'trajectories':24,'hop_outputs':72,'source_copy_terminal_retention':1.0,
            'reference_lookup_matches_copy':True,'results':results,'model_calls':0}

if __name__=='__main__':
    import json
    print(json.dumps(validate(),indent=2))
