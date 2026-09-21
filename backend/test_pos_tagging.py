from nlp.pos_tagging import (
    rule_based_pos_tagging,
    probabilistic_pos_tagging
)


sentence = (
    "The student developed a Python application "
    "using machine learning."
)


# ---------------------------------------
# RULE-BASED TAGGING
# ---------------------------------------

rule_results = rule_based_pos_tagging(sentence)


print("\n========================================")
print("RULE-BASED POS TAGGING")
print("========================================")

for word, tag in rule_results:
    print(f"{word:<15} → {tag}")


# ---------------------------------------
# PROBABILISTIC TAGGING
# ---------------------------------------

probabilistic_results = probabilistic_pos_tagging(
    sentence
)


print("\n========================================")
print("PROBABILISTIC POS TAGGING")
print("========================================")

for word, tag in probabilistic_results:
    print(f"{word:<15} → {tag}")
# ---------------------------------------
# ACCURACY EVALUATION
# ---------------------------------------

test_sentence = "The student developed software."

gold_standard = [
    ("The", "DT"),
    ("student", "NN"),
    ("developed", "VBD"),
    ("software", "NN"),
    (".", ".")
]


predicted = probabilistic_pos_tagging(test_sentence)


correct = 0

for predicted_item, gold_item in zip(
    predicted,
    gold_standard
):

    if predicted_item[1] == gold_item[1]:
        correct += 1


accuracy = (
    correct / len(gold_standard)
) * 100


print("\n========================================")
print("POS TAGGING ACCURACY")
print("========================================")

print("Correct tags:", correct)
print("Total tags:", len(gold_standard))
print(f"Accuracy: {accuracy:.2f}%")