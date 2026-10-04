"""Offline D5 failure reconciliation. No provider, credential, or dispatch imports."""
import argparse,collections,hashlib,json
from pathlib import Path

def digest(v):
    return hashlib.sha256(json.dumps(v,sort_keys=True).encode()).hexdigest()

def audit(root):
    root=Path(root);s=json.loads((root/'summary.json').read_text());rows=json.loads((root/'outcomes.json').read_text())
    assert len(rows)==s['planned']==s['terminal']==24
    assert digest(rows)==s['outcomes_hash']
    arms=('matrix_inherited','typed_inherited','matrix_records_only','typed_records_only')
    assigned=set();counts=collections.Counter();attempts=0;observed_cost=0.;cases=[]
    for i in range(6):
        case=json.loads((root/f'case-{i}.json').read_text());events=[json.loads(x) for x in (root/f'events-{i}.jsonl').read_text().splitlines()]
        requests={};terminal={};failures={}
        assert [e['event_index'] for e in events]==list(range(len(events)))
        for e in events:
            counts[e['kind']]+=1
            if e['kind']=='request':
                assert digest(e['request'])==e['request_hash'];assert e['arm'] not in requests
                requests[e['arm']]=e
                assert not {'evaluator','truth_hash','source_checks','acceptable','scorecard'}&set(e['request']['observation'])
            elif e['kind']=='call_error':
                assert e['arm'] in requests and e['call']==requests[e['arm']]['call']
                failures[e['arm']]=e;attempts+=e['usage']['calls'];observed_cost+=e['usage']['actual_usd']
            elif e['kind']=='terminal':
                r=e['outcome'];key=(r['case_id'],r['arm']);assert key not in assigned;assigned.add(key);terminal[r['arm']]=r
        assert set(requests)==set(terminal)==set(failures)==set(arms)
        for context in ('inherited','records_only'):
            assert requests['matrix_'+context]['request']['observation']==requests['typed_'+context]['request']['observation']
        for arm in arms:
            row=terminal[arm];assert row==next(r for r in rows if (r['case_id'],r['arm'])==(case['case_id'],arm))
            assert not row['valid'] and row['error']=='PolicyError'
            assert all(row[k] is None for k in ('review','compiled','decision','evaluation','authority','measurements'))
            e=failures[arm];assert e['usage']['calls']==2 and e['usage']['input_tokens']==e['usage']['output_tokens']==0
        cases.append({'case_id':case['case_id'],'logical_requests':4,'transport_attempts':8,'responses':0,'terminal_failures':4})
    assert attempts==s['calls']==48 and counts['response']==0 and counts['terminal']==24
    assert s['usage_missing']==48 and observed_cost==s['actual_usd']==0
    assert all(c['difference'] is None for c in s['paired_differences'])
    before=3.178320;after=4.868832
    return {'attempt':'native-D5-01','analysis_type':'retrospective_saved_data','assigned':24,'terminal':24,'valid':0,'invalid':24,'independent_case_clusters_assigned':6,'evaluable_case_clusters':0,'logical_requests':counts['request'],'transport_attempts':attempts,'responses':0,'terminal_events':counts['terminal'],'events_total':sum(counts.values()),'request_hashes_verified':True,'matched_reviewer_observations':True,'source_grades_assessed':0,'source_grades_agree':None,'scientific_contrasts_estimable':False,'actual_cost_usd':None,'observed_usage_cost_usd':observed_cost,'usage_missing_attempts':48,'usage_counters_reconcile':True,'usage_coverage_complete':False,'budget_cap_usd':8,'reserved_before_usd':before,'reserved_after_usd':after,'new_reservation_usd':round(after-before,6),'unreserved_usd':round(8-after,6),'provider_status':'not retained','retry_inference':'Each first transport failed with one of HTTP429/502/503/504 according to the frozen retry path; exact status and final error cause are unavailable.','effect_interpretation':'No usable evidence about model behavior or architecture effects. Missing responses are not bad procurement choices.','cases':cases,'file_hashes':{p.name:hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.iterdir()) if p.name in ('manifest.json','summary.json','outcomes.json') or p.name.startswith(('case-','events-'))}}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    result=audit(a.root);a.output.write_text(json.dumps(result,indent=2)+'\n');print('24 assignments and 48 failed transports reconciled; no scientific outcomes or complete cost data.')
