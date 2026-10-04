import hashlib,json,math,os,sys,tempfile,time,unittest
from pathlib import Path
from capture import run_once
from telemetry import Phases,PHASES,inspect_phases
from worker import execute

ROOT=Path(__file__).resolve().parent

class RepairTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup);self.root=Path(self.tmp.name)
        self.image=self.root/'pixels';self.image.write_bytes(b'NOT_A_REAL_RECEIPT');self.hash=hashlib.sha256(self.image.read_bytes()).hexdigest()
    def call(self,mode,deadline=2,eligible=1):
        return run_once([sys.executable,ROOT/'fault_child.py','--mode',mode,'--out','{out}','--phases','{phases}'],self.root/mode,self.image,self.hash,deadline,eligible)
    def test_normal_and_private_streams(self):
        r=self.call('normal');self.assertEqual(r['status'],'valid');self.assertTrue(r['latency_eligible']);self.assertTrue(r['phases']['complete'])
        self.assertNotIn('PRIVATE_',json.dumps(r));self.assertEqual((self.root/'normal/private/stderr.bin').read_bytes(),b'PRIVATE_STDERR_FIXTURE\n')
        self.assertEqual([json.loads(x)['status'] for x in (self.root/'normal/calls.jsonl').read_text().splitlines()],['started','valid'])
        self.assertEqual((self.root/'normal/private').stat().st_mode & 0o777,0o700)
    def test_timeout_retains_streams_and_partial_phase(self):
        r=self.call('timeout',.3,.2);self.assertEqual(r['category'],'timeout');self.assertEqual(r['phases']['last_phase'],'ocr_begin');self.assertTrue(r['direct_child_reaped'])
        self.assertEqual((self.root/'timeout/private/stderr.bin').read_bytes(),b'PRIVATE_STDERR_FIXTURE\n');self.assertFalse(r['phases']['complete'])
    def test_descendant_stops_writing_after_timeout(self):
        r=self.call('descendant',.4,.3);p=self.root/'descendant/private/child-heartbeat';self.assertTrue(p.exists());before=p.read_bytes();time.sleep(.12)
        self.assertEqual(before,p.read_bytes());self.assertEqual(r['category'],'timeout');self.assertTrue(r['group_cleanup_requested'])
    def test_nonzero_and_signal(self):
        for mode,category in [('error','worker_exit'),('signal','worker_signal')]:
            with self.subTest(mode=mode):
                r=self.call(mode);self.assertEqual(r['category'],category);self.assertEqual(r['status'],'error');self.assertTrue(r['direct_child_reaped'])
    def test_slow_valid_does_not_pass_latency(self):
        r=self.call('slow',1,.05);self.assertEqual(r['status'],'valid');self.assertFalse(r['latency_eligible'])
    def test_invalid_output_and_phase_contract(self):
        for mode,category in [('invalid_output','invalid_output'),('duplicate_phase','invalid_phases'),('partial_phase','invalid_phases'),('symlink_output','invalid_output')]:
            with self.subTest(mode=mode):self.assertEqual(self.call(mode)['category'],category)
    def test_refuses_duplicate_and_input_drift(self):
        self.call('normal')
        with self.assertRaises(FileExistsError):self.call('normal')
        self.image.write_bytes(b'changed')
        with self.assertRaisesRegex(ValueError,'input_mismatch'):self.call('unused')
        self.assertFalse((self.root/'unused').exists())
    def test_spawn_failure_has_terminal(self):
        r=run_once(['/nonexistent-antsy-fixture'],self.root/'spawn',self.image,self.hash,1,1)
        self.assertEqual(r['status'],'error');self.assertTrue(r['direct_child_reaped']);self.assertEqual(len((self.root/'spawn/calls.jsonl').read_text().splitlines()),2)
    def test_parent_interrupt_is_recorded_and_child_reaped(self):
        import subprocess
        from unittest.mock import patch
        original=subprocess.Popen;created=[]
        def interrupting(*args,**kwargs):
            proc=original(*args,**kwargs);created.append(proc);wait=proc.wait;first=[True]
            def once(timeout=None):
                if first[0]:first[0]=False;raise KeyboardInterrupt()
                return wait(timeout=timeout)
            proc.wait=once
            return proc
        with patch('capture.subprocess.Popen',side_effect=interrupting):
            with self.assertRaises(KeyboardInterrupt):self.call('timeout')
        r=json.loads((self.root/'timeout/result.json').read_text())
        self.assertEqual(r['category'],'supervisor_interrupted');self.assertTrue(r['direct_child_reaped'])
        self.assertIsNotNone(created[0].poll());self.assertEqual(len((self.root/'timeout/calls.jsonl').read_text().splitlines()),2)

    def test_time_contract(self):
        for d,e in [(91,45),(-1,1),(float('nan'),1),(1,2),(1,0)]:
            with self.subTest(deadline=d,eligibility=e),self.assertRaises(ValueError):run_once([],self.root/'bad',self.image,self.hash,d,e)
    def test_phase_faults_and_partial_tail(self):
        p=self.root/'phases'
        for events in [[{'seq':0,'phase':'PRIVATE_BAD','elapsed_s':0}],[{'seq':0,'phase':'worker_start','elapsed_s':float('nan')}],[{'seq':0,'phase':'worker_start','elapsed_s':1},{'seq':1,'phase':'imports_begin','elapsed_s':0}]]:
            p.write_text(''.join(json.dumps(x)+'\n' for x in events));r=inspect_phases(p,False);self.assertFalse(r['valid']);self.assertNotIn('PRIVATE_BAD',json.dumps(r))
        p.write_text('{"seq":0,"phase":"worker_start","elapsed_s":0}\n{');r=inspect_phases(p,False);self.assertTrue(r['valid']);self.assertTrue(r['tail_incomplete']);self.assertFalse(r['complete'])
    def test_phase_writer_rejects_unknown_and_collision(self):
        p=self.root/'phase';f=Phases(p)
        try:
            with self.assertRaises(ValueError):f.emit('PRIVATE_BAD')
            f.emit('worker_start')
        finally:f.close()
        with self.assertRaises(FileExistsError):Phases(p)
        self.assertNotIn('PRIVATE_BAD',p.read_text())
    def test_worker_parameters_and_frozen_parser_equivalence(self):
        sys.path.insert(0,str(ROOT.parent/'src'))
        from adapter import easyocr_words
        from fields import extract
        observations=[([[0,0],[40,0],[40,10],[0,10]],'TOTAL',.9),([[50,0],[95,0],[95,10],[50,10]],'10.00',.9)]
        seen={}
        class Reader:
            def readtext(self,image,**kwargs):seen.update(kwargs);return observations
        def loader(models):return Reader,easyocr_words,extract
        p=self.root/'phase';f=Phases(p);out=self.root/'out'
        try:execute(self.image,self.root,out,f,loader)
        finally:f.close()
        self.assertEqual(seen,{'decoder':'greedy','batch_size':1,'workers':0,'detail':1,'paragraph':False})
        self.assertEqual(json.loads(out.read_text()),{'candidate':extract(easyocr_words(observations)),'raw_words':easyocr_words(observations)})
        self.assertTrue(inspect_phases(p,True)['complete'])
        with self.assertRaises(FileExistsError):
            f=Phases(self.root/'phase2')
            try:execute(self.image,self.root,out,f,loader)
            finally:f.close()

if __name__=='__main__':unittest.main()
