# prompts/prompts.py

ARRANGE_NOTES_PROMPT = """
You are an expert note-making assistant. Convert old, messy, unorganized notes into FULLY ARRANGED, clean, exam-ready notes.

Goal: A student should be able to revise directly from these notes.

RULES:
- Keep language simple and clear.
- Do NOT add unnecessary or invented information. Only organize and clarify what is given.
- Preserve original meaning.
- Use proper headings, subheadings and bullet points.
- Break long paragraphs into points.
- Skip any section if the given notes have no content for it.

FORMAT:

# Title (short suitable title)

## 1. Summary
4-5 line summary of the notes.

## 2. Learning Objectives
3-4 key learning points (bullets).

## 3. Detailed Notes
Topic-wise with Main Headings (##), Sub-headings (###) and bullet points (-). Point-wise, not big paragraphs.

## 4. Definitions
Important definitions (only if present).

## 5. Table (only if it improves understanding)

## 6. Examples (only if present)

## 7. Formulas / Equations (only if present)

## 8. Key Points to Remember
6-8 most important short points.

## 9. Important Exam Questions
4-5 probable short-answer questions from the given notes.

## 10. Quick Revision
8-10 very short bullets for 5-minute revision.

Messy/Old Notes:
{notes}
"""

SUMMARY_PROMPT = """
Summarize the following study notes in simple language.

# Summary

## One Line Summary
(1 short line)

## Brief Summary
(60-80 words, short lines)

## Key Takeaways
(5-6 bullet points)

Notes:
{notes}
"""

FLASHCARDS_PROMPT = """
Create 8-10 study flashcards from the notes for recall practice.

Rules:
- Short clear questions.
- Short answers (1-3 lines).
- Cover definitions, terms, concepts, facts.

Format:

**Q1.** ...
**A1.** ...

**Q2.** ...
**A2.** ...

Notes:
{notes}
"""

QUIZ_PROMPT = """
Create exactly 5 MCQs based ONLY on the given notes.

Rules:
- 4 options each (A, B, C, D).
- One correct answer.
- Exam-level, clear (not confusing).

Format:

## MCQ Practice

**Q1.** ...
A) ...
B) ...
C) ...
D) ...

**Correct Answer:** A

(repeat for 5 questions)

Notes:
{notes}
"""

EXPLAIN_PROMPT = """
Explain the given notes in very simple language (class 8-10 level), like teaching a student.
Use simple examples from the topic itself where helpful.

# Simple Explanation

Explain point by point with bullets.

Notes:
{notes}
"""

HINDI_NOTES_PROMPT = """
Rearrange the following notes into clean, well-structured notes in simple Hindi.
Keep the meaning exactly the same. Do not add unrelated information.
Use proper headings, subheadings and bullet points.

Given Notes:
{notes}
"""

# Maps option -> prompt (used in ai_service)
PROMPT_MAP = {
    "arrange": ARRANGE_NOTES_PROMPT,
    "summary": SUMMARY_PROMPT,
    "flashcards": FLASHCARDS_PROMPT,
    "quiz": QUIZ_PROMPT,
    "explain": EXPLAIN_PROMPT,
    "hindi": HINDI_NOTES_PROMPT,
}