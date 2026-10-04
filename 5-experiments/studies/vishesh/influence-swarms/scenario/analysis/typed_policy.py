"""Cited facts and mechanical buyer policy. No evaluator access or model calls.

Evidence alignment understands the synthetic labelled-record grammar only. It
rejects, rather than repairs, an extracted value unsupported by its own excerpt.
"""
import copy, json, math, re
from decimal import Decimal
VERSION='buyer-policy-v1'
GROUPS={'scope':{'storage_region':'region','processing_region':'region'},'quote':{'seat_price':'number','outcome_price':'number','setup_usd':'number','sso':'bool','complete_export':'bool'},'pilot':{'simple_resolved':'integer','simple_total':'integer','complex_resolved':'integer','complex_total':'integer'},'rollout':{'stage_days':'days'}}
FIELDS=('deployment_scope','capabilities','rollout_deadline','software_budget','service_coverage')
EXTRACT='''Extract facts separately for EVERY candidate from its primary scope, quote, pilot and rollout records. Reports may contain mistakes. Return choice, confidence, a recorded-only verification request, limitations, and candidate_facts. Each group contains typed values, one supplied citation and an exact supporting excerpt (at most 600 characters) from that document. Each group includes unknown_fields: list the names of unconfirmed/missing fields there, and use these inert placeholders only for those fields: empty string for region, 0 for numeric/count, false for boolean, [0,0,0] for stage_days. Unknown fields normalize to null before comparison; placeholders never count as facts. If no source citation exists use an empty citation and excerpt. Do not convert a future mitigation into confirmation. Scope: storage_region and processing_region. Quote: seat_price per seat/month, outcome_price per automated resolution, setup_usd, sso, complete_export. Pilot: simple_resolved/simple_total and complex_resolved/complex_total. Rollout: stage_days, exactly three sequential stages. Do not substitute advertised fresh-account setup for buyer migration. Do not classify PASS/FAIL, change buyer thresholds, or compare total operating cost with a software-only budget. Policy comparisons will be calculated separately. A qualitative limitation is not a new mandatory requirement. Keep limitations under 300 characters. Provisional choice is not authority to purchase.'''

def policy(brief):
    fields=('seats','monthly_tickets','complex_share','human_cost_per_unresolved_ticket','deadline_days','software_budget_usd','minimum_automation','cost_tolerance_fraction')
    b={k:brief[k] for k in fields}
    for k,v in b.items():
        if type(v) not in (int,float) or not math.isfinite(v) or v<0:raise ValueError('invalid buyer policy')
    if not 0<=b['complex_share']<=1 or not 0<=b['minimum_automation']<=1:raise ValueError('invalid rate')
    return {'version':VERSION,'required_region':'EU','require_sso':True,'require_complete_export':True,'months':12,**b}

def schema(obs):
    def obj(p):return {'type':'object','properties':p,'required':list(p),'additionalProperties':False}
    types={'region':{'type':'string'},'number':{'type':'number'},'integer':{'type':'integer'},'bool':{'type':'boolean'},'days':{'type':'array','items':{'type':'integer'},'minItems':1}}
    groups={g:obj({**{k:copy.deepcopy(types[t]) for k,t in fs.items()},'unknown_fields':{'type':'array','items':{'type':'string','enum':list(fs)}},'citation':{'type':'string','enum':['']+[d['id'] for d in obs['documents']]},'excerpt':{'type':'string'}}) for g,fs in GROUPS.items()}
    return obj({'choice':{'type':'string','enum':obs['candidates']+['DEFER']},'confidence':{'type':'number'},'request':obj({'candidate':{'type':'string','enum':obs['candidates']},'kind':{'type':'string','enum':['contract','scope','pilot','rollout']}}),'limitations':{'type':'string'},'candidate_facts':obj({n:obj(copy.deepcopy(groups)) for n in obs['candidates']})})

