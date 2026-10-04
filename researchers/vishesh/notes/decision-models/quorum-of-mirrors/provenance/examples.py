"""Render named developer fixtures, never native/model evidence."""
import copy
import html
import json
from pathlib import Path
from gate import decide
from test_gate import valid, split_merge_attack


def main():
    cases=[]
    def add(name,reports,registry,verified=True):
        values={r['declared_root']:r['value'] for r in reports}
        naive=('ONE' if sum(values.values())>=2 else 'ZERO') if len(values)==3 else 'OUTSIDE SCOPE'
        cases.append({'case':name,'evidence_type':'constructed developer fixture','declared_label_choice':naive,
                      'gate':decide(reports,registry,registry_verified=verified)})
    reports,registry=valid();add('Complete consistent receipts',reports,registry)
    reports,registry=split_merge_attack();add('Split one acquisition; merge two other labels',reports,registry)
    reports,registry=valid();reports[0]['value']=0;add('Observation altered after acquisition',reports,registry)
    reports,registry=valid();reports.append(dict(reports[0],receipt_id='not-supplied'));add('Missing receipt despite three valid sources',reports,registry)
    reports,registry=valid();registry['alias']=dict(registry['r0'],value=0);add('Conflicting authoritative receipt entries',reports,registry)
    reports,registry=valid();add('Registry authentication not established',reports,registry,False)
    data={'evidence_type':'SOFTWARE FIXTURES — NOT MODEL OR REAL-WORLD EVIDENCE','native_calls':0,'cases':cases,
          'scope':'Authentication and statistical independence are external preconditions; this gate checks mappings and observation integrity only.'}
    here=Path(__file__).resolve().parent;(here/'examples.json').write_text(json.dumps(data,indent=2)+'\n')
    rows=''.join('<tr>'+''.join('<td>'+html.escape(str(x))+'</td>' for x in (c['case'],c['declared_label_choice'],c['gate']['decision'],c['gate']['reason']))+'</tr>' for c in cases)
    (here/'examples.html').write_text('<!doctype html><meta charset="utf-8"><title>Quorum provenance gate — software fixtures</title><style>body{font:16px system-ui;margin:2rem;max-width:1100px}table{border-collapse:collapse}th,td{border:1px solid #bbb;padding:.6rem}h1{font-size:26px}</style><h1>Verify acquisitions before counting votes</h1><p><b>SOFTWARE FIXTURES — NOT MODEL OR REAL-WORLD EVIDENCE</b></p><p>Claimed source labels can split one observation or merge independent ones. The gate counts acquisition IDs from an externally verified receipt registry and refuses incomplete or contradictory inputs.</p><table><tr><th>Constructed case</th><th>Declared-label rule</th><th>Receipt gate</th><th>Reason</th></tr>'+rows+'</table><p>Different acquisition IDs do not establish statistical independence. Registry authentication is an upstream precondition, not implemented cryptography. DEFER requests evidence; it does not guess a hidden answer.</p><p>No native run, machine allocation or model calls. Q1-02 remains 0/8 graded correct; the cause remains confounded. D1, M1 and C1 remain unrun.</p>')
    print(json.dumps({'constructed_cases':len(cases),'native_calls':0,'gate_decisions':[c['gate']['decision'] for c in cases]}))

if __name__=='__main__':main()
