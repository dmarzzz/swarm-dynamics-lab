"""Regenerate frozen assignments and reconcile saved science/accounting without API calls."""
import argparse,gzip,json,math,sys,tempfile
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'src'))
import study,sim,analyze,provider


def unique_index(records,key):
    indexed={key(record):record for record in records}
    assert len(indexed)==len(records),'duplicate_record'
    return indexed


def close(actual,expected,label):
    assert math.isclose(actual,expected,rel_tol=0,abs_tol=1e-9),(label,actual,expected)


def request_reservation(packet):
    """Mirror the frozen provider's public request envelope, excluding credential headers."""
    d=study.design();b=d['budget']
    body={'model':d['model'],'max_tokens':b['max_output_tokens'],'temperature':0,
          'system':provider.SYSTEM,'messages':[{'role':'user','content':json.dumps(packet,sort_keys=True)}],
          'output_config':{'format':{'type':'json_schema','schema':provider.SCHEMA}}}
    encoded=json.dumps(body).encode()
    assert len(encoded)<=b['max_input_bytes'],'oversized_recorded_packet'
    return ((len(encoded)+4096)*b['input_usd_per_million']+
            b['max_output_tokens']*b['output_usd_per_million'])/1e6



def verify_worlds(stored,regenerated):
    assert len(stored)==len(regenerated),'world_count_mismatch'
    differences=0;maximum=0.0
    for expected,actual in zip(stored,regenerated):
        # sin/cos coordinates are display-only and can differ by one final bit
        # between Linux and macOS libm. All decision-relevant fields stay exact.
        without_positions=lambda record:{**record,'world':{k:v for k,v in record['world'].items() if k!='positions'}}
        assert without_positions(expected)==without_positions(actual),'world_regeneration_mismatch'
        ep=expected['world']['positions'];ap=actual['world']['positions']
        assert ep.keys()==ap.keys(),'position_identity_mismatch'
        for node in ep:
            assert len(ep[node])==len(ap[node])==2,'position_dimension_mismatch'
            for old,new in zip(ep[node],ap[node]):
                assert type(old) is float and type(new) is float,'position_type_mismatch'
                difference=abs(old-new);maximum=max(maximum,difference)
                assert math.isclose(old,new,rel_tol=0,abs_tol=1e-15),'display_position_mismatch'
                differences+=old!=new
    return {'decision_fields_match_exactly':True,'display_coordinate_tolerance':1e-15,
            'display_coordinate_last_bit_differences':differences,'display_coordinate_max_abs_difference':maximum}


