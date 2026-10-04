"""Render the existing urgent-delay unit fixture, never a native study sweep."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).parent))
from test_rd5 import trajectory
from common import save
from rd5_render import render


def main():
    out=Path(__file__).parents[1]/'validation'/'scripted-preview'
    out.mkdir(parents=True,exist_ok=True)
    c,s,rows,_=trajectory('urgent','B2')
    for i,r in enumerate(rows):r.update(id='preview-'+str(i),root=c['id'],arm='B2',epoch=i)
    manifest=[{'id':r['id'],'root':c['id'],'arm':'B2','epoch':i,'status':'terminal'} for i,r in enumerate(rows)]
    # A distinct missing slot tests the visual missing-state encoding, not a fifth
    # opportunity in the scientific design.
    manifest.append({'id':'preview-missing','root':'missing-display-control','arm':'B2','epoch':3,'status':'planned'})
    save(out/'packet.json',{'stage':'UNIT-FIXTURE'})
    save(out/'records.json',rows);save(out/'manifest.json',manifest)
    save(out/'summary.json',{'stage':'UNIT-FIXTURE','origin':'SCRIPTED — NOT MODEL EVIDENCE',
                            'assigned':5,'terminal':4,'purpose':'Urgent-delay transition and missing-slot display controls only.'})
    render(out)
    print('Rendered development unit fixture; zero native calls.')


if __name__=='__main__':main()
