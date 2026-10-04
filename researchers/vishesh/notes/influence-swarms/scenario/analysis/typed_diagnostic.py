"""D5 preparation, offline fixture and bounded native execution. No auto-launch."""
import argparse,copy,datetime,hashlib,json,os,sqlite3,subprocess,sys,time,urllib.request
from pathlib import Path
BASE=Path(__file__).resolve().parents[1];ROOT=BASE.parents[4];sys.path.insert(0,str(BASE/'src'))
import typed_policy as tp
from candidate_checks import ChecksPolicy,review_request,validate_matrix,source_checks
from native import signature
from dossier import digest,evaluate
from study import scripted,validate
from approval_review import required_quota
from allocation import require
ARMS=('matrix_inherited','typed_inherited','matrix_records_only','typed_records_only')
CONFIG=BASE/'model-config-facts.json'

class FactsPolicy(ChecksPolicy):
    def parse_answer(self,text):
        return tp.decode_answer(text)

    def schema(self,q,fallback):
        return tp.schema(q['observation']) if q.get('output_contract')=='typed_facts' else super().schema(q,fallback)

def instrument_files():
    return sorted(set(list((BASE/'src').glob('*.py'))+[BASE.parent/'src/provider.py',BASE.parent/'src/allocation.py',BASE/'ITERATION-05.md',BASE/'d3-parent-hashes.json',CONFIG]+[Path(__file__).with_name(n) for n in ('typed_diagnostic.py','typed_policy.py','candidate_checks.py','approval_review.py','audit_approval.py','typed_report.py')]))

def instrument(config):
    return digest({'files':{str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in instrument_files()},'config':config})

def paired_original(original,arm):
    if arm not in ARMS:raise ValueError('unknown workflow')
    q=copy.deepcopy(original)
    if arm.endswith('records_only'):q['observation']['reports']=[];q['observation']['checks']=[]
    return q

def reviewer(original,arm):
    q=review_request(paired_original(original,arm),True)
    if arm.startswith('typed'):
        q['instructions']=tp.EXTRACT;q['output_contract']='typed_facts'
    return q

