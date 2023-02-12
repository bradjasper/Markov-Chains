#!/usr/bin/env python

"""
    Generate unique names using Markov Chains
"""

import string
import sys
from collections import defaultdict
import random


def weighted_choice(lst):
    n = random.uniform(0, 1)
    for item, weight in lst:
        if n < weight:
            break
        n = n - weight
    return item


def absolute_to_relative_weights(dictionary):
    total = float(sum(val for val in dictionary.values()))
    return dict((key, val / total) for key, val in dictionary.items())


def train(words):
    """Enter an array of words that we should train on, 
    return a probability dictionary """

    probabilities = defaultdict(int)
    acceptable = list(string.ascii_lowercase)
    acceptable.append(None)

    for word in words:
        l1 = None
        l2 = None
        for letter in word.lower():
            l1, l2 = l2, letter

            if l1 in acceptable and l2 in acceptable:
                probabilities[(l1, l2)] += 1
    return probabilities


def next_letter(probabilities, last=None):
    filtered = {}
    for pair, weight in probabilities.items():
        w1, w2 = pair
        if last == w1:
            filtered[w2] = weight
    if len(filtered):
        relative = absolute_to_relative_weights(filtered).items()
        return weighted_choice(relative)
    return None


def generate(probabilities, length=7, last=None):
    """Generate cool words from a probabilities dict"""

    word = []
    while len(word) != length:
        last = next_letter(probabilities, last)
        if not last:
            break
        word.append(last)
    return ''.join(word)


if __name__ == "__main__":

    # Train on crunchbase data
    words = open("crunchbase.txt").read().split()
    probabilities = train(words)

    for i in range(10):
        if len(sys.argv) == 2:
            base = sys.argv[1]
            word = base + generate(probabilities, last=base[-1], length=3)
            print(word)
        elif len(sys.argv) == 1:
            print(generate(probabilities, length=5))
        else:
            print("ERROR: Please enter either a single parameter or nothing")
