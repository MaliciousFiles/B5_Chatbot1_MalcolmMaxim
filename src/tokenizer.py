"""Tokenizes questions/comments to the bot with the help of NLTK.

There are two main functions:
- ``tokenize``: tokenizes, lemmatizes, spellchecks, and gets
synonyms for user input.
- ``get_synonyms``: gets synonyms for a particlar token. Used
by ``tokenize``.
"""

from nltk.corpus import wordnet
from nltk.data import path
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from spellchecker import SpellChecker

from pathlib import Path

#
# Startup
#

# BAD. I know, vendor lock-in. But right now we're
# doing it on replit, so it's fine.
path.append(
    str(
        Path("~/B5Chatbot1MalcolmMaxim/nltk_data").expanduser()
    )
)

# Class instances
lemmatizer = WordNetLemmatizer()
spellcheck = SpellChecker()

#
# Functions
#

def tokenize(user_input):
    """Peforms tokenization on user input as well as multiple
    other parsing steps including spellchecking, synonym generation
    and lemmatization.
    """
    lowercase_tokens = [t.lower() for t in word_tokenize(user_input)]
    tokens = []
    for token in lowercase_tokens:
        spellchecked = list(spellcheck.candidates(token))
        child_tokens = []
        for spellchecked_token in spellchecked:
            child_tokens.extend(get_synonyms(spellchecked_token))
        tokens.extend(child_tokens)
    tokens = [lemmatizer.lemmatize(t) for t in tokens]
    print(tokens)
    return tokens

def get_synonyms(token):
    """Returns a list of synonyms for ``token``.
    """
    result = {token}
    for context in wordnet.synsets(token):
        synonyms = context.lemma_names()
        result.update([i.lower() for i in synonyms])
    return list(result)
