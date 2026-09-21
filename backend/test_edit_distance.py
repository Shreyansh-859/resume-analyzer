from nlp.edit_distance import (
    minimum_edit_distance,
    find_best_correction
)


# -----------------------------------
# PART 1: Basic Edit Distance
# -----------------------------------

word1 = "kitten"
word2 = "sitting"

distance = minimum_edit_distance(word1, word2)

print("\n===================================")
print("MINIMUM EDIT DISTANCE")
print("===================================")

print("Word 1:", word1)
print("Word 2:", word2)
print("Edit Distance:", distance)


# -----------------------------------
# PART 2: Spelling Correction
# -----------------------------------

vocabulary = [
    "python",
    "machine",
    "learning",
    "developer",
    "database",
    "computer",
    "engineering",
    "natural",
    "language",
    "processing"
]


misspelled_words = [
    "pyhton",
    "machne",
    "developr",
    "databse"
]


print("\n===================================")
print("SPELLING CORRECTION")
print("===================================")

for word in misspelled_words:

    correction, distance = find_best_correction(
        word,
        vocabulary
    )

    print(
        f"{word} → {correction}"
        f"  (distance = {distance})"
    )