"""Same-input, authored-grammar baseline. Abstains outside recognized constructions."""
import re

def predict(claim,report):
 # Class vocabulary and evaluator identifiers are never inspected.
 t=report.lower()
 if any(x in t for x in ('not measured','not test accuracy','has not been evaluated','no replacement measurement','accuracy was not evaluated','no accuracy experiment','was not evaluated','no accuracy estimates','was never tested for accuracy','no accuracy result available','without accuracy measurements','only a planned accuracy experiment')):return 'UNCERTAIN'
 if 'for the requested method:' in t:t=t.split('for the requested method:',1)[1]
 if 'the corrected comparison is:' in t:t=t.split('the corrected comparison is:',1)[1]
 if 'actual results:' in t:t=t.split('actual results:',1)[1]
 m=re.search(r'achieved (\d+)% accuracy and the baseline achieved (\d+)%',t)
 if m:return 'SUPPORT' if int(m[1])>int(m[2]) else 'REFUTE'
 m=re.search(r'baseline answered (\d+) of 100 questions correctly.*answered (\d+) of 100 correctly',t)
 if m:return 'SUPPORT' if int(m[2])>int(m[1]) else 'REFUTE'
 m=re.search(r'baseline made (\d+) errors in 100 answers.*made (\d+) errors in 100 answers',t)
 if m:return 'SUPPORT' if int(m[2])<int(m[1]) else 'REFUTE'
 m=re.search(r'baseline of (\d+)% to (\d+)%',t)
 if m:return 'SUPPORT' if int(m[2])>int(m[1]) else 'REFUTE'
 if any(x in t for x in ('did not improve','accuracy was unchanged','lower accuracy than the baseline','worse than baseline','measured lower accuracy','fewer correct answers than the baseline','matched baseline accuracy exactly')):return 'REFUTE'
 if any(x in t for x in ('accuracy on','higher accuracy than the baseline','better than baseline','measured higher accuracy','improved measured accuracy','more correct answers than the baseline','outperformed baseline accuracy')):
  if 'improved over the baseline' in t or any(x in t for x in ('higher accuracy','better than baseline','improved measured accuracy','more correct answers','outperformed baseline accuracy')):return 'SUPPORT'
 return None
