import nltk

# 🔐 Force download BEFORE anything else
nltk.download("punkt")
nltk.download("stopwords")

import streamlit as st
import re
import heapq
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

st.title("📝 Text Summarizer (Streamlit + NLTK)")

text = st.text_area("Paste your text here:")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text!")
    else:
        # Step 1: Sentence Tokenization
        sentences = sent_tokenize(text)

        # Step 2: Word Frequency Table
        stop_words = set(stopwords.words("english"))
        word_frequencies = {}

        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # Step 3: Normalize frequencies
        max_freq = max(word_frequencies.values(), default=1)
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        # Step 4: Score sentences
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

        # Step 5: Get Top 3 Sentences
        summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        st.subheader("Summary:")
        st.success(summary)
