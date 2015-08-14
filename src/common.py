REPLACE = [
    "Right Hon.",
    "Hon.",
    "Right Honorable",
    "Honorable"
]


def clean_name(name):
    """Standard name-cleaning routine. Should accept any number of
    space-delimited words."""

    for i in REPLACE:
        name = name.replace(i, "")
    name = name.title()
    return name

