"""Read-only scientific recomputation; writes one verification receipt, never calls a model."""
import argparse,json,sys
from pathlib import Path
from PIL import Image
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import study,sim,analyze

def normalized(value):return json.loads(json.dumps(value,sort_keys=True))
def unique_index(rows,key):
    indexed={key(r):r for r in rows}
    assert len(indexed)==len(rows),'duplicate_record'
    return indexed

def verify(path):
    path=Path(path);summary=json.loads((path/'summary.json').read_text());stage=summary['params']['stage'];cfg=study.design()['cfg']
    assert summary['params']['source_hash']==study.source_hash(),'verification_requires_frozen_runtime'
    assignments=analyze.read_rows(path/'assignments.jsonl.gz');rows=analyze.read_rows(path/'episodes.jsonl.gz')
    indexed=unique_index(assignments,lambda a:a['id']);terminal=unique_index(rows,lambda a:a['id'])
    assert set(indexed)==set(terminal),'assigned_terminal_mismatch'
    regenerated=unique_index(study.assignments(stage),lambda a:a['id'])
    assert indexed==regenerated,'assignment_regeneration_mismatch'
    worlds=analyze.read_rows(path/'worlds.jsonl.gz');histories=analyze.read_rows(path/'history.jsonl.gz')
    world_index=unique_index(worlds,lambda w:(w['task'],w['identities'],w['strategy']))
    assert set(world_index)=={(a['task'],a['identities'],a['strategy']) for a in assignments if a['kind']=='pilot'},'world_assignment_coverage_mismatch'
    history_index=unique_index(histories,lambda h:(h['task'],h['identities'],h['strategy'],h['arm'],h['round']))
    expected_history={};round_count=0
    for key,stored in world_index.items():
        world=sim.make_world(*key,cfg)
        assert normalized(world)==stored,'world_regeneration_mismatch'
        for raw in world['rounds']:
            t=raw['round'];reports=raw['reports'];round_count+=1
            controlled=[r for r in reports if world['roles'][r['node']]=='attacker']
            assert len(controlled)==cfg['attacker_messages']==16
            assert len(reports)-len(controlled)==(18 if t<4 else 24)
            assert len({r['message'] for r in reports})==len(reports)
            honest_rare=[r for r in reports if world['roles'][r['node']]!='attacker' and r['skill']>=3]
            assert len(honest_rare)==(0 if t<4 else 3)
            if t>=4:assert {r['skill'] for r in honest_rare}=={3,4,5}
            assert all(r['claim']==world['truths'][t][r['skill']] for r in reports if world['roles'][r['node']]!='attacker')
            assert raw['attack_active']==(t>=4 and (key[2]=='sleeper' or key[2]=='relapse' and t in (4,7,8)))
            assert all((r['claim']!=world['truths'][t][r['skill']])==raw['attack_active'] for r in controlled)
        for arm in study.design()['arms']:
            for state in sim.simulate(world,arm,cfg):
                entry=dict(task=key[0],identities=key[1],strategy=key[2],arm=arm,**state)
                hkey=(*key,arm,state['round']);expected_history[hkey]=entry
                assert len(state['audits'])==4 and len({a['node'] for a in state['audits']})==4
                assert len(state['packet']['reports'])==12
                assert sum(sum(h.values()) for h in state['history_after'].values())==state['round']*4
                assert state['metrics']['new_identity_audits']+state['metrics']['veteran_audits']==4
                for report in state['packet']['reports']:
                    assert set(report)=={'node','skill','claim','message','join_round','audit_now','history'}
    assert history_index==expected_history,'history_or_reputation_metric_mismatch'
    for identifier,row in terminal.items():
        a=indexed[identifier];assert a['packet_hash']==study.digest(a['packet'])==row['packet_hash']
        assert row['source_hash']==summary['params']['source_hash']
        assert row['status'] in ('completed','failed','not_started')
        if row['status']=='completed':
            assert row['evaluation']==study.evaluate(a,row['answer']),identifier
            assert row['scripted_evaluation']==study.evaluate(a,study.scripted(a['packet'])),identifier
    good=[r for r in rows if r['status']=='completed']
    assert summary['planned']==len(assignments)==summary['terminal']==len(rows)
    assert summary['started']==sum(r['status']!='not_started' for r in rows)
    assert summary['graded']==summary['analyzed']==len(good)
    assert summary['invalid']==len(rows)-len(good)
    assert summary['not_started']==sum(r['status']=='not_started' for r in rows)
    assert summary['input_tokens']==sum(r.get('accounting',{}).get('input_tokens',0) for r in rows)
    assert summary['output_tokens']==sum(r.get('accounting',{}).get('output_tokens',0) for r in rows)
    assert summary['model_calls']==sum(r.get('accounting',{}).get('attempted',False) for r in rows)
    assert abs(summary['cost_usd']-sum(r.get('accounting',{}).get('actual_usd',0) for r in rows))<1e-12
    analysis=json.loads((path/'analysis.json').read_text());assert analysis==analyze.analyze(rows),'analysis_mismatch_use_matching_python_numpy'
    if stage=='S1':
        assert len(assignments)==1944 and len(analysis['cells'])==81
        assert all(c['assigned']==24 for c in analysis['cells'])
        assert len(worlds)==216 and len(histories)==5184
    if stage in ('S0','Q0'):assert summary['qualification']==study.qualification(rows)
    with Image.open(path/'replay.gif') as gif:
        frames=gif.n_frames
        for i in range(frames):gif.seek(i);gif.load()
        assert frames==(9 if stage=='Q0' else 8)
    with Image.open(path/'final_frame.png') as im:assert im.size==(1800,1200)
    receipt={'stage':stage,'source_hash':summary['params']['source_hash'],'assignments':len(assignments),'rows':len(rows),'invalid':summary['invalid'],'worlds':len(worlds),'world_rounds':round_count,'history_records':len(histories),'all_assignments_worlds_history_packets_grades_and_analysis_match':True,'accounting_reconciled':True,'gif_frames':frames,'final_size':[1800,1200],'note':'All science recomputed from frozen runtime; no model calls. Playback in public browser is a separate deployment check.'}
    (path/'verification-summary.json').write_text(json.dumps(receipt,indent=2)+'\n');return receipt
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');a=ap.parse_args();print(json.dumps(verify(a.path)))
