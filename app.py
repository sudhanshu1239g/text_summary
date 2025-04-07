import streamlit as st
import nltk
import re
import heapq
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# ✅ Download necessary NLTK data inside a try block
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

# 🧠 Streamlit UI
st.title("📝 Text Summarizer")

text = st.text_area("Enter your text to summarize:")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        # 1. Tokenize into sentences
        sentences = sent_tokenize(text)

        # 2. Word frequency table
        stop_words = set(stopwords.words("english"))
        word_frequencies = {}

        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # 3. Normalize frequencies
        max_freq = max(word_frequencies.values(), default=1)
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        # 4. Score sentences
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

        # 5. Get top 3 sentences
        summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        st.subheader("Summary:")
        st.success(summary)
