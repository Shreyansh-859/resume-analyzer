from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score


def create_dataset():
    """
    Create a small sentiment dataset.
    """

    texts = [
        "I really enjoyed this course",
        "The teacher explained everything clearly",
        "This project is very interesting",
        "I love this application",
        "The system works perfectly",
        "The user interface is excellent",
        "The lecture was informative",
        "I am happy with the result",
        "This is a useful project",
        "The application is easy to use",

        "I did not enjoy this course",
        "The explanation was confusing",
        "This project is very boring",
        "I hate this application",
        "The system does not work",
        "The user interface is terrible",
        "The lecture was disappointing",
        "I am unhappy with the result",
        "This project is useless",
        "The application is difficult to use"
    ]

    labels = [
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",
        "positive",

        "negative",
        "negative",
        "negative",
        "negative",
        "negative",
        "negative",
        "negative",
        "negative",
        "negative",
        "negative"
    ]

    return texts, labels


def train_classifier():
    """
    Train a Naive Bayes sentiment classifier.
    """

    texts, labels = create_dataset()

    X_train, X_test, y_train, y_test = train_test_split(
        texts,
        labels,
        test_size=0.25,
        random_state=42,
        stratify=labels
    )

    model = Pipeline([
        (
            "tfidf",
            TfidfVectorizer()
        ),
        (
            "classifier",
            MultinomialNB()
        )
    ])

    model.fit(X_train, y_train)

    predictions = model.predict(X_test)

    accuracy = accuracy_score(
        y_test,
        predictions
    )

    return model, accuracy, X_test, y_test, predictions


def predict_sentiment(model, text):
    """
    Predict the sentiment of new text.
    """

    prediction = model.predict([text])

    return prediction[0]