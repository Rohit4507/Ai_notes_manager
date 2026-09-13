# services/ai_service.py

import time

from google import genai
from google.genai import types

from config import MODEL_NAME, GENERATION_CONFIG
from prompts.prompts import PROMPT_MAP


class AIError(Exception):
    """Custom error for AI issues."""
    pass


def setup_gemini(api_key: str):
    """Create and return the Gemini client."""

    if not api_key:
        raise AIError("API key is missing.")

    try:
        client = genai.Client(api_key=api_key)
        return client
    except Exception as e:
        raise AIError(f"Failed to initialize Gemini: {e}")


def generate(
    client,
    task: str,
    notes_text: str,
    retries: int = 2
) -> str:
    """
    Generate the requested study output.

    task:
        arrange
        summary
        flashcards
        quiz
        explain
        hindi
    """

    if task not in PROMPT_MAP:
        raise AIError(f"Unknown task: {task}")

    if not notes_text or not notes_text.strip():
        raise AIError("No text provided to process.")

    prompt = PROMPT_MAP[task].format(notes=notes_text)

    last_error = None

    for attempt in range(retries + 1):

        try:
            response = client.models.generate_content(
                model=MODEL_NAME,
                contents=prompt,
                config=types.GenerateContentConfig(
                    max_output_tokens=GENERATION_CONFIG["max_output_tokens"],
                ),
            )

            if not response or not response.text:
                raise AIError("AI returned an empty response. Try again.")

            return response.text

        except Exception as e:

            last_error = e

            if attempt < retries:
                time.sleep(1.5)

    raise AIError(f"AI request failed: {last_error}")