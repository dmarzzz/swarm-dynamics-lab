"""Pixel-only cold OCR. No evaluator file, case ID or operator context accepted."""
import argparse
import json
import os
from pathlib import Path
import sys
from common import STUDY,original,load,sha,digest
sys.path.insert(0,str(STUDY/'execution-repair-v1'))
from telemetry import Phases

RAPID_PARAMS={'Global.log_level':'error','EngineConfig.onnxruntime.intra_op_num_threads':1,
              'EngineConfig.onnxruntime.inter_op_num_threads':1}

def settings(engine):
    return {'engine':engine,'threads':1,'cold_process':True,'external_image_resize':False,
            'rapid_params':RAPID_PARAMS if engine=='P' else None,
            'easyocr':{'languages':['en','id'],'gpu':False,'detect_network':'craft','recog_network':'latin_g2',
                       'quantize':False,'decoder':'greedy','batch_size':1,'workers':0,'paragraph':False,'download_enabled':False} if engine=='C' else None,
            'parser':'anchor-row-v2','effective_context_schema':1}


def components(engine,models):
    if engine=='C':
        worker=load('comparison_checker',STUDY/'execution-repair-v1/worker.py')
        factory,normalize,_=worker.load_components(models)
        return factory,lambda obj,image:obj.readtext(str(image),decoder='greedy',batch_size=1,workers=0,detail=1,paragraph=False),normalize
    import cv2
    from rapidocr import RapidOCR
    cv2.setNumThreads(1)
    def normalize(result):
        if result.txts is None:return []
        rows=[]
        for box,text,confidence in zip(result.boxes,result.txts,result.scores):
            xs=[float(p[0]) for p in box];ys=[float(p[1]) for p in box]
            x,y=min(xs),min(ys);w,h=max(xs)-x,max(ys)-y
            rows.append({'text':text,'confidence':float(confidence),'x':x,'y':y+h/2,'h':h,
                         'box':[round(x),round(y),round(w),round(h)]})
        return rows
    return lambda:RapidOCR(params=RAPID_PARAMS),lambda obj,image:obj(str(image)),normalize


def execute(image,engine,models,out,phases,loader=components):
    phases.emit('worker_start');phases.emit('imports_begin')
    factory,read,normalize=loader(engine,models)
    phases.emit('imports_end');phases.emit('reader_init_begin');reader=factory()
    phases.emit('reader_init_end');phases.emit('ocr_begin');raw=read(reader,image)
    phases.emit('ocr_end');phases.emit('extract_begin');words=normalize(raw)
    value={'candidate':original.extract(words),'raw_words':words}
    phases.emit('extract_end');phases.emit('output_begin')
    fd=os.open(out,os.O_WRONLY|os.O_CREAT|os.O_EXCL|getattr(os,'O_NOFOLLOW',0),0o600)
    with os.fdopen(fd,'w') as f:json.dump(value,f);f.flush();os.fsync(f.fileno())
    phases.emit('output_end')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--image',type=Path,required=True);p.add_argument('--engine',choices=['P','C'],required=True)
    p.add_argument('--models',type=Path,required=True);p.add_argument('--out',type=Path,required=True);p.add_argument('--phases',type=Path,required=True)
    a=p.parse_args();os.umask(0o077)
    from common import write
    write(a.out.parent/'effective-context.json',{'settings':settings(a.engine),'input_sha256':sha(a.image),
                                               'worker_source_sha256':sha(Path(__file__))})
    phases=Phases(a.phases)
    try:execute(a.image,a.engine,a.models,a.out,phases)
    finally:phases.close()
