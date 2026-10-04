"""RD5 prepare/run/relay/report. Preparation makes no provider calls."""
import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import time
from common import digest, save
from rd5_core import ARMS, SNAPSHOT, initial_state, step
from rd5_design import qualification, study, enumerate_requests
from rd5_runtime import BASE, source_hashes, validate_packet, verify_native, Native, relay_main


def prepare(stage, plan_commit):
    hashes = source_hashes()
    head = subprocess.check_output(['git','rev-parse','HEAD'],cwd=BASE,text=True).strip()
    if stage == 'Q5':
        definition = qualification(explicit_prepare=True)
        assignments = [{k:r[k] for k in ('id','root','domain','condition','representation')} for r in definition]
        allowed = {r['id']:{digest(r['request']):r['request']} for r in definition}
    elif stage == 'H5':
        definition = study(explicit_prepare=True)
        assignments = [dict(a,id=a['id']+'-'+str(epoch),trajectory=a['id'],epoch=epoch)
                       for a in definition['trajectories'] for epoch in range(4)]
        allowed = enumerate_requests(definition)
    else:
        raise ValueError('stage')
    packet = {'schema':'rd5-prepared-v1','stage':stage,'source_commit':head,'source_hashes':hashes,
              'instrument_sha256':digest(hashes),'definition':definition,'definition_sha256':digest(definition),
              'assignments':assignments,'assignment_sha256':digest(assignments),'allowed':allowed,'allowed_sha256':digest(allowed),
              'plan_commit':plan_commit,'plan_sha256':hashlib.sha256((BASE/'AMENDMENT-01.md').read_bytes()).hexdigest(),
              'max_calls':24 if stage=='Q5' else 36,'prior_calls':428,'lifetime_stop':488,
              'automatic_retries':0,'wall_seconds':1800,'served_model':SNAPSHOT,'qualification_required':stage=='H5'}
    validate_packet(packet)
    return packet


def score_row(row, root, epoch):
    truth = root['truth'][epoch]
    complete = row['status']=='completed' and row['action'] in ('PROCEED','HOLD')
    # Authored inspection semantics are evaluated independently from model scores.
    # Before critical_tick, all acquired texts are explicitly incomplete.
    justified = complete and row['tick'] >= root['critical_tick']
    return row | {'truth':truth,'correct':complete and row['action']==truth,
                  'wrong_proceed':complete and row['action']=='PROCEED' and truth=='HOLD',
                  'needless_hold':complete and row['action']=='HOLD' and truth=='PROCEED',
                  'justified':justified,'unjustified_commit':complete and not justified,
                  'critical':row['tick']==root['critical_tick']}


