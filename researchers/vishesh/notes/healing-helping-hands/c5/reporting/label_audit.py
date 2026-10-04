"""Retrospective reference arithmetic on retained reports; no model or fixture generator."""
import re,json,argparse,hashlib
from pathlib import Path

def from_report(row):
    text=row['report'];f=row['family']
    if any(s in text for s in ('was not measured','did not test accuracy','No accuracy estimates','has not been evaluated','no replacement measurement','accuracy was not evaluated','no accuracy experiment has run','was not evaluated')):return 'UNCERTAIN'
    if f=='counts':
        baseline,method=map(int,re.findall(r'answered (\d+) of 100',text));better=method>baseline
    elif f=='error_rates':
        baseline,method=map(int,re.findall(r'made (\d+) errors',text));better=method<baseline
    elif f=='before_after':
        baseline,method=map(int,re.findall(r'(\d+)%',text));better=method>baseline
    elif f in ('percentages','subgroup','superseded','irrelevant_metric','expectations','target_distractor'):
        method,baseline=map(int,re.findall(r'(\d+)%',text)[-2:]);better=method>baseline
    elif f=='negation':
        assert 'measured accuracy on' in text or 'measured accuracy was unchanged' in text
        better='improved over the baseline' in text
    elif f=='repeated_tests':
        assert ('higher' in text)!=('lower' in text);better='higher' in text
    elif f=='uncertainty':
        assert 'completed accuracy comparison' in text;better='better than baseline' in text
    else:raise ValueError('uncovered_family')
    return 'SUPPORT' if better else 'REFUTE'

def run(root,out):
    rows=json.loads((root/'observations.json').read_text());results=[{'id':r['id'],'derived_label':from_report(r),'stored_label':r['expected'],'matches':from_report(r)==r['expected']} for r in rows]
    d={'same_author_reference_audit':True,'scope':'Retrospective finite authored report label/number validation, not independent human labeling or external validity.','observations_sha256':hashlib.sha256((root/'observations.json').read_bytes()).hexdigest(),'checked':len(results),'mismatches':sum(not r['matches'] for r in results),'results':results};out.write_text(json.dumps(d,indent=2)+'\n');print(json.dumps({k:v for k,v in d.items() if k!='results'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('out',type=Path);a=p.parse_args();run(a.root,a.out)
