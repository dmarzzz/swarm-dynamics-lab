import sys,json
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
out=Path(sys.argv[1]);a=json.loads((out/'analysis.json').read_text());colors={'q0':'#a04377','q2':'#e4a53d','q4':'#278575','uniform':'#3b6cb0'}
fig,axes=plt.subplots(1,3,figsize=(14,4.8),layout='constrained');fig.suptitle('PC-4: verification has an opportunity cost',fontsize=19,weight='bold')
for p in colors:
 rows=[x for x in a['cells'] if x['policy']==p];axes[0].plot([x['false_count'] for x in rows],[100*x['loss'] for x in rows],marker='o',label=p,color=colors[p])
axes[0].set(xlabel='False reports (out of four)',ylabel='Loss (%) — wrong 1, UNKNOWN 0.25',xticks=[0,2,4]);axes[0].legend(frameon=False);axes[0].set_title('Native consensus, 32 paired worlds')
for i,p in enumerate(colors):
 row=next(x for x in a['cells'] if x['policy']==p and x['false_count']==4);axes[1].bar(i,row['wrong']/32,label='Wrong' if i==0 else None,color='#b74b4b');axes[1].bar(i,row['unknown']/32,bottom=row['wrong']/32,label='UNKNOWN' if i==0 else None,color='#bfc7d4')
axes[1].set(xticks=list(range(4)),xticklabels=list(colors),ylabel='Cells per map (out of 36)');axes[1].legend(frameon=False);axes[1].set_title('Four false reports: errors vs abstention')
xs=[100*r['primary'] for r in a['worlds']];axes[2].scatter(range(1,33),xs,color=colors['q4'],s=22);axes[2].axhline(0,color='#444',lw=1);axes[2].axhline(-200/36,color='#a04377',ls='--',label='Practical target -5.56 pp');m=a['overall']['mean']*100;lo,hi=[v*100 for v in a['overall']['descriptive_t31_interval']];axes[2].axhline(m,color=colors['q4'],label=f'Mean {m:.2f} pp');axes[2].axhspan(lo,hi,color=colors['q4'],alpha=.12,label='Descriptive 95% t interval');axes[2].set(xlabel='Independent root index',ylabel='q4 minus uniform loss (percentage points)');axes[2].set_title('Primary paired differences');axes[2].legend(frameon=False,fontsize=8)
for ax in axes:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.17);ax.set_axisbelow(True)
fig.supxlabel('Scripted inspections + native map interpretation; one model, synthetic stationary terrain. Lower loss is better.',fontsize=10)
fig.savefig(out/'results-frame.png',dpi=160)
