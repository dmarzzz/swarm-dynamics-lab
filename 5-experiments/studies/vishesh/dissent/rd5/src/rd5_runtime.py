"""Fail-closed RD5 transport, admission and the original cumulative budget ledger.

Secret material is consumed only by relay_main. Neither exceptions nor provider
response text are printed. Local loopback relay is exposed remotely only through
an operator-supervised encrypted forward to the exclusively claimed run host.
"""
import datetime as dt
import hashlib
import json
import math
import platform
import re
import sqlite3
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from http.server import BaseHTTPRequestHandler, HTTPServer
from common import digest, save
from rd5_core import SNAPSHOT

BASE = Path(__file__).resolve().parent.parent
OLD = BASE.parent/'src'
sys.path.insert(0, str(OLD))
from jev import validate, response_fingerprint

RESERVE = 1_344_000
RATE = 0.000000042
PORT = 18459
URL = 'http://127.0.0.1:'+str(PORT)


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, *args, **kwargs):
        raise ValueError('redirect_refused')


def budget_snapshot(db):
    count, committed = db.execute('SELECT count(*),coalesce(sum(coalesce(actual_nano,reserved_nano)),0) FROM calls').fetchone()
    return {'lifetime_calls': count, 'committed_nano': committed}


def reserve(db, stage, identity):
    if stage not in ('Q5', 'H5'):
        raise ValueError('stage')
    db.execute('BEGIN IMMEDIATE')
    try:
        prior = budget_snapshot(db)
        # An empty/copy-reset ledger cannot create a fresh budget. Historical calls
        # and reservations remain untouched; actual authority is still this DB.
        if prior['lifetime_calls'] < 428 or prior['committed_nano'] < 20_652_450:
            raise ValueError('original_ledger_required')
        count = db.execute("SELECT count(*) FROM calls WHERE key LIKE 'RD5:%'").fetchone()[0]
        stage_count = db.execute('SELECT count(*) FROM calls WHERE key LIKE ?', ('RD5:'+stage+':%',)).fetchone()[0]
        if (prior['lifetime_calls'] >= 488 or count >= 60 or stage_count >= (24 if stage == 'Q5' else 36)
                or prior['committed_nano']+RESERVE > 1_000_000_000):
            raise ValueError('budget_exhausted')
        key = 'RD5:'+stage+':'+identity
        db.execute('INSERT INTO calls(key,status,reserved_nano) VALUES(?,?,?)', (key, 'dispatch_unknown', RESERVE))
        db.commit()
        return key
    except BaseException:
        db.rollback()
        raise


def settle(db, key, response, req):
    """Record reliable usage even if semantic/route validation fails."""
    usage = response.get('usage', {}) if isinstance(response, dict) else {}
    cost = usage.get('cost') if isinstance(usage, dict) else None
    nano = math.ceil(cost*1e9) if type(cost) in (int,float) and math.isfinite(cost) and 0 <= cost <= 1 else None
    if nano is not None:
        db.execute('UPDATE calls SET actual_nano=? WHERE key=?', (nano, key))
        db.commit()
    db.execute('CREATE TABLE IF NOT EXISTS rd5_responses(key TEXT PRIMARY KEY,data TEXT)')
    diagnostic = response_fingerprint(response,req,SNAPSHOT)
    db.execute('INSERT INTO rd5_responses VALUES(?,?)',(key,json.dumps({'diagnostic':diagnostic},allow_nan=False))); db.commit()
    try:
        checked = validate(response, req, SNAPSHOT)
        if nano is None or nano > RESERVE:
            raise ValueError('cost_above_reservation')
    except Exception:
        db.execute('UPDATE calls SET status=? WHERE key=?', ('invalid_response',key)); db.commit()
        raise ValueError('invalid_response') from None
    db.execute('UPDATE calls SET status=? WHERE key=?', ('completed',key)); db.commit()
    db.execute('UPDATE rd5_responses SET data=? WHERE key=?',(json.dumps({'checked':checked,'diagnostic':diagnostic}),key)); db.commit()
    return checked


def source_hashes():
    paths = sorted((BASE/'src').glob('*.py')) + [BASE/'PLAN.md', BASE/'AMENDMENT-01.md', BASE/'spec/next-run-plan.json', OLD/'jev.py', OLD/'cases.py']
    root = Path(subprocess.check_output(['git','rev-parse','--show-toplevel'], cwd=BASE, text=True).strip())
    return {str(p.relative_to(root)): hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}


