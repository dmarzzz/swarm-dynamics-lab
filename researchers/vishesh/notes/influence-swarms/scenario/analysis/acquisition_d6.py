"""D6 offline-qualified acquisition primitive; no CLI or credential lookup.

A future admitted launcher must bind exact wire requests, source, public plan,
allocation and validator. This module cannot approve a run or create a budget.
"""
import hashlib,json,math,os,re,sqlite3,threading,urllib.error
from contextlib import closing
from pathlib import Path

MAX_REQUESTS=2
MAX_RESERVATION=.048640
SAFE_ID=re.compile(r'(?:req|request)_[A-Za-z0-9]{8,64}\Z')
class AcquisitionStopped(Exception):pass

def safe_http(exc):
    h=exc.headers or {};value=h.get('retry-after','');rid=h.get('request-id','')
    retry_after=int(value) if isinstance(value,str) and value.isascii() and value.isdigit() and len(value)<=5 and int(value)<=86400 else None
    return {'category':'http','http_status':exc.code if type(exc.code) is int and 100<=exc.code<=599 else None,
            'retry_after_seconds':retry_after,'request_id':rid if isinstance(rid,str) and SAFE_ID.fullmatch(rid) else None,
            'retry_permitted':False}

def usage(result):
    u=result.get('usage') if isinstance(result,dict) else None
    if not isinstance(u,dict) or any(type(u.get(k)) is not int or not 0<=u[k]<=10_000_000 for k in ('input_tokens','output_tokens')):return None
    return {k:u[k] for k in ('input_tokens','output_tokens')}

class Session:
    def __init__(self,directory,ledger):
        self.directory=Path(directory);self.ledger=Path(ledger)
        if not self.ledger.is_file():raise AcquisitionStopped('existing_ledger_required')
        # mkdir is the exclusive session claim. Existing/inflight journals cannot reopen.
        try:self.directory.mkdir(mode=0o700)
        except FileExistsError:raise AcquisitionStopped('prior_session_preserved') from None
        self.count=0;self.stopped=False;self.lock=threading.Lock();self._state('ready');self._event({'kind':'session','maximum_attempts':MAX_REQUESTS,'retries':0})
    def _state(self,status):
        p=self.directory/'state.json';tmp=self.directory/'state.tmp'
        with tmp.open('w') as f:json.dump({'state':status,'attempts':self.count,'unstarted':MAX_REQUESTS-self.count},f);f.flush();os.fsync(f.fileno())
        os.replace(tmp,p)
        fd=os.open(self.directory,os.O_RDONLY)
        try:os.fsync(fd)
        finally:os.close(fd)
    def _event(self,event):
        with (self.directory/'events.jsonl').open('a') as f:f.write(json.dumps(event,allow_nan=False)+'\n');f.flush();os.fsync(f.fileno())
    def _artifact(self,kind,raw):
        name=f'{self.count:02d}-{kind}.bin';path=self.directory/name
        fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o600)
        with os.fdopen(fd,'wb') as f:f.write(raw);f.flush();os.fsync(f.fileno())
        directory_fd=os.open(self.directory,os.O_RDONLY)
        try:os.fsync(directory_fd)
        finally:os.close(directory_fd)
        reference={'name':name,'bytes':len(raw),'sha256':hashlib.sha256(raw).hexdigest()}
        self._event({'kind':kind+'_artifact','attempt':self.count,**reference})
        return reference
    def _stop(self,detail):
        self.stopped=True
        self._event({'kind':'failure','attempt':self.count,**detail,'usage_known':False,'actual_usd':None,'retry_permitted':False})
        self._state('stopped');raise AcquisitionStopped(detail['category'])
    def dispatch(self,*args,**kwargs):
        with self.lock:
            try:return self._dispatch(*args,**kwargs)
            except BaseException:
                self.stopped=True
                raise
    def _dispatch(self,encoded,transport,validate,reservation,input_rate=1.,output_rate=5.):
        if json.loads((self.directory/'state.json').read_text())['state']!='ready':raise AcquisitionStopped('not_ready')
        if self.stopped or self.count>=MAX_REQUESTS:raise AcquisitionStopped('circuit_open_or_complete')
        if not isinstance(encoded,bytes) or len(encoded)>32768:raise AcquisitionStopped('request_bound')
        if type(reservation) not in (int,float) or not math.isfinite(reservation) or not 0<reservation<=MAX_RESERVATION:raise AcquisitionStopped('reservation_bound')
        if input_rate!=1. or output_rate!=5.:raise AcquisitionStopped('unapproved_rate')
        minimum=((len(encoded)+512)*input_rate+3072*output_rate)/1e6
        if reservation+1e-12<minimum:raise AcquisitionStopped('insufficient_reservation')
        # Existing database only. Reservation is irrevocable, including later journal failure.
        with closing(sqlite3.connect(f'file:{self.ledger}?mode=rw',uri=True,timeout=20)) as db, db:
            db.execute('BEGIN IMMEDIATE')
            cap,used,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
            if cap!=8 or used<4.868832-1e-8 or calls<246 or used+reservation>cap:
                self.stopped=True;self._state('budget_stopped');raise AcquisitionStopped('budget_lineage_or_capacity')
            db.execute('UPDATE budget SET reserved=?,calls=? WHERE id=1',(used+reservation,calls+1))
        self.count+=1;self._state('inflight')
        request_ref=self._artifact('request',encoded)
        self._event({'kind':'attempt_start','attempt':self.count,'reserved_usd':reservation,'retry_permitted':False,'request':request_ref})
        try:raw=transport(encoded)
        except urllib.error.HTTPError as e:self._stop(safe_http(e))
        except TimeoutError:self._stop({'category':'timeout'})
        except Exception:self._stop({'category':'transport'})
        if not isinstance(raw,bytes) or len(raw)>1_000_000:self._stop({'category':'response_bound'})
        self._artifact('response',raw)
        try:result=json.loads(raw)
        except Exception:self._stop({'category':'parse'})
        measured=usage(result)
        if measured is None:self._stop({'category':'missing_or_invalid_usage'})
        cost=(measured['input_tokens']*input_rate+measured['output_tokens']*output_rate)/1e6
        # Preserve known usage even if output validation fails; diagnostic logs contain no body.
        self._event({'kind':'usage','attempt':self.count,'usage_known':True,'tokens':measured,'reported_usd':cost})
        if not isinstance(result,dict) or result.get('stop_reason')!='end_turn':
            self.stopped=True;self._event({'kind':'failure','attempt':self.count,'category':'incomplete_output','usage_known':True,'actual_usd':cost,'retry_permitted':False});self._state('stopped');raise AcquisitionStopped('incomplete_output')
        try:answer=validate(result)
        except Exception:
            self.stopped=True;self._event({'kind':'failure','attempt':self.count,'category':'contract','usage_known':True,'actual_usd':cost,'retry_permitted':False});self._state('stopped');raise AcquisitionStopped('contract') from None
        self._event({'kind':'response_validated','attempt':self.count,'usage_known':True,'actual_usd':cost})
        self._state('complete' if self.count==MAX_REQUESTS else 'ready')
        return answer
