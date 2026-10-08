"""
Gemma 4 Inference Engine (Dual Mode: Hosted Google Gemini API + Local Offline Ollama)
Author: Avanish Ayyappan (avanishayyappan2007@gmail.com)
Model: Google Gemma 4 (26B MoE - 4B active parameters / Local Gemma 4 E2B via Ollama)
License: Apache-2.0
"""

import os
import time
import requests
from typing import Optional, Generator, Union, Dict, Any
from google import genai
from google.genai import types

DEFAULT_MODEL = "gemma-4-26b-a4b-it"
DEFAULT_OLLAMA_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")
DEFAULT_OLLAMA_MODEL = os.environ.get("OLLAMA_MODEL", "gemma4:e2b")

class GemmaEngine:
    def __init__(
        self,
        api_key: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        backend: str = "gemini_api",
        ollama_url: str = DEFAULT_OLLAMA_URL,
        ollama_model: str = DEFAULT_OLLAMA_MODEL
    ):
        self.backend = backend
        self.model = model
        self.ollama_url = ollama_url
        self.ollama_model = ollama_model
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")

        if self.backend == "gemini_api":
            if not self.api_key:
                raise ValueError("GEMINI_API_KEY is not set. Please provide a Google AI Studio API key.")
            self.client = genai.Client(api_key=self.api_key)
        else:
            self.client = None

    @staticmethod
    def is_ollama_available(url: str = DEFAULT_OLLAMA_URL) -> bool:
        """Checks if local Ollama server is running."""
        try:
            r = requests.get(f"{url}/api/tags", timeout=1.5)
            return r.status_code == 200
        except Exception:
            return False

    def analyze(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        thinking_level: str = "high",
        system_instruction: Optional[str] = None,
        retries: int = 3
    ) -> str:
        """
        Executes a Gemma 4 inference call with support for Multimodal input
        and Thinking mode. Includes retry logic for unstable hackathon Wi-Fi.
        """
        if self.backend == "ollama":
            return self._analyze_ollama(prompt, image_path, system_instruction)

        # Gemini API Backend (Gemma 4 26B MoE)
        contents = []
        if image_path and os.path.exists(image_path):
            uploaded_remote_file = self.client.files.upload(file=image_path)
            contents.append(uploaded_remote_file)

        contents.append(prompt)

        config_args = {}
        if thinking_level in ["high", "minimal"]:
            config_args["thinking_config"] = types.ThinkingConfig(thinking_level=thinking_level)
        
        if system_instruction:
            config_args["system_instruction"] = system_instruction

        config = types.GenerateContentConfig(**config_args)

        last_exception = None
        for attempt in range(1, retries + 1):
            try:
                response = self.client.models.generate_content(
                    model=self.model,
                    contents=contents,
                    config=config
                )
                return response.text
            except Exception as e:
                last_exception = e
                if attempt < retries:
                    time.sleep(1.5 * attempt)
                    continue
                raise RuntimeError(f"Gemma 4 API call failed after {retries} attempts: {last_exception}")

    def _analyze_ollama(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        system_instruction: Optional[str] = None
    ) -> str:
        """Offline local inference using Ollama."""
        endpoint = f"{self.ollama_url}/api/generate"
        payload: Dict[str, Any] = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False
        }
        if system_instruction:
            payload["system"] = system_instruction

        try:
            res = requests.post(endpoint, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            return data.get("response", "No response from local Ollama model.")
        except Exception as e:
            raise RuntimeError(f"Ollama local inference failed: {e}. Ensure Ollama is running (`ollama serve`).")

    def analyze_stream(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        thinking_level: str = "high"
    ) -> Generator[str, None, None]:
        """Stream output tokens in real-time for responsive live demos."""
        if self.backend == "ollama":
            yield self._analyze_ollama(prompt, image_path)
            return

        contents = []
        if image_path and os.path.exists(image_path):
            uploaded_remote_file = self.client.files.upload(file=image_path)
            contents.append(uploaded_remote_file)

        contents.append(prompt)

        config = types.GenerateContentConfig(
            thinking_config=types.ThinkingConfig(thinking_level=thinking_level)
        )

        response_stream = self.client.models.generate_content_stream(
            model=self.model,
            contents=contents,
            config=config
        )

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text
