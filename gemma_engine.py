"""
Gemma 4 Inference Engine
Author: Avanish Ayyappan (avanishayyappan2007@gmail.com)
Model: Google Gemma 4 (26B MoE - 4B active parameters)
License: Apache-2.0
"""

import os
import time
from typing import Optional, Generator, Union
from google import genai
from google.genai import types
from PIL import Image
import tempfile

DEFAULT_MODEL = "gemma-4-26b-a4b-it"

class GemmaEngine:
    def __init__(self, api_key: Optional[str] = None, model: str = DEFAULT_MODEL):
        self.api_key = api_key or os.environ.get("GEMINI_API_KEY")
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY is not set. Please provide a valid Google AI Studio API key.")
        
        self.client = genai.Client(api_key=self.api_key)
        self.model = model

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
        contents = []
        uploaded_remote_file = None

        if image_path and os.path.exists(image_path):
            # Upload media file to Google GenAI File API
            uploaded_remote_file = self.client.files.upload(file=image_path)
            contents.append(uploaded_remote_file)

        contents.append(prompt)

        # Configure thinking mode & system instruction
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

    def analyze_stream(
        self,
        prompt: str,
        image_path: Optional[str] = None,
        thinking_level: str = "high"
    ) -> Generator[str, None, None]:
        """
        Stream output tokens in real-time for responsive live demos.
        """
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