def summarize(packet, manifest, rows, calls):
    indexed = {r['id']:r for r in rows}
    if len(indexed)!=len(rows) or set(indexed)-{a['id'] for a in packet['assignments']}:
        raise ValueError('unknown_or_duplicate_rows')
    if [a['id'] for a in manifest] != [a['id'] for a in packet['assignments']]:
        raise ValueError('manifest_changed')
    terminal = {a['id'] for a in manifest if a['status']=='terminal'}
    if terminal != set(indexed):
        raise ValueError('terminal_mismatch')
    result = {'stage':packet['stage'],'origin':'native-jev','assigned':len(manifest),'terminal':len(rows),
              'unstarted':sum(a['status']=='planned' for a in manifest),'started_incomplete':sum(a['status']=='started' for a in manifest),
              'failed':sum(r['status']=='failed' for r in rows),'recorded_inference_attempts':len(calls),
              'valid_responses':sum(c['status']=='completed' for c in calls),
              'unreconciled_inference_attempts':sum(c['status']!='completed' for c in calls),
              'settled_valid_cost_usd':sum(c.get('checked',{}).get('cost_usd',0) for c in calls),
              'input_tokens':sum(c.get('checked',{}).get('input_tokens',0) for c in calls),
              'instrument_sha256':packet['instrument_sha256'],'served_model':SNAPSHOT}
    if packet['stage']=='Q5':
        result['by_representation']={rep:{'assigned':12,'valid':sum(r['status']=='completed' for r in rows if r['representation']==rep),
                    'correct':sum(r['correct'] for r in rows if r['representation']==rep)} for rep in ('raw','card')}
        card = result['by_representation']['card']
        result['qualification_passed'] = len(rows)==24 and result['valid_responses']==24 and card['valid']==12 and card['correct']==12
    else:
        result['by_arm']={}
        for arm in ARMS:
            own=[r for r in rows if r['arm']==arm]
            correct=sum(r['correct'] for r in own)
            result['by_arm'][arm]={'assigned':24,'terminal':len(own),'correct':correct,'correct_rate':correct/24,
                'wrong_proceed':sum(r['wrong_proceed'] for r in own),'needless_hold':sum(r['needless_hold'] for r in own),
                'defer':sum(r['action']=='DEFER' for r in own),'unjustified_commits':sum(r['unjustified_commit'] for r in own),
                'critical_correct':sum(r['correct'] for r in own if r['critical']),
                'early_correct':sum(r['correct'] for r in own if r['tick']<4),
                'late_correct':sum(r['correct'] for r in own if r['tick']>=4),
                'physical_checks':sum(r['checks_after']-r['checks_before'] for r in own),
                'receipt_count':sum(r['acquired'] for r in own),'inference_attempts':sum(r['inference_attempted'] for r in own)}
        result['paired_roots']=[]
        for root in packet['definition']['roots']:
            scores={arm:sum(r['correct'] for r in rows if r['root']==root['id'] and r['arm']==arm) for arm in ARMS}
            observed={arm:sum(r['root']==root['id'] and r['arm']==arm for r in rows) for arm in ARMS}
            result['paired_roots'].append({'root':root['id'],'mechanism':root['mechanism'],'direction':root['direction'],
                'correct':scores,'terminal':observed,'B2_minus_B1':scores['B2']-scores['B1'],'B1_minus_B0':scores['B1']-scores['B0'],
                'complete_pair':all(n==4 for n in observed.values())})
        b1,b2=result['by_arm']['B1'],result['by_arm']['B2']
        result['development_screen_passed']=(len(rows)==72 and result['failed']==0 and b2['correct']-b1['correct']>=2
                   and b2['wrong_proceed']<=b1['wrong_proceed'] and sum(v['unjustified_commits'] for v in result['by_arm'].values())==0)
        # Honest all-assigned missing bounds, not a zero imputation of paired effects.
        result['missing_bounds']={a:[v['correct'],v['correct']+24-v['terminal']+sum(r['status']=='failed' for r in rows if r['arm']==a)]
                                  for a,v in result['by_arm'].items()}
    return result


def audit_qualification(directory, instrument):
    packet=json.loads((directory/'packet.json').read_text())
    rows=json.loads((directory/'records.json').read_text())
    calls=json.loads((directory/'calls.json').read_text())
    manifest=json.loads((directory/'manifest.json').read_text())
    if packet['stage']!='Q5' or packet['instrument_sha256']!=instrument:
        raise ValueError('qualification_instrument')
    # Verify each answer against its own frozen request and expected label;
    # never accept a claimed passing summary or a scripted fixture.
    saved=json.loads((directory/'summary.json').read_text())
    if saved.get('origin')!='native-jev' or len(calls)!=24 or len({c['identity'] for c in calls})!=24:
        raise ValueError('qualification_origin_or_count')
    definitions={d['id']:d for d in packet['definition']}
    for c in calls:
        d=definitions[c['identity']]; checked=c.get('checked',{})
        if c['status']!='completed' or c['request']!=d['request'] or checked.get('request_sha256')!=digest(d['request']) or checked.get('served_model')!=SNAPSHOT:
            raise ValueError('qualification_call')
    actions={c['identity']:c['checked']['action'] for c in calls}
    for row in rows:
        d=definitions[row['id']]
        if row['action']!=actions[row['id']] or row['correct']!=(row['action']==d['expected']) or row['status']!='completed':
            raise ValueError('qualification_scoring')
    result=summarize(packet,manifest,rows,calls)
    if not result.get('qualification_passed'):
        raise ValueError('qualification_failed')
    return result


