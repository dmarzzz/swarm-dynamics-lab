"""C1 scoped reuse of durable credential-free transport; no new allowance."""
import os,sqlite3,json
from pathlib import Path
from native_provider import NativePolicy,HTTPPolicy,MODELS
class Policy(NativePolicy):
    def __init__(self):
        assert Path(os.environ['SWARM_BUDGET_LEDGER']).is_file()
        HTTPPolicy.__init__(self)
        assert self.model==MODELS[1] and self.base=='http://127.0.0.1:18765' and not self.key
        assert (self.input_rate,self.output_rate,self.max_output,self.max_input_bytes,self.cap)==(5,25,512,8000,8)
        self.run_id='controller-c1';self.limit=32;self.actual_usd=0.;self.usage_missing=0
        self.usage_path=Path(os.environ['SWARM_USAGE_LOG']);self.last_content=None
        with sqlite3.connect(self.ledger) as db:
            assert db.execute('select count(*) from immune_requests where run_id=?',(self.run_id,)).fetchone()[0]==0
    def record(self,row):
        if row['kind']=='response':
            choices=row['body'].get('choices',[])
            if choices:self.last_content=choices[0]['message']['content']
        super().record(row)
    def complete(self,request,fallback):
        result=super().complete(request,fallback)
        def unique(pairs):
            if len(dict(pairs))!=len(pairs):raise ValueError('duplicate_json_fields')
            return dict(pairs)
        assert json.loads(self.last_content,object_pairs_hook=unique)==result
        return result
