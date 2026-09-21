from nlp.ner_chunking import (
    named_entity_recognition,
    extract_entities,
    noun_phrase_chunking
)


sentence = (
    "Shreyansh works at Google in Mumbai. "
    "He studies Computer Engineering."
)


# ---------------------------------------
# NAMED ENTITY RECOGNITION
# ---------------------------------------

print("\n========================================")
print("NAMED ENTITY RECOGNITION")
print("========================================")

ner_tree = named_entity_recognition(sentence)

print("\nNER Tree:")
print(ner_tree)

print("\nTree Structure:")
ner_tree.pretty_print()


# ---------------------------------------
# EXTRACT ENTITIES
# ---------------------------------------

print("\n========================================")
print("EXTRACTED NAMED ENTITIES")
print("========================================")

entities = extract_entities(sentence)

for entity in entities:

    print(
        f"{entity['entity']:<25}"
        f" → {entity['type']}"
    )


# ---------------------------------------
# NOUN PHRASE CHUNKING
# ---------------------------------------

print("\n========================================")
print("NOUN PHRASE CHUNKING")
print("========================================")

chunk_tree = noun_phrase_chunking(sentence)

print("\nChunk Tree:")
print(chunk_tree)

print("\nTree Structure:")
chunk_tree.pretty_print()