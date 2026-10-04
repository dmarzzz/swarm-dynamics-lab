"""C4 native definitions, admission and incremental budget. No inference on import."""
import sys,json,hashlib,subprocess,time,sqlite3
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'src'))
sys.path.append(str(HERE.parent/'practical'))
from jev import request,validate,RATE,RESERVE
from jev_relay import NoRedirect,RESERVE_NANO
from providers import QWEN_DIGEST
from contract import admit,LIMITS
from scenarios import assignments
ATTEMPT='C4';UPSTREAM_TIMEOUT=60;LEDGER_CALL_CAP=2671
wire=lambda x:json.dumps(x,separators=(',',':')).encode()
digest=lambda x:hashlib.sha256(wire(x)).hexdigest()

def payloads(stage):return {digest(request(r,i,'C4-'+stage)):request(r,i,'C4-'+stage) for i,r in enumerate(assignments(stage))}

def reserve(db,h,max_calls=2671,settle=True):
    db.execute('BEGIN IMMEDIATE')
    try:
        db.execute('CREATE TABLE IF NOT EXISTS c4_hashes(hash TEXT PRIMARY KEY)')
        n,total=db.execute('SELECT count(*),coalesce(sum(CASE WHEN status="completed" THEN round(cost*1000000000) ELSE reserved END),0) FROM calls').fetchone()
        own=db.execute('SELECT coalesce(sum(CASE WHEN c.status="completed" THEN round(c.cost*1000000000) ELSE c.reserved END),0) FROM calls c JOIN c4_hashes h ON h.hash=c.hash').fetchone()[0]
        if n<2179 or n>=max_calls or total+RESERVE_NANO>100000000 or own+RESERVE_NANO>30000000:raise RuntimeError('budget_exhausted')
        db.execute('INSERT INTO calls(hash,reserved,status) VALUES(?,?,?)',(h,RESERVE_NANO,'started'));db.execute('INSERT INTO c4_hashes VALUES(?)',(h,));db.commit()
    except BaseException:db.rollback();raise

def sources(commit):
    root=Path(subprocess.check_output(['git','rev-parse','--show-toplevel'],cwd=HERE,text=True).strip());out={}
    paths=list(HERE.glob('*.py'))+[HERE.parent/'src'/n for n in ('jev.py','jev_relay.py','providers.py')]+[HERE.parent/'practical/reporting.py',HERE.parent.parent/'experiment-documentation/public_plan.py']
    for p in paths:
        rel=str(p.relative_to(root));expected=subprocess.check_output(['git','show',commit+':'+rel],cwd=root)
        if expected!=p.read_bytes():raise ValueError('source_mismatch')
        out[rel]=hashlib.sha256(expected).hexdigest()
    return out

def preflight(a,stage,parent=None,public_check=None):
    plan_hash=hashlib.sha256((HERE/'PLAN.md').read_bytes()).hexdigest()
    admit(a,stage,plan_hash,time.time())
    hashes=sources(a['source_commit'])
    if digest(hashes)!=a['scientific_hash']:raise ValueError('source_receipt_mismatch')
    approval=json.loads((HERE/'owner-approval.json').read_text())
    if approval.get('status')!='approved' or approval.get('plan_sha256')!=plan_hash:raise ValueError('owner_approval_missing')
    if public_check is None:
        sys.path.insert(0,str(HERE.parent.parent/'experiment-documentation'));from public_plan import check;public_check=check
    tldr=f'TLDR: C4-{stage} option-order agreement referral versus always-Jev, Qwen-only and same-count random referral; measure absolute error, missed errors and derived consultations on synthetic report families.'
    receipt=public_check('healing-helping-hands',tldr)
    if receipt['url']!=a['plan_url'] or receipt['plan_sha256']!=plan_hash or receipt['commit']!=a['source_commit'] or not receipt['url'].endswith('/c4/PLAN.md'):raise ValueError('wrong_registered_plan')
    if stage=='S1':
        if parent is None:raise ValueError('qualification_required')
        pm=json.loads((parent/'manifest.json').read_text());q=json.loads((parent/'qualification.json').read_text())
        if pm['status']!='completed' or not q['qualified'] or pm['source_hashes']!=hashes:raise ValueError('unqualified_instrument')
    return hashes,receipt,tldr
