"""Offline native integration tests: synthetic budgets and fake provider only."""
from copy import deepcopy
import datetime as dt
import hashlib
import json
from pathlib import Path
import shutil
import socket
import sqlite3
import sys
import tempfile
import unittest
from unittest.mock import patch, Mock
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import cases
import native
import native_gates as gates
from native_budget import Ledger, baseline, snapshot
from native_report import (save, read, inventory, audit_bundle, audit_qualification,
                           Events, check_events, reconcile, finish_bundle)

NOW=dt.datetime(2026,10,4,20,0,tzinfo=dt.timezone.utc)


def response(req, action=None):
    action=action or cases.reference(req)
    return {'model':gates.SNAPSHOT,'provider':'TypeSafe','answers':{'action':{
        'choice':action,'probabilities':{a:float(a==action) for a in cases.ACTIONS},'confidence':1}},
        'usage':{'input_tokens':100,'cost':0.0000042}}


class FakeProvider:
    def __init__(self): self.requests=[]; self.failure=False; self.bad=False; self.routes=0
    def route(self): self.routes+=1
    def send(self,data):
        self.requests.append(data)
        if self.failure: raise OSError('SENSITIVE_SENTINEL_MUST_NOT_ESCAPE')
        result=response(json.loads(data))
        if self.bad: result['provider']='unapproved'
        return result


class EngineTransport:
    def __init__(self,engine): self.engine=engine; self.before=False; self.after=False
    def health(self):
        if self.before: raise OSError('pre_dispatch_disconnect')
        gates.require(self.engine.healthy(),'unhealthy')
    def send(self,a):
        result=self.engine.handle({'id':a['id'],'request':a['request'],'ordered_request_sha256':a['ordered_request_sha256']})
        if self.after: raise OSError('post_dispatch_disconnect')
        return result


class NativeTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.root=Path(self.temp.name).resolve()
        # No test is permitted to contact any remote service or credential store.
        self.net=patch.object(socket.socket,'connect',side_effect=AssertionError('NETWORK_FORBIDDEN'));self.net.start()
        self.packet=gates.prepare('Q0')
        self.receipt={'attempt':'rd6-q0-offline','expires_utc':(NOW+dt.timedelta(minutes=40)).isoformat()}
        self.dbpath=self.root/'synthetic.sqlite'
        db=sqlite3.connect(self.dbpath)
        db.execute('CREATE TABLE calls(key TEXT PRIMARY KEY,status TEXT,reserved_nano INTEGER,actual_nano INTEGER)')
        rows=[('historical-'+str(i),'completed',0,0) for i in range(488)]
        rows[0]=('historical-0','dispatch_unknown',4_032_000,None)
        rows[1]=('historical-1','completed',18_667_069,18_667_069)
        db.executemany('INSERT INTO calls VALUES(?,?,?,?)',rows);db.commit()
        st=self.dbpath.stat()
        self.authority=dict(baseline(db),ledger_path=str(self.dbpath),ledger_device=st.st_dev,ledger_inode=st.st_ino)
        db.close();self.ledgers=[];self.engines=[]

    def tearDown(self):
        for e in self.engines:
            if not e.events.file.closed:e.close()
        for l in self.ledgers:
            if not l.lock.closed:l.close()
        self.net.stop();self.temp.cleanup()

    def ledger(self,path=None,authority=None):
        obj=Ledger(path or self.dbpath,authority or self.authority);self.ledgers.append(obj);return obj

    def engine(self,stage='Q0'):
        packet=gates.prepare(stage);receipt=dict(self.receipt,attempt='rd6-'+stage.lower()+'-offline')
        e=native.RelayEngine(packet,receipt,self.ledger(),FakeProvider(),self.root/('relay-'+stage),now=lambda:NOW)
        self.engines.append(e);return e

    def run_engine(self,e,**kw):
        transport=EngineTransport(e)
        for k,v in kw.items():setattr(transport,k,v)
        out=self.root/('worker-'+e.packet['stage'])
        native.run_worker(e.packet,e.receipt,out,transport,mode='synthetic-offline',now=lambda:NOW)
        return out,read(out/'outcomes.json')

    def ref(self,name,value):
        p=self.root/(name+'.json');save(p,value);return {'path':str(p),'sha256':gates.sha(p)}

    def admission(self):
        p=self.packet
        r={'schema':'rd6-admission-v1','mode':'native','packet_sha256':cases.digest(p),
           'attempt':'rd6-q0-offline','verified_utc':NOW.isoformat(),
           'expires_utc':(NOW+dt.timedelta(minutes=40)).isoformat(),'worker_host':'synthetic-host'}
        r['owner_approval']=self.ref('approval',{'decision':'approved','approver_role':'owner',
            'authorization_ref':'SYNTHETIC TEST ONLY','scopes':['launch'],'stages':['Q0','D0'],
            'proposal_sha256':p['proposal_sha256'],'instrument_sha256':p['instrument_sha256'],
            'manifest_sha256':p['manifest_sha256'],'max_lifetime_calls':650,'max_new_calls':162,
            'api_cap_nano':gates.CAP,'infra_cap_nano':gates.CAP})
        r['parent_handoff']=self.ref('parent',{'study_id':'right-dissenter','attempt':'rd5-h5-a1'})
        r['allocation']=self.ref('allocation',{'verified_utc':NOW.isoformat(),'approved_account_identity':'synthetic-team',
            'credential_account_identity':'synthetic-team','exclusive':True,'study_id':'right-dissenter',
            'host':'synthetic-host','hourly_rate_nano':71_430_000,'maximum_minutes':90,'provisioner_state_verified':True,'resource_plan_sha256':'a'*64,
            'claim_id':'synthetic-claim','claim_started_utc':NOW.isoformat(),
            'claim_until':(NOW+dt.timedelta(minutes=50)).isoformat()})
        allocation=read(r['allocation']['path'])
        r['allocation_lineage_sha256']=cases.digest({k:allocation[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
        r['budget']=self.ref('budget',dict(self.authority,authority='original-right-dissenter-ledger',
            original_ledger_verified=True,single_writer_verified=True,infra_committed_nano=720_248_442,
            infra_reserved_nano=107_145_000,verified_utc=NOW.isoformat()))
        r['runtime']=self.ref('runtime',{'verified_utc':NOW.isoformat(),'worker_host':'synthetic-host',
            'instrument_sha256':p['instrument_sha256'],'offline_checks_passed':True,
            'verified_ssh_host_key':True,'exclusive_transport_verified':True,'source_commit':'a'*40})
        r['public_plan']=self.ref('public',{'checked_utc':NOW.isoformat(),'experiment':'right-dissenter-rd6',
            'plan_sha256':p['plan_sha256'],'url':'https://github.com/dmarzzz/swarm-lab/blob/'+'a'*40+'/researchers/vishesh/notes/dissent/reopening/PLAN.md',
            'public_page_verified':True,'condition_tldrs':{c:'SYNTHETIC Q0 condition-specific question treatment comparator metrics and limitations. '+c for c in ('C00','C11')},
            'run_tldr':'Q0 qualification with separate source-only clean and full-context uncertainty controls.'})
        return r

    def check_admission(self,r,**kw):
        # Only replace the synthetic lineage value; production uses the frozen H5 hash.
        review=read(gates.BASE/'DIAGNOSTIC-REVIEW.json');review['parent_handoff_sha256']=r['parent_handoff']['sha256']
        real_read=gates.read
        def load(p):return review if Path(p)==gates.BASE/'DIAGNOSTIC-REVIEW.json' else real_read(p)
        with patch.object(gates,'PARENT',r['parent_handoff']['sha256']),patch.object(gates,'read',side_effect=load):
            return gates.validate_admission(self.packet,r,now=NOW,host='synthetic-host',**kw)

    def test_real_prospective_review_is_valid(self):gates.validate_review(read(gates.BASE/'DIAGNOSTIC-REVIEW.json'))
    def test_packet_has_exact_stage_assignments(self):
        for stage,n in gates.STAGES.items():
            p=gates.prepare(stage);gates.validate_packet(p);self.assertEqual(len(p['assignments']),n)
    def test_self_consistent_manifest_mutation_rejected(self):
        p=deepcopy(self.packet);p['assignments'][0]['request']['state']['extra']='forbidden'
        p['assignments'][0]['request_sha256']=cases.digest(p['assignments'][0]['request'])
        with self.assertRaises(ValueError):gates.validate_packet(p)
    def test_criteria_order_change_rejected(self):
        p=deepcopy(self.packet);c=p['assignments'][0]['request']['questions']['action']['criteria']
        p['assignments'][0]['request']['questions']['action']['criteria']=dict(reversed(list(c.items())))
        self.assertEqual(cases.digest(p),cases.digest(self.packet))
        with self.assertRaises(ValueError):gates.validate_packet(p)
    def test_synthetic_complete_admission(self):self.check_admission(self.admission())
    def test_admission_denies_missing_or_changed_evidence(self):
        r=self.admission()
        for key in ('owner_approval','parent_handoff','allocation','budget','runtime','public_plan'):
            with self.subTest(key=key):
                bad=deepcopy(r);bad[key]['sha256']='0'*64
                with self.assertRaises(ValueError):self.check_admission(bad)
    def test_admission_denies_old_cap_missing_approval_or_wrong_source(self):
        for key,value in [('max_lifetime_calls',500),('decision','pending'),('instrument_sha256','0'*64),('stages',['D0']),('max_new_calls',163)]:
            with self.subTest(key=key):
                r=self.admission();a=read(r['owner_approval']['path']);a[key]=value;r['owner_approval']=self.ref('approval',a)
                with self.assertRaises(ValueError):self.check_admission(r)
    def test_admission_denies_wrong_account_shared_worker_or_wrong_host(self):
        for key,value in [('credential_account_identity','different-team'),('exclusive',False),('host','another-host'),('provisioner_state_verified',False)]:
            with self.subTest(key=key):
                r=self.admission();a=read(r['allocation']['path']);a[key]=value;r['allocation']=self.ref('allocation',a)
                with self.assertRaises(ValueError):self.check_admission(r)
    def test_admission_denies_stale_or_short_lease(self):
        for field,value in [('verified_utc',(NOW-dt.timedelta(minutes=6)).isoformat()),('expires_utc',(NOW+dt.timedelta(minutes=30)).isoformat())]:
            r=self.admission();r[field]=value
            with self.assertRaises(ValueError):self.check_admission(r)
    def test_admission_denies_missing_condition_tldr(self):
        r=self.admission();a=read(r['public_plan']['path']);a['condition_tldrs'].pop('C11');r['public_plan']=self.ref('public',a)
        with self.assertRaises(ValueError):self.check_admission(r)
    def test_infra_limit_enforced(self):
        r=self.admission();a=read(r['budget']['path']);a['infra_committed_nano']=950_000_000
        r['budget']=self.ref('budget',a)
        with self.assertRaises(ValueError):self.check_admission(r)
    def test_original_ledger_baseline_preserved(self):
        e=self.engine();self.run_engine(e)
        self.assertEqual(baseline(e.ledger.db),{k:self.authority[k] for k in baseline(e.ledger.db)})
        self.assertEqual(snapshot(e.ledger.db)['lifetime_calls'],506)
    def test_copy_reset_and_missing_ledger_denied(self):
        copied=self.root/'copy.sqlite';shutil.copyfile(self.dbpath,copied)
        for path in (copied,self.root/'missing.sqlite'):
            with self.assertRaises((ValueError,FileNotFoundError)):self.ledger(path)
        db=sqlite3.connect(self.dbpath);db.execute("DELETE FROM calls WHERE key='historical-5'");db.commit();db.close()
        with self.assertRaises(ValueError):self.ledger()
    def test_second_writer_denied(self):
        self.ledger()
        with self.assertRaises(BlockingIOError):self.ledger()
    def test_duplicate_attempt_denied(self):
        l=self.ledger();l.begin(self.packet,'rd6-q0-one')
        with self.assertRaises(sqlite3.IntegrityError):l.begin(self.packet,'rd6-q0-two')
    def test_duplicate_assignment_denied(self):
        e=self.engine();a=e.packet['assignments'][0];t=EngineTransport(e);t.send(a)
        with self.assertRaises(ValueError):t.send(a)
        self.assertEqual(len(e.provider.requests),1)
    def test_ordered_wire_is_exact_and_no_evaluator_fields(self):
        e=self.engine();self.run_engine(e)
        self.assertEqual(e.provider.requests,[gates.wire(a['request']) for a in e.packet['assignments']])
        for data in e.provider.requests:
            self.assertEqual(set(json.loads(data)),{'model','provider','state','questions'})
    def test_repeats_are_new_calls_with_identical_inputs(self):
        e=self.engine('D0');out,rows=self.run_engine(e)
        self.assertEqual(len(e.provider.requests),144)
        self.assertEqual(snapshot(e.ledger.db)['lifetime_calls'],632)
        bycell={}
        for a,data in zip(e.packet['assignments'],e.provider.requests):bycell.setdefault((a['case'],a['condition']),[]).append(data)
        self.assertTrue(all(len(v)==2 and v[0]==v[1] for v in bycell.values()))
        summary=read(out/'summary.json');self.assertEqual(summary['repeat_cells_complete'],72);self.assertEqual(summary['primary_bounds'],[0,0])
        audit_bundle(out,read(out/'bundle.json')['sha256'])
    def test_all_calls_cumulative_limit_650(self):
        q=self.engine();self.run_engine(q);q.close()
        d=self.engine('D0');self.run_engine(d)
        self.assertEqual(snapshot(d.ledger.db)['lifetime_calls'],650)
        with self.assertRaises(ValueError):d.ledger.reserve(d.packet,d.packet['assignments'][0])
    def test_api_cap_reserve_before_dispatch(self):
        e=self.engine();e.ledger.db.execute("INSERT INTO calls VALUES('RD6:old:synthetic','dispatch_unknown',980000000,NULL)");e.ledger.db.commit()
        self.run_engine(e);self.assertEqual(e.provider.requests,[])
    def test_pre_dispatch_disconnect_has_zero_reservations_and_all_slots(self):
        e=self.engine();out,rows=self.run_engine(e,before=True)
        self.assertEqual(snapshot(e.ledger.db)['lifetime_calls'],488)
        self.assertEqual(len(rows),18);self.assertEqual(rows[0]['status'],'failed');self.assertEqual(rows[1]['status'],'unstarted')
        self.assertEqual(rows[0]['reservation'],'none')
    def test_post_dispatch_disconnect_does_not_retry_or_erase_charge(self):
        e=self.engine();out,rows=self.run_engine(e,after=True)
        self.assertEqual(len(e.provider.requests),1);self.assertEqual(rows[0]['status'],'failed')
        self.assertEqual(rows[0]['reservation'],'unknown');self.assertEqual(snapshot(e.ledger.db)['lifetime_calls'],489)
        self.assertEqual(e.ledger.db.execute("SELECT status FROM calls WHERE key LIKE 'RD6:%'").fetchone()[0],'completed')
    def test_provider_failure_retains_uncertain_reservation(self):
        e=self.engine();e.provider.failure=True;out,rows=self.run_engine(e)
        self.assertEqual(snapshot(e.ledger.db)['api_committed_nano'],22_699_069+gates.RESERVE)
        self.assertEqual(e.ledger.db.execute("SELECT actual_nano FROM calls WHERE key LIKE 'RD6:%'").fetchone()[0],None)
        all_text=''.join(p.read_text() for p in out.iterdir() if p.is_file())
        self.assertNotIn('SENSITIVE_SENTINEL',all_text)
    def test_bad_provider_schema_stops_and_accounts_cost(self):
        e=self.engine();e.provider.bad=True;out,rows=self.run_engine(e)
        self.assertEqual(len(e.provider.requests),1);self.assertEqual(rows[0]['status'],'invalid')
        self.assertEqual(e.ledger.db.execute("SELECT status FROM calls WHERE key LIKE 'RD6:%'").fetchone()[0],'invalid_response')
        self.assertEqual(snapshot(e.ledger.db)['api_committed_nano'],22_699_069+4200)
    def test_over_reservation_cost_is_recorded_and_stops(self):
        e=self.engine();a=e.packet['assignments'][0];key=e.ledger.reserve(e.packet,a);r=response(a['request']);r['usage']['cost']=.002
        with self.assertRaises(ValueError):e.ledger.settle(key,r,a['request'])
        self.assertEqual(snapshot(e.ledger.db)['api_committed_nano'],22_699_069+2_000_000)
    def test_expired_lease_never_dispatches(self):
        e=self.engine();e.now=lambda:NOW+dt.timedelta(minutes=40)
        self.run_engine(e);self.assertEqual(e.provider.requests,[])
    def test_q0_wrong_answer_blocks_d0(self):
        e=self.engine();e.provider.send=lambda data:response(json.loads(data),'PROCEED')
        out,rows=self.run_engine(e);self.assertFalse(read(out/'summary.json')['qualification_passed'])
        with self.assertRaises(ValueError):audit_qualification(out,gates.prepare('D0'),read(out/'bundle.json')['sha256'],{})
    def test_synthetic_q0_cannot_admit_native_d0(self):
        e=self.engine();out,rows=self.run_engine(e);self.assertTrue(read(out/'summary.json')['qualification_passed'])
        with self.assertRaises(ValueError):audit_qualification(out,gates.prepare('D0'),read(out/'bundle.json')['sha256'],{})
    def test_unknown_missingness_is_bounded_not_zero(self):
        e=self.engine('D0');out,rows=self.run_engine(e,before=True)
        s=read(out/'summary.json');self.assertEqual(s['primary_bounds'],[-1,1]);self.assertEqual(s['repeat_cells_complete'],0)
    def test_unknown_id_duplicate_and_changed_hash_rejected(self):
        e=self.engine();out,rows=self.run_engine(e)
        for f in ('id','ordered_request_sha256','request_sha256'):
            changed=deepcopy(rows);changed[0][f]='changed'
            with self.assertRaises(ValueError):reconcile(e.packet,changed)
        with self.assertRaises(ValueError):reconcile(e.packet,rows+[rows[0]])
    def test_bundle_tamper_rejected(self):
        e=self.engine();out,rows=self.run_engine(e);bundle=read(out/'bundle.json')
        (out/'summary.json').write_text('{}')
        with self.assertRaises(ValueError):audit_bundle(out,bundle['sha256'])
    def test_event_tamper_rejected(self):
        path=self.root/'events';e=Events(path);e.add('one');e.add('two');e.close()
        text=path.read_text().replace('"one"','"changed"');path.write_text(text)
        with self.assertRaises(ValueError):check_events(path)
    def test_grid_has_every_cell_and_input_link(self):
        e=self.engine('D0');out,rows=self.run_engine(e)
        view=(out/'replay.html').read_text()
        self.assertEqual(view.count('data-id='),144);self.assertEqual(view.count('<details id='),144)
        self.assertIn('SYNTHETIC OFFLINE',view)
        for a in e.packet['assignments']:self.assertIn('href="#'+a['id']+'"',view)
    def test_finalize_rejects_synthetic_and_unverified_stop(self):
        e=self.engine();out,rows=self.run_engine(e);cmd=Mock()
        with self.assertRaises(ValueError):native.finalize(out,self.ref('stop',{}),command=cmd)
        cmd.assert_not_called()
    def test_prepare_cli_does_not_open_ledger_or_provider(self):
        with patch.object(native,'Provider',side_effect=AssertionError('credential access')),patch.object(native,'Ledger',side_effect=AssertionError('ledger access')):
            p=gates.prepare('Q0');self.assertEqual(len(p['assignments']),18)
    def test_route_mismatch_fails_before_credential_read(self):
        with patch.object(native.Provider,'route',side_effect=ValueError('route_mismatch')):
            with self.assertRaises(ValueError):native.Provider(self.root/'never-read-credential')

    def test_collect_failure_preserves_source_and_never_reexecutes(self):
        from native_operator import collect
        e=self.engine();out,rows=self.run_engine(e);b=read(out/'bundle.json')['sha256'];before=inventory(out)
        def fail(*args):raise OSError('synthetic_upload_failure')
        with self.assertRaises(OSError):collect(out,self.root/'published',b,copier=fail)
        self.assertFalse((self.root/'published').exists());self.assertEqual(inventory(out),before)
        self.assertEqual(len(e.provider.requests),18)
        collect(out,self.root/'published',b);audit_bundle(self.root/'published',b)
    def test_supervisor_cleans_both_children_when_relay_dies(self):
        r=Mock();r.poll.side_effect=[None,1,1];r.pid=111
        w=Mock();w.poll.return_value=None;w.pid=222
        transport=Mock()
        with patch.object(native,'stop_child') as stop:
            with self.assertRaises(ValueError):native.supervise(['relay'],['worker'],transport,popen=Mock(side_effect=[r,w]))
            self.assertEqual([x.args[0] for x in stop.call_args_list],[w,r])
    def test_supervisor_cleans_relay_on_worker_creation_failure(self):
        r=Mock();r.poll.return_value=None;r.pid=111
        with patch.object(native,'stop_child') as stop:
            with self.assertRaises(OSError):native.supervise(['relay'],['worker'],Mock(),popen=Mock(side_effect=[r,OSError('synthetic_start_failure')]))
            stop.assert_called_once_with(r)
    def test_wall_deadline_stops_trickling_or_stalled_transport(self):
        import time
        with self.assertRaises(TimeoutError):
            with native.deadline(.01):time.sleep(.03)
    def test_finalization_hook_runs_only_after_verified_stop(self):
        # Fabricated native marker is strictly local test input, never exported.
        e=self.engine();out,rows=self.run_engine(e)
        execution=read(out/'execution.json');execution['mode']='native';save(out/'execution.json',execution)
        files=inventory(out);save(out/'bundle.json',{'files':files,'sha256':cases.digest(files)})
        stop=self.ref('stop',{'attempt':execution['attempt'],'bundle_sha256':cases.digest(files),
            'worker_stopped_verified':True,'relay_stopped_verified':True,'verifier':'SYNTHETIC TEST ONLY'})
        command=Mock(return_value=Mock(returncode=0,stdout=json.dumps({'closeout_status':'written_review_required'})))
        result=native.finalize(out,stop,command=command)
        self.assertIn('--worker-stopped',command.call_args.args[0]);self.assertEqual(result['scientific_review'],'required')
        command.return_value.stdout=json.dumps({'closeout_status':'failed'})
        with self.assertRaises(ValueError):native.finalize(out,stop,command=command)
    def test_grid_initial_transition_failure_final_statuses(self):
        from native_report import render
        e=self.engine('D0');out,complete=self.run_engine(e)
        rows=[dict(id=a['id'],request_sha256=a['request_sha256'],ordered_request_sha256=a['ordered_request_sha256'],status='unstarted',action=None) for a in e.packet['assignments']]
        for state in ('initial','transition','failure','final'):
            if state=='transition':rows[:2]=deepcopy(complete[:2])
            if state=='failure':rows[2].update(status='failed',reservation='unknown')
            if state=='final':rows=complete
            render(e.packet,rows,out,'SYNTHETIC OFFLINE '+state)
            view=(out/'replay.html').read_text()
            self.assertEqual(view.count('data-id='),144)
            self.assertEqual(view.count('class="unstarted"'),sum(r['status']=='unstarted' for r in rows))
            self.assertEqual(view.count('class="failed"'),sum(r['status']=='failed' for r in rows))
    def test_stable_degradation_requires_two_distinct_families(self):
        e=self.engine('D0');out,rows=self.run_engine(e);assignments=e.packet['assignments']
        families=list(dict.fromkeys(a['family'] for a in assignments))[:2]
        selected={next(a['case'] for a in assignments if a['family']==f) for f in families}
        for a,r in zip(assignments,rows):
            if a['condition']=='C11' and a['case'] in selected:
                wrong=response(a['request'],'DEFER')
                from native_budget import validate
                r.update(action='DEFER',visible_response=wrong,checked=validate(wrong,a['request'],gates.SNAPSHOT))
        s=reconcile(e.packet,rows)
        self.assertTrue(s['stable_degradation']['engineering_trigger']);self.assertEqual(len(s['stable_degradation']['cases']),2)
        self.assertAlmostEqual(s['primary_bounds'][0],-1/6)
        self.assertIn('history_ballots_interaction',s['secondary_contrasts'])

    def test_relay_accounting_reconciles_all_charges_and_events(self):
        from native_report import reconcile_accounting
        e=self.engine();out,rows=self.run_engine(e)
        accounting=e.ledger.accounting(e.packet)
        result=reconcile_accounting(e.packet,rows,accounting,e.out/'relay-events.jsonl')
        self.assertEqual(result['ledger_calls'],18);self.assertEqual(result['stage_committed_nano'],18*4200)
        accounting['calls'][0]['actual_nano']=0
        with self.assertRaises(ValueError):reconcile_accounting(e.packet,rows,accounting,e.out/'relay-events.jsonl')
    def test_relay_only_answer_is_reported_without_overwriting_worker(self):
        from native_report import reconcile_accounting
        e=self.engine();out,rows=self.run_engine(e,after=True)
        result=reconcile_accounting(e.packet,rows,e.ledger.accounting(e.packet),e.out/'relay-events.jsonl')
        self.assertEqual(result['relay_response_missing_from_worker'],[rows[0]['id']])
        self.assertEqual(rows[0]['status'],'failed');self.assertEqual(result['stage_committed_nano'],4200)

    def test_http_adapters_preserve_provider_body_and_order(self):
        import io
        a=self.packet['assignments'][0]
        p=native.Provider.__new__(native.Provider);p.secret='synthetic-test-only'
        p.opener=Mock();p.opener.open.return_value=io.BytesIO(json.dumps(response(a['request'])).encode())
        p.send(gates.wire(a['request']))
        request=p.opener.open.call_args.args[0]
        self.assertEqual(request.full_url,'https://openrouter.ai/api/alpha/decisions')
        self.assertEqual(request.data,gates.wire(a['request']))
        self.assertEqual(request.get_method(),'POST')
        transport=native.Transport(self.packet);transport.opener=Mock()
        transport.opener.open.return_value=io.BytesIO(b'{}');transport.send(a)
        body=json.loads(transport.opener.open.call_args.args[0].data)
        self.assertEqual(gates.wire(body['request']),gates.wire(a['request']))
        self.assertNotIn('expected',body)
    def test_relay_admission_failure_reads_no_credential_and_changes_no_ledger(self):
        with patch.object(native,'live_preflight',side_effect=ValueError('not_approved')),patch.object(native,'Provider') as provider,patch.object(native,'Ledger') as ledger:
            with self.assertRaises(ValueError):native.relay(self.packet,{},'unused','unused',self.root/'unused')
            provider.assert_not_called();ledger.assert_not_called()
    def test_redirects_are_never_followed(self):
        with self.assertRaises(ValueError):native.NoRedirect().redirect_request(None,None,302,'redirect',{},'https://example.invalid')

    def test_infrastructure_cannot_reset_prior_spend_or_underreserve(self):
        for key,value in [('infra_committed_nano',0),('infra_reserved_nano',1)]:
            r=self.admission();b=read(r['budget']['path']);b[key]=value;r['budget']=self.ref('budget',b)
            with self.assertRaises(ValueError):self.check_admission(r)

    def test_allocation_cannot_extend_beyond_90_minutes(self):
        r=self.admission();a=read(r['allocation']['path']);a['claim_until']=(NOW+dt.timedelta(minutes=91)).isoformat()
        r['allocation']=self.ref('allocation',a)
        r['allocation_lineage_sha256']=cases.digest({k:a[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
        with self.assertRaises(ValueError):self.check_admission(r)

    def test_worker_creates_missing_parents_without_changing_requests(self):
        e=self.engine();out=self.root/'missing'/'nested'/'attempt'
        self.assertTrue(native.run_worker(e.packet,e.receipt,out,EngineTransport(e),mode='synthetic-offline',now=lambda:NOW))
        self.assertEqual(len(e.provider.requests),18)
        self.assertEqual(e.provider.requests,[gates.wire(a['request']) for a in e.packet['assignments']])

    def test_existing_worker_output_is_never_reused(self):
        transport=Mock();out=self.root/'retained';out.mkdir();(out/'evidence').write_text('original')
        with self.assertRaises(FileExistsError):native.run_worker(self.packet,self.receipt,out,transport)
        transport.health.assert_not_called();transport.send.assert_not_called()
        self.assertEqual((out/'evidence').read_text(),'original')

    def test_startup_failure_has_safe_diagnostics_and_no_transport(self):
        out=self.root/'missing'/'worker';factory=Mock()
        with patch.object(native,'live_preflight',side_effect=ValueError('SENSITIVE_SENTINEL_MUST_NOT_ESCAPE')):
            with self.assertRaises(ValueError):native.admitted_worker(self.packet,self.receipt,out,transport_factory=factory)
        diagnostic=out.with_name(out.name+'.startup.json').read_text()
        self.assertNotIn('SENSITIVE_SENTINEL',diagnostic)
        self.assertEqual(json.loads(diagnostic)['error_category'],'startup_check_failed')
        self.assertFalse(out.exists());factory.assert_not_called()
        with self.assertRaises(FileExistsError):native.admitted_worker(self.packet,self.receipt,out,transport_factory=factory)
        self.assertEqual(out.with_name(out.name+'.startup.json').read_text(),diagnostic)

    def test_worker_preflight_makes_no_provider_or_ledger_access(self):
        out=self.root/'nested'/'worker'
        with patch.object(native,'live_preflight'),patch.object(native,'Provider') as p,patch.object(native,'Ledger') as ledger:
            native.worker_preflight(self.packet,self.receipt,out)
        self.assertTrue(out.parent.exists());self.assertFalse(out.exists())
        p.assert_not_called();ledger.assert_not_called()

    def test_admission_changed_after_staging_fails(self):
        p=self.root/'admission.json';save(p,self.receipt);expected=gates.sha(p)
        self.assertEqual(native.bound_admission(p,expected),self.receipt)
        save(p,dict(self.receipt,attempt='rd6-q0-changed'))
        with self.assertRaises(ValueError):native.bound_admission(p,expected)

    def test_remote_preflight_requires_exact_acknowledgment(self):
        from native_operator import remote_preflight
        from types import SimpleNamespace
        a=SimpleNamespace(remote_checkout='/synthetic/checkout',remote_packet='packet',remote_admission='receipt',remote_out='results/new',ssh_config='synthetic.conf',host_alias='synthetic')
        expected={'worker_preflight':'ready','packet_sha256':cases.digest(self.packet),'admission_sha256':'a'*64}
        command=Mock(return_value=Mock(returncode=0,stdout=json.dumps(expected)))
        self.assertEqual(remote_preflight(a,self.packet,'a'*64,command=command),expected)
        self.assertIn('check-worker',command.call_args.args[0][-1])
        for result in (Mock(returncode=1,stdout='SENSITIVE_SENTINEL'),Mock(returncode=0,stdout='{}'),Mock(returncode=0,stdout='not json')):
            command.return_value=result
            with self.assertRaises(ValueError):remote_preflight(a,self.packet,'a'*64,command=command)

    def replacement(self,ledger):
        old=deepcopy(self.packet);old['historical_fixture']=True
        ledger.begin(old,'rd6-q0-a1');ledger.finish('Q0','stopped')
        return {'attempt':'rd6-q0-a2','previous_attempt':'rd6-q0-a1',
                'previous_packet_sha256':cases.digest(old),'packet_sha256':cases.digest(self.packet),
                'owner_approval_sha256':'f'*64}

    def test_zero_dispatch_replacement_preserves_old_attempt_and_limits(self):
        l=self.ledger();r=self.replacement(l);before=l.db.execute('SELECT * FROM rd6_attempts').fetchall()
        l.begin(self.packet,'rd6-q0-a2',r)
        for a in self.packet['assignments']:
            key=l.reserve(self.packet,a);l.settle(key,response(a['request']),a['request'])
        l.finish('Q0','completed')
        self.assertEqual(l.db.execute('SELECT * FROM rd6_attempts').fetchall(),before)
        self.assertEqual(l.db.execute('SELECT attempt,status FROM rd6_zero_replacements').fetchall(),[('rd6-q0-a2','completed')])
        self.assertEqual(snapshot(l.db)['lifetime_calls'],506)
        with self.assertRaises(ValueError):l.reserve(self.packet,self.packet['assignments'][0])

    def test_zero_dispatch_replacement_rejects_any_rd6_reservation(self):
        l=self.ledger();r=self.replacement(l)
        for status in ('dispatch_unknown','completed','invalid_response','failed'):
            l.db.execute('INSERT INTO calls VALUES(?,?,?,?)',('RD6:Q0:sent',status,1344000,None));l.db.commit()
            with self.assertRaises(ValueError):l.begin(self.packet,'rd6-q0-a2',r)
            self.assertEqual(l.db.execute('SELECT count(*) FROM rd6_zero_replacements').fetchone()[0],0)
            l.db.execute("DELETE FROM calls WHERE key='RD6:Q0:sent'");l.db.commit()

    def test_zero_dispatch_replacement_rejects_active_or_wrong_predecessor(self):
        l=self.ledger();r=self.replacement(l)
        for change in ({'previous_attempt':'rd6-q0-other'},{'previous_packet_sha256':'b'*64},{'attempt':'rd6-q0-a3'},{'packet_sha256':'c'*64},{'owner_approval_sha256':None}):
            with self.assertRaises(ValueError):l.begin(self.packet,'rd6-q0-a2',dict(r,**change))
        l.db.execute("UPDATE rd6_attempts SET status='started'");l.db.commit()
        with self.assertRaises(ValueError):l.begin(self.packet,'rd6-q0-a2',r)

    def test_zero_dispatch_replacement_cannot_be_repeated_or_used_for_d0(self):
        l=self.ledger();r=self.replacement(l);l.begin(self.packet,'rd6-q0-a2',r);l.finish('Q0','stopped')
        with self.assertRaises(sqlite3.IntegrityError):l.begin(self.packet,'rd6-q0-a2',r)
        with self.assertRaises(ValueError):l.begin(gates.prepare('D0'),'rd6-d0-a2',r)

    def test_replacement_requires_explicit_bound_approval_and_review(self):
        receipt=self.admission();receipt['attempt']='rd6-q0-a2'
        approval=read(receipt['owner_approval']['path'])
        approval.update(replacement_attempt='rd6-q0-a2',previous_attempt='rd6-q0-a1',replacement_contract_sha256=gates.sha(gates.BASE/'STARTUP-REPAIR.md'))
        receipt['owner_approval']=self.ref('approval',approval)
        closeout=self.ref('zero-closeout',{'study_id':'right-dissenter','attempt':'rd6-q0-a1'})
        receipt['latest_closeout']=closeout
        proof=self.ref('zero-proof',{'attempt':'rd6-q0-a1','dispatched':0,'provider_responses':0,'native_calls':0,'lifetime_calls':488,'committed_api_nano':22699069,'worker_stopped_verified':True,'relay_stopped_verified':True})
        review=self.ref('zero-review',{'attempt':'rd6-q0-a1','verdict':'repair','operational_closeout_sha256':closeout['sha256'],'scientific_result':'not_tested','zero_dispatch_proof_sha256':proof['sha256'],
            'assessments':[{'dimension':d,'status':'unknown','finding':'SYNTHETIC TEST ONLY','next_action':'test','acceptance_check':'test'} for d in gates.DIMENSIONS]})
        r={'attempt':'rd6-q0-a2','previous_attempt':'rd6-q0-a1','previous_packet_sha256':gates.ZERO_PACKET,'packet_sha256':cases.digest(self.packet),'owner_approval_sha256':receipt['owner_approval']['sha256'],
           'previous_closeout_sha256':closeout['sha256'],'zero_dispatch_proof':proof,'owning_review':review}
        receipt['zero_dispatch_replacement']=self.ref('replacement',r)
        with patch.object(gates,'ZERO_PARENT',closeout['sha256']):
            gates.validate_replacement(self.packet,receipt,approval)
            for field in ('replacement_attempt','previous_attempt','replacement_contract_sha256'):
                changed=deepcopy(approval);del changed[field]
                with self.assertRaises(ValueError):gates.validate_replacement(self.packet,receipt,changed)
            changed=read(proof['path']);changed['native_calls']=1
            r['zero_dispatch_proof']=self.ref('zero-proof',changed);receipt['zero_dispatch_replacement']=self.ref('replacement',r)
            with self.assertRaises(ValueError):gates.validate_replacement(self.packet,receipt,approval)

    def test_replacement_cannot_extend_window_or_reset_infrastructure(self):
        # Scope evidence has separate tests; isolate cumulative resource arithmetic.
        def receipt():
            r=self.admission();r['zero_dispatch_replacement']={}
            a=read(r['allocation']['path']);a['claim_until']=(NOW+dt.timedelta(minutes=40)).isoformat()
            r['allocation']=self.ref('allocation',a)
            r['allocation_lineage_sha256']=cases.digest({k:a[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
            b=read(r['budget']['path']);b.update(infra_committed_nano=gates.ZERO_INFRA_COMMITTED,infra_reserved_nano=47_620_000)
            r['budget']=self.ref('budget',b);return r
        with patch.object(gates,'validate_replacement'):
            self.check_admission(receipt())
            for key,value in [('infra_committed_nano',720_248_442),('infra_reserved_nano',47_619_999),('infra_reserved_nano',80_219_859)]:
                r=receipt();b=read(r['budget']['path']);b[key]=value;r['budget']=self.ref('budget',b)
                with self.assertRaises(ValueError):self.check_admission(r)
            r=receipt();a=read(r['allocation']['path']);a['claim_until']=(NOW+dt.timedelta(minutes=41)).isoformat()
            r['allocation']=self.ref('allocation',a)
            r['allocation_lineage_sha256']=cases.digest({k:a[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
            with self.assertRaises(ValueError):self.check_admission(r)

    def test_zero_dispatch_replacement_rejects_orphan_response(self):
        l=self.ledger();r=self.replacement(l)
        l.db.execute('INSERT INTO rd6_responses VALUES(?,?)',('RD6:Q0:orphan','{}'));l.db.commit()
        with self.assertRaises(ValueError):l.begin(self.packet,'rd6-q0-a2',r)

    def test_failed_remote_startup_does_not_create_relay(self):
        import native_operator as op
        from types import SimpleNamespace
        p=self.root/'packet.json';save(p,self.packet)
        r=self.root/'receipt.json';save(r,self.receipt)
        config=self.root/'ssh.conf';config.write_text('synthetic')
        a=SimpleNamespace(packet=str(p),admission=str(r),ssh_config=str(config),host_alias='synthetic',
             remote_checkout='/synthetic/repo',remote_packet='packet',remote_admission='receipt',remote_out='results/new',
             out=str(self.root/'nested'/'supervisor'),credential='MUST_NOT_READ',ledger='MUST_NOT_OPEN')
        runtime={'ssh_config_sha256':gates.sha(config),'host_alias':a.host_alias,'remote_checkout':a.remote_checkout,'gnu_timeout_verified':True}
        self.receipt['runtime']={};save(r,self.receipt)
        with patch.object(op,'live_preflight'),patch.object(op,'evidence',return_value=runtime),patch.object(op,'remote_preflight',side_effect=ValueError('SENSITIVE_SENTINEL')),patch.object(op,'supervise') as supervisor:
            with self.assertRaises(ValueError):op.launch(a)
        supervisor.assert_not_called()
        status=(Path(a.out)/'supervisor.json').read_text()
        self.assertNotIn('SENSITIVE_SENTINEL',status)
        self.assertEqual(json.loads(status)['phase'],'remote_startup_check')

    def test_conditional_d0_retains_replacement_resource_window(self):
        self.packet=gates.prepare('D0');r=self.admission();r['attempt']='rd6-d0-offline'
        a=read(r['allocation']['path']);a['claim_until']=(NOW+dt.timedelta(minutes=40)).isoformat()
        r['allocation']=self.ref('allocation',a)
        r['allocation_lineage_sha256']=cases.digest({k:a[k] for k in ('claim_id','host','claim_started_utc','claim_until','resource_plan_sha256')})
        b=read(r['budget']['path']);b.update(infra_committed_nano=gates.ZERO_INFRA_COMMITTED,infra_reserved_nano=47_620_000);r['budget']=self.ref('budget',b)
        public=read(r['public_plan']['path']);public['run_tldr']='D0 SYNTHETIC TEST ONLY';public['condition_tldrs']={c:'SYNTHETIC TEST ONLY. Question treatment comparator metrics and limitations; not real registration. '+c for c in ('C00','C10','C01','C11','CT','CA')};r['public_plan']=self.ref('public',public)
        q=self.root/'qualification';q.mkdir();save(q/'execution.json',{'zero_dispatch_predecessor':'rd6-q0-a1'})
        r['qualification_directory']=str(q)
        self.check_admission(r)  # Pure resource check, not native qualification.
        b['infra_reserved_nano']=80_219_859;r['budget']=self.ref('budget',b)
        with self.assertRaises(ValueError):self.check_admission(r)


if __name__=='__main__':unittest.main()
