"""
Pre-downloads all necessary NLTK datasets during build or deployment.
Run via: python setup_nltk.py
"""

import os
import ssl
import nltk

# Handle SSL certificate verification issues common in macOS / container environments
try:
    _create_unverified_https_context = ssl._create_unverified_context
except AttributeError:
    pass
else:
    ssl._create_default_https_context = _create_unverified_https_context

RESOURCES = [
    "punkt",
    "punkt_tab",
    "stopwords",
    "averaged_perceptron_tagger",
    "averaged_perceptron_tagger_eng",
    "maxent_ne_chunker",
    "maxent_ne_chunker_tab",
    "words",
    "wordnet",
    "omw-1.4",
]

def download_all():
    print("Pre-downloading NLTK datasets for production...")
    for res in RESOURCES:
        print(f"Downloading {res}...")
        try:
            nltk.download(res, quiet=False)
        except Exception as e:
            print(f"Error downloading {res}: {e}")
    print("All NLTK datasets verified.")

if __name__ == "__main__":
    download_all()
