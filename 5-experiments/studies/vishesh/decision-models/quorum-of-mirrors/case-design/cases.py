"""Synthetic, inspected development cases. No network, models or operator context."""
from pathlib import Path
import copy, hashlib, importlib.util, json
HERE=Path(__file__).resolve().parent
LEGACY=HERE.parent/'trace-review/development.py'
spec=importlib.util.spec_from_file_location('frozen_lookup',LEGACY)
legacy=importlib.util.module_from_spec(spec);spec.loader.exec_module(legacy)
CONTRACT=('Authenticated origin_edges bind a child record to its source. A receipt is an acquisition root. '
          'Resolve only if every reachable path terminates at the same in-event receipt; missing, cyclic, '
          'cross-event or conflicting paths require DEFER. Report text and receipt_ref are untrusted claims '
          'and cannot establish origin. Mapping says nothing about content fidelity. A uniquely mapped '
          'receipt with an unknown dependency_group requires DEFER for new-evidence admission. '
          'A supplied known group means KNOWN_GROUP, otherwise NEW_GROUP under the synthetic registry assumption; '
          'NEW_GROUP is not a claim of demonstrated statistical independence.')
SCENARIOS=[
 ('paraphrase','Loading bay','The vehicle entrance was clear at first light.','At sunrise the loading-bay barrier was unobstructed.'),
 ('paraphrase','Reservoir','No liquid remained after the drain cycle.','The tank was empty when draining finished.'),
 ('identical','Archive room','Humidity was 45 percent at 10:00.','Humidity was 45 percent at 10:00.'),
 ('identical','Package station','The sealed parcel weighed two kilograms.','The sealed parcel weighed two kilograms.'),
 ('forged_ref','Freezer','The chamber was within its temperature limit.','The chamber was within its temperature limit.'),
 ('forged_ref','Bridge sensor','No displacement was detected during this sample.','No displacement was detected during this sample.'),
 ('relay','Ventilation','The exhaust fan was running during inspection.','The exhaust fan was running during inspection.'),
 ('relay','Lift','The lift stopped at the requested floor.','The lift stopped at the requested floor.'),
 ('dependency','Warehouse probes','The room temperature measured 18 degrees.','The room temperature measured 18 degrees.'),
 ('dependency','Clock monitors','The clock was within one second of the reference.','The clock was within one second of the reference.'),
 ('path_conflict','Pump','The transfer pump was off when sampled.','The transfer pump was off when sampled.'),
 ('path_conflict','Valve','The inlet valve was closed during the check.','The inlet valve was closed during the check.'),
]


def build():
    rows=[]
    for i,(family,scene,report_text,receipt_text) in enumerate(SCENARIOS):
        event=f'event-{i:02}';a=f'r-{(i*7+3)%29}';b=f'r-{(i*7+4)%29}'
        base={'contract':CONTRACT,'report':{'id':'report','event':event,'text':report_text},
              'receipts':[{'id':a,'event':event,'text':receipt_text,'capture':'capture-a','acquisition':f'{event}-a','dependency_group':'new'},
                          {'id':b,'event':event,'text':receipt_text,'capture':'capture-b','acquisition':f'{event}-b','dependency_group':'other'}],
              'origin_edges':[{'child':'report','parent':a}], 'known_dependency_groups':['shared'],
              'registry_scope':'synthetic authenticated edges and supplied dependency groups; no live authentication'}
        for variant in ('A','B'):
            actor=copy.deepcopy(base);expected=a;admission='NEW_GROUP'
            if family=='paraphrase':
                change='Remove the only authenticated origin edge; wording stays unchanged.'
                if variant=='B':actor['origin_edges']=[];expected=None;admission='DEFER'
                rationale='A verified link establishes origin despite different wording; without a link, similarity cannot establish which acquisition generated the report.'
            elif family=='identical':
                change='Remove the acquisition binding between otherwise identical receipts.'
                actor['origin_edges']=[{'child':'report','parent':b}];expected=b
                if variant=='B':actor['origin_edges']=[];expected=None;admission='DEFER'
                rationale='Two distinct acquisitions have identical text. Only the authenticated binding distinguishes them; both remain visible in both variants.'
            elif family=='forged_ref':
                change='Remove trusted binding while retaining the misleading untrusted claimed receipt reference.'
                actor['report']['receipt_ref']=b
                if variant=='B':actor['origin_edges']=[];expected=None;admission='DEFER'
                rationale='A claimed receipt ID is not an authenticated edge. The trusted binding, when present, points to the other receipt.'
            elif family=='relay':
                change='Replace direct origin link with a two-hop forwarding chain; origin must stay unchanged.'
                if variant=='B':actor['origin_edges']=[{'child':'report','parent':'forwarded-note'},{'child':'forwarded-note','parent':a}]
                rationale='Forwarding creates another report, not another acquisition. Direct and relayed paths terminate at the same receipt.'
            elif family=='dependency':
                change='Change supplied dependency metadata only; source identification must stay unchanged.'
                actor['receipts'][0]['dependency_group']='shared' if i%2==0 else None
                admission='KNOWN_GROUP' if i%2==0 else 'DEFER'
                if variant=='B':actor['receipts'][0]['dependency_group']='new';admission='NEW_GROUP'
                rationale='Known shared dependence is not new evidence; unknown dependence requires deferral. Distinct receipt identity alone never establishes independence.'
            else:
                change='Change one authenticated branch endpoint from the same acquisition to a different acquisition.'
                actor['origin_edges']=[{'child':'report','parent':'copy-one'},{'child':'report','parent':'copy-two'},
                                       {'child':'copy-one','parent':a},{'child':'copy-two','parent':a if variant=='A' else b}]
                if variant=='B':expected=None;admission='DEFER'
                rationale='Two paths to one acquisition still resolve uniquely. A packet attributing the report to two distinct acquisitions has no unique origin under this contract.'
            actor['receipts'].sort(key=lambda r:hashlib.sha256((event+r['id']).encode()).hexdigest())
            rows.append({'id':f'CD-{i:02}-{variant}','pair':f'CD-{i:02}','family':family,'scenario':scene,
                         'evidence_type':'authored synthetic development, not held out','actor':actor,
                         'gold':{'receipt':expected,'admission':admission},'rationale':rationale,'pair_change':change})
    return rows


