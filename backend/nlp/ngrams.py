from collections import Counter
import math


def generate_ngrams(tokens, n):
    """
    Generate N-grams from a list of tokens.
    """

    ngrams = []

    for i in range(len(tokens) - n + 1):
        ngram = tuple(tokens[i:i + n])
        ngrams.append(ngram)

    return ngrams


def calculate_counts(tokens):
    """
    Calculate unigram, bigram and trigram counts.
    """

    unigram_counts = Counter(
        generate_ngrams(tokens, 1)
    )

    bigram_counts = Counter(
        generate_ngrams(tokens, 2)
    )

    trigram_counts = Counter(
        generate_ngrams(tokens, 3)
    )

    return (
        unigram_counts,
        bigram_counts,
        trigram_counts
    )


def unigram_probability(word, unigram_counts, total_words):
    """
    Calculate probability of a word using
    the unigram model.
    """

    count = unigram_counts.get((word,), 0)

    return count / total_words


def bigram_probability(
    word1,
    word2,
    unigram_counts,
    bigram_counts
):
    """
    Calculate conditional probability:

    P(word2 | word1)
    """

    bigram_count = bigram_counts.get(
        (word1, word2),
        0
    )

    unigram_count = unigram_counts.get(
        (word1,),
        0
    )

    if unigram_count == 0:
        return 0

    return bigram_count / unigram_count


def trigram_probability(
    word1,
    word2,
    word3,
    bigram_counts,
    trigram_counts
):
    """
    Calculate conditional probability:

    P(word3 | word1, word2)
    """

    trigram_count = trigram_counts.get(
        (word1, word2, word3),
        0
    )

    bigram_count = bigram_counts.get(
        (word1, word2),
        0
    )

    if bigram_count == 0:
        return 0

    return trigram_count / bigram_count


def sequence_probability(
    sequence,
    unigram_counts,
    bigram_counts
):
    """
    Calculate sequence probability using
    the bigram model.
    """

    probability = 1.0

    for i in range(1, len(sequence)):

        word1 = sequence[i - 1]
        word2 = sequence[i]

        prob = bigram_probability(
            word1,
            word2,
            unigram_counts,
            bigram_counts
        )

        if prob == 0:
            return 0

        probability *= prob

    return probability


def calculate_perplexity(
    sequence,
    unigram_counts,
    bigram_counts
):
    """
    Calculate perplexity using a bigram model.
    """

    probability = sequence_probability(
        sequence,
        unigram_counts,
        bigram_counts
    )

    if probability == 0:
        return float("inf")

    N = len(sequence) - 1

    perplexity = math.pow(
        1 / probability,
        1 / N
    )

    return perplexity