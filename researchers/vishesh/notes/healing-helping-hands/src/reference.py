import random
from corpus import make,LABELS

def corpus(seed):
 c=make(seed);r=random.Random(seed+90000);x,y=r.randrange(16),r.randrange(3);c['erased']=[xx+20*yy for yy in range(y,y+8) for xx in range(x,x+5)];c['erasure_geometry']={'kind':'contiguous','x':x,'y':y,'width':5,'height':8};return c

def new_qualification():
 templates={
 'SUPPORT':['The accuracy test favored {m} over the baseline.','The authors observed more accurate answers after switching to {m}.','A completed comparison found improved accuracy for {m}.','{m} delivered an increase in measured accuracy.','The experiment found that {m} made answers more accurate.'],
 'REFUTE':['The accuracy test found {m} inferior to the baseline.','The authors observed less accurate answers after switching to {m}.','A completed comparison found reduced accuracy for {m}.','{m} delivered no increase in measured accuracy.','The experiment found that {m} did not make answers more accurate.'],
 'UNCERTAIN':['No accuracy test of {m} has taken place.','The authors discuss {m} without reporting any accuracy measurements.','The comparison of {m} covers storage costs, not accuracy.','{m} has not been evaluated for accuracy.','The proposed experiment on {m} has not yet produced accuracy data.']}
 out=[]
 for k in LABELS:
  for i in range(20):
   m=f'system K{i+401}';out.append({'claim':m+' improves accuracy.','report':templates[k][i%5].format(m=m),'expected':k})
 random.Random(8601).shuffle(out);return out
