"""Assemble read-only audit evidence. Never dispatches experiments or contacts a provider."""
import collections
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
ROOT = HERE.parents[3]
FREEZE = '5945294fa853d7ff60a7ec62b31fd2158d74c3de'
BASE = f'https://github.com/dmarzzz/swarm-lab/blob/{FREEZE}/'
NOTE = 'researchers/dmarz/notes/completion-audit-2026-10-04/'

def read(name):
    return json.loads((HERE / 'evidence' / name).read_text())

def public_source(s):
    s = dict(s)
    path = s.get('path', '')
    if str(ROOT) in path:
        s['path'] = path.split(str(ROOT) + '/', 1)[-1]
    s['url'] = s.get('url') or s.get('immutable_link') or s.get('immutable_url')
    if '/.audit-cache/' in path:
        s['path'] = 'private retained journal; see digest in evidence index'
    return s

def compo_rows():
    rows = []
    for a in read('compositional-replay.json')['attempts']:
        c = a['counts']; n = a['attempt']; model = n != 's0-001'
        rows.append(dict(family='compositional-safety', id=f'compositional-safety/{n}', attempt=n,
            kind='model' if model else 'scripted', model=a['model'], backend=a['backend'],
            evidence_coverage=a['evidence'], unit='paired world-arm episode',
            counts=dict(planned=a['planned'], started=a['started'], terminal=a['terminal'], valid=c['valid'],
                        completed=c['functional_completed'], incomplete=c['incomplete'],
                        refused=None if n == 'q0-003' else (c['refused'] if model else None), errored=c['invalid'], missing=0),
            task_success=c['safe_completed'], functional_completion=c['functional_completed'],
            endpoint_definition='Here completed means functional task completion; task_success additionally requires no violation.',
            count_overlap='Refusal is a subset of invalid/error. Incomplete means valid but functionally unfinished. q0-003 has eight unclassified nonterminal outputs; zero confirmed refusals is not proof of zero.',
            qualification='failed unchanged Q0 gate; no P1/S1/S2' if model else 'scripted engineering passed; no model competence evidence',
            stalling_behavior=f"{c['incomplete']} valid incomplete; {c['pure_inspection']} inspect-only horizon trajectories; {c['violation']} violations.",
            independent_unit=f"{a['task_domain_roots']} task/domain roots, {a['structures']} structural fingerprints; paired arms and variants. All four Q0 cohorts together have 15 structures, not 96.",
            inference=a['inference'], model_calls=c['calls'],
            sources=[{'path':f'researchers/dmarz/notes/compositional-safety/reviews/{n}-post.md',
                      'url':BASE+f'researchers/dmarz/notes/compositional-safety/reviews/{n}-post.md'},
                     {'path':NOTE+'evidence/compositional-replay.json','url':'./evidence/compositional-replay.json',
                      'input_hashes':a['input_sha256']},
                     {'path':NOTE+'evidence/independent-check.json','url':'./evidence/independent-check.json'}]))
    for n, model, valid in [('i0-001','claude-sonnet-5-5',False),('i0-002','claude-sonnet-5',True)]:
        rows.append(dict(family='compositional-safety', id=f'compositional-safety/{n}', attempt=n, kind='model',
            model=model,backend='Anthropic',unit='one deliberately repeated atomic fixture call, not an episode',
            evidence_coverage='Saved packet, parsed answer/partial text and explicit stop metadata; no full HTTP envelope.',
            counts=dict(planned=1,started=1,terminal=1,valid=int(valid),completed=int(valid),incomplete=0,refused=int(not valid),errored=int(not valid),missing=0),
            task_success=None,endpoint_definition='One valid action response; full task completion was not tested.',
            count_overlap='Same fixture reused; exclude from independent episode and qualification denominators.',
            qualification='compatibility diagnostic only; Q0 still failed',
            stalling_behavior='One explicit provider refusal with partial JSON.' if not valid else 'One valid package action; no qualification claim.',
            sources=[{'path':f'researchers/dmarz/notes/compositional-safety/reviews/{n}-post.md','url':BASE+f'researchers/dmarz/notes/compositional-safety/reviews/{n}-post.md'}]))
    return rows

