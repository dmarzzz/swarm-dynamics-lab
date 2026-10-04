"""Saved-data-only exact lineage replay, deterministic scoring and audit sample."""
import argparse,json,hashlib
from pathlib import Path
from corpus import canonical,sha
from contract import request,normalize

def analyze(p,out,gold):
    if sha(gold)!=p['gold_sha256']:raise ValueError('gold_mismatch')
    out=Path(out);parents={};hashes={};seen=set();rows=[]
    for cid in ('q01','q02'):
        qpath=out/(cid+'.response.json')
        if qpath.exists():
            generation=json.loads(qpath.read_text()).get('id')
            if isinstance(generation,str):seen.add(generation)
    for a in p['assignments']:
        r={**a,'status':'missing','correct':None,'false_certainty':None};path=out/(a['id']+'.response.json')
        if path.exists():
            try:
                req=json.loads((out/(a['id']+'.request.json')).read_text());raw=json.loads(path.read_text())
                previous=None if a['parent']is None else parents[a['parent']]
                expected=request(a['arm'],p['actors'][a['case_id']],previous,p['questions'][a['case_id']] if a['role']=='reader' else None)
                if req!=expected:raise ValueError('request_or_parent')
                obj,u=normalize(raw,len(canonical(req).encode())+1024,a['role'])
                if u['generation_id'] in seen:raise ValueError('generation_reuse')
                seen.add(u['generation_id']);parents[a['id']]=obj;hashes[a['id']]=sha(raw)
                receipt=json.loads((out/(a['id']+'.receipt.json')).read_text())
                if receipt['request_sha256']!=sha(req) or receipt['response_sha256']!=sha(raw) or receipt['parent_response_sha256']!=(None if a['parent']is None else hashes[a['parent']]):raise ValueError('receipt_hash')
                r.update(status='valid',output=obj,response_sha256=sha(raw))
                if a['role']=='reader':
                    truth=gold[a['case_id']]['answer'];r.update(truth=truth,correct=obj['answer']==truth,false_certainty=truth=='UNKNOWN' and obj['answer']!='UNKNOWN',abstained=obj['answer']=='UNKNOWN')
            except Exception as e:r.update(status='invalid',failure_type=type(e).__name__)
        elif (out/(a['id']+'.started.json')).exists():r['status']='started_missing'
        rows.append(r)
    readers=[r for r in rows if r['role']=='reader'];cells=[];pairs=[]
    for block in (1,2):
        for arm in ('P','R'):
            rr=[r for r in readers if r['block']==block and r['arm']==arm];valid=sum(r['status']=='valid' for r in rr);correct=sum(r['correct']is True for r in rr)
            cells.append({'block':block,'arm':arm,'assigned':len(rr),'valid':valid,'correct':correct,'missing_or_invalid':len(rr)-valid,'all_assigned_accuracy_bounds':[correct/len(rr),(correct+len(rr)-valid)/len(rr)],'false_certainty':sum(r['false_certainty']is True for r in rr)})
        for cid in gold:
            pp=[r for r in readers if r['block']==block and r['case_id']==cid];by={r['arm']:r for r in pp}
            pairs.append({'block':block,'case_id':cid,'R_minus_P':int(by['R']['correct'])-int(by['P']['correct']) if all(by[x]['correct']is not None for x in ('P','R')) else None})
    competence=[]
    for block in (1,2):
        for family in sorted({r['family'] for r in readers}):
            rr=[r for r in readers if r['block']==block and r['arm']=='R' and r['family']==family];correct=sum(r['correct']is True for r in rr)
            competence.append({'block':block,'family':family,'correct':correct,'assigned':3,'interpretation_screen_passed':correct/3>=.8,'meaning':'source available plus handoff, not singleton; 3/3 required by coarse 80% screen'})
    audit=[]
    for family in sorted({r['family'] for r in readers}):
        for outcome in (True,False):
            rr=[r for r in readers if r['family']==family and r['correct']is outcome]
            audit.extend(sorted(rr,key=lambda r:hashlib.sha256(('B3-audit-v1:'+r['id']).encode()).hexdigest())[:2])
    disagreement=[]
    for cid in gold:
        for arm in ('P','R'):
            rr=[r for r in readers if r['case_id']==cid and r['arm']==arm];answers=[r.get('output',{}).get('answer') for r in rr]
            disagreement.append({'case_id':cid,'arm':arm,'answers':answers,'disagrees':len(set(answers))>1 if None not in answers else None})
    return {'native_assignments':len(rows),'reader_assignments':len(readers),'worlds':24,'shared_families':8,'independent_family_warning':'Two repeats and two policies are nested; eight authored templates constrain generalization.','cells':cells,'paired_differences':pairs,'source_available_competence':competence,'repeat_disagreement':disagreement,'audit_required_ids':[r['id'] for r in audit],'audit_max':32,'audit_complete':False,'rows':rows}
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('out');ap.add_argument('--gold',required=True);args=ap.parse_args();p=json.loads((Path(args.out)/'packet.json').read_text());r=analyze(p,args.out,json.loads(Path(args.gold).read_text()));print(json.dumps(r,indent=2))
