"""RD6 manual native entrypoint. No launch without explicit bound admission.

All provider access lives in the local relay; workers only see the frozen actor
request. Offline tests inject transports and synthetic ledgers, never credentials.
"""
import argparse
from contextlib import contextmanager
import datetime as dt
import hashlib
from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import math
import os
from pathlib import Path
import signal
import subprocess
import sys
import tempfile
import time
import urllib.request
import urllib.error
from cases import digest
from native_gates import (BASE, ROOT, SNAPSHOT, RESERVE, prepare, validate_packet, validate_admission,
                          live_preflight, evidence, instant, read, require, wire)
from native_budget import Ledger, snapshot
from native_report import Events, save, finish_bundle, audit_bundle

PORT = 18469
RELAY = 'http://127.0.0.1:'+str(PORT)


@contextmanager
def deadline(seconds):
    """Wall-clock bound, including a server trickling bytes; Unix main thread only."""
    previous = signal.getsignal(signal.SIGALRM)
    def expired(*args): raise TimeoutError('request_deadline')
    signal.signal(signal.SIGALRM, expired)
    signal.setitimer(signal.ITIMER_REAL, seconds)
    try: yield
    finally:
        signal.setitimer(signal.ITIMER_REAL, 0)
        signal.signal(signal.SIGALRM, previous)


class DispatchFailure(ValueError):
    def __init__(self, status='failed', settled_nano=None):
        super().__init__('relay_stopped')
        self.status = status
        self.settled_nano = settled_nano


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,*args,**kwargs):
        raise ValueError('redirect_refused')


class Provider:
    def __init__(self, credential):
        self.opener = urllib.request.build_opener(NoRedirect())
        self.route_at = None
        self.route()
        credential = Path(credential)
        require(credential.is_file() and not credential.is_symlink()
                and not credential.stat().st_mode & 0o077, 'credential_permissions')
        self.secret = credential.read_text().strip()
        require(bool(self.secret), 'empty_credential')

    def route(self):
        if self.route_at is not None and time.monotonic()-self.route_at < 240: return
        with self.opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=15) as r:
            routes=json.loads(r.read(200000))['data']['endpoints']
        require(len(routes)==1, 'route_count')
        r=routes[0]
        prompt=float(r['pricing']['prompt']); completion=float(r['pricing']['completion'])
        require(r['provider_name']=='TypeSafe' and r['tag']=='typesafe' and r['status']==0
                and SNAPSHOT in r['name'] and math.isfinite(prompt) and 0 <= prompt <= 0.000000042
                and completion==0 and type(r['context_length']) is int and 0 < r['context_length'] <= 32000,
                'route_mismatch')
        self.route_at=time.monotonic()

    def send(self, data):
        # Exactly the ordered frozen bytes; no chat history, auto-retry or fallback.
        req=urllib.request.Request('https://openrouter.ai/api/alpha/decisions',data,
            {'Content-Type':'application/json','Authorization':'Bearer '+self.secret})
        with self.opener.open(req,timeout=40) as r:
            raw=r.read(200001)
        require(len(raw)<=200000, 'response_size')
        return json.loads(raw)


