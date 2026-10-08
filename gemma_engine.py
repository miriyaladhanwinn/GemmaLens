"""
MandiShield - Gemma 4 Agricultural Inference Engine
Dual Mode: Hosted Google Gemini API (gemma-4-26b-a4b-it) + Local Offline Ollama (gemma4:e2b)
Author: Avanish Ayyappan (avanishayyappan2007@gmail.com)
Model: Google Gemma 4 (26B MoE - 4B active parameters / Local Gemma 4 E2B via Ollama)
License: Apache-2.0
"""

import os
import time
import requests
from typing import Optional, Generator, Union, Dict, Any, List
from google import genai
from google.genai import types

from prompts import (
    PESTICIDE_LABEL_AUDIT_PROMPT,
    SEED_MORPHOLOGY_AUDIT_PROMPT,
    REGIONAL_FARMER_ADVISORY_PROMPT,
    DAO_LEGAL_COMPLAINT_PROMPT,
)

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
        ollama_model: str = DEFAULT_OLLAMA_MODEL,
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
        retries: int = 3,
    ) -> str:
        """
        Executes a Gemma 4 inference call with support for Multimodal input
        and Thinking mode. Includes retry logic for unstable hackathon Wi-Fi.
        """
        if self.backend == "ollama":
            return self._analyze_ollama(prompt, image_path, system_instruction)

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
                    model=self.model, contents=contents, config=config
                )
                return response.text
            except Exception as e:
                last_exception = e
                if attempt < retries:
                    time.sleep(1.5 * attempt)
                    continue
                raise RuntimeError(
                    f"Gemma 4 API call failed after {retries} attempts: {last_exception}"
                )

    def _analyze_ollama(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        system_instruction: Optional[str] = None,
    ) -> str:
        """Offline local inference using Ollama."""
        endpoint = f"{self.ollama_url}/api/generate"
        payload: Dict[str, Any] = {
            "model": self.ollama_model,
            "prompt": prompt,
            "stream": False,
        }
        if system_instruction:
            payload["system"] = system_instruction

        try:
            res = requests.post(endpoint, json=payload, timeout=60)
            res.raise_for_status()
            data = res.json()
            return data.get("response", "No response from local Ollama model.")
        except Exception as e:
            raise RuntimeError(
                f"Ollama local inference failed: {e}. Ensure Ollama is running (`ollama serve`)."
            )

    def analyze_stream(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        thinking_level: str = "high",
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
            model=self.model, contents=contents, config=config
        )

        for chunk in response_stream:
            if chunk.text:
                yield chunk.text

    # High-Level MandiShield Specialized Domain Workflows
    def audit_pesticide_label(
        self,
        image_path: Optional[str] = None,
        additional_notes: str = "",
        thinking_level: str = "high",
    ) -> str:
        """Audits pesticide packaging, CIB&RC registration, and toxicity diamond."""
        prompt = f"{PESTICIDE_LABEL_AUDIT_PROMPT}\n\nAdditional Input Context:\n{additional_notes}"
        return self.analyze(prompt=prompt, image_path=image_path, thinking_level=thinking_level)

    def audit_seed_sample(
        self,
        image_path: Optional[str] = None,
        sample_details: str = "",
        thinking_level: str = "high",
    ) -> str:
        """Audits seed physical morphology, coating uniformity, and germination purity."""
        prompt = f"{SEED_MORPHOLOGY_AUDIT_PROMPT}\n\nSample Details:\n{sample_details}"
        return self.analyze(prompt=prompt, image_path=image_path, thinking_level=thinking_level)

    def generate_farmer_advisory(self, audit_report: str) -> str:
        """Synthesizes multilingual farmer advice in English, Tamil, Hindi, and Telugu."""
        prompt = f"{REGIONAL_FARMER_ADVISORY_PROMPT}\n\nAUDIT REPORT FINDINGS:\n{audit_report}"
        return self.analyze(prompt=prompt, thinking_level="minimal")

    def generate_dao_complaint(
        self,
        farmer_name: str,
        farmer_village: str,
        farmer_district: str,
        shop_name: str,
        product_name: str,
        batch_no: str,
        violations: str,
    ) -> str:
        """Generates legal petition under Section 29 of the Insecticides Act 1968."""
        context = f"""
Complainant: {farmer_name}, Village: {farmer_village}, District: {farmer_district}
Vendor Shop: {shop_name}
Product Name: {product_name}, Batch No: {batch_no}
Specific Forensic Violations: {violations}
        """
        prompt = f"{DAO_LEGAL_COMPLAINT_PROMPT}\n\nCASE PARTICULARS:\n{context}"
        return self.analyze(prompt=prompt, thinking_level="minimal")
