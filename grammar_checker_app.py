import streamlit as st
import nltk
from nltk import pos_tag, download
from nltk.tokenize import word_tokenize
from nltk.data import find

# Set Streamlit page config FIRST
st.set_page_config(page_title="Grammar Checker", layout="centered")

# Function to download required NLTK data
import nltk
from nltk.data import find
import streamlit as st

def download_nltk_data():
    # Download 'punkt' tokenizer
    try:
        find('tokenizers/punkt')
    except LookupError:
        try:
            st.info("Downloading required tokenizer: punkt")
            nltk.download('punkt', quiet=True, raise_on_error=False)
        except:
            st.error("Could not download 'punkt' tokenizer.")

    # Download 'averaged_perceptron_tagger'
    try:
        find('taggers/averaged_perceptron_tagger')
    except LookupError:
        try:
            st.info("Downloading required tagger: averaged_perceptron_tagger")
            nltk.download('averaged_perceptron_tagger', quiet=True, raise_on_error=False)
        except:
            st.error("Could not download 'averaged_perceptron_tagger'.")

# Download necessary NLTK data
download_nltk_data()

# Grammar rules: (POS tag pairs → status)
grammar_rules = [
    (('DT', 'JJ', 'NN'), "OK"),
    (('DT', 'NN'), "OK"),
    (('JJ', 'NN'), "OK"),
    (('NN', 'VB'), "Error"),       
    (('VB', 'VB'), "Check"),       
    (('RB', 'RB'), "Check")        
]

# Grammar checking function
def check_grammar(sentence):
    tokens = word_tokenize(sentence)
    tagged = pos_tag(tokens)
    issues = []

    for i in range(len(tagged) - 1):
        pair = (tagged[i][1], tagged[i+1][1])
        for rule in grammar_rules:
            if pair == rule[0][:2]:
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
