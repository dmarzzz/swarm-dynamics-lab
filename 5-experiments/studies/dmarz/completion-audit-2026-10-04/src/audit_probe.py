"""Offline inspection of the newly published i0-003 diagnostic. No provider calls."""
import argparse
import hashlib
import json
from pathlib import Path
HERE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--input',type=Path,default=Path('/Users/halcyon/swarm-lab-lanes/patchwork-atlas/swarm-lab/researchers/dmarz/notes/compositional-safety/results'))
args=parser.parse_args()
p=args.input/'i0-003'
read=lambda name:json.loads((p/name).read_text())
manifest=read('manifest.json');results=read('results.json');hashes=read('artifact-hashes.json')
for name,digest in hashes.items(): assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest
parent={r['episode_id']:r for r in map(json.loads,(args.input/'q0-004/episodes.jsonl').read_text().splitlines())}
assert len(results)==16 and {(r['case'],r['condition']) for r in results}=={(r['case'],r['condition']) for r in manifest['assignments']}
comparisons=[]
for item in manifest['cases']:
    assert item['packet']==parent[item['source_episode']]['trace'][item['step']]['observation']
    n=item['case']; original=read(f'request-{n}-original.json'); clarified=read(f'request-{n}-clarified.json')
    po=json.loads(original['messages'][0]['content']); pc=json.loads(clarified['messages'][0]['content'])
    assert po==item['packet']
    contract=pc.pop('execution_contract');assert pc==po
    assert {k:v for k,v in original.items() if k!='messages'}=={k:v for k,v in clarified.items() if k!='messages'}
    assert len(original['messages'])==len(clarified['messages'])==1
    pair=[r for r in results if r['case']==n]
    for r in pair:assert r['advancing']==bool(r['valid'] and r['answer']['action'] in item['expected'])
    comparisons.append(dict(case=n,source_episode=item['source_episode'],step=item['step'],domain=po['domain'],
                            outcomes=pair,added_contract=contract))
counts={c:{'assigned':8,'valid':sum(r['valid'] for r in results if r['condition']==c),
           'advancing':sum(r['advancing'] for r in results if r['condition']==c),
           'explicit_refusals':sum(r['usage'].get('stop_reason')=='refusal' for r in results if r['condition']==c)} for c in ['original','clarified']}
result=dict(attempt='i0-003',source_commit=manifest['commit'],publication_commit='4d007242',
            files_hash_verified=len(hashes),actual_credential_free_request_bodies=16,full_provider_response_envelopes=False,
            request_comparison='Only the declared execution_contract differs in each pair. Original packets exactly match saved parent observations; expected actions absent from actor requests.',
            counts=counts,independent_units='Eight deliberately selected reused decision states; no full episode executed, no independent qualification roots.',
            conclusion='Clarification is partly useful in selected D1 cases, insufficient for D2. No full repair, qualification or causal isolated-model effect established.',
            comparisons=comparisons,input_sha256={n:hashlib.sha256((p/n).read_bytes()).hexdigest() for n in ['manifest.json','results.json','summary.json']})
(HERE/'evidence/probe-i0-003.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'counts':counts,'verified_files':len(hashes)}))
