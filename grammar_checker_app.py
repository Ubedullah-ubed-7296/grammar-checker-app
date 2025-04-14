import streamlit as st
import nltk
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import os

# Set page configuration before any other Streamlit UI elements
st.set_page_config(page_title="Grammar Checker", layout="centered")

# Ensure required NLTK data is downloaded
def download_nltk_data():
    try:
        nltk.data.find('tokenizers/punkt')
    except LookupError:
        st.write("Downloading 'punkt' tokenizer data...")
        nltk.download('punkt')

    try:
        nltk.data.find('taggers/averaged_perceptron_tagger')
    except LookupError:
        st.write("Downloading 'averaged_perceptron_tagger' tagger data...")
        nltk.download('averaged_perceptron_tagger')

# Add the specific NLTK data path
nltk.data.path.append(r'/root/nltk_data')  # This is a typical path on Streamlit Cloud or Docker-based environments

# Download NLTK data
download_nltk_data()

# Define grammar rules
grammar_rules = [
    (('DT', 'JJ', 'NN'), "OK"),
    (('DT', 'NN'), "OK"),
    (('JJ', 'NN'), "OK"),
    (('NN', 'VB'), "Error"),       
    (('VB', 'VB'), "Check"),       
    (('RB', 'RB'), "Check")        
]

def check_grammar(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    issues = []

    # Check consecutive pairs
    for i in range(len(tagged) - 1):
        pair = (tagged[i][1], tagged[i+1][1])
        for rule in grammar_rules:
            if pair == rule[0]:
                if rule[1] != "OK":
                    issues.append((tagged[i][0], tagged[i+1][0], rule[1]))

    return tagged, issues

# Streamlit UI
st.title("📝 Simple Grammar Checker")
sentence = st.text_area("Enter a sentence to check:", height=150)

if st.button("Check Grammar"):
    if not sentence.strip():
        st.warning("Please enter a sentence.")
    else:
        tagged, issues = check_grammar(sentence)

        st.subheader("📌 POS Tags")
        for word, tag in tagged:
            st.markdown(f"**{word}** — `{tag}`")

        if issues:
            st.subheader("⚠️ Grammar Issues Found")
            for w1, w2, issue in issues:
                st.error(f"'{w1} {w2}' ➤ {issue}")
        else:
            st.success("✅ No grammatical issues found based on the current rules.")
