"""Finite native executor; refuses absent or stale funded admission. No retries."""
import argparse,datetime,hashlib,json,os,socket,sqlite3,subprocess
from contextlib import closing
from pathlib import Path
import instrument as i
BASE=Path(__file__).resolve().parent

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def verify_admission(path):
    r=json.loads(Path(path).read_text());p=json.loads((BASE/'packet.json').read_text())
    assert r['stage']=='verification-v1' and r['funded'] is True and r['pi_decision_reference']
    assert r['commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=BASE).strip()
    assert r['packet_sha256']==sha(BASE/'packet.json') and r['plan_sha256']==sha(BASE/'PLAN.md')
    assert p['assignments']==i.assignments()
    for rel,h in p['source_sha256'].items():assert sha(BASE.parent/rel)==h
    assert r['max_calls']==192 and r['model_max_usd']==10.629120 and r['all_in_max_usd']==10.779120
    assert r['approved_cumulative_model_cap_usd']>=16.877155
    assert 0<=r['infrastructure_reserved_usd']<=.15 and r['infrastructure_centrally_reconciled'] is True
    assert r['rates_verified'] is True and r['remote_tests_passed'] is True and r['runtime_source_verified'] is True
    assert r['model']==i.MODEL and r['input_rate']==5 and r['output_rate']==25
    a=r['allocation'];assert a['host']==socket.gethostname() and a['exclusive'] and a['approved_account_verified'] and a['claim_reference']
    now=datetime.datetime.now(datetime.timezone.utc)
    assert datetime.datetime.fromisoformat(a['expires'].replace('Z','+00:00'))-now>datetime.timedelta(minutes=65)
    assert sha(os.environ['SWARM_BUDGET_LEDGER'])==r['ledger_sha256']
    with closing(sqlite3.connect('file:'+os.environ['SWARM_BUDGET_LEDGER']+'?mode=ro',uri=True)) as db:
        cap,reserved,calls=db.execute('select cap,reserved,calls from budget where id=1').fetchone()
        assert cap==r['approved_cumulative_model_cap_usd'] and calls==517 and abs(reserved-6.248035)<1e-8 and reserved+10.629120<=cap+1e-9
        assert db.execute('pragma integrity_check').fetchone()[0]=='ok'
        assert db.execute('select count(*) from immune_requests where run_id=?',('verification-v1',)).fetchone()[0]==0
    import sys
    sys.path.insert(0,str(BASE.parent.parent/'experiment-documentation'))
    from public_plan import check
    public=check('immune-response-v3','Verification v1: paired fresh confirmation/contradiction, unguarded versus explicit guard,6authored roots in3families,2fresh repeats,192calls; protected outcomes separate from proposal competence.')
    assert public['commit']==r['commit'] and public['plan_sha256']==r['plan_sha256']
    return r

def execute(out,admission):
    receipt=verify_admission(admission);out=Path(out);out.mkdir(parents=True,exist_ok=False)
    (out/'admission.json').write_text(json.dumps(receipt,indent=2))
    from native import Policy
    policy=Policy(os.environ['SWARM_BUDGET_LEDGER'],out/'usage.jsonl')
    rows=[];started=[];error=None;worlds={c['id']:c for c in i.study.roots()}
    with (out/'events.jsonl').open('x') as ef,(out/'episodes.jsonl').open('x') as rf:
        def emit(e):ef.write(json.dumps(e)+'\n');ef.flush();os.fsync(ef.fileno())
        try:
            for a in i.assignments():
                started.append(a['id']);emit({'kind':'episode_started',**a})
                def event(e):emit({'assignment':a['id'],**e})
                row=i.episode(worlds[a['case_id']],a,lambda q,b:policy.complete(q),event)
                rows.append(row);rf.write(json.dumps(row)+'\n');rf.flush();os.fsync(rf.fileno())
                emit({'kind':'episode_completed','assignment':a['id']})
        except Exception as e:
            error=type(e).__name__;emit({'kind':'stopped','category':error});raise
        finally:
            summary={'kind':'native','stage':'verification-v1','execution_complete':len(rows)==48,'started':len(started),
                     'incomplete':len(started)-len(rows),'unstarted':48-len(started),'error':error,'api_calls':policy.calls,
                     'actual_usd':policy.actual_usd,'scientific_review':'pending','successor_authorized':False,**i.analyze(rows)}
            (out/'episodes.json').write_text(json.dumps(rows,indent=2)+'\n')
            (out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
    return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--admission',required=True);a=p.parse_args()
    try:execute(a.out,a.admission)
    except Exception as e:print(json.dumps({'stopped':type(e).__name__}));raise SystemExit(1)
