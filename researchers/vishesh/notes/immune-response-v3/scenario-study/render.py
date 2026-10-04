import os,tempfile,json,sys
from pathlib import Path
os.environ.setdefault('MPLCONFIGDIR',str(Path(tempfile.gettempdir())/'immune-scenario-mpl'))
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from PIL import Image
ARMS=['retain','reset','revision_check'];COLORS=['#f2ae72','#8dacf6','#66d9bd']
def plot(rows,path,tick=6):
 fig,axes=plt.subplots(2,2,figsize=(16,9),facecolor='#102330');fig.suptitle('Immune Response · measured recovery decisions',color='white',fontsize=22)
 for ax,case in zip(axes.flat,['stale_advice','migrated_data','false_alarm','registry_partition']):
  ax.set_facecolor('#182f3c');ax.set_title(case.replace('_',' '),color='white',fontsize=16)
  for a,col in zip(ARMS,COLORS):
   rs=[r for r in rows if r['case']==case and r['arm']==a];
   if not rs:continue
   vals=[sum(r['trace'][i]['healthy'] for r in rs)/len(rs) for i in range(tick)]
   ax.plot(range(1,tick+1),vals,'o-',label=a,color=col,linewidth=2,alpha=.8)
  ax.set_xlim(.7,6.3);ax.set_ylim(-.1,1.15);ax.set_xticks(range(1,7));ax.set_yticks([0,1],['unhealthy','healthy']);ax.tick_params(colors='white');ax.grid(alpha=.15);ax.set_xlabel('Recorded tool-action tick',color='white')
  if ax.lines:ax.legend(facecolor='#182f3c',labelcolor='white',fontsize=9)
 fig.text(.05,.015,'All four compatibility / data / feature checks must pass. Lines may overlap. Scripted solver success is feasibility evidence only.',color='#b9cad3',fontsize=11)
 fig.tight_layout(rect=[0,.04,1,.94]);fig.savefig(path,dpi=100,facecolor=fig.get_facecolor());plt.close(fig)
def render(out):
 out=Path(out);rows=[json.loads(x) for x in (out/'episodes.jsonl').read_text().splitlines()];plot(rows,out/'final_frame.png');frames=[]
 for t in range(1,7):
  p=out/f'frame-{t}.png';plot(rows,p,t);frames.append(Image.open(p).convert('RGB').quantize(colors=32))
 frames[0].save(out/'replay.gif',save_all=True,append_images=frames[1:],duration=850,loop=0,optimize=True)
 html=(Path(__file__).parent/'replay.html').read_text().replace('DATA_HERE',json.dumps({'rows':rows,'manifest':json.loads((out/'manifest.json').read_text())}).replace('</','<\\/'))
 (out/'replay.html').write_text(html)
if __name__=='__main__':render(sys.argv[1])
