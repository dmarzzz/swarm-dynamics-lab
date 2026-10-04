"""Authored event ledgers. Only id/time/text records are actor-visible.

All values are fictional task facts, including credential-version identifiers.
Gold and structured updates are evaluator-only; no network or model calls.
"""
from copy import deepcopy
import json

def event(text, **updates):
    return {'text': text, 'updates': updates}

def case(id, rule, expected, rows, mutation):
    return {'id': id, 'rule': rule, 'expected': expected,
            'events': [dict(r, id=f'e{i+1:02d}', time=f'09:{i+1:02d}') for i,r in enumerate(rows)],
            'mutation': dict(mutation, id='e99', time='09:59')}

CASES = [
case('b2-01', 'Release both Cedar and Bay only if each latency is within the current limit, rollback is tested at both, and approval is recorded. Otherwise HOLD.', 'HOLD', [
 event('The original latency limit is 80 ms.', limit=80),
 event('Cedar latency is 100 ms; Bay latency is 110 ms. These are read-only tests, not write-path tests.', cedar=100,bay=110),
 event('The limit is corrected to 120 ms; measurements are unchanged.',limit=120),
 event('Cedar rollback is tested; Bay rollback is not tested.',rollback=['Cedar']),
 event('Approval is requested, but the receipt is unavailable; approval is unknown.',approval=False),
 event('Two Cedar summaries repeat the same acquisition; they are not independent tests.'),
 ], event('Bay rollback is now tested and approval is recorded. Cedar rollback remains tested.',rollback=['Cedar','Bay'],approval=True)),
case('b2-02', 'Restore service only with two independent passing probes taken after the restart and current restoration authorization. Otherwise HOLD.', 'GO', [
 event('The restart occurred at 08:50.',restart=850),
 event('Two failure reports both copy probe O from 08:40; they are one old observation.',old_origin='O'),
 event('Probe A passed at 08:55 from acquisition A.',a_time=855,a_origin='A',a_pass=True),
 event('Probe B passed at 08:57 from acquisition B.',b_time=857,b_origin='B',b_pass=True),
 event('Probe A and probe B use independent acquisitions, not copied results.'),
 event('The current restoration authorization is recorded.',authorization=True),
 ],event('Correction: probe B is a forwarded copy of acquisition A; there is no independent B acquisition.',b_origin='A')),
case('b2-03', 'Delete a backup generation only if that exact generation has a passed restore test, a retained second copy, and deletion authorization. Otherwise HOLD.', 'HOLD', [
 event('The requested deletion target is generation G8.',target='G8'),
 event('The reported restore test passed.',restore_pass=True),
 event('The test receipt identifies generation G7, not G8.',tested='G7'),
 event('A second copy of G8 is retained.',second_copy=True),
 event('Deletion authorization for G8 is recorded.',authorization=True),
 event('No additional restore result for G8 is available.'),
 ],event('A new restore test of G8 passed; its matching-generation receipt is available.',tested='G8',restore_pass=True)),
case('b2-04', 'Start maintenance only if the entire planned work interval is inside the latest authorized window, inclusive of endpoints, and rollback is ready. Otherwise HOLD.', 'GO', [
 event('The original authorized window is 10:00 through 10:20.',start=1000,end=1020),
 event('The work is planned for 10:10 through 10:30.',work_start=1010,work_end=1030),
 event('The authorized window is revised to 10:00 through 10:40, replacing the earlier end.',start=1000,end=1040),
 event('The revision changes the window, not the planned work interval.'),
 event('Rollback is ready for this maintenance.',rollback=True),
 event('An old reminder still displays 10:20; it copies the superseded schedule.'),
 ],event('The work end is changed to 10:45; its start stays 10:10.',work_end=1045)),
case('b2-05', 'Approve the two-item purchase only if the combined current cost is at most 100 units and both items are eligible. Individual item totals are not separate allowances. Otherwise HOLD.', 'HOLD', [
 event('Item A originally costs 40 units.',a=40),
 event('Item B costs 50 units.',b=50),
 event('Item A is corrected to 60 units; its earlier quote is superseded.',a=60),
 event('Both items are eligible.',eligible=True),
 event('Two forwarded quotes for A refer to the same item, not extra purchases.'),
 event('No discount or additional allowance has been authorized.'),
 ],event('Item A is repriced to 45 units; the previous 60-unit price is superseded.',a=45)),
case('b2-06', 'Release a shipment only if every included lot has a passed inspection and a release receipt. Excluded lots do not block this shipment. Otherwise HOLD.', 'GO', [
 event('The shipment originally includes lots L1, L2 and L3.',included=['L1','L2','L3']),
 event('L1 passed inspection and has its release receipt.',ok1=True),
 event('L2 passed inspection and has its release receipt.',ok2=True),
 event('L3 is damaged and has no release receipt.',ok3=False),
 event('The shipment is revised to include only L1 and L2; L3 is excluded.',included=['L1','L2']),
 event('The revision does not repair L3 or grant it release approval.'),
 ],event('The shipment is changed to include L1, L2 and L3.',included=['L1','L2','L3'])),
case('b2-07', 'Export only if current consent covers every requested field and the destination is approved. Consent for overlapping fields is insufficient. Otherwise HOLD.', 'HOLD', [
 event('The requested fields are name, region and contact.',requested=['name','region','contact']),
 event('The current consent receipt covers name and region only.',consented=['name','region']),
 event('The destination is approved.',destination=True),
 event('A second consent email forwards the same receipt; it adds no fields.'),
 event('Permission for contact was requested but is not recorded.'),
 event('Removing contact has been suggested, but the export request is unchanged.'),
 ],event('A new consent receipt now covers name, region and contact.',consented=['name','region','contact'])),
case('b2-08', 'Deploy only if tests pass and rollback is ready, plus an audit unless a written exception matches both the deployment version and site. Otherwise HOLD.', 'GO', [
 event('The deployment target is version V4 at site East.',version='V4',site='East'),
 event('Tests passed for this deployment.',tests=True),
 event('Rollback is ready.',rollback=True),
 event('The audit is incomplete.',audit=False),
 event('A written exception waives the audit only for V4 at East.',ex_version='V4',ex_site='East'),
 event('The exception does not waive testing or rollback and says nothing about other sites.'),
 ],event('The deployment target changes to V4 at West.',site='West')),
case('b2-09', 'Activate only if both consumers acknowledge the latest key version and activation is authorized. Earlier-version acknowledgements do not qualify. Otherwise HOLD.', 'HOLD', [
 event('The initial key version label is K7.',version='K7'),
 event('Consumer A acknowledges K7.',ack_a='K7'),
 event('Consumer B acknowledges K7.',ack_b='K7'),
 event('Rotation advances the latest version to K8.',version='K8'),
 event('Activation authorization is recorded.',authorization=True),
 event('No K8 acknowledgements are available; forwarded K7 receipts remain old evidence.'),
 ],event('Consumers A and B now acknowledge K8.',ack_a='K8',ack_b='K8')),
case('b2-10', 'Close the incident only if two independent current checks pass and the incident owner records closure approval. A proposed monitor is not a closure prerequisite. Otherwise HOLD.', 'GO', [
 event('An earlier symptom report predates the current checks.'),
 event('Current check A passes, from acquisition P.',a=True,a_origin='P'),
 event('Current check B passes, from acquisition Q.',b=True,b_origin='Q'),
 event('P and Q are separate acquisitions; the repeated symptom emails share the old report.'),
 event('The incident owner records closure approval.',approval=True),
 event('A future monitor is proposed but not started.',monitor_started=False),
 ],event('The owner withdraws closure approval.',approval=False)),
case('b2-11', 'Grant access only if the security role and the data-owner role each approve, and the account is verified. Repeated copies of one role approval do not satisfy the other. Otherwise HOLD.', 'HOLD', [
 event('The account is verified.',verified=True),
 event('The security role approves.',security=True),
 event('A message titled second approval forwards the security receipt; its author is not the data owner.'),
 event('The data-owner role has not approved.',data_owner=False),
 event('A reminder to the data owner is sent; it is not an approval.'),
 event('The two security messages have the same receipt identifier, so they are one approval.'),
 ],event('The data-owner role now issues its own approval.',data_owner=True)),
case('b2-12', 'Release the batch only if its unchanged measured error satisfies the latest error rule and provenance is complete. Apply the stated inclusive or strict relation exactly. Otherwise HOLD.', 'GO', [
 event('The original error rule is error at most 2 units.',limit=2,inclusive=True),
 event('Measured aggregate error is 3 units.',error=3),
 event('The error rule is corrected to error at most 3 units, including equality.',limit=3,inclusive=True),
 event('This correction does not change the measured error.'),
 event('Provenance for the whole batch is complete.',provenance=True),
 event('A duplicated report copies the same measurement; it is not a second batch or a new estimate.'),
 ],event('The latest rule now requires error strictly less than 3 units; equality no longer qualifies.',limit=3,inclusive=False)),
]

