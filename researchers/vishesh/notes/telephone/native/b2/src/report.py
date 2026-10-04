"""Offline source/parent replay and decision analysis; no model scoring."""
import argparse,json
from pathlib import Path
from native import packet, normalize, sha
from prepare import ROOT, request
from corpus import canonical

def analyze(out):
    p=packet()
    if json.loads((out/'packet.json').read_text())!=p:raise ValueError('packet_mismatch')
    gold=json.loads((ROOT/'prepared/gold.json').read_text())
    rows=[];parents={};generations=set();labels=[]
    for cid in ('q01','q02'):
        f=out/(cid+'.response.json')
        if f.exists():
            generation=json.loads(f.read_text()).get('id')
            if generation:generations.add(generation)
    for a in p['assignments']:
        prefix=out/a['id'].replace(':','_');row={**a,'outcome':'missing','correct':None,'decision':None}
        raw_path=Path(str(prefix)+'.response.json');req_path=Path(str(prefix)+'.request.json')
        if raw_path.exists():
            if a['parent'] is not None and a['parent']not in parents:raise ValueError('orphan_response')
            actual=json.loads(req_path.read_text());expected=request(a['arm'],p['actors'][a['case_id']],parents.get(a['parent']))
            if actual!=expected:raise ValueError('request_or_parent_mismatch')
            raw=json.loads(raw_path.read_text())
            try:obj,usage=normalize(raw,len(canonical(actual).encode())+1024)
            except (ValueError,TypeError,KeyError):row['outcome']='invalid'
            else:
                if usage['generation_id']in generations:raise ValueError('duplicate_provider_generation')
                generations.add(usage['generation_id']);parents[a['id']]=obj
                expected_decision=gold[a['case_id']]['decision'];d=obj['decision']
                outcome='correct' if d==expected_decision else 'unknown' if d=='UNKNOWN' else 'false_go' if d=='GO' else 'false_hold'
                row.update(outcome=outcome,correct=d==expected_decision,decision=d,response_sha256=sha(raw),**usage)
        elif Path(str(prefix)+'.started.json').exists():row['outcome']='started_no_response'
        for t in gold[a['case_id']]['targets']:
            labels.append({'assignment':a['id'],'target_id':t['id'],'response_sha256':row.get('response_sha256'),
                           'report_content':'unscored' if row['correct']is not None else None,'strict_integrated':'unscored' if row['correct']is not None else None,
                           'pass_1':None,'pass_2':None,'response_span':None,'rationale':None})
        rows.append(row)
    byid={r['id']:r for r in rows};blocks=[]
    for block in (1,2):
        contrasts=[]
        for cid in p['actors']:
            a,b=[byid[f'block-{block}:{cid}:{arm}:3']['correct'] for arm in ('P','R')]
            contrasts.append({'case_id':cid,'P':a,'R':b,'delta':None if a is None or b is None else int(b)-int(a),
                              'lower':(0 if b is None else int(b))-(1 if a is None else int(a)),
                              'upper':(1 if b is None else int(b))-(0 if a is None else int(a))})
        competence={}
        for arm in ('P','R'):
            first=[r for r in rows if r['block']==block and r['arm']==arm and r['hop']==1]
            valid=sum(r['correct']is not None for r in first);correct=sum(r['correct']is True for r in first)
            competence[arm]={'assigned':12,'valid':valid,'correct':correct,'screen_passed':valid==12 and correct>=10}
        complete=[r['delta'] for r in contrasts if r['delta']is not None]
        blocks.append({'block':block,'contrasts':contrasts,'complete_pairs':len(complete),'observed_pair_mean':sum(complete)/len(complete) if complete else None,
                       'assigned_bounds':[sum(r['lower'] for r in contrasts)/12,sum(r['upper'] for r in contrasts)/12],'first_hop_competence':competence})
    repeat={}
    for arm in ('P','R'):
        pairs=[(byid[f'block-1:{c}:{arm}:3']['decision'],byid[f'block-2:{c}:{arm}:3']['decision']) for c in p['actors']]
        available=[(a,b) for a,b in pairs if a is not None and b is not None]
        repeat[arm]={'available_root_pairs':len(available),'decision_disagreements':sum(a!=b for a,b in available),'missing_pairs':12-len(available)}
    root_effects=[]
    for ix,cid in enumerate(p['actors']):
        a,b=[block['contrasts'][ix] for block in blocks]
        root_effects.append({'case_id':cid,'mean_paired_delta':None if a['delta']is None or b['delta']is None else (a['delta']+b['delta'])/2,
                            'bounds':[(a['lower']+b['lower'])/2,(a['upper']+b['upper'])/2],
                            'block_delta_disagrees':None if a['delta']is None or b['delta']is None else a['delta']!=b['delta']})
    complete=[r['mean_paired_delta'] for r in root_effects if r['mean_paired_delta']is not None]
    return {'observed_valid_calls':sum(r['correct']is not None for r in rows),'assigned_calls':144,'planned_roots':12,'blocks':blocks,'repeat_disagreement':repeat,
            'root_effects':root_effects,'complete_root_mean':sum(complete)/len(complete) if complete else None,'complete_roots':len(complete),
            'assigned_root_bounds':[sum(r['bounds'][i] for r in root_effects)/12 for i in (0,1)],
            'rows':rows,'semantic_annotations':labels,'semantic_review_complete':False,'fresh_run_stability_accepted':False}

def validate_annotations(report,annotations):
    expected={(r['assignment'],r['target_id']):r for r in report['semantic_annotations']};seen=set()
    for row in annotations:
        key=(row['assignment'],row['target_id'])
        if key not in expected or key in seen:raise ValueError('annotation_coverage')
        seen.add(key);template=expected[key]
        if row.get('response_sha256')!=template['response_sha256']:raise ValueError('annotation_hash')
        if template['response_sha256'] is None:
            if row.get('report_content') is not None or row.get('strict_integrated') is not None:raise ValueError('missing_scored')
        else:
            for k in ('report_content','strict_integrated','pass_1','pass_2'):
                if row.get(k)not in ('retained','lost','ambiguous'):raise ValueError('unscored_annotation')
            if not row.get('rationale') or not isinstance(row.get('response_span'),str):raise ValueError('annotation_evidence')
    if seen!=set(expected):raise ValueError('annotation_incomplete')

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('out');ap.add_argument('destination');args=ap.parse_args()
    result=analyze(Path(args.out))
    with Path(args.destination).open('x') as f:json.dump(result,f,indent=2)
    print(json.dumps({'assigned':result['assigned_calls'],'valid':result['observed_valid_calls'],'semantic_review_complete':False}))
