"""A1 manual native contract: orbital queue admission required; no resume or retries."""
import argparse,hashlib,json,os,resource,socket,sqlite3,subprocess,sys,time,urllib.request,urllib.error
from pathlib import Path
from design import ROOT,EXPERIMENT,MODEL,assignments,source_hash,digest,check,execution_request
from admission import validate,public_check,GateError
from scoring import policy_score
from analyze import summarize
from provider_diagnostics import http_failure
ALLOCATION_LEDGER=Path('/srv/swarm/theseus-execution-allocations.sqlite')

def write_new(path,value):
    with Path(path).open('x') as f:json.dump(value,f,sort_keys=True);f.flush();os.fsync(f.fileno())
def reserve(ledger,cost,now):
    with sqlite3.connect(ledger,timeout=30) as db:
        db.execute('BEGIN IMMEDIATE');cap,used,calls,deadline=db.execute('SELECT cap,used,calls,deadline FROM budget WHERE id=1').fetchone()
        if cap!=2.5 or calls>=204 or used+cost>cap or now>=deadline:raise GateError('budget_or_deadline')
        db.execute('UPDATE budget SET used=?,calls=? WHERE id=1',(used+cost,calls+1))
    return calls+1

def invoke(body,key,timeout):
    headers={'Content-Type':'application/json','x-api-key':key,'anthropic-version':'2023-06-01','anthropic-workspace-id':os.environ['SWARM_MODEL_WORKSPACE_ID']}
    req=urllib.request.Request('https://api.anthropic.com/v1/messages',data=json.dumps(body).encode(),headers=headers)
    result={'value':None,'raw_text':None,'error':None,'actual_usd':None,'usage':None,'response_received':False,'started_epoch':time.time()}
    try:
        with urllib.request.urlopen(req,timeout=timeout) as response:raw=response.read(1_000_001)
        if len(raw)>1_000_000:raise GateError('response_bound')
        data=json.loads(raw);result['response_received']=True;result['served_model']=data.get('model');u=data.get('usage',{})
        result['raw_text']=''.join(x['text'] for x in data.get('content',[]) if x.get('type')=='text')
        if all(type(u.get(k)) is int for k in ('input_tokens','output_tokens')):
            result['usage']={k:u[k] for k in ('input_tokens','output_tokens')};result['actual_usd']=(u['input_tokens']+5*u['output_tokens'])/1e6
        result['stop_reason']=data.get('stop_reason') if data.get('stop_reason') in ('end_turn','max_tokens','refusal') else 'other'
        if result['stop_reason']!='end_turn':result['error']='incomplete_output'
        else:
            try:result['value']=json.loads(result['raw_text'])
            except (ValueError,TypeError):result['value']=None # contract failure, not a hidden retry/transport error
        if result.get('served_model')!=MODEL:result['error']='served_model_mismatch'
        if result['usage'] is None:result['error']='usage_missing'
    except urllib.error.HTTPError as e:
        result.update(http_failure(e,time.time()))
        result['error']='http_'+str(result['http_status'])
        e.close()
    except Exception as e:result['error']='provider_'+type(e).__name__
    result['finished_epoch']=time.time();return result

def prepare(output):
    p=Path(output);p.mkdir();design=assignments();checks=check();rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    write_new(p/'assignments.json',{'status':'prepared_not_run','assignments':design,'assignments_sha256':digest(design),'instrument_sha256':source_hash(),'source_commit':rev})
    sha=hashlib.sha256((ROOT/'A1-PLAN.md').read_bytes()).hexdigest()
    receipt={'status':'blocked','experiment':EXPERIMENT,'source_commit':rev,'instrument_sha256':source_hash(),'assignments_sha256':digest(design),'model':MODEL,'max_calls':204,'cap_usd':2.5,'max_seconds':7200,'workers':1,'retries':0,'input_rate':1,'output_rate':5,'prior_spend_usd':.8122310437,'total_authority_usd':5,'infrastructure_hold_usd':.1,'allocation_reserved_usd':2.6,'update_approval_sha256':sha,'plan_sha256':sha,'plan_url':'https://github.com/dmarzzz/swarm-lab/blob/'+rev+'/researchers/vishesh/notes/swarm-of-theseus/execution-diagnostic/A1-PLAN.md','research_review_status':'not-required-owner-direction','authority_allocation_id':'theseus-a1-7300-7305-v1'}
    write_new(p/'admission-template.json',receipt);write_new(p/'checks.json',checks)
    print(json.dumps({'status':'prepared_not_run','calls':204,'admission':'blocked'}))