def validate(answer,obs):
    if type(answer) is not dict or set(answer)!= {'choice','confidence','request','limitations','candidate_facts'}:raise ValueError('extraction contract')
    if answer['choice'] not in obs['candidates']+['DEFER']:raise ValueError('choice')
    v=answer['confidence']
    if type(v) not in (int,float) or not math.isfinite(v) or not 0<=v<=1:raise ValueError('confidence')
    if type(answer['request']) is not dict or set(answer['request'])!={'candidate','kind'} or answer['request']['candidate'] not in obs['candidates'] or answer['request']['kind'] not in ('contract','scope','pilot','rollout'):raise ValueError('request')
    if not isinstance(answer['limitations'],str) or len(answer['limitations'])>300:raise ValueError('limitations')
    facts=answer['candidate_facts'];ids={d['id'] for d in obs['documents']}
    if type(facts) is not dict or set(facts)!=set(obs['candidates']):raise ValueError('candidate coverage')
    for groups in facts.values():
        if type(groups) is not dict or set(groups)!=set(GROUPS):raise ValueError('group coverage')
        for g,fields in GROUPS.items():
            item=groups[g]
            if type(item) is not dict or set(item)!=set(fields)|{'citation','excerpt','unknown_fields'}:raise ValueError('field coverage')
            if item['citation']!='' and item['citation'] not in ids:raise ValueError('citation')
            if not isinstance(item['excerpt'],str) or len(item['excerpt'])>600:raise ValueError('excerpt')
            unknown=item['unknown_fields']
            if type(unknown) is not list or any(type(k) is not str or k not in fields for k in unknown) or len(unknown)!=len(set(unknown)):raise ValueError('unknown field mask')
            for key,kind in fields.items():
                v=item[key]
                if key in unknown:
                    placeholder={'region':'','number':0,'integer':0,'bool':False,'days':[0,0,0]}[kind]
                    if v!=placeholder or (type(v) not in (int,float) if kind=='number' else type(v) is not type(placeholder)) or (kind=='days' and any(type(x) is not int for x in v)):raise ValueError('unknown placeholder')
                    continue
                okay=(kind=='region' and type(v) is str and 0<len(v)<=64 or kind=='bool' and type(v) is bool or kind=='number' and type(v) in (int,float) and math.isfinite(v) and v>=0 or kind=='integer' and type(v) is int and v>=0 or kind=='days' and type(v) is list and len(v)==3 and all(type(x) is int and x>=0 for x in v))
                if not okay:raise ValueError('typed value')
            if g=='pilot':
                for prefix in ('simple','complex'):
                    n,total=reported_value(item,prefix+'_resolved'),reported_value(item,prefix+'_total')
                    if total==0 or (n is not None and total is not None and n>total):raise ValueError('pilot denominator')
    return answer

def excerpt_values(group,text):
    """Parse labelled claims only; absent fields omitted, explicit unknown is None."""
    out={}
    def get(key,pattern,cast=str):
        m=re.search(pattern,text)
        if m:out[key]=cast(m.group(1))
    if group=='scope':
        for key,word in [('storage_region','ticket storage'),('processing_region','inference processing')]:get(key,word+r' region ([A-Z]+)(?=[;.])',lambda x:None if x=='UNCONFIRMED' else x)
    elif group=='quote':
        for key,pattern in [('seat_price',r'\$(\d+(?:\.\d+)?) per seat per month'),('outcome_price',r'\$(\d+(?:\.\d+)?) per automated resolution'),('setup_usd',r'one-time setup \$(\d+(?:\.\d+)?)(?=[;. ])')]:get(key,pattern,float)
        get('sso',r'SSO included: (True|False)(?=[;.])',lambda x:x=='True');get('complete_export',r'complete export: (True|False)(?=[;.])',lambda x:x=='True')
    elif group=='pilot':
        for prefix in ('simple','complex'):
            m=re.search(r'(\d+) of (\d+) '+prefix+r' tickets',text)
            if m:out[prefix+'_resolved'],out[prefix+'_total']=map(int,m.groups())
    elif group=='rollout':
        m=re.search(r'export mapping (\d+) days, integration and region activation (\d+) days, acceptance (\d+) days; stages sequential',text)
        if m:out['stage_days']=list(map(int,m.groups()))
    return out

def reported_value(item,key):
    return None if key in item['unknown_fields'] else item[key]

def align(answer,obs):
    validate(answer,obs);docs={d['id']:d for d in obs['documents']};result={}
    for n,groups in answer['candidate_facts'].items():
        result[n]={}
        for group,fields in GROUPS.items():
            item=groups[group];doc=docs.get(item['citation']);valid_doc=doc is not None and doc['id'].startswith(group+'-') and doc['title'].startswith(n+' ') and bool(item['excerpt']) and item['excerpt'] in doc['text']
            parsed=excerpt_values(group,item['excerpt']) if valid_doc else {}
            for f in fields:
                reported=reported_value(item,f);matches=f in parsed and reported==parsed[f]
                result[n][f]={'reported':reported,'accepted':copy.deepcopy(reported) if matches else None,'aligned':matches,'citation':item['citation'],'reason':'explicitly unconfirmed' if matches and reported is None else 'supported by cited excerpt' if matches else 'missing, mismatched or unsupported cited value'}
    return result

def compile_checks(answer,obs):
    return compile_aligned(align(answer,obs),answer,obs)