def actor(c):
    return {'records':[{'id':'rule','time':'09:00','text':c['rule']}] +
            [{k:r[k] for k in ('id','time','text')} for r in c['events']]}

def fold(c):
    state={}
    for r in sorted(c['events'],key=lambda r:r['time']): state.update(r['updates'])
    return state

def decide(c):
    s=fold(c);i=c['id']
    if i=='b2-01': ok=max(s['cedar'],s['bay'])<=s['limit'] and set(s['rollback'])=={'Cedar','Bay'} and s['approval']
    elif i=='b2-02': ok=s['a_pass'] and s['b_pass'] and min(s['a_time'],s['b_time'])>s['restart'] and s['a_origin']!=s['b_origin'] and s['authorization']
    elif i=='b2-03': ok=s['restore_pass'] and s['tested']==s['target'] and s['second_copy'] and s['authorization']
    elif i=='b2-04': ok=s['start']<=s['work_start']<=s['work_end']<=s['end'] and s['rollback']
    elif i=='b2-05': ok=s['a']+s['b']<=100 and s['eligible']
    elif i=='b2-06': ok=all(s['ok'+lot[1:]] for lot in s['included'])
    elif i=='b2-07': ok=set(s['requested'])<=set(s['consented']) and s['destination']
    elif i=='b2-08': ok=s['tests'] and s['rollback'] and (s['audit'] or (s['version'],s['site'])==(s['ex_version'],s['ex_site']))
    elif i=='b2-09': ok=s['ack_a']==s['ack_b']==s['version'] and s['authorization']
    elif i=='b2-10': ok=s['a'] and s['b'] and s['a_origin']!=s['b_origin'] and s['approval']
    elif i=='b2-11': ok=s['security'] and s['data_owner'] and s['verified']
    elif i=='b2-12': ok=(s['error']<=s['limit'] if s['inclusive'] else s['error']<s['limit']) and s['provenance']
    else: raise ValueError(i)
    return 'GO' if ok else 'HOLD'

