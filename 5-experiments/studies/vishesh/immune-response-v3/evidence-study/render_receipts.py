"""Measured trace rendering; missing cells remain visibly unobserved."""
import hashlib,json,os,tempfile,sys
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'immune-receipt-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
CASES=['stale_advice','migrated_data','false_alarm','registry_partition']
def plot(rows,path,tick=6,backend='pending'):
 fig,axes=plt.subplots(4,2,figsize=(18,12),facecolor='#102330',sharex=True,sharey=True)
 fig.suptitle('Immune Response | '+backend+' | evidence receipts',color='white',fontsize=24)
 for i,case in enumerate(CASES):
  for j,mem in enumerate(['clean','stale']):
   ax=axes[i,j];ax.set_facecolor('#182f3c');ax.set_title(case.replace('_',' ')+' / '+mem+' memory',color='white',fontsize=13)
   for checked,col,marker in [(False,'#f2ae72','o'),(True,'#66d9bd','s')]:
    rs=[r for r in rows if r['case']==case and r['memory']==mem and r['checked']==checked]
    if not rs:continue
    r=rs[0];h=r['trace'][:tick];values=[int(all(r['initial_checks'].values()))]+[x['healthy'] for x in h]
    ax.plot(range(len(values)),values,marker=marker,fillstyle='none',markersize=9 if checked else 5,label='checked' if checked else 'raw',color=col,lw=2,alpha=.8)
    for x in h:
     if all(x['before_checks'].values()) and not x['healthy']:ax.scatter(x['tick'],.16,marker='x',color='#ff7979',s=65)
     if x['rejected_action']:ax.scatter(x['tick'],.32,marker='^',color='#ffc36d',s=50)
     if x['claim_errors']:ax.scatter(x['tick'],.48,marker='D',color='#c8a3ff',s=35)
   if not ax.lines:ax.text(.5,.5,'Not yet recorded',ha='center',transform=ax.transAxes,color='#b9cad3')
   else:ax.legend(facecolor='#182f3c',labelcolor='white',fontsize=9,loc='center right')
   ax.set_xlim(-.2,6.2);ax.set_ylim(-.12,1.18);ax.set_xticks(range(7));ax.set_yticks([0,1],['unhealthy','healthy']);ax.tick_params(colors='white');ax.grid(alpha=.15)
   if i==3:ax.set_xlabel('Initial snapshot (0), then recorded tool-action ticks',color='white')
 fig.text(.06,.025,'One paired episode per cell; overlapping lines are expected. Red ×: lost healthy service | Orange triangle: rejected action | Purple diamond: false probe claim',color='#b9cad3',fontsize=11)
 fig.tight_layout(rect=[0,.055,1,.95]);fig.savefig(path,dpi=100,facecolor=fig.get_facecolor());plt.close(fig)
def render(out):
 out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];m=json.loads((out/'manifest.json').read_text())
 plot(rows,out/'final_frame.png',backend=m['backend']);frames=[]
 for t in range(7):
  p=out/f'frame-{t}.png';plot(rows,p,t,m['backend']);frames.append(Image.open(p).convert('RGB').quantize(colors=48))
 frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=1000,loop=0)
 html=(Path(__file__).parent/'replay.html').read_text().replace('DATA_HERE',json.dumps({'rows':rows,'manifest':m}).replace('</','<\\/'));(out/'replay.html').write_text(html)
 (out/'visualization-provenance.json').write_text(json.dumps({'renderer_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'template_sha256':hashlib.sha256((Path(__file__).parent/'replay.html').read_bytes()).hexdigest(),'episodes_sha256':hashlib.sha256((out/'episodes.jsonl').read_bytes()).hexdigest(),'frames':7,'backend':m['backend']},indent=2))
if __name__=='__main__':render(sys.argv[1])