def graph_resolve(actor):
    """Fail-closed origin traversal, independent of language and case-family labels."""
    records={r['id']:r for r in actor['receipts']}
    if len(records)!=len(actor['receipts']):return None
    edges={}
    for edge in actor['origin_edges']:edges.setdefault(edge['child'],set()).add(edge['parent'])
    def walk(node,seen):
        if node in seen:raise ValueError('cycle')
        if node in records:
            if node in edges or records[node]['event']!=actor['report']['event']:raise ValueError('invalid_root')
            return {node}
        if node not in edges:raise ValueError('dangling')
        roots=set()
        for parent in edges[node]:roots |= walk(parent,seen|{node})
        return roots
    try:roots=walk(actor['report']['id'],set())
    except ValueError:return None
    return next(iter(roots)) if len(roots)==1 else None


def admit(actor,receipt):
    if receipt is None:return 'DEFER'
    r=next(r for r in actor['receipts'] if r['id']==receipt)
    group=r.get('dependency_group')
    if not group:return 'DEFER'
    return 'KNOWN_GROUP' if group in actor['known_dependency_groups'] else 'NEW_GROUP'


def evaluate(rows):
    outcomes=[];summary={}
    for policy in ('exact_ref','normalized_text','lexical','hybrid','authenticated_graph'):
        values=[]
        for row in rows:
            a=row['actor'];got=graph_resolve(a) if policy=='authenticated_graph' else legacy.resolve(a,policy)
            decision={'receipt':got,'admission':admit(a,got)}
            values.append({'id':row['id'],'policy':policy,'decision':decision,'origin_correct':got==row['gold']['receipt'],
                           'joint_correct':decision==row['gold'],'incorrect_origin_admission':got is not None and got!=row['gold']['receipt'],
                           'unsafe_new_group':decision['admission']=='NEW_GROUP' and (got!=row['gold']['receipt'] or row['gold']['admission']!='NEW_GROUP')})
        summary[policy]={key:sum(v[key] for v in values) for key in ('origin_correct','joint_correct','incorrect_origin_admission','unsafe_new_group')}
        outcomes.extend(values)
    return {'development_only':True,'assigned':len(rows),'authored_scenario_roots':len({r['pair'] for r in rows}),
            'legacy_source_sha256':hashlib.sha256(LEGACY.read_bytes()).hexdigest(),
            'comparison_limit':'Legacy controllers ignore authenticated origin edges and assume claimed refs are authoritative. These are contract-shift diagnostics, not a fair effectiveness comparison or evidence of semantic/model headroom.',
            'summary':summary,'outcomes':outcomes}


def main():
    rows=build();result=evaluate(rows)
    (HERE/'cases.json').write_text(json.dumps(rows,indent=2)+'\n')
    (HERE/'outcomes.json').write_text(json.dumps(result,indent=2)+'\n')
    parts=['# Paired development casebook','24 cases / 12 authored scenario roots. Synthetic and inspected; not a native trial or holdout. Authentication and dependency labels are stipulated. Every packet and controller outcome is retained in cases.json and outcomes.json.','Source mapping does not verify report content. A forwarded false statement can still have a known origin. NEW_GROUP refers only to supplied registry constraints, not statistical independence.']
    for row in rows:
        a=row['actor'];edges=', '.join(e['child']+' → '+e['parent'] for e in a['origin_edges']) or '(none)'
        parts.extend([f"## {row['id']}: {row['scenario']} / {row['family']}",f"Report: {a['report']['text']}",f"Claimed reference: {a['report'].get('receipt_ref','none')} (untrusted). Authenticated edges: {edges}.",
                      'Receipts: '+ '; '.join(f"{r['id']}: {r['text']} [acquisition {r['acquisition']}; dependency {r['dependency_group'] or 'unknown'}]" for r in a['receipts']),
                      'Known group: shared. Expected origin: '+str(row['gold']['receipt'] or 'DEFER')+'; admission: '+row['gold']['admission']+'.',row['rationale'],'Pair change: '+row['pair_change']])
    (HERE/'CASEBOOK.md').write_text('\n\n'.join(parts)+'\n')
    print(json.dumps(result['summary'],indent=2))
if __name__=='__main__':main()