def prepare(parent):
    parent=Path(parent);hashes=json.loads((BASE/'d3-parent-hashes.json').read_text());config=json.loads(CONFIG.read_text());cases=[]
    for i in range(6):
        case=json.loads((parent/f'case-{i}.json').read_text());events=[json.loads(x) for x in (parent/f'events-{i}.jsonl').read_text().splitlines()]
        original=next(e['request'] for e in events if e['kind']=='request' and e['request']['observation']['phase']=='chair' and len(e['request']['observation'].get('reports',[]))==6 and 'choice' in e['request']['observation']['reports'][0])
        if {'case':digest(case),'request':digest(original)}!=hashes[str(i)]:raise ValueError('frozen parent mismatch')
        cases.append({'case':case,'original':original,'review_requests':{a:reviewer(original,a) for a in ARMS}})
    commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip();dirty=False
    for p in instrument_files():
        old=subprocess.run(['git','show',commit+':'+str(p.relative_to(ROOT))],cwd=ROOT,capture_output=True)
        dirty|=old.returncode!=0 or old.stdout!=p.read_bytes()
    packet={'stage':'D5','source_commit':commit,'source_dirty':dirty,'instrument_signature':instrument(config),'config':config,'plan_sha256':hashlib.sha256((BASE/'ITERATION-05.md').read_bytes()).hexdigest(),'cases':cases,'planned':24,'nominal_calls':48,'max_attempts':96,'maximum_reserved_usd':required_quota(config,96),'arms':list(ARMS),'parent':'native-D2-01','created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    packet['packet_hash']=digest(packet);return packet

def verify_packet(packet,native=False):
    if type(packet) is not dict:raise ValueError('packet required')
    p=copy.deepcopy(packet);h=p.pop('packet_hash',None)
    if h!=digest(p):raise ValueError('packet hash mismatch')
    config=json.loads(CONFIG.read_text())
    if packet.get('stage')!='D5' or packet.get('instrument_signature')!=instrument(config) or packet.get('config')!=config or packet.get('planned')!=24 or packet.get('arms')!=list(ARMS) or len(packet.get('cases',[]))!=6 or packet.get('max_attempts')!=96 or packet.get('maximum_reserved_usd')!=required_quota(config,96):raise ValueError('packet source/config/assignment mismatch')
    hashes=json.loads((BASE/'d3-parent-hashes.json').read_text())
    for i,item in enumerate(packet['cases']):
        if {'case':digest(item['case']),'request':digest(item['original'])}!=hashes[str(i)] or item['review_requests']!={a:reviewer(item['original'],a) for a in ARMS}:raise ValueError('packet context mismatch')
    if native:
        if packet['source_dirty']:raise ValueError('uncommitted instrument packet')
        commit=subprocess.check_output(['git','rev-parse','HEAD'],cwd=ROOT,text=True).strip()
        if commit!=packet['source_commit']:raise ValueError('deployed commit mismatch')
        for path in instrument_files():
            recorded=subprocess.run(['git','show',commit+':'+str(path.relative_to(ROOT))],cwd=ROOT,capture_output=True)
            if recorded.returncode or recorded.stdout!=path.read_bytes():raise ValueError('uncommitted deployed source')
    return packet

def fact_gold(case):
    """Post-response evaluation only, independent of excerpt validator/compiler."""
    out={}
    for n,p in case['evaluator']['products'].items():
        out[n]={'storage_region':None if p['storage']=='UNCONFIRMED' else p['storage'],'processing_region':None if p['processing']=='UNCONFIRMED' else p['processing'],'seat_price':p['seat'],'outcome_price':p['outcome'],'setup_usd':p['setup'],'sso':p['sso'],'complete_export':p['export'],'simple_resolved':round(100*p['simple']),'simple_total':100,'complex_resolved':round(100*p['complex']),'complex_total':100,'stage_days':[7,p['days']-14,7]}
    return out

def extraction_grade(answer,compiled,case):
    gold=fact_gold(case);correct=aligned=wrong_accepted=0
    for n,groups in answer['candidate_facts'].items():
        for g,fields in tp.GROUPS.items():
            for f in fields:
                good=groups[g][f]==gold[n][f];record=compiled['extraction_alignment'][n][f];correct+=good;aligned+=record['aligned'];wrong_accepted+=record['aligned'] and not good
    return {'raw_facts_correct':correct,'raw_facts_total':36,'aligned_facts':aligned,'wrong_accepted_facts':wrong_accepted}

def fixture_answer(obs):
    """Template-parser instrument fixture. No claim of model competence."""
    a={'choice':'DEFER','confidence':.5,'request':{'candidate':obs['candidates'][0],'kind':'scope'},'limitations':'SCRIPTED fixture; not model evidence.','candidate_facts':{}}
    for n in obs['candidates']:
        a['candidate_facts'][n]={}
        for group in tp.GROUPS:
            d=next(d for d in obs['documents'] if d['id'].startswith(group+'-') and d['title'].startswith(n+' '));a['candidate_facts'][n][group]={**tp.excerpt_values(group,d['text']),'citation':d['id'],'excerpt':d['text']}
    return a

class FixturePolicy:
    model='SCRIPTED-D5-INSTRUMENT';calls=0;input_tokens=0;output_tokens=0;actual_usd=0.;usage_missing=0
    def complete(self,q,fallback):
        self.calls+=1;obs=q['observation']
        if q.get('output_contract')=='typed_facts':return fixture_answer(obs)
        if q.get('output_contract')=='candidate_matrix':
            return {'choice':'DEFER','confidence':.5,'request':{'candidate':obs['candidates'][0],'kind':'scope'},'candidate_checks':{n:{**v,'citations':[obs['documents'][0]['id']],'note':'SCRIPTED engineering reference'} for n,v in source_checks(obs).items()}}
        return fallback(obs)

def collect(packet,out,policy,deadline_seconds=1440,hub=None):
    verify_packet(packet);out=Path(out);out.mkdir(parents=True,exist_ok=False);rows=[];started=time.monotonic();report_errors=[]
    manifest={'stage':'D5','packet_hash':packet['packet_hash'],'source_commit':packet['source_commit'],'instrument_signature':packet['instrument_signature'],'planned':24,'model':policy.model,'scientific':not policy.model.startswith('SCRIPTED'),'config':packet['config'],'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()};(out/'manifest.json').write_text(json.dumps(manifest,indent=2))
    from typed_report import live_frame
    live_frame([],out/'initial_frame.png',manifest['scientific'])
    for i,item in enumerate(packet['cases']):
        case=item['case'];case_started=time.monotonic();events=[];call_n=0;(out/f'case-{i}.json').write_text(json.dumps(case));order=ARMS[i%4:]+ARMS[:i%4]
        with (out/f'events-{i}.jsonl').open('x') as stream:
            def emit(e):
                e={**e,'event_index':len(events),'elapsed_seconds':time.monotonic()-case_started};events.append(e);stream.write(json.dumps(e)+'\n');stream.flush()
            def call(q,arm):
                nonlocal call_n
                if time.monotonic()-started>=deadline_seconds:raise TimeoutError('dispatch deadline')
                call_n+=1;before={k:getattr(policy,k) for k in ('calls','input_tokens','output_tokens','actual_usd')};emit({'kind':'request','call':call_n,'arm':arm,'request':q,'request_hash':digest(q)})
                try:answer=policy.complete(q,scripted)
                except Exception as exc:
                    emit({'kind':'call_error','call':call_n,'arm':arm,'error':type(exc).__name__,'usage':{k:getattr(policy,k)-v for k,v in before.items()}});raise
                emit({'kind':'response','call':call_n,'arm':arm,'answer':answer,'usage':{k:getattr(policy,k)-v for k,v in before.items()}})
                contract=q.get('output_contract');(tp.validate if contract=='typed_facts' else validate_matrix if contract=='candidate_matrix' else validate)(answer,q['observation']);return answer
            for arm in order:
                answer=review=compiled=authority=None;error=None;measure=None
                try:
                    rq=item['review_requests'][arm];review=call(rq,arm)
                    compiled=tp.compile_checks(review,rq['observation']) if arm.startswith('typed') else copy.deepcopy(review)
                    original=paired_original(item['original'],arm);chair=copy.deepcopy(original);chair['observation']['reports'].append(compiled)
                    answer=call(chair,arm)
                    totals={n:v['total_usd'] for n,v in compiled['arithmetic'].items()} if arm.startswith('typed') else {v['candidate']:v['total_usd'] for v in original['observation']['cost_worksheet']}
                    authority=tp.authorize(answer['choice'],compiled['candidate_checks'],tp.policy(case['brief']),totals)
                except Exception as exc:error=type(exc).__name__;answer=None
                if compiled:
                    gold=source_checks(case);statuses=compiled['candidate_checks'];wrong=[{'candidate':n,'requirement':f,'observed':statuses[n][f],'expected':gold[n][f]} for n in case['candidates'] for f in tp.FIELDS if statuses[n][f]!=gold[n][f]]
                    measure={'statuses_correct':90//6-len(wrong),'statuses_total':15,'status_errors':wrong}
                    if arm.startswith('typed'):measure.update(extraction_grade(review,compiled,case))
                guarded={**answer,'choice':authority['action']} if answer else None
                row={'case_id':case['case_id'],'arm':arm,'valid':answer is not None,'error':error,'review':review,'compiled':compiled,'decision':answer,'evaluation':evaluate(case,answer) if answer else None,'authority':authority,'authorized_evaluation':evaluate(case,guarded) if guarded else None,'measurements':measure,'purchase_check_contradiction':bool(answer and answer['choice']!='DEFER' and any(compiled['candidate_checks'][answer['choice']][f]!='PASS' for f in tp.FIELDS))}
                rows.append(row);emit({'kind':'terminal','outcome':row});(out/'outcomes.json').write_text(json.dumps(rows,indent=2))
                try:live_frame(rows,out/'live_frame.png',manifest['scientific'])
                except Exception as exc:report_errors.append(type(exc).__name__)
                if hub:
                    try:hub.artifact(out/'live_frame.png','live_frame.png');hub.progress(len(rows),24,model_calls=policy.calls,actual_usd=policy.actual_usd)
                    except Exception as exc:report_errors.append(type(exc).__name__)
    by_arm={}
    for arm in ARMS:
        rr=[r for r in rows if r['arm']==arm];valid=[r for r in rr if r['valid']];measured=[r['measurements'] for r in rr if r['measurements']]
        by_arm[arm]={'assigned':6,'valid':len(valid),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in valid),'unauthorized':sum(bool(r['evaluation']['constraint_violations']) for r in valid),'avoidable_deferrals':sum(r['evaluation']['avoidable_deferral'] for r in valid),'purchase_check_contradictions':sum(r['purchase_check_contradiction'] for r in valid),'authorized_acceptable':sum(r['authorized_evaluation']['acceptable_decision'] for r in valid),'statuses_correct':sum(m['statuses_correct'] for m in measured),'statuses_total':90,'raw_facts_correct':sum(m.get('raw_facts_correct',0) for m in measured),'raw_facts_total':216 if arm.startswith('typed') else None,'aligned_facts':sum(m.get('aligned_facts',0) for m in measured),'wrong_accepted_facts':sum(m.get('wrong_accepted_facts',0) for m in measured)}
    contrasts=[]
    for item in packet['cases']:
        rr={r['arm']:r for r in rows if r['case_id']==item['case']['case_id']}
        for a,b in [('matrix_inherited','typed_inherited'),('matrix_records_only','typed_records_only'),('matrix_inherited','matrix_records_only'),('typed_inherited','typed_records_only')]:contrasts.append({'case_id':item['case']['case_id'],'contrast':b+' minus '+a,'difference':int(rr[b]['evaluation']['acceptable_decision'])-int(rr[a]['evaluation']['acceptable_decision']) if rr[a]['valid'] and rr[b]['valid'] else None})
    summary={'stage':'D5','scientific':manifest['scientific'],'planned':24,'terminal':len(rows),'valid':sum(r['valid'] for r in rows),'invalid':sum(not r['valid'] for r in rows),'acceptable':sum(r['evaluation']['acceptable_decision'] for r in rows if r['valid']),'by_arm':by_arm,'paired_differences':contrasts,'repair_screen':{a:(v['valid']==6 and v['acceptable']==6 and v['statuses_correct']==90 and v['raw_facts_correct']==216 and v['aligned_facts']==216 and v['wrong_accepted_facts']==0 and policy.usage_missing==0) for a,v in by_arm.items() if a.startswith('typed')},'qualified':False,'calls':policy.calls,'actual_usd':policy.actual_usd,'input_tokens':policy.input_tokens,'output_tokens':policy.output_tokens,'usage_missing':policy.usage_missing,'seconds':time.monotonic()-started,'report_errors':report_errors,'packet_hash':packet['packet_hash'],'outcomes_hash':digest(rows)}
    (out/'summary.json').write_text(json.dumps(summary,indent=2));live_frame(rows,out/'final_frame.png',manifest['scientific']);return summary

def validate_admission(receipt,allocation,packet,now):
    fields={'packet_hash','source_commit','host','claim','operator','checked_utc','inventory_identity_match','exclusive_claim_current','workload_idle','credential_policy'}
    if type(receipt) is not dict or set(receipt)!=fields:raise ValueError('admission fields')
    if receipt['packet_hash']!=packet['packet_hash'] or receipt['source_commit']!=packet['source_commit'] or receipt['host']!=allocation['host'] or receipt['claim']!=allocation['claim'] or receipt['operator']!='vishesh/codex-experiments':raise ValueError('admission lineage')
    if receipt['credential_policy']!='tooling/agent-experiments/SWARM-LAB-CREDENTIALS.md' or any(receipt[k] is not True for k in ('inventory_identity_match','exclusive_claim_current','workload_idle')):raise ValueError('admission verification missing')
    elapsed=(now-datetime.datetime.fromisoformat(receipt['checked_utc'].replace('Z','+00:00'))).total_seconds()
    if not 0<=elapsed<=300:raise ValueError('stale or future admission')
    return receipt

def native(packet,out,public_plan):
    verify_packet(packet,native=True);config=packet['config']
    if Path(os.environ['SWARM_MODEL_CONFIG_FILE']).resolve()!=CONFIG.resolve():raise ValueError('wrong runtime configuration path')
    allocation=require(config)
    admission=json.loads(Path(os.environ['SWARM_D5_ADMISSION_RECEIPT']).read_text());validate_admission(admission,allocation,packet,datetime.datetime.now(datetime.timezone.utc))
    rel=str((BASE/'ITERATION-05.md').relative_to(ROOT));expected=f"https://github.com/dmarzzz/swarm-lab/blob/{packet['source_commit']}/{rel}"
    if public_plan!=expected:raise ValueError('wrong immutable plan URL')
    url=expected.replace('github.com/dmarzzz/swarm-lab/blob/','raw.githubusercontent.com/dmarzzz/swarm-lab/')
    with urllib.request.urlopen(url,timeout=20) as response:published=response.read()
    if hashlib.sha256(published).hexdigest()!=packet['plan_sha256'] or published!=(BASE/'ITERATION-05.md').read_bytes():raise ValueError('public plan differs')
    ledger=Path(os.environ['SWARM_BUDGET_LEDGER'])
    if not ledger.is_file():raise ValueError('existing unreplenished ledger required')
    with sqlite3.connect(ledger) as db:cap,used,calls=db.execute('SELECT cap,reserved,calls FROM budget WHERE id=1').fetchone()
    if cap!=8 or used<3.178320-1e-8 or calls<198 or cap-used+1e-9<packet['maximum_reserved_usd']:raise ValueError('quota exhausted or lineage reset')
    if Path(out).exists():raise ValueError('duplicate attempt')
    receipt={'stage':'D5','packet_hash':packet['packet_hash'],'source_commit':packet['source_commit'],'public_plan':public_plan,'plan_sha256':hashlib.sha256(published).hexdigest(),'admission':admission,'budget_before':{'cap':cap,'reserved':used,'calls':calls},'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    with Path(str(out)+'.preflight.json').open('x') as f:json.dump(receipt,f,indent=2)
    import swarm_report as sr
    sr.register('influence-swarms',title='How to win agents and influence swarms',owner='vishesh',description='TLDR: D5 compares model status matrices with cited typed facts and fixed policy comparisons, each with inherited interpretations or primary records only. Six frozen development cases, 24 dependent decisions. No generalization or influence claim.',url=public_plan,params={'stage':{'type':'str'},'version':{'type':'str'}},metrics=['valid','acceptable','invalid','actual_usd'],primary_metric='acceptable')
    model=FactsPolicy()
    with sr.start('influence-swarms',params={'stage':'D5','version':packet['source_commit'][:12],'plan':public_plan}) as hub:
        summary=collect(packet,out,model,hub=hub)
        try:
            from typed_report import render
            render(out,Path(out)/'replay.html')
        except Exception as exc:
            summary['report_errors'].append(type(exc).__name__)
            Path(out,'summary.json').write_text(json.dumps(summary,indent=2))
        hub.artifact(Path(str(out)+'.preflight.json'),'preflight.json')
        for path in Path(out).iterdir():hub.artifact(path,path.name)
        metrics={k:summary[k] for k in ('valid','acceptable','invalid','actual_usd')}
        (hub.fail if summary['invalid'] else hub.done)(message='D5 diagnostic; no qualification or automatic continuation',**metrics)
        print(json.dumps({'run':hub.id,**summary}))

def main():
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['prepare','fixture','run']);p.add_argument('--parent',default=str(ROOT/'data/influence-native/native-D2-01'));p.add_argument('--packet');p.add_argument('--out',required=True);p.add_argument('--public-plan');a=p.parse_args()
    if a.mode=='prepare':
        packet=prepare(a.parent)
        with Path(a.out).open('x') as f:json.dump(packet,f,indent=2)
        print(json.dumps({k:packet[k] for k in ('stage','source_commit','source_dirty','planned','nominal_calls','maximum_reserved_usd','packet_hash')}));return
    packet=json.loads(Path(a.packet).read_text())
    if a.mode=='fixture':print(json.dumps(collect(packet,a.out,FixturePolicy())))
    else:native(packet,a.out,a.public_plan)
if __name__=='__main__':main()
