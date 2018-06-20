"""
Basic spellcheck base on Peter Norvig's Algorithm

"""

import os
import pkgutil
import sys
import warnings

_ALPHABET = 'abcdefghijklmnopqrstuvwxyz'

# this is the bayesian dictionary, which is auto-populated using the comma-delimited list in `corpus.txt'
_DICTIONARY = {}


def update_dictionary(corpus):
    """
    populating the dictionary with the corpus entries
    """
    for line in corpus:
        name, val = line.split(",")
        val = int(val)
        _DICTIONARY[name] = val


def first_order_variants(word):
    """
    find the variants of a misspelled word
    """
    splits = [(word[:i], word[i:]) for i in range(len(word) + 1)]
    deletes = [a + b[1:] for a, b in splits if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in splits if len(b) > 1]
    replaces = [a + c + b[1:] for a, b in splits for c in _ALPHABET if b]
    inserts = [a + c + b for a, b in splits for c in _ALPHABET]
    return set(deletes + transposes + replaces + inserts)


def second_order_variants(word):
    "return second-order candidates"
    return set(e2 for e1 in first_order_variants(word) for e2 in first_order_variants(e1) if e2 in _DICTIONARY)


def known(*words):
    """
    Return all the words in *words which are in the dictionary
    """
    return set(w for w in words if w in _DICTIONARY)


def correct(word):
    """
    pick the 'best' repleacement for the misspelled word
    """
    candidates = known(word) or known(*first_order_variants(word)) or second_order_variants(word) or [word]
    return max(candidates, key=_DICTIONARY.get)


def guesses(word):
    """
    return all of the first order variants of the word
    """
    result = list(known(*first_order_variants(word)))
    result.sort()
    return result


def add(word, priority=4):
    _DICTIONARY[word.lower().strip()] = priority

# import initializations
#
# the dictionary is initialised
if sys.version_info.major >= 3:
    _corpus = (i.decode("utf-8") for i in pkgutil.get_data("spellchecker", "corpus.txt").splitlines())
else:
    _corpus = (i for i in pkgutil.get_data("spellchecker", "corpus.txt").splitlines())

update_dictionary(_corpus)
del _corpus

# try to load environment variable with a corpus file

if os.environ.get('spellchecker'):
    abs = os.path.abspath(os.path.expandvars(os.environ['spellchecker']))
    if os.path.exists(abs):
        with open(abs, 'rt') as user_dictionary:
            update_dictionary(user_dictionary)
    else:
        warnings.warn("could not find dictionary '{}'".format(abs))