def validate_packet(packet):
    if packet.get('schema') != 'rd5-prepared-v1' or packet.get('stage') not in ('Q5','H5'):
        raise ValueError('packet_schema')
    if packet['source_hashes'] != source_hashes() or packet['instrument_sha256'] != digest(source_hashes()):
        raise ValueError('instrument_mismatch')
    if packet['assignment_sha256'] != digest(packet['assignments']) or packet['allowed_sha256'] != digest(packet['allowed']):
        raise ValueError('packet_integrity')
    if packet['definition_sha256'] != digest(packet['definition']):
        raise ValueError('definition_mismatch')
    if packet.get('proposal_sha256') != hashlib.sha256((BASE/'spec/next-run-plan.json').read_bytes()).hexdigest():
        raise ValueError('proposal_mismatch')
    if len(packet['assignments']) != (24 if packet['stage']=='Q5' else 72):
        raise ValueError('assignment_count')
    if len({a['id'] for a in packet['assignments']}) != len(packet['assignments']):
        raise ValueError('duplicate_assignment')


def verify_receipt(packet, receipt, *, check_host=True, now=None):
    """Offline receipt structure/binding; online plan and runtime checks follow.

    Fleet/account/page fields are fresh operator attestations, not independent
    audits. They must name actual evidence files and hashes, not a fabricated pass.
    """
    now = now or dt.datetime.now(dt.timezone.utc)
    parse = lambda value: dt.datetime.fromisoformat(value.replace('Z','+00:00'))
    if receipt.get('packet_sha256') != digest(packet) or receipt.get('stage') != packet['stage']:
        raise ValueError('receipt_binding')
    age = (now-parse(receipt['verified_utc'])).total_seconds()
    if not 0 <= age <= 300 or parse(receipt['claim_until']) < now+dt.timedelta(minutes=31):
        raise ValueError('receipt_expired')
    if check_host and platform.node() != receipt['host']:
        raise ValueError('wrong_host')
    for field in ('exclusive_claim_verified','approved_fleet_account_verified','public_page_verified',
                  'original_budget_verified','single_ledger_authority_verified','supervised_transport_verified'):
        if receipt.get(field) is not True:
            raise ValueError('missing_'+field)
    for field in ('allocation_receipt_sha256','public_page_receipt_sha256','budget_receipt_sha256'):
        if not re.fullmatch('[0-9a-f]{64}',receipt.get(field,'')):
            raise ValueError('missing_'+field)
    if not receipt.get('claim_id') or not receipt.get('run_id') or len(receipt.get('run_tldr','')) < 80:
        raise ValueError('missing_run_identity')
    if receipt.get('api_cap_usd') != 1 or receipt.get('infrastructure_cap_usd') != 1 or receipt.get('max_lifetime_calls') != 500:
        raise ValueError('original_cap_required')
    approval=receipt.get('owner_plan_approval',{})
    if (approval.get('decision')!='approved' or approval.get('approver_role')!='owner'
        or approval.get('plan_sha256')!=packet['proposal_sha256']
        or approval.get('execution_sha256')!=packet['instrument_sha256']
        or 'launch' not in approval.get('scopes',[]) or packet['stage'] not in approval.get('stages',[])
        or not approval.get('authorization_ref')):
        raise ValueError('owner_updated_plan_approval_required')
    if packet['stage'] == 'H5' and (not receipt.get('qualification_directory') or not re.fullmatch('[0-9a-f]{64}',receipt.get('qualification_bundle_sha256',''))):
        raise ValueError('qualification_required')


def verify_native(packet, receipt, *, check_host=True):
    validate_packet(packet)
    verify_receipt(packet, receipt, check_host=check_host)
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
    if receipt['source_commit'] != head or packet['source_commit'] != head:
        raise ValueError('source_commit_mismatch')
    expected_url = 'https://github.com/dmarzzz/swarm-lab/blob/'+packet['plan_commit']+'/researchers/vishesh/notes/dissent/rd5/AMENDMENT-01.md'
    sys.path.insert(0,str(BASE.parents[1]/'experiment-documentation'))
    import public_plan
    public = public_plan.check('right-dissenter-rd5',receipt['run_tldr'])
    if public['url'] != expected_url or public['plan_sha256'] != packet['plan_sha256']:
        raise ValueError('public_plan_binding')
    if packet['stage'] == 'H5':
        from rd5_cli import audit_qualification
        audit_qualification(Path(receipt['qualification_directory']), packet['instrument_sha256'],receipt['qualification_bundle_sha256'])
    return public


def route_check(opener):
    with opener.open('https://openrouter.ai/api/v1/models/typesafe/jev-1.13/endpoints',timeout=25) as r:
        routes = json.load(r)['data']['endpoints']
    if len(routes) != 1:
        raise ValueError('route_count')
    route = routes[0]
    if (route['provider_name'] != 'TypeSafe' or route['tag'] != 'typesafe' or route['status'] != 0
        or SNAPSHOT not in route['name'] or float(route['pricing']['prompt']) > RATE
        or float(route['pricing']['completion']) != 0 or route['context_length'] > 32000):
        raise ValueError('route_mismatch')
    return {'snapshot':SNAPSHOT,'max_reservation_nano':RESERVE,'route_checked':True}


