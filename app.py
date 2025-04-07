import streamlit as st

st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("📝 Simple Text Summarizer")

text = st.text_area("Enter text to summarize:", height=300)

def summarize(text, max_sentences=3):
    # Naive sentence splitter (no nltk)
    sentences = text.replace("\n", " ").split(". ")
    sentences = [s.strip() for s in sentences if len(s.strip()) > 20]
    # Pick the first few sentences (you can add more logic later)
    return sentences[:max_sentences]

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        summary = summarize(text)
        st.subheader("Summary:")
        for sentence in summary:
            st.write(f"• {sentence}")
