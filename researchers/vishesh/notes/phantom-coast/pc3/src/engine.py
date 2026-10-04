"""Durable execution core. Transport is injected; all experimental inputs are whitelisted."""
import copy
import datetime
import json
import time
from pathlib import Path
from contract import Episode
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
        self.start=clock();self.failures=0;self.stop=None
        self.rows=[dict(a,status='not-started') for a in schedule(stage,sorted(worlds))];self.by={r['id']:r for r in self.rows}
        self.episodes={eid(seed,c):Episode(w,**c,admission=admission) for seed,w in worlds.items() for c in conditions(seed)} if stage=='S1' else {}
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
            for row in self.rows:self.call(row,clean_packet(self.worlds[row['seed']],row['actor'],row['kind'])[0],row['kind'])
            result=qualified(self.rows,self.worlds)
        else:
            for seed,w in self.worlds.items():
                cs=conditions(seed)
                es={eid(seed,c):self.episodes[eid(seed,c)] for c in cs}
                for slot in range(1,13):
                    for c in cs:
                        id=eid(seed,c);e=es[id]
                        if not self.active():break
                        n={'team':3,'single':1,'uniform':0}[c['policy']]
                        packets=[e.packet(actor) for actor in range(n)]  # Round barrier: freeze before first call.
                        group=[self.by[f'{id}-slot{slot}-{actor}'] for actor in range(n)]
                        for r,p in zip(group,packets):self.call(r,p,'choice')
                        if n and not any(r['status']!='not-started' for r in group):break
                        choices=[r.get('checked',{}).get('result',{}).get('choice') if r['status']=='valid' else None for r in group]
                        event=e.step(choices);self.journal('sensing',dict(episode=id,event=event))
                    if not self.active():break
                for c in cs:
                    id=eid(seed,c);e=es[id]
                    for row in (r for r in self.rows if r.get('episode')==id and r['kind']!='choice'):
                        if len(e.events)!=12:continue
                        packet=e.packet(row['actor']);packet['task']='Map the current terrain from the acquired evidence. UNKNOWN is legal when unresolved.'
                        if row['kind']=='yoked':packet['previous_proposals']=[];packet['actor']='fresh-yoked-judge'
                        self.call(row,packet,'map')
                self.save_episodes()
            result=contrasts(self.save_episodes())
        result.update(stage=self.stage,attempt=self.attempt,assigned=len(self.rows),started=sum(r['status']!='not-started' for r in self.rows),terminal=sum(r['status'] in ('valid','invalid','failed') for r in self.rows),valid=sum(r['status']=='valid' for r in self.rows),stop_reason=self.stop,budget=self.ledger.summary())
        result['usage_by_policy']={p:dict(calls=sum(r.get('policy','qualification')==p and r['status']!='not-started' for r in self.rows),valid=sum(r.get('policy','qualification')==p and r['status']=='valid' for r in self.rows),known_cost_usd=sum(r.get('checked',{}).get('usage',{}).get('cost',0) for r in self.rows if r.get('policy','qualification')==p),input_tokens=sum(r.get('checked',{}).get('usage',{}).get('input_tokens',0) for r in self.rows if r.get('policy','qualification')==p)) for p in sorted({r.get('policy','qualification') for r in self.rows})}
        self.persist();result['wall_seconds']=self.clock()-self.start
        save(self.out/'summary.json',result);return result
    def save_episodes(self):
        rows=[]
        for seed,w in self.worlds.items():
            for c in conditions(seed):
                id=eid(seed,c);e=self.episodes[id]
                records=[r for r in self.rows if r.get('episode')==id and r['kind']!='choice']
                rows.append(dict(c,id=id,seed=seed,family=w['family'],truth=w['truth'],report_cells=w['region'],order=e.order,uniform=e.uniform,events=e.events,endpoint=endpoint(e,records),packet=e.packet(),status='complete' if len(e.events)==12 and all(r['status'] in ('valid','invalid','failed') for r in records) else 'partial_or_unstarted'))
        save(self.out/'episodes.json',rows);return rows
