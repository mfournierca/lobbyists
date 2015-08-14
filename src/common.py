REPLACE = [
    ".",
    " the ",
    " right ",
    " rt ",
    " hon ",
    " honorable "
 ]


def clean_name(name):
    """Standard name-cleaning routine. Should accept any number of
    space-delimited words."""

    name = name.lower()
    for i in REPLACE:
        name = name.replace(i, "")
    name = name.title()
    return name


def clean_last_and_first_name(lastname, firstname):
    lastname = clean_name(lastname)
    firstname = clean_name(firstname)
    if lastname == "Harper" and firstname in ["Stephen", "Stepen", "Steven"]:
        firstname = "Stephen"
    return lastname, firstname
