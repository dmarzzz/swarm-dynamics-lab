"""Receipt total contract: no annotation-aligned extraction, explicit abstention."""
import collections,re
from decimal import Decimal,InvalidOperation

def amount(text):
    if not isinstance(text,str):return None
    s=re.sub(r'^(?:rp\.?|idr)\s*','',text.strip(),flags=re.I).strip()
    if re.fullmatch(r'\d+',s):return str(Decimal(s).quantize(Decimal('.01')))
    # Both conventional punctuation orders, with unambiguous grouped thousands.
    for group,decimal in [(',',r'\.'),(r'\.',',')]:
        if re.fullmatch(r'\d{1,3}(?:'+group+r'\d{3})+(?:'+decimal+r'\d{2})?',s):
            g=group.replace('\\','');d=decimal.replace('\\','')
            return str(Decimal(s.replace(g,'').replace(d,'.')).quantize(Decimal('.01')))
    if re.fullmatch(r'\d+[.,]\d{2}',s):return str(Decimal(s.replace(',','.')).quantize(Decimal('.01')))
    return None

ANCHOR=re.compile(r'\b(?:grand\s+total|total\s+bayar|jumlah\s+bayar|total)\b',re.I)
EXCLUDE=re.compile(r'\b(?:sub\s*total|subtotal|qty|quantity|items?|cash|change|kembali|tunai|tax|pajak|service)\b',re.I)
NUMBER=re.compile(r'(?<![\w.,-])(?:Rp\.?\s*)?\d[\d.,]*(?![\w.,])',re.I)

def extract(lines):
    found=[]
    for line in lines:
        text=line['text'];anchor=ANCHOR.search(text)
        if not anchor or EXCLUDE.search(text):continue
        tail=text[anchor.end():].strip(' :\t');value=amount(tail)
        if value is not None:found.append((value,line['confidence']))
    values={v for v,c in found}
    if not values:return {'status':'missing','value':None,'confidence':0.}
    if len(values)>1:return {'status':'ambiguous','value':None,'confidence':0.}
    value=next(iter(values));return {'status':'ok','value':value,'confidence':max(c for v,c in found)}

def reference(gt):
    # Gold parser uses annotated field labels, never actor OCR line anchors.
    texts=[' '.join(w['text'] for w in line['words']) for line in gt['valid_line'] if line['category']=='total.total_price']
    if not texts:return {'status':'missing','value':None}
    parsed=[amount(t) for t in texts]
    if any(v is None for v in parsed) or len(set(parsed))!=1:return {'status':'ambiguous','value':None}
    return {'status':'ok','value':parsed[0]}

def consensus(candidates):
    # Dictionary keys are pipeline identities; one source cannot vote twice.
    counts=collections.Counter(c['value'] for c in candidates.values() if c['status']=='ok')
    if not counts:return None
    ranked=counts.most_common()
    return ranked[0][0] if ranked[0][1]>=2 and (len(ranked)==1 or ranked[0][1]>ranked[1][1]) else None

def highest(candidates):
    valid=[(c['confidence'],k,c['value']) for k,c in candidates.items() if c['status']=='ok']
    return max(valid,key=lambda x:(x[0],x[1]))[2] if valid else None

def actor(record):return {k:dict(record['pipelines'][k]['candidate']) for k in 'ABC'}
ARMS=('fixed-B','confidence','agreement','always-check','selective-check')

def run_policy(initial,checker,arm):
    if arm not in ARMS:raise ValueError('unknown policy')
    visible={k:dict(v) for k,v in initial.items()};events=[];used=[]
    if arm=='fixed-B':value=visible['B']['value'] if visible['B']['status']=='ok' else None
    elif arm=='confidence':value=highest(visible)
    else:
        value=consensus(visible)
        for tool in ('D','E') if arm in ['always-check','selective-check'] else ():
            if arm=='selective-check' and value is not None:break
            before={k:dict(v) for k,v in visible.items()};response=checker(tool);used.append(tool);visible[tool]=dict(response);value=consensus(visible)
            events.append({'tool':tool,'before':before,'response':dict(response),'after_value':value})
    return {'value':value,'action':'refer' if value is None else 'accept','checks':used,'events':events}

def grade(result,gold):
    if gold['status']!='ok':return {'scorable':False,'correct':False,'wrong':False,'refer':result['action']=='refer'}
    refer=result['action']=='refer';return {'scorable':True,'correct':not refer and result['value']==gold['value'],'wrong':not refer and result['value']!=gold['value'],'refer':refer}