class RelayEngine:
    def __init__(self, packet, receipt, ledger, provider, directory, *, now=None, monotonic=None):
        self.packet, self.receipt, self.ledger, self.provider = packet,receipt,ledger,provider
        self.now = now or (lambda: dt.datetime.now(dt.timezone.utc))
        self.monotonic = monotonic or time.monotonic
        self.started=self.monotonic(); self.stopped=False; self.index=0
        self.out=Path(directory); self.out.mkdir(parents=True,exist_ok=False)
        self.events=Events(self.out/'relay-events.jsonl')
        self.events.add('relay_start',packet_sha256=digest(packet),stage=packet['stage'])
        try: self.ledger.begin(packet,receipt['attempt'],
            evidence(receipt['zero_dispatch_replacement']) if 'zero_dispatch_replacement' in receipt else None)
        except BaseException:
            self.events.close(); raise

    def healthy(self):
        return (not self.stopped and self.monotonic()-self.started < 1800
                and self.now()+dt.timedelta(seconds=60) <= instant(self.receipt['expires_utc']))

    def stop(self):
        if not self.stopped:
            self.stopped=True
            self.ledger.finish(self.packet['stage'],'completed' if self.index==len(self.packet['assignments']) else 'stopped')
            self.events.add('relay_stop',completed=self.index,budget=snapshot(self.ledger.db))

    def handle(self, body):
        key=None
        try:
            require(self.healthy(), 'lease_or_runtime_expired')
            require(set(body)=={'id','request','ordered_request_sha256'}, 'relay_shape')
            require(self.index < len(self.packet['assignments']), 'stage_complete')
            a=self.packet['assignments'][self.index]
            require(body['id']==a['id'] and body['ordered_request_sha256']==a['ordered_request_sha256']
                    and wire(body['request'])==wire(a['request']), 'unfrozen_or_duplicate_request')
            self.provider.route()  # metadata only, before reservation
            require(self.healthy(), 'lease_or_runtime_expired')
            key=self.ledger.reserve(self.packet,a)
            self.events.add('reservation',id=a['id'],reserved_nano=RESERVE,
                            ordered_request_sha256=a['ordered_request_sha256'])
            started=self.monotonic()
            with deadline(60):
                response=self.provider.send(wire(a['request']))
            checked=self.ledger.settle(key,response,a['request'])
            elapsed=self.monotonic()-started
            require(elapsed <= 60, 'request_timeout')
            self.events.add('response',id=a['id'],result=checked,latency_seconds=elapsed)
            self.index+=1
            return dict(checked,id=a['id'],ordered_request_sha256=a['ordered_request_sha256'],
                        latency_seconds=elapsed,reservation='settled')
        except Exception:
            self.stop()
            # Every provider or arbitrary exception is replaced, never echoed.
            self.events.add('failure',reservation_exists=key is not None)
            row = self.ledger.db.execute('SELECT status,actual_nano FROM calls WHERE key=?',(key,)).fetchone() if key else None
            raise DispatchFailure('invalid' if row and row[0]=='invalid_response' else 'failed', row[1] if row else None) from None

    def close(self):
        try:
            self.stop()
            save(self.out/'accounting.json',self.ledger.accounting(self.packet))
        finally:
            self.events.close(); self.ledger.close()


class Transport:
    def __init__(self, packet):
        self.packet=packet; self.opener=urllib.request.build_opener(NoRedirect())

    def health(self):
        with self.opener.open(RELAY+'/health',timeout=3) as r:
            data=json.load(r)
        require(data=={'ready':True,'packet_sha256':digest(self.packet)}, 'relay_not_ready')

    def send(self, a):
        body={'id':a['id'],'request':a['request'],'ordered_request_sha256':a['ordered_request_sha256']}
        req=urllib.request.Request(RELAY+'/decision',wire(body),{'Content-Type':'application/json'})
        try:
            with deadline(60):
                with self.opener.open(req,timeout=60) as r:
                    raw=r.read(200001)
        except urllib.error.HTTPError as error:
            try: detail=json.loads(error.read(4096))
            except Exception: detail={}
            status='invalid' if detail.get('status')=='invalid' else 'failed'
            nano=detail.get('settled_nano')
            raise DispatchFailure(status,nano if type(nano) is int and nano >= 0 else None) from None
        require(len(raw)<=200000,'response_size')
        return json.loads(raw)


