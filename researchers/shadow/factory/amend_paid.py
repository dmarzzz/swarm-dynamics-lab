"""Generate separate prospective attempt files. Original specs and outcomes untouched."""
import json
import factory as f

names=[]
for old in json.loads((f.ROOT/'queue.json').read_text())['specs']:
    s=json.loads((f.ROOT/'specs'/f'{old}.json').read_text())
    s.update(id=old+'-or',parent_attempt=old,route='openrouter',model='anthropic/claude-sonnet-4.6',
             max_paid_usd=4,concurrency=2,created_at=f.now(),
             amendment='2026-10-04: original pool cohort stopped at four HTTP429 failures; separate OpenRouter attempt, all assignments requalified, no pooled outcomes. Global USD20 locked ledger, USD4/spec. No retries. No change to scientific contrast.',
             request_config='Anthropic-only provider, no fallbacks, reasoning disabled, temperature0, max_tokens500, provider max price input3/output15 USD/M. Native pool max_tokens/temperature matched; endpoint/output envelope differs.')
    s['source_sha256'][str((f.ROOT/'paid.py').relative_to(f.REPO))]=f.sha(f.ROOT/'paid.py')
    path=f.ROOT/'specs'/f"{s['id']}.json"
    if path.exists():raise SystemExit('refuse overwrite')
    f.dump(path,s);names.append(s['id'])
f.dump(f.ROOT/'queue-paid.json',dict(specs=names,hard_paid_cap_usd=20,per_spec_paid_cap_usd=4))
