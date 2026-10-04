import io
import json
import sys
import types
import unittest
from unittest.mock import patch, Mock
from reporting import Reporter


class Reporting(unittest.TestCase):
    def test_public_tldr_verified_before_execution(self):
        run = Mock()
        run.progress.return_value = True
        sr = types.SimpleNamespace(start=Mock(return_value=run))
        tldr = 'TLDR: qualification test; no model calls.'
        def public(request, timeout):
            self.assertEqual(request.get_header('User-agent'), 'SwarmLab-PlanPreflight/1.0')
            return io.BytesIO(json.dumps({'params': {'tldr': tldr}}).encode())
        with patch.dict(sys.modules, swarm_report=sr), patch('reporting.urllib.request.urlopen', side_effect=public):
            Reporter('optimal-swarm-size-q1', {'id': 'test'}, tldr)
        run.fail.assert_not_called()

    def test_wrong_public_tldr_fails_closed(self):
        run = Mock()
        run.progress.return_value = True
        sr = types.SimpleNamespace(start=Mock(return_value=run))
        with patch.dict(sys.modules, swarm_report=sr), patch('reporting.urllib.request.urlopen', return_value=io.BytesIO(b'{"params":{}}')):
            with self.assertRaisesRegex(RuntimeError, 'public_run_preflight_failed'):
                Reporter('optimal-swarm-size-q1', {'id': 'test'}, 'TLDR: expected')
        run.fail.assert_called_once()
