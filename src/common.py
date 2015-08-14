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

