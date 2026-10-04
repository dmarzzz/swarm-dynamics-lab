"""Rebuild all paired PC-1 native timelines; no sampling or new provider calls."""
import argparse
import hashlib
import json
from pathlib import Path
from instrument import world,aggregate,bounds


def build(records_path,output):
    records=json.loads(records_path.read_text());by={r['id']:r for r in records}
    assert len(by)==len(records)==522
    frames=[]
    for seed in range(206,212):
        w=world(seed,stage='S0')
        for comm in ('private','social'):
            for state in ('reset','retain'):
                for step in range(3):
                    histories=[]
                    for h in ('A','B'):
                        rs=[by[f'{seed}-{h}-{comm}-{state}-{step}-{a}'] for a in range(3)]
                        outcomes=[r.get('checked',{}).get('response') if r['status']=='valid' else None for r in rs]
                        m=aggregate(outcomes);e=rs[0]['request']['state']['evidence']
                        histories.append(dict(history=h,map=m,error=bounds(m,w['truth']),
                            acquisitions=len({r['acquisition_id'] for r in e['observations']}),withdrawn=len(e['withdrawn']),
                            actors=[dict(id=r['id'],status=r['status'],map=o['map'] if o else {},request_sha256=r['request_sha256'],
                                         prior=r['request']['state']['prior'] is not None,peers=len(r['request']['state']['peers'])) for r,o in zip(rs,outcomes)]))
                    frames.append(dict(seed=seed,communication=comm,state=state,step=step,truth=w['truth'],region=w['exposed'],histories=histories))
    payload=dict(mode='Measured native PC-1 S0-A1',source_sha256=hashlib.sha256(records_path.read_bytes()).hexdigest(),
                 frames=frames,comparison_count=24,paired_frame_count=72,actor_map_count=432)
    template=Path(__file__).with_name('native-replay-template.html').read_text()
    output.write_text(template.replace('__DATA__',json.dumps(payload,separators=(',',':')).replace('</','<\\/')))
    return payload


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('records',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    result=build(a.records,a.output);print(json.dumps({k:result[k] for k in result if k!='frames'}))
