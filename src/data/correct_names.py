import pandas
import numpy
import Levenshtein
from sklearn import cluster
import Levenshtein


def find_correct_names(names):
    """Given a list of (lastname, firstname, count) tuples find the correct
    spelling of each name.

    We accomplish this in 2 steps:

    - Cluster the names so that different spellings are in the same cluster
    - Take the most frequent spelling from each cluster and consider it correct

    Return a dataframe containing the original and correct name on each row.
    """

    df = pandas.DataFrame(names, columns=["lastname", "firstname", "count"])
    df["name"] = df["lastname"] + df["firstname"]

    df = _cluster_and_label(df, column="name", label="label")

    # find the index of the max count within each label
    correct = df.groupby("label")["count"].idxmax()
    correct = pandas.DataFrame(correct)
    correct.columns = ["maxcount_index"]
    correct["label"] = correct.index

    # add the correct name on each row
    # merge inner left to preserve index
    df = pandas.merge(df, correct, how="left", on="label")
    df["correct_firstname"] = df.apply(
        lambda row: df.ix[row["maxcount_index"]]["firstname"],
        axis=1
    )
    df["correct_lastname"] = df.apply(
        lambda row: df.ix[row["maxcount_index"]]["lastname"],
        axis=1
    )

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

    # sort so the comparison width works as expected
    df = df.sort([col])

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
