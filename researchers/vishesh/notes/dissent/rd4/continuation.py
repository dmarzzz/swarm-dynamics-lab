"""Unstarted-only continuation. Never retries or rewrites terminal parent outcomes."""
import argparse,hashlib,json,os,sys,time,urllib.request,urllib.error
from pathlib import Path
BASE=Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent/'src'))
from cases import digest
from rd4_design import assignments,trajectories,execute,wire,frozen_requests
from rd4_worker import verify,analyze,EXPERIMENT
from live_worker import NativePolicy,save,quiet

PARENT_FILES=('configuration.json','manifest.json','records.json','calls.json','summary.json')
def transport_healthy():
    try:
        with urllib.request.urlopen('http://127.0.0.1:18449/',timeout=3):return False
    except urllib.error.HTTPError as e:
        healthy=e.code==501;e.close();return healthy
    except (OSError,ValueError):return False

def partition(manifest,records):
    original=assignments('S4');expected=[(a['case_id'],a['arm']) for a in original]
    actual=[(a['case_id'],a['arm']) for a in manifest['assignments']]
    if actual!=expected:raise ValueError('parent_assignment_changed')
    terminals=set();pending=[]
    for x in manifest['assignments']:
        key=(x['case_id'],x['arm'])
        if x['status']=='terminal':terminals.add(key)
        elif x['status']=='planned':pending.append(dict(x))
        else:raise ValueError('ambiguous_parent_assignment')
    by={}
    for r in records:by.setdefault((r['case_id'],r['arm']),[]).append(r)
    if set(by)!=terminals:raise ValueError('parent_terminal_mismatch')
    for rows in by.values():
        if [r['epoch'] for r in rows]!=list(range(4)):raise ValueError('parent_epoch_mismatch')
    return pending

def combine(parent,added):
    by={}
    for r in parent+added:
        key=(r['case_id'],r['arm'],r['epoch'])
        if key in by:raise ValueError('duplicate_terminal_row')
        by[key]=r
    order=[(a['case_id'],a['arm'],i) for a in assignments('S4') for i in range(4)]
    if set(by)-set(order):raise ValueError('unknown_terminal_row')
    return [by[k] for k in order if k in by]

def annotate(out,segments):
    from PIL import Image,ImageDraw
    from live_render import font,MUTED
    label='Combined cohort: '+' + '.join(segments)+'; prior failures retained.'
    p=out/'final_frame.png';im=Image.open(p).convert('RGB');ImageDraw.Draw(im).text((70,175),label,font=font(22),fill=MUTED);im.save(p)
    p=out/'measured_replay.gif'
    if p.exists():
        frames=[]
        with Image.open(p) as gif:
            for i in range(gif.n_frames):
                gif.seek(i);im=gif.convert('RGB');ImageDraw.Draw(im).text((70,175),label,font=font(22),fill=MUTED);frames.append(im)
        frames[0].save(p,save_all=True,append_images=frames[1:],duration=1100,loop=1,optimize=False)

