import pandas
import numpy
import Levenshtein
from sklearn import cluster
import Levenshtein


def _filter_known_correct_names(names):
    """Manually filter out known correct names from the provided list of names.

    The names list must contain tuples of the form

    ("lastname", "firstname", count)

    The filtered list is returned.

    The clustering strategy for finding the correct spelling of names has
    some flaws. The algorithm has a high precision, but not perfect - it will
    "correct" valid names in some cases. For example, using a max Levenshtein
    distance of 3 for the clustering will cause "Gord Brown" and "Lois Brown"
    to be considered the same, and "corrected".
    """


    names = filter(lambda x: x[0] == "Brown" and x[1] == "Gord", names)
    names = filter(lambda x: x[0] == "Brown" and x[1] == "Lois", names)
    return names


def find_correct_names(names):
    """Given a list of (lastname, firstname, count) tuples find the correct
    spelling of each name.

    We accomplish this in 2 steps:

    - Cluster the names so that different spellings are in the same cluster
    - Take the most frequent spelling from each cluster and consider it correct

    Return a dataframe containing the original and correct name on each row.
    """

    names = _filter_known_correct_names(names)

    df = pandas.DataFrame(names, columns=["lastname", "firstname", "count"])
    df["name"] = df["lastname"] + df["firstname"]

    # sort so the comparison width works as expected
    df = df.sort("name")

    df = _cluster_and_label(df, column="name", label="label")

    # find the index of the max count within each label
    correct = df.groupby("label")["count"].idxmax()
    correct = pandas.DataFrame(correct)
    correct.columns = ["maxcount_index"]
    correct["label"] = correct.index

    # add correct names
    correct["correct_firstname"] = correct.apply(
        lambda row: df.ix[row["maxcount_index"]]["firstname"],
        axis=1
    )
    correct["correct_lastname"] = correct.apply(
        lambda row: df.ix[row["maxcount_index"]]["lastname"],
        axis=1
    )

    # merge inner left to preserve index
    df = pandas.merge(df, correct, how="left", on="label")

    return df


def _cluster_and_label(df, column="name", label="label", cluster_dist=3):
    """Cluster a dataframe on the given column and add a "label" column"""

    # remove non-ascii characters, sklearn crashes
    df[column] = df[column].apply(
        lambda x: "".join([i for i in x if 0 < ord(i) < 127])
    )

    dist = _build_distance_matrix(df)

    dbscan = cluster.DBSCAN(
        eps=cluster_dist,
        metric="precomputed",
        min_samples=1
    )
    labels = dbscan.fit_predict(dist)

    df[label] = labels
    return df


def _build_distance_matrix(
        df,
        col="name",
        width=10,
        default_dist_value=10000
    ):
    dist = numpy.ndarray((len(df), len(df)))
    dist.fill(default_dist_value)

    for i, n in enumerate(df[col]):
        if i - width <= 0:
            lower = 0
        else:
            lower = i - width

        if i + width >= len(df[col]):
            upper = len(df[col]) - 1
        else:
            upper = i + width

        for j, m in enumerate(df[col][lower:upper + 1]):
            pos = j + lower
            d = Levenshtein.distance(n, m)
            dist[i][pos] = d

    return dist
