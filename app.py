import streamlit as st
import nltk
import re
import heapq
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# ✅ Download punkt and stopwords to default NLTK data path
nltk.download("punkt")
nltk.download("stopwords")

# 🧠 Streamlit UI
st.title("📝 Text Summarizer App")

text = st.text_area("Enter your text below:")

if st.button("Summarize"):
    if text.strip() == "":
        st.warning("Please enter some text to summarize.")
    else:
        # 1. Tokenize into sentences
        sentences = sent_tokenize(text)

        # 2. Clean text
        stop_words = set(stopwords.words("english"))
        word_frequencies = {}
        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        # 3. Normalize frequencies
        max_freq = max(word_frequencies.values())
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        # 4. Score sentences
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

        # 5. Pick top 3 sentences
        summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        st.subheader("Summary:")
        st.success(summary)