def verify_accounting(rows,indexed,summary):
    b=study.design()['budget'];paid=summary['params']['backend']=='anthropic'
    for row in rows:
        account=row.get('accounting',{})
        if row['status']=='not_started':assert not account,'not_started_has_call_accounting'
        if account.get('attempted'):
            assert paid,'scripted_row_attempted_api'
            close(account['reserved_usd'],request_reservation(indexed[row['id']]['packet']),'request_reservation_mismatch')
        if account.get('usage_reported'):
            assert account.get('attempted') is True,'usage_without_attempt'
            assert all(type(account.get(k)) is int and account[k]>=0 for k in ('input_tokens','output_tokens')),'invalid_usage_counter'
            expected=(account['input_tokens']*b['input_usd_per_million']+account['output_tokens']*b['output_usd_per_million'])/1e6
            close(account['actual_usd'],expected,'token_cost_mismatch')
        if paid and row['status']=='completed':
            assert account.get('attempted') is True and account.get('usage_reported') is True,'completed_api_usage_missing'
        if not paid:
            assert not account.get('attempted',False)
            close(account.get('actual_usd',0),0,'scripted_cost_nonzero')
    for field in ('input_tokens','output_tokens'):
        assert summary[field]==sum(r.get('accounting',{}).get(field,0) for r in rows),field+'_mismatch'
    calls=sum(r.get('accounting',{}).get('attempted',False) for r in rows)
    reported=sum(r.get('accounting',{}).get('usage_reported',False) for r in rows)
    cost=sum(r.get('accounting',{}).get('actual_usd',0) for r in rows)
    reserved=sum(r.get('accounting',{}).get('reserved_usd',0) for r in rows if r.get('accounting',{}).get('attempted',False))
    assert summary['model_calls']==calls,'model_call_count_mismatch'
    close(summary['cost_usd'],cost,'stage_cost_mismatch')
    initial=summary['initial_study_accounting'];final=summary['study_accounting']
    if paid:
        assert final['attempted_calls']-initial['attempted_calls']==calls,'ledger_attempt_delta_mismatch'
        assert final['usage_reported_calls']-initial['usage_reported_calls']==reported,'ledger_response_delta_mismatch'
        close(final['actual_usd']-initial['actual_usd'],cost,'ledger_actual_delta_mismatch')
        close(final['reserved_usd']-initial['reserved_usd'],reserved,'ledger_reservation_delta_mismatch')
        assert final['attempted_calls']<=b['max_attempted_calls'],'study_call_cap_exceeded'
        assert final['reserved_usd']<=b['aggregate_usd']+1e-9,'study_reservation_cap_exceeded'
        # Concurrent calls may settle before their outcome is recorded. Snapshots need
        # monotone bounds; they need not equal the already-recorded response prefix.
        previous=initial
        for row in rows:
            snapshot=row['study_accounting']
            for field in ('attempted_calls','usage_reported_calls','actual_usd','reserved_usd'):
                assert previous[field]-1e-9<=snapshot[field]<=final[field]+1e-9,'ledger_snapshot_out_of_bounds'
            assert snapshot['usage_reported_calls']<=snapshot['attempted_calls'],'more_responses_than_attempts'
            previous=snapshot
        assert not rows or rows[-1]['study_accounting']==final,'final_snapshot_mismatch'
    else:
        assert initial==final=={} and calls==0,'scripted_ledger_not_empty'
    return {'model_calls':calls,'usage_reported_calls':reported,'cost_usd':cost,'reserved_usd_this_stage':reserved}


