"""Six-call recovery of a known returned fault. No provider or credentials."""
import hashlib,json,sqlite3,sys,datetime
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'r41'))
import cases as c,instrument as i,runtime as r
CASE='r40-development-unit_price-3'
FAILED='truthful/large-commercial-11/initial'
NODES=(FAILED,'truthful/large-commercial-00/revision','truthful/large-commercial-10/revision','truthful/large-commercial-11/revision','truthful/lead-commercial','truthful/large-final')
MAX_CALLS=6;MAX_COST=.034176

def restore(cases,records,failed_request,failed_response):
    rows=[x for x in records if x['case_id']==CASE]
    r.require(len(rows)==1 and rows[0]['repetition']==0,'one_original_root')
    case=next(x for x in cases if x['id']==CASE);root=i.Root(case,0,('truthful',))
    original=rows[0];r.require([x['id'] for x in original['nodes']]==[n['id'] for n in root.nodes],'node_assignment')
    missing=[]
    for entry in original['nodes']:
        if entry['state']=='valid':root.accept(root.item(entry['id']),entry['answer'])
        else:
            expected='format_failed' if entry['id']==FAILED else 'blocked'
            r.require(entry['state']==expected and entry['answer'] is None,'original_failure_state');missing.append(entry['id'])
    r.require(tuple(missing)==NODES,'only_known_branch')
    item=root.item(FAILED);r.require(c.encoded(item['wire'])==failed_request,'identical_failed_request')
    _,_,fault=r.response(failed_response,case,item['node']);r.require(fault=='length','known_returned_length_only')
    return root

def reserve(ledger,attempt,source,manifest,node,wirehash,until):
    r.require(node in NODES,'recovery_node')
    r.require(datetime.datetime.now(datetime.timezone.utc)+datetime.timedelta(seconds=90)<r.utc(until),'deadline')
    with r.database(ledger) as db:
        db.execute('BEGIN IMMEDIATE')
        g=db.execute('SELECT source,manifest,max_calls,maximum,used_calls,reserved,status FROM r42_scope WHERE attempt=?',(attempt,)).fetchone()
        r.require(g and g[0:2]==(source,manifest) and g[2]==MAX_CALLS and abs(g[3]-MAX_COST)<1e-10 and g[6]=='funded','finite_source_grant')
        r.require(g[4]<g[2] and g[5]+i.RESERVATION<=g[3]+1e-10,'grant_exhausted')
        cap,total,count=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
        r.require(cap==50 and total+i.RESERVATION<=cap,'original_ceiling')
        ordinal=g[4]+1
        db.execute('INSERT INTO r42_work VALUES(?,?,?,?,?,?,NULL)',(attempt,node,ordinal,wirehash,i.RESERVATION,'reserved_unknown'))
        db.execute('UPDATE r42_scope SET used_calls=used_calls+1,reserved=reserved+? WHERE attempt=?',(i.RESERVATION,attempt))
        db.execute('UPDATE budget SET reserved=reserved+?,calls=calls+1 WHERE id=1',(i.RESERVATION,))
        return ordinal

class Continuation:
    def __init__(self,root,out,ledger,attempt,source,manifest,until):
        self.root=root;self.out=Path(out);self.out.mkdir(mode=0o700);self.ledger=ledger;self.attempt=attempt;self.source=source;self.manifest=manifest;self.until=until
    def run(self,transport):
        failure=None;started=0;valid=0
        for node in NODES:
            try:
                item=self.root.item(node);raw=c.encoded(item['wire'])
                ordinal=reserve(self.ledger,self.attempt,self.source,self.manifest,node,item['wire_sha256'],self.until);started+=1
                r.save(self.out/f'{ordinal:04d}-request.bin',raw)
                r.save(self.out/f'{ordinal:04d}-assignment.json',{'node':item['node'],'parent_hashes':item['parent_hashes'],'context_sha256':item['context_sha256'],'wire_sha256':item['wire_sha256'],'is_retry':node==FAILED})
                response=transport(raw,node);r.save(self.out/f'{ordinal:04d}-response.bin',response)
                body,answer,fault=r.response(response,self.root.case,item['node'])
                with r.database(self.ledger) as db:db.execute('UPDATE r42_work SET status=?,cost=? WHERE attempt=? AND node=?',('known_format_failure' if fault else 'validated',body['usage']['cost'],self.attempt,node))
                if fault:self.root.fail(item,fault);failure=fault;break
                self.root.accept(item,answer);valid+=1;r.save(self.out/f'{ordinal:04d}-validated.json',answer)
            except Exception as e:
                failure=str(e) if isinstance(e,r.Stop) else type(e).__name__;break
        record=self.root.export();r.save(self.out/'recovered-root.json',record)
        with r.database(self.ledger) as db:
            rows=db.execute('SELECT status,cost FROM r42_work WHERE attempt=?',(self.attempt,)).fetchall()
            db.execute("UPDATE r42_scope SET status='closed' WHERE attempt=?",(self.attempt,))
        result={'attempt':self.attempt,'assigned_new_nodes':6,'started':started,'valid_new':valid,'failure':failure,'complete':valid==6,'unknown_usage':sum(cost is None for _,cost in rows),'known_cost':sum(cost for _,cost in rows if cost is not None),'retained_reservation':len(rows)*i.RESERVATION,'retry_calls':int(started>0),'original_first_pass_qualification':'failed','interpretation':'recovery-assisted; imported reports are not fresh samples'}
        r.save(self.out/'summary.json',result);return record,result
