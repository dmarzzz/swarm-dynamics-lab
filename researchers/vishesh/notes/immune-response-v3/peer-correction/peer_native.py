"""Credential-free relay adapter. Funded stages still require fresh native admission."""
import hashlib
import json
import os
import sqlite3
import time
import uuid
from contextlib import closing
from pathlib import Path
import peer_instrument as i
from native_provider import NativePolicy

DISPATCH_ENABLED = True
STAGES = {'peer-correction-q1':(48,2.657280), 'peer-correction-p1':(184,10.186240)}
CAMPAIGN_MAX = 12.843520


class Policy(NativePolicy):
    def __init__(self, ledger, usage_path, stage, packet_sha256, deadline):
        if stage not in STAGES:raise ValueError('unfunded_stage')
        self.ledger=str(Path(ledger).resolve())
        if not Path(self.ledger).is_file():raise ValueError('original_ledger_required')
        if deadline<=time.time():raise ValueError('expired_stage')
        self.usage_path=Path(usage_path);self.run_id=stage
        self.limit,self.model_max=STAGES[stage]
        self.deadline=deadline;self.model='anthropic/claude-opus-4.6'
        self.input_rate=5;self.output_rate=25;self.max_output=512;self.max_input_bytes=8000
        self.base='http://127.0.0.1:18765';self.key=''
        self.calls=0;self.actual_usd=0.;self.usage_missing=0;self.last_content=None
        with closing(self.connection()) as db,db:
            db.execute('BEGIN IMMEDIATE')
            # Require existing ledger/schema; never create/reset budget or request tables.
            db.execute('select cap,reserved,calls from budget where id=1').fetchone()
            if db.execute('select count(*) from immune_requests where run_id=?',(stage,)).fetchone()[0]:
                raise ValueError('attempt_already_dispatched')
            db.execute('create table if not exists immune_peer_claims(run_id text primary key,packet_sha256 text,started real)')
            if db.execute('select 1 from immune_peer_claims where run_id=?',(stage,)).fetchone():
                raise ValueError('attempt_already_claimed')
            db.execute('insert into immune_peer_claims values(?,?,?)',(stage,packet_sha256,time.time()))

    def connection(self):
        return sqlite3.connect('file:'+self.ledger+'?mode=rw',uri=True,timeout=20)

    def reserve(self,encoded):
        if time.time()>=self.deadline:raise ValueError('stage_deadline')
        if len(encoded)>8000:raise ValueError('wire_limit')
        cost=((len(encoded)+512)*5+512*25)/1e6
        rid=uuid.uuid4().hex
        with closing(self.connection()) as db,db:
            db.execute('BEGIN IMMEDIATE')
            cap,used,calls=db.execute('select cap,reserved,calls from budget where id=1').fetchone()
            count,reserved=db.execute('select count(*),coalesce(sum(reserved_usd),0) from immune_requests where run_id=?',(self.run_id,)).fetchone()
            campaign_calls,campaign_reserved=db.execute('select count(*),coalesce(sum(reserved_usd),0) from immune_requests where run_id in (?,?)',tuple(STAGES)).fetchone()
            if (round(used+cost,6)>cap or count>=self.limit or reserved+cost>self.model_max+1e-9
                or campaign_calls>=232 or campaign_reserved+cost>CAMPAIGN_MAX+1e-9):
                raise ValueError('persistent_budget_or_stage_limit')
            db.execute('update budget set reserved=?,calls=? where id=1',(round(used+cost,6),calls+1))
            db.execute('insert into immune_requests values(?,?,?,?,?,?,?,?,?,?)',
                       (rid,self.run_id,hashlib.sha256(encoded).hexdigest(),'reserved_unresolved',cost,None,None,None,time.time(),None))
        self.calls+=1;self.usage_missing+=1;self.export()
        return rid

    def finish(self,request_id,state,usage=None):
        usage=usage or {}
        known=all(type(usage.get(k)) is int and usage[k]>=0 for k in ('input_tokens','output_tokens'))
        actual=(usage['input_tokens']*5+usage['output_tokens']*25)/1e6 if known else None
        with closing(self.connection()) as db,db:
            db.execute('update immune_requests set state=?,input_tokens=?,output_tokens=?,actual_usd=?,ended=? where request_id=?',
                       (state,usage.get('input_tokens') if known else None,usage.get('output_tokens') if known else None,actual,time.time(),request_id))
        if known:self.actual_usd+=actual;self.usage_missing-=1
        self.export()

    def export(self):
        with closing(self.connection()) as db:
            db.row_factory=sqlite3.Row
            rows=[dict(r) for r in db.execute('select * from immune_requests where run_id=? order by started',(self.run_id,))]
        self.usage_path.parent.mkdir(parents=True,exist_ok=True,mode=0o700)
        temporary=self.usage_path.with_suffix('.tmp')
        with temporary.open('w') as f:
            for row in rows:f.write(json.dumps(row)+'\n')
            f.flush();os.fsync(f.fileno())
        os.replace(temporary,self.usage_path)

    def record(self,row):
        if row['kind']=='response':
            choices=row['body'].get('choices',[])
            if choices:self.last_content=choices[0]['message']['content']
        super().record(row)

    def complete(self,request,fallback=None):
        if not DISPATCH_ENABLED:raise ValueError('native_dispatch_disabled_pending_grant')
        result=super().complete(request,fallback)
        def unique(pairs):
            if len(dict(pairs))!=len(pairs):raise ValueError('duplicate_json_fields')
            return dict(pairs)
        if json.loads(self.last_content,object_pairs_hook=unique)!=result:raise ValueError('response_mismatch')
        return result
