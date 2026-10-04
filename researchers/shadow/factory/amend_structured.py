import json
import factory as f
names=[]
for old in json.loads((f.ROOT/'queue-paid.json').read_text())['specs']:
    s=json.loads((f.ROOT/'specs'/f'{old}.json').read_text())
    s.update(id=old+'-json',parent_attempt=old,created_at=f.now(),qualification_roots={'ring':5140,'community':5145},
        amendment='2026-10-04: prior paid attempts returned valid factual content wrapped in prose, rejected by strict parser. New attempt adds native strict JSON-schema output; fresh qualification roots 5140/5145. No answer salvage. Main comparison roots, estimator, sample size and prediction unchanged. Shared ledger retains all prior costs within USD20.',
        request_config=s['request_config']+' Plus response_format json_schema strict=True using the parent provider.SCHEMA.',
        protocol=s['protocol'].replace('one root/family','fresh roots ring5140/community5145'))
    s['source_sha256'][str((f.ROOT/'structured.py').relative_to(f.REPO))]=f.sha(f.ROOT/'structured.py')
    path=f.ROOT/'specs'/f"{s['id']}.json"
    if path.exists():raise SystemExit('refuse overwrite')
    f.dump(path,s);names.append(s['id'])
f.dump(f.ROOT/'queue-structured.json',dict(specs=names,hard_paid_cap_usd=20,per_spec_paid_cap_usd=4))
