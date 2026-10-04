"""Publish measured pilot analysis and corrected cost carry-forward; no model calls."""
import json
from pathlib import Path
import shutil
import subprocess
import analyze
import render
import study
import worker


def publish(sr):
    runs=sr.runs('sybil-specialists-api',limit=5000)
    selected={}
    for stage in ('S0','Q0','S1'):
        matches=[r for r in runs if r.get('params',{}).get('stage')==stage and r.get('params',{}).get('kind')!='analysis']
        assert len(matches)==1 and matches[0]['status']=='done' and matches[0]['metrics']['invalid']==0
        selected[stage]=matches[0]
    assert len({r['params']['source_hash'] for r in selected.values()})==1
    run_id='sybil-specialists-api/analysis-api-001'
    assert not any(r['run']==run_id for r in runs),'analysis_exists_no_overwrite'
    def path(r): return study.ROOT/'results'/f'{r["run"].replace("/","__")}-attempt-{r["attempts"]}'
    q=analyze.analyze(path(selected['Q0'])); result=analyze.analyze(path(selected['S1']))
    assert q['qualification']['passed'] and result['valid']==result['planned']==192
    out=study.ROOT/'results'/'sybil-specialists-api__analysis-api-001-attempt-1'
    out.mkdir(exist_ok=False)
    source=path(selected['S1'])/'episodes.jsonl'
    rows=[json.loads(line) for line in source.read_text().splitlines()]
    shutil.copy2(source,out/'replay_source.jsonl')
    count=render.replay(rows,out,'S1',192,initial_accounting=q['study_accounting'])
    result.update(qualification_screen=q['qualification'],qualification_cost_usd=q['cost_usd'],
                  source_runs={stage:r['run'] for stage,r in selected.items()},
                  visualization={'mapping':'v1.1','frames':count},new_model_calls=0,
                  analysis_code=subprocess.check_output(['git','rev-parse','HEAD'],cwd=study.ROOT,text=True).strip(),
                  reporting_amendment='Original pilot hub progress used aggregate study usage then stage totals at completion. '
                                      'Raw per-call accounting and scientific scores are correct and unchanged. '
                                      'This replay carries Q0 usage into its initial frame; all later frames use recorded study totals.')
    worker.write_json(out/'analysis.json',result)
    delta=result['primary']['mean']; badges=result['badges_high_attack_pass']['mean']
    with sr.start('sybil-specialists-api',run=run_id,params={'kind':'analysis','stage':'S1','backend':'anthropic',
             'simulation_code':result['params']['code'],'analysis_code':result['analysis_code']}) as run:
        for name in ('final_frame.png','replay.gif','initial_frame.png','analysis.json','replay_source.jsonl'):
            worker.upload(run,out/name)
        run.done(message=f'Haiku pilot: 192/192 valid, 12 paired worlds; qualification 24/24 exact. '
                 f'Coverage-minus-degree rare accuracy {delta:+.3f}; visible-minus-masked badges under weak checks {badges:+.3f}. '
                 'All four policies and attacker admission shown. Synthetic environment; exploratory only. No new model calls for analysis.',
                 rare_accuracy_difference=delta,badge_accuracy_difference=badges,worlds=12,invalid=0,model_calls=0)
    return {'run':run_id,'analysis_code':result['analysis_code'],'new_model_calls':0,'primary':delta,'badges':badges}


if __name__=='__main__':
    import swarm_report as sr
    print(json.dumps(publish(sr)))
