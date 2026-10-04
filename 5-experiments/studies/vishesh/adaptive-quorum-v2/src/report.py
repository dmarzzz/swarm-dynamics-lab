"""Upload audited completed local results; no inference or credentials in code."""
import argparse
import hashlib
import json
from pathlib import Path
import swarm_report as sr


def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args();d=a.directory
    receipt=d/'hub-receipt.json'
    if receipt.exists():raise SystemExit('existing receipt; do not duplicate upload')
    manifest=json.loads((d/'manifest.json').read_text());summary=json.loads((d/'summary.json').read_text())
    if not manifest['complete'] or summary['episodes']!=168:raise SystemExit('incomplete qualification')
    exp='adaptive-quorum-api-v2'
    sr.register(exp,title='Antsy',description='Local exploratory qualification, five versus nine scouts. Synthetic APIs, constraints and mock tests. See protocol limits and clean qualification gate.',owner='vishesh',params={'stage':{'type':'str','role':'stage'},'backend':{'type':'str','role':'condition'},'code':{'type':'str','role':'fixed'}},metrics=['episodes','invalid','qualified'],primary_metric='qualified',url='https://github.com/dmarzzz/swarm-lab/tree/main/researchers/vishesh/notes/adaptive-quorum-v2')
    digest=hashlib.sha256((d/'episodes.jsonl').read_bytes()).hexdigest()[:12]
    run_id=f'{exp}/{manifest["backend"]}-S0-{digest}'
    receipt.write_text(json.dumps({'run':run_id,'upload_complete':False}))
    with sr.start(exp,run=run_id,params={'stage':'S0','backend':manifest['backend'],'code':manifest['code']}) as run:
        for name in ('manifest.json','summary.json','episodes.jsonl','model-receipts.jsonl','assignments.json','audit.json','analysis.md','replay.html','final_frame.png'):
            if (d/name).exists():run.artifact(d/name,name)
        run.done(message='Exploratory qualification; evidence cutoff is not wall-clock deadline. No S1 launch.',episodes=summary['episodes'],invalid=sum(c['invalid'] for c in summary['cells']),qualified=int(summary['qualified']))
    receipt.write_text(json.dumps({'run':run_id,'upload_complete':True}));print(receipt.read_text())


if __name__=='__main__':main()
