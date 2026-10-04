"""Saved-data-only presentation; never dispatches model calls or alters scores."""
from pathlib import Path
import json,csv,collections,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

def report(root):
 root=Path(root);s=json.loads((root/'summary.json').read_text());rows=list(csv.DictReader((root/'decisions.csv').open()));colors={'D':'#2563eb','E':'#e76f23'}
 fig,axs=plt.subplots(1,3,figsize=(16,5));worlds=list(s['arms']['D']['world_correct_out_of_64'])
 for arm in ('D','E'):
  a=s['arms'][arm];axs[0].plot(range(6),[a['world_correct_out_of_64'][w]/64*100 for w in worlds],'o-',label=arm+' '+('batch of 8' if arm=='D' else 'one case'),color=colors[arm]);axs[1].bar(arm,a['valid_release_correct']/48*100,color=colors[arm]);axs[1].text(arm,a['valid_release_correct']/48*100+1,f"{a['valid_release_correct']}/48",ha='center');axs[2].bar(arm,a['actual_model_usd'],color=colors[arm]);axs[2].text(arm,a['actual_model_usd']+.002,f"${a['actual_model_usd']:.4f}\n{a['calls']} calls",ha='center')
 axs[0].set(xticks=range(6),xticklabels=worlds,ylim=(0,105),ylabel='Strict correct (%)',title='Six world results · 64 assigned decisions/arm/world');axs[0].legend(loc='lower left');axs[1].set(ylim=(0,110),ylabel='Valid-release recall (%)',title='Useful actions · 12 distinct positive cases');axs[2].set(ylim=(0,max(a['actual_model_usd'] for a in s['arms'].values())*1.3+.001),ylabel='Actual model cost (USD)',title='Observed cost · not compute matched')
 for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
 fig.suptitle('Swarm of Theseus D2 — held-out executor qualification',fontsize=20);fig.text(.05,.02,f"{s['terminal_calls']}/432 calls · {s['assigned_decisions']} assigned decisions · six worlds, 96 distinct case/family pairs · repeated calls are dependent. No cultural-preservation claim.",fontsize=11);fig.tight_layout(rect=(0,.06,1,.93));fig.savefig(root/'results.png',dpi=160);plt.close(fig)
 details={}
 for arm in ('D','E'):
  rs=[r for r in rows if r['arm']==arm];groups=collections.defaultdict(list)
  for r in rs:groups[(r['seed'],r['context'],r['id'])].append(r)
  failures=[{'seed':k[0],'context':k[1],'id':k[2],'presentations_wrong':sum(r['correct']!='True' for r in v),'source':v[0]['source'],'positions':{r['order']:r['position'] for r in v}} for k,v in groups.items() if any(r['correct']!='True' for r in v)]
  repeat_disagreement=order_disagreement=early_correct=late_correct=early_n=late_n=0
  for k,vs in groups.items():
   v={(r['order'],r['repeat']):r for r in vs}
   for order in ('base','reverse'):repeat_disagreement+=v[(order,'0')]['action']!=v[(order,'1')]['action']
   for repeat in ('0','1'):order_disagreement+=v[('base',repeat)]['action']!=v[('reverse',repeat)]['action']
  for r in rs:
   if int(r['position'])<=4:early_n+=1;early_correct+=r['correct']=='True'
   else:late_n+=1;late_correct+=r['correct']=='True'
  details[arm]={'distinct_failing_case_families':len(failures),'failures':failures,'repeat_action_disagreements_out_of_192':repeat_disagreement,'order_action_disagreements_out_of_192':order_disagreement,'early_correct':early_correct,'early_n':early_n,'late_correct':late_correct,'late_n':late_n,'atomic_order_is_identical_input':arm=='E'}
 (root/'diagnosis.json').write_text(json.dumps(details,indent=2));print(json.dumps(details))
if __name__=='__main__':report(sys.argv[1])
