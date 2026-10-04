"""Durable execution core. Transport is injected; all experimental inputs are whitelisted."""
import copy
import datetime
import json
import time
from pathlib import Path
from contract import packet
from design import schedule,conditions,eid,clean_packet,qualified,endpoint,contrasts
from wire import request,validate,reservation,digest,failure_code

def save(path,value):
    path=Path(path);tmp=path.with_suffix(path.suffix+'.tmp')
    with tmp.open('w') as f:
        json.dump(value,f,indent=2,allow_nan=False);f.flush()
        import os
        os.fsync(f.fileno())
    tmp.replace(path)

class Engine:
    def __init__(self,stage,attempt,out,ledger,transport,worlds,admission=None,progress=lambda *a:None,clock=time.monotonic):
        self.stage=stage;self.attempt=attempt;self.out=Path(out);self.ledger=ledger;self.transport=transport;self.worlds=worlds;self.admission=admission;self.progress=progress;self.clock=clock
        self.executed=set();self.start=clock();self.failures=0;self.stop=None
        self.rows=[dict(a,status='not-started') for a in schedule(stage,sorted(worlds))];self.by={r['id']:r for r in self.rows}
        self.out.mkdir(parents=True,exist_ok=False)
        save(self.out/'manifest.json',dict(stage=stage,attempt=attempt,assignments=schedule(stage,sorted(worlds))))
        save(self.out/'worlds.json',worlds);self.persist()
    def persist(self):save(self.out/'records.json',self.rows)
    def journal(self,kind,value):
        import os
        with (self.out/'events.jsonl').open('a') as f:
            f.write(json.dumps({'kind':kind,'value':value},separators=(',',':'),allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    def active(self):
        if not self.stop and (self.clock()-self.start>=3600 or self.failures>=5):self.stop='wall_time' if self.clock()-self.start>=3600 else 'five_consecutive_failures'
        if self.admission is not None and not self.admission.current():self.stop='admission_deadline'
        return self.stop is None
    def call(self,row,packet,kind):
        if not self.active():return
        req=request(packet,kind);row.update(request=req,request_sha256=digest(req))
        # Reservation precedes any wire effect. A crash after reserve is charged as uncertain.
        try:self.ledger.reserve(self.attempt+':'+row['id'],reservation(req))
        except Exception:self.stop='budget_or_duplicate_guard';self.persist();return
        row.update(status='started',started_utc=datetime.datetime.now(datetime.timezone.utc).isoformat());self.journal('call-start',row)
        started=self.clock()
        try:
            raw=self.transport(req);checked=validate(raw,req)
        except Exception as exc:
            # Never retain exception text, request headers or provider error bodies.
            row.update(status='invalid' if isinstance(exc,ValueError) else 'failed',failure_code=failure_code(exc))
            self.ledger.finish(self.attempt+':'+row['id']);self.failures+=1
        else:
            self.ledger.finish(self.attempt+':'+row['id'],round(checked['usage']['cost']*1e9))
            row.update(status='valid',checked=checked);self.failures=0
        row['elapsed_seconds']=self.clock()-started;self.journal('call-terminal',row)
        self.progress(sum(r['status']!='not-started' for r in self.rows),len(self.rows),self.ledger.summary())
    def run(self):
        if self.stage=='Q0':
            for row in self.rows:self.call(row,clean_packet(self.worlds[row['seed']],row['actor'],row['case']),'map')
            result=qualified(self.rows,self.worlds)
        else:
            for seed,w in self.worlds.items():
                if not self.active():break
                for c in conditions(seed):
                    id=eid(seed,c)
                    if not self.active():break
                    p,path=packet(w,**c);self.executed.add(id)
                    for i,cell in enumerate(path):self.journal('sensing',dict(episode=id,slot=i+1,target=cell,scripted=True))
                    for actor in range(3):self.call(self.by[f'{id}-map-{actor}'],packet(w,actor=actor,**c)[0],'map')
                self.persist()
            result=contrasts(self.save_episodes())
        result.update(stage=self.stage,attempt=self.attempt,assigned=len(self.rows),started=sum(r['status']!='not-started' for r in self.rows),terminal=sum(r['status'] in ('valid','invalid','failed') for r in self.rows),valid=sum(r['status']=='valid' for r in self.rows),stop_reason=self.stop,budget=self.ledger.summary())
        self.persist();result['wall_seconds']=self.clock()-self.start;save(self.out/'summary.json',result);return result
    def save_episodes(self):
        rows=[]
        for seed,w in self.worlds.items():
            for c in conditions(seed):
                id=eid(seed,c);p,path=packet(w,slots=12 if id in self.executed else 0,**c);path=path if id in self.executed else [];records=[self.by[f'{id}-map-{actor}'] for actor in range(3)]
                rows.append(dict(c,id=id,seed=seed,family=w['family'],truth=w['truth'],report_cells=w['region'],path=path,packet=p,endpoint=endpoint(w,p,records),status='complete' if all(r['status'] in ('valid','invalid','failed') for r in records) else 'partial_or_unstarted'))
        save(self.out/'episodes.json',rows);return rows
