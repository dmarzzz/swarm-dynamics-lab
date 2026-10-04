"""Offline replay audit of physical journals and logical protocol; no inference."""
import hashlib,json,tarfile
from pathlib import Path
import scale_pilot as sp,scale_recovery as recovery
from scale_qualification import normalize
BASE=sp.BASE

def audit(stage):
 p=BASE/f'reviews/native-{stage}-01';s=json.loads((p/'summary.json').read_text());events=[json.loads(x) for x in (p/'events.jsonl').read_text().splitlines()];starts=[e for e in events if e['kind']=='attempt_start'];usages=[e for e in events if e['kind']=='usage'];protocol=recovery.Protocol(stage) if stage=='SC-LUNA' else sp.Protocol(stage);rows=[json.loads(x) for x in (p/'protocol.jsonl').read_text().splitlines()];validated=0;failures=[]
 with tarfile.open(p/'raw-records.tar.gz','r:gz') as archive:
  files={m.name:archive.extractfile(m).read() for m in archive.getmembers() if m.isfile()}
 for e in events:
  if e['kind'] in ('request_artifact','response_artifact'):
   raw=files[e['name']];assert len(raw)==e['bytes'] and hashlib.sha256(raw).hexdigest()==e['sha256'],'physical_artifact_changed'
 for index,start in enumerate(starts,1):
  item=protocol.next();raw=files[start['request']['name']];assert raw==sp.encode(item['wire_body']),'wire_changed'
  response=files.get(f'{index:02d}-response.bin');assert response is not None,'response_missing'
  try:a=protocol.check(item,normalize(json.loads(response)))
  except Exception as exc:
   failures.append({'physical_request':index,'classification':type(exc).__name__});assert index==len(starts),'dispatch_after_failure';continue
  row=rows[validated];assert row['answer']==a and row['wire_sha256']==item['wire_sha256'],'logical_record_changed';protocol.accept(item,a);validated+=1
 assert validated==s['valid']==len(rows) and len(starts)==s['calls'];assert len(usages)+s['usage_missing']==s['calls']
 total=sum(e['reported_usd'] for e in usages);assert abs(total-s['observed_usage_cost_usd'])<1e-10
 assert len(failures)==s['failed']
 expected=(recovery.assessment if stage=='SC-LUNA' else sp.assessment)(protocol);assert expected==json.loads((p/'assessment.json').read_text()),'assessment_changed'
 return {'stage':stage,'physical_requests':len(starts),'validated_new_outputs':validated,'reused_outputs':67 if stage=='SC-LUNA' else 0,'all_artifact_hashes_match':True,'all_wires_reconstructed':True,'assessment_reproduced':True,'usage_reconciled':True,'failed_response_preserved':failures,'model_calls':0}
if __name__=='__main__':
 results=[audit(s) for s in ('SP-SOL','SP-LUNA','SC-LUNA') if (BASE/f'reviews/native-{s}-01/summary.json').exists()];out=BASE/'scale-up/saved-audit.json';out.write_text(json.dumps(results,indent=2)+'\n');print(json.dumps(results))
