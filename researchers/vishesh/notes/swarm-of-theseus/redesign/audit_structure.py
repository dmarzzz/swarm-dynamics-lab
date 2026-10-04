"""Retrospective structural audit of saved S1 outcomes; makes no model calls."""
import collections,json,sys
from pathlib import Path

def audit(root):
    rows=[json.loads(p.read_text()) for p in sorted(Path(root).glob('*/outcome.json'))]
    assert len(rows)==36 and all(r['status']=='completed' for r in rows)
    means={a:sum(r['final_accuracy'] for r in rows if r['arm']==a)/6 for a in sorted({r['arm'] for r in rows})}
    edges=[p for r in rows if r['arm'] in ('mentor','both') for access in r['access'] for p in access['parent_ids']]
    requests=[]
    for p in sorted(Path(root).glob('*/events.jsonl')):
        for line in p.read_text().splitlines():
            e=json.loads(line)
            if e.get('kind')=='request' and e.get('operation')=='solve': requests.append(e)
    xor=[e for e in requests if e['request']['observation']['scenario'] in ('seed-bank','repair-dock')]
    signatures={tuple(c['assay']) for e in xor for c in e['request']['observation']['cases']}
    assert all({tuple(c['assay']) for c in e['request']['observation']['cases']}==signatures for e in xor)
    assert len(signatures)==4 and len(edges)==36
    assert len(requests)==36*6*3
    repair_post=[e for e in requests if e['request']['observation']['scenario']=='repair-dock' and e['step']>=4]
    return {'type':'retrospective structural audit, not a new experiment','outcomes':len(rows),'mean_accuracy':means,
      'mentor_parent_edges':len(edges),'mentor_edges_from_original_founders':sum(p.startswith('founder-') for p in edges),
      'mentor_edges_from_descendants':sum(not p.startswith('founder-') for p in edges),
      'distinct_binary_feature_vectors':len(signatures),'binary_vectors_per_solve':4,
      'repair_post_change_solve_requests':len(repair_post),'repair_post_change_requests_with_explicit_bulletin':sum('current_bulletin' in e['request']['observation'] for e in repair_post),
      'interpretation':'Task accuracy does not identify emergent culture. Mentoring has one founder-to-newcomer hop; binary test cases recycle the full four-vector domain; repair actors receive the updated rule.'}
if __name__=='__main__':
    result=audit(sys.argv[1]);Path(sys.argv[2]).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result))
