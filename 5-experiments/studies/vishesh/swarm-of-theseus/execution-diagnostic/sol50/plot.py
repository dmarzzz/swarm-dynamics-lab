from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(__file__).resolve().parent
fig,axes=plt.subplots(1,2,figsize=(11,4.4));fig.patch.set_facecolor('#fafafa')
labels=['Correct founder notes','Correct intended peer pairs','Pairs accepted by router'];values=[5,5,1]
axes[0].barh(labels,values,color=['#24776c','#24776c','#c05442']);axes[0].invert_yaxis();axes[0].set_xlim(0,5.6);axes[0].set_xlabel('Members (5 assigned)')
for j,x in enumerate(values):axes[0].text(x+.07,j,f'{x}/5',va='center')
labels2=['Founder actions','Joint task actions','Joint actions given\ndelivered evidence'];vals=[30,18,30]
axes[1].barh(labels2,vals,color=['#24776c','#c05442','#738194']);axes[1].invert_yaxis();axes[1].set_xlim(0,34);axes[1].set_xlabel('Correct decisions (30 observed per row)')
for j,x in enumerate(vals):axes[1].text(x+.4,j,f'{x}/30',va='center')
for ax in axes:
 for side in ['top','right']:ax.spines[side].set_visible(False)
 ax.grid(axis='x',alpha=.15);ax.set_axisbelow(True)
fig.suptitle('SOL50 qualification: correct destinations, broken address routing',fontsize=14)
fig.text(.5,.02,'Native qualification only • one 5-member world • 17 calls • no handover or 50-member pilot\nCorrect deferral after lost messages is not successful task service.',ha='center',fontsize=9)
fig.tight_layout(rect=(0,.10,1,.92));fig.savefig(p/'qualification.png',dpi=160);plt.close(fig)
print('Aggregate qualification figure saved.')
