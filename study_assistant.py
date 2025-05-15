# pdf_summarizer_app.py

import os
# 🔒 Prevent Streamlit + torch.classes crash
os.environ["STREAMLIT_WATCHER_TYPE"] = "none"
import streamlit as st
import pdfplumber
from transformers import pipeline



# 📄 Page setup
st.set_page_config(page_title="AI PDF Summarizer", page_icon="📚")
st.title("📚 AI PDF Summarizer")

# 🧠 Load model (cached)
@st.cache_resource
def load_model():
    return pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")

summarizer = load_model()

# 📤 File uploader
uploaded_file = st.file_uploader("Upload a PDF or TXT file", type=["pdf", "txt"])

# 🧾 Extract text
def extract_text(file):
    if file.name.endswith(".txt"):
        return file.read().decode("utf-8")
    elif file.name.endswith(".pdf"):
        full_text = ""
        with pdfplumber.open(file) as pdf:
            for i, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text += text + "\n"
                else:
                    st.warning(f"⚠️ No text found on page {i+1}")
        return full_text
    return ""

# 📚 Summarize in chunks
def summarize_text(text, chunk_size=1024, max_chunks=5):
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    summaries = []
    for chunk in chunks[:max_chunks]:  # Limit for speed
        try:
            result = summarizer(chunk, max_length=150, min_length=40, do_sample=False)
            summaries.append(result[0]["summary_text"])
        except Exception as e:
            st.error(f"Error summarizing chunk: {e}")
    return "\n\n".join(summaries)

# 🖼️ App interface
if uploaded_file:
    text = extract_text(uploaded_file)

    if not text.strip():
        st.error("❌ No extractable text found.")
    else:
        st.subheader("📄 Preview of Extracted Text")
        st.text_area("Text Preview", text[:2000], height=200)

        if st.button("✨ Generate Summary"):
            with st.spinner("Summarizing..."):
                summary = summarize_text(text)
                st.subheader("🧠 Summary")
                st.write(summary)
