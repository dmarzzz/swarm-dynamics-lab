"""Reconstruct model labels and deterministic worlds from durable C1 observations."""
import json,argparse,collections,math
from pathlib import Path
from definition import assess,digest,request,ARMS
from worker import rollout

def audit(root):
    m=json.loads((root/'manifest.json').read_text());rows=json.loads((root/'observations.json').read_text());summary=json.loads((root/'summary.json').read_text());assert summary==assess(rows)
    events=[json.loads(x) for x in (root/'calls.jsonl').read_text().splitlines()];started={e['id']:e for e in events if e['type']=='start'};terminal=[e for e in events if e['type'] in ('completed','failed')]
    assert len(started)==len([e for e in events if e['type']=='start']);assert len({e['id'] for e in terminal})==len(terminal);assert set(e['id'] for e in terminal)<=set(started)
    for e in started.values():assert e['payload_hash']==digest(e['payload'])
    assert dict(collections.Counter(e['model'] for e in started.values()))=={k:v for k,v in m['calls'].items() if v}
    done=[e for e in terminal if e['type']=='completed'];jev={started[e['id']]['payload_hash']:e for e in done if e['model']=='jev'};qwen=[e for e in done if e['model']=='qwen']
    for i,r in enumerate(rows):
        if 'qwen' in r['labels']:assert qwen[i]['result']['label']==r['labels']['qwen']
        for arm in ('jev','qwen+jev'):
            if arm in r['labels']:
                p=request(r,r['index'],r['scope'],r['labels']['qwen'] if arm=='qwen+jev' else None);assert jev[digest(p)]['result']['label']==r['labels'][arm]
    world_count=frame_count=0
    for w in json.loads((root/'world-assignments.json').read_text()):
        if w['status']!='completed':continue
        c=json.loads((root/f'corpus-{w["seed"]}.json').read_text());t=json.loads((root/f'tapes-{w["seed"]}.json').read_text())[w['model']];expected=rollout(c,t,w['layout'],w['arm'],w['scenario'],cap=16);saved=json.loads((root/(w['id']+'.json')).read_text())
        for k,v in expected.items():assert saved[k]==v
        assert math.isclose(saved['metrics']['post_event_error'],sum(f['incorrect_or_missing'] for f in saved['frames'][10:])/20)
        world_count+=1;frame_count+=len(saved['frames'])
    out={'source':'same-author replay and arithmetic audit','verified_observations':len(rows),'verified_worlds':world_count,'verified_frames':frame_count,'call_starts':len(started),'call_terminal':len(terminal),'input_tokens':sum(e['result'].get('input_tokens',0) for e in done),'output_tokens':sum(e['result'].get('output_tokens',0) for e in done),'cost_usd':sum(e['result'].get('cost_usd',0) for e in done),'seconds_by_component':{a:sum(e['seconds'] for e in terminal if e['model']==a) for a in ('qwen','jev')}}
    (root/'audit.json').write_text(json.dumps(out,indent=2));return out
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);a=p.parse_args();print(json.dumps(audit(a.root)))
