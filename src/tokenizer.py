# Tokenizes questions/comments with the help of NLTK

from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.data import path
from nltk.corpus import wordnet

from spellchecker import SpellChecker

from pathlib import Path

path.append(str(Path("~/B5Chatbot1MalcolmMaxim/nltk_data").expanduser()))

lemmatizer = WordNetLemmatizer()
spellcheck = SpellChecker()


def tokenize(user_input):
    tokens = [t.lower() for t in word_tokenize(user_input)] # split into tokens
    # spell check
    for i in range(len(tokens)):
        tokens += spellcheck.candidates(tokens.pop(i))
    tokens = get_synonyms_for_tokens(tokens) # add synonyms
    lemmatized = [lemmatizer.lemmatize(t) for t in tokens] # lemmatize
    return lemmatized

def get_synonyms(token):
    result = {token}
    for context in wordnet.synsets(token):
        synonyms = context.lemma_names()
        result.update([i.lower() for i in synonyms])
    return list(result)


def get_synonyms_for_tokens(tokens):
    result = set(tokens)
    for token in tokens:
        result.update(get_synonyms(token))
    return list(result)