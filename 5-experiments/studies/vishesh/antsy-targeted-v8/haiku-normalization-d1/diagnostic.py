"""Bounded used-case normalization diagnostic; never a fresh qualification."""
import sys,json,time,os,concurrent.futures,argparse
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'haiku-panel-v1/src'))
import design,run
from experiment_ops.trace_receipts import KINDS,retain,audit
EXTRA=" This receipt is from an Indonesian receipt corpus. Interpret amounts in the original currency's major units. A period separating a final group of three digits is commonly a thousands separator, not a decimal point. Preserve the full amount when removing grouping separators. Use the receipt's labels and consistent number formatting; refer if the convention remains ambiguous."
ATTEMPT='D1-normalization-attempt-1'
def prepare(inputs,out):
    out.mkdir(mode=0o700,exist_ok=False);rows=[];allowed={}
    for c in json.loads((inputs/'cases.json').read_text()):
        if c['stage']!='Q0':continue
        im=inputs/'images'/c['image'];assert design.sha(im)==c['image_sha256']
        for repeat in range(4):
            for arm in ('original','locale'):
                p=design.request(im.read_bytes(),1)
                if arm=='locale':p['messages'][1]['content'][0]['text']+=EXTRA
                identity=f'D1-{c["id"]}-{repeat}-{arm}';allowed[identity]=design.digest(p)
                (out/(identity+'.json')).write_text(json.dumps(p))
                rows.append({'id':identity,'unit':c['id'],'arm':arm,'gold':c['gold'],'payload_sha256':allowed[identity]})
    assert len(rows)==16
    (out/'rows.json').write_text(json.dumps(rows));(out/'allowlist.json').write_text(json.dumps(allowed))
    return {'assignments':16,'rows_sha256':design.sha(out/'rows.json'),'allowlist_sha256':design.sha(out/'allowlist.json')}
def collect(packet,out,cap,port):
    import swarm_report as sr
    rows=json.loads((packet/'rows.json').read_text());assert len(rows)==16
    out.mkdir(mode=0o700,exist_ok=False);(out/'private').mkdir()
    source=design.digest({p.name:design.sha(p) for p in sorted(HERE.glob('*')) if p.is_file()})
    manifest={'schema_version':1,'study':'antsy-targeted-v8','attempt':ATTEMPT,'source_sha256':source,'config_sha256':design.sha(packet/'allowlist.json'),'assignments':[{k:r[k] for k in ('id','unit','arm')} for r in rows],'calls':[{'assignment':r['id'],'call_id':None,'status':'unstarted','artifacts':{}} for r in rows]}
    def save():run.save(out/'trace-manifest.json',manifest)
    def blob(v):
        x=retain(out/'private/blobs',json.dumps(v,sort_keys=True).encode());x['path']='private/blobs/'+x['path'];return x
    save();records=[];stop='completed';started=time.monotonic()
    sr.report('start',experiment=run.EXP,run=run.EXP+'/'+ATTEMPT,step=0,total=16,message='Used-case locale diagnostic; not fresh qualification')
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:
            for offset in range(0,16,2):
                if time.monotonic()-started>540:stop='deadline';break
                batch=[]
                for i in range(offset,offset+2):
                    r=rows[i];p=json.loads((packet/(r['id']+'.json')).read_text());assert design.digest(p)==r['payload_sha256']
                    a={k:{'absent':'not_reached'} for k in KINDS}
                    for k in ('transition','stdout','stderr'):a[k]={'absent':'not_applicable'}
                    a['input']=blob(p);a['context']=blob({'fresh_context':True,'arm':r['arm'],'request_sha256':r['payload_sha256'],'model':design.MODEL,'provider':design.PROVIDER})
                    manifest['calls'][i].update(call_id=r['id'],status='started',artifacts=a);save()
                    batch.append((i,time.monotonic(),pool.submit(run.invoke,'http://127.0.0.1:'+str(port)+'/antsy',cap,r['id'],p)))
                for i,t,f in batch:
                    try:v=f.result()
                    except Exception:v={'error':'relay_connection_failure','parsed':None,'usage':None,'actual_usd':None}
                    r=rows[i];a=manifest['calls'][i]['artifacts'];a['response']=blob(v);a['phases']=blob({'start':t,'end':time.monotonic()})
                    if v.get('parsed') is not None:a['parsed']=blob(v['parsed'])
                    a['usage']=blob({'usage':v['usage'],'actual_usd':v['actual_usd']}) if v.get('usage') else {'absent':'not_collected'}
                    correct=bool(v.get('parsed') and v['parsed']['decision']=='accept' and v['parsed']['amount']==r['gold'])
                    a['grade']=blob({'correct':correct});manifest['calls'][i]['status']='failed' if v.get('error') else 'valid';save()
                    records.append({'id':r['id'],'case':r['unit'],'arm':r['arm'],'correct':correct,**v});run.save(out/'private/records.json',records)
                    if v.get('error'):stop=v['error']
                if stop!='completed':break
    finally:
        coverage=audit(out,'antsy-targeted-v8',ATTEMPT)
        if coverage['status']!='verified_declared_coverage' and stop=='completed':stop='trace_gap'
        counts=[{'case':case,'arm':arm,'n':sum(r['case']==case and r['arm']==arm for r in records),'correct':sum(r['case']==case and r['arm']==arm and r['correct'] for r in records)} for case in sorted({r['unit'] for r in rows}) for arm in ('original','locale')]
        summary={'attempt':ATTEMPT,'started':len(records),'assigned':16,'valid':sum(not r.get('error') for r in records),'stop':stop,'trace_status':coverage['status'],'actual_usd':sum(r.get('actual_usd') or 0 for r in records),'counts':counts,'repair_supported_on_used_cases':stop=='completed' and all(r['correct']==4 for r in counts if r['arm']=='locale'),'fresh_qualification_passed':False}
        run.save(out/'summary.json',summary);run.save(out/'trace-audit.json',coverage)
        for name in ('summary.json','trace-audit.json'):sr.upload(run.EXP+'/'+ATTEMPT,out/name,name=name)
        sr.report('done' if stop=='completed' else 'fail',experiment=run.EXP,run=run.EXP+'/'+ATTEMPT,step=len(records),total=16,metrics={'valid':summary['valid'],'cost_usd':summary['actual_usd']},message='Used-case diagnostic complete; original evaluation remains blocked')
    print(json.dumps(summary))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('operation',choices=['prepare','collect']);p.add_argument('--inputs',type=Path);p.add_argument('--packet',type=Path,required=True);p.add_argument('--out',type=Path);p.add_argument('--capability',type=Path);p.add_argument('--port',type=int);a=p.parse_args()
    if a.operation=='prepare':print(json.dumps(prepare(a.inputs,a.packet)))
    else:collect(a.packet,a.out,a.capability.read_text().strip(),a.port)
