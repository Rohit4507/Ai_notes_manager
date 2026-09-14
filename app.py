# app.py
import streamlit as st

import config
from services.pdf_service import extract_text_from_pdf, get_pdf_stats, PDFError
from services.ai_service import setup_gemini, generate, AIError
import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

def save_feedback(comment):
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    credentials = Credentials.from_service_account_file(
        "credentials.json",
        scopes=scopes,
    )

    client = gspread.authorize(credentials)

    sheet = client.open("Smart Notes Feedback").sheet1

    sheet.append_row([
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        comment.strip(),
    ])

    return True


# ---------------- Page Setup ----------------
st.set_page_config(
    page_title=config.APP_TITLE,
    page_icon=config.APP_ICON,
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
<style>
    .main-title {
        font-size: 2.7rem; font-weight: 800; text-align: center;
        background: linear-gradient(90deg, #4A90E2, #50C878);
        -webkit-background-clip: text; -webkit-text-fill-color: transparent;
        margin-bottom: 0.2rem; line-height: 1.2;
    }
    .subtitle { text-align:center; font-size:1.05rem; color:#666; margin-bottom:2rem; }
    .stButton>button {
        background: linear-gradient(90deg, #4A90E2, #3B7BD9);
        color:#fff; font-weight:600; padding:0.7rem 1.5rem;
        border-radius:12px; border:none;
        box-shadow:0 4px 12px rgba(74,144,226,0.2); transition:all .2s;
    }
    .stButton>button:hover { transform:translateY(-1px); color:#fff;
        box-shadow:0 6px 16px rgba(74,144,226,0.3); }
    .info-box { background:#e7f3ff; padding:1rem 1.2rem; border-radius:10px;
        border-left:4px solid #1f7ae0; color:#1f2937; }
    .feature-box { background:#f7f9fc; padding:1rem; border-radius:12px;
        border-left:4px solid #4A90E2; margin-bottom:1rem; }
</style>
""",
    unsafe_allow_html=True,
)


# ---------------- Cache the model ----------------
@st.cache_resource
def load_model():
    return setup_gemini(config.GEMINI_API_KEY)


# ---------------- Options ----------------
OPTIONS = {
    "✨ Fully Arranged Clean Notes (Recommended)": "arrange",
    "📝 Quick Summary": "summary",
    "🃏 Make Flashcards": "flashcards",
    "📋 Create MCQ Quiz": "quiz",
    "🧑‍🏫 Explain Like a Teacher": "explain",
    "🇮🇳 Convert to Hindi Notes": "hindi",
}

SPINNER_MSG = {
    "arrange": "🧹 Rearranging into clean structured notes...",
    "summary": "📝 Creating summary...",
    "flashcards": "🃏 Generating flashcards...",
    "quiz": "📋 Creating MCQs...",
    "explain": "🧠 Explaining in simple words...",
    "hindi": "🇮🇳 Converting to Hindi notes...",
}


# ---------------- Sidebar ----------------
def render_sidebar():
    with st.sidebar:
        st.markdown("## About")
        st.markdown(
            '<div class="feature-box">Convert old/messy notes into clean, '
            "structured, exam-ready notes using AI.</div>",
            unsafe_allow_html=True,
        )

        st.markdown("## Features")
        st.markdown(
            """
- 📄 Upload PDF
- 🧾 Fully Arranged Notes
- 📝 Summary
- 🃏 Flashcards
- 📋 MCQ Quiz
- 🧑‍🏫 Simple Explanation
- 🇮🇳 Hindi Notes
- ⬇️ Download (.md / .txt)
            """
        )

        st.markdown("---")
        st.markdown("## Status")

        if not config.GEMINI_API_KEY:
            st.error("❌ API Key Missing")
            st.info(
                "Create a `.env` file and add:\n\n"
                "`GEMINI_API_KEY=your_key`\n\n"
                "Get key: https://aistudio.google.com/"
            )
            st.stop()

        st.success("✅ API Key Connected")
        st.caption(f"Max pages read: {config.MAX_PDF_PAGES}")
        st.caption("Best with typed (non-scanned) PDFs.")

        



# ---------------- Main ----------------
def main():
    st.markdown(f'<h1 class="main-title">{config.APP_ICON} {config.APP_TITLE}</h1>',
                unsafe_allow_html=True)
    st.markdown(
        '<p class="subtitle">Upload old/messy notes (PDF) → Get fully arranged, '
        "clean & exam-ready notes</p>",
        unsafe_allow_html=True,
    )

    render_sidebar()

    # Load model (cached)
    try:
        model = load_model()
    except AIError as e:
        st.error(f"AI setup failed: {e}")
        st.stop()

    st.markdown(
        '<div class="info-box">💡 Upload your notes PDF. AI will rearrange them into '
        "headings, bullets, summary, important questions & quick revision.</div>",
        unsafe_allow_html=True,
    )
    st.write("")

    # ---- Upload ----
    uploaded_file = st.file_uploader("Upload PDF", type=["pdf"])

    extracted_text = ""

    if uploaded_file is not None:
        # File size check
        size_mb = len(uploaded_file.getvalue()) / (1024 * 1024)
        if size_mb > config.MAX_FILE_SIZE_MB:
            st.error(
                f"File is {size_mb:.1f} MB. Max allowed is "
                f"{config.MAX_FILE_SIZE_MB} MB. Please upload a smaller PDF."
            )
        else:
            with st.spinner("📄 Extracting text from PDF..."):
                try:
                    pdf_bytes = uploaded_file.getvalue()
                    stats = get_pdf_stats(pdf_bytes)
                    extracted_text = extract_text_from_pdf(pdf_bytes)

                    words = len(extracted_text.split())
                    c1, c2, c3 = st.columns(3)
                    c1.metric("Words", f"{words:,}")
                    c2.metric("Characters", f"{len(extracted_text):,}")
                    c3.metric("PDF Pages", stats.get("pages", "-"))

                    st.success(f"✅ Text extracted from '{uploaded_file.name}'")

                    with st.expander("👁️ Preview extracted text (first 400 words)"):
                        preview = " ".join(extracted_text.split()[:400])
                        st.text_area("Preview", preview + " ...",
                                     height=150, disabled=True)

                except PDFError as e:
                    st.warning(f"⚠️ {e}")
                    extracted_text = ""
                except Exception as e:
                    st.error(f"Unexpected error: {e}")
                    extracted_text = ""

    st.markdown("---")

    # ---- Choose task ----
    st.subheader("1. What do you want?")
    choice = st.radio("Select", list(OPTIONS.keys()),
                      horizontal=True, label_visibility="collapsed")
    task = OPTIONS[choice]

    st.markdown("---")

    # ---- Generate ----
    if st.button("🚀 Generate", type="primary",
                 use_container_width=True, disabled=not extracted_text):
        with st.spinner(SPINNER_MSG[task]):
            try:
                result = generate(model, task, extracted_text)
                st.session_state["result"] = result
                st.session_state["result_task"] = task
            except AIError as e:
                st.error(f"❌ {e}")
                st.info("Try again, or upload a smaller PDF.")

    # ---- Result ----
    if "result" in st.session_state:
        st.markdown("---")
        st.subheader("2. Your Result")
        st.markdown(st.session_state["result"])

        st.markdown("---")
        st.subheader("3. Download")
        d1, d2 = st.columns(2)
        d1.download_button(
            "⬇️ Download .md",
            data=st.session_state["result"],
            file_name="clean-notes.md",
            mime="text/markdown",
            use_container_width=True,
        )
        d2.download_button(
            "⬇️ Download .txt",
            data=st.session_state["result"],
            file_name="clean-notes.txt",
            mime="text/plain",
            use_container_width=True,
        )

    elif not uploaded_file:
        st.markdown("---")
        st.markdown(
            """
### How it works
1. **Upload** your messy notes PDF
2. **Choose** what you want (Notes / Summary / Flashcards / Quiz)
3. **Download** clean, arranged notes in 1 click
            """
        )

    st.markdown("---")
    st.markdown(
        "<div style='text-align:center;color:#9ca3af;padding:1rem;'>"
        "Smart Notes Organizer • Streamlit + Google Gemini AI</div>",
        unsafe_allow_html=True,
    )

# ---------------- Suggestions & Feedback ----------------

col_suggestion, col_support = st.columns(2)

with col_suggestion:
    st.markdown("### 💡 Your Suggestions")

    suggestion = st.text_area(
        "Comment your suggestion...",
        placeholder="Tell me what you would like to improve or add.",
        label_visibility="collapsed",
        height=50,
    )

    btn_col = st.columns([1, 5, 1])[1]

with btn_col:
    if st.button("📩 Submit"):
        if suggestion.strip():
            try:
                save_feedback(suggestion)
                st.success("Thanks! Your suggestion has been submitted. ❤️")

            except Exception as e:
                import traceback
                st.error(f"Error: {repr(e)}")
                st.code(traceback.format_exc())

        else:
            st.warning("Please enter a suggestion first.")


with col_support:
    st.markdown("### ☕ Support the Project")

    st.caption(
        "If this tool helped you, you can support its development. ❤️"
    )

    st.link_button(
    "🚬 Buy Me a Choti advanced",
    "https://www.buymeacoffee.com/rohit06",
    use_container_width=True,
)


if __name__ == "__main__":
    main()