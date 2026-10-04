"""Descriptive qualification audit; no independence or significance inflation."""
import argparse
import collections
import json
from pathlib import Path


def main():
    ap=argparse.ArgumentParser();ap.add_argument('directory',type=Path);a=ap.parse_args()
    manifest=json.loads((a.directory/'manifest.json').read_text())
    if not manifest['complete']:raise SystemExit('Do not analyze partial qualification as complete')
    rows=[json.loads(line) for line in (a.directory/'episodes.jsonl').read_text().splitlines()]
    keys=[(r['task_id'],r['agents'],r['deadline'],r['arm']) for r in rows]
    if len(keys)!=len(set(keys)) or len(rows)!=168:raise SystemExit('assignment mismatch')
    summary=json.loads((a.directory/'summary.json').read_text())
    lookup=dict(zip(keys,rows));contrasts=[]
    for task in manifest['design']['qualification_tasks']:
        for n in (5,9):
            for d in (3,6):
                left=lookup[task,n,d,'adaptive'];right=lookup[task,n,d,'fixed']
                contrasts.append({'task':task,'agents':n,'deadline':d,
                                  'loss_difference':left['evaluation']['loss']-right['evaluation']['loss']})
    targets=collections.Counter(r['evaluation']['target'] for r in rows if r['arm']=='central-at-deadline' and r['agents']==9 and r['deadline']==3)
    audit={'task_clusters':len(manifest['design']['qualification_tasks']),'target_counts':dict(targets),
           'missing_target_labels':sorted(set(('A','B','C','NONE'))-set(targets)),
           'adaptive_minus_fixed':contrasts,'all_assigned_outcomes':len(rows)}
    (a.directory/'audit.json').write_text(json.dumps(audit,indent=2))
    lines=['# Factual API qualification results','',f"Backend: {manifest['backend']}. Source: `{manifest['code']}`.",'',
           f"Completed {len(rows)} arm outcomes across {audit['task_clusters']} task clusters. Numerical clean-task qualification pass: **{summary['qualified']}**.",
           f"Target coverage: {dict(targets)}; missing labels: {audit['missing_target_labels']}. This is not a balanced benchmark.",'',
           '| Policy | Agents | Deadline | Correct/assigned | Constraint violations | Abstentions | False NONE | Invalid |',
           '|---|---:|---:|---:|---:|---:|---:|---:|']
    for c in summary['cells']:
        lines.append(f"| {c['arm']} | {c['agents']} | {c['deadline']} | {c['correct']}/{c['assigned']} | {c['constraint_violation']} | {c['abstention']} | {c['false_none']} | {c['invalid']} |")
    lines+=['',f"Physical model calls: {summary['physical_calls']}; estimated input tokens: {summary['input_tokens_estimate']}; episode wall seconds: {summary['wall_s']:.2f}.",'',
            'No p-values or independent-agent sample counts. Full tapes are shared across stopping policies. Root availability is not causal evidence use. Verification has a terminal probe allowance; evidence deadlines are not wall-clock service guarantees.',
            '', 'Do not launch development after a failed clean-task screen. Publish failed decisions and improve or replace the decision layer on separate development fixtures. Jev via OpenRouter remains a separately qualified future backend.']
    (a.directory/'analysis.md').write_text('\n'.join(lines)+'\n')
    print(json.dumps({'qualified':summary['qualified'],'outcomes':len(rows),'missing_labels':audit['missing_target_labels']}))


if __name__=='__main__':main()
