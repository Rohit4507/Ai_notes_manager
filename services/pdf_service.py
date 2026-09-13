# services/pdf_service.py
import fitz  # PyMuPDF
from config import MAX_PDF_PAGES, MAX_CHARS


class PDFError(Exception):
    """Custom error for PDF issues."""
    pass


def extract_text_from_pdf(pdf_bytes: bytes) -> str:
    """
    Extract readable text from a PDF (bytes).
    Raises PDFError with a clear message on failure.
    """
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
    except Exception:
        raise PDFError("This file could not be opened as a PDF. Please upload a valid PDF.")

    if doc.page_count == 0:
        doc.close()
        raise PDFError("This PDF has no pages.")

    if doc.page_count > MAX_PDF_PAGES:
        pages_to_read = MAX_PDF_PAGES
    else:
        pages_to_read = doc.page_count

    full_text = ""
    for i in range(pages_to_read):
        page = doc[i]
        text = page.get_text("text")
        if text:
            full_text += text + "\n\n"

    doc.close()

    # Clean empty lines
    full_text = "\n".join(line for line in full_text.splitlines() if line.strip())
    full_text = full_text.strip()

    if not full_text:
        raise PDFError(
            "No readable text found. This looks like a scanned/handwritten PDF. "
            "OCR support can be added later."
        )

    # Trim if too long (protect API)
    if len(full_text) > MAX_CHARS:
        full_text = full_text[:MAX_CHARS]

    return full_text


def get_pdf_stats(pdf_bytes: bytes) -> dict:
    """Return quick stats about the PDF."""
    try:
        doc = fitz.open(stream=pdf_bytes, filetype="pdf")
        pages = doc.page_count
        doc.close()
        return {"pages": pages}
    except Exception:
        return {"pages": 0}
    