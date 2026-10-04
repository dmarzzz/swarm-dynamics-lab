"""Recompute stored public packets, grades and analyses without provider calls."""
import argparse,gzip,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import study,sim,analyze

def verify(path):
    path=Path(path);assignments=analyze.read_rows(path/'assignments.jsonl.gz');rows=analyze.read_rows(path/'episodes.jsonl.gz')
    indexed={a['id']:a for a in assignments};assert len(indexed)==len(assignments)
    assert len({r['id'] for r in rows})==len(rows);assert set(indexed)=={r['id'] for r in rows}
    worlds={}
    with gzip.open(path/'worlds.jsonl.gz','rt') as f:
        for line in f:
            w=json.loads(line);worlds[(w['n'],w['world']['task'],w['kind'],w['rate'])]=w['world']
    for row in rows:
        a=indexed[row['id']];assert a['packet_hash']==study.digest(a['packet'])==row['packet_hash']
        assert all(set(r)=={'node','skill','claim','age','activity','verification'} for r in a['packet']['reports'])
        assert len(a['verification_events'])==a['checks']
        checked=[event['node'] for event in a['verification_events']];assert len(checked)==len(set(checked))
        world=worlds[(a['n'],a['task'],a['kind'],a['attacker_pass'] if a['kind']=='pilot' else .1)]
        admitted=[r['node'] for r in a['packet']['reports']]
        # Voting tie order has no effect because ties abstain.
        gm=sim.evaluate(world,admitted,sim.decide(world['public'],admitted),checked)
        assert gm==a['graph_metrics'],a['id']
        if row['status']=='completed':
            assert row['evaluation']==study.evaluate(a,row['answer']),row['id']
            assert row['scripted_evaluation']==study.evaluate(a,study.scripted(a['packet'])),row['id']
    summary=json.loads((path/'summary.json').read_text());assert summary['planned']==len(rows)
    assert summary['invalid']==sum(r['status']!='completed' for r in rows)
    analysis=json.loads((path/'analysis.json').read_text());assert analysis==analyze.analyze(rows),'analysis_mismatch_use_matching_python'
    if summary['params']['stage']=='S1':
        assert len(analysis['cells'])==120
        assert all(c['assigned']==24 for c in analysis['cells'])
    if summary['params']['stage'] in ('S0','Q0'):assert summary['qualification']==study.qualification(rows)
    from PIL import Image
    with Image.open(path/'replay.gif') as gif:frames=gif.n_frames;[gif.seek(i) for i in range(frames)]
    result={'assignments':len(assignments),'rows':len(rows),'invalid':summary['invalid'],'all_packet_hashes_grades_and_analysis_match':True,'gif_frames':frames}
    (path/'verification-summary.json').write_text(json.dumps(result,indent=2));return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');args=ap.parse_args();print(json.dumps(verify(args.path)))
