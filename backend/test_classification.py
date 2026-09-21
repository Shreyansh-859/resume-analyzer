from nlp.classification import (
    train_classifier,
    predict_sentiment
)


# ---------------------------------------
# TRAIN MODEL
# ---------------------------------------

model, accuracy, X_test, y_test, predictions = (
    train_classifier()
)


print("\n========================================")
print("NAIVE BAYES TEXT CLASSIFICATION")
print("========================================")


# ---------------------------------------
# TEST DATA
# ---------------------------------------

print("\n========================================")
print("TEST DATA PREDICTIONS")
print("========================================")

for text, actual, predicted in zip(
    X_test,
    y_test,
    predictions
):

    print("\nText:", text)
    print("Actual:", actual)
    print("Predicted:", predicted)


# ---------------------------------------
# ACCURACY
# ---------------------------------------

print("\n========================================")
print("CLASSIFICATION ACCURACY")
print("========================================")

print(
    f"Accuracy: {accuracy * 100:.2f}%"
)


# ---------------------------------------
# NEW TEXT PREDICTION
# ---------------------------------------

print("\n========================================")
print("NEW TEXT PREDICTION")
print("========================================")


new_texts = [
    "I really like this application",
    "This system is terrible",
    "The project is useful and interesting",
    "The application is difficult and confusing"
]


for text in new_texts:

    sentiment = predict_sentiment(
        model,
        text
    )

    print("\nText:", text)
    print("Predicted Sentiment:", sentiment)