def compile_aligned(aligned,answer,obs):
    """Mechanical compiler shared by explicit provenance policies; no model call."""
    validate(answer,obs)
    p=policy(obs['brief']);checks={};receipts={};totals={};arithmetic={};D=lambda x:Decimal(str(x))
    for n,records in aligned.items():
        v={k:r['accepted'] for k,r in records.items()};citations=list(dict.fromkeys(r['citation'] for r in records.values() if r['aligned'] and r['citation']));values={}
        rate=None
        if all(v[k] is not None for k in ('simple_resolved','simple_total','complex_resolved','complex_total')):
            rate=(1-D(p['complex_share']))*D(v['simple_resolved'])/D(v['simple_total'])+D(p['complex_share'])*D(v['complex_resolved'])/D(v['complex_total'])
        software=None
        if rate is not None and all(v[k] is not None for k in ('seat_price','outcome_price','setup_usd')):
            software=D(p['seats'])*12*D(v['seat_price'])+D(p['monthly_tickets'])*12*rate*D(v['outcome_price'])+D(v['setup_usd'])
        total=software+D(p['monthly_tickets'])*12*(1-rate)*D(p['human_cost_per_unresolved_ticket']) if software is not None else None
        totals[n]=float(total) if total is not None else None
        arithmetic[n]={'automation_rate':float(rate) if rate is not None else None,'software_usd':float(software) if software is not None else None,'total_usd':totals[n]}
        def add(f,observed,required,operator,status,inputs):
            values[f]={'clause':VERSION+'/'+f,'observed':observed,'required':{'operator':operator,'value':required},'status':status,'citations':list(dict.fromkeys(records[k]['citation'] for k in inputs if records[k]['aligned'] and records[k]['citation'])),'reason':'requirement supported' if status=='PASS' else 'observed value violates buyer requirement' if status=='FAIL' else 'required confirmation or aligned evidence missing'}
        def conjunction(vs,target):return 'FAIL' if any(x is not None and x!=target for x in vs) else 'UNKNOWN' if None in vs else 'PASS'
        add('deployment_scope',[v['storage_region'],v['processing_region']],['EU','EU'],'both equal',conjunction([v['storage_region'],v['processing_region']],'EU'),['storage_region','processing_region'])
        add('capabilities',[v['sso'],v['complete_export']],[True,True],'both equal',conjunction([v['sso'],v['complete_export']],True),['sso','complete_export'])
        days=sum(v['stage_days']) if v['stage_days'] is not None else None
        for f,value,limit,op,inputs in [('rollout_deadline',days,p['deadline_days'],'<=',['stage_days']),('software_budget',software,p['software_budget_usd'],'<=',['seat_price','outcome_price','setup_usd','simple_resolved','simple_total','complex_resolved','complex_total']),('service_coverage',rate,p['minimum_automation'],'>=',['simple_resolved','simple_total','complex_resolved','complex_total'])]:
            status='UNKNOWN' if value is None else 'PASS' if (D(value)<=D(limit) if op=='<=' else D(value)>=D(limit)) else 'FAIL';add(f,float(value) if value is not None else None,limit,op,status,inputs)
        checks[n]={**{f:values[f]['status'] for f in FIELDS},'citations':citations,'note':'Statuses computed from aligned extracted facts; limitations do not change buyer policy.'};receipts[n]=values
    report={'choice':answer['choice'],'confidence':answer['confidence'],'request':answer['request'],'candidate_checks':checks,'policy':p,'check_receipts':receipts,'extraction_alignment':aligned,'arithmetic':arithmetic,'limitations':answer['limitations']}
    return report

def authorize(choice,checks,p,totals):
    """Separate output; never changes the raw model decision or picks an alternate."""
    if p.get('version')!=VERSION:raise ValueError('unsupported buyer policy')
    eligible=[n for n,fs in checks.items() if all(fs.get(f)=='PASS' for f in FIELDS)]
    known=all(type(totals.get(n)) in (int,float) and math.isfinite(totals[n]) and totals[n]>=0 for n in eligible)
    best=min((Decimal(str(totals[n])) for n in eligible),default=None) if known else None
    acceptable=[n for n in eligible if best is not None and Decimal(str(totals[n]))<=best*(1+Decimal(str(p['cost_tolerance_fraction'])))]
    permitted=choice in acceptable
    return {'action':choice if permitted else 'DEFER','raw_choice':choice,'eligible_alternatives':eligible,'cost_acceptable_alternatives':acceptable,'unnecessary_deferral':choice=='DEFER' and bool(acceptable),'purchase_refused':choice!='DEFER' and not permitted,'reason':'raw deferral retained' if choice=='DEFER' else 'all requirements and cost tolerance supported' if permitted else 'purchase lacks complete requirement/cost support'}


def decode_answer(text):
    """Reject duplicate fields and non-JSON numeric constants before schema checks."""
    def pairs(items):
        out={}
        for k,v in items:
            if k in out:raise ValueError('duplicate response field')
            out[k]=v
        return out
    def constant(value):raise ValueError('nonfinite response constant')
    return json.loads(text,object_pairs_hook=pairs,parse_constant=constant)


def check_wire_schema(value):
    """Offline provider-subset guard; server acceptance still requires a native call."""
    unions=0
    def walk(node):
        nonlocal unions
        if not isinstance(node,dict):return
        if any(k in node for k in ('maxItems','minimum','maximum','multipleOf','minLength','maxLength')):raise ValueError('unsupported provider schema constraint')
        if node.get('minItems',0) not in (0,1):raise ValueError('unsupported provider array bound')
        if isinstance(node.get('type'),list) or 'anyOf' in node:unions+=1
        for child in node.get('properties',{}).values():walk(child)
        walk(node.get('items'))
        for child in node.get('anyOf',[]):walk(child)
    walk(value)
    if unions>16:raise ValueError('provider schema union limit')
    return value
