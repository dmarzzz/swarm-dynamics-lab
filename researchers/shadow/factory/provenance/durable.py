"""Create-once evidence and compatible cumulative reservation ledgers."""
from contextlib import contextmanager
from datetime import datetime,timezone
import fcntl
import hashlib
import json
import math
import os
from pathlib import Path
import tempfile


def now(): return datetime.now(timezone.utc).isoformat()
def sha(path): return hashlib.sha256(Path(path).read_bytes()).hexdigest()
def read(path): return json.loads(Path(path).read_text())


def immutable(path,value):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    data=(json.dumps(value,sort_keys=True,indent=2,allow_nan=False)+'\n').encode()
    fd,temp=tempfile.mkstemp(prefix='.pending-',dir=path.parent)
    try:
        with os.fdopen(fd,'wb') as h:
            h.write(data);h.flush();os.fsync(h.fileno())
        os.link(temp,path)  # atomic, fails if the unique ID already exists
        dfd=os.open(path.parent,os.O_RDONLY)
        try: os.fsync(dfd)
        finally: os.close(dfd)
    finally:
        os.unlink(temp)
    return sha(path)


@contextmanager
def locked(path):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('a+') as h:
        fcntl.flock(h,fcntl.LOCK_EX)
        yield h


def append_locked(h,row):
    h.seek(0,2);h.write(json.dumps(row,sort_keys=True,allow_nan=False)+'\n');h.flush();os.fsync(h.fileno())


class BudgetStop(RuntimeError): pass


class PaidLedger:
    """Same file/schema as the pre-existing factory ledger, no new allowance.

    Lock the actual ledger inode, not a separate per-adapter lock file. Historical
    unresolved reservations retain full liability. Caller IDs include cohort.
    """
    def __init__(self,path):self.path=Path(path)

    def _state(self,h):
        h.seek(0);reserves={};settled={}
        for line in h:
            e=json.loads(line);key=(e['spec'],e['call']);v=e['usd']
            if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise BudgetStop('invalid_ledger_cost')
            if e['kind']=='reserve':
                if key in reserves:raise BudgetStop('duplicate_ledger_reservation')
                reserves[key]=v
            elif e['kind']=='settle':
                if key not in reserves or key in settled:raise BudgetStop('invalid_ledger_settlement')
                settled[key]=v
            else:raise BudgetStop('invalid_ledger_event')
        return reserves,settled

    def reserve(self,spec,call,usd):
        if type(usd) not in (int,float) or not math.isfinite(usd) or usd<0:raise BudgetStop('invalid_cost')
        with locked(self.path) as h:
            rs,ss=self._state(h);key=(spec,call)
            if key in rs:raise BudgetStop('duplicate_paid_reservation')
            liabilities={k:ss.get(k,v) for k,v in rs.items()}
            if sum(liabilities.values())+usd>20+1e-10:raise BudgetStop('factory_cap')
            if sum(v for k,v in liabilities.items() if k[0]==spec)+usd>4+1e-10:raise BudgetStop('spec_cap')
            append_locked(h,dict(kind='reserve',spec=spec,call=call,usd=usd,time=now()))

    def settle(self,spec,call,usd):
        if type(usd) not in (int,float) or not math.isfinite(usd) or usd<0:raise BudgetStop('invalid_actual_cost')
        with locked(self.path) as h:
            rs,ss=self._state(h);key=(spec,call)
            if key not in rs or key in ss:raise BudgetStop('invalid_settlement')
            append_locked(h,dict(kind='settle',spec=spec,call=call,usd=usd,time=now()))
            if usd>rs[key]+1e-10:raise BudgetStop('liability_envelope_breached')

    def liability(self,spec=None):
        if not self.path.exists():return 0
        with locked(self.path) as h:
            rs,ss=self._state(h)
            return sum(ss.get(k,v) for k,v in rs.items() if spec is None or k[0]==spec)
