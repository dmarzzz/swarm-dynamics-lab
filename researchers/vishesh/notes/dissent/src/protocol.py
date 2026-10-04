"""Bounded challenge state machine. Policies receive only whitelisted actor fields."""
from copy import deepcopy
from dataclasses import dataclass, field
from cases import digest

ACTIONS = ('PROCEED', 'HOLD', 'DEFER')
ARMS = ('majority', 'blind-veto', 'always-check', 'evidence-gate', 'matched-random', 'pooled', 'exact-reference')

def majority(votes):
    if not votes or any(v not in ACTIONS for v in votes):
        raise ValueError('invalid_votes')
    p, h = votes.count('PROCEED'), votes.count('HOLD')
    return 'PROCEED' if p > h else 'HOLD' if h > p else 'DEFER'

def actor_packet(case, check=None):
    task = case['task']
    packet = {'task': {k: deepcopy(task[k]) for k in ('scope','revision','now','ttl','deadline','instructions')},
              'records': [{k: deepcopy(e[k]) for k in ('id','root','scope','revision','observed_at','text')} for e in case['evidence']],
              'votes': list(case['votes']), 'challenge': None}
    c = case.get('challenge')
    if c:
        packet['challenge'] = {k: deepcopy(c[k]) for k in ('claim','alternative','evidence_ids','check','withdraw_if','expires_at')}
    if check:
        packet['check_record'] = {k: deepcopy(check[k]) for k in ('id','root','scope','revision','observed_at','text')}
    return packet


def validate_challenge(packet, closed):
    c, t = packet['challenge'], packet['task']
    if c is None: return False, 'absent', None
    if c['alternative'] not in ACTIONS[:2] or c['withdraw_if'] not in ACTIONS[:2] or c['alternative'] == c['withdraw_if']:
        return False, 'invalid_alternative', None
    if c['check'] != 'independent-check': return False, 'unallowed_check', None
    if type(c['expires_at']) is not int or c['expires_at'] < t['now']:
        return False, 'expired', None
    ids = c['evidence_ids']
    records = {e['id']:e for e in packet['records']}
    if not isinstance(ids, list) or not ids or len(ids) != len(set(ids)) or any(i not in records for i in ids):
        return False, 'invalid_reference', None
    chosen = [records[i] for i in ids]
    if any(e['scope'] != t['scope'] or e['revision'] != t['revision'] for e in chosen):
        return False, 'wrong_scope', None
    if any(e['observed_at'] > t['now'] or t['now']-e['observed_at'] > t['ttl'] for e in chosen):
        return False, 'stale_or_future', None
    # Alias IDs do not create fresh evidence. Time/source/content/version do.
    lineage = sorted({(e['root'], e['scope'], e['revision'], e['observed_at'], e['text']) for e in chosen})
    key = digest({'scope':t['scope'],'revision':t['revision'],'lineage':lineage})
    if key in closed: return False, 'already_closed', key
    return True, 'valid', key

@dataclass
class Ledger:
    max_checks: int = 1
    checks: int = 0
    closed: set = field(default_factory=set)
    resolutions: dict = field(default_factory=dict)
    current: dict | None = None


def choose(policy, phase, packet):
    result = policy(phase, deepcopy(packet))
    allowed = ('CHECK','KEEP','DEFER') if phase == 'admission' else ACTIONS
    if result not in allowed: raise ValueError('invalid_policy_action')
    return result


