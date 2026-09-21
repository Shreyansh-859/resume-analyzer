from nltk.corpus import wordnet
from nltk.wsd import lesk
from nltk.tokenize import word_tokenize


def perform_wsd(sentence, target_word):
    """
    Perform Word Sense Disambiguation
    using the Lesk algorithm.
    """

    tokens = word_tokenize(sentence)

    sense = lesk(tokens, target_word)

    return sense


def get_definition(sense):
    """
    Get the dictionary definition
    of a WordNet sense.
    """

    if sense is None:
        return "No sense found."

    return sense.definition()


def get_examples(sense):
    """
    Get example sentences associated
    with a WordNet sense.
    """

    if sense is None:
        return []

    return sense.examples()


def get_synonyms(word):
    """
    Find synonyms of a word using WordNet.
    """

    synonyms = set()

    synsets = wordnet.synsets(word)

    for synset in synsets:

        for lemma in synset.lemmas():

            synonyms.add(lemma.name())

    return sorted(synonyms)


def get_antonyms(word):
    """
    Find antonyms of a word using WordNet.
    """

    antonyms = set()

    synsets = wordnet.synsets(word)

    for synset in synsets:

        for lemma in synset.lemmas():

            for antonym in lemma.antonyms():

                antonyms.add(antonym.name())

    return sorted(antonyms)


def get_wordnet_relations(word):
    """
    Display basic WordNet semantic relations.
    """

    synsets = wordnet.synsets(word)

    relations = []

    for synset in synsets[:3]:

        relations.append({
            "synset": synset.name(),
            "definition": synset.definition(),
            "hypernyms": [
                item.name()
                for item in synset.hypernyms()
            ],
            "hyponyms": [
                item.name()
                for item in synset.hyponyms()
            ]
        })

    return relations