from nlp.ngrams import (
    generate_ngrams,
    calculate_counts,
    unigram_probability,
    bigram_probability,
    trigram_probability,
    sequence_probability,
    calculate_perplexity
)


# -----------------------------------------
# SAMPLE TEXT
# -----------------------------------------

text = """
machine learning is a field of artificial intelligence
machine learning uses data
natural language processing is a field of artificial intelligence
"""


# Convert text into simple tokens
tokens = text.lower().split()


# -----------------------------------------
# GENERATE N-GRAMS
# -----------------------------------------

unigrams = generate_ngrams(tokens, 1)
bigrams = generate_ngrams(tokens, 2)
trigrams = generate_ngrams(tokens, 3)


print("\n==========================================")
print("UNIGRAMS")
print("==========================================")

print(unigrams)


print("\n==========================================")
print("BIGRAMS")
print("==========================================")

print(bigrams)


print("\n==========================================")
print("TRIGRAMS")
print("==========================================")

print(trigrams)


# -----------------------------------------
# COUNTS
# -----------------------------------------

unigram_counts, bigram_counts, trigram_counts = (
    calculate_counts(tokens)
)


print("\n==========================================")
print("N-GRAM COUNTS")
print("==========================================")

print("\nUnigram counts:")
print(unigram_counts)

print("\nBigram counts:")
print(bigram_counts)

print("\nTrigram counts:")
print(trigram_counts)


# -----------------------------------------
# PROBABILITY
# -----------------------------------------

word = "machine"

prob = unigram_probability(
    word,
    unigram_counts,
    len(tokens)
)

print("\n==========================================")
print("UNIGRAM PROBABILITY")
print("==========================================")

print(
    f"P({word}) = {prob:.4f}"
)


prob = bigram_probability(
    "machine",
    "learning",
    unigram_counts,
    bigram_counts
)

print("\n==========================================")
print("BIGRAM PROBABILITY")
print("==========================================")

print(
    "P(learning | machine) = "
    f"{prob:.4f}"
)


prob = trigram_probability(
    "machine",
    "learning",
    "is",
    bigram_counts,
    trigram_counts
)

print("\n==========================================")
print("TRIGRAM PROBABILITY")
print("==========================================")

print(
    "P(is | machine, learning) = "
    f"{prob:.4f}"
)


# -----------------------------------------
# SEQUENCE PROBABILITY
# -----------------------------------------

sequence = [
    "machine",
    "learning",
    "is",
    "a",
    "field"
]

probability = sequence_probability(
    sequence,
    unigram_counts,
    bigram_counts
)

print("\n==========================================")
print("SEQUENCE PROBABILITY")
print("==========================================")

print(
    "Sequence:",
    " ".join(sequence)
)

print(
    "Probability:",
    probability
)


# -----------------------------------------
# PERPLEXITY
# -----------------------------------------

perplexity = calculate_perplexity(
    sequence,
    unigram_counts,
    bigram_counts
)

print("\n==========================================")
print("PERPLEXITY")
print("==========================================")

print(
    "Perplexity:",
    perplexity
)