"""Render and publish already-completed diagnostics; never invokes a model."""
import argparse,json
from pathlib import Path
from render import diagnostic


def main():
    import swarm_report as sr
    ap=argparse.ArgumentParser();ap.add_argument('--root',type=Path,required=True);a=ap.parse_args()
    for stage in ('D0','Q1','Q2'):
        folder=a.root/(stage+'-attempt-1');rows=[json.loads(x) for x in (folder/'results.jsonl').read_text().splitlines()]
        summary=json.loads((folder/'summary.json').read_text());manifest=json.loads((folder/'manifest.json').read_text())
        diagnostic(rows,folder/'final_frame.png',stage+' diagnostic' if stage=='D0' else stage+' qualification')
        run=sr.start('adaptive-quorum-api-v2',run='adaptive-quorum-api-v2/repair-v3-'+stage+'-attempt-1',params={'stage':stage,'backend':'laya' if stage=='D0' else 'laya-hybrid','kind':'diagnostic' if stage=='D0' else 'qualification','code':manifest['code'],'retrospective_report':True},message='Retrospective publication of completed recorded attempt; no model rerun.')
        sr.report('progress','adaptive-quorum-api-v2',run.id,url='https://github.com/dmarzzz/swarm-lab/tree/main/researchers/vishesh/notes/adaptive-quorum-v2/repair-v3',strict=True)
        for name in ('final_frame.png','summary.json','manifest.json','results.jsonl','assignments.json','receipts.json'):run.artifact(folder/name,name)
        message='Execution complete; diagnostic-only, combined-task competence failed.' if stage=='D0' else 'Execution complete; qualification '+('passed.' if summary['qualification_pass'] else 'FAILED; preserved boundary error, repaired in later architecture.')
        run.done(message=message,completed=len(rows),correct=sum(r['correct'] for r in rows),invalid=sum(r['error'] is not None for r in rows),qualification_pass=int(summary.get('qualification_pass',False)))
    print(json.dumps({'published':['D0','Q1','Q2']}))


if __name__=='__main__':main()
