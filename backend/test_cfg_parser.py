from nlp.cfg_parser import (
    top_down_parse,
    bottom_up_parse
)


sentence = "the smart student studies"


print("\n========================================")
print("SYNTACTIC PARSING USING CFG")
print("========================================")

print("\nSentence:")
print(sentence)


# ---------------------------------------
# TOP-DOWN PARSING
# ---------------------------------------

print("\n========================================")
print("TOP-DOWN PARSING")
print("========================================")

top_down_trees = top_down_parse(sentence)

if len(top_down_trees) == 0:
    print("No parse tree found.")
else:
    for tree in top_down_trees:
        print(tree)
        print("\nTree Structure:")
        tree.pretty_print()


# ---------------------------------------
# BOTTOM-UP PARSING
# ---------------------------------------

print("\n========================================")
print("BOTTOM-UP PARSING")
print("========================================")

bottom_up_trees = bottom_up_parse(sentence)

if len(bottom_up_trees) == 0:
    print("No parse tree found.")
else:
    for tree in bottom_up_trees:
        print(tree)
        print("\nTree Structure:")
        tree.pretty_print()


# ---------------------------------------
# COMPARISON
# ---------------------------------------

print("\n========================================")
print("TOP-DOWN vs BOTTOM-UP")
print("========================================")

print("Top-Down parse trees:",
      len(top_down_trees))

print("Bottom-Up parse trees:",
      len(bottom_up_trees))

if len(top_down_trees) > 0:
    print("\nTop-Down Parsing: SUCCESS")
else:
    print("\nTop-Down Parsing: FAILED")

if len(bottom_up_trees) > 0:
    print("Bottom-Up Parsing: SUCCESS")
else:
    print("Bottom-Up Parsing: FAILED")