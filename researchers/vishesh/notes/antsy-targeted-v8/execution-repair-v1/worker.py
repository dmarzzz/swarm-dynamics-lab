"""Proposed D1 checker; instrumented cold phases, unchanged OCR/parser parameters.

No launcher/admission is supplied here. Native use requires the separately approved
D1 contract. Offline tests inject a fake engine; they never import model packages.
"""
import argparse,json,os,random,sys
from pathlib import Path
from telemetry import Phases

ROOT=Path(__file__).resolve().parents[1]


def load_components(models):
    import numpy as np
    import torch,cv2,easyocr
    sys.path.insert(0,str(ROOT/'src'))
    from fields import extract
    from adapter import easyocr_words
    random.seed(0);np.random.seed(0);torch.manual_seed(0)
    torch.set_num_threads(1);torch.set_num_interop_threads(1);cv2.setNumThreads(1)
    def factory():
        reader=easyocr.Reader(['en','id'],gpu=False,model_storage_directory=str(models),
            user_network_directory=str(models/'user'),detect_network='craft',recog_network='latin_g2',
            download_enabled=False,verbose=False,quantize=False,detector=False)
        reader.quantize=False;reader.setDetector('craft')
        return reader
    return factory,easyocr_words,extract


def execute(image,models,out,phases,loader=load_components):
    phases.emit('worker_start');phases.emit('imports_begin')
    factory,normalize,extract=loader(models)
    phases.emit('imports_end');phases.emit('reader_init_begin')
    reader=factory()
    phases.emit('reader_init_end');phases.emit('ocr_begin')
    observations=reader.readtext(str(image),decoder='greedy',batch_size=1,workers=0,detail=1,paragraph=False)
    phases.emit('ocr_end');phases.emit('extract_begin')
    words=normalize(observations);result={'candidate':extract(words),'raw_words':words}
    phases.emit('extract_end');phases.emit('output_begin')
    # Exclusive creation preserves any existing or partial result.
    fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w') as f:json.dump(result,f);f.flush();os.fsync(f.fileno())
    phases.emit('output_end')


def main():
    p=argparse.ArgumentParser();p.add_argument('--image',type=Path,required=True);p.add_argument('--models',type=Path,required=True)
    p.add_argument('--out',type=Path,required=True);p.add_argument('--phases',type=Path,required=True);a=p.parse_args()
    os.umask(0o077);phases=Phases(a.phases)
    try:execute(a.image,a.models,a.out,phases)
    finally:phases.close()

if __name__=='__main__':main()