def reference(c):
    """Independent reverse-query implementation, no fold/decide reuse.

    This is same-author arithmetic checking, not independent human validation.
    """
    def latest(k):
        for r in sorted(c['events'],key=lambda r:r['time'],reverse=True):
            if k in r['updates']:return r['updates'][k]
        raise KeyError(k)
    g=latest;i=c['id']
    if i=='b2-01': checks=[g('cedar')<=g('limit'),g('bay')<=g('limit'),'Cedar' in g('rollback'),'Bay' in g('rollback'),g('approval')]
    elif i=='b2-02': checks=[g('a_pass'),g('b_pass'),g('a_time')>g('restart'),g('b_time')>g('restart'),len({g('a_origin'),g('b_origin')})==2,g('authorization')]
    elif i=='b2-03': checks=[g('tested')==g('target'),g('restore_pass'),g('second_copy'),g('authorization')]
    elif i=='b2-04': checks=[g('work_start')>=g('start'),g('work_end')<=g('end'),g('work_end')>=g('work_start'),g('rollback')]
    elif i=='b2-05': checks=[g('a')<=100-g('b'),g('eligible')]
    elif i=='b2-06': checks=[not any(lot in g('included') and not g('ok'+lot[1:]) for lot in ['L1','L2','L3'])]
    elif i=='b2-07': checks=[not set(g('requested')).difference(g('consented')),g('destination')]
    elif i=='b2-08': checks=[g('tests'),g('rollback'),g('audit') or (g('version')==g('ex_version') and g('site')==g('ex_site'))]
    elif i=='b2-09': checks=[g('ack_a')==g('version'),g('ack_b')==g('version'),g('authorization')]
    elif i=='b2-10': checks=[g('a'),g('b'),len({g('a_origin'),g('b_origin')})==2,g('approval')]
    elif i=='b2-11': checks=[g('security'),g('data_owner'),g('verified')]
    elif i=='b2-12': checks=[g('provenance'),g('error')<g('limit') or (g('error')==g('limit') and g('inclusive'))]
    else: raise ValueError(i)
    return 'GO' if all(checks) else 'HOLD'

def mutated(c):
    out=deepcopy(c);out['events'].append(out.pop('mutation'));out['expected']='HOLD' if c['expected']=='GO' else 'GO';return out

def gold(c):
    # Full event meanings, including supersession and scope, are explicit targets.
    p=actor(c)
    return {'decision':c['expected'],'targets':[{'id':r['id'],'source_span':r['text'],'required_meaning':r['text']} for r in p['records']]}

def copy_output(c):
    return {'handoff':'\n'.join(f"{r['id']} [{r['time']}] {r['text']}" for r in actor(c)['records']), 'decision':decide(c)}

def source_controller(packet):
    """Frozen authored-vocabulary parser/controller on actor-visible source only.

    A narrow engineered baseline, never a free-prose scorer or learned model.
    Unknown wording fails closed rather than guessing. Mapping rules encode the
    authored event semantics, not target decisions or future information.
    """
    records=packet['records']
    matches=[c for c in CASES if any(r['text']==c['rule'] for r in records)]
    if len(matches)!=1:raise ValueError('unknown_or_conflicting_rule')
    template=matches[0];vocabulary={r['text']:r['updates'] for r in template['events']+[template['mutation']]}
    parsed=[]
    for r in records:
        if r['text']==template['rule']:continue
        if r['text'] not in vocabulary:raise ValueError('unknown_record')
        parsed.append({'id':r['id'],'time':r['time'],'text':r['text'],'updates':deepcopy(vocabulary[r['text']])})
    return decide({'id':template['id'],'events':parsed})

def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=False)
