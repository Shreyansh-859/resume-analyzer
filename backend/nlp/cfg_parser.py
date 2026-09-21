import nltk
from nltk import CFG
from nltk.parse import RecursiveDescentParser
from nltk.parse import BottomUpChartParser


def create_grammar():
    """
    Create a small Context-Free Grammar.
    """

    grammar = CFG.fromstring("""
        S -> NP VP

        NP -> DT NN
        NP -> DT JJ NN

        VP -> V NP
        VP -> V

        DT -> 'the' | 'a'
        JJ -> 'smart' | 'good'
        NN -> 'student' | 'teacher' | 'book'
        V -> 'reads' | 'helps' | 'studies'
    """)

    return grammar


def top_down_parse(sentence):
    """
    Perform Top-Down parsing using
    Recursive Descent Parser.
    """

    grammar = create_grammar()

    parser = RecursiveDescentParser(grammar)

    tokens = sentence.lower().split()

    trees = list(parser.parse(tokens))

    return trees


def bottom_up_parse(sentence):
    """
    Perform Bottom-Up parsing using
    Chart Parser.
    """

    grammar = create_grammar()

    parser = BottomUpChartParser(grammar)

    tokens = sentence.lower().split()

    trees = list(parser.parse(tokens))

    return trees