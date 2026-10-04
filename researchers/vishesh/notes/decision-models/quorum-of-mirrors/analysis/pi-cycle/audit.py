"""Retrospective Q1 diagnosis and prospective software verification; no network or model calls."""
from collections import Counter
import hashlib
import html
import itertools
import json
import math
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
STUDY=HERE.parents[1]
sys.path.insert(0,str(STUDY))
from qualification import validate_response, digest


def exact_trusted_rule(reports):
    """Scoped to exactly three binary sources with equal reliability > .5; otherwise refuse."""
    roots={}
    if not isinstance(reports,list) or not reports:raise ValueError('reports_required')
    for report in reports:
        root=report.get('visible_root');value=report.get('value');q=report.get('q')
        if not isinstance(root,str) or not root:raise ValueError('trusted_lineage_required')
        if type(value) is not int or value not in (0,1):raise ValueError('binary_observation_required')
        if type(q) not in (int,float) or not math.isfinite(q) or not .5<q<1:raise ValueError('reliability_outside_scope')
        observation=(value,q)
        if root in roots and roots[root]!=observation:raise ValueError('inconsistent_source')
        roots[root]=observation
    if len(roots)!=3:raise ValueError('three_sources_required')
    if len({q for value,q in roots.values()})!=1:raise ValueError('equal_reliability_required')
    return 'ONE' if sum(value for value,q in roots.values())>=2 else 'ZERO'


def verify_rule():
    checked=0
    for bits,q,counts in itertools.product(itertools.product((0,1),repeat=3),(.65,.8),itertools.product(range(1,8),repeat=3)):
        reports=[{'visible_root':f's{i}','value':bits[i],'q':q} for i in range(3) for _ in range(counts[i])]
        # Independently compute likelihood using the three generating observations, never the dedup code.
        p_one=math.prod(q if bit else 1-q for bit in bits)
        p_zero=math.prod(1-q if bit else q for bit in bits)
        expected='ONE' if p_one>p_zero else 'ZERO'
        assert exact_trusted_rule(reports)==expected
        checked+=1
    return {'configurations':checked,'mismatches':0,'evidence_type':'exhaustive software verification; not model observations or population n'}


def audit():
    folder=STUDY/'results/QM-Q1-02'
    m=json.loads((folder/'manifest.json').read_text())
    receipts=[json.loads(line) for line in (folder/'receipts.jsonl').read_text().splitlines() if line]
    accounting=[json.loads(line) for line in (folder/'accounting.jsonl').read_text().splitlines() if line]
    assignments={row['id']:row for row in m['assignments']};by={r['id']:r for r in receipts};billing={r['id']:r for r in accounting}
    assert len(assignments)==len(by)==len(billing)==len(receipts)==len(accounting)==16
    assert set(assignments)==set(by)==set(billing)
    rows=[];actual=0
    for ident,assignment in assignments.items():
        receipt=by[ident];assert receipt['status']=='complete' and receipt['request_sha256']==assignment['request_sha256']
        assert digest(assignment['request'])==assignment['request_sha256']==billing[ident]['request_sha256']
        response=validate_response(receipt['response']);assert response['usage']==billing[ident]['usage']
        actual+=response['usage']['cost']
        if assignment['lineage']!='full':continue
        state=assignment['request']['state'];target=exact_trusted_rule(state['reports'])
        assert target==assignment['expected']
        reports=state['reports'];report_choice='ONE' if sum(r['value'] for r in reports)>len(reports)/2 else 'ZERO'
        priors=Counter(r['choice'] for r in state['prior_decisions'] if r.get('status')=='available')
        prior_choice=priors.most_common(1)[0][0]
        rows.append({'id':ident,'context':assignment['context'],'q':assignment['q'],'target':target,
            'native_choice':response['choice'],'report_majority':report_choice,'prior_majority':prior_choice,
            'prior_choice_counts':dict(priors),'correct':response['choice']==target,
            'signals_confounded':report_choice==prior_choice and report_choice!=target})
    assert len(rows)==8
    source_refs={str((folder/name).relative_to(STUDY)):hashlib.sha256((folder/name).read_bytes()).hexdigest() for name in ('manifest.json','receipts.jsonl','accounting.jsonl','summary.json')}
    return {'analysis':'retrospective; no new native run','native_attempt':'QM-Q1-02','assigned':16,'started':16,'valid':16,'graded':8,
        'ungraded_partial':8,'correct':sum(r['correct'] for r in rows),'confounded_cases':sum(r['signals_confounded'] for r in rows),
        'known_attempt_actual_usd':round(actual,12),'rows':rows,'source_sha256':source_refs,'software_verification':verify_rule(),
        'disposition':'complete_valid_result; park D1; no M1/C1','mechanism_identified':False,
        'reason':'Every D1 result retains exact source-aware arithmetic as the practical choice on this complete trusted-lineage grammar.'}


def save():
    result=audit();(HERE/'audit.json').write_text(json.dumps(result,indent=2)+'\n')
    columns=('id','context','q','target','native_choice','report_majority','prior_majority')
    table='<table><tr>'+''.join('<th>'+html.escape(k)+'</th>' for k in columns)+'</tr>'+''.join('<tr>'+''.join('<td>'+html.escape(str(row[k]))+'</td>' for k in columns)+'</tr>' for row in result['rows'])+'</table>'
    (HERE/'cases.html').write_text('<!doctype html><meta charset="utf-8"><title>Quorum saved-data decision audit</title><style>body{font:16px system-ui;margin:2rem;max-width:1100px}table{border-collapse:collapse}td,th{border:1px solid #bbb;padding:.5rem}h1{font-size:26px}</style><h1>Quorum: the failure is real; its cause is confounded</h1><p>Retrospective saved evidence. Q1-02: 16 valid / 16 assigned, 0 correct / 8 graded. Eight partial-lineage cases are ungraded. No new model calls.</p><p>In every graded case, report-count and prior-choice majorities point to the same wrong answer. This cannot establish which one the model followed. Target uses exact source-aware arithmetic, not a sampled hidden truth.</p>'+table+'<h2>Engineering decision</h2><p>For this synthetic, complete trusted-lineage grammar, deduplicate and compute exact MAP directly. All 5,488 software configurations match an independently calculated likelihood reference. These are software checks, not native observations or independent worlds. Reject missing or contradictory provenance instead of pretending it is trusted.</p><p>D1 remains unrun and is parked because its possible outcomes do not change that decision. The cause of the native errors, real-world source matching and swarm efficacy remain unresolved.</p>')
    print(json.dumps({k:v for k,v in result.items() if k not in ('rows','source_sha256')},indent=2))

if __name__=='__main__':save()
