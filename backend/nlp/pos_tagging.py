import nltk
from nltk import word_tokenize
from nltk import pos_tag


def tokenize_sentence(sentence):
    """
    Convert a sentence into individual tokens.
    """
    return word_tokenize(sentence)


def probabilistic_pos_tagging(sentence):
    """
    POS tagging using NLTK's trained probabilistic tagger.
    """
    tokens = tokenize_sentence(sentence)

    tagged_words = pos_tag(tokens)

    return tagged_words


def rule_based_pos_tagging(sentence):
    """
    Simple rule-based POS tagger.

    This is intentionally small so that
    the rules can be understood easily.
    """

    tokens = tokenize_sentence(sentence)

    tagged_words = []

    for word in tokens:

        lower_word = word.lower()

        # Determiners
        if lower_word in ["a", "an", "the"]:
            tag = "DT"

        # Pronouns
        elif lower_word in [
            "i", "you", "he", "she",
            "we", "they", "it"
        ]:
            tag = "PRP"

        # Common verbs
        elif lower_word in [
            "is", "am", "are",
            "was", "were",
            "be", "have", "has",
            "do", "does"
        ]:
            tag = "VB"

        # Words ending in -ing
        elif lower_word.endswith("ing"):
            tag = "VBG"

        # Words ending in -ly
        elif lower_word.endswith("ly"):
            tag = "RB"

        # Words ending in -ed
        elif lower_word.endswith("ed"):
            tag = "VBD"

        # Simple adjective rule
        elif lower_word.endswith(
            ("ous", "ful", "able", "ive", "al")
        ):
            tag = "JJ"

        # Proper noun heuristic
        elif word[0].isupper():
            tag = "NNP"

        # Default
        else:
            tag = "NN"

        tagged_words.append((word, tag))

    return tagged_words