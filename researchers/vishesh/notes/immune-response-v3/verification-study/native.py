"""Stage-scoped original-ledger transport, gated by the native runner."""
import hashlib,json,os,sqlite3,time,uuid
from contextlib import closing
from pathlib import Path
import instrument
from native_provider import NativePolicy

class Policy(NativePolicy):
    def __init__(self,ledger,usage_path):
        self.ledger=str(Path(ledger));self.usage_path=Path(usage_path)
        if not Path(ledger).is_file():raise ValueError('original_ledger_required')
        self.model=instrument.MODEL;self.input_rate=5;self.output_rate=25;self.max_output=512;self.max_input_bytes=8000
        self.base='http://127.0.0.1:18765';self.key='';self.run_id='verification-v1';self.limit=192
        self.calls=0;self.actual_usd=0.;self.usage_missing=0;self.last_content=None
        with closing(sqlite3.connect('file:'+self.ledger+'?mode=rw',uri=True)) as db:
            if db.execute('select count(*) from immune_requests where run_id=?',(self.run_id,)).fetchone()[0]:raise ValueError('attempt_already_dispatched')

    def reserve(self,encoded):
        if len(encoded)>8000:raise ValueError('wire_limit')
        cost=((len(encoded)+512)*5+512*25)/1e6;rid=uuid.uuid4().hex
        with closing(sqlite3.connect('file:'+self.ledger+'?mode=rw',uri=True,timeout=20)) as db,db:
            db.execute('BEGIN IMMEDIATE')
            cap,used,calls=db.execute('select cap,reserved,calls from budget where id=1').fetchone()
            count,reserved=db.execute('select count(*),coalesce(sum(reserved_usd),0) from immune_requests where run_id=?',(self.run_id,)).fetchone()
            if round(used+cost,6)>cap or count>=192 or reserved+cost>10.629120+1e-9:raise ValueError('persistent_budget_or_stage_limit')
            db.execute('update budget set reserved=?,calls=? where id=1',(round(used+cost,6),calls+1))
            db.execute('insert into immune_requests values (?,?,?,?,?,?,?,?,?,?)',(rid,self.run_id,hashlib.sha256(encoded).hexdigest(),'reserved_unresolved',cost,None,None,None,time.time(),None))
        self.calls+=1;self.usage_missing+=1;self.export();return rid

    def export(self):
        with closing(sqlite3.connect('file:'+self.ledger+'?mode=rw',uri=True)) as db:
            db.row_factory=sqlite3.Row;rows=[dict(r) for r in db.execute('select * from immune_requests where run_id=? order by started',(self.run_id,))]
        self.usage_path.parent.mkdir(parents=True,exist_ok=True);temp=self.usage_path.with_suffix('.tmp')
        with temp.open('w') as f:
            for r in rows:f.write(json.dumps(r)+'\n')
            f.flush();os.fsync(f.fileno())
        os.replace(temp,self.usage_path)

    def record(self,row):
        if row['kind']=='response':
            choices=row['body'].get('choices',[])
            if choices:self.last_content=choices[0]['message']['content']
        super().record(row)

    def complete(self,request,fallback=None):
        result=super().complete(request,fallback)
        def unique(pairs):
            if len(dict(pairs))!=len(pairs):raise ValueError('duplicate_json_fields')
            return dict(pairs)
        if json.loads(self.last_content,object_pairs_hook=unique)!=result:raise ValueError('response_mismatch')
        return result
