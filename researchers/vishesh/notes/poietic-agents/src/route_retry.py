"""Bounded same-request transport adapter; injected I/O only, no credentials or CLI.

This module does not grant admission. A future admitted worker must supply the original
transactional ledger, private raw-response transport archive and fixed deadline.
"""
import copy
import math
import random
import time
from pathlib import Path
import json
from common import canonical,digest
from native import reserve_nano,usage_receipt,verify_catalog
from q30v3 import wire as qualified_wire
from provider_diagnostics import safe_error,has_provider_error

BASE=Path(__file__).resolve().parents[1]
MAX_PHYSICAL=54
MAX_RETRIES=6

def contract():return json.loads((BASE/'route-repair/model.json').read_text())

def wire(sections):
    req=qualified_wire(contract(),sections)
    req['provider'].update(require_parameters=True,data_collection='deny')
    if len(canonical(req))>7500:raise ValueError('request_input_bound')
    return req

def validate_catalog(data):
    c=contract();receipt=verify_catalog(data,c)
    e=next(x for x in data['data']['endpoints'] if x['tag']==c['provider_tag'])
    if e.get('quantization')!='bf16' or e.get('model_id')!=c['requested_model_id']:raise ValueError('catalog_model_precision')
    if not {'response_format','reasoning','reasoning_effort','temperature','max_tokens'}<=set(e.get('supported_parameters',[])):raise ValueError('catalog_parameter_support')
    if e.get('context_length',0)<9216 or e.get('max_completion_tokens',0)<1024:raise ValueError('catalog_context_limits')
    return dict(receipt,parameter_support=True,terms_reviewed=False,native_qualified=False)

def retry_delay(receipt,retry_number,remaining_seconds,jitter):
    if not receipt.get('retry_eligible_envelope') or retry_number not in (1,2):return None
    if receipt.get('diagnostic_conflicts') or receipt.get('provider_name_mismatch'):return None
    if receipt.get('provider_status',429)!=429:return None
    if receipt.get('limit_source') in ('openrouter_credits','openrouter_key_limit') or receipt.get('limit_reason')=='weight_exceeds_budget':return None
    if receipt.get('provider_code') in ('insufficient_quota','insufficient_credits'):return None
    if receipt.get('provider_error_type') in ('authentication','permission_denied','payment_required','invalid_request'):return None
    hint=receipt.get('retry_after_seconds',0)
    if type(hint) not in (int,float) or not math.isfinite(hint) or not 0<=hint<=60:return None
    if type(jitter) not in (int,float) or not math.isfinite(jitter) or not 0<=jitter<=1:raise ValueError('retry_jitter')
    delay=max(5,5*2**(retry_number-1),hint)+jitter
    return delay if delay+50<remaining_seconds else None

def _reserve_scoped(budget, call_id, request_hash, amount):
    # Same original transactional authority; atomic stage/retry ceilings cannot be
    # reset by another adapter object. A new database is never opened here.
    db=budget.db;db.execute('BEGIN IMMEDIATE')
    try:
        cap,maximum,deadline=db.execute('SELECT cap,calls,deadline FROM authority WHERE id=1').fetchone()
        count,used=db.execute('SELECT COUNT(*),COALESCE(SUM(COALESCE(settled,reserve)),0) FROM charges').fetchone()
        stage=db.execute("SELECT id FROM charges WHERE id LIKE 'Q30-05:%'").fetchall()
        retries=sum(not x[0].endswith(':physical-0') for x in stage)
        if db.execute('SELECT 1 FROM charges WHERE id=?',(call_id,)).fetchone():raise ValueError('duplicate_call')
        if len(stage)>=MAX_PHYSICAL or (not call_id.endswith(':physical-0') and retries>=MAX_RETRIES):raise ValueError('stage_physical_cap')
        if type(amount) is not int or amount<=0 or used+amount>cap or count>=maximum or time.time()>=deadline:raise ValueError('budget_or_deadline')
        db.execute('INSERT INTO charges VALUES (?,?,?,NULL,?,?)',(call_id,request_hash,amount,'reserved',time.time()));db.commit()
    except BaseException:
        db.rollback();raise

