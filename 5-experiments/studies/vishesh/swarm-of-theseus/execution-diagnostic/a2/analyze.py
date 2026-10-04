"""Saved-data only. Assigned denominators, acquisition and execution remain distinct."""
import json,csv
from pathlib import Path
from design import d1,digest,execution_request
from scoring import policy_score,policy_reference,action_score

def summarize(root):
    root=Path(root); manifest=json.loads((root/'manifest.json').read_text()); design=manifest['assignments']
    learners={};rows=[];audits=[];hash_errors=[];actual=0.;unknown=0;started=0;terminal=0;reserved=0.;provider_errors=0
    for a in design:
        start=root/'calls'/(a['id']+'-started.json'); finish=root/'calls'/(a['id']+'-finished.json')
        if start.exists():
            started+=1; st=json.loads(start.read_text());reserved+=st['reserved_usd']
            if st['request_sha256']!=digest(st['request']):hash_errors.append(a['id'])
        else:st=None
        if finish.exists():
            terminal+=1;result=json.loads(finish.read_text());provider_errors+=bool(result.get('error'))
            if result.get('actual_usd') is None:unknown+=1
            else:actual+=result['actual_usd']
        else:result={'value':None,'raw_text':None,'error':'not_started' if not st else 'unfinished','actual_usd':None}
        if st and not finish.exists():unknown+=1
        if a['kind']=='learn':
            p=policy_score(a,result);reference=policy_reference(a,result)
            if any(p[k]!=reference[k] for k in reference):audits.append(a['id'])
            if st and st['request']!=a['request']:hash_errors.append(a['id'])
            learners[a['id']]=p
        else:
            score=action_score(a,result); direct=d1.score(dict(a,arm='E'),result)['rows'][0]
            if any(score[k]!=direct[k] for k in ('correct','action','truth','valid_response')):audits.append(a['id'])
            mapping=a['rule'] if a['arm']=='ceiling' else learners[a['parent']]['mapping']
            if st and (mapping is None or st['request']!=execution_request(a,mapping)):hash_errors.append(a['id'])
            rows.append({'assignment':a['id'],'seed':a['seed'],'family':a['context'],'arm':a['arm'],'started':bool(st),'terminal':finish.exists(),'response_received':bool(result.get('response_received')),**score})
    arms={}
    for arm in ('learned','ceiling'):
        rs=[r for r in rows if r['arm']==arm]; correct=sum(r['correct'] for r in rs)
        families={f:sum(r['correct'] for r in rs if r['family']==f) for f in ('release','incident')}
        worlds={str(w):sum(r['correct'] for r in rs if r['seed']==w) for w in sorted({r['seed'] for r in rs})}
        false_release=sum(r['family']=='release' and r['truth']!='ship' and r['action']=='ship' for r in rs)
        false_incident=sum(r['family']=='incident' and r['truth']=='none' and r['action'] not in (None,'none') for r in rs)
        useful=sum(r['family']=='release' and r['truth']=='ship' and r['correct'] for r in rs)
        valid=sum(r['valid_response'] for r in rs)
        arms[arm]={'assigned':len(rs),'observed':sum(r['response_received'] for r in rs),'observed_accuracy':correct/sum(r['response_received'] for r in rs) if any(r['response_received'] for r in rs) else None,'correct':correct,'valid':valid,'family_correct':families,'root_correct':worlds,'false_releases':false_release,'false_incident_activations':false_incident,'useful_releases':useful,'qualified':bool(correct>=95 and min(families.values())>=46 and min(worlds.values())>=15 and valid==96 and false_release==0 and false_incident==0 and useful>=11)}
    learning={'assigned':12,'exact_mapping':sum(p['exact_mapping'] for p in learners.values()),'valid_support':sum(p['support_valid'] for p in learners.values()),'qualified_policies':sum(p['qualified'] for p in learners.values())}
    missing_exposure=0.
    for a in design:
        s=root/'calls'/(a['id']+'-started.json');f=root/'calls'/(a['id']+'-finished.json')
        if s.exists() and (not f.exists() or json.loads(f.read_text()).get('actual_usd') is None):missing_exposure+=json.loads(s.read_text())['reserved_usd']
    summary={'evidence_type':manifest.get('evidence_type'),'assigned_calls':204,'started_calls':started,'terminal_calls':terminal,'graded_decisions':192,'observed_decisions':sum(r['response_received'] for r in rows),'terminal_decision_records':sum(r['terminal'] for r in rows),'learning':learning,'arms':arms,'audit_disagreements':audits,'request_hash_mismatches':hash_errors,'provider_errors':provider_errors,'unknown_usage_calls':unknown,'actual_model_usd':round(actual,9),'reserved_dispatch_usd':round(reserved,9),'unresolved_exposure_usd':round(missing_exposure,9),'prior_estimated_usd':.8122310437,'prior_unresolved_usd':.010452,'cumulative_estimated_plus_unresolved_usd':.8226830437+actual+missing_exposure,'qualification_passed':bool(started==terminal==204 and not unknown and not audits and not hash_errors and not provider_errors and learning['qualified_policies']==12 and all(v['qualified'] for v in arms.values()))}
    (root/'summary.json').write_text(json.dumps(summary,indent=2));(root/'policies.json').write_text(json.dumps(learners,indent=2))
    with (root/'decisions.csv').open('w') as f:
        writer=csv.DictWriter(f,fieldnames=list(rows[0]));writer.writeheader();writer.writerows(rows)
    return summary
