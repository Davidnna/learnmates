"""Focused tests for the bounded OpenAI-compatible retry helper; no live API calls are made."""
import sys
import types
import unittest
from unittest.mock import patch

from app import _chat_completion_with_retries


class FakeAPIStatusError(Exception):
    def __init__(self, status_code):
        super().__init__(f"fake status {status_code}")
        self.status_code = status_code


class FakeAPIConnectionError(Exception):
    pass


class FakeAPITimeoutError(Exception):
    pass


class FakeCompletions:
    def __init__(self, outcomes):
        self.outcomes = list(outcomes)
        self.calls = 0

    def create(self, **kwargs):
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, Exception):
            raise outcome
        return outcome


class FakeClient:
    def __init__(self, outcomes):
        self.completions = FakeCompletions(outcomes)
        self.chat = types.SimpleNamespace(completions=self.completions)


class ChatCompletionRetryTests(unittest.TestCase):
    def setUp(self):
        self.openai_stub = types.ModuleType("openai")
        self.openai_stub.APIStatusError = FakeAPIStatusError
        self.openai_stub.APIConnectionError = FakeAPIConnectionError
        self.openai_stub.APITimeoutError = FakeAPITimeoutError
        self.patch_openai = patch.dict(sys.modules, {"openai": self.openai_stub})
        self.patch_openai.start()
        self.addCleanup(self.patch_openai.stop)

    def test_retries_temporary_503_then_succeeds(self):
        expected = object()
        client = FakeClient([FakeAPIStatusError(503), expected])
        with patch("app.time.sleep") as sleep:
            result = _chat_completion_with_retries(client, "test-model", [], attempts=3)
        self.assertIs(result, expected)
        self.assertEqual(client.completions.calls, 2)
        sleep.assert_called_once()

    def test_does_not_retry_non_transient_404(self):
        client = FakeClient([FakeAPIStatusError(404), object()])
        with patch("app.time.sleep") as sleep:
            with self.assertRaises(FakeAPIStatusError):
                _chat_completion_with_retries(client, "test-model", [], attempts=3)
        self.assertEqual(client.completions.calls, 1)
        sleep.assert_not_called()

    def test_passes_json_response_format_when_requested(self):
        expected = object()
        client = FakeClient([expected])
        result = _chat_completion_with_retries(
            client, "test-model", [], response_format={"type": "json_object"}
        )
        self.assertIs(result, expected)
        self.assertEqual(client.completions.calls, 1)


if __name__ == "__main__":
    unittest.main()
