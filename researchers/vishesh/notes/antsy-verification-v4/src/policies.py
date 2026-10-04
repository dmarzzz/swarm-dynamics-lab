"""Actors receive only confidence signals and paid QA responses, never hidden quality."""
import collections,copy,itertools,json,random
MODES=('A','B','C')
ARMS=('best-fixed','confidence-only','random-checks','decision-focused','single-agent','swarm-fixed','swarm-adaptive')
ROLES=('layout specialist','text-quality auditor','coverage skeptic','cost controller','verification coordinator')


def calibrate(records):
    bias={}
    for m in MODES:
        pairs=[(v['observations'][j]['confidence'],v['evaluation']['regions'][j]) for r in records for v in [r['modes'][m]] for j in range(3) if v['evaluation']['regions'][j] is not None]
        bias[m]=sum(y-x for x,y in pairs)/len(pairs)
    means={m:sum(r['modes'][m]['evaluation']['recall'] for r in records)/len(records) for m in MODES}
    return {'bias':bias,'best_fixed':max(MODES,key=means.get),'n':len(records)}


def initial(record,cal):
    return {'id':record['id'],'observations':{m:copy.deepcopy(record['modes'][m]['observations']) for m in MODES},'bias':dict(cal['bias']),'checks':[]}


def estimate(board,m):
    vals=[]
    for region,obs in enumerate(board['observations'][m]):
        known=next((c for c in board['checks'] if c['mode']==m and c['region']==region),None)
        if known is not None:
            if known['quality'] is not None:vals.append(known['quality'])
        else:vals.append(max(0,min(1,obs['confidence']+board['bias'][m])))
    return sum(vals)/len(vals) if vals else 0


def choose(board):return max(MODES,key=lambda m:(estimate(board,m),-MODES.index(m)))
def available(board,m):return [j for j in range(3) if not any(c['mode']==m and c['region']==j for c in board['checks'])]
def region_for(board,m):return min(available(board,m),key=lambda j:(board['observations'][m][j]['confidence'],j))


def purchase(board,truth,mode,region=None):
    if len(board['checks'])>=2:raise ValueError('budget_exhausted')
    if region is None:region=region_for(board,mode)
    if region not in available(board,mode):raise ValueError('duplicate_check')
    board['checks'].append({'mode':mode,'region':region,'quality':truth['modes'][mode]['evaluation']['regions'][region]})


def actor_input(board,role,shared):
    lines=['Two checks maximum. Choose which OCR configuration to verify next, or STOP to commit to the current estimated leader. Checks reveal annotated-token recall in its least-confident unchecked region. These confidence estimates may be wrong.']
    lines.append(f"Checks left: {2-len(board['checks'])}. Current estimated leader: {choose(board)}.")
    # Specialists see complementary confidence signals; union available to centralized baseline.
    modes=MODES if shared or role>=3 else (MODES[role],)
    for m in modes:
        obs=board['observations'][m]
        lines.append(f"{m}: estimated quality {estimate(board,m):.2f}; OCR confidence by region "+','.join(f"{o['confidence']:.2f}" for o in obs)+'.')
    for c in board['checks']:lines.append(f"Verified {c['mode']} region {c['region']}: "+('no annotated target text' if c['quality'] is None else f"actual recall {c['quality']:.2f}")+'.')
    return '\n'.join(lines)


def query_model(runtime,board,role,shared,context):
    options={m:f'Check configuration {m}' for m in MODES if available(board,m)}|{'STOP':'Stop checking and commit'}
    instructions=f'You are the {ROLES[role]}. Select the most useful next check for choosing high-quality OCR. Stop if another check is unlikely to change the choice. Consider uncertainty and the two-check limit.'
    return runtime.choose(actor_input(board,role,shared),instructions,options,context)


def policy(record,cal,arm,runtime=None,seed=71,tape=None):
    board=initial(record,cal);events=[];calls=0;error=None
    if arm=='best-fixed':return {'choice':cal['best_fixed'],'checks':[],'events':[],'logical_calls':0,'valid':True}
    if arm=='confidence-only':return {'choice':choose(board),'checks':[],'events':[],'logical_calls':0,'valid':True}
    rng=random.Random(f'{record["id"]}:{seed}')
    try:
        for step in range(2):
            before=copy.deepcopy(board);votes=[];stop=False
            if arm=='random-checks':
                m=rng.choice(MODES);purchase(board,record,m)
            elif arm=='decision-focused':
                # Exploit likely best configurations while checking their uncertain region.
                m=max(MODES,key=lambda m:estimate(board,m)+.25*(1-min(board['observations'][m][j]['confidence'] for j in available(board,m))))
                purchase(board,record,m)
            elif arm=='single-agent':
                votes=[query_model(runtime,board,4,True,{'task':record['id'],'arm':arm,'step':step,'role':4})];calls+=1;stop=votes[0]=='STOP'
                if not stop:purchase(board,record,votes[0])
            else:
                if tape is not None:votes=tape[step]
                else:
                    votes=[query_model(runtime,board,i,False,{'task':record['id'],'arm':'swarm','step':step,'role':i}) for i in range(5)]
                calls+=5;stop=arm=='swarm-adaptive' and votes.count('STOP')>=(4 if step==0 else 3)
                if not stop:
                    counts=collections.Counter(v for v in votes if v!='STOP')
                    m=max(MODES,key=lambda m:(counts[m],estimate(board,m),-MODES.index(m)))
                    purchase(board,record,m)
            events.append({'step':step,'before':before,'votes':votes,'stop':stop,'after_checks':copy.deepcopy(board['checks']),'choice':choose(board)})
            if stop:break
    except Exception as exc:error=type(exc).__name__
    return {'choice':choose(board) if not error else None,'checks':board['checks'],'events':events,'logical_calls':calls,'valid':error is None,'error':error}


def evaluate(record,result):
    scores={m:record['modes'][m]['evaluation']['recall'] for m in MODES};best=max(scores.values());q=scores[result['choice']] if result['valid'] else 0
    return {'quality':q,'oracle_quality':best,'regret':best-q,'checks':len(result['checks']),'total_field_exact':record['modes'][result['choice']]['evaluation']['total_field_exact'] if result['valid'] else False,'within_2pp_oracle':best-q<=.02,'utility_at_002':q-.02*len(result['checks'])}


def budget_oracle(record,cal):
    # Evaluator-only optimistic ceiling with up to two paid checks; not an implementable policy.
    best=0
    for checks in itertools.chain.from_iterable(itertools.combinations([(m,j) for m in MODES for j in range(3)],n) for n in range(3)):
        b=initial(record,cal)
        for m,j in checks:purchase(b,record,m,j)
        best=max(best,record['modes'][choose(b)]['evaluation']['recall'])
    return best
