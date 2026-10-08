from google import genai
from google.genai import types

client = genai.Client()

response = client.models.generate_content(
    model="gemma-4-26b-a4b-it",
    contents="Analyze the edge cases and memory safety risks in this C pointer arithmetic snippet...",
    config=types.GenerateContentConfig(
        thinking_config=types.ThinkingConfig(thinking_level="high")  # Activates Gemma 4 deep reasoning
    ),
)

print(response.text)