def step(case, arm, policy, ledger=None, *, random_check=None):
    if arm not in ARMS: raise ValueError('unknown_arm')
    if arm=='matched-random' and type(random_check) is not bool:raise ValueError('frozen_random_assignment_required')
    ledger = ledger or Ledger()
    packet = actor_packet(case); initial = majority(packet['votes']); now = packet['task']['now']
    cached = ledger.current
    applicable = cached is not None and cached['scope']==packet['task']['scope'] and cached['revision']==packet['task']['revision'] and cached['request_tick']<=now and now-cached['observed_at']<=packet['task']['ttl']
    current = cached['action'] if applicable else ('DEFER' if cached is not None else initial)
    if arm == 'majority': current = initial
    packet['current_decision'] = current
    for oldkey, resolved in list(ledger.resolutions.items()):
        if resolved['scope'] != packet['task']['scope'] or resolved['revision'] != packet['task']['revision'] or not (resolved['request_tick']<=now and now-resolved['observed_at']<=packet['task']['ttl']):
            ledger.closed.discard(oldkey)
    events = [{'phase':'initial','tick':now,'action':initial,'votes':packet['votes'],
               'unique_sources':len({e['root'] for e in packet['records']})}]
    action, status, reason, admitted, used = current, 'completed', 'no_intervention', False, False
    valid, validity, key = validate_challenge(packet, ledger.closed)
    events.append({'phase':'challenge','tick':now,'valid':valid,'reason':validity,
                   'alternative':packet['challenge']['alternative'] if packet['challenge'] else None})
    try:
        if arm not in ('majority','pooled') and validity == 'already_closed':
            action = ledger.resolutions[key]['action']; now=max(now,ledger.resolutions[key]['observed_at']); reason = 'retained_closure'
        elif arm == 'pooled':
            action = choose(policy, 'resolve', packet)
            reason = 'pooled_evidence'
        elif arm != 'majority' and valid:
            if arm == 'blind-veto':
                action = packet['challenge']['alternative']; reason = 'unconditional_reversal'
            else:
                gate = choose(policy, 'admission', packet) if arm == 'evidence-gate' else ('CHECK' if arm != 'matched-random' or random_check else 'KEEP')
                events.append({'phase':'admission','tick':now,'action':gate})
                if gate == 'DEFER': action, reason = 'DEFER', 'admission_deferred'
                elif gate == 'CHECK':
                    admitted = True
                    if ledger.checks >= ledger.max_checks:
                        action, reason = 'DEFER', 'check_budget_exhausted'
                    else:
                        ledger.checks += 1; used = True
                        v = case['verification']; now += v['delay']
                        if not v['available']:
                            action, status, reason = 'DEFER', 'unavailable', 'check_unavailable'
                            events.append({'phase':'verification','tick':now,'status':'unavailable'})
                        else:
                            observed = deepcopy(v['record']); observed['observed_at'] = now
                            events.append({'phase':'verification','tick':now,'status':'observed','record':observed})
                            if now > packet['task']['deadline']:
                                action, status, reason = 'DEFER', 'late', 'deadline_missed'
                            else:
                                revised = actor_packet(case, observed)
                                revised['task']['now'] = now
                                revised['current_decision'] = current
                                action = choose(policy, 'resolve', revised); reason = 'checked'
                                if action != 'DEFER':
                                    ledger.closed.add(key)
                                    ledger.resolutions[key]={'action':action,'scope':packet['task']['scope'],'revision':packet['task']['revision'],'observed_at':now,'request_tick':packet['task']['now']}
                                    ledger.current=dict(ledger.resolutions[key])
                else: reason = 'challenge_not_admitted'
        elif arm != 'majority': reason = validity
    except Exception as exc:
        # Fixed error type only; a provider's message could contain request/credential data.
        action, status, reason = 'DEFER', 'failed', type(exc).__name__
    if arm == 'pooled' and action != 'DEFER' and status == 'completed':
        applicable_records=[e for e in packet['records'] if e['scope']==packet['task']['scope'] and e['revision']==packet['task']['revision'] and 0<=now-e['observed_at']<=packet['task']['ttl']]
        if applicable_records:ledger.current={'action':action,'scope':packet['task']['scope'],'revision':packet['task']['revision'],'observed_at':max(e['observed_at'] for e in applicable_records),'request_tick':now}
    if action == 'DEFER' and status == 'completed': status = 'unresolved'
    closure = ('supported' if action == packet['challenge']['alternative'] else 'withdrawn') if key in ledger.closed and packet['challenge'] else 'open'
    if validity == 'already_closed': closure = 'suppressed_repeat'
    events.append({'phase':'resolution','tick':now,'action':action,'status':status,'reason':reason,'closure':closure})
    gold = case['gold']['action']
    completed = status == 'completed' and action != 'DEFER' and now <= packet['task']['deadline']
    return {'case_id':case['case_id'], 'scenario':case['scenario'], 'arm':arm, 'events':events,
            'actor':packet,'evaluator':{'gold_action':gold}, 'initial':initial, 'final':action,
            'status':status,'reason':reason,'on_time':now<=packet['task']['deadline'],'correct_completion':completed and action==gold,
            'initial_correct':initial==gold, 'correction':completed and initial!=gold and action==gold,
            'corruption':completed and initial==gold and action!=gold,'checks':int(used), 'admitted':admitted,
            'closure':closure,'ticks':now-case['task']['now']}


def episode(case, arm, policy, *, random_check=None):
    frames = case['frames'] or [case]
    ledger = Ledger(max_checks=2 if case['frames'] else 1)
    return [step(frame,arm,policy,ledger,random_check=random_check) for frame in frames]


def summarize(records):
    n = len(records)
    initially_wrong = sum(not r['initial_correct'] for r in records)
    initially_right = n-initially_wrong
    count = lambda k:sum(bool(r[k]) for r in records)
    return {'assigned_decisions':n,'correct_on_time':count('correct_completion'),
            'correct_on_time_rate':count('correct_completion')/n if n else None,
            'wrong_initial':initially_wrong,'right_initial':initially_right,
            'corrections':count('correction'),'harmful_reversals':count('corruption'),
            'correction_rate':count('correction')/initially_wrong if initially_wrong else None,
            'harmful_reversal_rate':count('corruption')/initially_right if initially_right else None,
            'unresolved':sum(r['final']=='DEFER' for r in records),'checks':sum(r['checks'] for r in records),
            'failures':sum(r['status']=='failed' for r in records),
            'wrong_proceed':sum(r['final']=='PROCEED' and r['evaluator']['gold_action']=='HOLD' for r in records),
            'unnecessary_hold':sum(r['final']=='HOLD' and r['evaluator']['gold_action']=='PROCEED' for r in records)}
