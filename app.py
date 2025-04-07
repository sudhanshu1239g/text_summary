import streamlit as st
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer

st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("📝 Text Summarizer")

text = st.text_area("Enter text to summarize:", height=300)

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        parser = PlaintextParser.from_string(text, Tokenizer("english"))
        summarizer = LsaSummarizer()
        summary = summarizer(parser.document, sentences_count=3)

        st.subheader("Summary:")
        for sentence in summary:
            st.write(str(sentence))
