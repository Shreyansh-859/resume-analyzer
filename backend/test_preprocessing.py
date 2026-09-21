from nlp.preprocessing import preprocess_text, validate_script


text = """
I am a computer engineering student.
I have experience in Python and machine learning.
"""


# -------------------------------
# SCRIPT VALIDATION
# -------------------------------

script_result = validate_script(text)

print("\n========== SCRIPT VALIDATION ==========")
print(script_result)


# -------------------------------
# TOKENIZATION + STOP WORDS
# -------------------------------

tokens, filtered_tokens = preprocess_text(text)


print("\n========== ORIGINAL TEXT ==========")
print(text)

print("\n========== TOKENS ==========")
print(tokens)

print("\n========== AFTER STOP-WORD REMOVAL ==========")
print(filtered_tokens)