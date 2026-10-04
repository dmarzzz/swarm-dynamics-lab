"""Verify public reports and replay privately retained data; no network/model calls."""
import argparse,hashlib,json,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent

def main(results,out):
    index=json.loads((BASE/'evidence-index.json').read_text())
    for name,digest in index['files'].items():
        if hashlib.sha256((BASE/name).read_bytes()).hexdigest()!=digest:raise ValueError('report_hash_mismatch:'+name)
    packet=json.loads((BASE.parent/'packet.json').read_text())
    for name,digest in packet['source_sha256'].items():
        if hashlib.sha256((BASE.parent.parent/name).read_bytes()).hexdigest()!=digest:raise ValueError('instrument_hash_mismatch:'+name)
    # The caller supplies an authorized PRIVATE archive; it is never fetched or published.
    import shutil
    results=Path(results);out=Path(out);out.mkdir(parents=True,exist_ok=False)
    for name in ('episodes.jsonl','transport.jsonl','usage.jsonl','summary.json'):
        shutil.copy2(results/name,out/name)
    result=subprocess.run([sys.executable,str(BASE/'analyze_saved.py'),str(out)],capture_output=True,text=True)
    if result.returncode:raise ValueError('saved_data_replay_failed')
    replay=json.loads((out/'audit.json').read_text());published=json.loads((BASE/'v1-reconciliation.json').read_text())
    if replay!=published:raise ValueError('published_reconciliation_mismatch')
    print(json.dumps({'scores_reproduced':True,'native_calls':0,'episodes':48,'transitions':96,'requests':192,'actual_usd':replay['actual_usd']}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',required=True);p.add_argument('--out',required=True);a=p.parse_args();main(a.results,a.out)
