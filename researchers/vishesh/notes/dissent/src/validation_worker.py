"""D1 response-contract diagnostic. Never substitutes observations into S1."""
import argparse,collections,json,os,time
from pathlib import Path
from live_worker import verify_config,save,quiet,NativePolicy
from live_design import assignments,validation_diagnostic,frozen_requests,SNAPSHOT

def main(a):
    config=json.loads(a.config.read_text());receipt=verify_config(config,'D1');a.out.mkdir(parents=True,exist_ok=False)
    save(a.out/'configuration.json',config);save(a.out/'public-plan-receipt.json',receipt)
    planned=assignments('D1')
    for x in planned:x['status']='planned'
    save(a.out/'manifest.json',{'assignments':planned,'total':9,'stage':'D1'})
    policy=NativePolicy(a.out,frozen_requests('D1'));rows=[]
    os.environ.update(SWARM_SOURCE='vishesh/codex-decision-models',SWARM_HOST=config['host'])
    import swarm_report as sr
    run=quiet(sr.start,'right-dissenter',run=config['run_id'],params={'stage':'D1','source':config['source_commit'],'design':'RD-3-diagnostic'},message=config['run_tldr']);quiet(run.__enter__)
    quiet(sr.report,'log',experiment='right-dissenter',run=config['run_id'],url=config['plan_url'],message='Nine-call validation diagnostic; no S1 replacement.')
    for item,c in zip(planned,validation_diagnostic()):
        if policy.consecutive>=5 or time.monotonic()-policy.started>2700:break
        try:action=policy(c['phase'],c['packet']);status='completed'
        except Exception:action=None;status='failed'
        rows.append({'case_id':c['case_id'],'arm':c['arm'],'status':status,'action':action,'expected':c['expected'],'correct':action==c['expected'] if c['expected'] is not None and status=='completed' else None})
        item['status']=status;save(a.out/'records.json',rows);save(a.out/'manifest.json',{'assignments':planned,'total':9,'stage':'D1'})
        quiet(run.progress,len(rows),9,terminal=len(rows))
    per={arm:{'assigned':n,'valid':sum(x['arm']==arm and x['status']=='completed' for x in rows),'correct':sum(x['correct'] is True for x in rows if x['arm']==arm)} for arm,n in [('reproduction',3),('fresh-control',6)]}
    report={'stage':'D1','assigned':9,'terminal':len(rows),'missing':9-len(rows),'by_input_class':per,'errors':dict(collections.Counter(x['error'] for x in policy.calls if x['status']=='failed')),'cost_usd':sum(x.get('checked',{}).get('cost_usd',0) for x in policy.calls),'input_tokens':sum(x.get('checked',{}).get('input_tokens',0) for x in policy.calls),'unique_requests':len(policy.calls),'elapsed_seconds':time.monotonic()-policy.started,'served_model':SNAPSHOT,'changes_S1_scores':False}
    save(a.out/'summary.json',report)
    from live_render import base,font,GREEN,FG,MUTED
    im,d=base('The Right Dissenter | validation diagnostic','Native Jev | 3 reproduction inputs + 6 fresh controls | S1 remains unchanged')
    for i,(arm,v) in enumerate(per.items()):
        y=270+i*200;d.text((70,y),arm,font=font(36),fill=FG);d.rectangle((500,y,1530,y+55),fill='#253642')
        if v['valid']:d.rectangle((500,y,500+1030*v['valid']/v['assigned'],y+55),fill=GREEN)
        d.text((500,y+80),str(v['valid'])+'/'+str(v['assigned'])+' valid replies',font=font(30),fill=MUTED)
    d.text((70,730),'Fresh controls correct: '+str(per['fresh-control']['correct'])+'/6',font=font(32),fill=FG)
    for i,(code,n) in enumerate(report['errors'].items()):d.text((70,820+i*55),code+': '+str(n),font=font(28),fill=FG)
    d.text((70,995),'Observed validation codes classify this attempt; original generic failures are not backfilled.',font=font(24),fill=MUTED)
    im.save(a.out/'final_frame.png')
    for f in a.out.iterdir():
        if f.suffix in ('.json','.png'):quiet(run.artifact,str(f),f.name)
    quiet(run.fail if report['missing'] else run.done,message='D1 complete; '+str(report['errors'])+'; S1 outcomes preserved.',terminal=len(rows),cost_usd=report['cost_usd'])
    print(json.dumps(report))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--config',type=Path,required=True);p.add_argument('--out',type=Path,required=True)
    try:main(p.parse_args())
    except Exception as e:print(json.dumps({'diagnostic_failed':type(e).__name__}));raise SystemExit(1)
