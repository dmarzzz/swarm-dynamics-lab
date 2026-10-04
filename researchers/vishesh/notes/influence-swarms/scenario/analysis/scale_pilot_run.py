"""Scale model/role qualification runner; no automatic successor or retry."""
import time,tarfile
import argparse,datetime,hashlib,json,os,re,resource,socket,sqlite3,subprocess,sys,urllib.request
from contextlib import closing
from pathlib import Path
from scale_acquisition import Session,AcquisitionStopped
from openrouter_d7 import MODEL,PROVIDER,normalize,verify_route
from output_contract_d8 import JSON_ONLY
from readiness_contract import verify_item
from openrouter_errors import safe_relay_error
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[4]
PACKET=None;PLAN=BASE/'scale-up/PILOT.md'
from scale_pilot import Protocol,manifest,assessment,encode,CONFIGS
from scale_qualification import MODELS as ROLE_MODELS
MODELS=CONFIGS
def build(stage):
    p=manifest(stage);floor={"SP-SOL":(6.5593024,297),"SP-LUNA":(7.6846784,333)}[stage]
    p.update(expected_budget={"cap":8,"reserved":floor[0],"calls":floor[1]},launch_enabled=True,requests=[])
    return p

def sha(raw):return hashlib.sha256(raw).hexdigest()
def verify_packet(packet):
    assert packet==build(packet['stage']),'packet_source_mismatch'
    for stage in ('SD-SOL','SD-LUNA3'):
        receipt=json.loads((BASE/f'reviews/native-{stage}-01/assessment.json').read_text());assert receipt['qualified'] is True and len(receipt['rows'])==3
    for stage in ('SQ-SOL','SQ-LUNA'):
        receipt=json.loads((BASE/f'reviews/native-{stage}-01/assessment.json').read_text());assert len(receipt['rows'])==9 and all(r['status']=='valid' for r in receipt['rows']);aud=[r for r in receipt['rows'] if r['role']=='auditor'];assert len(aud)==3 and all(r['passes'] for r in aud)
    return packet

def prepare(admission_path,out):
    global PACKET
    a=json.loads(Path(admission_path).read_text());PACKET=BASE/a['packet_relative']
    assert PACKET.resolve().is_relative_to((BASE/'reviews').resolve()) and PACKET.suffix=='.json'
    now=datetime.datetime.now(datetime.timezone.utc)
    assert a['stage'] in MODELS and a['attempt']=='native-'+a['stage']+'-01' and a['owner_approved'] is True
    assert a['host']==socket.gethostname() and a['exclusive_claim_current'] is True and a['account_resource_matched'] is True and a['workload_idle'] is True
    assert 0<=(now-datetime.datetime.fromisoformat(a['checked_utc'])).total_seconds()<300
    assert datetime.datetime.fromisoformat(a['until'])>now+datetime.timedelta(minutes=5)
    assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()==a['source_commit']
    assert not subprocess.check_output(['git','status','--porcelain','--untracked-files=no'],cwd=ROOT,text=True).strip()
    assert sha(PACKET.read_bytes())==a['packet_sha256']
    p=verify_packet(json.loads(PACKET.read_text()));assert p['stage']==a['stage']
    url=f"https://github.com/dmarzzz/swarm-lab/blob/{a['source_commit']}/{PLAN.relative_to(ROOT)}"
    assert a['public_plan']==url
    with urllib.request.urlopen(url.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/'),timeout=20) as response:raw=response.read()
    assert raw==PLAN.read_bytes() and sha(raw)==a['plan_sha256']
    out=Path(out);assert not out.exists() and not Path(str(out)+'.start.json').exists()
    rows=subprocess.check_output(['ps','-eo','pid=,comm='],text=True).splitlines()
    assert not [r for r in rows if len(r.split())==2 and r.split()[1].startswith(('python','node','uvicorn','gunicorn')) and int(r.split()[0])!=os.getpid()]
    assert not subprocess.check_output(['docker','ps','-q'],text=True).strip()
    with closing(sqlite3.connect('file:'+a['ledger']+'?mode=ro',uri=True)) as db:budget=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
    expected=p['expected_budget'];assert budget[0]==8 and abs(budget[1]-expected['reserved'])<1e-8 and budget[2]==expected['calls']
    assert budget[1]>=5.501152-1e-9 and budget[2]>=259 and budget[2]+p['maximum_transport_attempts']<=529
    assert budget[1]+p['maximum_total_reservation_usd']<=7.9603392+1e-9
    return a,p,budget


def collect(packet,out,ledger,transport,until,hub=None):
    protocol=Protocol(packet['stage']);session=Session(out,ledger,maximum_requests=packet['maximum_transport_attempts'],reserved_ceiling=7.9603392,calls_ceiling=529,http_error_adapter=safe_relay_error);rows=[];started=time.monotonic();failure=None
    try:
        while not protocol.complete:
            if time.monotonic()-started>2700 or datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=90)>datetime.datetime.fromisoformat(until):raise AcquisitionStopped('deadline_or_allocation')
            item=protocol.next();before=time.monotonic();q=CONFIGS[packet['stage']][0];model,ir,orr=ROLE_MODELS[q]
            answer=session.dispatch(encode(item['wire_body']),transport,lambda r:protocol.check(item,r),item['maximum_reservation_usd'],input_rate=ir,output_rate=orr,response_adapter=normalize)
            protocol.accept(item,answer);rows.append({**protocol.records[-1],'elapsed_seconds':time.monotonic()-before,'wire_bytes':item['wire_bytes'],'reserved_usd':item['maximum_reservation_usd']})
            with (Path(out)/'protocol.jsonl').open('a') as f:f.write(json.dumps(rows[-1])+'\n');f.flush();os.fsync(f.fileno())
            if hub and (session.count%10==0 or protocol.complete):hub.progress(session.count,packet['maximum_transport_attempts'],valid=len(rows))
    except Exception as e:failure=str(e) if isinstance(e,AcquisitionStopped) else type(e).__name__
    finally:
        events=[json.loads(x) for x in (Path(out)/'events.jsonl').read_text().splitlines()];usages=[e for e in events if e['kind']=='usage'];missing=session.count-len(usages);reserved=sum(e['reserved_usd'] for e in events if e['kind']=='attempt_start');cost=sum(e['reported_usd'] for e in usages)
        summary={'stage':packet['stage'],'attempt':'native-'+packet['stage']+'-01','planned':packet['maximum_transport_attempts'],'calls':session.count,'valid':len(rows),'failed':int(failure is not None),'unstarted':packet['maximum_transport_attempts']-session.count,'complete':protocol.complete,'failure':failure,'usage_missing':missing,'actual_usd':None if missing else cost,'observed_usage_cost_usd':cost,'new_reserved_usd':reserved,'elapsed_seconds':time.monotonic()-started,'team_size':packet['team_size'],'independent_worlds':1}
        (Path(out)/'summary.json').write_text(json.dumps(summary,indent=2));(Path(out)/'assessment.json').write_text(json.dumps(assessment(protocol),indent=2))
    return summary

