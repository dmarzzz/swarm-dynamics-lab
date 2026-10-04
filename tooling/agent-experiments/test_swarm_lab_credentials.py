import subprocess
import unittest
from unittest.mock import patch
import swarm_lab_credentials as credentials


class CredentialPolicy(unittest.TestCase):
    def test_exact_selector_and_single_key_payload(self):
        fake = subprocess.CompletedProcess([], 0, 'Swarm Lab: sk-ant-test-only-placeholder', '')
        with patch.object(credentials.subprocess, 'run', return_value=fake) as call:
            payload = credentials.credential_payload()
        self.assertEqual(call.call_args.args[0], ['security','find-generic-password','-a','vishesh','-s','swarm-lab-anthropic','-w'])
        self.assertEqual(payload, {'SWARM_MODEL_API_KEY':'sk-ant-test-only-placeholder'})
        credentials.validate_payload(payload)

    def test_missing_entry_does_not_use_environment_fallback(self):
        with patch.dict('os.environ', {'ANTHROPIC_API_KEY':'sk-ant-unrelated-placeholder'}), patch.object(credentials.subprocess, 'run', return_value=subprocess.CompletedProcess([], 44, '', 'sensitive native diagnostic')):
            with self.assertRaisesRegex(credentials.CredentialUnavailable, '^swarm_lab_keychain_unavailable$'):
                credentials.credential_payload()

    def test_ambiguous_or_invalid_record_rejected(self):
        for content in ('', 'sk-ant-one sk-ant-two', 'not-an-anthropic-key'):
            with patch.object(credentials.subprocess, 'run', return_value=subprocess.CompletedProcess([], 0, content, '')):
                with self.assertRaises(credentials.CredentialUnavailable):credentials.credential_payload()

    def test_other_secrets_cannot_be_added_to_payload(self):
        for payload in ({}, {'ANTHROPIC_API_KEY':'sk-ant-general'}, {'SWARM_MODEL_API_KEY':'sk-ant-lab','SWARM_MODEL_WORKSPACE_ID':'another-project'}, {'SWARM_MODEL_API_KEY':'wrong-format'}):
            with self.assertRaises(credentials.CredentialUnavailable):credentials.validate_payload(payload)

if __name__ == '__main__':unittest.main()
