import json,html
from pathlib import Path
from PIL import Image,ImageDraw
def render(out):
    out=Path(out);s=json.loads((out/'summary.json').read_text());rows=json.loads((out/'decisions.json').read_text());im=Image.new('RGB',(1100,420),'#f5f7fa');d=ImageDraw.Draw(im)
    d.text((25,20),'PC-5 | native one-step choices | 32 paired layouts | scripted map consequences',fill='#172b3b')
    d.text((25,50),'Optimal action: reliability 0.8 -> explore unknown; reliability 0.2 -> verify report',fill='#172b3b')
    for i,c in enumerate(s['cells']):
        y=95+i*60;d.text((25,y),f"{c['objective']} | reliability {c['reliability']}",fill='#172b3b');d.rectangle((230,y,230+600*c['optimal']/c['assigned'],y+26),fill='#278575' if c['objective']=='explicit' else '#5375b1');d.text((850,y),f"{c['optimal']}/{c['assigned']} optimal | regret {c['expected_regret']:.3f}",fill='#172b3b')
    a=s['overall'];d.text((25,355),f"Primary explicit-minus-legacy regret: {a['mean']:.4f}; practical target -0.10; met: {a['practical_success']}",fill='#172b3b');d.text((25,388),'Diagnostic of decision-contract disclosure. Not evidence of multi-step planning or swarm intelligence.',fill='#172b3b');im.save(out/'final_frame.png')
    body=''.join('<tr>'+''.join('<td>'+html.escape(str(r[k]))+'</td>' for k in ('seed','objective','reliability','choice_role','status','optimal','expected_regret','realized_scripted_loss'))+'</tr>' for r in rows)
    (out/'measured-replay.html').write_text((Path(__file__).parent/'replay-template.html').read_text().replace('__ROWS__',body))
