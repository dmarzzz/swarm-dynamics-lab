"""Embed measured replay data as gzip; no external data requests or inference."""
from pathlib import Path
import base64,gzip,json,argparse

def package(folder):
    text=(folder/'data.js').read_text()
    assert text.startswith('const DATA=') and text.rstrip().endswith(';')
    raw=text[len('const DATA='):].rstrip().removesuffix(';')
    json.loads(raw)
    payload=base64.b64encode(gzip.compress(raw.encode(),mtime=0)).decode()
    html=(folder/'index.html').read_text()
    boot='<script type="module">const packed=Uint8Array.from(atob("'+payload+'"),c=>c.charCodeAt(0));const DATA=JSON.parse(await new Response(new Blob([packed]).stream().pipeThrough(new DecompressionStream("gzip"))).text());\n'
    html=html.replace('<script src="data.js"></script><script>',boot)
    for name in ('outcomes.png','recovery.gif'):
        html=html.replace('href="'+name+'"','href="https://swarm-live.pages.dev/api/a/healing-helping-hands/C3-S1/'+name+'"')
    (folder/'replay.html').write_text(html)
    print(json.dumps({'bytes':len(html.encode()),'compression':'gzip embedded; measured data unchanged'}))
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('folder',type=Path);package(p.parse_args().folder)