class Native:
    def __init__(self, packet, out):
        self.packet, self.out, self.calls = packet, Path(out), []
        self.opener = urllib.request.build_opener(NoRedirect())
        self.stopped = False
        self.started = time.monotonic()

    def healthy(self):
        if self.stopped or time.monotonic()-self.started > 1800:
            return False
        try:
            with self.opener.open(URL+'/health',timeout=3) as r:
                response = json.load(r)
            return response == {'ready':True,'packet_sha256':digest(self.packet)}
        except Exception:
            return False

    def resolve(self, identity, req):
        if self.stopped or digest(req) not in self.packet['allowed'].get(identity,{}):
            raise ValueError('unfrozen_request')
        if any(c['identity']==identity for c in self.calls):
            raise ValueError('duplicate_identity')
        row = {'identity':identity,'request_sha256':digest(req),'request':req,'status':'dispatch_unknown'}
        self.calls.append(row); save(self.out/'calls.json',self.calls)
        try:
            wire = urllib.request.Request(URL+'/decision',json.dumps({'identity':identity,'request':req}).encode(),{'Content-Type':'application/json'})
            with self.opener.open(wire,timeout=45) as r:
                response = json.load(r)
            checked = response['checked']
            if checked['request_sha256'] != digest(req) or checked['served_model'] != SNAPSHOT:
                raise ValueError('relay_contract')
            row.update(status='completed',checked=checked)
        except Exception:
            # Worker uncertainty is not evidence of provider non-dispatch. Reconcile
            # against the authoritative relay ledger before any continuation.
            row['status'] = 'dispatch_unknown'; self.stopped = True
            save(self.out/'calls.json',self.calls)
            raise RuntimeError('inference_failure') from None
        save(self.out/'calls.json',self.calls)
        return checked['action']


def relay_main(packet, receipt, credential, ledger):
    verify_native(packet,receipt,check_host=False)
    if credential.stat().st_mode & 0o077:
        raise ValueError('credential_permissions')
    # Refuse to silently create an empty/reset ledger.
    db = sqlite3.connect('file:'+str(ledger)+'?mode=rw',uri=True)
    baseline = budget_snapshot(db)
    if baseline['lifetime_calls'] < 428 or baseline['committed_nano'] < 20_652_450:
        raise ValueError('original_ledger_required')
    opener = urllib.request.build_opener(NoRedirect())
    route_check(opener)
    secret = credential.read_text().strip()
    if not secret:
        raise ValueError('empty_credential')
    # Durable shared-stage fence: restarts need a separately assessed run identity.
    db.execute('CREATE TABLE IF NOT EXISTS rd5_attempts(run_id TEXT PRIMARY KEY,packet_sha256 TEXT,started TEXT)')
    db.execute('INSERT INTO rd5_attempts VALUES(?,?,?)',(receipt['run_id'],digest(packet),receipt['verified_utc'])); db.commit()
    stopped = False
    deadline = time.monotonic()+1800
    class Handler(BaseHTTPRequestHandler):
        def log_message(self,*args): pass
        def respond(self,code,body):
            data = json.dumps(body,allow_nan=False).encode()
            self.send_response(code); self.send_header('Content-Type','application/json')
            self.send_header('Content-Length',str(len(data))); self.end_headers()
            try: self.wfile.write(data)
            except OSError: pass
        def do_GET(self):
            ready = not stopped and time.monotonic()<deadline
            self.respond(200 if ready and self.path=='/health' else 503,{'ready':ready,'packet_sha256':digest(packet)})
        def do_POST(self):
            nonlocal stopped
            key = None
            try:
                if stopped or time.monotonic()>=deadline or self.path!='/decision':
                    raise ValueError('relay_stopped')
                length = int(self.headers.get('Content-Length','0'))
                if not 0 < length <= 20000:
                    raise ValueError('request_size')
                body = json.loads(self.rfile.read(length)); identity, req = body['identity'],body['request']
                if packet['allowed'].get(identity,{}).get(digest(req)) != req:
                    raise ValueError('unfrozen_request')
                key = reserve(db,packet['stage'],identity)
                wire = urllib.request.Request('https://openrouter.ai/api/alpha/decisions',json.dumps(req).encode(),
                                              {'Authorization':'Bearer '+secret,'Content-Type':'application/json'})
                with opener.open(wire,timeout=35) as r:
                    response = json.loads(r.read(200000))
                checked = settle(db,key,response,req)
                self.respond(200,{'checked':checked})
            except Exception:
                stopped = True
                # No arbitrary exception, provider body, headers or credentials escape.
                self.respond(503,{'error':'relay_stopped','reservation_exists':key is not None})
    server = HTTPServer(('127.0.0.1',PORT),Handler); server.timeout=1
    print(json.dumps({'relay':'ready','stage':packet['stage'],'packet_sha256':digest(packet)}),flush=True)
    try:
        while not stopped and time.monotonic()<deadline:
            server.handle_request()
    finally:
        server.server_close(); db.close()
