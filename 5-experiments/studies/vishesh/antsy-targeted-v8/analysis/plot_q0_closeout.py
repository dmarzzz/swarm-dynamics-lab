"""Saved-journal accounting figure. No native inference or modification of run artifacts."""
import argparse,json
from pathlib import Path
from PIL import Image,ImageDraw

def render(results,out):
    rows=json.loads((results/'assignments.json').read_text())
    expected={(i,w) for i in range(60,80) for w in ('P','C')}
    assert len(rows)==40 and {(r['id'],r['worker']) for r in rows}==expected
    cells={(r['id'],r['worker']):r for r in rows}
    colors={'valid':'#45cba1','error':'#fa6767','unstarted':'#39495b'}
    assert all(r['status'] in colors for r in rows)
    im=Image.new('RGB',(1600,900),'#101b29');d=ImageDraw.Draw(im)
    def text(x,y,s,size=25,color='white'):d.text((x,y),s,fill=color,font_size=size)
    text(55,45,'Antsy Q0: the checker hit the clock',42)
    text(55,110,'Execution failed. Qualification incomplete. Two complete pairs cannot establish benefit.',25)
    text(55,195,'Every assigned receipt and reader',29)
    for j,i in enumerate(range(60,80)):
        x=205+j*65;text(x,250,str(i),21)
        for k,w in enumerate(('P','C')):
            y=292+k*98;r=cells[i,w]
            d.rounded_rectangle((x,y,x+51,y+60),radius=6,fill=colors[r['status']])
            if r['wall_s'] is not None:text(x,y+64,f"{r['wall_s']:.1f}s",15)
    text(55,303,'Primary',24);text(55,401,'Checker',24)
    text(55,505,'5 valid calls   /   1 timeout   /   34 unstarted   /   0 unresolved starts',29)
    text(55,560,'Receipt 62: primary abstained; checker killed after 45.08 seconds. No checker answer retained.',24)
    text(55,610,'Green means valid execution, not necessarily a correct answer. Gray cells were never run.',23)
    text(55,690,'Receipts 60-61: both readers correct. Receipt 62 is partial; 17 pairs never started.',25)
    text(55,737,'No error-correlation estimate, no conditional rescue estimate, no S1, no automatic retry.',24)
    text(55,822,'Retrospective saved-data plot | 20 planned paired receipt units, not 40 independent samples',20,'#aab9cb')
    im.save(out)

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--results',type=Path,required=True);p.add_argument('--out',type=Path,required=True);a=p.parse_args();render(a.results,a.out)
