"""Reconstruct every request, terminal response and score from saved native records."""
import argparse,json,collections
from pathlib import Path
from runtime import request,digest,validate
from contract import qwen_payload,score,qualify

def run(root):
    rows=json.loads((root/'observations.json').read_text());m=json.loads((root/'manifest.json').read_text());events=[json.loads(l) for l in (root/'calls.jsonl').read_text().splitlines()];starts={};terminal={};reconstructed={r['id']:{} for r in rows};seconds=collections.Counter();cost=0.;tokens=collections.Counter()
    index={r['id']:(i,r) for i,r in enumerate(rows)}
    for e in events:
        cid=e['id']
        if e['type']=='start':
            assert cid not in starts;starts[cid]=e;i,r=index[e['row_id']]
            expected=request(r,i,'C4-'+m['stage']) if e['model']=='jev' else qwen_payload(r,0 if e['variant']=='a' else 1)
            assert expected==e['payload'] and digest(expected)==e['payload_hash']
        else:
            assert cid in starts and cid not in terminal;terminal[cid]=e;s=starts[cid];seconds[s['model']]+=e['seconds']
            if e['type']=='completed':
                value=e['result'];label=validate(value['raw'])['label'] if s['model']=='jev' else json.loads(value['raw']['message']['content'])['label'];assert label==value['label'];reconstructed[s['row_id']][s['variant']]=label;cost+=value.get('cost_usd',0)
                for k in ('input_tokens','output_tokens'):tokens[k]+=value.get(k,0)
    assert len(starts)==len(terminal)
    for r in rows:assert reconstructed[r['id']]==r['labels']
    expected=score(rows);assert expected==json.loads((root/'summary.json').read_text())
    if m['stage']=='S0':assert qualify(rows)==json.loads((root/'qualification.json').read_text())
    # Separate direct reference count, independent of the policy scorer.
    complete=[r for r in rows if r['status']=='completed'];wrong={k:sum(r['labels'][k]!=r['expected'] for r in complete) for k in ('a','b','jev')};accepted_wrong=sum(r['labels']['a']==r['labels']['b'] and r['labels']['a']!=r['expected'] for r in complete);referrals=sum(r['labels']['a']!=r['labels']['b'] for r in complete)
    assert referrals==expected['counterfactual_cascade_jev_calls'] and accepted_wrong==sum(x['accepted_wrong'] for x in expected['families'].values())
    a={'same_author_audit':True,'attempt':m['attempt'],'status':m['status'],'assigned':len(rows),'completed':len(complete),'starts':len(starts),'terminal':len(terminal),'completed_calls':sum(e['type']=='completed' for e in terminal.values()),'cost_usd':cost,'tokens':dict(tokens),'seconds_by_component':dict(seconds),'complete_case_wrong':wrong,'accepted_wrong':accepted_wrong,'referrals':referrals,'all_payload_hashes_verified':True,'all_scores_reconstructed':True}
    (root/'audit.json').write_text(json.dumps(a,indent=2)+'\n');print(json.dumps(a));return a
if __name__=='__main__':p=argparse.ArgumentParser();p.add_argument('root',type=Path);run(p.parse_args().root)
