"""Saved-data-only R1 plots and repeat diagnostics."""
from pathlib import Path
import json,csv,collections,sys
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
p=Path(sys.argv[1]);s=json.loads((p/'summary.json').read_text());rows=list(csv.DictReader((p/'decisions.csv').open()));colors={'E':'#e76f23','F':'#087f68'};fig,axs=plt.subplots(1,3,figsize=(16,5));worlds=list(s['arms']['E']['world_correct_out_of_32']);details={}
for arm in ('E','F'):
 a=s['arms'][arm];axs[0].plot(range(6),[a['world_correct_out_of_32'][w]/32*100 for w in worlds],'o-',label=arm+(' unchanged' if arm=='E' else ' repaired'),color=colors[arm]);axs[1].bar(arm,a['incident_false_activation'],color=colors[arm]);axs[1].text(arm,a['incident_false_activation']+.1,str(a['incident_false_activation']),ha='center');axs[2].bar(arm,a['actual_model_usd'],color=colors[arm]);axs[2].text(arm,a['actual_model_usd']+.002,f"${a['actual_model_usd']:.4f}\n{a['calls']} calls",ha='center')
 groups=collections.defaultdict(list)
 for r in rows:
  if r['arm']==arm:groups[(r['seed'],r['context'],r['id'])].append(r)
 failures=[{'seed':k[0],'context':k[1],'id':k[2],'wrong_presentations':sum(r['correct']!='True' for r in rs),'source':rs[0]['source'],'actions':[r['action'] for r in rs],'truth':rs[0]['truth']} for k,rs in groups.items() if any(r['correct']!='True' for r in rs)]
 details[arm]={'distinct_failing_case_families':len(failures),'failures':failures,'repeat_disagreements_out_of_96':sum(rs[0]['action']!=rs[1]['action'] for rs in groups.values())}
axs[0].set(xticks=range(6),xticklabels=worlds,ylim=(0,105),ylabel='Strict correct (%)',title='Six fresh worlds · 32 decisions/arm/world');axs[0].legend(loc='lower left');axs[1].set(ylim=(0,max(a['incident_false_activation'] for a in s['arms'].values())+2),ylabel='False incident activations',title='Qualification requires zero');axs[2].set(ylim=(0,max(a['actual_model_usd'] for a in s['arms'].values())*1.3+.001),ylabel='Actual model cost (USD)',title='Same call counts · observed token cost')
for ax in axs:ax.spines[['top','right']].set_visible(False);ax.grid(axis='y',alpha=.2)
fig.suptitle('Swarm of Theseus R1 — one targeted atomic repair',fontsize=20);fig.text(.05,.02,f"{s['terminal_calls']}/384 calls · 96 distinct case/family pairs · bundled schema + instruction repair · qualification is not cultural preservation.",fontsize=11);fig.tight_layout(rect=(0,.06,1,.93));fig.savefig(p/'results.png',dpi=160);plt.close(fig);(p/'diagnosis.json').write_text(json.dumps(details,indent=2));print(json.dumps(details))
