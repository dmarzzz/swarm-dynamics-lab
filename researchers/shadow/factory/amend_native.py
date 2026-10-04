import json
import factory as f
names=[]
order=['split-sonnet-no-links-strong','split-sonnet-linked-strong','split-sonnet-no-links-weak','split-sonnet-linked-weak','split-sonnet-four-checks']
for original in order:
    old=original+'-or-json';s=json.loads((f.ROOT/'specs'/f'{old}.json').read_text())
    s.update(id=original+'-native-json',parent_attempt=old,created_at=f.now(),route='anthropic-pool',model='claude-sonnet-4-6',max_paid_usd=0,
        qualification_roots={'ring':5141,'community':5146},
        amendment='2026-10-04: shared OpenRouter key hit its provider-enforced USD5 daily limit after 100 valid structured calls in the first study. Do not change key limits or select another credential. New native-schema pool cohort, fresh qualification roots, bounded HTTP429 backoff. No earlier outcomes pooled. Root-first dispatch to maximize complete pairs at interruption.',
        request_config='Native Messages API, local pool, output_config.format json_schema from parent, temperature0, max_tokens500. Max three attempts per assignment; only HTTP429, wait max(Retry-After,120s then240s), never past22Z. No paid fallback.',
        protocol='12 clean fixtures (fresh roots ring5141/community5146 x six shapes), all exact required; 48 parent comparison roots x four cells. Randomize ROOT order, finish four-cell root blocks. No answer retry, no optional sample extension. Earlier cohorts remain separate.',
        max_transport_attempts=612)
    s['source_sha256'][str((f.ROOT/'pool_structured.py').relative_to(f.REPO))]=f.sha(f.ROOT/'pool_structured.py')
    path=f.ROOT/'specs'/f"{s['id']}.json"
    if path.exists():raise SystemExit('refuse overwrite')
    f.dump(path,s);names.append(s['id'])
f.dump(f.ROOT/'queue-native.json',dict(specs=names,hard_paid_cap_usd=20,new_cohort_paid_usd=0,stops_on_failed_qualification=True))
