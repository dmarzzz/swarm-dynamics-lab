"""Verify audit-to-source binding; semantic judgments are authored, not computed."""
import argparse,hashlib,json
from pathlib import Path
from prepare_cases import convert
from contract import actor_only

def verify(source,report):
 raw=source.read_bytes();audit=json.loads(report.read_text())
 assert hashlib.sha256(raw).hexdigest()==audit['source_sha256']
 rows=json.loads(raw);seen=set()
 for item in audit['cases']:
  assert item['source_index'] not in seen;seen.add(item['source_index'])
  row=rows[item['source_index']];actor,reason=convert(row,item['source_index']);assert reason is None
  actor=actor_only(actor)
  assert hashlib.sha256(json.dumps(actor,sort_keys=True).encode()).hexdigest()==item['actor_sha256']
  assert actor['case_id']==item['case_id'] and row['label']==item['published_label']
  assert set(item['evidence_refs'])<={e['evidence_id'] for e in actor['evidence']}
  assert all('label' not in e and 'justification' not in e and 'source_url' not in e for e in actor['evidence'])
 assert len(seen)==8
 return {'verified_case_bindings':len(seen),'native_calls':0,'semantic_verdicts_independently_verified':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('source',type=Path);p.add_argument('--report',type=Path,default=Path(__file__).with_name('development-eight-audit.json'));a=p.parse_args();print(json.dumps(verify(a.source,a.report)))