def execute(packet, backend, out):
    """Instrument execution; production entry always calls verify_native first.

    Offline tests inject a fake backend and development definitions, never a
    credential or native endpoint. No automatic resume is provided.
    """
    out=Path(out)
    manifest=[dict(a,status='planned') for a in packet['assignments']]
    rows=[]
    save(out/'manifest.json',manifest);save(out/'records.json',rows);save(out/'calls.json',[])
    def finish(row,a):
        a['status']='terminal';rows.append(row|{k:v for k,v in a.items() if k!='status'})
        save(out/'records.json',rows);save(out/'manifest.json',manifest)
    if packet['stage']=='Q5':
        definitions={d['id']:d for d in packet['definition']}
        for a in manifest:
            if not backend.healthy(): break
            d=definitions[a['id']];a['status']='started';save(out/'manifest.json',manifest)
            try:
                action=backend.resolve(a['id'],d['request']);status='completed'
            except Exception:
                action='DEFER';status='failed'
            finish({'action':action,'status':status,'expected':d['expected'],'correct':status=='completed' and action==d['expected']},a)
            if status=='failed': break
    else:
        roots={r['id']:r for r in packet['definition']['roots']}
        state=None
        for a in manifest:
            root=roots[a['root']];epoch=a['epoch']
            if epoch==0:
                if not backend.healthy(): break
                state=initial_state(root['initial'],root['frames'][0]['task'])
            def persist(s):
                a['status']='started'
                save(out/'manifest.json',manifest)
                save(out/('state-'+a['trajectory']+'.json'),s)
            state,row=step(root['frames'][epoch],state,a['arm'],backend,a['id'],persist)
            if row['status']=='unstarted': break
            finish(score_row(row,root,epoch),a)
            if row['status']=='failed': break
    return summarize(packet,manifest,rows,backend.calls)


def run(packet, receipt, out):
    public=verify_native(packet,receipt)
    out.mkdir(parents=True,exist_ok=False)
    save(out/'packet.json',packet);save(out/'public-plan-receipt.json',public)
    # Private receipt is retained privately by the operator, not exported as an artifact.
    save(out/'admission-reference.json',{'receipt_sha256':digest(receipt),'run_id':receipt['run_id'],'source_commit':receipt['source_commit']})
    native=Native(packet,out)
    result=execute(packet,native,out)
    save(out/'summary.json',result)
    from rd5_render import render
    render(out)
    return result


def main():
    p=argparse.ArgumentParser();subs=p.add_subparsers(dest='op',required=True)
    prepare_p=subs.add_parser('prepare');prepare_p.add_argument('--stage',choices=['Q5','H5'],required=True)
    prepare_p.add_argument('--plan-commit',required=True);prepare_p.add_argument('--output',type=Path,required=True)
    for op in ('run','relay'):
        sub=subs.add_parser(op);sub.add_argument('--packet',type=Path,required=True);sub.add_argument('--receipt',type=Path,required=True)
        if op=='run':sub.add_argument('--output',type=Path,required=True)
        else:
            sub.add_argument('--credential-file',type=Path,required=True);sub.add_argument('--ledger',type=Path,required=True)
    report=subs.add_parser('report');report.add_argument('--results',type=Path,required=True)
    a=p.parse_args()
    if a.op=='prepare':
        if a.output.exists():raise ValueError('packet_exists')
        packet=prepare(a.stage,a.plan_commit);save(a.output,packet)
        print(json.dumps({'prepared':a.stage,'assignments':len(packet['assignments']),'max_calls':packet['max_calls'],
                          'request_variants':sum(map(len,packet['allowed'].values())),'packet_sha256':digest(packet)}))
    elif a.op=='report':
        from rd5_render import render
        render(a.results)
    else:
        packet=json.loads(a.packet.read_text());receipt=json.loads(a.receipt.read_text())
        if a.op=='relay':relay_main(packet,receipt,a.credential_file,a.ledger)
        else:print(json.dumps(run(packet,receipt,a.output)))


if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps({'operation_failed':type(e).__name__}))
        raise SystemExit(1)
