"""Offline-only D10 packet builder. No credentials, network, budget writes or launch."""
import copy,hashlib,json,sys
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]
import typed_policy as tp
import typed_diagnostic as td
from source_bound_policy import compile_source
from openrouter_d7 import MODEL,PROVIDER
from output_contract_d8 import JSON_ONLY

def report_surface(report):
    r=copy.deepcopy(report)
    for fields in r['extraction_alignment'].values():
        for fact in fields.values():
            fact.pop('quote_exact',None)
            fact['reason']='verified explicitly unknown' if fact['aligned'] and fact['accepted'] is None else 'verified against selected source' if fact['aligned'] else 'unsupported by selected evidence'
    return r

def prepare():
    requests=[];sources=[];policy=object.__new__(td.FactsPolicy)
    for stage in ('D9-B','D9-C'):
        ppath=BASE/'reviews'/f'{stage}-packet.json';spath=BASE/'reviews'/f'native-{stage}-01/summary.json'
        packet=json.loads(ppath.read_text());summary=json.loads(spath.read_text())
        sources.extend([{'path':str(p.relative_to(BASE)),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in (ppath,spath)])
        for original,result in zip(packet['requests'],summary['assignments']):
            if result['status']!='valid':continue
            answer=result['answer'];obs=original['request']['observation'];index=len(requests)//2
            order=('exact_excerpt','cited_document') if index%2==0 else ('cited_document','exact_excerpt')
            for condition in order:
                compiled=tp.compile_checks(answer,obs) if condition=='exact_excerpt' else compile_source(answer,obs)
                # Frozen reviewer observation derives from the original D5 chair;
                # restore only its declared role/phase and append one verified report.
                chair_obs=copy.deepcopy(obs);chair_obs['phase']='chair';chair_obs.pop('role',None);
                from study import CHAIR
                q={'instructions':CHAIR+' Use the cost_worksheet for arithmetic where available; its cited input records are evidence, not certified truth. It gives no final recommendation.','observation':chair_obs}
                expected=json.loads((BASE/'d3-parent-hashes.json').read_text())[str(index)]['request']
                assert td.digest(q)==expected,'frozen parent mismatch'
                chair_obs['reports'].append(report_surface(compiled))
                schema=policy.schema(q,td.scripted);tp.check_wire_schema(schema)
                wire={'model':MODEL,'provider':PROVIDER,'reasoning':{'enabled':False},'stream':False,'max_tokens':3072,'temperature':0,'messages':[{'role':'system','content':q['instructions']+JSON_ONLY},{'role':'user','content':json.dumps(chair_obs)}],'response_format':{'type':'json_schema','json_schema':{'name':'chair_output','strict':True,'schema':schema}}}
                raw=json.dumps(wire).encode();assert len(raw)<=32768
                td.validate(td.scripted(chair_obs),chair_obs)
                requests.append({'case_id':original['case_id'],'condition':condition,'tldr':f"Saved-input chair comparison on {original['case_id']}: {condition} verification, same dossier/team advice and budget; measure raw source-policy-acceptable choice, blocker handling and separate guard; development case, not a holdout.",'wire_body':wire,'wire_bytes':len(raw),'wire_sha256':hashlib.sha256(raw).hexdigest(),'maximum_reservation_usd':.048640})
    assert len(requests)==10 and len({i['case_id'] for i in requests})==5
    return {'stage':'D10-proposed','launch_enabled':False,'model_calls':0,'maximum_transport_attempts':10,'retries':0,'stop_on_first_failure':True,'maximum_total_reservation_usd':.486400,'source_evidence':sources,'excluded_first_attempt_case':'seasonal-usage-cost','requests':requests}
if __name__=='__main__':
    out=BASE/'reviews/D10-proposed-packet.json';p=prepare();out.write_text(json.dumps(p,indent=2)+'\n');print(json.dumps({'prepared_requests':len(p['requests']),'model_calls':0,'launch_enabled':False,'max_wire_bytes':max(i['wire_bytes'] for i in p['requests'])}))
