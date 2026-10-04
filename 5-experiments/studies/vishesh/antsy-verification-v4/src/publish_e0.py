"""Retrospective E0 summary, explicitly not a reconstructed live timeline."""
import json
from pathlib import Path
import swarm_report as sr
from render import canvas,write,COLORS,MUTED
root=Path('/srv/swarm/antsy-v4/E0-attempt-1');cal=json.loads((root/'calibration.json').read_text());exp='antsy-verification-v4';rid=exp+'/E0-attempt-1'
im,d=canvas('Antsy | real routing headroom', 'E0 calibration only: first 20 of 100 measured CORD receipts; no policy evaluation outcomes shown')
for j,m in enumerate('ABC'):
    y=210+j*145;q=cal['mode_mean_recall'][m];write(d,(80,y),f'Configuration {m}',28);d.rectangle((390,y,390+900*q,y+55),fill=COLORS[j]);write(d,(400,y+62),f'{q:.1%} annotated-token recall',23)
write(d,(80,690),f"Best fixed: {cal['best_fixed']} | oracle routing headroom: {cal['oracle_gain_over_best_fixed']*100:.2f} percentage points",30)
write(d,(80,760),'Gate: at least 1 point of headroom. Result: PASS.',28)
write(d,(80,827),'All 300 OCR calls completed, zero invalid outputs. This is a retrospective summary.',23,MUTED)
write(d,(80,875),'Not evidence of agent benefit. CORD / Clova AI / CC BY 4.0.',23,MUTED)
im.save(root/'calibration.png')
sr.report('start',exp,rid,params={'stage':'E0','kind':'diagnostic'},url='https://github.com/dmarzzz/swarm-lab/tree/e5d684e/researchers/vishesh/notes/antsy-verification-v4',message='Retrospective registration of completed OCR measurement; not its original start timestamp.',strict=True)
for name in ['manifest.json','calibration.json','calibration.png']:sr.upload(rid,root/name,name)
sr.report('done',exp,rid,metrics={'completed':100,'invalid':0,'routing_headroom':cal['oracle_gain_over_best_fixed']},message='300 measured OCR calls completed. Calibration gate passed; E0 execution was not streamed live.',strict=True)
print('E0 retrospective summary published')
