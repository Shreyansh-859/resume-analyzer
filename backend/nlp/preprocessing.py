import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords


def tokenize_text(text):
    """
    Break the input text into individual tokens.
    """
    tokens = word_tokenize(text)
    return tokens


def remove_stopwords(tokens):
    """
    Remove common English stop words.
    """
    stop_words = set(stopwords.words("english"))

    filtered_words = []

    for word in tokens:
        if word.lower() not in stop_words:
            filtered_words.append(word)

    return filtered_words


def preprocess_text(text):
    """
    Perform basic text preprocessing.
    """
    tokens = tokenize_text(text)

    filtered_tokens = remove_stopwords(tokens)

    return tokens, filtered_tokens
def validate_script(text):
    """
    Check whether the text mainly contains
    English/Latin alphabet characters.
    """

    letters = []

    for char in text:
        if char.isalpha():
            letters.append(char)

    if len(letters) == 0:
        return {
            "valid": False,
            "message": "No alphabetic characters found."
        }

    latin_letters = 0

    for char in letters:
        if ('a' <= char.lower() <= 'z'):
            latin_letters += 1

    percentage = (latin_letters / len(letters)) * 100

    return {
        "valid": percentage >= 70,
        "latin_percentage": round(percentage, 2)
    }