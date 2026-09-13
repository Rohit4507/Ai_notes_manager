# Smart Notes Organizer 📚

Upload old/messy notes (PDF) → Get clean, well-arranged, exam-ready notes using AI.

## Setup

1. Get free API key: https://aistudio.google.com/
2. Create `.env` file:
GEMINI_API_KEY=your_key_here

text

3. Install:
pip install -r requirements.txt

text

4. Run:
streamlit run app.py

text


## Features
- Fully Arranged Notes
- Summary
- Flashcards
- MCQ Quiz
- Simple Explanation
- Hindi Notes
- Download as .md / .txt

## Notes
- Works best with typed PDFs (not scanned/handwritten).
- Max 40 pages, 15 MB per file (change in `config.py`).

## Structure
- `app.py` – UI
- `config.py` – settings
- `services/` – PDF + AI logic (reusable for FastAPI later)
- `prompts/` – all AI prompts
Run Now
Bash

cd Smart-Notes-Organizer
pip install -r requirements.txt
streamlit run app.py
