"""Evaluator-only timeline. Images are outputs, never actor observations."""
from PIL import Image, ImageDraw, ImageFont
from engine import evaluate

def font(size):
    for p in ('/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf', '/System/Library/Fonts/Supplemental/Arial.ttf'):
        try: return ImageFont.truetype(p, size)
        except OSError: pass
    return ImageFont.load_default()

def frame(rows, spec, title, step=None):
    im=Image.new('RGB', (1600, 900), '#101823'); d=ImageDraw.Draw(im)
    d.text((45, 30), 'PERMITTED ACTIONS / GLOBAL OUTCOMES', font=font(29), fill='#edf4ff')
    d.text((45, 85), title[:110], font=font(20), fill='#c5d1df')
    d.text((45, 125), 'Evaluator view: blue = action, red = violation, amber = blocked; absent cells = no event', font=font(19), fill='#b5c4d6')
    d.text((45, 159), 'Recorded action order; one column per turn. Actor packets do not contain this verdict.', font=font(18), fill='#b5c4d6')
    columns=max(24,max((len(r['events']) for r in rows),default=0))
    x0=190; width=1008//columns; y0=238
    for i in range(columns): d.text((x0+i*width+4, 210), str(i), font=font(12), fill='#bdccdf')
    for j,r in enumerate(rows[:7]):
        y=y0+j*73; ev=[e for e in r['events'] if step is None or e['event']<=step]
        result=evaluate(spec,ev)
        d.text((50,y+12), r['arm'], font=font(27), fill='#f4f6fa')
        for i in range(columns):
            color='#273341'
            if i < len(ev):
                e=ev[i]; color='#397dbe'
                if e['operation'] in ('wait','inspect','message'): color='#546778'
                if e['status']=='blocked': color='#d6a641'
                elif e['event'] in result['violation_events']: color='#d95364'
            d.rounded_rectangle((x0+i*width,y,x0+i*width+width-4,y+43),radius=4,fill=color)
            if i<len(ev): d.text((x0+i*width+3,y+12),ev[i]['operation'][:2],font=font(11),fill='white')
        terminal = step is None or step>=len(r['events'])
        status = 'invalid' if terminal and not r['validity']['ok'] else 'safe complete' if result['completion'] else 'violation' if result['violation'] else 'incomplete'
        d.text((1230,y+8),status,font=font(20),fill='#f4f6fa')
        d.text((1230,y+35),f"effects {result['completed_effects']} | blocked {result['blocked']}",font=font(15),fill='#b5c4d6')
    d.text((45,820),'D1: restricted ancestry   D2: reused approval   D3: aggregate overspend',font=font(20),fill='#bdccdf')
    d.text((45,854),'Synthetic development tasks. Reference runs and model runs are labeled separately.',font=font(17),fill='#bdccdf')
    return im

def artifacts(rows,spec,title,directory):
    frame(rows,spec,title).save(directory/'final_frame.png')
    frames=[frame(rows,spec,title,step=-1)]
    for i in range(max((len(r['events']) for r in rows),default=0)):
        frames.append(frame(rows,spec,title,step=i))
    frames.append(frame(rows,spec,title))
    frames[0].save(directory/'replay.gif',save_all=True,append_images=frames[1:],duration=450,loop=0)
