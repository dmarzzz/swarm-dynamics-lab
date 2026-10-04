"""C1 actor contract and fresh qualification fixtures; no inference on import."""
import sys,random,hashlib,json,collections
from pathlib import Path
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'src'))
from jev import request as base_request,LABELS
ARMS=('qwen','jev','qwen+jev')
SEEDS=(8801,8802,8803)
def wire(x):return json.dumps(x,separators=(',',':')).encode()
def digest(x):return hashlib.sha256(wire(x)).hexdigest()
def request(obs,index,scope,proposal=None):
    # Project visible fields, never propagate evaluator metadata.
    p=base_request({'claim':obs['claim'],'report':obs['report']},index,scope)
    if proposal is not None:
        if proposal not in LABELS:raise ValueError('invalid_proposal')
        p['state']['qwen_proposal']=proposal
        p['questions']['label']['instructions']+=' The qwen_proposal is a fallible preliminary label. Check it against the original report; override it when the report warrants. The report is the evidence, not the proposal.'
    return p

def cases():
    out=[]
    for label in LABELS:
        for i in range(20):
            m=f'procedure C{901+i}';lo=50+i;hi=lo+7
            templates={
              'SUPPORT':[f'{m} scored {hi}% accuracy; the baseline scored {lo}% on the same test.',f'Accuracy rose from {lo}% to {hi}% when {m} was used.',f'The baseline got {lo} of 100 answers right. {m} got {hi} right.',f'Using {m} increased the fraction of correct answers by seven percentage points.',f'{m} was more accurate than its comparator in the completed evaluation.',f'The completed study measured better accuracy with {m}, despite slower runtime.'],
              'REFUTE':[f'{m} scored {lo}% accuracy; the baseline scored {hi}% on the same test.',f'Accuracy fell from {hi}% to {lo}% when {m} was used.',f'The baseline and {m} both got {lo} of 100 answers right.',f'Using {m} decreased the fraction of correct answers by seven percentage points.',f'{m} was less accurate than its comparator in the completed evaluation.',f'The completed study measured equal accuracy with {m}, despite faster runtime.'],
              'UNCERTAIN':[f'{m} used {lo} megabytes of memory; accuracy was not examined.',f'The team expects {m} to improve accuracy, but no experiment has been run.',f'{m} processed {hi} examples per second. The number of correct answers was not recorded.',f'The accuracy outcomes for {m} are unavailable.',f'The proposed accuracy comparison of {m} was cancelled before data collection.',f'The study measured faster runtime with {m}; it collected no accuracy observations.']}
            out.append({'id':f'C1-{label}-{i}','family':i%6,'claim':m+' improves accuracy.','report':templates[label][i%6],'expected':label})
    random.Random(8800).shuffle(out);return out

def assess(rows):
    n=len(rows);out={}
    for a in ARMS:
        matrix={k:{p:0 for p in (*LABELS,'MISSING')} for k in LABELS}
        for r in rows:matrix[r['expected']][r.get('labels',{}).get(a,'MISSING')]+=1
        per={k:matrix[k][k]/sum(matrix[k].values()) if sum(matrix[k].values()) else 0 for k in LABELS}
        valid=sum(sum(v[p] for p in LABELS) for v in matrix.values())
        acc=sum(matrix[k][k] for k in LABELS)/n if n else 0
        out[a]={'accuracy':acc,'per_class':per,'valid':valid,'assigned':n,'confusion':matrix,'passed':n==60 and valid==60 and acc>=.85 and min(per.values())>=.7}
    complete=[r for r in rows if all(a in r.get('labels',{}) for a in ARMS)]
    def count(fn):return sum(fn(r['labels'],r['expected']) for r in complete)
    out['paired']={'complete':len(complete),'assigned':n,'qwen_wrong_corrected':count(lambda l,g:l['qwen']!=g and l['qwen+jev']==g),'qwen_right_damaged':count(lambda l,g:l['qwen']==g and l['qwen+jev']!=g),'anchoring':count(lambda l,g:l['jev']==g and l['qwen']!=g and l['qwen+jev']==l['qwen']),'composite_jev_agree':count(lambda l,g:l['qwen+jev']==l['jev']),'accuracy_delta':out['qwen+jev']['accuracy']-out['jev']['accuracy']}
    out['admit_s1']=out['qwen+jev']['passed'] and out['jev']['passed']
    return out