def run_worker(packet, receipt, out, transport, *, mode='native', monotonic=None, now=None):
    """Transport-injected worker. Production caller must pass live_preflight first."""
    clock=monotonic or time.monotonic
    utc=now or (lambda:dt.datetime.now(dt.timezone.utc))
    out=Path(out); out.mkdir(parents=True,exist_ok=False)
    save(out/'packet.json',packet)
    rows=[{'id':a['id'],'request_sha256':a['request_sha256'],
           'ordered_request_sha256':a['ordered_request_sha256'],'status':'unstarted','action':None,
           'reservation':'none'} for a in packet['assignments']]
    save(out/'outcomes.json',rows)
    events=Events(out/'events.jsonl'); events.add('assignment',packet_sha256=digest(packet),assigned=len(rows))
    started=clock(); failure=False
    from native_budget import validate
    try:
        for a,row in zip(packet['assignments'],rows):
            try:
                require(clock()-started < 1800 and utc()+dt.timedelta(seconds=60) <= instant(receipt['expires_utc']), 'worker_lease_expired')
                transport.health()
                events.add('request',id=a['id'],ordered_request_sha256=a['ordered_request_sha256'])
                row.update(status='failed',reservation='unknown')
                save(out/'outcomes.json',rows)
                events.add('dispatch',id=a['id'])
                response=transport.send(a)
                row['status']='invalid'
                checked=validate(response['visible_response'],a['request'],SNAPSHOT)
                require(response['id']==a['id'] and response['ordered_request_sha256']==a['ordered_request_sha256']
                        and response['checked']==checked and checked['input_tokens'] <= 32000
                        and response['settled_nano']==math.ceil(checked['cost_usd']*1e9)
                        and 0 <= response['settled_nano'] <= RESERVE
                        and type(response['latency_seconds']) in (int,float)
                        and 0 <= response['latency_seconds'] <= 60, 'relay_response_binding')
                row.update(status='completed',action=checked['action'],checked=checked,
                    visible_response=response['visible_response'],settled_nano=response['settled_nano'],
                    reservation='settled',latency_seconds=response['latency_seconds'])
            except Exception as error:
                failure=True
                if isinstance(error,DispatchFailure):
                    row['status']=error.status
                    if error.settled_nano is not None:
                        row['settled_nano']=error.settled_nano; row['reservation']='settled'
                elif row['status'] != 'invalid': row['status']='failed'
                row['action']=None
                row['failure']='transport_or_contract_failure'
                events.add('failure',id=a['id'],reservation=row['reservation'])
                break
    except BaseException:
        failure=True
        raise
    finally:
        for row in rows:
            events.add('terminal',id=row['id'],outcome_sha256=digest(row))
        events.close()
        finish_bundle(out,packet,rows,{'status':'stopped' if failure else 'completed',
            'attempt':receipt['attempt'],'allocation_lineage_sha256':receipt.get('allocation_lineage_sha256'),
            'zero_dispatch_predecessor':'rd6-q0-a1' if 'zero_dispatch_replacement' in receipt else None,
            'worker_loop_ended':True,'elapsed_seconds':clock()-started},mode=mode)
    return not failure


def bound_admission(path, expected):
    data=Path(path).read_bytes()
    require(hashlib.sha256(data).hexdigest()==expected,'admission_bytes_changed')
    return json.loads(data)


def worker_preflight(packet, receipt, out):
    """No provider, credential or ledger access; test exact remote startup inputs."""
    live_preflight(packet,receipt,worker=True)
    out=Path(out)
    require(not out.exists(),'worker_output_exists')
    out.parent.mkdir(parents=True,exist_ok=True)
    # Exercise actual parent write access without creating/reusing the run output.
    with tempfile.TemporaryFile(dir=out.parent) as probe:
        probe.write(b'rd6-startup');probe.flush();os.fsync(probe.fileno())


