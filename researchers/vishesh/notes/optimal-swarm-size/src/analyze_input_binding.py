"""Saved-data Q-A7 analysis only; no transport, credentials or new model calls."""
import argparse,hashlib,json
from pathlib import Path
from tasks import generate,evaluate,digest
from stage_audit import evidence_stage_audit

def analyze(base):
    base=Path(base);reconciliation=json.loads((base/'reconciliation.json').read_text());records=[];coverage=[]
    for path in sorted(base.glob('*/outcome.json')):
        record=json.loads(path.read_text());a=record['assignment']
        task=generate(a['family'],a['structure'],a['root'],width=a['width'])
        assert digest(task.public)==a['public_task_sha256']
        assert evaluate(task,record.get('artifact') or '{}')==record['evaluation']
        assert evidence_stage_audit(task,record)==record['stage_diagnostics']
        trace=[json.loads(line) for line in path.with_name('trace.jsonl').read_text().splitlines()]
        requests=[e for e in trace if e['kind']=='request_context'];responses=[e for e in trace if e['kind']=='model_response']
        assert all(hashlib.sha256(e['serialized_request'].encode()).hexdigest()==e['sha256'] for e in requests)
        for response in responses:
            parsed=json.loads(response['text'])
            if response['phase']=='work':assert parsed['artifact']==record['work_artifacts'][response['item']]
            elif response['phase']=='integrate':assert parsed==json.loads(record['artifact'])
            elif response['phase'] in ('plan','plan_repair'):assert 'dependencies' in parsed
        d=record['stage_diagnostics']
        coverage.append({'id':a['id'],'requests':len(requests),'responses':len(responses),'all_request_hashes_match':True,
            'visible_responses_reconcile_to_saved_actions':True,'first_worker_value_error':d['first_worker_value_error'],'first_final_value_error':d['first_final_value_error'],
            'local_arithmetic_mismatches':d['local_arithmetic_mismatches'],'correct_to_wrong':d['correct_to_wrong'],'wrong_to_correct':d['wrong_to_correct']})
        records.append({'id':a['id'],'root':a['root'],'structure':a['structure'],'arm':a['arm'],
            'quality':record['evaluation']['quality'],'success':record['operational_success'],'failure':record['failure'],
            'elapsed_s':record['elapsed_s'],'correct_items_per_second':record['correct_items_per_second'],
            'exposure_microdollars':record['exposure_microdollars'],'local_arithmetic_mismatches':len(d['local_arithmetic_mismatches']),
            'worker_wrong_values':d['worker_wrong_values'],'worker_wrong_proofs':d['worker_wrong_proofs'],'correct_to_wrong':d['correct_to_wrong'],'wrong_to_correct':d['wrong_to_correct']})
    pairs=[]
    for root in (6,7):
        for structure in ('parallel','chain'):
            arms={r['arm']:r for r in records if r['root']==root and r['structure']==structure}
            if set(arms)!={'full','bound'}:pairs.append({'root':root,'structure':structure,'observed':False});continue
            f,b=arms['full'],arms['bound'];pairs.append({'root':root,'structure':structure,'observed':True,
                'full_quality':f['quality'],'bound_quality':b['quality'],'quality_delta':b['quality']-f['quality'],
                'full_correct_items_per_second':f['correct_items_per_second'],'bound_correct_items_per_second':b['correct_items_per_second']})
    observed=[p for p in pairs if p['observed']];bound=[r for r in records if r['arm']=='bound']
    complete=len(observed)==4
    support=complete and all(sum(p['quality_delta'] for p in observed if p['root']==root)>0 for root in (6,7)) and sum(p['quality_delta'] for p in observed)/4>=.125 and sum(r['quality'] for r in bound)/4>=.90 and all(sum(p['quality_delta'] for p in observed if p['structure']==s)>=0 for s in ('parallel','chain'))
    return {'scope':'two development roots; paired descriptive diagnostic, not optimal-N or population inference',
        'assigned':reconciliation['assigned'],'terminal':reconciliation['terminal'],'unstarted':reconciliation['unstarted'],
        'stop_reason':reconciliation['stop_reason'],'records':records,'pairs':pairs,'trace_coverage':coverage,
        'request_count':sum(c['requests'] for c in coverage),'response_count':sum(c['responses'] for c in coverage),
        'saved_scores_and_stage_audits_recomputed':True,'predeclared_support_threshold_met':support,
        'inference':'threshold met; fresh qualification still required' if support else 'no promotion; inspect mixed/floor/operational limits'}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('results',type=Path);a=p.parse_args()
    report=analyze(a.results);(a.results/'analysis.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({'terminal':report['terminal'],'requests':report['request_count'],'support':report['predeclared_support_threshold_met']}))
