"""Audit a complete valid bundle and replay every observation without network calls."""
from __future__ import annotations
import argparse
import copy
import gzip
import json
from pathlib import Path
from analyze import summarize,contrast
from sim import run_episode
from tasks import digest


def read_lines(root,name):
    path=root/name
    raw=path.read_bytes() if path.exists() else gzip.decompress((root/(name+'.gz')).read_bytes())
    return [json.loads(line) for line in raw.decode().splitlines() if line]


def identity(row):
    return row['task_id'],row['seed'],json.dumps(row['arm'],sort_keys=True)


def audit(root):
    root=Path(root);manifest=json.loads((root/'manifest.json').read_text())
    summary=json.loads((root/'summary.json').read_text());params=manifest['params']
    rows=read_lines(root,'episodes.jsonl');journal=read_lines(root,'events.jsonl')
    assert sorted(map(identity,rows))==sorted(map(identity,manifest['planned_episodes'])),'Assignment ledger differs'
    assert all(row['validity']['ok'] for row in rows),'Replay audit requires a complete valid bundle; preserve and inspect failures separately'
    assert len({identity(row) for row in rows})==len(rows),'Duplicate episodes'
    streams={};pairs=[];pending=None;usage={'input_tokens':0,'output_tokens':0}
    for item in journal:
        label=json.dumps(item['stream'],sort_keys=True);event=item['event'];stream=streams.setdefault(label,[])
        assert event['previous']==(stream[-1]['hash'] if stream else '0'*64),'Broken event chain'
        assert digest({k:v for k,v in event.items() if k!='hash'})==event['hash'],'Event digest differs'
        stream.append(event)
        if event['kind']=='call_start':
            assert pending is None,'Overlapping calls in sequential transcript'
            pending=event['request']
        elif event['kind']=='call_response':
            assert pending is not None,'Response without request'
            pairs.append((pending,event['response']));pending=None
            for key in usage:usage[key]+=event.get('usage',{}).get(key,0)
        elif event['kind']=='call_failure':raise AssertionError('Failed call in valid-bundle replay')
    assert pending is None,'Unfinished model request'
    for row in rows:
        common={'task_id':row['task_id'],'seed':row['seed']}
        for field,label in (
            ('events',{**common,'phase':'continuation','arm':row['arm']}),
            ('acquisition_events',{**common,'phase':'acquisition','attack':row['arm']['attack']})):
            assert row[field]==streams[json.dumps(label,sort_keys=True)],'Episode trace differs from journal'

    class Replay:
        name=manifest['provider'];scientific=manifest['scientific']
        def __init__(self):self.index=0
        def complete(self,request):
            expected,response=pairs[self.index];self.index+=1
            assert request==expected,'Replay observation differs'
            return copy.deepcopy(response)
    provider=Replay();replayed=[]
    for task in params['tasks']:
        for seed in params['seeds']:
            replayed.extend(run_episode(task,seed,'controlled-tool-exposure',1,manifest['arms'],
                                        {'n_agents':params['n_agents']},provider))
    assert provider.index==len(pairs),'Unused model responses'
    observed={identity(row):row for row in rows}
    for row in replayed:
        saved=observed[identity(row)]
        for field in ('result','evaluation','snapshot_hash','world_hash'):
            assert row.get(field)==saved.get(field),'Replay differs: '+field
    assert summary['cells']==summarize(rows),'Summary differs'
    if summary['primary_candidate'] is not None:assert summary['primary_candidate']==contrast(rows),'Contrast differs'
    if manifest['scientific']:assert summary['actual_http_calls']==len(pairs),'Physical request count differs'
    accounting=summary.get('usage_accounting',{})
    if accounting:
        assert accounting['usage_missing_calls']==0,'Incomplete usage accounting'
        assert all(accounting[k]==v for k,v in usage.items()),'Usage totals differ'
        limits=manifest['model_limits'];cost=(usage['input_tokens']*limits['input_rate']+usage['output_tokens']*limits['output_rate'])/1e6
        assert abs(accounting['actual_cost_usd']-cost)<1e-8,'Cost differs'
    return {'episodes':len(rows),'policy_calls':len(pairs),'observations_replayed':True,
            'event_chains_verified':len(streams),'scores_verified':True,'usage_verified':bool(accounting),
            'runtime_commit':manifest['git_commit'],'audit_source_sha256':digest(Path(__file__).read_text())}


def main():
    p=argparse.ArgumentParser();p.add_argument('bundle');a=p.parse_args()
    print(json.dumps(audit(a.bundle),indent=2))

if __name__=='__main__':main()
