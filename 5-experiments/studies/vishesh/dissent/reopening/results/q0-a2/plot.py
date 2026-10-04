from pathlib import Path
import json,hashlib
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch
base=Path(__file__).resolve().parent
audit=json.loads((base/'trace-audit.json').read_text())['rows']
groups=['clean','conflict','stale'];counts=[sum(r['group']==g for r in audit) for g in groups];correct=[sum(r['group']==g and r['correct'] for r in audit) for g in groups]
assert counts==[12,3,3] and correct==[12,3,0]
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':12,'svg.fonttype':'none'})
fig=plt.figure(figsize=(12,7.4),facecolor='#f5f7fa');ax=fig.add_axes([.27,.43,.59,.29]);ax.set_facecolor('#f5f7fa')
green='#197565';orange='#c55435';dark='#152938';muted='#4b6272'
fig.text(.07,.92,'Expired evidence passed through the decision gate',fontsize=23,weight='bold',color=dark)
fig.text(.07,.866,'RD6 Q0-A2  |  18 valid native responses  |  15 correct  |  Qualification failed',fontsize=13,color=muted)
for i,(n,c) in enumerate(zip(counts,correct)):
 y=2-i;ax.barh(y,1,height=.5,color='#e1e7ed');ax.barh(y,c/n,height=.5,color=green)
 if c==0:ax.plot(0,y,'o',color=orange,markersize=10,clip_on=False)
 ax.text(1.035,y,f'{c}/{n}',va='center',color=dark,fontsize=16,weight='bold')
ax.set_yticks([2,1,0],['Clear current evidence','Conflicting current evidence','Expired evidence']);ax.tick_params(axis='y',length=0,pad=13,labelsize=12)
ax.set_xlim(0,1.08);ax.set_xticks([0,.5,1],['0%','50%','100%']);ax.set_ylim(-.6,2.6);ax.set_xlabel('Correct decisions within each control group',labelpad=9,color=muted)
for spine in ax.spines.values():spine.set_visible(False)
ax.tick_params(axis='x',length=0,labelcolor=muted);ax.grid(axis='x',color='#dce3e9',lw=.8);ax.set_axisbelow(True)
fig.text(.07,.31,'The same observable failure in three domains',fontsize=15,color=dark,weight='bold')
for x,domain,content in [(.07,'PROCESS','Reading 23; allowed 10–30'),(.365,'BRIDGE','Capacity 26; required 20'),(.66,'REQUIRED TEST','Compatibility test passed')]:
 patch=FancyBboxPatch((x,.15),.268,.118,boxstyle='round,pad=0.01',transform=fig.transFigure,facecolor='#fff0e9',edgecolor='none');fig.add_artist(patch)
 fig.text(x+.014,.235,domain,fontsize=10,weight='bold',color=orange)
 fig.text(x+.014,.198,content,fontsize=11,color=dark)
 fig.text(x+.014,.163,'Age 9 > TTL 7: chose PROCEED',fontsize=10.5,color=dark)
fig.text(.07,.089,'Required action for expired evidence: DEFER. All three current-conflict controls correctly deferred.',fontsize=10.5,color=muted)
fig.text(.07,.047,'Authored development controls; no field-rate estimate or causal context ablation. D0 was not run.',fontsize=10.5,color=muted)
fig.savefig(base/'qualification.png',dpi=170,facecolor=fig.get_facecolor())
fig.savefig(base/'qualification.svg',facecolor=fig.get_facecolor())
(base/'figure-data.json').write_text(json.dumps({'source':'trace-audit.json','source_sha256':hashlib.sha256((base/'trace-audit.json').read_bytes()).hexdigest(),'groups':groups,'assigned':counts,'correct':correct,'native_requests':18,'qualification':'failed','D0':'not_run'},indent=2)+'\n')
print(json.dumps({'plot_written':True,'plotted_requests':sum(counts),'correct':sum(correct)}))
