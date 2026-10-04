#!/usr/bin/env python3
"""Update only the editorial row owned by this bounded descriptive pilot."""
import json
from pathlib import Path
ROOT=Path(__file__).resolve().parents[4]
P='researchers/shadow/notes/wild-delete-return/'
row={
 'id':'wild-delete-return',
 'title':'Wiki deletion-return: bounded paired-window pilot',
 'documents':[P+'README.md',P+'FINDING.md'],
 'experiment_ids':['wild-delete-return'], 'registration_paths':[P+'experiment.json'],
 'evidence_confidence':{
   'score':1,
   'claim':'The predeclared 30-minute paired windows contain 83 observed saves before and 83 after first deletion on 2,728 eligible pages; 19 pages have a post-guard save.',
   'rationale':'All 5,144 selected page assignments, exclusions and windows were recomputed by separate same-author code. Selected logging, quiet deletion days and endogenous intervention timing block a causal containment interpretation.'},
 'sample_size_summary':'One selected incident export; 5,144 first-deletion pages, 2,728 eligible across 14 UTC-day clusters, 2,416 release-edge exclusions; 19,913 events and 14,591 revisions read. Pages are dependent; 83 before/83 after saves. Zero model calls.',
 'sources':[P+'PLAN.md',P+'results/A1/summary.json',P+'results/A1/reference-check.json',P+'POST-MORTEM.md'],
 'status_at_assessment':'complete_bounded_descriptive_null_no_scaling_or_causal_inference',
 'assessor':'shadow/sol-audit-gap','assessed_at':'2026-10-04',
 'source_commit':'473077421c01a8fa382f93bbb2f23f074ff29ec1'
}
if __name__=='__main__':
    path=ROOT/'experiments/evidence-metadata.json'
    data=json.loads(path.read_text())
    positions=[i for i,s in enumerate(data['studies']) if s['id']==row['id']]
    assert len(positions)<=1
    if positions:
        data['studies'][positions[0]]=row
    else:
        data['studies'].append(row)
    path.write_text(json.dumps(data,indent=2,ensure_ascii=True)+'\n')
    print('Updated wild-delete-return row only.')