def main():
    resource.setrlimit(resource.RLIMIT_CORE,(0,0));os.umask(0o077)
    parser=argparse.ArgumentParser();parser.add_argument('--admission',required=True);parser.add_argument('--out',required=True);parser.add_argument('--check-only',action='store_true');args=parser.parse_args()
    a,p,budget=prepare(args.admission,args.out)
    if args.check_only:print(json.dumps({'ready':True,'model_calls':0,'budget':budget}));return
    sys.path[:0]=[str(ROOT/'tooling/agent-experiments'),'/usr/local/lib/swarm']
    import swarm_report as sr
    # Publish plan + both condition-specific TLDRs before creating the model session.
    sr.register('influence-swarms',title='How to win agents and influence swarms',owner='vishesh',url=a['public_plan'],description=p['tldr'],params={'stage':{'type':'str'},'version':{'type':'str'}},metrics=['valid','failed','unstarted'],primary_metric='valid')
    with Path(str(args.out)+'.start.json').open('x') as f:json.dump({'stage':p['stage'],'source_commit':a['source_commit'],'packet_sha256':a['packet_sha256'],'plan':a['public_plan'],'budget_before':budget},f)
    # Dedicated SSH-forwarded loopback relay holds the credential locally.
    endpoint='http://127.0.0.1:18779/'
    opener=urllib.request.build_opener(urllib.request.ProxyHandler({}))
    def transport(raw):
        req=urllib.request.Request(endpoint,data=raw,headers={'Content-Type':'application/json'})
        with opener.open(req,timeout=75) as response:return response.read(1_000_001)
    params={'stage':p['stage'],'version':a['source_commit'][:12],'plan':a['public_plan'],'conditions':[{'case_id':p['case_spec']['id'],'condition':w,'tldr':p['tldr']+' Condition:'+w+'. Same primary records and fixed two-neighbor graph; fresh role states.'} for w in p['conditions']]}
    with sr.start('influence-swarms',params=params) as hub:
        visible=json.loads(subprocess.check_output(['curl','--fail','--silent','--show-error','--max-time','25','https://swarm-live.pages.dev/api/runs/'+hub.id]))
        assert visible['params']['plan']==a['public_plan'] and visible['params']['stage']==p['stage']
        assert visible['params']['conditions']==params['conditions']
        summary=collect(p,args.out,a['ledger'],transport,a['until'],hub)
        summary.update(run=hub.id,source_commit=a['source_commit'],packet_sha256=a['packet_sha256'],public_plan=a['public_plan'])
        (Path(args.out)/'summary.json').write_text(json.dumps(summary,indent=2))
        with tarfile.open(Path(args.out)/'raw-records.tar.gz','w:gz') as archive:
            for file in Path(args.out).glob('*.bin'):archive.add(file,arcname=file.name)
        for name in ('summary.json','assessment.json','events.jsonl','protocol.jsonl','raw-records.tar.gz'):
            file=Path(args.out)/name
            if file.exists():hub.artifact(file,file.name)
        (hub.done if summary['complete'] else hub.fail)(message='Bounded diagnostic; no automatic successor',valid=summary['valid'],failed=summary['failed'],unstarted=summary['unstarted'])
        print(json.dumps({k:summary[k] for k in ('run','calls','valid','failed','unstarted','actual_usd','usage_missing','failure')}))

if __name__=='__main__':
    try:main()
    except Exception as exc:print(json.dumps({'stopped':True,'error_type':type(exc).__name__}));raise SystemExit(1)
