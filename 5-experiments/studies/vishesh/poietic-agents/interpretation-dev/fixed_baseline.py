"""Hand-authored fixed router for INSPECTED DEVELOPMENT fixtures, not native evidence.

No label file, network, provider or evaluator access. The supported policy grammar
is intentionally visible; a complete solution is not hidden to favor adaptation.
"""
import copy,json
from decimal import Decimal

POLICIES={
 'dispatch':[
  'Dispatch urgent orders first. Break ties by earlier due_day, then order ID.',
  'Dispatch earliest due_day first. Break ties by order ID.'],
 'returns':[
  'Refund if days_since_delivery <= 14 and opened is false. Damaged items qualify regardless of opened status, but the day limit still applies.',
  'Refund if days_since_delivery <= 14 and opened is false. Damaged items qualify regardless of opened status and day limit.'],
 'temperature':[
  'Hold batch if any reading is above 8 Celsius. Convert Fahrenheit using (F - 32) * 5 / 9. Equality does not trigger hold.',
  'Hold batch if any reading is at or above 8 Celsius. Convert Fahrenheit using (F - 32) * 5 / 9. Equality triggers hold.'],
 'capacity':[
  'Use the newest signed capacity report at or before decision_day. Unsigned reports are advisory. Reserve quantity only if available >= quantity; otherwise wait.']}

def public_context(case):
    source=case['public']
    return copy.deepcopy({'task':{k:source['task'][k] for k in ('kind','instruction')},
        'documents':[{k:d[k] for k in ('id','kind','version','body')} for d in source['documents']]})

def integer(x):
    if type(x) is not int:raise ValueError('integer')
    return x

def boolean(x):
    if type(x) is not bool:raise ValueError('boolean')
    return x

def decide(context):
    relevant=[d for d in context['documents'] if d['kind'] in ('policy','facts')]
    citations=sorted({d['id'] for d in relevant})
    unknown={'status':'insufficient_evidence','value':None,'citations':citations}
    try:
        unique={json.dumps(d,sort_keys=True):d for d in relevant};docs=list(unique.values())
        policy,= [d for d in docs if d['kind']=='policy'];facts,=[d for d in docs if d['kind']=='facts']
        kind=context['task']['kind'];version=POLICIES[kind].index(policy['body']);f=facts['body']
        if kind=='dispatch':
            orders=f['orders']
            if not orders:raise ValueError('no_orders')
            for o in orders:
                integer(o['due_day']);boolean(o['urgent'])
                if not isinstance(o['id'],str):raise ValueError('id')
            key=(lambda o:(not o['urgent'],o['due_day'],o['id'])) if version==0 else (lambda o:(o['due_day'],o['id']))
            value=min(orders,key=key)['id']
        elif kind=='returns':
            days=integer(f['days_since_delivery']);opened=boolean(f['opened']);damaged=boolean(f['damaged'])
            value=(days<=14 and (not opened or damaged)) if version==0 else ((days<=14 and not opened) or damaged)
        elif kind=='temperature':
            values=[]
            for row in f['readings']:
                x=Decimal(row['value']);unit=row['unit']
                if not x.is_finite() or unit not in ('F','C'):raise ValueError('unit')
                values.append((x-32)*5/9 if unit=='F' else x)
            if not values:raise ValueError('empty')
            value=any(x>8 for x in values) if version==0 else any(x>=8 for x in values)
        else:
            day=integer(f['decision_day']);qty=integer(f['quantity'])
            available=[r for r in f['reports'] if boolean(r['signed']) and integer(r['day'])<=day]
            latest=max(integer(r['day']) for r in available)
            levels={integer(r['available']) for r in available if r['day']==latest}
            if len(levels)!=1:raise ValueError('conflicting_authority')
            value='reserve' if levels.pop()>=qty else 'wait'
        return dict(status='answer',value=value,citations=citations)
    except (ValueError,KeyError,TypeError,ArithmeticError):return unknown

def valid_output(result,kind):
    if not isinstance(result,dict) or set(result)!={'status','value','citations'}:return False
    if not isinstance(result['citations'],list) or not all(isinstance(x,str) for x in result['citations']):return False
    if result['status']=='insufficient_evidence':return result['value'] is None
    if result['status']!='answer':return False
    return type(result['value']) is (bool if kind in ('returns','temperature') else str)
