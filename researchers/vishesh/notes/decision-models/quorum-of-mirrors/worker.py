"""Single S0 worker on the exclusively allocated host; credentials remain in local relay."""
import argparse,csv,hashlib,html,json,os,time,urllib.request
from pathlib import Path
from qualification import manifest,validate_manifest,validate_response,analyze


def render(data,receipts,out):
    by_id={r['id']:r for r in receipts};rows=[]
    for a in data['assignments']:
        r=by_id.get(a['id']);choice='';status='unstarted'
        if r:
            status=r['status']
            if status=='complete':choice=validate_response(r['response'])['choice']
        rows.append([a['id'],a['expected'],status,choice])
    with (out/'matrix.csv').open('w') as f:
        w=csv.writer(f);w.writerow(['invocation','expected_MAP','status','choice']);w.writerows(rows)
    table=''.join('<tr>'+''.join('<td>'+html.escape(str(v))+'</td>' for v in row)+'</tr>' for row in rows)
    page='<!doctype html><meta charset="utf-8"><title>Quorum S0 competence</title><style>body{font:16px system-ui;max-width:950px;margin:40px auto}td,th{padding:7px 14px;text-align:left;border-bottom:1px solid #ddd}</style><h1>Quorum S0: evidence-reading qualification</h1><p>32 assigned calls; expected labels are exact MAP choices, not sampled world truth. Unstarted assignments remain visible. This is not a swarm efficacy experiment.</p><table><tr><th>Invocation</th><th>Expected MAP</th><th>Status</th><th>Actual choice</th></tr>'+table+'</table>'
    (out/'matrix.html').write_text(page)


def main():
    p=argparse.ArgumentParser();p.add_argument('--relay',required=True);p.add_argument('--launch',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);a=p.parse_args()
    if not a.relay.startswith('http://127.0.0.1:'):raise ValueError('loopback_required')
    launch=json.loads(a.launch.read_text());now=time.time()
    if launch['experiment']!='quorum-of-mirrors' or launch['host']!='sim-shadow' or not now<min(launch['claim_until'],launch['deadline']):
        raise ValueError('allocation_expired')
    if launch['api_cap_usd']!=1 or not launch['owner_approved']:raise ValueError('budget_missing')
    for name,expected in launch['source_sha256'].items():
        if hashlib.sha256(Path(name).read_bytes()).hexdigest()!=expected:raise ValueError('source_mismatch')
    from public_plan import check
    receipt=check('quorum-of-mirrors',launch['run_tldr'])
    if receipt['url']!=launch['public_plan_url'] or receipt['plan_sha256']!=launch['plan_sha256']:
        raise ValueError('public_plan_mismatch')
    a.out.mkdir(exist_ok=False);data=manifest();validate_manifest(data)
    (a.out/'manifest.json').write_text(json.dumps(data,indent=2));(a.out/'public-plan-receipt.json').write_text(json.dumps(receipt,indent=2))
    receipts=[];render(data,receipts,a.out)
    import swarm_report as sr
    run=sr.start('quorum-of-mirrors',run='quorum-of-mirrors/qm-s0-01',params={'stage':'S0','calls':32,'condition':'explicit-lineage-skewed-repeat'},message=launch['run_tldr'])
    for row in data['assignments']:
        if time.time()>min(launch['deadline'],launch['claim_until']):break
        record={'id':row['id'],'request_sha256':row['request_sha256'],'status':'failed'};start=time.monotonic()
        try:
            payload=json.dumps({'id':row['id'],'request':row['request']}).encode()
            with urllib.request.urlopen(urllib.request.Request(a.relay,payload,{'Content-Type':'application/json'}),timeout=40) as r:
                reply=json.load(r)
            if not reply.get('ok'):
                record.update(reason=reply.get('reason','relay_failed'),http_status=reply.get('http_status'))
            else:
                validate_response(reply['response']);record.update(status='complete',response=reply['response'])
        except Exception as exc:record['reason']=type(exc).__name__
        record['wall_s']=time.monotonic()-start;receipts.append(record)
        with (a.out/'receipts.jsonl').open('a') as f:
            f.write(json.dumps(record)+'\n');f.flush();os.fsync(f.fileno())
        s=analyze(data,receipts);render(data,receipts,a.out)
        run.progress(len(receipts),32,force=True,valid=s['valid'],correct=s['correct'],unstarted=s['unstarted'])
        if record['status']!='complete':break
    summary=analyze(data,receipts);summary['actual_api_usd']=sum(r.get('response',{}).get('usage',{}).get('cost',0) for r in receipts)
    summary['execution_complete']=len(receipts)==32 and summary['failed']==0
    (a.out/'summary.json').write_text(json.dumps(summary,indent=2));render(data,receipts,a.out)
    for path in a.out.iterdir():run.artifact(str(path),name=path.name)
    if summary['qualified']:run.done(message='S0 competence passed; no swarm efficacy conclusion',correct=summary['correct'],valid=summary['valid'])
    else:run.fail(message='S0 qualification failed; retained all assigned outcomes',correct=summary['correct'],valid=summary['valid'])
    print(json.dumps(summary),flush=True)

if __name__=='__main__':
    try:main()
    except Exception as exc:
        print('Worker stopped: '+type(exc).__name__,flush=True);raise SystemExit(1)
