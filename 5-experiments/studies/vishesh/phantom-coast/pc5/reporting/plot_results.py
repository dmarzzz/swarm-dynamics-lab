import sys,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(sys.argv[1]);s=json.loads((out/'summary.json').read_text());fig,ax=plt.subplots(1,3,figsize=(14,4.7),layout='constrained');fig.suptitle('PC-5: explicit decision rules help, but not in every condition',fontsize=18,weight='bold');colors={'legacy':'#5375b1','explicit':'#278575'}
for objective,offset in [('legacy',-.18),('explicit',.18)]:
 rows=[next(c for c in s['cells'] if c['objective']==objective and c['reliability']==p) for p in (.8,.2)];xs=[i+offset for i in range(2)]
 ax[0].bar(xs,[100*c['optimal']/c['assigned'] for c in rows],.34,label=objective,color=colors[objective]);ax[1].bar(xs,[c['expected_regret'] for c in rows],.34,label=objective,color=colors[objective])
 for x,c in zip(xs,rows):ax[0].text(x,100*c['optimal']/32+2,f"{c['optimal']}/32",ha='center',fontsize=9)
for x in ax[:2]:x.set_xticks([0,1],['80% reliable\nExplore unknown is optimal','20% reliable\nVerify report is optimal']);x.legend(frameon=False)
ax[0].set(ylabel='Optimal native choices (%)',ylim=(0,105));ax[0].set_title('The reliable-source condition regresses')
ax[1].set(ylabel='Mean expected regret per decision');ax[1].set_title('Errors differ in expected cost')
a=s['overall'];xs=[r['primary'] for r in s['worlds']];ax[2].scatter(range(1,33),xs,s=22,color=colors['explicit']);ax[2].axhline(0,color='#444',lw=1);ax[2].axhline(-.1,color='#a04377',ls='--',label='Practical target -0.10');ax[2].axhline(a['mean'],color=colors['explicit'],label=f"Mean {a['mean']:.3f}");ax[2].axhspan(*a['descriptive_t31_interval'],color=colors['explicit'],alpha=.13,label='Descriptive 95% t interval');ax[2].set(xlabel='Independent layout index',ylabel='Explicit minus legacy expected regret');ax[2].set_title('Paired primary contrast');ax[2].legend(frameon=False,fontsize=8)
for x in ax:x.spines[['right','top']].set_visible(False);x.grid(axis='y',alpha=.17);x.set_axisbelow(True)
fig.supxlabel('32 paired layouts; two risk templates; native choices and scripted consequences. One-step diagnostic, not general planning.',fontsize=10);fig.savefig(out/'results-frame.png',dpi=160)