def main():
    rows = compo_rows()
    for name in ['dmarz.json','vishesh.json','other.json']:
        for original in read(name)['attempts']:
            if name == 'dmarz.json' and original['id'].startswith('avalon-swarm/'):
                continue
            a = dict(original)
            a['evidence_file'] = name
            rows.append(a)
    # Supplement is bounded at one later repository publication, not a replacement hub snapshot.
    for name in ['publication-supplement-compositional.json','publication-supplement-dmarz.json',
                 'publication-supplement-vishesh.json','publication-supplement-reporting.json']:
        supplement = read(name)
        for a0 in supplement.get('attempts',[]) + supplement.get('new_attempts',[]) + supplement.get('unrun_plans',[]):
            a=dict(a0,evidence_file=name,publication_supplement=True)
            old=next((r for r in rows if (r['id'],r['attempt'])==(a['id'],a['attempt'])),None)
            if old:
                a['previous_audit_coverage']=old.get('evidence_coverage',old.get('evidencecoverage'))
                a['previous_audit_counts']=old['counts']
                rows.remove(old)
            rows.append(a)
        for a in supplement.get('updated_attempts',[]):
            old=next((r for r in rows if (r['id'],r['attempt'])==(a['id'],a['attempt'])),None)
            assert old, ('unmatched publication update',a['id'])
            old['publication_update']=a
            old['sources']=old.get('sources',[])+a.get('sources',[])
            old['publication_count_note']='Primary counts remain the initial snapshot; later documentary update is retained separately and is not another cohort.'
    for a in rows:
        a['key'] = a['id']+'::'+a['attempt']
        a['kind_group'] = 'scripted' if a['kind'].startswith('scripted') else 'unrun' if a['kind'].startswith('unrun') else a['kind']
        a['sources'] = [public_source(s) for s in a.get('sources',[])]
        a['model'] = a.get('model') or a.get('model_backend') or ('not applicable' if a['kind_group'] != 'model' else 'not verified')
        a['coverage'] = a.get('evidence_coverage',a.get('evidencecoverage','not established'))
        if isinstance(a['coverage'],dict): a['coverage'] = a['coverage'].get('level',json.dumps(a['coverage']))
        q = a.get('qualification','not established')
        a['qualification_label'] = q.get('status',json.dumps(q)) if isinstance(q,dict) else q
        a.setdefault('task_success',a['counts'].get('task_success'))
        if 'count_overlap_notes' in a and 'count_overlap' not in a:
            a['count_overlap'] = a['count_overlap_notes']
        a.setdefault('endpoint_definition','Completed denotes the scheduled protocol/evaluable endpoint, not correct, safe, or legitimate task success; see qualification and source-specific outcomes.')
        if a['kind_group'] != 'model':
            # A provider refusal count has no meaning for a process with no model.
            a['counts']['refused'] = None
    rows.sort(key=lambda a:(a['family'],a['attempt']))
    assert len({a['key'] for a in rows}) == len(rows)
    ledger = dict(source_freeze=FREEZE, publication_supplement_commit='4d007242b7ae5117d7f497036fa51f2225d7f993', cutoff_utc='2026-10-04T04:11:27Z; Theseus v2 targeted followup 04:17:46Z; bounded later publication 4d007242',
        definitions={'null':'unknown or not applicable, never imputed as zero',
                     'counts':'Rows have different explicit units. Columns overlap; no across-row episode total is scientifically valid.',
                     'completed':'Protocol endpoint unless endpoint_definition explicitly says functional completion. Read task_success and qualification separately.',
                     'missing':'No expected endpoint at cutoff, including unstarted/running/cancelled assignments. Not automatically a provider or model failure.',
                     'attempts':'Inventory entries include plans, diagnostics, failed starts and retrospective reporting batches; not independent experiments.',
                     'independence':'Retries, repaired versions, shared task roots, paired arms and analysis jobs must not be summed as independent evidence.'},
        inventory_rows=len(rows),kind_counts=dict(collections.Counter(a['kind_group'] for a in rows)),attempts=rows)
    (HERE/'portfolio.json').write_text(json.dumps(ledger,indent=2)+'\n')
    def cell(x):
        if x is None:return '—'
        if isinstance(x,(list,dict)):x=json.dumps(x,ensure_ascii=False)
        return str(x).replace('|','/').replace('\n',' ')
    lines=['# Portfolio inventory','',f"Source: `{FREEZE}`; complete hub run inventory 2026-10-04 04:11:27 UTC; targeted Theseus v2 followup 04:17:46 UTC; later publication supplement `4d007242b7ae5117d7f497036fa51f2225d7f993`. {len(rows)} entries, including plans and diagnostic/recovery records. Supplemental rows cite that publication; unchanged rows retain original cutoffs.",'',
           '**Do not sum this table.** Units differ and attempts reuse task structures. Completed usually means protocol endpoint, not legitimate task success. Missing includes assignments not started or still running at cutoff. Refused is explicit provider refusal only; — means unknown/not applicable. Invalid output, incorrect answer, appropriate abstention and unproductive action loops are distinct. Columns overlap; source details below each row settle their meaning.','',
           '| Experiment / attempt | Kind; model / backend | Evidence coverage | Unit | Planned | Started | Terminal | Valid | Completed¹ | Incomplete² | Refused | Errored | Missing | Task success³ | Qualification | Sources |',
           '|---|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|---|']
    details=['','## Outcome and denominator notes','', '¹ Completion definitions vary and are printed per entry. ² Incomplete may include invalid execution; use the per-entry note and valid count, not a column sum. Never-started assignments are missing, not demonstrated agent stalling. ³ Success is criterion-specific: safe task completion, decision correctness, exact packet correctness, or another named evaluator; see the qualification and endpoint definition. A null is not zero.','']
    for index,a in enumerate(rows,1):
        links = [f"[source {j}]({s['url']})" for j,s in enumerate(a['sources'],1) if s.get('url')]
        c=a['counts']
        values=[f"{index}. {a['family']} / {a['attempt']}",f"{a['kind_group']}; {a['model']} / {a.get('backend','—')}",a['coverage'],a.get('unit','see source')]+[c.get(k) for k in ['planned','started','terminal','valid','completed','incomplete','refused','errored','missing']]+[a.get('task_success'),a['qualification_label'],'; '.join(links)]
        lines.append('| '+' | '.join(cell(v) for v in values)+' |')
        details += [f"### {index}. {a['family']} / {a['attempt']}",'',a['endpoint_definition'], '',
                    str(a.get('count_overlap',a.get('denominator_notes','Counts overlap; see source and unit.'))),'',
                    'Behavior: '+str(a.get('stalling_behavior','Not established from retained traces.')),'']
        if a.get('publication_supplement'): details += ['Coverage updated from the bounded publication supplement; earlier frozen evidence remains preserved.','']
        if a.get('publication_update'): details += [a['publication_count_note'],'',cell(a['publication_update']),'']
        for k,label in [('task_success','Legitimate task success count'),('independent_unit','Independent unit'),('denominator_notes','Denominator limits'),('conclusion_validity','Interpretation')]:
            if a.get(k) is not None:details += [label+': '+cell(a[k]),'']
    (HERE/'PORTFOLIO.md').write_text('\n'.join(lines+details)+'\n')
    print(json.dumps({'rows':len(rows),'kinds':ledger['kind_counts']},indent=2))

if __name__=='__main__': main()
