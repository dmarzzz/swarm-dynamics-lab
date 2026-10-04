"""Independent same-author arithmetic and visible-grammar check on saved rows."""
import collections,hashlib,json,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent.parent))
from parser_reference import predict

def check(root):
 rows=json.loads((root/'observations.json').read_text());summary=json.loads((root/'summary.json').read_text());out={};totals=collections.Counter();labels=0
 for family in sorted({r['family'] for r in rows}):
  group=[r for r in rows if r['family']==family];assert all(r['status']=='completed' for r in group);n=len(group);k=sum(r['labels']['a']!=r['labels']['b'] for r in group)
  rank=lambda r:hashlib.sha256(json.dumps({'salt':'C5-matched-v1','id':r['id']},sort_keys=True,separators=(',',':')).encode()).hexdigest()
  referred={r['id'] for r in sorted(group,key=rank)[:k]};correct=collections.Counter()
  for r in group:
   assert predict(r['claim'],r['report'])==r['expected'];labels+=1;a,b,j=[r['labels'][v] for v in ('a','b','jev')]
   pred={'qwen':a,'haiku_b':b,'jev':j,'cascade':a if a==b else j,'matched':j if r['id'] in referred else a}
   for key,val in pred.items():correct[key]+=val==r['expected']
  errors={key:1-value/n for key,value in correct.items()}
  for key in ('qwen','jev','cascade','matched'):assert abs(errors[key]-summary['families'][family]['error'][key])<1e-12
  expected=(1-k/n)*errors['qwen']+k/n*errors['jev'];assert abs(expected-summary['families'][family]['uniform_random_expected_error'])<1e-12
  out[family]={'cases':n,'referrals':k,'correct':dict(correct),'analytic_random_expected_error':expected};totals.update(correct)
 result={'all_family_arithmetic_reconstructed':True,'visible_label_checks':labels,'label_mismatches':0,'correct':dict(totals),'families':out,'independence':'same-author separate implementation; no external adjudication'}
 (root/'reference-check.json').write_text(json.dumps(result,indent=2)+'\n');return result
if __name__=='__main__':print(json.dumps(check(Path(sys.argv[1])),indent=2))
