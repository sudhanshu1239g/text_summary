import streamlit as st
import nltk
import os
import heapq
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize


# 🔽 NLTK setup for Streamlit Cloud
nltk_data_path = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_path, exist_ok=True)
nltk.data.path.append(nltk_data_path)

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', download_dir=nltk_data_path)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', download_dir=nltk_data_path)

# Download resources once
nltk.download('punkt')
nltk.download('stopwords')

# Streamlit UI
st.set_page_config(page_title="Text Summarizer", layout="centered")
st.title("🧠 AI Text Summarizer")
st.write("Paste any long text below, and get a short summary using basic NLP.")

# Text input area
user_text = st.text_area("📜 Enter your text here:", height=250)

# Summary length slider
summary_length = st.slider("How many sentences should the summary have?", 1, 5, 3)

if st.button("✨ Summarize"):
    if not user_text.strip():
        st.warning("Please enter some text first.")
    else:
        # Step 1: Clean text
        text = re.sub(r'\s+', ' ', user_text)
        sentences = sent_tokenize(text)

        # Step 2: Word frequency table
        stop_words = set(stopwords.words("english"))
        word_frequencies = {}

        for word in word_tokenize(text.lower()):
            if word.isalpha() and word not in stop_words:
                if word not in word_frequencies:
                    word_frequencies[word] = 1
                else:
                    word_frequencies[word] += 1

        # Step 3: Sentence scores
        sentence_scores = {}
        for sent in sentences:
            for word in word_tokenize(sent.lower()):
                if word in word_frequencies:
                    if len(sent.split(' ')) < 30:
                        if sent not in sentence_scores:
                            sentence_scores[sent] = word_frequencies[word]
                        else:
                            sentence_scores[sent] += word_frequencies[word]

        # Step 4: Summary
        summary_sentences = heapq.nlargest(summary_length, sentence_scores, key=sentence_scores.get)
        summary = ' '.join(summary_sentences)

        st.subheader("✅ Summary:")
        st.success(summary)
