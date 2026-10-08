"""
Unit Tests for GemmaEngine
Author: Avanish Ayyappan (avanishayyappan2007@gmail.com)
License: Apache-2.0
"""

import unittest
from unittest.mock import MagicMock, patch
import os
import sys

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from gemma_engine import GemmaEngine, DEFAULT_MODEL, DEFAULT_OLLAMA_MODEL

class TestGemmaEngine(unittest.TestCase):
    def test_missing_api_key_raises_error(self):
        """Verify that initializing with no API key in gemini_api mode raises ValueError."""
        with patch.dict(os.environ, {}, clear=True):
            with self.assertRaises(ValueError):
                GemmaEngine(api_key="", backend="gemini_api")

    def test_ollama_mode_init_without_key(self):
        """Verify that Ollama offline mode initializes successfully without cloud API key."""
        engine = GemmaEngine(backend="ollama", ollama_url="http://localhost:11434")
        self.assertEqual(engine.backend, "ollama")
        self.assertEqual(engine.ollama_model, DEFAULT_OLLAMA_MODEL)

    @patch("requests.get")
    def test_ollama_availability_check(self, mock_get):
        """Test health check detection for local Ollama daemon."""
        mock_get.return_value.status_code = 200
        self.assertTrue(GemmaEngine.is_ollama_available("http://localhost:11434"))

        mock_get.side_effect = Exception("Connection refused")
        self.assertFalse(GemmaEngine.is_ollama_available("http://localhost:11434"))

    @patch("google.genai.Client")
    def test_engine_initialization_with_key(self, mock_client):
        """Test proper client instantiation with explicit API key."""
        engine = GemmaEngine(api_key="test_fake_api_key", backend="gemini_api")
        self.assertEqual(engine.model, DEFAULT_MODEL)
        mock_client.assert_called_once_with(api_key="test_fake_api_key")

if __name__ == "__main__":
    unittest.main()
