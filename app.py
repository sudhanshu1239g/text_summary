import streamlit as st
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import re

st.set_page_config(page_title="Smart Text Summarizer", layout="centered")
st.title("🧠 Smart Text Summarizer")

def split_into_sentences(text):
    # Simple regex-based sentence splitter
    sentences = re.split(r'(?<=[.!?]) +', text)
    return [s.strip() for s in sentences if len(s.strip()) > 0]

def summarize_text(text, num_sentences=3):
    sentences = split_into_sentences(text)
    
    if len(sentences) <= num_sentences:
        return sentences

    # TF-IDF Vectorization
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(sentences)

    # Sentence similarity matrix
    similarity_matrix = cosine_similarity(tfidf_matrix, tfidf_matrix)

    # Rank sentences using similarity to others
    scores = similarity_matrix.sum(axis=1)
    ranked_sentences = [sentences[i] for i in np.argsort(scores)[-num_sentences:]]
    
    # Keep original order
    summary = sorted(ranked_sentences, key=lambda s: sentences.index(s))
    return summary

text = st.text_area("Enter text to summarize:", height=300)

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text.")
    else:
        summary = summarize_text(text)
        st.subheader("🔍 Summary:")
        for sentence in summary:
            st.write(f"• {sentence}")
