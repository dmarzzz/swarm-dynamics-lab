"""Plot saved evidence; deterministic controllers are counterfactual, not model runs."""
import json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
B=Path(__file__).resolve().parents[1];s=json.loads((B/'results/prior-analysis.json').read_text());fig,ax=plt.subplots(1,3,figsize=(15,5.2),layout='constrained');fig.suptitle('Phantom Coast PI review: improvement is not sufficient for a useful controller',fontsize=17,weight='bold')
for i,p in enumerate((.8,.2)):
 row=s['paired_strata'][i];start=0
 for k,label,color in [('improved','Improved','#168777'),('regressed','Regressed','#c6574b'),('both_correct','Both correct','#7794b5'),('both_wrong','Both wrong','#bcb8b1')]:
  n=row[k];ax[0].barh(i,n,left=start,color=color,label=label if i==0 else None)
  if n:ax[0].text(start+n/2,i,str(n),ha='center',va='center',color='white' if k!='both_wrong' else '#222',weight='bold')
  start+=n
ax[0].set(yticks=[0,1],yticklabels=['80% reliable','20% reliable'],xlim=(0,32),xlabel='Paired layouts (32 per stratum)',title='Explicit vs legacy: who changed?');ax[0].legend(frameon=False,loc='upper center',bbox_to_anchor=(.5,-.15),ncol=2,fontsize=9)
names=['legacy','explicit','always_check','always_explore','analytic'];means=[sum(r['expected_regret'] for r in s['policies'] if r['policy']==n)/2 for n in names];ys=list(range(5));ax[1].barh(ys,means,color=['#557cac','#258879','#9f9f9f','#b9b9b9','#252525']);ax[1].set(yticks=ys,yticklabels=['Native legacy','Native explicit','Always check*','Always explore*','Analytic minimum*'],xlabel='Expected regret / decision',xlim=(0,.34),title='Strong simple controllers matter');ax[1].invert_yaxis()
for y,x in zip(ys,means):ax[1].text(x+.007,y,f'{x:.3f}',va='center',fontsize=10)
counts=s['verify_cost_qwen_attempt002']['counts'];ns=[counts[k] for k in ('both_correct','exact_swap','swap_small_zero','other')];ax[2].bar(range(4),ns,color=['#258879','#c6574b','#b87954','#bcb8b1']);ax[2].set(xticks=range(4),xticklabels=['Correct\ncosts','Exact\nswap','Swap +\nzero','Other'],ylabel='Declared-cost outputs / 24',ylim=(0,13),title='Related Qwen diagnostic: mapping errors')
for x,n in enumerate(ns):ax[2].text(x,n+.3,str(n),ha='center')
for a in ax:a.spines[['top','right']].set_visible(False)
fig.supxlabel('Retrospective analysis: PC5 32 roots / 128 choices; Qwen 12 roots / 24 choices, kept separate.\n*Analytic counterfactuals on the declared one-step contract, not additional model runs. PC6 parked before dispatch.',fontsize=10)
fig.savefig(B/'results/pi-review.png',dpi=150)
