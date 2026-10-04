"""Audit a completed local bundle against its frozen assignments and saved evidence."""
import argparse
import hashlib
import json
import math
from collections import Counter
from pathlib import Path
from PIL import Image
from analyze import summarize
from engine import evaluate, task


def equivalent(a,b):
    if isinstance(a,dict): return isinstance(b,dict) and a.keys()==b.keys() and all(equivalent(a[k],b[k]) for k in a)
    if isinstance(a,list): return isinstance(b,list) and len(a)==len(b) and all(equivalent(x,y) for x,y in zip(a,b))
    if isinstance(a,float): return isinstance(b,(int,float)) and math.isclose(a,b,rel_tol=0,abs_tol=1e-10)
    return a==b


def verify(directory):
    p=Path(directory)
    manifest=json.loads((p/'manifest.json').read_text())
    saved=json.loads((p/'summary.json').read_text())
    hashes=json.loads((p/'artifact-hashes.json').read_text())
    for name, digest in hashes.items():
        assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest, name
    rows=[json.loads(l) for l in (p/'episodes.jsonl').read_text().splitlines()]
    expected={f"{manifest['attempt']}/{a['task_id']}/{a['domain']}/{a['variant']}/{a['arm']}" for a in manifest['assignments']}
    assert len(expected)==len(manifest['assignments'])==len(rows)
    assert {r['episode_id'] for r in rows}==expected
    dispatch=[json.loads(l) for l in (p/'dispatch.jsonl').read_text().splitlines()]
    assert Counter((d['episode_id'],d['event']) for d in dispatch)==Counter((e,k) for e in expected for k in ('start','terminal'))
    for r in rows:
        assert r['hashes']==manifest['hashes'] and r['commit']==manifest['commit']
        spec=task(r['task_id'],r['domain'],r['variant'],r['n'])
        assert hashlib.sha256(json.dumps(spec,sort_keys=True).encode()).hexdigest()==r['task_sha256']
        assert evaluate(spec,r['events'])==r['evaluation'], r['episode_id']
    rebuilt=summarize(rows,manifest['stage'],len(expected))
    for key in rebuilt: assert equivalent(rebuilt[key],saved[key]), key
    usage=[t.get('usage',{}) for r in rows for t in r['trace']]
    assert sum(bool(u.get('attempted')) for u in usage)==saved['accounting']['attempted_calls']
    assert abs(sum(u.get('actual_usd',0) for u in usage)-saved['accounting']['actual_usd'])<1e-8
    bundles={(r['task_id'],r['domain'],r['variant']) for r in rows}
    for tid,domain,variant in bundles:
        sub=p/f'{tid}-{domain}-{variant}'
        for name in ('live.png','final_frame.png','replay.gif'):
            with Image.open(sub/name) as im:
                assert im.size==(1600,900)
                for index in range(getattr(im,'n_frames',1)): im.seek(index); im.load()
    return dict(attempt=manifest['attempt'],episodes=len(rows),bundles=len(bundles),
                verified_files=len(hashes),safe=saved['safe_completion'],invalid=saved['invalid'],
                violations=saved['violation'],qualification_pass=saved['qualification_pass'],
                accounting=saved['accounting'])


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path)
    print(json.dumps(verify(p.parse_args().directory),indent=2))
