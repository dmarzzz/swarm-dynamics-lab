"""Reviewer arithmetic on completed S0 and generic bit patterns; no S1 generator/seeds."""
from pathlib import Path
from itertools import product
import json, hashlib
ROOT=Path(__file__).resolve().parents[4]
BASE=ROOT/'researchers/vishesh/notes/decision-models/quorum-of-mirrors'
OUT=Path(__file__).resolve().parent
m=json.loads((BASE/'results/QM-S0-02/manifest.json').read_text())
receipts=[json.loads(s) for s in (BASE/'results/QM-S0-02/receipts.jsonl').read_text().splitlines()]
ri={r['id']:r for r in receipts}
rows=[]
for a in m['assignments']:
    r=ri[a['id']]
    digest=hashlib.sha256(json.dumps(a['request'],sort_keys=True,separators=(',',':')).encode()).hexdigest()
    assert digest==a['request_sha256']==r['request_sha256']
    reports=a['request']['state']['reports']
    roots={x['visible_root']:x['bit'] for x in reports}
    assert len(roots)==3
    label=lambda ones,n:'ONE' if 2*ones>n else 'ZERO'
    oracle=label(sum(roots.values()),3)
    naive=label(sum(x['bit'] for x in reports),9)
    assert oracle==a['expected']
    choice=r['response']['answers']['decision']['choice']
    rows.append(dict(id=a['id'],case=a['case'],oracle=oracle,naive=naive,choice=choice,conflict=naive!=oracle,correct=choice==oracle))
# Exhaustive algebra over the stated supports. No random roots are generated.
patterns=[]
for bits in product((0,1),repeat=3):
    for favored in range(3):
        for shape in ('balanced','skew'):
            copies=[3,3,3] if shape=='balanced' else [7 if i==favored else 1 for i in range(3)]
            ones=sum(b*c for b,c in zip(bits,copies))
            prediction=int(ones in (2,6,8,9))
            root_majority=int(sum(bits)>=2)
            assert prediction==root_majority
            patterns.append(dict(bits=bits,favored=favored,shape=shape,ones=ones,majority=root_majority))
strata={name:{'calls':sum(r['conflict']==flag for r in rows),'correct':sum(r['correct'] for r in rows if r['conflict']==flag)} for name,flag in [('conflict',True),('agreement',False)]}
result={'scope':'Completed S0 plus generic exhaustive bit/copy arithmetic; no reserved S1 worlds opened','model_calls':0,'s0':{'calls':len(rows),'model_correct':sum(r['correct'] for r in rows),'naive_correct':sum(not r['conflict'] for r in rows),'root_rule_correct':32,'strata':strata,'errors':[r for r in rows if not r['correct']]},'observable_count_rule':{'enumerations':len(patterns),'correct':len(patterns),'predict_ONE_for_report_one_counts':[2,6,8,9],'needs_root_ids':False,'needs_copy_shape_label':False,'assumptions':'Three roots, common q>0.5, fair truth prior, multiplicities either (3,3,3) or a permutation of (7,1,1). This is MAP agreement, not perfect world-truth accuracy.'},'budget':{'current_new_calls':544,'current_total_calls':576,'current_total_reserved_usd':576*.001344,'optional_matched_pooled_extra_calls':48,'optional_total_calls':624,'optional_total_reserved_usd':624*.001344}}
(OUT/'quorum-arithmetic.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
