def minimum_edit_distance(source, target):
    """
    Calculate the Minimum Edit Distance between two strings.

    Operations:
    - Insertion
    - Deletion
    - Substitution
    """

    rows = len(source) + 1
    columns = len(target) + 1

    # Create the DP table
    dp = [[0 for _ in range(columns)] for _ in range(rows)]

    # Cost of converting source into an empty string
    for i in range(rows):
        dp[i][0] = i

    # Cost of converting empty string into target
    for j in range(columns):
        dp[0][j] = j

    # Fill the table
    for i in range(1, rows):
        for j in range(1, columns):

            if source[i - 1] == target[j - 1]:
                substitution_cost = 0
            else:
                substitution_cost = 1

            insertion = dp[i][j - 1] + 1
            deletion = dp[i - 1][j] + 1
            substitution = dp[i - 1][j - 1] + substitution_cost

            dp[i][j] = min(
                insertion,
                deletion,
                substitution
            )

    return dp[rows - 1][columns - 1]


def find_best_correction(word, vocabulary):
    """
    Find the vocabulary word with the smallest
    edit distance from the input word.
    """

    best_word = None
    best_distance = float("inf")

    for candidate in vocabulary:

        distance = minimum_edit_distance(
            word.lower(),
            candidate.lower()
        )

        if distance < best_distance:
            best_distance = distance
            best_word = candidate

    return best_word, best_distance