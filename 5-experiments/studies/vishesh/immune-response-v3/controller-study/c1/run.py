"""Finite C1 packet executor. Native runs fail closed without current admission."""
import argparse,copy,datetime,hashlib,importlib.util,json,os,socket,sqlite3,subprocess,sys
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent))
import cases,public_reference,controller
spec=importlib.util.spec_from_file_location('c1_candidate',BASE.parent/'next-contract/candidate.py');candidate=importlib.util.module_from_spec(spec);spec.loader.exec_module(candidate)
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def assignments():
    return [{'case_id':c['id'],'order':order} for i,c in enumerate(cases.development()) for order in (('action_first','justification_first') if i%2==0 else ('justification_first','action_first'))]
def verify_admission(receipt):
    r=json.loads(Path(receipt).read_text());now=datetime.datetime.now(datetime.timezone.utc)
    assert r['stage']=='controller-c1' and r['funded'] is True and r['pi_decision_reference']
    assert r['commit']==subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
    assert not subprocess.check_output(['git','diff','--name-only','HEAD'],cwd=BASE).strip()
    assert r['packet_sha256']==sha(BASE/'packet.json') and r['plan_sha256']==sha(BASE/'PLAN.md')
    assert r['max_calls']==32 and r['model_max_usd']==1.771520 and r['all_in_max_usd']==1.921520
    assert 0<=r['infrastructure_reserved_usd']<=.15 and r['infrastructure_centrally_reconciled'] is True
    a=r['allocation'];assert a['host']==socket.gethostname() and a['exclusive'] and a['approved_account_verified'] and a['claim_reference']
    assert datetime.datetime.fromisoformat(a['expires'].replace('Z','+00:00'))-now>datetime.timedelta(minutes=65)
    assert r['public_plan_verified'] is True and r['remote_tests_passed'] is True
    sys.path.insert(0,str(BASE.parent.parent.parent/'experiment-documentation'))
    from public_plan import check
    public=check('immune-response-v3','C1: four paired development roots, action-first versus observable justification-first; fixed outcomes and diagnosis,32calls, no hidden-reasoning or population claim.')
    assert public['commit']==r['commit'] and public['plan_sha256']==r['plan_sha256']
    assert sha(os.environ['SWARM_BUDGET_LEDGER'])==r['ledger_sha256']
    with sqlite3.connect('file:'+os.environ['SWARM_BUDGET_LEDGER']+'?mode=ro',uri=True) as db:
        cap,reserved,calls=db.execute('select cap,reserved,calls from budget').fetchone()
        assert cap==8 and reserved+1.771520<=cap and calls==485
        assert db.execute('pragma integrity_check').fetchone()[0]=='ok'
    return r

def execute(out,backend='scripted',admission=None,policy=None):
    packet=json.loads((BASE/'packet.json').read_text());assert packet['assignments']==assignments()
    for rel,digest in packet['source_sha256'].items():assert sha(BASE.parent/rel)==digest,rel
    receipt=verify_admission(admission) if backend=='openrouter' else None
    out=Path(out);out.mkdir(parents=True,exist_ok=False)
    if receipt:
        (out/'admission.json').write_text(json.dumps(receipt,indent=2))
        os.environ.update(SWARM_USAGE_LOG=str(out/'usage.jsonl'),SWARM_MODEL_CONFIG_FILE=str(BASE.parent/'opus-config.json'))
        # Import explicitly: parent simulator imports alter sys.path.
        ns=importlib.util.spec_from_file_location('c1_native',BASE/'native.py');native=importlib.util.module_from_spec(ns);ns.loader.exec_module(native);policy=native.Policy()
    manifest={'stage':'controller-c1','runtime_commit':subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip(),'backend':backend,'packet_sha256':sha(BASE/'packet.json'),'assignments':packet['assignments'],'max_calls':32}
    (out/'manifest.json').write_text(json.dumps(manifest,indent=2));roots={c['id']:c for c in cases.development()};rows=[];started=0;complete=False;error=None
    with (out/'events.jsonl').open('x') as ef,(out/'episodes.jsonl').open('x') as rf:
        def emit(e):ef.write(json.dumps(e)+'\n');ef.flush();os.fsync(ef.fileno())
        try:
            for assignment in packet['assignments']:
                started+=1;c=roots[assignment['case_id']];state=copy.deepcopy(c['initial']);trace=[];history=[];emit({'kind':'episode_started',**assignment})
                for tick in (1,2):
                    o=cases.observe(c,state,tick,history,[]);q=candidate.diagnosis_request(o)
                    d=policy.complete(q,None) if policy else public_reference.labels(o);emit({'kind':'diagnosis_response',**assignment,'tick':tick,'request':q,'response':d});controller.validate_diagnosis(o,d)
                    q=candidate.action_request(c,o,d,assignment['order'])
                    if policy:a=policy.complete(q,None)
                    else:
                        a=public_reference.choose(o);a={k:a[k] for k in q['response_schema']['required']}
                    emit({'kind':'action_response',**assignment,'tick':tick,'request':q,'response':a,'observed_key_order':list(a)})
                    if list(a)!=q['response_schema']['required']:raise ValueError('ordering_manipulation_failed')
                    decoded=cases.f.controller.decode(c['fixture'],a);x=cases.f.step(c['fixture'],state,decoded);x.update(tick=tick,observation=o,diagnosis=d,diagnosis_correct=d==public_reference.labels(o),raw_response=a,observed_key_order=list(a));trace.append(x);history.append({'action':decoded,'result':x['result']});emit({'kind':'frame',**assignment,**x})
                row={**assignment,'model':'opus','split':'development','condition':assignment['order'],'case':c,'trace':trace,'outcome_pass':cases.gate(c,trace),'diagnosis_pass':all(x['diagnosis_correct'] for x in trace)};row['qualified']=row['outcome_pass'] and row['diagnosis_pass'];rows.append(row);rf.write(json.dumps(row)+'\n');rf.flush();os.fsync(rf.fileno());print(json.dumps({'recorded':len(rows),'assigned':8}),flush=True)
            complete=True
        except Exception as e:
            error=str(e) if str(e)=='ordering_manipulation_failed' else type(e).__name__;emit({'kind':'stopped','category':error});raise
        finally:
            summary={'stage':'controller-c1','backend':backend,'execution_complete':complete,'assigned':8,'started':started,'recorded':len(rows),'unstarted':8-started,'incomplete':started-len(rows),'error':error,'api_calls':policy.calls if policy else 0,'actual_usd':policy.actual_usd if policy else 0,'manual_consistency_review':'pending' if backend=='openrouter' else 'not_native','successor_authorized':False,'cells':[{k:v for k,v in r.items() if k not in ('case','trace')} for r in rows]}
            (out/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--out',required=True);p.add_argument('--backend',choices=['scripted','openrouter'],required=True);p.add_argument('--admission');a=p.parse_args()
    try:execute(a.out,a.backend,a.admission)
    except Exception as e:print(json.dumps({'stopped':type(e).__name__}),flush=True);raise SystemExit(1)
