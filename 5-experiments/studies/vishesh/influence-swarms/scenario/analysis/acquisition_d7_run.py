"""Owner-approved D7 manual runner. OpenRouter credential stays in the local bounded relay."""
import argparse,datetime,hashlib,json,os,resource,socket,sqlite3,subprocess,sys,urllib.request
from contextlib import closing
from pathlib import Path
from acquisition_d6 import Session,AcquisitionStopped
from openrouter_d7 import MODEL,PROVIDER,normalize,verify_route
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[4]
PACKET=BASE/'reviews/D7-acquisition-packet.json';PLAN=BASE/'ITERATION-07-ROUTE.md'

def sha(raw):return hashlib.sha256(raw).hexdigest()
def verify_packet(packet):
    assert packet['maximum_transport_attempts']==2 and packet['retries']==0 and packet['stop_on_first_failure'] is True
    assert packet['maximum_total_reservation_usd']==.097280
    assert [r['arm'] for r in packet['requests']]==['matrix_inherited','typed_inherited']
    for item in packet['requests']:
        b=item['wire_body'];wire=json.dumps(b).encode()
        assert len(wire)==item['wire_bytes']<=32768 and sha(wire)==item['wire_sha256']
        assert b['model']==MODEL and b['max_tokens']==3072 and b['temperature']==0
        assert item['maximum_reservation_usd']==.048640
        assert b['messages'][0]=={'role':'system','content':item['request']['instructions']} and json.loads(b['messages'][1]['content'])==item['request']['observation']
        assert b['provider']==PROVIDER and b['reasoning']=={'enabled':False} and b['stream'] is False
    return packet

