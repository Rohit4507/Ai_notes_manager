# config.py
"""Central config so you can change settings in one place."""

import os
from dotenv import load_dotenv

load_dotenv()

# API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
MODEL_NAME = "gemini-3.6-flash"

# Limits (protect API cost + performance)
MAX_PDF_PAGES = 40
MAX_CHARS = 40000          # ~ safe input size for the model
MAX_FILE_SIZE_MB = 15

# AI generation settings
GENERATION_CONFIG = {
    "max_output_tokens": 4000,
}

# App info
APP_TITLE = "Smart Notes Organizer"
APP_ICON = "📚"