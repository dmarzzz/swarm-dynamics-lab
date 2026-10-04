"""Strict policy/citation checks, with a separate exhaustive reference computation."""
import importlib.util,json
from design import ROOT,SOURCES,candidates
spec=importlib.util.spec_from_file_location('r1_reference',ROOT/'r1/scoring.py');ref=importlib.util.module_from_spec(spec);spec.loader.exec_module(ref)
def policy_score(a,result):
    v=result.get('value'); mapping=v.get('mapping') if isinstance(v,dict) else None
    valid=isinstance(v,dict) and set(v)=={'mapping','support'} and isinstance(mapping,dict) and set(mapping)==set('AB') and all(type(s) is str and s in SOURCES for s in mapping.values()) and len(set(mapping.values()))==2 and not result.get('error')
    support=v.get('support') if isinstance(v,dict) else None
    contract=valid and isinstance(support,dict) and set(support)==set('AB')
    evidence={}
    for cls in 'AB':
        ids=support.get(cls) if isinstance(support,dict) else None
        rows=[h for h in a['history'] if h['case']['class']==cls]
        known={h['case']['id'] for h in rows}
        shape=isinstance(ids,list) and bool(ids) and all(type(i) is str and i in known for i in ids) and len(ids)==len(set(ids))
        contract=bool(contract and shape)
        cited=[h for h in rows if shape and h['case']['id'] in ids]
        evidence[cls]=bool(valid and shape and candidates(cited,cls,a['context'])==[mapping[cls]])
    return {'mapping_valid':bool(valid),'contract_valid':bool(contract),'exact_mapping':bool(valid and mapping==a['rule']),'support_valid':all(evidence.values()),'support_by_class':evidence,'mapping':mapping if valid else None,'qualified':bool(contract and mapping==a['rule'] and all(evidence.values()))}

def policy_reference(a,result):
    try:v=json.loads(result['raw_text'])
    except (ValueError,TypeError,KeyError):return {'exact_mapping':False,'qualified':False}
    if not isinstance(v,dict) or set(v)!= {'mapping','support'} or result.get('error'):return {'exact_mapping':False,'qualified':False}
    m=v['mapping']; supports=v['support']; good=isinstance(m,dict) and set(m)=={'A','B'} and all(isinstance(x,str) and x in ('probe','ledger','canary') for x in m.values()) and len(set(m.values()))==2
    exact=good and m==a['rule']; ok=good and isinstance(supports,dict) and set(supports)=={'A','B'}
    for cls in ('A','B'):
        ids=supports.get(cls) if isinstance(supports,dict) else None
        hs={h['case']['id']:h for h in a['history'] if h['case']['class']==cls}
        if not isinstance(ids,list) or not ids or any(not isinstance(i,str) or i not in hs for i in ids) or len(set(ids))!=len(ids):ok=False;continue
        possible=[]
        for s in ('probe','ledger','canary'):
            consistent=True
            for i in ids:
                h=hs[i];e=h['case']['evidence'][s];truth=('activated' if e['signal'] else 'quiet') if a['context']=='incident' else ('ship' if e['signal'] and e['fresh'] else 'hold')
                consistent &= h['outcome']==truth
            if consistent:possible.append(s)
        ok=ok and possible==[m[cls]]
    return {'exact_mapping':bool(exact),'qualified':bool(exact and ok)}

def action_score(a,result):return ref.reference(a,result)[0]
