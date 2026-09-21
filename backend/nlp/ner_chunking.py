import nltk

from nltk import word_tokenize
from nltk import pos_tag
from nltk import ne_chunk


def named_entity_recognition(sentence):
    """
    Perform Named Entity Recognition using NLTK.
    """

    tokens = word_tokenize(sentence)

    tagged_words = pos_tag(tokens)

    named_entities = ne_chunk(tagged_words)

    return named_entities


def extract_entities(sentence):
    """
    Extract only named entities from the
    NER tree.
    """

    tree = named_entity_recognition(sentence)

    entities = []

    for item in tree:

        if hasattr(item, "label"):

            entity_name = " ".join(
                word for word, tag in item
            )

            entity_type = item.label()

            entities.append({
                "entity": entity_name,
                "type": entity_type
            })

    return entities


def noun_phrase_chunking(sentence):
    """
    Perform simple noun phrase chunking.
    """

    tokens = word_tokenize(sentence)

    tagged_words = pos_tag(tokens)

    grammar = r"""
        NP: {<DT>?<JJ>*<NN.*>+}
    """

    chunk_parser = nltk.RegexpParser(grammar)

    chunk_tree = chunk_parser.parse(tagged_words)

    return chunk_tree