"""Allowlisted, durable child phase events; no exception text or observation payloads."""
import json,math,os,time
from pathlib import Path

PHASES=('worker_start','imports_begin','imports_end','reader_init_begin','reader_init_end',
        'ocr_begin','ocr_end','extract_begin','extract_end','output_begin','output_end')

class Phases:
    def __init__(self,path):
        self.fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
        self.started=time.monotonic();self.index=0
    def emit(self,phase):
        if self.index>=len(PHASES) or phase!=PHASES[self.index]:
            raise ValueError('invalid_phase_sequence')
        event={'seq':self.index,'phase':phase,'elapsed_s':time.monotonic()-self.started}
        data=(json.dumps(event)+'\n').encode()
        while data:
            n=os.write(self.fd,data);data=data[n:]
        os.fsync(self.fd);self.index+=1
    def close(self):
        os.close(self.fd)


def inspect_phases(path,complete):
    """Partial final bytes are retained privately; never promoted to a complete event."""
    p=Path(path)
    if not p.exists() or p.is_symlink() or not p.is_file():return {'valid':False,'complete':False,'last_phase':None,'events':[],'tail_incomplete':False}
    raw=p.read_bytes();lines=raw.splitlines(keepends=True);tail=bool(lines and not lines[-1].endswith(b'\n'))
    if tail:lines=lines[:-1]
    events=[];valid=True
    for line in lines:
        try:
            e=json.loads(line);i=len(events)
            if set(e)!= {'seq','phase','elapsed_s'} or type(e['seq']) is not int or e['seq']!=i or i>=len(PHASES) or e['phase']!=PHASES[i]:raise ValueError()
            x=e['elapsed_s']
            if type(x) not in (int,float) or not math.isfinite(x) or x<0 or events and x<events[-1]['elapsed_s']:raise ValueError()
            events.append({'seq':i,'phase':PHASES[i],'elapsed_s':x})
        except (ValueError,TypeError,KeyError,UnicodeError):valid=False;break
    done=valid and not tail and len(events)==len(PHASES)
    valid=valid and bool(events) and (not complete or done)
    return {'valid':valid,'complete':done,'last_phase':events[-1]['phase'] if events else None,'events':events,'tail_incomplete':tail}
