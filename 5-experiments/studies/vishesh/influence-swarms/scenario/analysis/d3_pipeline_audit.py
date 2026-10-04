"""Retrospective saved-data audit only; no providers, credentials or dispatch imports."""
import collections,hashlib,json
from pathlib import Path
BASE=Path(__file__).resolve().parents[1]

def analyze():
    paths={k:BASE/'reviews'/('native-D3-01-'+k+'.json') for k in ('audit','reconciliation','summary')}
    values={k:json.loads(p.read_text()) for k,p in paths.items()}
    a,r,s=values['audit'],values['reconciliation'],values['summary']
    audit={v['case_id']:v for v in a};cases=r['cases']
    assert len(audit)==len(a)==len(cases)==6
    assert set(audit)=={v['case_id'] for v in cases}
    confusion=collections.Counter();by_requirement=collections.Counter();rows=[]
    for case in cases:
        item=audit[case['case_id']];checks=item['matrix']['candidate_checks'];correct=0
        for candidate,gold in item['source_checks'].items():
            for field,expected in gold.items():
                actual=checks[candidate][field];assert actual in ('PASS','FAIL','UNKNOWN')
                confusion[(expected,actual)]+=1;correct+=expected==actual
                if expected!=actual:by_requirement[field]+=1
        assert correct==case['matrix_correct']
        reviewer=item['matrix']['choice'];chair=case['choices']['matrix_standard']
        rows.append({'case_id':case['case_id'],'reviewer_provisional_choice':reviewer,
            'reviewer_choice_acceptable':reviewer in case['source_acceptable'],
            'standard_chair_choice':chair,'consistency_chair_choice':case['choices']['matrix_consistent'],
            'chair_acceptable':chair in case['source_acceptable'],
            'source_acceptable':case['source_acceptable'],'correct_statuses':correct,'status_denominator':15,
            'conversion':'unchanged' if reviewer==chair else 'changed_to_correct_action' if chair in case['source_acceptable'] else 'changed_to_incorrect_action',
            'unnecessary_deferral':chair=='DEFER' and 'DEFER' not in case['source_acceptable']})
    total=sum(confusion.values());correct=sum(n for (a,b),n in confusion.items() if a==b)
    assert total==s['matrix_total']==90 and correct==s['matrix_correct']==76
    assert s['planned']==s['terminal']==s['valid']==18 and s['calls']==30
    assert all(x['standard_chair_choice']==x['consistency_chair_choice'] for x in rows)
    assert sum(x['chair_acceptable'] for x in rows)==s['by_arm']['matrix_standard']['acceptable']==4
    return {'analysis_type':'retrospective_saved_data','model_calls':0,'independent_development_clusters':6,
        'native_D3_calls':30,'native_D3_valid_decisions':18,
        'confusion':[{'source':a,'model':b,'count':n} for (a,b),n in sorted(confusion.items())],
        'errors_by_requirement':dict(sorted(by_requirement.items())),
        'reviewer_acceptable':sum(x['reviewer_choice_acceptable'] for x in rows),'chair_acceptable':4,
        'conversions':dict(collections.Counter(x['conversion'] for x in rows)),
        'unnecessary_deferrals':sum(x['unnecessary_deferral'] for x in rows),
        'narrative_authorization_acceptable':None,'narrative_authorization_reason':'not applied; legacy zero is not an observed failure',
        'typed_extraction_accuracy':None,'typed_extraction_reason':'not instrumented in D3',
        'causal_peer_or_gate_effect':'not identified by these provisional-to-final transitions',
        'cases':rows,'evidence':[{'path':p.relative_to(BASE).as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in paths.values()]}

if __name__=='__main__':
    out=BASE/'reviews/D3-retrospective-pipeline.json'
    with out.open('x') as f:json.dump(analyze(),f,indent=2);f.write('\n')
    print('Retrospective audit reconciled six clusters, 90 statuses and 18 final decisions; zero new model calls.')
