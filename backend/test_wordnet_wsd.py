from nlp.wordnet_wsd import (
    perform_wsd,
    get_definition,
    get_examples,
    get_synonyms,
    get_antonyms,
    get_wordnet_relations
)


# ---------------------------------------
# WSD EXAMPLE 1
# ---------------------------------------

sentence1 = (
    "I went to the bank to deposit money."
)

target_word = "bank"

sense1 = perform_wsd(
    sentence1,
    target_word
)


print("\n========================================")
print("WORD SENSE DISAMBIGUATION")
print("========================================")

print("\nSentence:")
print(sentence1)

print("\nTarget word:")
print(target_word)

print("\nSelected sense:")

if sense1:
    print(sense1.name())
    print("Definition:", get_definition(sense1))

    examples = get_examples(sense1)

    print("Examples:", examples)

else:
    print("No sense found.")


# ---------------------------------------
# WSD EXAMPLE 2
# ---------------------------------------

sentence2 = (
    "The fisherman sat on the bank of the river."
)

sense2 = perform_wsd(
    sentence2,
    target_word
)

print("\n========================================")
print("SECOND WSD EXAMPLE")
print("========================================")

print("\nSentence:")
print(sentence2)

print("\nTarget word:")
print(target_word)

print("\nSelected sense:")

if sense2:
    print(sense2.name())
    print("Definition:", get_definition(sense2))

else:
    print("No sense found.")


# ---------------------------------------
# SYNONYMS
# ---------------------------------------

word = "good"

synonyms = get_synonyms(word)

print("\n========================================")
print("WORDNET SYNONYMS")
print("========================================")

print("Word:", word)
print("Synonyms:")

print(synonyms[:20])


# ---------------------------------------
# ANTONYMS
# ---------------------------------------

antonyms = get_antonyms(word)

print("\n========================================")
print("WORDNET ANTONYMS")
print("========================================")

print("Word:", word)
print("Antonyms:")

print(antonyms)


# ---------------------------------------
# WORDNET RELATIONS
# ---------------------------------------

relations = get_wordnet_relations("computer")

print("\n========================================")
print("WORDNET SEMANTIC RELATIONS")
print("========================================")

for relation in relations:

    print("\nSynset:")
    print(relation["synset"])

    print("Definition:")
    print(relation["definition"])

    print("Hypernyms:")
    print(relation["hypernyms"])

    print("Hyponyms:")
    print(relation["hyponyms"])