import re

REPLACE = [
    ".",
    " the ",
    " right ",
    " rt ",
    " hon ",
    " honorable ",
    " honourable ",
    " mp "
]

SUB = [
    "^the ",
    "^right ",
    "^rt ",
    "^hon ",
    "^honorable ",
    "^honourable ",
    "^mp "
]


def clean_name(name):
    """Standard name-cleaning routine. Should accept any number of
    space-delimited words."""

    name = name.lower()
    for i in REPLACE:
        name = name.replace(i, "")
    for i in SUB:
        name = re.sub(i, "", name)
    name = name.title()
    return name


def clean_last_and_first_name(lastname, firstname):
    lastname = clean_name(lastname)
    firstname = clean_name(firstname)
    if lastname == "Harper" and firstname in ["Stephen", "Stepen", "Steven"]:
        firstname = "Stephen"
    return lastname, firstname