def main(a):
    config=json.loads(a.config.read_text());parent=Path(config['parent_directory'])
    for name,h in config['parent_sha256'].items():
        if name not in PARENT_FILES or hashlib.sha256((parent/name).read_bytes()).hexdigest()!=h:raise ValueError('parent_hash_mismatch')
    for file,h in config['continuation_file_hashes'].items():
        if hashlib.sha256(Path(file).read_bytes()).hexdigest()!=h:raise ValueError('continuation_source_mismatch')
    previous={name:json.loads((parent/name).read_text()) for name in PARENT_FILES}
    pending=partition(previous['manifest.json'],previous['records.json'])
    if digest(pending)!=config['continuation_assignment_sha256'] or len(pending)!=config.get('expected_pending_trajectories',40):raise ValueError('continuation_assignment_mismatch')
    total=len(pending)*4;segment=config.get('continuation_stage','S4-C1');segments=config.get('execution_segments',['S4-A1','S4-C1'])
    receipt=verify(config,'S4');a.out.mkdir(parents=True,exist_ok=False)
    for name,data in [('configuration.json',config),('public-plan-receipt.json',receipt),('manifest.json',{'stage':segment,'assignments':pending,'assigned':total,'parent_sha256':config['parent_sha256']})]:save(a.out/name,data)
    native=NativePolicy(a.out,frozen_requests('S4'),request_builder=wire)
    inherited={c['request_sha256']:c for c in previous['calls.json']};native.cache.update(inherited)
    save(a.out/'inherited-calls.json',previous['calls.json']);save(a.out/'records.json',[]);rows=[]
    os.environ.update(SWARM_SOURCE='vishesh/codex-decision-models',SWARM_HOST=config['host'])
    import swarm_report as sr
    run=quiet(sr.start,EXPERIMENT,run=config['run_id'],params={'stage':segment,'design':'RD-4','source':config['source_commit'],'plan_url':config['plan_url'],'scripted_votes':True},message=config['run_tldr']);quiet(run.__enter__)
    quiet(sr.report,'log',experiment=EXPERIMENT,run=config['run_id'],url=config['plan_url'],message='Prospective unstarted-only continuation; no prior answer replaced.')
    cases={c['case_id']:c for c in trajectories()}
    health_stopped=False
    for item in pending:
        if not transport_healthy():health_stopped=True;break
        if native.consecutive>=5 or time.monotonic()-native.started>2700:break
        item['status']='started';save(a.out/'manifest.json',{'stage':segment,'assignments':pending,'assigned':total,'parent_sha256':config['parent_sha256']})
        rows.extend(execute(cases[item['case_id']],item['arm'],native));item['status']='terminal'
        save(a.out/'records.json',rows);save(a.out/'manifest.json',{'stage':segment,'assignments':pending,'assigned':total,'parent_sha256':config['parent_sha256']})
        quiet(run.progress,len(rows),total,terminal=len(rows))
    if any(c['request_sha256'] in inherited for c in native.calls):raise ValueError('parent_request_retried')
    continuation={'stage':segment,'assigned':total,'terminal':len(rows),'missing':total-len(rows),'new_requests':len(native.calls),'valid_new_requests':sum(c['status']=='completed' for c in native.calls),'inherited_logical_uses':sum(h in inherited for h in native.request_history),'logical_calls':native.logical_calls,'cost_usd':sum(c.get('checked',{}).get('cost_usd',0) for c in native.calls),'elapsed_seconds':time.monotonic()-native.started,'parent_unchanged':True,'health_stopped':health_stopped}
    save(a.out/'summary.json',continuation)
    combined=a.out/'combined';combined.mkdir()
    allrows=combine(previous['records.json'],rows);allcalls=previous['calls.json']+native.calls
    report=analyze('S4',allrows,allcalls,previous['summary.json']['logical_calls']+native.logical_calls,config,previous['summary.json']['elapsed_seconds']+continuation['elapsed_seconds']);report['execution_segments']=segments;report['provider_reservations_not_worker_attempts']=True
    merged_manifest=previous['manifest.json'];changed={(x['case_id'],x['arm']):x for x in pending}
    merged_manifest['assignments']=[changed.get((x['case_id'],x['arm']),x) for x in merged_manifest['assignments']]
    merged_manifest['execution_segments']=segments;save(combined/'manifest.json',merged_manifest)
    save(combined/'records.json',allrows);save(combined/'calls.json',allcalls);save(combined/'summary.json',report);save(combined/'configuration.json',config)
    from rd4_render import render
    render(combined);annotate(combined,segments)
    for f in a.out.iterdir():
        if f.suffix=='.json':quiet(run.artifact,str(f),f.name)
    for f in combined.iterdir():
        quiet(run.artifact,str(f),'combined-'+f.name)
    quiet(run.fail if continuation['missing'] else run.done,message='Unstarted-only continuation complete; combined '+str(len(allrows))+'/576, prior failures retained.',terminal=len(rows),cost_usd=continuation['cost_usd'])
    print(json.dumps(continuation),flush=True)
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'continuation_failed':type(e).__name__}));raise SystemExit(1)