def admitted_worker(packet, receipt, out, *, transport_factory=Transport):
    """Safe startup telemetry even if admission fails before the response bundle."""
    out=Path(out);out.parent.mkdir(parents=True,exist_ok=True)
    diagnostic=out.with_name(out.name+'.startup.json')
    # Do not overwrite evidence from a previous invocation.
    with diagnostic.open('x') as f:f.write('{}\n')
    status={'schema':'rd6-startup-v1','packet_sha256':digest(packet),
            'phase':'admission','state':'starting','native_dispatch':'not_started'}
    save(diagnostic,status)
    try:
        worker_preflight(packet,receipt,out)
        status.update(phase='worker_loop',state='running',native_dispatch='inspect_original_ledger')
        save(diagnostic,status)
        okay=run_worker(packet,receipt,out,transport_factory(packet))
        status.update(phase='finished',state='completed' if okay else 'stopped')
        return okay
    except BaseException:
        status.update(state='failed',error_category='startup_check_failed' if status['phase']=='admission' else 'worker_loop_failed')
        raise
    finally:
        save(diagnostic,status)


def relay(packet, receipt, credential, ledger_path, out):
    live_preflight(packet,receipt)  # no credentials read until admitted
    authority=evidence(receipt['budget'])
    require(str(Path(ledger_path).resolve())==authority['ledger_path'], 'ledger_argument_mismatch')
    provider=Provider(credential)
    ledger=Ledger(ledger_path,authority)
    engine=None; server=None
    try:
        engine=RelayEngine(packet,receipt,ledger,provider,out)
        class Handler(BaseHTTPRequestHandler):
            def log_message(self,*args): pass
            def answer(self,status,body):
                data=wire(body)
                self.send_response(status);self.send_header('Content-Type','application/json')
                self.send_header('Content-Length',str(len(data)));self.end_headers()
                try: self.wfile.write(data)
                except OSError: engine.stop()
            def do_GET(self):
                ready=self.path=='/health' and engine.healthy()
                self.answer(200 if ready else 503,{'ready':ready,'packet_sha256':digest(packet)})
            def do_POST(self):
                try:
                    require(self.path=='/decision','relay_path')
                    size=int(self.headers.get('Content-Length','0'))
                    require(0 < size <= 20000,'request_size')
                    result=engine.handle(json.loads(self.rfile.read(size)))
                    self.answer(200,result)
                except Exception as error:
                    engine.stop(); self.answer(503,{'error':'relay_stopped',
                        'status':error.status if isinstance(error,DispatchFailure) else 'failed',
                        'settled_nano':error.settled_nano if isinstance(error,DispatchFailure) else None})
        class Server(HTTPServer): allow_reuse_address=True
        server=Server(('127.0.0.1',PORT),Handler); server.timeout=1
        def stop(*args): engine.stop()
        signal.signal(signal.SIGTERM,stop); signal.signal(signal.SIGINT,stop)
        print(json.dumps({'relay':'ready','packet_sha256':digest(packet)}),flush=True)
        while engine.healthy(): server.handle_request()
    finally:
        if server: server.server_close()
        if engine: engine.close()
        else: ledger.close()


def stop_child(child):
    if child.poll() is None:
        os.killpg(child.pid,signal.SIGTERM)
        try: child.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(child.pid,signal.SIGKILL);child.wait(timeout=5)