class TransportStopped(ValueError):pass

class Adapter:
    def __init__(self,budget,transport,deadline,*,clock=time.monotonic,wall=time.time,sleep=time.sleep,jitter=random.random,emit=lambda r:None):
        self.budget,self.transport,self.deadline=budget,transport,deadline
        self.clock,self.wall,self.sleep,self.jitter,self.emit=clock,wall,sleep,jitter,emit
        self.physical=0;self.retries=0;self.last=None;self.seen=set();self.stopped=False
        self.allowed={f'Q30-05:cheap_generative:{c}:{s}' for c in range(12) for s in range(4)}
    def _wait(self,delay):
        until=self.clock()+delay
        while self.clock()<until:
            left=until-self.clock()
            if self.wall()+left+50>=self.deadline:raise TransportStopped('retry_deadline')
            self.sleep(left)
    def invoke(self,logical_id,request):
        if self.stopped or logical_id not in self.allowed or logical_id in self.seen:raise ValueError('closed_or_unassigned_logical_request')
        c=contract();expected=wire(json.loads(request['messages'][0]['content']))
        if request!=expected:raise ValueError('pinned_request_contract')
        self.seen.add(logical_id);request=copy.deepcopy(request);request_hash=digest(request)
        for attempt in range(3):
            if self.physical>=MAX_PHYSICAL or (attempt and self.retries>=MAX_RETRIES) or self.wall()+50>=self.deadline:
                self.stopped=True;raise TransportStopped('physical_or_time_cap')
            if self.last is not None:
                try:self._wait(max(0,5-(self.clock()-self.last)))
                except TransportStopped:self.stopped=True;raise
            physical_id=logical_id+':physical-'+str(attempt)
            try:_reserve_scoped(self.budget,physical_id,request_hash,reserve_nano(c))
            except Exception:
                self.stopped=True;raise TransportStopped('budget_guard') from None
            self.physical+=1;self.retries+=bool(attempt);self.last=self.clock()
            row=dict(id=physical_id,logical_id=logical_id,request_sha256=request_hash,physical_index=self.physical,started_monotonic=self.last)
            try:
                status,raw,headers=self.transport(copy.deepcopy(request))
            except Exception:
                self.budget.settle(physical_id);row.update(status='ambiguous_transport',retry=False);self.emit(row);self.stopped=True
                raise TransportStopped('ambiguous_transport_no_retry') from None
            if status==200 and not has_provider_error(raw):
                try:self.budget.settle(physical_id,math.ceil(usage_receipt(raw,c)['cost_usd']*1e9))
                except (ValueError,KeyError,TypeError,AttributeError):
                    self.budget.settle(physical_id);self.stopped=True;row.update(status='billing_failure',retry=False);self.emit(row)
                    raise TransportStopped('billing_failure_no_retry') from None
                if raw.get('model') not in c['accepted_response_model_ids'] or raw.get('provider')!=c['provider_name']:
                    row.update(status='route_mismatch',retry=False);self.emit(row);self.stopped=True
                    raise TransportStopped('route_mismatch_no_retry')
                row.update(status='returned',response_sha256=digest(raw),retry=False);self.emit(row)
                # Parsing and semantic checks belong to the owning worker;
                # they must never call invoke again with this logical ID.
                return raw
            self.budget.settle(physical_id)
            receipt=safe_error(status,raw,headers,c['provider_name'],self.wall())
            delay=retry_delay(receipt,attempt+1,self.deadline-self.wall(),self.jitter()) if self.physical<MAX_PHYSICAL and self.retries<MAX_RETRIES else None
            row.update(status='refused',diagnostic=receipt,retry=delay is not None,delay_s=delay);self.emit(row)
            if delay is None:self.stopped=True;raise TransportStopped('transport_refusal_no_retry')
            try:self._wait(delay)
            except TransportStopped:self.stopped=True;raise
        self.stopped=True;raise TransportStopped('logical_retry_cap')
