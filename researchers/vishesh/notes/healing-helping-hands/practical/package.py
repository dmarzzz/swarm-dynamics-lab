"""Noncircular reproducible replay archive with an external checksum receipt."""
import argparse,hashlib,json,zipfile
from pathlib import Path
NAMES=('index.html','data.js','recovery.gif','outcomes.png','initial.png','event.png','final.png','round-00.png','round-10.png','round-20.png','round-29.png','paired-effects.json','effects.json','render-provenance.json','capacity-outcomes.png','capacity-results.json')
def sha(b):return hashlib.sha256(b).hexdigest()
def package(site,mapping):
 files={n:sha((site/n).read_bytes()) for n in NAMES if (site/n).is_file()}
 if not {'index.html','data.js','recovery.gif','outcomes.png'}<=files.keys():raise ValueError('incomplete_replay')
 prior=json.loads((site/'artifact-manifest.json').read_text()) if (site/'artifact-manifest.json').exists() else {}
 inner={**{k:v for k,v in prior.items() if k not in ('files','archive_checksum')},'mapping':mapping,'files':files,'archive_checksum':'See archive-checksums.json outside replay.zip; no circular archive digest.'}
 (site/'artifact-manifest.json').write_text(json.dumps(inner,indent=2)+'\n')
 with zipfile.ZipFile(site/'replay.zip','w',compression=zipfile.ZIP_DEFLATED) as z:
  for n in sorted([*files,'artifact-manifest.json']):
   info=zipfile.ZipInfo(n,date_time=(1980,1,1,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;z.writestr(info,(site/n).read_bytes())
 outer={'replay.zip':sha((site/'replay.zip').read_bytes()),'artifact-manifest.json':sha((site/'artifact-manifest.json').read_bytes())};(site/'archive-checksums.json').write_text(json.dumps(outer,indent=2)+'\n')
 with zipfile.ZipFile(site/'replay.zip') as z:
  assert z.testzip() is None
  assert 'archive-checksums.json' not in z.namelist()
  for n,digest in files.items():assert sha(z.read(n))==digest
 assert 'replay.zip' not in inner['files']
 print(json.dumps({'mapping':mapping,'payloads_verified':len(files),'archive_sha256':outer['replay.zip'],'noncircular':True}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--site',type=Path,required=True);p.add_argument('--mapping',required=True);a=p.parse_args();package(a.site,a.mapping)
