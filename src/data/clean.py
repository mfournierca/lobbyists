import re

import pandas as pd
import Levenshtein


PUNCTUATION = [
    ".",
    ","
]

REPLACE = [
    "the",
    "right",
    "rt",
    "hon",
    "honorable",
    "honourable",
    "mp",
    "pc"
]

SUB = ["^" + r + "\s+" for r in REPLACE]
SUB += ["\s+" + r + "\s+" for r in REPLACE]


def clean_name(name):
    """Clean the provided name. Capitalize properly, remove punctuation,
    titles and pronouns. """

    name = name.lower()
    name = name.strip()
    for p in PUNCTUATION:
        name = name.replace(p, "")
    for i in SUB:
        name = re.sub(i, "", name)
    name = name.title()
    return name


def clean_last_and_first_name(lastname, firstname):
    return clean_name(lastname), clean_name(firstname)

