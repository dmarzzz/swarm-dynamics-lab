"""Frozen finite-support D1 design and saved-evidence analysis. No native transport."""
import hashlib
import html
import itertools
import json
from pathlib import Path
import random
import sys
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from qualification import MODEL, CRITERIA, RESERVE, digest, validate_response

QUAL = 'QM-D1-Q0-01'
MAIN = 'QM-D1-01'
CONTEXTS = ('none', 'self-correct', 'self-wrong', 'peers-correct', 'peers-wrong')
REPRESENTATIONS = ('deduplicated', 'copied')
INSTRUCTIONS = ('Select the more likely hidden binary state, ZERO or ONE. The prior probability '
    'of each state is 1/2. Each observation reports the true state with probability q. '
    'Distinct visible_root labels identify independent observations conditional on the state. '
    'Reports with the same visible_root are copies of one observation: count that source once. '
    'The prior decisions are scripted choices based on these same reports, not fresh measurements. '
    'Use the reports to make your decision regardless of available prior choices. '
    'Select DEFER only if unable to determine which state is more likely.')


def ordered(tag, values):
    return sorted(values, key=lambda value: hashlib.sha256(f'{tag}:{value}'.encode()).hexdigest())


def make_manifest(attempt):
    if attempt not in (QUAL, MAIN):
        raise ValueError('unknown_attempt')
    qualification = attempt == QUAL
    patterns = list(itertools.product((0, 1), repeat=3)) if qualification else [(1,0,0),(0,1,1),(0,0,0),(1,1,1)]
    fixtures = list(itertools.product((.72,) if qualification else (.65,.80), patterns))
    rows = []
    for repeat in (1,) if qualification else (1,2):
        block = []
        for f, (q, bits) in enumerate(fixtures):
            target = 'ONE' if sum(bits) >= 2 else 'ZERO'
            # Tag excludes bits, q, target, arm and stage. Label complements share aliases/order.
            tag = str(f // 2)
            aliases = ordered('aliases:' + tag, ['s00','s01','s02'])
            # Keep the same source-level records in both representations; extra copies have new IDs.
            full = [dict(id=f'd{i*7+j:02}', value=bits[i], q=q, visible_root=aliases[i])
                    for i, count in enumerate((7,1,1)) for j in range(count)]
            # Report ordering depends only on neutral IDs, never values.
            full.sort(key=lambda r: hashlib.sha256(f"reports:{tag}:{r['id']}".encode()).hexdigest())
            for representation, context in itertools.product(
                    ('deduplicated',) if qualification else REPRESENTATIONS,
                    ('none',) if qualification else CONTEXTS):
                reports = full if representation == 'copied' else [r for r in full if r['id'] in ('d00','d07','d14')]
                prior = None if context == 'none' else target if context.endswith('correct') else ('ONE' if target=='ZERO' else 'ZERO')
                priors = []
                for slot in range(0 if prior is None else 1 if context.startswith('self') else 3):
                    other = 'ZERO' if prior=='ONE' else 'ONE'
                    priors.append({'slot':slot,'choice':prior,'choice_scores':{prior:.80,other:.15,'DEFER':.05}})
                body = {'model':MODEL,'provider':{'only':['typesafe'],'allow_fallbacks':False},
                    'state':{'reports':reports, 'prior_role':'none' if not priors else 'self' if context.startswith('self') else 'peers',
                             'prior_decisions':priors},
                    'questions':{'decision':{'type':'choice','instructions':INSTRUCTIONS,'criteria':dict(CRITERIA)}}}
                if len(json.dumps(body).encode()) > 16000:
                    raise ValueError('request_size')
                block.append({'id':f'{attempt}-{f:02}-{representation}-{context}-r{repeat}',
                    'fixture':f,'q':q,'bits':list(bits),'stratum':'agreement' if len(set(bits))==1 else 'conflict',
                    'representation':representation,'context':context,'repeat':repeat,'expected':target,
                    'prior':prior,'request':body,'request_sha256':digest(body),
                    'run_tldr':f'D1 {representation}, {context}, q={q}, repetition {repeat}: source-MAP accuracy on fixed binary reports; scripted priors, no interacting swarm.'})
        random.Random(20261004 + repeat - 1).shuffle(block)
        rows.extend(block)
    return {'experiment':'quorum-of-mirrors','attempt':attempt,'stage':'clean-qualification' if qualification else 'diagnostic',
            'assignments':rows,'assignments_sha256':digest(rows),'max_calls':len(rows),
            'reserved_usd':round(len(rows)*RESERVE,9)}


def validate_manifest(manifest):
    if not isinstance(manifest,dict) or manifest != make_manifest(manifest.get('attempt')):
        raise ValueError('manifest_mismatch')


def analyze(manifest, receipts):
    validate_manifest(manifest)
    rows = {r['id']:r for r in manifest['assignments']}
    saved = {}
    for receipt in receipts:
        ident = receipt.get('id')
        if ident not in rows or ident in saved or receipt.get('request_sha256') != rows[ident]['request_sha256']:
            raise ValueError('duplicate_unknown_or_mismatched_receipt')
        if receipt.get('status') not in ('complete','failed'):
            raise ValueError('nonterminal_receipt')
        if receipt['status']=='complete':
            validate_response(receipt.get('response'))
        saved[ident] = receipt
    cells = []
    for ident,row in rows.items():
        receipt = saved.get(ident,{})
        status = receipt.get('status','unstarted')
        choice = validate_response(receipt['response'])['choice'] if status=='complete' else None
        reports = row['request']['state']['reports']
        majority = 'ONE' if sum(r['value'] for r in reports)>len(reports)/2 else 'ZERO'
        cells.append({k:row[k] for k in ('id','fixture','stratum','representation','context','repeat','expected')} |
                     {'status':status,'choice':choice,'correct':choice==row['expected'],
                      'prior_match':choice==row['prior'] if choice is not None and row['prior'] is not None else None,
                      'report_majority_match':choice==majority if choice is not None else None})
    def counts(group):
        result={'assigned':len(group),'valid':sum(c['status']=='complete' for c in group),
            'correct':sum(c['correct'] for c in group),'wrong':sum(c['choice'] in ('ZERO','ONE') and not c['correct'] for c in group),
            'defer':sum(c['choice']=='DEFER' for c in group),'failed':sum(c['status']=='failed' for c in group),
            'unstarted':sum(c['status']=='unstarted' for c in group)}
        result['prior_eligible']=sum(c['prior_match'] is not None for c in group)
        result['prior_matches']=sum(c['prior_match'] is True for c in group)
        result['report_majority_matches']=sum(c['report_majority_match'] is True for c in group)
        result['accuracy_bounds']=[result['correct']/len(group),(result['correct']+result['failed']+result['unstarted'])/len(group)]
        return result
    result=counts(cells)
    result.update(attempt=manifest['attempt'],cells=cells,qualified=False)
    complete=[r for r in receipts if r['status']=='complete']
    result['valid_response_usage']={key:round(sum(r['response']['usage'][key] for r in complete),12) for key in ('cost','input_tokens','output_tokens')}
    known=[r['response']['usage']['cost'] for r in complete]+[r['accounting']['usage']['cost'] for r in receipts if r['status']=='failed' and r.get('accounting')]
    result['accounting_summary']={'reserved_usd':round(len(receipts)*RESERVE,9),'known_actual_usd':round(sum(known),12),'unknown_charge_calls':len(receipts)-len(known)}
    result['latency_s']=[r.get('wall_s') for r in receipts]
    controls=[c for c in cells if c['stratum']=='agreement' and c['context']=='none']
    result['unanimous_controls']=counts(controls)
    if manifest['attempt']==QUAL:
        result['qualified']=result['valid']==8 and result['correct']>=7 and all(c['correct'] for c in controls)
        return result
    result['arms']={f'{rep}/{ctx}/{stratum}':counts([c for c in cells if (c['representation'],c['context'],c['stratum'])==(rep,ctx,stratum)])
                   for rep,ctx,stratum in itertools.product(REPRESENTATIONS,CONTEXTS,('conflict','agreement'))}
    lookup={(c['fixture'],c['representation'],c['context'],c['repeat']):c for c in cells}
    fixtures=sorted({c['fixture'] for c in cells if c['stratum']=='conflict'})
    pairs=[]
    for f,repeat in itertools.product(fixtures,(1,2)):
        d=lookup[f,'deduplicated','none',repeat];r=lookup[f,'copied','none',repeat]
        lo=int(d['correct'])-int(r['correct'])-int(r['status']!='complete')
        hi=int(d['correct'])+int(d['status']!='complete')-int(r['correct'])
        pairs.append({'fixture':f,'repeat':repeat,'difference':int(d['correct'])-int(r['correct']), 'bounds':[lo,hi]})
    effects=[sum(p['difference'] for p in pairs if p['fixture']==f)/2 for f in fixtures]
    blocks=[sum(p['difference'] for p in pairs if p['repeat']==rep)/4 for rep in (1,2)]
    effect=sum(effects)/4
    interpretable=result['valid']==160 and all(c['correct'] for c in controls)
    result['primary']={'pairs':pairs,'fixture_effects':effects,'block_effects':blocks,'effect':effect,
        'bounds':[sum(p['bounds'][i] for p in pairs)/8 for i in (0,1)],'interpretable':interpretable,
        'decision':'withheld' if not interpretable else 'normalization_signal' if effect>=.5 and min(effects)>=0 and min(blocks)>=0 else 'criterion_not_met'}
    result['context_effects']={f'{rep}/{ctx}/{stratum}':
        result['arms'][f'{rep}/{ctx}/{stratum}']['accuracy_bounds'][0]-result['arms'][f'{rep}/none/{stratum}']['accuracy_bounds'][0]
        for rep,ctx,stratum in itertools.product(REPRESENTATIONS,CONTEXTS[1:],('conflict','agreement'))}
    repeat_pairs=[(lookup[f,rep,ctx,1],lookup[f,rep,ctx,2]) for f,rep,ctx in itertools.product(range(8),REPRESENTATIONS,CONTEXTS)]
    result['repeat_agreement']={'assigned_pairs':80,'valid_pairs':sum(a['choice'] is not None and b['choice'] is not None for a,b in repeat_pairs),
        'agree':sum(a['choice'] is not None and a['choice']==b['choice'] for a,b in repeat_pairs)}
    return result


def render(manifest, receipts, destination, scripted=False):
    summary=analyze(manifest,receipts)
    order={r['id']:i+1 for i,r in enumerate(receipts)}
    rows=[]
    for cell in summary['cells']:
        fields=[cell[k] for k in ('id','representation','context','repeat','expected','status','choice')]
        rows.append('<tr data-step="'+str(order.get(cell['id'],len(receipts)+1))+'">'+''.join('<td>'+html.escape(str(x))+'</td>' for x in fields)+'</tr>')
    replay=[]
    for n in range(len(receipts)+1):
        prefix=analyze(manifest,receipts[:n]);replay.append({k:prefix[k] for k in ('assigned','valid','correct','failed','unstarted','valid_response_usage','accounting_summary')})
    Path(destination).write_text('<!doctype html><meta charset="utf-8"><title>Quorum D1 receipt replay</title>'
        '<style>body{font:15px system-ui;margin:2rem}td,th{border:1px solid #bbb;padding:.5rem}table{border-collapse:collapse}.future{opacity:.45}</style>'
        '<h1>Quorum D1 — all assigned cases</h1><p>'+('SCRIPTED — NOT MODEL EVIDENCE' if scripted else 'Saved native evidence')+'</p>'
        '<p>Static calls with scripted prior choices; no simulated conversation. Missing answers remain visible.</p>'
        '<label>Receipts visible <input id="step" type="range" min="0" max="'+str(len(receipts))+'" value="'+str(len(receipts))+'"></label><pre id="counts"></pre>'
        '<table><thead><tr>'+''.join('<th>'+s+'</th>' for s in ('ID','Representation','Context','Repeat','MAP target','Status','Choice'))+'</tr></thead><tbody>'+''.join(rows)+'</tbody></table>'
        '<script>const replay='+json.dumps(replay)+'; const slider=document.getElementById("step");'
        'document.querySelectorAll("tbody tr").forEach(r=>{r.dataset.status=r.children[5].textContent;r.dataset.choice=r.children[6].textContent;});'
        'function show(){const n=Number(slider.value);document.getElementById("counts").textContent=JSON.stringify(replay[n],null,2);'
        'document.querySelectorAll("tbody tr").forEach(r=>{const future=Number(r.dataset.step)>n;r.classList.toggle("future",future);r.children[5].textContent=future?"unstarted":r.dataset.status;r.children[6].textContent=future?"—":r.dataset.choice;});}'
        'slider.oninput=show;show();</script>')
    return replay