def verify(path):
    path=Path(path);summary=json.loads((path/'summary.json').read_text());params=summary['params'];stage=params['stage']
    assert stage in ('S0','Q0','S1'),'unsupported_stage'
    assert params['source_hash']==study.source_hash(),'verification_requires_frozen_runtime'
    assert params['backend']==('scripted' if stage=='S0' else 'anthropic'),'stage_backend_mismatch'
    assignments=analyze.read_rows(path/'assignments.jsonl.gz');rows=analyze.read_rows(path/'episodes.jsonl.gz')
    indexed=unique_index(assignments,lambda a:a['id']);terminal=unique_index(rows,lambda r:r['id'])
    assert set(indexed)==set(terminal),'assigned_terminal_mismatch'
    stored_worlds=analyze.read_rows(path/'worlds.jsonl.gz')
    world_key=lambda w:(w['n'],w['world']['task'],w['kind'],w['rate'])
    world_records=unique_index(stored_worlds,world_key)
    # This runs the same simulator/check policies from the immutable source on the
    # declared seeds. It detects tampered packets, omitted cells and changed worlds,
    # rather than only checking whether retained inputs agree with retained grades.
    with tempfile.TemporaryDirectory(prefix='sybil-budget-verification-') as temporary:
        regenerated=study.assignments(stage,Path(temporary))
        regenerated_worlds=analyze.read_rows(Path(temporary)/'worlds.jsonl.gz')
    assert assignments==regenerated,'assignment_regeneration_mismatch'
    world_verification=verify_worlds(stored_worlds,regenerated_worlds)
    expected_world_keys={(a['n'],a['task'],a['kind'],a['attacker_pass'] if a['kind']=='pilot' else .1) for a in assignments}
    assert set(world_records)==expected_world_keys,'world_assignment_coverage_mismatch'
    previous_elapsed=0
    for index,row in enumerate(rows,1):
        a=indexed[row['id']]
        assert row['status'] in ('completed','failed','not_started'),'unknown_terminal_status'
        assert row['source_hash']==params['source_hash'] and row['code']==params['code'],'row_provenance_mismatch'
        assert row['stage']==stage,'row_stage_mismatch'
        if row['status']!='not_started':assert row['backend']==params['backend'],'row_backend_mismatch'
        assert row['completion_index']==index,'completion_order_mismatch'
        assert previous_elapsed<=row['elapsed_seconds']<=summary['elapsed_seconds'],'elapsed_order_mismatch'
        previous_elapsed=row['elapsed_seconds']
        assert all(row[k]==a[k] for k in ('task','n','arm','checks','visibility','attacker_pass','kind')),'assignment_label_mismatch'
        assert a['packet_hash']==study.digest(a['packet'])==row['packet_hash'],'packet_hash_mismatch'
        assert all(set(r)=={'node','skill','claim','age','activity','verification'} for r in a['packet']['reports']),'actor_packet_allowlist_mismatch'
        assert len(a['verification_events'])==a['checks'],'check_count_mismatch'
        checked=[event['node'] for event in a['verification_events']];assert len(checked)==len(set(checked)),'duplicate_check'
        world=world_records[(a['n'],a['task'],a['kind'],a['attacker_pass'] if a['kind']=='pilot' else .1)]['world']
        assert all(world['checks'][event['node']]==event['pass'] for event in a['verification_events']),'check_outcome_mismatch'
        admitted=[r['node'] for r in a['packet']['reports']]
        gm=sim.evaluate(world,admitted,sim.decide(world['public'],admitted),checked)
        assert gm==a['graph_metrics'],('graph_metric_mismatch',a['id'])
        if row['status']=='completed':
            assert row['evaluation']==study.evaluate(a,row['answer']),('grade_mismatch',row['id'])
            assert row['scripted_evaluation']==study.evaluate(a,study.scripted(a['packet'])),('scripted_grade_mismatch',row['id'])
    assert len({r['run'] for r in rows})==1,'mixed_run_ids'
    good=[r for r in rows if r['status']=='completed']
    assert summary['planned']==len(assignments)==summary['terminal']==len(rows),'assigned_terminal_counter_mismatch'
    assert summary['started']==sum(r['status']!='not_started' for r in rows),'started_counter_mismatch'
    assert summary['graded']==summary['analyzed']==len(good),'graded_analyzed_counter_mismatch'
    assert summary['invalid']==len(rows)-len(good),'invalid_counter_mismatch'
    assert summary['not_started']==sum(r['status']=='not_started' for r in rows),'not_started_counter_mismatch'
    accounting=verify_accounting(rows,indexed,summary)
    analysis=json.loads((path/'analysis.json').read_text());assert analysis==analyze.analyze(rows),'analysis_mismatch_use_matching_python'
    if stage=='S1':
        assert len(assignments)==2880 and len(analysis['cells'])==120
        assert all(c['assigned']==24 for c in analysis['cells'])
        assert len(stored_worlds)==240
    if stage in ('S0','Q0'):assert summary['qualification']==study.qualification(rows),'qualification_summary_mismatch'
    else:assert summary['qualification'] is None,'unexpected_scientific_qualification'
    from PIL import Image
    with Image.open(path/'replay.gif') as gif:
        frames=gif.n_frames
        for i in range(frames):gif.seek(i);gif.load()
        assert gif.size==(1920,1440),'replay_dimensions_mismatch'
        expected_frames=min(sum(r['status']!='not_started' for r in rows)+1,25)
        assert frames==expected_frames==summary['visualization']['frames'],'replay_frame_count_mismatch'
    with Image.open(path/'final_frame.png') as im:assert im.size==(1920,1440),'final_dimensions_mismatch'
    result={'stage':stage,'source_hash':params['source_hash'],'assignments':len(assignments),'rows':len(rows),'worlds':len(stored_worlds),'invalid':summary['invalid'],
        'all_assignments_worlds_packets_grades_and_analysis_match':True,'all_packet_hashes_grades_and_analysis_match':True,
        'all_execution_counters_reconciled':True,'accounting_reconciled':True,'accounting':accounting,'world_verification':world_verification,'gif_frames':frames,
        'note':'Assignments, worlds and check trajectories regenerated from frozen source; no API calls. Public browser playback is a separate deployment check.'}
    (path/'verification-summary.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('path');args=ap.parse_args();print(json.dumps(verify(args.path)))
