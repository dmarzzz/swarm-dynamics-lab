import json,sys
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
root=Path(sys.argv[1]);out=Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=True);labels=['SUPPORT','REFUTE','UNCERTAIN'];bg='#101716';ink='#edf4e9'
plt.rcParams.update({'figure.facecolor':bg,'axes.facecolor':bg,'text.color':ink,'axes.labelcolor':ink,'xtick.color':ink,'ytick.color':ink})
for attempt in ['pilot-01','pilot-02','diagnostic-03','diagnostic-04','jev-qualification-01']:
 p=root/attempt
 if attempt.startswith('diagnostic'):models=json.loads((p/'summary.json').read_text())
 else:
  models=json.loads((p/'qualification.json').read_text())
  if 'records' in models:models={'jev':models}
 fig,axes=plt.subplots(1,len(models),figsize=(max(14,6*len(models)),5),dpi=130,squeeze=False)
 for ax,(model,r) in zip(axes[0],models.items()):
  matrix=np.zeros((3,3),int);missing=0
  for x in r['records']:
   if x.get('label') not in labels:missing+=1;continue
   matrix[labels.index(x['expected']),labels.index(x['label'])]+=1
  ax.imshow(matrix,cmap='Greens',vmin=0,vmax=max(sum(row) for row in matrix));ax.set_xticks(range(3),labels,fontsize=9);ax.set_yticks(range(3),labels,fontsize=9);ax.set(xlabel='Observed label',ylabel='Expected fixture label');correct=int(np.trace(matrix));ax.set_title(f'{model}: {correct}/{len(r["records"])} correct\n{missing} failed or not-run')
  for i in range(3):
   for j in range(3):ax.text(j,i,str(matrix[i,j]),ha='center',va='center',color='white' if matrix[i,j]>matrix.max()*.5 else '#153024',fontsize=28)
 fig.suptitle('Healing Helping Hands | '+attempt+' | classification evidence',fontsize=19);fig.text(.04,.018,'Raw case counts. Each panel uses its attempt’s frozen fixtures. Different attempts are not paired model comparisons. Earlier failures are retained.',fontsize=10);fig.tight_layout(rect=(0,.07,1,.88));fig.savefig(out/(attempt+'-qualification.png'));plt.close(fig)
print('Rendered five qualification/diagnostic figures from recorded decisions.')
