from nlp.stemming import compare_stemming_lemmatization


words = [
    "running",
    "runs",
    "runner",
    "studies",
    "studying",
    "connected",
    "connection",
    "easily",
    "better"
]


results = compare_stemming_lemmatization(words)


print("\n==============================================")
print("       STEMMING vs LEMMATIZATION")
print("==============================================")

print(
    f"{'Original':<15}"
    f"{'Stemmed':<15}"
    f"{'Lemmatized':<15}"
)

print("-" * 45)

for result in results:

    print(
        f"{result['original']:<15}"
        f"{result['stemmed']:<15}"
        f"{result['lemmatized']:<15}"
    )