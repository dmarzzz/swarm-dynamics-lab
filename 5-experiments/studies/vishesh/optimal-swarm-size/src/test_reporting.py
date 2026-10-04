import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from reporting import Reporter

class Reporting(unittest.TestCase):
    def test_public_tldr_verified_before_execution(self):
        tldr='TLDR: qualification test; no model calls.'
        def public(request,timeout):
            self.assertEqual(request.get_header('User-agent'),'SwarmLab-PlanPreflight/1.0')
            return io.BytesIO(json.dumps({'params':{'tldr':tldr}}).encode())
        with patch('reporting.deliver',return_value={'acknowledged':True}),patch('reporting.urllib.request.urlopen',side_effect=public):
            Reporter('optimal-swarm-size-q1',{'id':'test'},tldr)

    def test_wrong_public_tldr_fails_closed(self):
        with patch('reporting.deliver',return_value={'acknowledged':True}),patch('reporting.urllib.request.urlopen',return_value=io.BytesIO(b'{"params":{}}')):
            with self.assertRaisesRegex(RuntimeError,'public_run_preflight_failed'):
                Reporter('optimal-swarm-size-q1',{'id':'test'},'TLDR: expected')

    def test_unacknowledged_publication_is_retained(self):
        reporter=Reporter.__new__(Reporter);reporter.id='test/run';reporter.experiment='test'
        with tempfile.TemporaryDirectory() as temp:
            target=Path(temp)
            for name in ('assignment.json','trace.jsonl','outcome.json','replay.html'):(target/name).write_text('{}')
            with patch('reporting.deliver',return_value={'acknowledged':False,'spooled':True,'code':'reporting_failed'}):
                receipt=reporter.finish(target,{'failure':None,'evaluation':{'quality':1},'operational_success':True,'elapsed_s':1,'exposure_microdollars':0})
            self.assertFalse(receipt['complete']);self.assertEqual(len(receipt['artifacts']),4)
            self.assertEqual(receipt,json.loads((target/'publication.json').read_text()))

    def test_progress_uses_assignment_width_and_sends_terminal_count(self):
        for width in (2,16):
            tldr='TLDR: width-aware offline progress test.'
            with patch('reporting.deliver',return_value={'acknowledged':True}) as deliver,patch('reporting.urllib.request.urlopen',return_value=io.BytesIO(json.dumps({'params':{'tldr':tldr}}).encode())),patch('reporting.time.monotonic',return_value=10):
                reporter=Reporter('test',{'id':'width-test','width':width},tldr)
                reporter.last_progress=9.9
                reporter.progress(width)
                self.assertEqual(deliver.call_args.args[0],'progress')
                self.assertEqual(deliver.call_args.args[3]['total'],width)
                self.assertEqual(deliver.call_args.args[3]['step'],width)
