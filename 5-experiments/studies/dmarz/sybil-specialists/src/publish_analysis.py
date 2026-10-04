"""Publish an already-reconciled scripted analysis using the server reporter alias."""
import argparse
import json
from pathlib import Path
import swarm_report as sr


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('directory',type=Path)
    ap.add_argument('--analysis-code',required=True)
    a=ap.parse_args()
    result=json.loads((a.directory/'analysis.json').read_text())
    assert result['backend']=='scripted' and result['invalid']==0
    assert result['assigned_arm_records']==1120 and result['independent_world_clusters']==12
    runs=sr.runs('sybil-specialists',limit=5000)
    expected=json.loads((a.directory/'S1-reconciliation.json').read_text())
    assert len(expected)==18
    source={r['params']['code'] for r in runs if r['run'] in {e['run'] for e in expected}}
    assert len(source)==1
    run_id='sybil-specialists/analysis-scripted-001'
    assert not any(r['run']==run_id for r in runs), 'Analysis already published; inspect instead of overwriting'
    with sr.start('sybil-specialists',run=run_id,params={'kind':'analysis','stage':'S1','backend':'scripted',
            'simulation_code':source.pop(),'analysis_code':a.analysis_code}) as run:
        for name in ['tradeoff.png','analysis.json','S0-reconciliation.json','S1-reconciliation.json','environment.json']:
            receipt=run.artifact(a.directory/name,name)
            assert receipt and not receipt.get('spooled'), 'Analysis artifact not durably acknowledged'
        delta=result['mean_rare_accuracy_difference']; risk=result['mean_malicious_admission_difference']
        run.done(message=f'SCRIPTED S1: 12 paired worlds, 18 conditions, 864 arm outcomes, zero invalid and zero API calls. '
                 f'Primary coverage-minus-degree: rare accuracy {delta:+.3f}; malicious admission {risk:+.3f}. '
                 'Synthetic modeled verifier; no LLM or general security finding. Chart covers all arms and cells.',
                 rare_accuracy_difference=delta,malicious_admission_difference=risk,worlds=12,invalid=0)
    print(run_id)


if __name__=='__main__': main()
