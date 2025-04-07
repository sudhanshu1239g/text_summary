import nltk
import os
import streamlit as st
import heapq
import re
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

# 🚨 Force download + suppress re-download if already present
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
if not os.path.exists(nltk_data_dir):
    os.mkdir(nltk_data_dir)

nltk.data.path.append(nltk_data_dir)
nltk.download('punkt', download_dir=nltk_data_dir)
nltk.download('stopwords', download_dir=nltk_data_dir)

# Streamlit app
st.title("🧠 Text Summarizer")

text = st.text_area("Paste the text you want to summarize:")

if st.button("Summarize"):
    if not text.strip():
        st.warning("Please enter some text to summarize.")
    else:
        sentences = sent_tokenize(text)
        stop_words = set(stopwords.words("english"))
        word_frequencies = {}

        for word in word_tokenize(text.lower()):
            if word.isalnum() and word not in stop_words:
                word_frequencies[word] = word_frequencies.get(word, 0) + 1

        max_freq = max(word_frequencies.values(), default=1)
        for word in word_frequencies:
            word_frequencies[word] /= max_freq

        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    sentence_scores[sent] = sentence_scores.get(sent, 0) + word_frequencies[word]

        summary_sentences = heapq.nlargest(3, sentence_scores, key=sentence_scores.get)
        summary = " ".join(summary_sentences)

        st.subheader("✂️ Summary:")
        st.success(summary)
