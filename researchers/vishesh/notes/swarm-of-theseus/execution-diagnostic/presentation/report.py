"""Render frozen D1 measured evidence; no model calls or inferential claims."""
import json,sys,collections
from pathlib import Path
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
root=Path(sys.argv[1]);s=json.loads((root/'summary.json').read_text());m=json.loads((root/'manifest.json').read_text())
assert s['status']=='measured'
labels=['A: legacy','B: executor','C: keyed evidence','D: no notebook','E: atomic calls']
keys=[(seed,ctx) for seed in (610,611,612) for ctx in ('release','incident','migration-old','migration-new')]
z=[[s['cells'][f'{seed}/{ctx}/{arm}']['correct']/8 for arm in 'ABCDE'] for seed,ctx in keys]
fig,ax=plt.subplots(figsize=(12,9));fig.patch.set_facecolor('#f7f9fb');ax.set_facecolor('#f7f9fb')
im=ax.imshow(z,cmap='YlGnBu',vmin=0,vmax=1,aspect='auto');ax.set_xticks(range(5),labels);ax.xaxis.tick_top();ax.set_yticks(range(12),[f'{seed} / {ctx}' for seed,ctx in keys])
for i,row in enumerate(z):
 for j,v in enumerate(row):ax.text(j,i,f'{round(v*8)}/8',ha='center',va='center',color='white' if v>.65 else '#152632',fontsize=12,fontweight='bold')
for y in (3.5,7.5):ax.axhline(y,color='white',linewidth=3)
fig.suptitle('Theseus D1: explicit-rule execution after interface repairs',fontsize=17,y=.99)
fig.text(.02,.03,f"Measured: {s['completed_call_records']}/144 calls · 480 assigned decisions · 3 worlds · model cost ${s['estimated_actual_usd']:.4f}\nEach cell retains all 8 assigned decisions, including invalid/missing outputs. Descriptive results; no cultural-preservation claim.",fontsize=10)
fig.colorbar(im,ax=ax,fraction=.035,pad=.02,label='Assigned accuracy');fig.tight_layout(rect=(0,.095,1,.955));fig.savefig(root/'results.png',dpi=180);plt.close(fig)
