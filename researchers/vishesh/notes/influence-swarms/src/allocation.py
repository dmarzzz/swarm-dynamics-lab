from contextlib import closing
"""Non-overlapping quota leases. Run reservation on the existing budget authority.

No key material is read. A lease is never silently refunded or copied to another host.
The operator separately verifies the merged exclusive fleet claim immediately before launch.
"""
import argparse,datetime,json,os,socket,sqlite3
from pathlib import Path

class AllocationError(Exception):pass

def reserve(authority,lease_id,host,claim,until,amount):
    if not 0<amount<=8:raise AllocationError('quota outside authorized repair envelope')
    if not Path(authority).is_file():raise AllocationError('existing authority required')
    with closing(sqlite3.connect(authority,timeout=20)) as db, db:
        db.execute('BEGIN IMMEDIATE')
        db.execute('CREATE TABLE IF NOT EXISTS allocations (id TEXT PRIMARY KEY, receipt TEXT)')
        old=db.execute('SELECT receipt FROM allocations WHERE id=?',(lease_id,)).fetchone()
        receipt={'lease_id':lease_id,'experiment':'influence-swarms','host':host,'claim':claim,'exclusive':True,'until':until,'cap_usd':amount}
        if old:
            if json.loads(old[0])!=receipt:raise AllocationError('lease already bound differently')
            return receipt
        cap,used=db.execute('SELECT cap,reserved FROM budget WHERE id=1').fetchone()
        if used+amount>cap:raise AllocationError('shared budget exhausted')
        db.execute('UPDATE budget SET reserved=reserved+? WHERE id=1',(amount,))
        db.execute('INSERT INTO allocations VALUES (?,?)',(lease_id,json.dumps(receipt)))
    return receipt

def validate(receipt,host,now):
    if receipt.get('experiment')!='influence-swarms' or receipt.get('host')!=host or receipt.get('exclusive') is not True or not receipt.get('claim'):raise AllocationError('dedicated allocation mismatch')
    if not 0<receipt.get('cap_usd',0)<=8:raise AllocationError('invalid subquota')
    if datetime.datetime.fromisoformat(receipt['until'].replace('Z','+00:00'))<=now:raise AllocationError('allocation expired')
    return receipt

def require(config):
    path=os.environ.get('SWARM_ALLOCATION_RECEIPT')
    if not path:raise AllocationError('exclusive allocation receipt required')
    receipt=validate(json.loads(Path(path).read_text()),socket.gethostname(),datetime.datetime.now(datetime.timezone.utc))
    if config['total_api_cap_usd']!=receipt['cap_usd']:raise AllocationError('quota config mismatch')
    if not os.environ.get('SWARM_BUDGET_LEDGER'):raise AllocationError('host subquota ledger required')
    return receipt

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--authority',required=True);p.add_argument('--lease-id',required=True);p.add_argument('--host',required=True);p.add_argument('--claim',required=True);p.add_argument('--until',required=True);p.add_argument('--amount',type=float,default=8);a=p.parse_args()
    print(json.dumps(reserve(a.authority,a.lease_id,a.host,a.claim,a.until,a.amount)))