def run(receipt_path,output):
    receipt=json.loads(Path(receipt_path).read_text());design=assignments();check();root=Path(output).resolve()
    repo=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=ROOT,text=True).strip());rev=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
    if root==repo or repo in root.parents or root.exists():raise GateError('fresh_external_output_required')
    if subprocess.check_output(['git','status','--porcelain'],cwd=ROOT,text=True).strip():raise GateError('clean_source_required')
    validate(receipt,rev,design)
    if socket.gethostname().split('.')[0]!=receipt['host']:raise GateError('runtime_host_mismatch')
    pub=public_check(receipt)
    if receipt.get('status')!='diagnostic-only':raise GateError('operator_not_admitted')
    if not ALLOCATION_LEDGER.exists():raise GateError('original_allocation_ledger_missing')
    if not os.environ.get('SWARM_MODEL_API_KEY') or not os.environ.get('SWARM_MODEL_WORKSPACE_ID'):raise GateError('authorized_credential_or_route_missing')
    resource.setrlimit(resource.RLIMIT_CORE,(0,0));key=os.environ['SWARM_MODEL_API_KEY']
    sys.path.insert(0,'/usr/local/lib/swarm');import swarm_report as sr
    # The queue operator reconciles/retire-transfers the original ledger, never creates a new authority.
    with sqlite3.connect(ALLOCATION_LEDGER,timeout=30) as db:
        db.execute('BEGIN IMMEDIATE')
        db.execute('INSERT INTO allocations VALUES (?,?,?)',(receipt['authority_allocation_id'],str(root),digest(design)))
    root.mkdir();(root/'calls').mkdir();(root/'outcomes').mkdir();deadline=min(time.time()+7200,receipt['claim_until_epoch']);ledger=root/'quota.sqlite'
    with sqlite3.connect(ledger) as db:
        db.execute('CREATE TABLE budget (id INTEGER PRIMARY KEY,cap REAL,used REAL,calls INTEGER,deadline REAL)');db.execute('INSERT INTO budget VALUES (1,2.5,0,0,?)',(deadline,))
    write_new(root/'manifest.json',{'evidence_type':'measured_model_outputs','assignments':design,'source_commit':rev,'instrument_sha256':source_hash(),'admission':receipt,'public_preflight':pub})
    policies={};stop=None;pending=set()
    def report(kind,a,**kw):
        if not sr.report(kind,EXPERIMENT,a['id'],source='vishesh/codex-theseus',strict=True,**kw):raise GateError('report_not_acknowledged')
    try:
        for a in design:
            if a['kind']=='execute' and a['arm']=='learned' and policies[a['parent']]['mapping'] is None:
                write_new(root/'outcomes'/(a['id']+'.json'),{'status':'dependency_invalid','assigned':True});continue
            mapping=None if a['kind']=='learn' else a['rule'] if a['arm']=='ceiling' else policies[a['parent']]['mapping']
            body=a['request'] if a['kind']=='learn' else execution_request(a,mapping);encoded=json.dumps(body).encode()
            if len(encoded)>(8000 if a['kind']=='learn' else 2500):raise GateError('input_bound')
            if time.time()>=deadline:raise GateError('deadline_or_claim_expired')
            report('plan',a,message=a['tldr'],url=receipt['plan_url'],params={'arm':a['arm'],'seed':a['seed'],'context':a['context'],'tldr':a['tldr']});report('start',a,message=a['tldr']);pending.add(a['id'])
            cost=(len(encoded)+512+6000)/1e6;call=reserve(ledger,cost,time.time())
            write_new(root/'calls'/(a['id']+'-started.json'),{'request':body,'request_sha256':digest(body),'checkpoint_sha256':digest(mapping),'reserved_usd':cost,'call':call,'started_epoch':time.time()})
            result=invoke(body,key,max(.1,min(45,deadline-time.time())));write_new(root/'calls'/(a['id']+'-finished.json'),result)
            if a['kind']=='learn':policies[a['id']]=policy_score(a,result)
            write_new(root/'outcomes'/(a['id']+'.json'),{'status':'provider_failed' if result['error'] else 'complete'})
            report('progress',a,message=a['tldr'],metrics={'completed_calls':call});report('fail' if result['error'] else 'done',a,message=a['tldr']);pending.discard(a['id'])
            if result['error']:raise GateError('provider_or_accounting_stop')
            if result['actual_usd']>cost:raise GateError('actual_exceeds_reservation')
    except Exception as e:stop=type(e).__name__
    finally:
        failures=[]
        for a in design:
            p=root/'outcomes'/(a['id']+'.json')
            if not p.exists():write_new(p,{'status':'not_completed','assigned':True})
            if a['id'] in pending:
                try:report('fail',a,message=a['tldr']+' Stopped; retained evidence, no retry.')
                except Exception:failures.append(a['id'])
        analysis_error=None
        try:summarize(root)
        except Exception as e:analysis_error=type(e).__name__
        write_new(root/'terminal.json',{'status':'stopped' if stop else 'complete','safe_error_class':stop,'reporting_pending':failures,'analysis_error_class':analysis_error,'retries':0})
        write_new(root/'handoff.json',{'status':'scientific_review_required','attempt':'A1','evidence':'manifest.json, calls/, summary.json, terminal.json','next_action':'Run shared offline finalize hook and complete scientific assessment; retain original ledger, upload/readback, release claim. No successor dispatch.'})
    print(json.dumps({'status':'stopped' if stop else 'complete','scientific_review':'required'}))

if __name__=='__main__':
    p=argparse.ArgumentParser();s=p.add_subparsers(dest='mode',required=True);a=s.add_parser('prepare');a.add_argument('output');b=s.add_parser('run');b.add_argument('--admission',required=True);b.add_argument('--output',required=True);c=s.add_parser('analyze');c.add_argument('output');args=p.parse_args()
    try:
        if args.mode=='prepare':prepare(args.output)
        elif args.mode=='run':run(args.admission,args.output)
        else:print(json.dumps(summarize(args.output)))
    except Exception as e:print(json.dumps({'status':'blocked','safe_error_class':type(e).__name__,'safe_reason':str(e) if isinstance(e,GateError) else 'inspect_nonsecret_operator_state'}));sys.exit(1)
