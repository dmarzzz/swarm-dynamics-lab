"""Per-round progress image adapter; never retries scientific decisions."""
import time
from pathlib import Path
from visualize import plot

class LiveFrames:
    def __init__(self,job,out,arms,interval=5):
        self.job=job;self.out=Path(out);self.arms=arms;self.interval=interval;self.last=0.;self.traces={};self.errors=0
    def __call__(self,event,done,total):
        if 'score' not in event:return
        task,world,stream=event['task_id'],event['world'],event['stream']
        self.traces.setdefault((task,world,stream),[]).append(event['score'])
        if time.monotonic()-self.last<self.interval:return
        self.last=time.monotonic()
        common=self.traces.get((task,world,'common'),[]);rows=[]
        for arm in self.arms:
            branch=self.traces.get((task,world,arm),[])
            history=(common[:3] if arm=='CLEAN' else common[:6])+branch
            if history:rows.append({'task_id':task,'world':world,'arm':arm,'trajectory':history})
        if not rows:return
        try:
            p=self.out/'live_frame.png';plot(rows,p,title='Immune response: measured progress',backend='anthropic')
            self.job.artifact(p,p.name)
            self.job.progress(done,total,message=f'{world}: {stream}, round {event["round"]}',episodes=done)
        except Exception:
            self.errors+=1
            # Rendering/reporting may be retried from the trace; model decisions never are.
