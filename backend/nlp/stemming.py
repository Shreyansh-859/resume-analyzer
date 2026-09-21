import nltk

from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer


# Create stemming and lemmatization objects
stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()


def perform_stemming(words):
    """
    Apply Porter stemming to a list of words.
    """
    stemmed_words = []

    for word in words:
        stemmed_word = stemmer.stem(word)
        stemmed_words.append(stemmed_word)

    return stemmed_words


def perform_lemmatization(words):
    """
    Apply WordNet lemmatization to a list of words.
    """
    lemmatized_words = []

    for word in words:
        lemma = lemmatizer.lemmatize(word)
        lemmatized_words.append(lemma)

    return lemmatized_words


def compare_stemming_lemmatization(words):
    """
    Compare original words, stems and lemmas.
    """

    stemmed = perform_stemming(words)
    lemmatized = perform_lemmatization(words)

    comparison = []

    for i in range(len(words)):
        comparison.append({
            "original": words[i],
            "stemmed": stemmed[i],
            "lemmatized": lemmatized[i]
        })

    return comparison