def supervise(relay_argv, worker_argv, transport, *, timeout=1800, popen=subprocess.Popen, diagnostics=None):
    """Own both local process groups; never treats SSH exit as remote stop proof."""
    children=[]
    state=diagnostics if diagnostics is not None else {}
    try:
        state['phase']='relay_start'
        children.append(popen(relay_argv,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
        ready=False
        for _ in range(100):
            require(children[0].poll() is None,'relay_start_failed')
            try: transport.health(); ready=True; break
            except Exception: time.sleep(.1)
        require(ready,'relay_ready_timeout')
        state['phase']='worker_start'
        children.append(popen(worker_argv,start_new_session=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL))
        state['phase']='worker_wait'
        start=time.monotonic()
        while children[1].poll() is None:
            require(children[0].poll() is None,'relay_exited')
            require(time.monotonic()-start < timeout,'supervisor_timeout')
            time.sleep(.1)
        state['worker_exit_code']=children[1].returncode
        require(children[1].returncode==0,'worker_exit')
        state['phase']='completed'
    finally:
        for child in reversed(children): stop_child(child)


def finalize(out, stop_receipt, *, command=subprocess.run):
    """Required shared offline closeout hook, after actual worker/relay stop checks."""
    out=Path(out).resolve();bundle=read(out/'bundle.json')
    audit_bundle(out,bundle['sha256'])
    execution=read(out/'execution.json'); stop=evidence(stop_receipt)
    require(execution['mode']=='native' and stop.get('attempt')==execution['attempt']
            and stop.get('bundle_sha256')==bundle['sha256'] and stop.get('worker_stopped_verified') is True
            and stop.get('relay_stopped_verified') is True and stop.get('verifier'), 'verified_stop_required')
    outcome='completed' if execution['status']=='completed' else ('ambiguous' if any(r.get('reservation')=='unknown' for r in read(out/'outcomes.json')) else 'failed')
    result=command([sys.executable,str(ROOT/'scripts/experiment.py'),'finalize','right-dissenter',
        '--attempt',execution['attempt'],'--results',str(out),'--outcome',outcome,'--worker-stopped'],
        cwd=ROOT,capture_output=True,text=True)
    require(result.returncode==0,'shared_finalize_failed')
    try: closeout=json.loads(result.stdout)
    except Exception: closeout={}
    require(closeout.get('closeout_status')=='written_review_required','shared_finalize_incomplete')
    return {'operational_finalize':'completed','scientific_review':'required','allocation_release':'not_verified'}


def main():
    p=argparse.ArgumentParser(description=__doc__); sub=p.add_subparsers(dest='cmd',required=True)
    prep=sub.add_parser('prepare');prep.add_argument('--stage',choices=('Q0','D0'),required=True);prep.add_argument('--out',required=True)
    for name in ('relay','worker','check-worker'):
        c=sub.add_parser(name);c.add_argument('--packet',required=True);c.add_argument('--admission',required=True);c.add_argument('--out',required=True)
        c.add_argument('--admission-sha256',required=True)
        if name=='relay':c.add_argument('--credential',required=True);c.add_argument('--ledger',required=True)
    r=sub.add_parser('report');r.add_argument('--out',required=True);r.add_argument('--bundle-sha256',required=True)
    f=sub.add_parser('finalize');f.add_argument('--out',required=True);f.add_argument('--stop-receipt',required=True)
    a=p.parse_args()
    try:
        if a.cmd=='prepare':
            out=Path(a.out);require(not out.exists(),'prepare_output_exists');save(out,prepare(a.stage))
            print(json.dumps({'prepared':a.stage,'native_admission':False,'model_calls':0}))
        elif a.cmd=='report':
            packet,rows=audit_bundle(a.out,a.bundle_sha256)
            print(json.dumps({'stage':packet['stage'],'assignments':len(rows),'integrity':'verified','provider_authenticity':'requires_relay_review'}))
        elif a.cmd=='finalize': print(json.dumps(finalize(a.out,read(a.stop_receipt))))
        else:
            packet=read(a.packet);receipt=bound_admission(a.admission,a.admission_sha256)
            if a.cmd=='relay': relay(packet,receipt,a.credential,a.ledger,a.out)
            elif a.cmd=='check-worker':
                worker_preflight(packet,receipt,a.out)
                print(json.dumps({'worker_preflight':'ready','packet_sha256':digest(packet),'admission_sha256':a.admission_sha256}))
            else:
                def interrupted(*args): raise TimeoutError('worker_stop_signal')
                signal.signal(signal.SIGTERM,interrupted);signal.signal(signal.SIGINT,interrupted)
                okay=admitted_worker(packet,receipt,a.out)
                raise SystemExit(0 if okay else 1)
    except Exception:
        # Do not print arbitrary exception/provider/config contents or tracebacks.
        print(json.dumps({'status':'blocked_or_stopped','detail':'inspect saved allowlisted events and admission evidence'}))
        raise SystemExit(1) from None


if __name__=='__main__': main()
