#!/usr/bin/env python3
"""Upsert only this lane's editorial evidence row; then run the shared renderer."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
PREFIX = 'researchers/shadow/notes/wild-evidence-depth/'
ROW = {
    'id': 'wild-evidence-depth',
    'title': 'SwarmTraces evidence depth: fixed-export census',
    'documents': [PREFIX + 'README.md', PREFIX + 'FINDING.md'],
    'experiment_ids': ['wild-evidence-depth'],
    'registration_paths': [PREFIX + 'experiment.json'],
    'evidence_confidence': {
        'score': 1,
        'claim': 'In this selected release, 7,733/91,037 payload artifacts have a direct response child; response-link coverage varies with artifact length.',
        'rationale': 'Complete corpus census, graph fixtures and separate same-author arithmetic agree. Selection, response semantics and original event independence are unknown; no success rate or causal inference is supported.'
    },
    'sample_size_summary': 'Observed: one selected incident corpus; 189,579/189,579 rows analyzed, 91,037 payloads, 7,733 response-linked payloads; zero parse failures/exclusions. Rows are dependent artifacts, not independent trials. Zero model calls.',
    'sources': [PREFIX + 'PLAN.md', PREFIX + 'results/summary.json', PREFIX + 'results/reference-check.json', PREFIX + 'POST-MORTEM.md'],
    'status_at_assessment': 'complete_descriptive_census_no_execution_or_success_inference',
    'assessor': 'shadow/sol-audit-gap', 'assessed_at': '2026-10-04',
    'source_commit': 'd7301e98cefafe96f1a23c3d257beab06fea129c'
}

if __name__ == '__main__':
    path = ROOT / 'experiments/evidence-metadata.json'
    data = json.loads(path.read_text())
    positions = [i for i, row in enumerate(data['studies']) if row['id'] == ROW['id']]
    assert len(positions) <= 1
    if positions:
        data['studies'][positions[0]] = ROW
    else:
        data['studies'].append(ROW)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=True) + '\n')
    print('Updated only wild-evidence-depth evidence row.')