def prepare(admission_path,out):
    a=json.loads(Path(admission_path).read_text());now=datetime.datetime.now(datetime.timezone.utc)
    assert a['stage']=='D7' and a['attempt']=='native-D7-01' and a['owner_approved'] is True
    assert a['host']==socket.gethostname() and a['exclusive_claim_current'] is True and a['account_resource_matched'] is True and a['workload_idle'] is True
    assert 0<=(now-datetime.datetime.fromisoformat(a['checked_utc'])).total_seconds()<300
    assert datetime.datetime.fromisoformat(a['until'])>now+datetime.timedelta(minutes=5)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==a['source_commit']
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    assert sha(PACKET.read_bytes())==a['packet_sha256']
    p=verify_packet(json.loads(PACKET.read_text()))
    url=f"https://github.com/dmarzzz/swarm-lab/blob/{a['source_commit']}/{PLAN.relative_to(ROOT)}"
    assert a['public_plan']==url
    with urllib.request.urlopen(url.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'),timeout=20) as response:raw=response.read()
    assert raw==PLAN.read_bytes() and sha(raw)==a['plan_sha256']
    out=Path(out);assert not out.exists() and not Path(str(out)+'.start.json').exists()
    rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines()
    assert not [r for r in rows if len(r.split())==2 and r.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(r.split()[0])!=os.getpid()]
    assert not subprocess.check_output(['docker','ps','-q'],text=True).strip()
    with closing(sqlite3.connect('file:'+a['ledger']+'?mode=ro',uri=True)) as db:budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
    assert budget[0]==8 and abs(budget[1]-4.917472)<1e-8 and budget[2]==247 and budget[0]-budget[1]>=.097280
    return a,p,budget

def validator(item):
    import typed_policy as tp
    from candidate_checks import validate_matrix
    def check(result):
        verify_route(result)
        assert isinstance(result['content'],list) and len(result['content'])==1 and result['content'][0]['type']=='text'
        answer=tp.decode_answer(result['content'][0]['text'])
        (tp.validate if item['arm'].startswith('typed') else validate_matrix)(answer,item['request']['observation'])
        return answer
    return check

def collect(packet,out,ledger,transport):
    session=Session(out,ledger);rows=[{'arm':i['arm'],'status':'unstarted'} for i in packet['requests']]
    try:
        for n,item in enumerate(packet['requests']):
            rows[n]['status']='started'
            try:
                answer=session.dispatch(json.dumps(item['wire_body']).encode(),transport,validator(item),.048640,response_adapter=normalize)
                rows[n].update(status='valid',answer=answer)
            except AcquisitionStopped as e:
                rows[n].update(status='failed',category=str(e));break
            except Exception:
                rows[n].update(status='failed',category='local_io_or_runtime');break
    finally:
        events=[json.loads(x) for x in (Path(out)/'events.jsonl').read_text().splitlines()]
        failures=[e for e in events if e['kind']=='failure'];usages=[e for e in events if e['kind']=='usage'];calls=session.count
        total=sum(e['reported_usd'] for e in usages);missing=calls-len(usages)
        summary={'stage':'D7','attempt':'native-D7-01','planned':2,'started':calls,'terminal':sum(r['status'] in ('valid','failed') for r in rows),'valid':sum(r['status']=='valid' for r in rows),'failed':sum(r['status']=='failed' for r in rows),'unstarted':sum(r['status']=='unstarted' for r in rows),'calls':calls,'usage_missing':missing,'observed_usage_cost_usd':total,'actual_usd':None if missing else total,'new_reserved_usd':round(.048640*calls,6),'qualified':False,'failures':failures,'assignments':rows}
        (Path(out)/'summary.json').write_text(json.dumps(summary,indent=2))
    return summary

def main():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.umask(0o077)
    parser=argparse.ArgumentParser();parser.add_argument('--admission',required=True);parser.add_argument('--out',required=True);parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
    a,p,budget=prepare(args.admission,args.out)
    if args.check_only:print(json.dumps({'ready':True,'model_calls':0,'budget':budget}));return
    sys.path[:0]=[str(ROOT/'tooling/agent-experiments'),'/usr/local/lib/swarm']
    import swarm_report as sr
    # Publish plan + both condition-specific TLDRs before creating the model session.
    sr.register('influence-swarms',title='How to win agents and influence swarms',owner='vishesh',url=a['public_plan'],description='D7 OpenRouter acquisition diagnostic: can matrix then typed reviewer contracts return valid responses? At most two calls, no retries, stop on first failure. One inspected case, no behavior-effect claim.',params={'stage':{'type':'str'},'version':{'type':'str'}},metrics=['valid','failed','unstarted'],primary_metric='valid')
    with Path(str(args.out)+'.start.json').open('x') as f:json.dump({'stage':'D7','source_commit':a['source_commit'],'packet_sha256':a['packet_sha256'],'plan':a['public_plan'],'budget_before':budget},f)
    # Dedicated SSH-forwarded loopback relay holds the credential locally.
    endpoint='http://127.0.0.1:18767/'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def transport(raw):
        req=urllib.request.Request(endpoint,data=raw,headers={'Content-Type':'application/json'})
        with opener.open(req,timeout=75) as response:return response.read(1_000_001)
    with sr.start('influence-swarms',params={'stage':'D7','version':a['source_commit'][:12],'plan':a['public_plan'],'matrix_tldr':'First contract: matrix reviewer acquisition on frozen regional case; valid output and usage or stop. No behavioral effect estimate.','typed_tldr':'Second contract: typed reviewer acquisition, only if matrix succeeds; valid output and usage or stop. Same case, no causal effect estimate.'}) as hub:
        visible=json.loads(subprocess.check_output(['curl','--fail','--silent','--show-error','--max-time','25','https://swarm-live.pages.dev/api/runs/'+hub.id]))
        assert visible['params']['plan']==a['public_plan'] and visible['params']['stage']=='D7'
        assert visible['params']['matrix_tldr'] and visible['params']['typed_tldr']
        summary=collect(p,args.out,a['ledger'],transport)
        summary.update(run=hub.id,source_commit=a['source_commit'],packet_sha256=a['packet_sha256'],public_plan=a['public_plan'])
        (Path(args.out)/'summary.json').write_text(json.dumps(summary,indent=2))
        for file in Path(args.out).iterdir():hub.artifact(file,file.name)
        (hub.done if summary['valid']==2 else hub.fail)(message='D7 acquisition only; no automatic follow-up',valid=summary['valid'],failed=summary['failed'],unstarted=summary['unstarted'])
        print(json.dumps({k:summary[k] for k in ('run','started','valid','failed','unstarted','actual_usd','usage_missing','failures')}))

if __name__=='__main__':
    try:main()
    except Exception as exc:print(json.dumps({'stopped':True,'error_type':type(exc).__name__}));raise SystemExit(1)
